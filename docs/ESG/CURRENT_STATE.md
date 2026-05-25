# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-25
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)
> 전체 설계 문서: [full_plan.md](./full_plan.md)

---

## 🟢 현재 단계

**핵심 기능 전체 완료 + 운영 중 (Fly.io + Supabase + Vercel)**

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

---

## 배포 구성

| 역할 | 플랫폼 | 비고 |
|------|--------|------|
| Backend (FastAPI) | Fly.io | `auto_stop_machines = false`, WebSocket 상시 가동 |
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
| POST | `/machines/request` | Mode B: 세탁기 1대 배정 | 필요 |
| POST | `/queue/join` | Mode C: 대기열 등록 | 필요 |
| DELETE | `/queue/leave` | 대기열 취소 | 필요 |
| GET | `/queue/status` | 대기 상태 조회 (새로고침 복원용) | 필요 |
| GET | `/admin/machines` | 전체 세탁기 목록 | admin |
| PATCH | `/admin/machines/{id}` | 세탁기 상태 변경 + 큐 알림 트리거 | admin |
| POST | `/iot/machines/{id}/status` | IoT 신호 수신 (`is_running` bool) | Device Key |
| WS | `/ws` | 실시간 연결 | JWT 쿼리 파라미터 |

---

## 백엔드 파일 구조

| 파일 | 내용 |
|------|------|
| `app/models/user.py` | User ORM (id, username, password_hash, gender, role, email, is_verified) |
| `app/models/machine.py` | Machine ORM (floor, machine_number, status, gender_restriction, soft_reserve 필드) |
| `app/models/queue_entry.py` | QueueEntry ORM (user_id, gender, status, created_at) |
| `app/models/email_verification.py` | EmailVerification ORM (email, code, expires_at) |
| `app/core/security.py` | bcrypt 해싱, JWT 생성/검증 |
| `app/core/dependencies.py` | get_current_user, get_admin_user (role 체크) |
| `app/core/ws_manager.py` | ConnectionManager 싱글톤, gender 채널 분리, user_id 타겟 알림 |
| `app/core/email.py` | Gmail SMTP — send_verification_email() |
| `app/repositories/machine_repo.py` | count_available, soft_reserve, release_expired(lazy), get_by_id, set_status, seed(17대) |
| `app/repositories/queue_repo.py` | join, leave, get_position, get_next_waiter, get_all_waiting, count_waiting |
| `app/api/ws.py` | JWT 검증 → 초기 상태 전송 → 30s keepalive + _notify_queue_and_broadcast, broadcast_queue_positions |
| `app/api/auth.py` | register, verify-email, login, PATCH password, PATCH username |
| `app/api/machines.py` | GET /machines, POST /machines/request |
| `app/api/queue.py` | POST /queue/join, DELETE /queue/leave, GET /queue/status |
| `app/api/admin.py` | GET /admin/machines, PATCH /admin/machines/{id} (available 시 큐 알림 연동) |
| `app/api/iot.py` | POST /iot/machines/{id}/status (X-Device-Key 인증) |

---

## 프론트엔드 파일

| 파일 | 내용 |
|------|------|
| `src/api/auth.ts` | register, login, verifyEmail, changePassword, changeUsername |
| `src/api/machines.ts` | getMachines, requestMachine |
| `src/api/queue.ts` | joinQueue, leaveQueue, getQueueStatus |
| `src/api/admin.ts` | adminGetMachines, adminSetStatus |
| `src/hooks/useWebSocket.ts` | 3s 자동 재연결, WsMessage 타입 (machines_updated / queue_notify / queue_position_updated) |
| `src/pages/GenderSelectPage.tsx` | 성별 선택 + 구역 안내 문구 |
| `src/pages/LoginPage.tsx` | 로그인/회원가입 탭 전환 + 비밀번호 표시 토글 |
| `src/pages/VerifyEmailPage.tsx` | 6자리 코드 입력 → 인증 완료 |
| `src/pages/DashboardPage.tsx` | Mode A/B/C, modeBResult/queueInfo 상위 상태 관리, 실시간 순번, 설정 버튼 |
| `src/pages/SettingsPage.tsx` | 비밀번호/아이디 변경 토글 폼, 로그아웃 |
| `src/pages/AdminPage.tsx` | 층별 기기 상태 토글 (admin role 필요) |
| `src/store/authStore.ts` | Zustand (user, gender, setUser, logout) + localStorage persist |
| `src/store/machineStore.ts` | Zustand (data, loading, error) |
| `public/manifest.json` | PWA manifest (display: standalone) |

---

## 알려진 이슈 / 해결된 버그

| 이슈 | 상태 |
|------|------|
| 대시보드 로딩 무한 (WS 업데이트마다 깜박임) | ✅ 수정 — data 있으면 loading 화면 미표시 |
| Resend 무료 플랜 외부 도메인 발송 불가 | ✅ Gmail SMTP 전환 |
| Vercel working-directory 이중 적용 | ✅ 제거로 해결 |
| WsMessage TypeScript 타입 누락 (queue_position_updated) | ✅ 수정 |
| 모바일 horizontal overflow | ✅ boxSizing: border-box 적용 |
| Mode B 배정 후 결과 즉시 사라짐 | ✅ modeBResult 상위 상태로 올림 |
| Mode C 대기 중 모드 B 전환 시 대기 상태 소멸 | ✅ queueInfo 상위 상태로 올림 |
| Mode B/C 뷰 동시 표시 (대기 중 + 사용 버튼) | ✅ queueInfo 있으면 Mode B/A 뷰 숨김 |
| 어드민 available 전환 시 큐 알림 미발송 | ✅ _notify_queue_and_broadcast 연결 |
| React StrictMode WS 1006 disconnect | 미해결 (두 번째 연결 정상 동작) |

---

## 알려진 제약 / 향후 과제

| 항목 | 내용 |
|------|------|
| `in_use` 자동 해제 | 없음 — 어드민 수동 또는 IoT 연동 필요 |
| IoT 실제 연동 | 엔드포인트 준비 완료, 장치 연결 대기 |
| Alembic 마이그레이션 | `create_all()` 사용 중 — 스키마 변경 이력 없음 |
| PWA Push Notification | WebSocket 인앱 알림만 — 백그라운드 미지원 |
| 통계 | `machine_status_logs` 미구현 |
