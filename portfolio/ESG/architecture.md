# 시스템 아키텍처

## 전체 구성

```
┌─────────────────────────────────────────────────────┐
│                    클라이언트                         │
│   React + TypeScript + Zustand                      │
│   Vercel (CDN, SPA rewrites)                        │
└──────────────┬──────────────────────────────────────┘
               │ HTTPS REST + WSS
               │
┌──────────────▼──────────────────────────────────────┐
│                    백엔드                             │
│   FastAPI (Python 3.12)                             │
│   Fly.io (Docker, 256MB, auto_stop=false)           │
│                                                     │
│   ┌─────────────┐  ┌──────────────┐                │
│   │  REST API   │  │  WebSocket   │                │
│   │  /auth/*    │  │  /ws         │                │
│   │  /machines/*│  │  30s keepalive│               │
│   │  /queue/*   │  │  ConnectionMgr│               │
│   │  /admin/*   │  └──────────────┘                │
│   │  /iot/*     │                                   │
│   └─────────────┘                                   │
└──────────────┬──────────────────────────────────────┘
               │ SQLAlchemy + psycopg2
               │
┌──────────────▼──────────────────────────────────────┐
│                   데이터베이스                         │
│   PostgreSQL (Supabase)                             │
│   연결 풀링 내장, 500MB 무료                          │
└─────────────────────────────────────────────────────┘

    +
┌─────────────────────────────────────────────────────┐
│              IoT 장치 (예정)                          │
│   HTTP POST /iot/machines/{id}/status               │
│   X-Device-Key 헤더 인증                             │
└─────────────────────────────────────────────────────┘
```

---

## 주요 API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/machines` | 성별별 세탁기 현황 + 모드 |
| GET | `/machines/my-reservation` | 현재 사용자의 활성 소프트 예약 |
| POST | `/machines/request` | Mode B 세탁기 배정 요청 |
| POST | `/queue/join` | 대기열 등록 |
| DELETE | `/queue/leave` | 대기열 취소 |
| GET | `/queue/status` | 대기열 현황 조회 (waiting/notified 모두 반영) |
| POST | `/queue/accept` | 5분 수락 대기 → 수락 확정 |
| POST | `/auth/register` | 회원가입 (OTP 발송) |
| POST | `/auth/verify-email` | 이메일 OTP 인증 |
| POST | `/auth/login` | 로그인 |
| PATCH | `/auth/password` | 비밀번호 변경 |
| PATCH | `/auth/username` | 아이디 변경 |
| GET | `/admin/machines` | 어드민: 전체 기기 목록 |
| PATCH | `/admin/machines/{id}` | 어드민: 기기 상태 변경 |
| POST | `/iot/machines/{id}/status` | IoT 장치 상태 수신 |

---

## 데이터 모델

```
User
├── id (PK)
├── username (unique)
├── email (unique, nullable — 기존 계정 호환)
├── hashed_password
├── gender (male/female)
├── is_admin
└── is_verified

Machine
├── id (PK)
├── floor
├── machine_number
├── gender (male/female)
├── status (available/in_use/soft_reserved)
├── reserved_by_user_id (FK → User, nullable)
└── reserved_until (nullable)

QueueEntry
├── id (PK)
├── user_id (FK → User, unique)
├── gender
├── status (waiting / notified / expired)
├── created_at               ← 순위 정렬 기준
├── notified_at (nullable)   ← offer 발송 시각
└── expires_at (nullable)    ← 5분 수락 마감

EmailVerification
├── id (PK)
├── email
├── code (6자리)
└── expires_at
```

---

## 세탁기 상태 전이

```
         어드민/IoT 신호
         (is_running=true)
              │
    ┌─────────▼──────────┐
    │      in_use        │
    │   (세탁 중)         │
    └─────────┬──────────┘
              │ 완료 (is_running=false)
              │ 또는 어드민 수동 변경
              ▼
    ┌──────────────────────┐
    │      available       │◄─── Lazy Expiration (5분/10분 만료)
    │   (사용 가능)         │
    └──────┬──────┬────────┘
           │ B모드 │ A모드
           │배정   │직접예약
           ▼       ▼
    ┌──────────────────────────────────────────┐
    │            soft_reserved                 │
    │  5분 (C모드 offer hold) / 10분 (확정 예약) │
    └──────────────────────────────────────────┘
```

