# EDK — 테스트 전략 (Test Strategy)

> 원본: pmg-ic-pbl/docs/test_strategy.md
> 상태: EDK 전환 후 재작성 필요

---

## 1. 테스트 파일 구조 (EDK 전환 후)

```
tests/
├── test_exceptions.py     # 재활용 가능
├── test_ingredient.py     # 재활용 가능 (재고 로직 동일)
├── test_medicine.py       # 신규 (test_product.py 교체)
├── test_cart.py           # 재활용 가능 (로직 변경 없음)
├── test_payment.py        # 재활용 가능 (로직 변경 없음)
├── test_stats.py          # 재활용 가능
├── test_data_manager.py   # 수정 필요 (medicines.json 기준)
└── test_controller.py     # 수정 필요 (DrugController 기준)
```

---

## 2. 재활용 가능한 테스트

| 파일 | 재활용 여부 | 사유 |
|------|-----------|------|
| test_exceptions.py | ✅ 재활용 | 예외 클래스 변경 없음 |
| test_ingredient.py | ✅ 재활용 | 재고 로직 동일 |
| test_cart.py | ✅ 재활용 | 장바구니 로직 변경 없음 |
| test_payment.py | ✅ 재활용 | 결제 로직 변경 없음 |
| test_stats.py | ✅ 재활용 | 통계 로직 동일 |
| test_product.py | ❌ 교체 | Coffee/Gummy → Medicine으로 교체 |
| test_controller.py | 🔄 수정 | DrugController 기준으로 업데이트 |
| test_data_manager.py | 🔄 수정 | medicines.json 데이터 구조 반영 |

---

## 3. 신규 테스트 — test_medicine.py

| 테스트 | 시나리오 | 검증 |
|--------|---------|------|
| test_medicine_create | Medicine 객체 생성 | 속성 정확성 확인 |
| test_medicine_is_available | is_available=True/False | 판매 가능 여부 |
| test_medicine_symptom_category | symptom_category 설정 | 카테고리 매핑 |
| test_medicine_price | base_price 반환 | 가격 정확성 |

---

## 4. 수정 필요 테스트 — test_controller.py (DrugController)

| 테스트 | 내용 |
|--------|------|
| test_get_medicines_by_symptom | 증상 카테고리로 제품 필터링 |
| test_add_medicine_to_cart | 의약품 장바구니 추가 |
| test_cash_payment_deducts_stock | 결제 후 재고 차감 |
| test_admin_replenish | 관리자 재고 보충 |
| test_admin_auth | 관리자 인증 |

---

## 5. 경계값 우선순위 (재활용)

| 우선순위 | 경계값 |
|---------|--------|
| 🔴 최우선 | stock = 0 (품절) |
| 🔴 최우선 | stock = max_capacity |
| 🔴 최우선 | inserted_amount = final_amount (잔돈 0원) |
| 🟡 중요 | 빈 cart에서 결제 시도 |
| 🟡 중요 | quantity = 1 (최소 수량) |

---

## 6. 테스트 실행 방법

```bash
# project/ 디렉토리 안에서
set PYTHONPATH=src && python -m unittest discover -s tests        # cmd
$env:PYTHONPATH="src"; python -m unittest discover -s tests       # PowerShell
```
