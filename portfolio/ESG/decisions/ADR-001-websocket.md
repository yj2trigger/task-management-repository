# ADR-001: 실시간 통신 방식 — WebSocket 채택

## 상태
채택됨 (2025-05-24)

## 컨텍스트

세탁기 예약 서비스의 실시간 요구사항:

1. 세탁기 상태 변경(available → soft_reserved)을 **모든 연결 클라이언트에 즉시 반영**
2. 대기열 알림(`queue_notify`)을 **특정 사용자(user_id)에게만** 전송 — 배정 정보는 본인만 수신
3. 대기 순번 변경을 **대기 중인 모든 사용자에게 동시에** 전송

세 요구사항의 공통점: **서버가 클라이언트에게 먼저 데이터를 푸시해야 함.**

## 검토한 선택지

### Option A: Short Polling

```
클라이언트 → GET /machines (매 5초)
```

| 항목 | 내용 |
|------|------|
| 장점 | 구현 단순, 모든 환경 호환 |
| 단점 | 5초 지연, user_id 타겟 전송 불가, 불필요한 요청 |
| 결론 | 핵심 요구사항 충족 불가 → **탈락** |

사용자 100명 기준 폴링: 초당 20 req → 변경 없어도 지속 발생.

### Option B: Server-Sent Events (SSE)

```
클라이언트 → GET /stream (한 번 연결)
서버 → 이벤트 스트림 전송 (단방향)
```

| 항목 | 내용 |
|------|------|
| 장점 | WebSocket보다 구현 단순, HTTP 기반 |
| 단점 | 서버→클라이언트 단방향만, Reconnect 직접 구현 필요 |
| 결론 | 단방향으로 충분하지 않음 → **탈락** |

`queue_notify` (특정 유저)와 `machines_updated` (전체)를 하나의 연결로 처리하려면
결국 WebSocket과 유사한 연결 관리가 필요해짐.

### Option C: WebSocket ✅

```
클라이언트 → WS /ws?token=JWT (인증 포함)
서버 ↔ 클라이언트 양방향 유지
```

| 항목 | 내용 |
|------|------|
| 장점 | user_id 타겟 전송, gender 채널 분리, keepalive 루프에서 만료 처리 통합 |
| 단점 | 연결 관리 코드 필요, Vercel 미지원 → 백엔드 분리 배포 |

## 결정

**WebSocket 채택.**

결정적 이유: `queue_notify`가 **특정 사용자에게만** 전송되어야 함.
SSE로도 가능하지만, 30초 keepalive 루프에서 `release_expired` 처리를
함께 수행하는 구조는 WebSocket이 더 자연스럽고 단일 연결로 통합 가능.

## 구현 핵심

```python
class ConnectionManager:
    # gender 채널 분리: 남성/여성 세탁기 정보 격리
    connections: dict[str, dict[int, WebSocket]]
    # {"male": {user_id: ws}, "female": {user_id: ws}}

    async def broadcast(self, gender: str, message: dict):
        # machines_updated: 전체 gender 채널에 전송

    async def send_to_user(self, user_id: int, gender: str, message: dict):
        # queue_notify: 특정 사용자에게만 전송
```

```python
# WS 루프: keepalive + lazy expiration 통합
while True:
    try:
        await asyncio.wait_for(ws.receive_text(), timeout=30.0)
    except asyncio.TimeoutError:
        pass  # 30초마다 만료 체크 트리거

    released = machine_repo.release_expired(db)
    if released:
        await _notify_queue_and_broadcast(db, gender)
        # 만료 → available → 대기자 알림 → 모드 재계산 → 전체 broadcast
```

## 트레이드오프

| 포기한 것 | 얻은 것 |
|-----------|---------|
| Vercel 단일 플랫폼 배포 | 별도 스케줄러(APScheduler/Celery) 불필요 |
| SSE 대비 연결 관리 코드 증가 | user_id 타겟 + 전체 broadcast 통합 |
| | gender 채널 분리로 정보 격리 |

## 결과 (사후)

- Fly.io에서 `auto_stop_machines = false` 설정으로 WS 장기 연결 안정적 유지
- React StrictMode 이중 마운트로 첫 WS 연결 즉시 종료(1006) → 두 번째 연결 정상 (영향 없음)
- 3초 자동 재연결 로직(`useWebSocket.ts`)으로 일시적 네트워크 단절 대응
