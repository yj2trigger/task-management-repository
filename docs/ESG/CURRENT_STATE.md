# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-25
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)

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

---

## 배포 구성

| 역할 | 플랫폼 | 비고 |
|------|--------|------|
| Backend (FastAPI) | Fly.io | `auto_stop_machines = false`, WebSocket 상시 가동 |
| Database (PostgreSQL) | Supabase | 무료 500MB |
| Frontend (React) | Vercel | CDN, SPA 라우팅 rewrites |

---

## 알려진 이슈

| 이슈 | 현상 | 상태 |
|------|------|------|
| 대시보드 로딩 무한 | WS machines_updated마다 loading=true → 화면 깜박임 | ✅ 수정 완료 |
| Resend 무료 플랜 제한 | 외부 도메인 발송 불가 | ✅ Gmail SMTP로 전환 완료 |
| Vercel URL 경로 이중 적용 | cd.yml working-directory 충돌 | ✅ working-directory 제거로 해결 |

---

## 현재 백엔드 파일 구조

| 파일 | 내용 |
|------|------|
| `app/models/user.py` | User ORM (id, username, password_hash, gender, role, email, is_verified) |
| `app/models/machine.py` | Machine ORM (floor, machine_number, status, gender_restriction, soft_reserve 필드) |
| `app/models/queue_entry.py` | QueueEntry ORM (user_id, gender, status, created_at, notified_at, expires_at) |
| `app/models/email_verification.py` | EmailVerification ORM (email, code, expires_at) |
| `app/core/security.py` | bcrypt 해싱, JWT 생성/검증 |
| `app/core/dependencies.py` | HTTPBearer → get_current_user |
| `app/core/ws_manager.py` | ConnectionManager 싱글톤, gender 채널 분리, user_id 타겟 알림 |
| `app/core/email.py` | Gmail SMTP — send_verification_email() |
| `app/repositories/machine_repo.py` | count_available, soft_reserve, release_expired(lazy), seed(17대) |
| `app/repositories/queue_repo.py` | join, leave, get_position, get_next_waiter, get_all_waiting, count_waiting |
| `app/api/ws.py` | JWT 검증 → 초기 상태 전송 → 30s keepalive loop + broadcast_queue_positions |
| `app/api/auth.py` | POST /auth/register, /auth/verify-email, /auth/login |
| `app/api/queue.py` | POST /queue/join, DELETE /queue/leave |

---

## 현재 프론트엔드 파일

| 파일 | 내용 |
|------|------|
| `src/api/auth.ts` | register(+email), login, verifyEmail |
| `src/api/machines.ts` | getMachines, requestMachine |
| `src/api/queue.ts` | joinQueue, leaveQueue (응답에 total 포함) |
| `src/hooks/useWebSocket.ts` | 3s 자동 재연결 |
| `src/pages/GenderSelectPage.tsx` | 성별 선택 + 구역 안내 문구 |
| `src/pages/LoginPage.tsx` | 로그인/회원가입 탭 전환 + 비밀번호 표시 토글 |
| `src/pages/VerifyEmailPage.tsx` | 6자리 코드 입력 → 인증 완료 |
| `src/pages/DashboardPage.tsx` | Mode A/B/C, 대기열 순번 실시간, queue_notify 배너 |
| `src/store/machineStore.ts` | Zustand (data, loading, error) |
| `public/manifest.json` | PWA manifest (display: standalone) |

---

## 플레이스홀더 (미구현, 계획됨)

| 항목 | 내용 |
|------|------|
| Alembic 마이그레이션 | `create_all()` 대체 — 스키마 변경 이력 관리 |
| 관리자 페이지 | `/admin/machines/{id}` PATCH — 세탁기 상태 직접 변경 |
| PWA Push Notification | WebSocket 인앱 알림 → 백그라운드 알림 전환 |
| IoT 연동 | LG 세탁기 실제 상태 연동 (현재 더미데이터) |
| 통계 | `machine_status_logs` 테이블 + 시간대별 혼잡도 API |

---

## 🚨 현재 리스크

- IoT(LG 세탁기) 연동 방식 미확정 → 더미데이터로 우선 진행
- React StrictMode + WS 1006 disconnect: StrictMode 이중 마운트로 첫 WS 즉시 종료됨 (두 번째 연결은 정상)
- Supabase DB 스키마 변경 시 `create_all()`로는 ALTER 불가 → 수동 SQL 필요 (Alembic 미도입)
