# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-30
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)
> 전체 설계 문서: [full_plan.md](./full_plan.md)
> 상세 기술 명세 (API · 파일 구조 · 배포): [portfolio/ESG/architecture.md](../../portfolio/ESG/architecture.md)

---

## 현재 단계

**핵심 기능 전체 완료 + 운영 중 (Fly.io NRT + Supabase + Vercel) + GitHub Actions IoT 릴레이 운영 중**

---

## 핵심 비즈니스 로직: 3-Mode State Machine

| 모드 | 조건 | 동작 |
|------|------|------|
| Mode A | 4대 이상 | 층별 이용 가능 세탁기 수 표시 |
| Mode B | 1~3대 | 버튼 누르면 1:1 세탁기 위치 안내 + 10분 소프트 예약 |
| Mode C | 0대 | 대기열 등록 → 빈 자리 발생 시 순서대로 알림 + 실시간 순번 표시 |

---

## 구현 진행 현황

| 기능 | 백엔드 | 프론트엔드 |
|------|--------|----------|
| 1. 프로젝트 골격 + Docker | ✅ | ✅ |
| 2. 성별 선택 | — | ✅ |
| 3. 인증 (JWT register/login) | ✅ | ✅ |
| 4. 세탁기 상태 조회 (Mode A/B/C) | ✅ | ✅ |
| 5. Mode B 소프트 예약 + Mode C 대기열 | ✅ | ✅ |
| 6. WebSocket 실시간 연결 | ✅ | ✅ |
| 7. Docker Compose 로컈 실행 | ✅ | ✅ |
| 8. CI/CD (GitHub Actions → Fly.io + Vercel) | ✅ | ✅ |
| 9. 운영 고려사항 (rate limit, soft_reserve 중복 방지) | ✅ | — |
| 10. 이메일 인증 (@hanyang.ac.kr + 6자리 OTP) | ✅ | ✅ |
| 11. 대기 순번 실시간 표시 (WS queue_position_updated) | ✅ | ✅ |
| 12. 모바일 PWA (standalone + Fullscreen API) | — | ✅ |
| 13. 관리자 페이지 (세탁기 상태 변경 + 전력 그래프) | ✅ | ✅ |
| 14. 비밀번호 / 아이디 변경 (설정 페이지) | ✅ | ✅ |
| 15. IoT 신호 수신 엔드포인트 (power_w + poll_tick 포함) | ✅ | — |
| 16. GitHub Actions IoT 릴레이 (12초 주기, 분당 5회) | ✅ | — |
| 17. DB Quota 관리 (전력 로그 30일 보존) | ✅ | — |
| 18. 소프트 예약 → 이용 중 자동 전환 + machine_started 알림 | ✅ | ✅ |
| 19. IoT 감지 임계값 히스테리시스 (10W 시작 / 5W 정지) | ✅ | — |
| 20. PollingInfoBar (12초 주기 표시 + 다음 갱신 카운트다운) | — | ✅ |
| 21. 관리자 페이지 WS 실시간 + 10초 폴링 자동 갱신 | ✅ | ✅ |
| 22. broken 상태 IoT 자동 전환 차단 | ✅ | — |
| 23. 관리자 그래프 롤링 24h 윈도우 (자정 전환 버그 해결) | — | ✅ |
| 24. 로컈 릴레이 스크립트 (project/relay/) | ✅ | — |

---

## IoT 연동 아키텍처 (GitHub Actions 릴레이)

**평패나이:** SmartThings 서버가 Fly.io 전체 datacenter IP 차단 (지역 무관, SIN/NRT/IAD 모두 차단확인). 로컈 IP(한국망)로는 정상 접근 가능.

**해결:** GitHub Actions 러너에서 SmartThings API 호출 → ESG IoT 엔드포인트로 중계.

