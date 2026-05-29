# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-30
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)
> 전체 설계 문서: [full_plan.md](./full_plan.md)
> 상세 기술 명세 (API · 파일 구조 · 배포): [portfolio/ESG/architecture.md](../../portfolio/ESG/architecture.md)

---

## 현재 단계

**핵심 기능 전체 완료 + 운영 중 (Fly.io + Supabase + Vercel) + SmartThings IoT 부분 연동 중**

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
| 15. IoT 신호 수신 엔드포인트 | ✅ | — |
| 16. SmartThings 연동 (PAT + 주기적 전력 polling) | ✅ | — |
| 17. DB Quota 관리 (전력 로그 30일 보존) | ✅ | — |
| 18. 소프트 예약 → 이용 중 자동 전환 + machine_started 알림 | ✅ | ✅ |
| 19. IoT 감지 임계값 히스테리시스 (10W 시작 / 5W 정지) | ✅ | — |
| 20. per-machine 스케줄러 (우선 3대 fast / 나머지 slow) | ✅ | — |
| 21. PollingInfoBar (IoT 감지 주기 + 다음 갱신 카운트다운) | — | ✅ |
| 22. 관리자 페이지 WS 실시간 + 10초 폴링 자동 갱신 | ✅ | ✅ |
| 23. broken 상태 IoT 자동 전환 차단 | ✅ | — |

---

## IoT 연동 현황 (SmartThings)

**플랫폼:** Samsung SmartThings (PAT 방식, Fly.io 시크릿)

| 항목 | 내용 |
|------|------|
| 연동 기기 | 세탁기 1대 (`SMARTTHINGS_DEVICE_1`) |
| 시작 임계값 | 10W (급수 밸브 15~30W 캐치) |
| 정지 임계값 | 5W (사이클 중간 정지 3~15W 오판단 방지) |
| Polling 기본 주기 | 120초 (일반) / 60초 (우선 기기) |
| 우선 기기 로직 | Mode A: 층별 유일 available 우선, 부족 시 다른 available로 채움 |
| | Mode B: available 세탁기 자체 fast |
| | Mode C: soft_reserved 세탁기 fast |
| 전력 로그 보존 | 30일 |
| 현재 이슈 | PAT 인증 오류 간헐적 발생 — Fly.io secret 갱신 필요 |

**SSOT 원칙:** threshold는 `fly.toml [env]`가 원본. config.py는 로컈 dev 기본값. DB system_settings 미사용.

---

## 해결된 버그 (2026-05-29~30)

| 이슈 | 상태 |
|------|------|
| soft_reserved + 전력 낙음 → available 강제 전환 버그 | ✅ 예약 유지로 수정 |
| _last_states 또는 DB 불일치 시 상태 교정 안 됨 | ✅ 항상 _apply_state_change 호출로 수정 |
| AdminPage THRESHOLD_W=100 하드코딩 | ✅ GET /admin/settings 동적 로드로 수정 |
| fly.toml [env] POWER_THRESHOLD_W=100 오버라이드 | ✅ 10으로 수정 (SSOT 교정) |
| AdminPage 머신 목록 배포 후 자동 갱신 안 됨 | ✅ WS 구독 + 10초 폴링 추가 |
| SmartThings 타임아웃 10초 초과 시 복구 불가 | ✅ 30초로 연장 |
| broken 기기 IoT 전력 감지 시 in_use 자동 전환 | ✅ broken 상태 보호 추가 |
| GitHub Actions Node.js 20 디프리케이션 | ✅ 24로 업그레이드 |
| 대시보드 로딩 무한 (이전에 해결) | ✅ data 있으면 loading 화면 미표시 |
| React StrictMode WS 1006 disconnect | 미해결 (두 번째 연결 정상 동작) |

---

## 알려진 제약 / 향후 과제

| 항목 | 내용 |
|------|------|
| SmartThings PAT 안정성 | 401 오류 간헐적 발생 — PAT 유효기한 없음이나 Fly.io secret 번것 수동 교체 필요 |
| IoT 기기 확장 | 현재 1대 연동 — `SMARTTHINGS_DEVICE_2` 등 추가로 확장 가능 |
| in_use 자동 해제 | 없음 — IoT 전력 낙음 시에만 available 전환 |
| PWA Push Notification | WebSocket 인앱 알림만 — 백그라운드 미지원 |
| DB Quota 관리 | Supabase 500MB 무료 한도 — 전력 로그 30일 자동 정리 적용 중 |
| 통계 분석 | machine_power_logs 수집 중 — 요일·시간대별 펨러링 기능 미구현 |
| Alembic 마이그레이션 | 미적용 (`create_all()` 사용 중) |
