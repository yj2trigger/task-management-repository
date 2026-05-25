# ADR-003: 소프트 예약 만료 처리 — Lazy Expiration 채택

## 상태
채택됨 (2025-05-24)

## 컨텍스트

Mode B/C에서 세탁기를 10분간 소프트 예약(`soft_reserved`)한 후
미사용 시 자동으로 `available` 복귀 + 대기열 다음 순서에게 알림이 필요.

문제: **"10분 후"를 어떻게 처리할 것인가.**

## 검토한 선택지

### Option A: APScheduler (백그라운드 스케줄러)

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(release_expired, 'interval', seconds=30)
scheduler.start()
```

| 항목 | 내용 |
|------|------|
| 장점 | 정확한 시간 처리, 요청과 독립적 |
| 단점 | 의존성 추가, 프로세스 재시작 시 스케줄 소멸, FastAPI 생명주기와 별도 관리 |
| 결론 | 프로토타입에서 복잡도 대비 이득 없음 → **보류** |

### Option B: Celery + Redis

```python
@celery.task
def release_machine(machine_id):
    ...

release_machine.apply_async(countdown=600)  # 10분 후 실행
```

| 항목 | 내용 |
|------|------|
| 장점 | 정확한 만료 처리, 분산 작업 가능 |
| 단점 | Redis 인프라 추가 필요, 설정 복잡, 과도한 오버엔지니어링 |
| 결론 | 현재 규모에 과도함 → **탈락** |

### Option C: Lazy Expiration ✅

```python
def release_expired(db: Session) -> int:
    now = datetime.now(timezone.utc)
    expired = db.query(Machine).filter(
        Machine.status == "soft_reserved",
        Machine.reserved_until < now
    ).all()
    for m in expired:
        m.status = "available"
        m.reserved_by_user_id = None
        m.reserved_until = None
    if expired: db.commit()
    return len(expired)
```

요청/이벤트가 발생할 때 만료 여부를 확인하고 그때 처리.

| 항목 | 내용 |
|------|------|
| 장점 | 의존성 없음, 단일 프로세스, 구현 단순 |
| 단점 | 만료 감지가 다음 이벤트까지 지연 (최대 30초) |

## 결정

**Lazy Expiration 채택.**

WebSocket keepalive 루프(30초)에서 `release_expired` 호출:

```python
# ws.py — 30초마다 자동 실행
try:
    await asyncio.wait_for(ws.receive_text(), timeout=30.0)
except asyncio.TimeoutError:
    pass

released = machine_repo.release_expired(db)
if released:
    await _notify_queue_and_broadcast(db, gender)
```

이미 존재하는 WS keepalive 루프를 재활용하므로 추가 인프라 없이 처리 가능.
만료 처리 지연 최대 30초 — 세탁기 예약 서비스에서 허용 가능한 수준.

## 트레이드오프

| 포기한 것 | 얻은 것 |
|-----------|---------|
| 정확한 만료 시각 처리 | 인프라 단순성 (Redis, Celery 불필요) |
| 즉각적 만료 감지 | WS 루프와 통합으로 별도 관리 포인트 없음 |

## 결과 (사후)

- 실제 동작: WS 연결된 사용자가 있는 한 30초마다 만료 처리 실행
- WS 연결 없는 상황(모든 사용자 오프라인)에서는 만료 처리 미발생
  → 실서비스 전환 시 APScheduler 도입 검토 대상
