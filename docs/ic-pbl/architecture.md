# ic-pbl 아이스크림 키오스크 — 아키텍처

> 상태: 아이스크림 키오스크 완성 + 의존성 분리 리팩터링 완료 (2026-06-03)

---

## 1. 파일 구조

```
project/
├── src/
│   └── app/
│       ├── main.py              # 진입점 (--gui → GUI, 기본 → 안내 메시지)
│       ├── exceptions.py        # 커스텀 예외 6종
│       ├── ice_cream.py         # IceCreamProduct
│       ├── option.py            # Option, OptionGroup
│       ├── ingredient.py        # Ingredient — 재고 수량
│       ├── cart.py              # Cart, OrderItem
│       ├── payment.py           # CashPayment, CardPayment, ChangeReserve
│       ├── password_utils.py    # hash_password / verify_password (scrypt)
│       ├── data_manager.py      # DataManager — JSON 읽기/쓰기
│       ├── kiosk_controller.py  # KioskController — GUI의 단일 진입점
│       └── gui/
│           ├── app.py           # run_gui(controller, cart) — QApplication 래퍼
│           ├── main_window.py   # KioskWindow(controller, cart) — QStackedWidget + 네비게이션
│           ├── voice_service.py # VoiceService — TTS 음성 안내
│           ├── screens/
│           │   ├── idle.py
│           │   ├── main_menu.py
│           │   ├── customize.py
│           │   ├── cart.py
│           │   ├── payment_method.py
│           │   ├── cash_payment.py
│           │   ├── receipt.py
│           │   ├── admin_auth.py
│           │   └── admin_menu.py
│           └── widgets/
│               ├── stick_preview.py
│               └── scoop_preview.py
├── tests/
│   ├── conftest.py
│   ├── test_cart.py
│   ├── test_payment.py
│   ├── test_data_manager.py
│   ├── test_exceptions.py
│   ├── test_gui_app.py
│   ├── test_gui_screens.py
│   ├── test_password_utils.py
│   └── test_kiosk_controller.py  # KioskController 단위 테스트 (2026-06-03 추가)
├── pyproject.toml
├── requirements.txt
├── build_windows.ps1            # → dist\kiosk.exe
└── build_mac.sh                 # → dist/kiosk.app
```

> `stats.py`, `test_stats.py` 제거됨: Statistics 클래스가 결제 흐름에 연결되지 않은 미완성 기능이었음.

---

## 2. 레이어 구조 (의존성 방향)

```
GUI (screens/)
  │  controller.메서드() 만 호출 — 도메인 객체 직접 접근 금지
  ▼
KioskController           ← GUI의 유일한 진입점
  │  도메인 객체 조합
  ▼
도메인: Cart, Payment, Ingredient, IceCreamProduct, Option, ChangeReserve
  │  예외 → exceptions.py
  ▼
DataManager               ← JSON 읽기/쓰기
```

**핵심 원칙:**
- GUI가 도메인 객체를 직접 생성하거나 속성을 변경하지 않는다.
- GUI가 도메인 구조(Cart.items, CashPayment 등)에 의존하지 않는다.
- 도메인 구조가 바뀌어도 GUI 코드는 수정 불필요.

---

## 3. 클래스 책임 정의

### ice_cream.py

**`IceCreamProduct`**

| 속성 | 설명 |
|------|------|
| `product_id` | 식별자 |
| `name` | 상품명 |
| `base_price` | 기본 가격 |
| `is_available` | 판매 가능 여부 |
| `product_type` | `"stick"` or `"scoop"` |

`calculate_price(selected_options)` → 기본 가격 + 선택 옵션 extra_price 합산

### option.py

**`Option`** — 단일 옵션 항목 (option_id, name, extra_price, required_ingredients_dic)

**`OptionGroup`** — 옵션 그룹 (group_id, name, active_for 상품타입 목록, options 목록)

### kiosk_controller.py

**`KioskController`** — GUI의 단일 진입점. 모든 비즈니스 로직을 캡슐화.

**공개 API 분류:**

| 그룹 | 메서드 |
|------|--------|
| 상품 조회 | `get_available_products()`, `get_option_groups()`, `get_unavailable_options()` |
| 장바구니 조회 | `is_cart_empty()`, `get_cart_items() → list[dict]`, `get_cart_subtotal()`, `get_final_amount()` |
| 장바구니 변경 | `add_to_cart()`, `remove_from_cart()`, `update_cart_qty()`, `clear_cart()` |
| 현금 결제 | `start_cash_payment()`, `get_inserted_amount()`, `insert_cash()`, `can_complete_payment()`, `process_cash_payment() → (snapshot, amount, change)`, `cancel_cash_payment() → int` |
| 카드 결제 | `start_card_payment()`, `process_card_payment() → (snapshot, amount)` |
| 관리자 조회 | `get_cash_status() → dict`, `get_stock_status() → list[dict]` |
| 관리자 변경 | `authenticate_admin()`, `admin_replenish()`, `admin_set_price()`, `admin_toggle_product()`, `admin_add_cash()`, `admin_change_password()` |

**결제 반환값 설계:**
- `process_cash_payment()` → `(snapshot, final_amount, change_result)` 튜플
  - snapshot: cart 비우기 전 OrderItem 리스트 (영수증 표시용)
  - change_result: {권종: 반환장수} 잔돈 딕셔너리
- `process_card_payment()` → `(snapshot, final_amount)` 튜플
- 실패 시 PaymentException raise + `_active_payment` 자동 정리

### gui/main_window.py

**`KioskWindow(controller, cart)`** — QStackedWidget 기반 화면 관리

> `change_reserve`는 생성자 파라미터에서 제거됨 (2026-06-03). controller.change_reserve로 접근.

네비게이션 API:
- `go_to_idle()` / `go_to_main_menu()` / `go_to_customize(product)`
- `go_to_cart()` / `go_to_payment_method()` / `go_to_cash_payment()` / `go_to_card_payment()`
- `go_to_receipt(items, amount, method, change)` / `go_to_admin_auth()` / `go_to_admin_menu()`

---

## 4. 설계 결정

| 결정 | 이유 |
|------|------|
| Cart/Payment 재활용 | 실제 판매 서비스, 결제 로직 그대로 |
| QStackedWidget 유지 | 화면 전환 구조가 아이스크림 흐름과 동일 |
| Options 분리 (option.py) | 상품과 옵션 독립, 상품 타입별 활성 옵션 필터링 |
| scrypt 비밀번호 해시 | 단방향 해시, 레거시 평문 PIN 자동 마이그레이션 |
| JSON 데이터 파일 | DB 없이 로컬 단독 실행 |
| KioskController 단일 진입점 | GUI가 도메인 구조에 의존하지 않도록. Cart 구조 변경 시 GUI 수정 불필요. |
| get_cart_items() → list[dict] | OrderItem 객체를 GUI에 노출하지 않음. dict 구조만 의존. |
| process_*_payment() tuple 반환 | snapshot을 controller가 직접 생성. GUI가 cart를 직접 읽을 필요 없음. |
| AppData 경로 IceCreamKiosk | 구 EDK(Erica Drug King) 폴더명에서 변경 (2026-06-03) |
