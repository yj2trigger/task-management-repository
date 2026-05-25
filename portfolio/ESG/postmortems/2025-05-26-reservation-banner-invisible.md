# Postmortem: 소프트 예약 배너 즉시 소멸 (timezone 버그)

**날짜:** 2025-05-26  
**심각도:** 핵심 기능 불동작 (예약 결과 화면에 전혀 표시 안 됨)  
**해결 소요 시간:** 증상 확인 5분, 원인 분석 10분, 수정 5분

---

## 증상

Mode B 배정 또는 C모드 수락 후:
- 소프트 예약 배너가 표시되지 않음 ("전혀 안 보여요")
- `GET /machines/my-reservation` 호출 시 서버는 정상 응답
- `activeReservation` state는 set 되지만 즉시 사라짐

---

## 원인 분석

### 5 Whys

**왜** 배너가 안 보이는가?  
→ `activeReservation` state가 set된 직후 `null`로 초기화되기 때문

**왜** 즉시 초기화되는가?  
→ auto-clear `useEffect`에서 `ms <= 0` 조건 충족 → `setActiveReservation(null)` 호출

**왜** `ms <= 0`인가?  
→ `new Date(reserved_until).getTime() - Date.now()` 가 음수

**왜** 음수인가?  
→ 백엔드 datetime이 `"2025-05-26T03:30:00"` (Z 없음)으로 직렬화됨  
→ JS `new Date("2025-05-26T03:30:00")` = **로컬 시각(KST)** 으로 해석  
→ KST = UTC+9이므로, 실제 UTC 시각(12:30)보다 9시간 앞선 시각으로 인식

**루트 코즈:**  
SQLAlchemy `Column(DateTime)` (timezone 없음) → PostgreSQL `TIMESTAMP WITHOUT TIME ZONE` 저장  
→ 조회 시 timezone-naive datetime 반환 → FastAPI 직렬화 시 `Z` 접미사 없음  
→ JS가 서버 시각(UTC)을 로컬(KST)로 잘못 해석 → 9시간 차이 → 즉시 만료

### 코드 레벨

```python
# machine.py 모델 — timezone 없는 컬럼
reserved_until = Column(DateTime, nullable=True)  # ← TIMESTAMP WITHOUT TIME ZONE

# 저장 시 UTC-aware datetime 사용
machine.reserved_until = datetime.now(timezone.utc) + timedelta(minutes=10)
# → DB에 저장될 때 timezone 정보 탈락
# → 조회 시: datetime(2025, 5, 26, 3, 30, 0)  (naive, 실제로는 UTC)
```

```typescript
// useEffect — 즉시 소멸 유발
const ms = new Date(reservation.reserved_until).getTime() - Date.now()
// new Date("2025-05-26T03:30:00") → KST 03:30 → UTC -05:30 환산
// Date.now() → UTC 12:30
// ms = UTC(-5:30) - UTC(12:30) = 음수 → setActiveReservation(null)
```

---

## 해결 과정

**접근 1 (검토):** DB 컬럼을 `DateTime(timezone=True)`로 변경  
→ PostgreSQL 스키마 변경 필요 (마이그레이션), Supabase 테이블 수정 필요  
→ 위험도 높음, 즉각 적용 어려움 → **보류**

**접근 2 (채택):** 프론트엔드에서 timezone-naive 문자열을 UTC로 강제 파싱

```typescript
// asUtc 헬퍼 추가
function asUtc(s: string): Date {
  return new Date(s.endsWith('Z') || s.includes('+') ? s : s + 'Z')
}

// 모든 서버 datetime 파싱에 적용
const ms = asUtc(reservation.reserved_until).getTime() - Date.now()
```

적용 범위: auto-clear useEffect, `PendingOfferBanner`, `ActiveReservationBanner`

---

## 예방 조치

향후 DB 마이그레이션 시 `DateTime(timezone=True)` 로 전환.  
그 전까지: 서버 datetime을 파싱하는 코드는 반드시 `asUtc()` 사용.

---

## 학습

**"명백한 UTC"가 JS에선 로컬시간:**  
ISO 8601에서 `Z` 또는 `+00:00` 없는 datetime 문자열은  
ECMAScript 표준상 로컬 시간으로 해석 (브라우저마다 다를 수 있으나 크롬/V8은 로컬).

```
"2025-05-26T12:30:00"   → new Date() → KST 해석 → UTC 03:30 (9시간 전)
"2025-05-26T12:30:00Z"  → new Date() → UTC 해석 → 정확
```

**교훈:** 백엔드-프론트 datetime 계약은 항상 명시적 timezone(Z 또는 오프셋) 포함.  
SQLAlchemy `DateTime` vs `DateTime(timezone=True)` 차이를 프로젝트 초기에 결정해야 함.

**면접 활용 포인트:**  
"timezone-naive datetime이 야기한 subtle 버그"로 활용 가능.  
증상(기능 완전 불동작) ↔ 원인(9시간 차이) 격차가 크고, 디버깅 과정이 흥미로움.
