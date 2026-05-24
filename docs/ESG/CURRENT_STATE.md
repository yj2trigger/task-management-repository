# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-24
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)

---

## 🔵 현재 단계

**구현 8단계 완료 (CI/CD 워크플로우) → Railway 수동 연결 + 구현 9단계(운영) 대기**

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 서비스명 | 기숙사 세탁기 예약 서비스 |
| 한 줄 정의 | 기숙사생들이 세탁기 사용 가능 여부를 원격으로 보고 합리적으로 판단할 수 있도록 하는 앱 |
| 기술 스택 | React + TypeScript / FastAPI / PostgreSQL / Docker / Railway |
| 목적 | 과제 프로토타입 + 실제 배포 + 포트폴리오 |
| 인증 방식 | JWT (username/password) — 프로토타입용. 향후 카카오 OAuth 전환 예정 |

---

## 핵심 비즈니스 로직: 3-Mode State Machine

| 모드 | 조건 | 동작 |
|------|------|------|
| Mode A | 4대 이상 | 층별 이용 가능 세탁기 수 표시 |
| Mode B | 1~3대 | 버튼 누르면 1:1 세탁기 위치 안내 + 10분 소프트 예약 |
| Mode C | 0대 | 대기열 등록 → 빈 자리 발생 시 순서대로 알림 |

---

## 구현 진행 현황

| 기능 | 백엔드 | 프론트엔드 |
|------|--------|----------|
| 1. 프로젝트 골격 + Docker | ✅ 완료 | ✅ 완료 |
| 2. 성별 선택 | — | ✅ 완료 |
| 3. 인증 (JWT register/login) | ✅ 완료 | ✅ 완료 |
| 4. 세탁기 상태 조회 (Mode A/B/C) | ✅ 완료 | ✅ 완료 |
| 5. Mode B 소프트 예약 + Mode C 대기열 | ✅ 완료 | ✅ 완료 |
| 6. WebSocket 실시간 연결 | ✅ 완료 | ✅ 완료 |
| 7. Docker Compose 로컬 실행 | ✅ 완료 | ✅ 완료 |
| 8. CI/CD (GitHub Actions → Railway) | ✅ 완료 | ✅ 완료 |
| 9. 운영 고려사항 (rate limit 등) | ⏳ 대기 | — |

---

## 알려진 이슈

| 이슈 | 현상 | 상태 |
|------|------|------|
| 대시보드 로딩 무한 | 회원가입 후 `loading: true` 미해제 | ✅ 수정 완료 |

---

## 플레이스홀더 (미구현, 계획됨)

| 항목 | 내용 |
|------|------|
| 카카오 OAuth | 1인 다계정 방지. `User`에 `kakao_id` 컬럼, `/auth/kakao` 엔드포인트 |
| 관리자 페이지 | `/admin/machines/{id}` PATCH — 세탁기 상태 직접 변경 |
| Rate limiting | `slowapi` (9단계) |
| soft_reserve 재요청 방지 | user당 active reserve 1개 제한 |
| PWA Push Notification | WebSocket 인앱 알림 → 백그라운드 알림 전환 |
| IoT 연동 | LG 세탁기 실제 상태 연동 (현재 더미데이터) |

---

## 구현 3~7단계 완료 내용 (2026-05-24)

### Backend
| 파일 | 내용 |
|------|------|
| `app/models/user.py` | User ORM (id, username, password_hash, gender, role) |
| `app/models/machine.py` | Machine ORM (floor, machine_number, status, gender_restriction, soft_reserve 필드) |
| `app/models/queue_entry.py` | QueueEntry ORM (user_id, gender, status, created_at, notified_at, expires_at) |
| `app/core/security.py` | bcrypt 해싱, JWT 생성/검증 (python-jose) |
| `app/core/dependencies.py` | HTTPBearer → get_current_user |
| `app/core/ws_manager.py` | ConnectionManager 싱글톤, gender 채널 분리, user_id 타겟 알림 |
| `app/repositories/machine_repo.py` | count_available, soft_reserve, release_expired(lazy), seed(17대) |
| `app/repositories/queue_repo.py` | join, leave, get_position, get_next_waiter |
| `app/api/ws.py` | JWT 검증 → accept → 초기 상태 전송 → 30s keepalive loop |
| `app/main.py` | lifespan에 seed() 추가 |

### Frontend
| 파일 | 내용 |
|------|------|
| `src/api/auth.ts` | register, login |
| `src/api/machines.ts` | getMachines, requestMachine |
| `src/api/queue.ts` | joinQueue, leaveQueue |
| `src/hooks/useWebSocket.ts` | 3s 자동 재연결, machines_updated / queue_notify 처리 |
| `src/pages/LoginPage.tsx` | 로그인/회원가입 탭 전환 UI |
| `src/pages/DashboardPage.tsx` | Mode A/B/C 뷰, 대기열 알림 배너 |
| `src/store/machineStore.ts` | Zustand (data, loading, error) |

### Infra
- `docker-compose.yml`: db + backend + frontend 3컨테이너
- `.env.example` → `.env` 로컬 생성 필요
- `backend/Dockerfile`: python:3.11-slim, psycopg2-binary
- `frontend/Dockerfile`: node:20-alpine, npm run dev --host

---

## 🚨 현재 리스크

- IoT(LG 세탁기) 연동 방식 미확정 → 더미데이터로 우선 진행
- React StrictMode + WS 1006 disconnect: StrictMode 이중 마운트로 첫 WS 즉시 종료됨 (두 번째 연결은 정상)
- 대시보드 loading 무한 버그 수정 중

---

## 상세 설계 문서

- `full_plan.md` (ESG 레포) ← 1~9단계 설계 전체
- `dev_log.md` (ESG 레포) ← 구현 사고 기록, 에러 해결 과정, 플레이스홀더 목록
