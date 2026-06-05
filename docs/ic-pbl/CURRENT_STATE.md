# CURRENT_STATE — ic-pbl 아이스크림 키오스크

> Last Update: 2026-06-05
> Phase: **완료** — 기능 구현, 버그 수정, 의존성 분리, 전체 파일 헤더 주석 완료, 149 tests passing

---

## 도메인 현황

아이스크림 키오스크 (stick ₩3,000 / scoop ₩4,000). 커스터마이징 옵션(형태, 코팅, 토핑, 용기, 맛), 재고 기반 주문, 현금/카드 결제, 관리자 메뉴.

**GUI 흐름:** idle → main_menu → customize → cart → payment_method → cash/card → receipt

**레이어 원칙:** GUI (screens/) → KioskController → 도메인 (Cart, Payment, Ingredient, ...)
GUI는 KioskController의 공개 메서드만 호출한다. 도메인 객체를 직접 생성·접근·조작하지 않는다.

---

## 구현 완료 현황

### Core

| 파일 | 역할 |
|------|------|
| `ice_cream.py` | `IceCreamProduct` — product_id, name, base_price, is_available, product_type |
| `option.py` | `Option`, `OptionGroup` — 커스터마이징 옵션 |
| `kiosk_controller.py` | 상품/옵션/장바구니/결제/관리자 전체 비즈니스 로직. GUI의 단일 진입점. |
| `data_manager.py` | products.json / ingredients.json / options.json / admin_config.json / change_reserve.json |
| `main.py` | GUI 진입점, 데이터 초기화 (`--gui` 플래그). `(controller, cart)` 반환. |
| `password_utils.py` | `hash_password` / `verify_password` (scrypt) |
| `cart.py` | `OrderItem`, `Cart` |
| `payment.py` | `CashPayment`, `CardPayment`, `ChangeReserve` |
| `ingredient.py` | `Ingredient` — 재고 수량 관리 |
| `exceptions.py` | 커스텀 예외 6종 |

> `stats.py` 미연동 상태: `Statistics` 클래스 구현은 완료되어 있으나 `KioskController._save_after_payment()`에 연결되지 않음 (dead code 주석으로 표시). 향후 통계 화면 추가 시 연동 예정.

### KioskController 공개 API (전체)

**조회:**
`get_available_products()`, `get_option_groups(product)`, `get_unavailable_options(product, selected)`,
`is_cart_empty()`, `get_cart_items() → list[dict]`, `get_cart_subtotal()`, `get_final_amount()`,
`get_inserted_amount()`, `can_complete_payment()`, `get_cash_status() → dict`, `get_stock_status() → list[dict]`

**장바구니:**
`add_to_cart()`, `remove_from_cart()`, `update_cart_qty()`, `clear_cart()`

**결제:**
`start_cash_payment()`, `insert_cash()`, `process_cash_payment() → (snapshot, amount, change)`,
`cancel_cash_payment() → int`,
`start_card_payment()`, `process_card_payment() → (snapshot, amount)`

**관리자:**
`authenticate_admin()`, `admin_replenish()`, `admin_set_price()`, `admin_toggle_product()`,
`admin_add_cash()`, `admin_change_password()`

### GUI

| 파일 | 역할 |
|------|------|
| `gui/app.py` | `run_gui(controller, cart)` — QApplication 진입점 |
| `gui/main_window.py` | `KioskWindow(controller, cart)` — QStackedWidget + 네비게이션 API |
| `gui/voice_service.py` | TTS 음성 안내 (edge-tts + pygame) |
| `gui/screens/idle.py` | 대기 화면 |
| `gui/screens/main_menu.py` | 상품 목록 화면 |
| `gui/screens/customize.py` | 옵션 커스터마이징 |
| `gui/screens/cart.py` | 장바구니 (controller.get_cart_items() → dict 리스트 사용) |
| `gui/screens/payment_method.py` | 결제 수단 선택 |
| `gui/screens/cash_payment.py` | 현금 결제 (controller 전담) |
| `gui/screens/receipt.py` | 영수증 |
| `gui/screens/admin_auth.py` | 관리자 인증 화면 |
| `gui/screens/admin_menu.py` | 관리자 메뉴 (get_stock_status/get_cash_status 경유) |
| `gui/widgets/stick_preview.py` | 스틱 아이스크림 미리보기 |
| `gui/widgets/scoop_preview.py` | 스쿱 아이스크림 미리보기 |

### 테스트

| 파일 | 케이스 수 |
|------|---------|
| `test_cart.py` | 19 |
| `test_payment.py` | 35 |
| `test_data_manager.py` | 13 |
| `test_exceptions.py` | 16 |
| `test_gui_app.py` | 9 |
| `test_gui_screens.py` | 23 |
| `test_password_utils.py` | 7 |
| `test_kiosk_controller.py` | 27 |
| **합계** | **149 passed** |

---

## 실행 방법

```bash
# project/ 디렉토리 안에서
pip install -e ".[dev]"
python -m app.main --gui   # GUI 모드
python -m pytest tests/ -v # 테스트
```

## 빌드

```powershell
.\build_windows.ps1   # → dist\kiosk.exe  (AppData\IceCreamKiosk\data\)
```
```bash
bash build_mac.sh     # → dist/kiosk.app
```
