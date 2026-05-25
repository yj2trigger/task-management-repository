# CURRENT_STATE — EDK (ic-pbl)

> Last Update: 2026-05-25
> Phase: 도메인 전환 — EDK(Erica Drug King) 리팩터링 대기 중 (미착수)

---

## ⚠️ 프로젝트 방향 전환

**기존**: Micro-Factory Kiosk (커피/영양구미 판매)
**변경**: EDK — 증상 선택 기반 일반의약품/영양제 실제 판매 키오스크

기존 PyQt6 GUI 아키텍처(QStackedWidget, screens/, voice_service)는 그대로 재활용.
결제 시스템(payment.py, cart.py, ChangeReserve)은 유지 — 실제 판매이므로 필수.

---

## Current Active Unit

없음 — 전체 태스크 backlog.md 대기 중.

현재 코드베이스는 원본 Micro-Factory Kiosk (Coffee/Gummy 도메인) 그대로.

---

## ✅ 재활용 확정 유닛

> 클래스/모듈 단위 재활용 전략 (구 클래스 → 신 클래스 매핑): [requirements.md § 2.4](./requirements.md)

| 파일 | 재활용 방식 |
|------|-----------|
| exceptions.py | 그대로 재활용 |
| ingredient.py | 의약품/영양제 재고로 재활용 |
| cart.py | 그대로 재활용 (실제 판매, 장바구니 필요) |
| payment.py | 그대로 재활용 (현금/카드 결제 필요) |
| data_manager.py | 의약품 JSON 데이터 관리로 재활용 |
| gui/app.py | 그대로 재활용 |
| gui/voice_service.py | 그대로 재활용 |
| gui/screens/admin_auth.py | 그대로 재활용 |
| gui/screens/cart.py | 그대로 재활용 |
| gui/screens/payment_method.py | 그대로 재활용 |
| gui/screens/cash_payment.py | 그대로 재활용 |
| gui/screens/receipt.py | 그대로 재활용 |

---

## 🔄 EDK 전환 작업 목록

→ 상세 태스크 목록: [tasks/backlog.md](../../tasks/backlog.md) § [ic-pbl] EDK 도메인 전환

---

## 목표 파일 구조 (전환 후)

→ 상세: [architecture.md § 2. EDK 전환 후 목표 파일 구조](./architecture.md)

---

## 데이터 파일 구성

→ 상세 (갱신 시점 포함): [scope.md § 7. 데이터 파일 구성](./scope.md)

---

## Current Risks

- 기존 테스트(test_*.py)가 구 도메인(커피/구미) 기반 — 전환 후 재작성 필요
- cart/payment 테스트는 로직 변경 없으면 재활용 가능

---

## 실행 방법

```bash
# project/ 디렉토리 안에서
python -m app.main        # CLI 모드
python -m app.main --gui  # GUI 모드
```
