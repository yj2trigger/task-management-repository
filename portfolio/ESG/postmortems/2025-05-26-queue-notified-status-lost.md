# 사고: 대기열 notified 상태 새로고침 시 소멸

**날짜:** 2025-05-26  
**심각도:** Medium (사용자 혼란 — 수락 배너 사라짐, 대기 취소 버튼 대신 등록 버튼 표시)

---

## 증상

- 대기열 offer를 받은 사용자(status=notified)가 페이지를 새로고침하면:
  - 5분 수락 배너가 보이지 않음
  - "대기 취소" 버튼 대신 "대기열 등록" 버튼 표시
  - 다시 등록 시도 → 400 "이미 대기열에 등록되어 있습니다"
- waiting 상태 사용자는 정상 복원됨 (취소 버튼 표시, 순위 표시)

---

## 원인

`GET /queue/status` 내부에서 `get_waiting_entry(db, user_id)` 를 호출 — `status == "waiting"` 항목만 조회:

```python
# 버그 코드
entry = queue_repo.get_waiting_entry(db, current_user.id)
if not entry:
    return QueueStatusResponse(in_queue=False)   # notified 사용자도 여기서 반환됨
```

`notified` 상태 사용자는 `in_queue=False` 로 응답 → 프론트 마운트 시 `pendingOffer` / `queueInfo` 모두 복원 실패.

---

## 해결

**Backend** — `get_entry()` (status 무관 조회)로 변경, notified 분기 추가:

```python
entry = queue_repo.get_entry(db, current_user.id)
if not entry:
    return QueueStatusResponse(in_queue=False)
if entry.status == "notified":
    return QueueStatusResponse(in_queue=True, is_notified=True, accept_until=entry.expires_at)
# waiting 분기
position = queue_repo.get_position(...)
return QueueStatusResponse(in_queue=True, queue_position=position, total=total)
```

**Frontend** — 마운트 시 `getMyReservation()` + `getQueueStatus()` 병렬 호출, 우선순위:

```typescript
const [res, status] = await Promise.all([getMyReservation(token), getQueueStatus(token)])
if (status.is_notified && status.accept_until && res.active && res.assigned_machine) {
    setPendingOffer({ machine: res.assigned_machine, accept_until: status.accept_until })
} else if (res.active && res.assigned_machine && res.reserved_until) {
    setActiveReservation(...)
} else if (status.in_queue && status.queue_position != null) {
    setQueueInfo(...)
}
```

---

## 근본 원인

**상태 복원 설계 누락.** C모드 구현 시 `notified` 상태를 API 응답에 포함하지 않음.  
`waiting` 복원만 구현하고 `notified` 복원을 누락 — 상태 추가 시 복원 경로도 함께 설계해야 함.

---

## 재발 방지

- 새로운 엔티티 상태 추가 시 체크리스트:
  - [ ] 해당 상태를 클라이언트에 노출하는 status API 업데이트
  - [ ] 페이지 마운트(새로고침) 시 해당 상태 복원 경로 구현
  - [ ] 상태별 UI 분기 확인 (올바른 버튼/배너 표시)