---

## QueueEntry 상태 전이

```
waiting → notified  (offer 발송, 5분 hold)
notified → [삭제]   (수락 → 소프트 예약 10분 확정)
notified → waiting  (5분 만료 → created_at=now → 맨 뒤)
waiting → [삭제]    (대기 취소)
```

### GET /queue/status 응답

```python
# waiting 상태
{ in_queue: True, queue_position: 2, total: 5, is_notified: False }

# notified 상태 (offer 수신, 수락 대기 중)
{ in_queue: True, is_notified: True, accept_until: "2025-05-26T10:05:00" }

# 대기열 없음
{ in_queue: False }
```

`get_entry()` (status 무관) 조회 → notified 포함 모든 상태 반영.  
페이지 새로고침 시 프론트엔드가 이 응답으로 pendingOffer / queueInfo 복원.

---

## 모드 결정 로직

```python
available_count = count(machines where status='available' and gender=gender)

if available_count >= 4:   mode = 'A'  # 직접 선택
elif available_count >= 1: mode = 'B'  # 시스템 배정
else:                      mode = 'C'  # 대기열
```

---

## WebSocket 이벤트 흐름

```
사용자 연결: wss://backend/ws?token={jwt}
                │
                ▼
         ConnectionManager
         gender별 그룹 관리

이벤트 타입:
    machines_updated      { type, mode, floors }
                          → 전체 브로드캐스트
    queue_offer           { type, machine, accept_until }
                          → 특정 사용자에게 (5분 수락 요청)
    queue_offer_expired   { type, message }
                          → 5분 미수락 사용자에게
    queue_position_updated{ type, position, total }
                          → 대기 중인 각 사용자에게
```

### WS Keepalive (30초)

```python
# 30초마다 자동 실행
released = machine_repo.release_expired(db)          # 5분/10분 만료 기기 해제
expired_user_ids = queue_repo.reset_expired_notifications(db, gender)
for uid in expired_user_ids:
    await manager.send_to_user(uid, gender, {"type": "queue_offer_expired", ...})
if released or expired_user_ids:
    await _notify_queue_and_broadcast(db, gender)    # 다음 대기자에게 offer
```

---

## C모드 대기열 전체 흐름

```
세탁기 가용 → _notify_queue_and_broadcast()
    │
    ├─ 1. 대기열 첫 번째 사용자 조회 (status=waiting)
    │
    ├─ 2. 기기 soft_reserve(5분) + entry status → notified
    │
    ├─ 3. WS queue_offer 이벤트 발송 (accept_until 포함)
    │      프론트: 노란 배너 + 카운트다운 + 수락 버튼
    │
    ├─ 4A. 수락 (POST /queue/accept)
    │       → reserved_until 10분으로 연장
    │       → queue entry 삭제
    │       → 프론트: 초록 배너 + 10분 카운트다운
    │
    └─ 4B. 5분 미수락 (WS keepalive 감지)
            → 기기 available 복귀
            → entry status=waiting, created_at=now (맨 뒤)
            → WS queue_offer_expired 발송
            → 다음 대기자에게 새 offer
```

---

## 소프트 예약 복원

```typescript
// DashboardPage 마운트 시
getMyReservation(token).then((res) => {
  if (res.active && res.assigned_machine && res.reserved_until) {
    setActiveReservation({ machine: res.assigned_machine, reserved_until: res.reserved_until })
  }
})
```

React state는 새로고침 시 소멸 → 서버 API로 복원.  
`reserved_until` 까지 카운트다운 표시, 만료 시 자동 소멸.

---

## Datetime Timezone 처리

```typescript
// 백엔드 DateTime 컬럼이 timezone 없이 직렬화됨
// → JS new Date()가 로컬(KST)로 해석 → 9시간 오차
// → asUtc() 헬퍼로 UTC 강제 지정

function asUtc(s: string): Date {
  return new Date(s.endsWith('Z') || s.includes('+') ? s : s + 'Z')
}
```

---

## 배포 파이프라인

```
GitHub push (main branch)
    │
    ├─ test-backend   (pytest)
    ├─ test-frontend  (tsc --noEmit + vite build)
    │
    └─ deploy-backend (needs: both tests pass)
           └─ flyctl deploy --remote-only

Vercel: GitHub 연동 자동 배포 (별도 CD 불필요)
```

---

## 기술 선택 요약

