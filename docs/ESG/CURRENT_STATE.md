# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-28
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)
> 설계 문서: [full_plan.md](./full_plan.md)
> 아키텍처: [architecture.md](../../portfolio/ESG/architecture.md)

---

## 🟢 현재 단계

**핵심 기능 완료 + SmartThings IoT 전력 수집 운영 중 (Fly.io + Supabase + Vercel)**

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 서비스명 | 기숙사 세탁기 예약 서비스 |
| 한 줄 정의 | 기숙사생들이 세탁기 사용 가능 여부를 원격으로 보고 합리적으로 판단할 수 있도록 하는 앱 |
| 기술 스택 | React + TypeScript / FastAPI / PostgreSQL / Docker / Fly.io + Supabase + Vercel |
| 목적 | 과제 프로토타입 + 실제 배포 + 포트폴리오 |
| 인증 방식 | JWT + @hanyang.ac.kr 이메일 도메인 제한 + 6자리 OTP |

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
| 7. Docker Compose 로컬 실행 | ✅ | ✅ |
| 8. CI/CD (GitHub Actions → Fly.io + Vercel) | ✅ | ✅ |
| 9. 운영 고려사항 (rate limit, soft_reserve 중복 방지) | ✅ | — |
| 10. 이메일 인증 (@hanyang.ac.kr + 6자리 OTP) | ✅ | ✅ |
| 11. 대기 순번 실시간 표시 (WS queue_position_updated) | ✅ | ✅ |
| 12. 모바일 PWA (standalone + Fullscreen API) | — | ✅ |
| 13. 관리자 페이지 (세탁기 상태 변경) | ✅ | ✅ |
| 14. 비밀번호 / 아이디 변경 (설정 페이지) | ✅ | ✅ |
| 15. IoT 신호 수신 엔드포인트 | ✅ | — |
| 16. machine_status_logs 누적 | ✅ | — |
| 17. SmartThings 전력 polling (ADR-007) | ✅ | — |
| 18. machine_power_logs 누적 + 7일 자동 정리 | ✅ | — |
| 19. 관리자 전력 그래프 (24h, 60s 자동갱신) | ✅ | ✅ |
| 20. 전력 임계값 설정 (system_settings) | ✅ | — |

---

## 배포 구성

| 역할 | 플랫폼 | 비고 |
|------|--------|------|
| Backend (FastAPI + SmartThings polling) | Fly.io | `auto_stop_machines = false`, WebSocket 상시 가동 |
| Database (PostgreSQL) | Supabase | 무료 500MB |
| Frontend (React) | Vercel | CDN, SPA 라우팅 rewrites |

---

## API 엔드포인트 전체 목록

| Method | Path | 설명 | 인증 |
|--------|------|------|------|
| POST | `/auth/register` | 회원가입 (@hanyang.ac.kr 필수) | 불필요 |
| POST | `/auth/verify-email` | OTP 인증 → JWT 반환 | 불필요 |
| POST | `/auth/login` | 로그인 → JWT 반환 | 불필요 |
| PATCH | `/auth/password` | 비밀번호 변경 (현재 비번 검증) | 필요 |
| PATCH | `/auth/username` | 아이디 변경 → 새 JWT 반환 | 필요 |
| GET | `/machines` | 현재 모드 + 층별 상태 | 필요 |
| GET | `/machines/my-reservation` | 현재 사용자 활성 소프트 예약 | 필요 |
| POST | `/machines/request` | Mode B: 세탁기 1대 배정 | 필요 |
| POST | `/queue/join` | Mode C: 대기열 등록 | 필요 |
| DELETE | `/queue/leave` | 대기열 취소 | 필요 |
| POST | `/queue/accept` | Mode C: 5분 수락 대기 확정 | 필요 |
| GET | `/queue/status` | 대기 상태 조회 (새로고침 복원용) | 필요 |
| GET | `/admin/machines` | 전체 세탁기 목록 | admin |
| PATCH | `/admin/machines/{id}` | 세탁기 상태 변경 + 큐 알림 트리거 + status_log 기록 | admin |
| GET | `/admin/machines/{id}/power-history` | 전력 이력 조회 (최대 168h) | admin |
| GET | `/admin/settings` | 전력 임계값 조회 | admin |
| PATCH | `/admin/settings` | 전력 임계값 수정 | admin |
| POST | `/iot/machines/{id}/status` | IoT 신호 수신 (`is_running` bool) | Device Key |
| WS | `/ws` | 실시간 연결 | JWT 쿼리 파라미터 |

