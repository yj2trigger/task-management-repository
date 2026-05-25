# ADR-005: IoT 연동 설계 — 엔드포인트 선설계

## 상태
채택됨 (장치 연결 대기 중, 2025-05-25)

## 컨텍스트

실제 세탁기의 작동 상태(가동 중 / 종료)를 시스템에 반영해야 함.
현재: 어드민이 수동으로 상태 변경. 한계: 세탁이 끝나도 즉각 반영 불가.

요구사항:
- 세탁기 장치가 작동 상태를 서버에 전송
- 서버가 상태 변경 + 대기열 알림 처리
- 장치 연결 전에도 시스템이 동작해야 함 (Graceful degradation)

## 검토한 선택지

### Option A: IoT 연동 완성 후 개발

장치 구입/연결 확정 후 설계.

**문제:** 장치 없이 백엔드 개발 불가 → 개발 블로킹.

### Option B: MQTT 브로커

```
세탁기 → MQTT Broker → 서버 (subscribe)
```

| 항목 | 내용 |
|------|------|
| 장점 | IoT 표준, 저전력 장치 친화적 |
| 단점 | 브로커 인프라 추가 필요, 현재 장치 프로토콜 미확정 |
| 결론 | 장치 스펙 미확정 상태에서 과도한 선택 → **보류** |

### Option C: REST Webhook 엔드포인트 선설계 ✅

```
세탁기 → POST /iot/machines/{id}/status
         {"is_running": true | false}
```

장치가 HTTP 요청을 보낼 수 있으면 즉시 연동 가능.
장치 없이도 curl/Postman으로 테스트 가능.

## 결정

**REST Webhook + Device Key 인증으로 선설계.**

```python
# 인증: X-Device-Key 헤더 (JWT 아님 — 장치는 로그인 흐름 불가)
def _verify_device_key(x_device_key: str = Header(...)):
    if not settings.iot_device_key:
        raise HTTPException(503, "IoT 연동이 설정되지 않았습니다")
    if x_device_key != settings.iot_device_key:
        raise HTTPException(403, "인증 실패")

# 신호 처리
@router.post("/iot/machines/{machine_id}/status")
async def receive_machine_signal(machine_id, body: MachineSignal, ...):
    new_status = "in_use" if body.is_running else "available"

    if machine.status == new_status:
        return {"changed": False}  # 중복 신호 무시

    machine_repo.set_status(db, machine, new_status)

    if new_status == "available":
        # 대기열 확인 → 첫 대기자 알림 → 전체 broadcast
        background_tasks.add_task(_handle_available, gender)
    else:
        # machines_updated broadcast만
        background_tasks.add_task(_handle_in_use, gender)
```

`IOT_DEVICE_KEY` 미설정 시 503 반환 → 장치 없는 환경에서 안전하게 비활성화.

## 트레이드오프

| 포기한 것 | 얻은 것 |
|-----------|---------|
| IoT 표준 프로토콜(MQTT) | 즉시 테스트 가능 (curl) |
| 장치별 최적화 | 장치 스펙 무관 (HTTP 가능하면 연동) |
| | 장치 없이도 시스템 완성 |

## 결과 (사후)

- 엔드포인트 구현 완료, curl로 동작 확인
- `fly secrets set IOT_DEVICE_KEY=<값>` 설정 후 즉시 활성화 가능
- 실제 장치 연결 시 추가 개발 없이 URL + Key만 장치에 설정하면 연동 완료