```
[GitHub Actions, 12초 주기]
  └─ SmartThings API 폴링 (GitHub IP 허용)
  └─ POST /iot/machines/{id}/status
       ├─ power_w 로그 저장 (machine_power_logs)
       ├─ 상태 전환 (available ↔ in_use)
       └─ poll_tick WS 브로드쾐스트 → 사용자 카운트다운 동기화
```

| 항목 | 내용 |
|------|------|
| 연동 기기 | 세탁기 1대 (`SMARTTHINGS_DEVICE_01`) |
| 릴레이 주기2 | 12초 (5분 워크플로 내 25회) |
| SmartThings rate limit | 250 req/분 (토큰당) — 1대 기준 5 req/분 시 2% 사용 |
| 50대 확장 시 | 분당 5회 × 50대 = 250 req/분 한도 도달 |
| 시작 임계값 | 10W (급수 밸브 15~30W 캐치) |
| 정지 임계값 | 5W (사이클 중간 정지 3~15W 오판단 방지) |
| 전력 로그 보존 | 30일 |
| 로컈 스크립트 | `project/relay/relay.py` — 노트북 백업용 |
| Fly.io 리전 | NRT (Tokyo) — 한국 사용자 지연시간 최적화 |

**SSOT 원칙:**
- threshold: `fly.toml [env]` 원본, config.py 로컈 dev 기본값
- DB system_settings 미사용 (제거)
- 서버 SmartThings polling 제거, GitHub Actions만 사용

---

## 해결된 버그 (2026-05-29~30)

| 이슈 | 상태 |
|------|------|
| soft_reserved + 전력 낙음 → available 강제 전환 버그 | ✅ 예약 유지로 수정 |
| _last_states 또는 DB 불일치 시 상태 교정 안 됨 | ✅ IoT 엔드포인트에서 정상 처리 |
| AdminPage THRESHOLD_W=100 하드코딩 | ✅ GET /admin/settings 동적 로드 |
| fly.toml [env] POWER_THRESHOLD_W=100 오버라이드 | ✅ 10으로 수정 (SSOT 교정) |
| AdminPage 머신 목록 배포 후 자동 갱신 안 됨 | ✅ WS 구독 + 10초 폴링 추가 |
| SmartThings Fly.io datacenter IP 전체 차단 | ✅ GitHub Actions 릴레이로 우회 |
| 관리자 그래프 자정 전환 시 데이터 공백 | ✅ 롤링 24h 윈도우로 수정 |
| IoT 엔드포인트 power_w 미저장 (그래프 공백) | ✅ power_w 수신 시 로그 저장 추가 |
| poll_tick 동기화 대기 중 표시 | ✅ IoT 엔드포인트 호출 시 poll_tick 브로드쾐스트 |
| broken 기기 IoT 전력 감지 시 in_use 자동 전환 | ✅ broken 상태 보호 추가 |
| GitHub Actions Node.js 20 디프리케이션 | ✅ 24로 업그레이드 |
| React StrictMode WS 1006 disconnect | 미해결 (두 번째 연결 정상 동작) |

---

## 알려진 제약 / 향후 과제

| 항목 | 내용 |
|------|------|
| IoT 기기 확장 | 현재 1대 연동 — `SMARTTHINGS_DEVICE_02` 등 추가 + GitHub Secrets 등록으로 확장 |
| in_use 자동 해제 | 없음 — IoT 전력 낙음 시에만 available 전환 |
| PWA Push Notification | WebSocket 인앱 알림만 — 백그라운드 미지원 |
| DB Quota 관리 | Supabase 500MB 무료 한도 — 전력 로그 30일 자동 정리 적용 중 |
| 통계 분석 | machine_power_logs 수집 중 — 요일·시간대별 펨러링 기능 미구현 |
| Alembic 마이그레이션 | 미적용 (`create_all()` 사용 중) |
| 릴레이 실패 시 | GitHub Actions 6분 타임아웃 초과 가능성 — 50대 확장 시 병렬 요청 공학 필요 |