---

## 백엔드 파일 구조

| 파일 | 내용 |
|------|------|
| `app/models/user.py` | User ORM |
| `app/models/machine.py` | Machine + MachineStatusLog + MachinePowerLog ORM |
| `app/models/queue_entry.py` | QueueEntry ORM |
| `app/models/email_verification.py` | EmailVerification ORM |
| `app/models/system_settings.py` | SystemSettings ORM (key/value_float) |
| `app/core/security.py` | bcrypt 해싱, JWT 생성/검증 |
| `app/core/dependencies.py` | get_current_user, get_admin_user |
| `app/core/ws_manager.py` | ConnectionManager 싱글톤, gender 채널 분리 |
| `app/core/email.py` | Gmail SMTP — send_verification_email() |
| `app/repositories/machine_repo.py` | count_available, soft_reserve, release_expired, get_by_id, set_status, seed |
| `app/repositories/machine_status_log_repo.py` | create (상태 변경 이력 기록) |
| `app/repositories/machine_power_log_repo.py` | create, get_history, delete_old (7일) |
| `app/repositories/queue_repo.py` | join, leave, get_position, get_next_waiter, reset_expired_notifications |
| `app/repositories/system_settings_repo.py` | get_float, set_float |
| `app/repositories/user_repo.py` | get_by_username, create |
| `app/services/auth_service.py` | 토큰 생성/검증, register, login |
| `app/services/machine_service.py` | Mode 계산, get_dashboard |
| `app/services/queue_service.py` | 대기열 비즈니스 로직 |
| `app/services/smartthings_client.py` | SmartThings API — get_power_w(device_id) |
| `app/services/smartthings_poller.py` | poll_loop() — 백그라운드 태스크, ADR-007 적응형 주기 |
| `app/api/ws.py` | JWT 검증 → 초기 상태 → 30s keepalive, _notify_queue_and_broadcast |
| `app/api/auth.py` | register, verify-email, login, PATCH password/username |
| `app/api/machines.py` | GET /machines, GET /machines/my-reservation, POST /machines/request |
| `app/api/queue.py` | POST /queue/join, DELETE /queue/leave, POST /queue/accept, GET /queue/status |
| `app/api/admin.py` | GET/PATCH /admin/machines, GET power-history, GET/PATCH /admin/settings |
| `app/api/iot.py` | POST /iot/machines/{id}/status (X-Device-Key 인증) |
| `app/main.py` | lifespan (seed + smartthings_poller 시작), logging 레벨 설정 |

---

## 프론트엔드 파일

| 파일 | 내용 |
|------|------|
| `src/api/auth.ts` | register, login, verifyEmail, changePassword, changeUsername |
| `src/api/machines.ts` | getMachines, requestMachine, getMyReservation |
| `src/api/queue.ts` | joinQueue, leaveQueue, acceptOffer, getQueueStatus |
| `src/api/admin.ts` | adminGetMachines, adminSetStatus, adminGetPowerHistory |
| `src/hooks/useWebSocket.ts` | 3s 자동 재연결, WsMessage 타입 분기 |
| `src/pages/GenderSelectPage.tsx` | 성별 선택 + 구역 안내 |
| `src/pages/LoginPage.tsx` | 로그인/회원가입 탭 + 비밀번호 보기 토글 |
| `src/pages/VerifyEmailPage.tsx` | 6자리 코드 입력 |
| `src/pages/DashboardPage.tsx` | Mode A/B/C, 소프트예약 복원, 5분 수락 대기, 실시간 순번 |
| `src/pages/SettingsPage.tsx` | 비밀번호/아이디 변경, 로그아웃 |
| `src/pages/AdminPage.tsx` | 층별 기기 상태 토글 + PowerGraph (recharts, 24h, 60s 갱신) |
| `src/store/authStore.ts` | Zustand (user, gender, setUser, logout) + localStorage persist |
| `src/store/machineStore.ts` | Zustand (data, loading, error) |
| `public/manifest.json` | PWA manifest (display: standalone) |

