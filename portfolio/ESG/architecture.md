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
│   │  /auth/*    │  │  /ws/{gender}│                │
│   │  /machines/*│  │  30s keepalive│               │
│   │  /admin/*   │  │  ConnectionMgr│               │
│   │  /iot/*     │  └──────────────┘                │
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

Queue
├── id (PK)
├── user_id (FK → User)
├── gender
└── created_at

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
    │      available       │◄──── 10분 만료 (Lazy Expiration)
    │   (사용 가능)         │
    └──────┬──────┬────────┘
           │ B모드 │ A모드
           │배정   │직접예약
           ▼       ▼
    ┌──────────────────────┐
    │   soft_reserved      │
    │   (소프트 예약, 10분) │
    └──────────────────────┘
```

---

## 모드 결정 로직

```python
# 성별별 available 기기 수에 따라 모드 결정
available_count = count(machines where status='available' and gender=gender)

if available_count >= THRESHOLD_A:   # 여유 (기본값: 3)
    mode = 'A'  # 직접 선택
elif available_count >= THRESHOLD_B: # 경쟁 (기본값: 1)
    mode = 'B'  # 시스템 배정
else:
    mode = 'C'  # 대기열
```

---

## WebSocket 이벤트 흐름

```
사용자 연결: ws://backend/ws/{gender}?token={jwt}
                │
                ▼
         ConnectionManager
         gender별 그룹 관리

세탁기 상태 변경 시:
    1. DB 업데이트
    2. Queue 확인 → 첫 대기자에게 queue_notify 이벤트
    3. 전체 브로드캐스트 → machines_updated 이벤트

이벤트 타입:
    machines_updated: { type, mode, machines, floors }
    queue_notify:     { type, message, position }
```

### WS Keepalive (30초)

```python
try:
    await asyncio.wait_for(ws.receive_text(), timeout=30.0)
except asyncio.TimeoutError:
    pass

# 30초마다 자동 실행
released = machine_repo.release_expired(db)
if released:
    await _notify_queue_and_broadcast(db, gender)
```

만료된 소프트 예약을 30초마다 자동 해제.

---

## 대기열 알림 흐름

```
_notify_queue_and_broadcast(db, gender)
    │
    ├─ 1. 만료 예약 해제 (release_expired)
    │
    ├─ 2. 대기열 첫 번째 사용자 확인
    │      있음 → WS queue_notify 이벤트 전송
    │              → 해당 사용자: Mode B 화면으로 전환
    │      없음 → 스킵
    │
    └─ 3. 전체 브로드캐스트 (machines_updated)
           → 모든 연결된 사용자 화면 갱신
```

---

## 배포 파이프라인

```
GitHub push (develope branch)
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
| DB ORM | SQLAlchemy | Python 생태계 표준, 마이그레이션 |
| 실시간 | WebSocket | SSE/폴링 대비 양방향, 저지연 |
| 배포 (BE) | Fly.io | WS 장기 연결, Cold Start 없음 |
| 배포 (FE) | Vercel | CDN, SPA rewrites, GitHub 연동 |
| DB | Supabase | 관리형 PostgreSQL, 연결 풀 내장 |
| 이메일 | Gmail SMTP | 외부 도메인 발송, 무료 500통/일 |