| 계층 | 기술 | 선택 이유 |
|------|------|----------|
| Frontend | React + TypeScript | 타입 안전성, 컴포넌트 재사용 |
| 상태관리 | Zustand | Redux 대비 보일러플레이트 없음 |
| Backend | FastAPI | 비동기 WS 지원, 자동 OpenAPI 문서 |
| DB ORM | SQLAlchemy | Python 생태계 표준 |
| 실시간 | WebSocket | SSE/폴링 대비 양방향, 저지연 |
| 배포 (BE) | Fly.io | WS 장기 연결, Cold Start 없음 |
| 배포 (FE) | Vercel | CDN, SPA rewrites, GitHub 연동 |
| DB | Supabase | 관리형 PostgreSQL, 연결 풀 내장 |
| 이메일 | Gmail SMTP | 외부 도메인 발송, 무료 500통/일 |

---

## 백엔드 파일 구조

| 파일 | 내용 |
|------|------|
| `app/models/user.py` | User ORM (id, username, password_hash, gender, role, email, is_verified) |
| `app/models/machine.py` | Machine ORM (floor, machine_number, status, gender_restriction, soft_reserve 필드) |
| `app/models/queue_entry.py` | QueueEntry ORM (user_id, gender, status, created_at, notified_at, expires_at) |
| `app/models/email_verification.py` | EmailVerification ORM (email, code, expires_at) |
| `app/core/security.py` | bcrypt 해싱, JWT 생성/검증 |
| `app/core/dependencies.py` | get_current_user, get_admin_user (role 체크) |
| `app/core/ws_manager.py` | ConnectionManager 싱글톤, gender 채널 분리, user_id 타겟 알림 |
| `app/core/email.py` | Gmail SMTP — send_verification_email() |
| `app/repositories/machine_repo.py` | count_available, soft_reserve, release_expired(lazy), get_by_id, set_status, seed(17대) |
| `app/repositories/queue_repo.py` | join, leave, get_position, get_next_waiter, get_all_waiting, count_waiting |
| `app/api/ws.py` | JWT 검증 → 초기 상태 전송 → 30s keepalive + _notify_queue_and_broadcast, broadcast_queue_positions |
| `app/api/auth.py` | register, verify-email, login, PATCH password, PATCH username |
| `app/api/machines.py` | GET /machines, POST /machines/request, GET /machines/my-reservation |
| `app/api/queue.py` | POST /queue/join, DELETE /queue/leave, GET /queue/status, POST /queue/accept |
| `app/api/admin.py` | GET /admin/machines, PATCH /admin/machines/{id} (available 시 큐 알림 연동) |
| `app/api/iot.py` | POST /iot/machines/{id}/status (X-Device-Key 인증) |

---

## 프론트엔드 파일 구조

| 파일 | 내용 |
|------|------|
| `src/api/auth.ts` | register, login, verifyEmail, changePassword, changeUsername |
| `src/api/machines.ts` | getMachines, requestMachine, getMyReservation |
| `src/api/queue.ts` | joinQueue, leaveQueue, getQueueStatus, acceptOffer |
| `src/api/admin.ts` | adminGetMachines, adminSetStatus |
| `src/hooks/useWebSocket.ts` | 3s 자동 재연결, WsMessage 타입 (machines_updated / queue_notify / queue_position_updated / queue_offer / queue_offer_expired) |
| `src/pages/GenderSelectPage.tsx` | 성별 선택 + 구역 안내 문구 |
| `src/pages/LoginPage.tsx` | 로그인/회원가입 탭 전환 + 비밀번호 표시 토글 |
| `src/pages/VerifyEmailPage.tsx` | 6자리 코드 입력 → 인증 완료 |
| `src/pages/DashboardPage.tsx` | Mode A/B/C, modeBResult/queueInfo/pendingOffer 상위 상태 관리, 실시간 순번, 수락 배너 |
| `src/pages/SettingsPage.tsx` | 비밀번호/아이디 변경 토글 폼, 로그아웃 |
| `src/pages/AdminPage.tsx` | 층별 기기 상태 토글 (admin role 필요) |
| `src/store/authStore.ts` | Zustand (user, gender, setUser, logout) + localStorage persist |
| `src/store/machineStore.ts` | Zustand (data, loading, error) |
| `public/manifest.json` | PWA manifest (display: standalone) |
