# ADR-006: C모드 대기열 — 즉시 배정 vs 5분 수락 대기

## 상태
채택됨 (2025-05-26)

## 컨텍스트

Mode C 대기열에서 세탁기가 비었을 때 첫 번째 대기자에게 어떻게 배정할 것인가.

초기 구현: 세탁기 가용 시 즉시 소프트 예약 → `queue_notify` 이벤트로 결과 통보.

문제: 사용자가 알림을 즉시 확인하지 못할 수 있음.  
즉시 예약이 되면 → 알림 못 본 사용자가 세탁기를 못 찾아감 → 10분 낭비.  
또한 "배정 받았는지 모르는 채로" 예약 시간이 소진되는 UX 문제.

## 검토한 선택지

### Option A: 즉시 배정 (기존)

```python
machine_repo.soft_reserve(db, machine, waiter.user_id)  # 10분
queue_repo.leave(db, waiter.user_id)
# → queue_notify 이벤트 (결과 통보)
```

| 항목 | 내용 |
|------|------|
| 장점 | 구현 단순 |
| 단점 | 사용자가 알림 놓치면 10분 낭비, 대기자에게 불공평 |

### Option B: 5분 수락 대기 ✅

```python
machine_repo.soft_reserve(db, machine, waiter.user_id, duration_minutes=5)  # 5분 hold
queue_repo.set_notified(db, waiter, accept_minutes=5)
# → queue_offer 이벤트 (수락 요청)
```

수락 시: `POST /queue/accept` → 10분으로 연장.  
미수락 시 (5분 경과): 기기 해제 + 대기자 맨 뒤로 → 다음 대기자에게 offer.

| 항목 | 내용 |
|------|------|
| 장점 | 사용자가 인지하고 수락한 후 예약 확정, 미인지 낭비 방지 |
| 단점 | 구현 복잡도 증가, 추가 상태(notified) 및 엔드포인트 필요 |

### Option C: Push Notification

앱 푸시로 즉시 알림 → 사용자가 확인 후 앱 진입.

| 항목 | 내용 |
|------|------|
| 장점 | 앱 미실행 시에도 알림 가능 |
| 단점 | PWA/네이티브 구현 필요, 프로토타입 단계에서 과도 |

## 결정

**5분 수락 대기 창 방식 채택.**

```python
# ws.py — offer 발송
machine_repo.soft_reserve(db, machine, waiter.user_id, duration_minutes=5)
entry = queue_repo.set_notified(db, waiter, accept_minutes=5)
await manager.send_to_user(waiter.user_id, gender, {
    "type": "queue_offer",
    "machine": {...},
    "accept_until": entry.expires_at.isoformat(),
})

# queue.py — 수락 엔드포인트
@router.post("/accept")
async def accept_queue_offer(...):
    machine = machine_repo.get_active_reserve(db, current_user.id)
    machine_repo.soft_reserve(db, machine, current_user.id, duration_minutes=10)
    queue_repo.leave(db, current_user.id)
```

```python
# WS keepalive — 5분 만료 처리
expired_user_ids = queue_repo.reset_expired_notifications(db, gender)
for uid in expired_user_ids:
    await manager.send_to_user(uid, gender, {
        "type": "queue_offer_expired",
        "message": "5분이 경과하여 대기열 맨 뒤로 이동되었습니다"
    })
```

## QueueEntry 상태 전이

```
waiting → notified (offer 발송, 5분 hold)
notified → [삭제] (수락 → 소프트 예약 확정)
notified → waiting (5분 만료 → 뒤로 이동, created_at = now)
```

## 트레이드오프

| 포기한 것 | 얻은 것 |
|-----------|---------|
| 구현 단순성 | 사용자 인지 보장 후 예약 확정 |
| 즉시 배정 | 미확인 낭비 방지 |
| | 맨 뒤 이동으로 공정한 재기회 |

## 결과 (사후)

- WS keepalive 30초 주기로 만료 체크 → 최대 30초 지연 후 처리 (허용 범위)
- 프론트엔드: 노란 배너 + 카운트다운 + 수락 버튼 / 수락 후 초록 배너 + 10분 카운트다운
- `queue_offer_expired` 이벤트 수신 시 프론트가 `getQueueStatus()` 재호출 → 업데이트된 순위 표시
