# ic-pbl 아이스크림 키오스크 — 테스트 전략 (Test Strategy)

> 작성일: 2026-06-03 (최종 업데이트)
> 상태: 149 tests passing

---

## 1. 테스트 파일 구조

```
tests/
├── conftest.py              # KioskController + IceCreamProduct fixtures
├── test_cart.py             # 19 cases
├── test_payment.py          # 35 cases
├── test_data_manager.py     # 13 cases
├── test_exceptions.py       # 16 cases
├── test_gui_app.py          # 9 cases
├── test_gui_screens.py      # 23 cases
├── test_password_utils.py   # 7 cases
└── test_kiosk_controller.py # 27 cases (2026-06-03 추가)
```

**합계: 149 passed**

---

## 2. 파일별 테스트 책임

| 파일 | 케이스 수 | 테스트 대상 |
|------|---------|-----------|
| `test_cart.py` | 19 | Cart.add / remove / total, OrderItem 소계, 재고 연동 |
| `test_payment.py` | 35 | CashPayment 투입/완료, ChangeReserve 그리디 잔돈, CardPayment |
| `test_data_manager.py` | 13 | JSON 읽기/쓰기, 파일 없을 때 기본값 생성 |
| `test_exceptions.py` | 16 | 커스텀 예외 6종 생성 및 메시지 |
| `test_gui_app.py` | 9 | QApplication 초기화, GUI 진입점 |
| `test_gui_screens.py` | 23 | 각 화면 전환 API, 위젯 상태 |
| `test_password_utils.py` | 7 | hash_password / verify_password, 레거시 평문 마이그레이션 |
| `test_kiosk_controller.py` | 27 | KioskController 공개 API 전체: 장바구니, 결제 흐름, 취소, 상태 조회, 관리자 |

---

## 3. 경계값 우선순위

| 우선순위 | 경계값 |
|---------|--------|
| 최우선 | stock = 0 (품절, 옵션 비활성화) |
| 최우선 | stock = max_capacity (보충 한도 초과) |
| 최우선 | inserted_amount = final_amount (잔돈 0원) |
| 최우선 | ChangeReserve 잔돈 부족 → InsufficientChangeException |
| 중요 | 빈 cart에서 결제 시도 |
| 중요 | quantity = 1 (최소 수량) |

---

## 4. 테스트 실행 방법

```bash
# project/ 디렉토리 안에서
pip install -e ".[dev]"
python -m pytest tests/ -v
```

```powershell
# PowerShell
$env:PYTHONPATH="src"; python -m pytest tests/ -v
```
