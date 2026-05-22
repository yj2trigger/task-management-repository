# EDK (Erica Drug King) — 아키텍처

> 원본: pmg-ic-pbl/docs/architecture.md (Micro-Factory Kiosk 기반)
> 상태: EDK 전환 중 — 업데이트 필요

---

## 1. 현재 파일 구조 (구현 완료 기준)

```
project/
├── src/
│   └── app/
│       ├── main.py              # 진입점 (--gui 플래그 or frozen → GUI, 기본 → CLI)
│       ├── exceptions.py        # 커스텀 예외 6종
│       ├── product.py           # Product, Coffee, Gummy, CustomOption, OptionGroup
│       ├── ingredient.py        # Ingredient
│       ├── cart.py              # Cart, OrderItem
│       ├── payment.py           # Payment, CashPayment, CardPayment, ChangeReserve
│       ├── stats.py             # Statistics
│       ├── data_manager.py      # DataManager — JSON 읽기/쓰기 전담
│       ├── kiosk_controller.py  # KioskController — 비즈니스 로직 조율
│       ├── cli_view.py          # CLIView — 터미널 인터페이스
│       └── gui/
│           ├── app.py           # run_gui() — QApplication 래퍼
│           ├── main_window.py   # KioskWindow — QStackedWidget + 네비게이션 API
│           ├── voice_service.py # VoiceService — TTS 음성 안내
│           └── screens/
│               ├── idle.py
│               ├── main_menu.py
│               ├── product_list.py
│               ├── customize.py
│               ├── cart.py
│               ├── payment_method.py
│               ├── cash_payment.py
│               ├── receipt.py
│               ├── admin_auth.py
│               └── admin_menu.py
├── tests/
└── project/
```

---

## 2. EDK 전환 후 목표 파일 구조

```
project/
├── src/
│   └── app/
│       ├── main.py
│       ├── exceptions.py        # 재활용
│       ├── medicine.py          # 신규 (product.py 교체)
│       ├── ingredient.py        # 재활용
│       ├── cart.py              # 재활용
│       ├── payment.py           # 재활용
│       ├── data_manager.py      # 수정
│       ├── drug_controller.py   # 신규 (kiosk_controller.py 교체)
│       ├── cli_view.py          # 수정
│       └── gui/
│           ├── app.py           # 재활용
│           ├── main_window.py   # 수정
│           ├── voice_service.py # 재활용
│           └── screens/
│               ├── idle.py              # 재활용
│               ├── symptom_select.py    # 신규
│               ├── medicine_list.py     # 신규
│               ├── medicine_detail.py   # 신규
│               ├── cart.py              # 재활용
│               ├── payment_method.py    # 재활용
│               ├── cash_payment.py      # 재활용
│               ├── receipt.py           # 재활용
│               ├── emergency.py         # 신규
│               ├── admin_auth.py        # 재활용
│               └── admin_menu.py        # 수정
```

---

## 3. 의존성 방향

```
exceptions.py
    ↑ (모든 파일이 import)

medicine.py   ingredient.py   payment.py
    ↑               ↑               ↑
    └──────────── cart.py           │
                    ↑               │
                    └────── data_manager.py
                                    ↑
                           drug_controller.py
                                    ↑
                              cli_view.py
                                    ↑
                                main.py
```

---

## 4. 클래스 책임 정의 (EDK 기준)

### medicine.py

**`Medicine(Product)`** — 의약품/영양제 1종

| 속성 | 설명 |
|------|------|
| `medicine_id` | 식별자 |
| `name` | 제품명 |
| `base_price` | 가격 |
| `is_available` | 판매 가능 여부 |
| `symptom_category` | 증상 카테고리 (두통/감기/소화불량 등) |
| `description` | 효능 설명 |
| `dosage` | 복용법 |
| `caution` | 주의사항 |

### 재활용 클래스 (변경 없음)

- `Ingredient` — 재고 수량 관리
- `Cart` / `OrderItem` — 장바구니
- `Payment` / `CashPayment` / `CardPayment` / `ChangeReserve` — 결제
- `DataManager` — JSON I/O (medicines.json / symptoms.json으로 전환)
- `exceptions.py` — 예외 클래스 전체

---

## 5. 설계 결정 이유

| 결정 | 이유 |
|------|------|
| Cart/Payment 재활용 | 실제 판매 서비스이므로 결제 로직 유지 필요 |
| PyQt6 QStackedWidget 유지 | 화면 전환 구조가 EDK 흐름과 동일 |
| medicine.py로 교체 | Product 구조 그대로, symptom_category 필드 추가로 최소 변경 |
| DrugController | KioskController 메서드 구조 재활용, 증상 매핑 로직 추가 |
