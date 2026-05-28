# ADR-007: SmartThings 적응형 Polling

**날짜:** 2026-05-28  
**상태:** 채택됨

---

## 컨텍스트

세탁기 전력 상태를 실시간으로 파악하기 위해 SmartThings Cloud API에서 전력값(W)을 주기적으로 수집해야 한다.

핵심 긴장 관계:
- **너무 빈번한 polling** → SmartThings API rate limit 위험 + 불필요한 DB 쓰기
- **너무 드문 polling** → 세탁기 완료 감지 지연 → 대기열 알림 지연

추가 제약:
- 이용 가능한 세탁기가 적을수록(Mode C/B) 전력 변화에 빠르게 반응해야 함
- 야간에는 세탁 수요가 없으므로 polling 주기를 늘려야 함
- 다수의 세탁기를 지원해야 함 (`SMARTTHINGS_DEVICE_XX` 패턴으로 확장)

---

## 결정

**Mode 기반 적응형 polling 주기 + 야간 절전 모드 적용.**

```python
def _calc_interval(mode: str) -> float:
    kst_hour = (datetime.now(timezone.utc).hour + 9) % 24
    if kst_hour < 7 or kst_hour >= 22:   # 야간 (22:00–07:00 KST)
        return 900.0
    return {"A": 480.0, "B": 120.0, "C": 60.0}.get(mode, 120.0)
```

| 상황 | 주기 | 이유 |
|------|------|------|
| 야간 (22:00–07:00 KST) | 900s (15분) | 수요 없음, API 절약 |
| Mode A (4대 이상) | 480s (8분) | 여유 있음, 빠른 감지 불필요 |
| Mode B (1~3대) | 120s (2분) | 경쟁 상황, 중간 빈도 |
| Mode C (0대) | 60s (1분) | 만원, 빈 세탁기 즉시 감지 필요 |

---

## 구현 세부사항

### 환경변수 패턴

```
SMARTTHINGS_PAT=<Personal Access Token>
SMARTTHINGS_DEVICE_01=<SmartThings device_id>  → machine_id=1
SMARTTHINGS_DEVICE_02=<SmartThings device_id>  → machine_id=2
```

접미사 숫자가 machine_id. 새 기기 추가 시 GitHub Secret → CD workflow로 자동 전파.

### 내결함성 설계

각 단계를 독립 try/except로 격리. 한 단계 실패가 전체 루프 중단으로 이어지지 않음:

```python
# mode/threshold 조회 실패 → 기본값으로 fallback
try:
    mode, threshold = _get_mode_and_threshold()
except:
    mode, threshold = "A", 100.0

# 개별 기기 오류 → 해당 기기만 건너뜀
for machine_id, device_id in device_map.items():
    try:
        power_w = await smartthings_client.get_power_w(device_id)
        machine_power_log_repo.create(db, machine_id, power_w)
        ...
    except Exception as e:
        logger.warning(f"polling error (machine {machine_id}): {e}")
```

### 시작 조건

`SMARTTHINGS_PAT` 미설정 시 polling 비활성 (INFO 로그 후 즉시 종료).  
`SMARTTHINGS_DEVICE_XX` 미설정 시 동일.

### 전력 데이터 보존

`machine_power_logs` 테이블에 누적. 7일 초과 데이터는 polling 루프 내 24시간마다 자동 삭제 (`delete_old(db, days=7)`).

### 어드민 조회

`GET /admin/machines/{id}/power-history?hours=24` — 최대 168h 조회 가능.

---

## 고려한 대안

| 대안 | 탈락 이유 |
|------|----------|
| 고정 주기 (예: 60s 항상) | Mode A에서 불필요한 API 호출, 야간 절전 없음 |
| WebSocket push (SmartThings Rules) | SmartThings Rules API 설정 복잡, 서버 수신 엔드포인트 추가 필요 |
| 별도 Lambda/워커 | 인프라 추가 없이 Fly.io 단일 머신에서 해결 가능 |
| IoT REST 엔드포인트 (`/iot`) 만 사용 | 실제 기기를 Fly.io에 직접 연결해야 함, SmartThings 없으면 불가 |

---

## 결과

- SmartThings polling 2026-05-28 배포 완료
- 전력 데이터 DB 누적 확인
- 관리자 전력 그래프 24h 표시 확인
- 실제 기기(세탁기) 부착은 별도 물리 작업 대기 중
