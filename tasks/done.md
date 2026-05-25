# ✅ Done

> 완료된 태스크 목록입니다.

---

## [ic-pbl] Core 구현 완료 (2026-05-12)

- [x] UNIT-01~12: 전체 테스트 PASS
- [x] 시나리오 테스트: 29/29 PASS

## [ic-pbl] GUI 구현 완료 (PyQt6, 2026-05-22)

- [x] gui/app.py, main_window.py, voice_service.py
- [x] 화면 7종: idle, main_menu, product_list, customize, cart, payment_method, cash_payment, receipt
- [x] 관리자 화면: admin_auth, admin_menu

## [ic-pbl] CI 인프라 (2026-05-26)

- [x] Gemini PR 자동 리뷰 워크플로 (`gemini-2.5-flash-lite`)
- [x] `develope` → `develop` 이름 수정, 브랜치 전략 수립

## [ic-pbl] EDK 도메인 전환 완료 (2026-05-26)

- [x] EDK-01: `medicine.py`, `symptom.py`, `test_medicine.py` 신규 + `product.py` 삭제 (PR #6)
- [x] EDK-03: `data_manager.py` — `medicines.json` / `symptoms.json`, 샘플 5의약품 + 8증상 (PR #7)
- [x] EDK-02: `drug_controller.py` — 증상→의약품 매핑 4메서드 (PR #8)
- [x] EDK-04: `main.py` — `DrugController` + `DataManager` 초기화로 교체, Coffee/Gummy 제거 (PR #9)
- [x] EDK-05: `cli_view.py` — 증상 선택 → 의약품 탐색 → 결제 흐름, CLI 실행 가능 (PR #10)
  - `medicine.py` `calculate_price(selected_options=None)` Cart 호환
  - `main.py` CLIView 인자 `cart`, `change_reserve` 추가

## [ic-pbl] GUI-EDK 도메인 GUI 전환 (PR #11 제출, 2026-05-26)

- [x] GUI-EDK-01: `main_window.py` — `KioskWindow(controller, cart, change_reserve)`, EDK 네비게이션 API
- [x] GUI-EDK-02: `symptom_select.py` 신규 — 증상 그리드, 응급 빨간색, 장바구니 요약
- [x] GUI-EDK-03: `medicine_list.py` 신규 — 증상별 의약품 카드
- [x] GUI-EDK-04: `medicine_detail.py` 신규 — 의약품 상세 + 수량 스피너 + 장바구니
- [x] GUI-EDK-05: `emergency.py` 신규 — 응급 경고 + 119 안내
- [x] GUI-EDK-06: `admin_menu.py` 재작성 — 의약품 ON/OFF 및 가격, 재료 관련 기능 제거
- [x] 개편 화면: `idle.py`, `cart.py`, `payment_method.py`, `cash_payment.py`, `admin_auth.py`, `app.py`, `main.py`

---

## [ESG] 설계 완료

- [x] 1~7단계 전체

## [ESG] 구현 완료

- [x] 구현 1~10단계 (2026-05-23~25)

## [ESG] 기능 추가 / 버그 수정 / 기술부체 (2026-05-25)

- [x] 대기순번 실시간, PWA, 관리자, 설정, IoT 엔드포인트 등
- [x] 로딩 버그, 모바일 UI, WS 타입, 대기열 상태, 어드민 알림 수정
- [x] datetime/Alembic/pytest/GitHub 협업 설정/CI·CD
