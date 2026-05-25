# 🔄 In Progress

> 현재 진행 중인 태스크 목록입니다.

---

## [ic-pbl] 테스트 재작성 — EDK 도메인 기준

- [ ] 구 도메인 테스트 제거: `test_product.py`, `test_ingredient.py`, `test_controller.py`, `test_scenarios.py`, `test_cli_integration.py`
- [ ] `conftest.py` 재작성: EDK fixtures (`medicine`, `symptom`, `cart`)
- [ ] `test_cart.py` 재작성: Medicine 기반 Cart 동작 검증
- [ ] `test_gui_app.py`, `test_gui_screens.py` 재작성: EDK KioskWindow 기반
- [ ] `test_edk_integration.py` 신규: 증상 선택 → 의약품 탐색 → 결제 시나리오
