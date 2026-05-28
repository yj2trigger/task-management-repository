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
│                                                     │
│   ┌─────────────────────────────────────────────┐  │
│   │  SmartThings Poller (백그라운드 태스크)        │  │
│   │  ADR-007 적응형 주기 (60~900s)               │  │
│   │  → MachinePowerLog 기록                       │  │
│   └─────────────────────────────────────────────┘  │
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
│              SmartThings Cloud                      │
│   GET /devices/{id}/status → powerMeter.power.value │
│   인증: Bearer SMARTTHINGS_PAT                      │
└─────────────────────────────────────────────────────┘

    +
┌─────────────────────────────────────────────────────┐
│              IoT 장치 (REST, 선설계 완료)              │
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
| PATCH | `/admin/machines/{id}` | 어드민: 기기 상태 변경 + status_log 기록 |
| GET | `/admin/machines/{id}/power-history` | 어드민: 전력 이력 (최대 168h) |
| GET | `/admin/settings` | 어드민: 전력 임계값 조회 |
| PATCH | `/admin/settings` | 어드민: 전력 임계값 수정 |
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
├── gender_restriction (male/female/NULL=공용)
├── status (available/in_use/soft_reserved/broken)
├── reserved_by_user_id (FK → User, nullable)
└── reserved_until (nullable, TIMESTAMPTZ)

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
└── expires_at (TIMESTAMPTZ)

MachineStatusLog                    ← 상태 변경 이력 (통계용)
├── id (PK)
├── machine_id (FK → Machine)
├── previous_status (nullable)      ← 이전 상태
├── status                          ← 변경된 상태
├── changed_by_user_id (FK → User, nullable)
├── source (admin/iot/system)
├── is_running (nullable, bool)     ← IoT 신호 원본값
├── changed (bool)                  ← 실제로 상태가 바뀌었는지
└── changed_at (TIMESTAMPTZ, index) ← 통계 핵심

MachinePowerLog                     ← 전력 이력 (SmartThings polling)
├── id (PK)
├── machine_id (FK → Machine)
├── power_w (float)                 ← 측정된 전력값 (W)
└── recorded_at (TIMESTAMPTZ, index)← 기록 시각

SystemSettings                      ← 시스템 설정 key/value
├── key (PK, varchar)               ← 예: "power_threshold_w"
└── value_float (float, nullable)
```

---

## SmartThings Polling (ADR-007)

```
app startup (lifespan)
    └─ asyncio.create_task(smartthings_poller.poll_loop())

poll_loop():
    while True:
        mode = get_current_mode(db, gender)    ← DB에서 Mode 조회
        threshold = system_settings.get_float(db, "power_threshold_w", 100.0)
        interval = _calc_interval(mode)        ← ADR-007 주기 결정

        for machine_id, device_id in device_map.items():
            power_w = await smartthings_client.get_power_w(device_id)
            machine_power_log_repo.create(db, machine_id, power_w)
            is_running = power_w >= threshold
            if state_changed:
                await _apply_state_change(machine_id, is_running)

        await asyncio.sleep(interval)

ADR-007 적응형 주기 (KST 기준):
    야간 (22:00–07:00) → 900s
    낮 Mode A (4대 이상)  → 480s
    낮 Mode B (1~3대)     → 120s
    낮 Mode C (0대)       → 60s   ← 이용 가능 적을수록 높은 빈도

환경변수:
    SMARTTHINGS_PAT        = Personal Access Token
    SMARTTHINGS_DEVICE_01  = device_id (machine_id=1)
    SMARTTHINGS_DEVICE_02  = device_id (machine_id=2)  (필요시 추가)

SmartThings API:
    GET https://api.smartthings.com/v1/devices/{device_id}/status
    → components.main.powerMeter.power.value (float, W)
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
           │배정   │
           ▼
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
{ in_queue: True, is_notified: True, accept_until: "2025-05-26T10:05:00Z" }

# 대기열 없음
{ in_queue: False }
```

---

## 모드 결정 로직

```python
available_count = count(machines where status='available' and gender=gender)

if available_count >= 4:   mode = 'A'
elif available_count >= 1: mode = 'B'
else:                      mode = 'C'
```

---

## WebSocket 이벤트 흐름

```
사용자 연결: wss://backend/ws?token={jwt}
                │
                ▼
         ConnectionManager
         gender별 그룹 + user_id→WebSocket 매핑

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
released = machine_repo.release_expired(db)
expired_user_ids = queue_repo.reset_expired_notifications(db, gender)
for uid in expired_user_ids:
    await manager.send_to_user(uid, gender, {"type": "queue_offer_expired", ...})
if released or expired_user_ids:
    await _notify_queue_and_broadcast(db, gender)
```

---

## C모드 대기열 전체 흐름

```
세탁기 가용 → _notify_queue_and_broadcast()
    │
    ├─ 1. 대기열 첫 번째 사용자 조회 (status=waiting)
    ├─ 2. 기기 soft_reserve(5분) + entry status → notified
    ├─ 3. WS queue_offer 이벤트 발송 (accept_until 포함)
    │      프론트: 노란 배너 + 카운트다운 + 수락 버튼
    ├─ 4A. 수락 (POST /queue/accept)
    │       → reserved_until 10분으로 연장
    │       → queue entry 삭제
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

---

## Datetime Timezone 처리

```typescript
// 백엔드 DateTime(timezone=True) → PostgreSQL TIMESTAMPTZ → ISO 8601 with +00:00
// JS new Date()가 UTC로 정확히 파싱됨

// SQLite 테스트 환경에서는 naive → guard 필요
function asUtc(s: string): Date {
  return new Date(s.endsWith('Z') || s.includes('+') ? s : s + 'Z')
}
```

---

## 배포 파이프라인

```
GitHub push (main branch)
    │
    ├─ test-backend   (pytest, SQLite)
    ├─ test-frontend  (vitest)
    │
    └─ deploy-backend (needs: both tests pass)
           ├─ flyctl secrets set SMARTTHINGS_PAT SMARTTHINGS_DEVICE_01
           └─ flyctl deploy --remote-only --strategy=immediate

Vercel: GitHub 연동 자동 배포
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
| SmartThings | asyncio + httpx | FastAPI 비동기 생태계 통합 |
| 배포 (BE) | Fly.io | WS 장기 연결, Cold Start 없음 |
| 배포 (FE) | Vercel | CDN, SPA rewrites, GitHub 연동 |
| DB | Supabase | 관리형 PostgreSQL, 연결 풀 내장 |
| 이메일 | Gmail SMTP | 외부 도메인 발송, 무료 500통/일 |