---

## 환경변수

| 변수 | 위치 | 설명 |
|------|------|------|
| `DATABASE_URL` | Fly.io Secrets | Supabase PostgreSQL (Direct URL) |
| `SECRET_KEY` | Fly.io Secrets | JWT 서명 키 |
| `GMAIL_USER` | Fly.io Secrets | OTP 이메일 발신 계정 |
| `GMAIL_APP_PASSWORD` | Fly.io Secrets | Gmail 앱 비밀번호 |
| `IOT_DEVICE_KEY` | Fly.io Secrets | IoT REST 엔드포인트 인증 키 |
| `CORS_ORIGINS` | Fly.io Secrets | Vercel 프론트 URL |
| `SMARTTHINGS_PAT` | GitHub Secret → Fly.io Secrets | SmartThings Personal Access Token |
| `SMARTTHINGS_DEVICE_01` | GitHub Secret → Fly.io Secrets | SmartThings 장치 ID (machine_id=1) |
| `VITE_API_URL` | Vercel Environment | 백엔드 API URL |

> `SMARTTHINGS_DEVICE_XX` 패턴: 접미사 숫자 = machine_id (예: `SMARTTHINGS_DEVICE_02` → machine_id=2)
> GitHub Actions CD가 `flyctl secrets set`으로 자동 전파.

---

## 알려진 이슈 / 해결된 버그

| 이슈 | 상태 |
|------|------|
| 대시보드 로딩 무한 (WS 업데이트마다 깜박임) | ✅ 수정 |
| Resend 무료 플랜 외부 도메인 발송 불가 | ✅ Gmail SMTP 전환 |
| WsMessage TypeScript 타입 누락 | ✅ 수정 |
| 모바일 horizontal overflow | ✅ boxSizing: border-box |
| Mode B 배정 후 결과 즉시 사라짐 | ✅ modeBResult 부모로 lift up |
| Mode C 대기 중 모드 전환 시 대기 소멸 | ✅ queueInfo 부모로 lift up |
| 어드민 available 전환 시 큐 알림 미발송 | ✅ _notify_queue_and_broadcast 연결 |
| SmartThings polling INFO 로그 안 보임 | ✅ logging.getLogger("app").setLevel(INFO) |
| polling 루프 DB 오류 시 전체 중단 | ✅ 각 단계 독립 try/except |
| `flyctl secrets deploy` 실패 (머신 없음) | ✅ `flyctl secrets set` 사용 |
| polling 적응형 주기 역전 (Mode A가 가장 빠름) | ✅ 수정 (C=60s, B=120s, A=480s) |
| 상태 버튼 너비 불일치 (사용 중 ↔ 이용 가능) | ✅ minWidth: 4.8rem 고정 |
| React StrictMode WS 1006 disconnect | 미해결 (두 번째 연결 정상, 프로덕션 무관) |

---

## 알려진 제약 / 향후 과제

| 항목 | 내용 |
|------|------|
| `in_use` 자동 해제 | 없음 — 어드민 수동 또는 IoT REST 엔드포인트 (`/iot`) 필요 |
| IoT 실제 장치 연결 | SmartThings polling 구현 완료, 실제 기기 부착은 별도 작업 |
| ConnectionManager | 단일 인스턴스 — 다중 서버 시 Redis pub/sub 필요 (현재 Fly.io 1대) |
| PWA Push Notification | WebSocket 인앱 알림만 — 백그라운드 미지원 |
| 통계 UI | machine_status_logs + machine_power_logs 누적 중, 시간대별 혼잡도 UI 미구현 |
| 전력 임계값 UI | 어드민 UI 없음, API만 존재 (`PATCH /admin/settings`) |