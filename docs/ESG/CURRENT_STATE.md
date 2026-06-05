# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-30
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)
> 전체 설계 문서: [full_plan.md](./full_plan.md)
> 상세 기술 명세 (API · 파일 구조 · 배포): [portfolio/ESG/architecture.md](../../portfolio/ESG/architecture.md)

---

## 현재 단계

**핵심 기능 전체 완료 + 운영 중 (Fly.io NRT + Supabase + Vercel)**

**IoT 릴레이:** GitHub Actions `workflow_dispatch` 기반, cron-job.org 외부 트리거 방식으로 전환 예정

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
| 13. 관리자 페이지 (세탁기 상태 + 전력 그래프 롤링 24h) | ✅ | ✅ |
| 14. 비밀번호 / 아이디 변경 (설정 페이지) | ✅ | ✅ |
| 15. IoT 엔드포인트 (power_w + poll_tick 포함) | ✅ | — |
| 16. GitHub Actions IoT 릴레이 (12초 주기) | ✅ | — |
| 17. DB Quota 관리 (전력 로그 30일 보존) | ✅ | — |
| 18. 소프트 예약 → 이용 중 자동 전환 + machine_started 알림 | ✅ | ✅ |
| 19. IoT 감지 임계값 히스테리시스 (10W 시작 / 5W 정지) | ✅ | — |
| 20. PollingInfoBar (12초 주기 단일 표시) | — | ✅ |
| 21. 관리자 페이지 WS 실시간 + 10초 폴링 자동 갱신 | ✅ | ✅ |
| 22. broken 상태 IoT 자동 전환 차단 | ✅ | — |
| **23. cron-job.org 외부 트리거** | 특 미완료 | — |

---

## IoT 연동 아키텍처

### 현재 운영 방식

```
[GitHub Actions, workflow_dispatch 기반]
  └─ cron-job.org가 5분마다 GitHub API 호출 → 워크플로우 트리거 (예정)
  └─ 워크플로우 실행: SmartThings 폴링 (12초 × 25회)
       ├─ power_w 로그 저장
       ├─ 상태 전환 (available ↔ in_use)
       └─ poll_tick WS 브로드쾐스트
```

| 항목 | 내용 |
|------|------|
| 연동 기기 | 세탁기 1대 (`SMARTTHINGS_DEVICE_01`) |
| 릴레이 주기 | 12초 (5분 워크플로우 내 25회) |
| SmartThings rate limit | 250 req/분 — 50대 확장 시도 한도 유지 |
| 시작 임계값 | 10W |
| 정지 임계값 | 5W |
| Fly.io 리전 | NRT (Tokyo) — 한국 사용자 지연시간 최적화 |

### 트리거 전환 이유

| 방식 | 트리거 주체 | 신뢰도 | 비고 |
|---|---|---|---|
| GitHub `schedule` | GitHub 내부 스케줄러 | 낙음 | 수시간 지연·누락 확인됨 |
| cron-job.org + `workflow_dispatch` | 외부 크론 서비스 | 높음 | 분 단위 정확, 무료 |

**SSOT 원칙:** threshold는 `fly.toml [env]` 원본. config.py는 로컈 dev 기본값.

### cron-job.org 설정 계획

1. GitHub PAT 발급 (스코프: `workflow`)
2. cron-job.org 가입 → 크론 생성
   - URL: `https://api.github.com/repos/yj2trigger/ESG/actions/workflows/relay.yml/dispatches`
   - Method: POST
   - 주기: 5분
   - Headers: `Authorization: Bearer <PAT>`, `Content-Type: application/json`
   - Body: `{"ref": "main"}`
3. relay.yml에서 `schedule` 트리거 제거 (`workflow_dispatch`만 유지)

---

## 해결된 버그 (2026-05-29~30)

| 이슈 | 상태 |
|------|------|
| soft_reserved + 전력 낙음 → available 강제 전환 버그 | ✅ |
| DB/in-memory 상태 불일치 시 DB 교정 안 됨 | ✅ |
| AdminPage THRESHOLD_W=100 하드코딩 | ✅ |
| fly.toml [env] POWER_THRESHOLD_W=100 오버라이드 | ✅ (SSOT 교정) |
| SmartThings Fly.io datacenter IP 차단 | ✅ GitHub Actions 릴레이로 우회 |
| 관리자 그래프 자정 전환 데이터 공백 | ✅ 롤링 24h 윈돈우 |
| IoT power_w 미저장 | ✅ 수신 시 로그 저장 추가 |
| broken 기기 IoT 자동 전환 | ✅ 보호 추가 |
| relay 워크플로우 timeout 6분 초과 | ✅ 8분으로 연장 + pip 쾐시 |
| GitHub `schedule` 트리거 신뢰 불가 | 교체 예정 (cron-job.org) |
| 테스트 settings 전역 오염 | ✅ autouse reset fixture + 키 통일 |
| React StrictMode WS 1006 disconnect | 미해결 |

---

## 알려진 제약 / 향후 과제

| 항목 | 내용 |
|------|------|
| **cron-job.org 연동** | 미완료 — GitHub `schedule` 대체하여 relay 실행 안정성 확보 필요 |
| IoT 기기 확장 | 1대 연동 — `SMARTTHINGS_DEVICE_02` + GitHub Secrets 추가로 확장 |
| in_use 자동 해제 | 없음 — IoT 전력 낙음 시에만 available 전환 |
| PWA Push Notification | WebSocket 인앱 알림만 — 백그라운드 미지원 |
| DB Quota 관리 | 전력 로그 30일 자동 정리 적용 중 |
| 통계 분석 | machine_power_logs 수집 중 — 기능 미구현 |
| Alembic 마이그레이션 | 미적용 (`create_all()` 사용 중) |
