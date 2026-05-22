# CURRENT_STATE — EDK (ic-pbl)

> Last Update: 2026-05-23
> Phase: 도메인 전환 — EDK(Erica Drug King) 리팩터링 시작

---

## ⚠️ 프로젝트 방향 전환

**기존**: Micro-Factory Kiosk (커피/영양구미 판매)
**변경**: EDK — 증상 선택 기반 일반의약품/영양제 실제 판매 키오스크

기존 PyQt6 GUI 아키텍처(QStackedWidget, screens/, voice_service)는 그대로 재활용.
결제 시스템(payment.py, cart.py, ChangeReserve)은 유지 — 실제 판매이므로 필수.

---

## Current Active Unit

**EDK-01**: `product.py` → `medicine.py` 리팩터링
- Coffee, Gummy → Medicine 클래스로 교체
- product_type → symptom_category 개념으로 전환

---

## ✅ 재활용 확정 유닛

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

### Core

| 작업 | 파일 | 상태 |
|------|------|------|
| EDK-01 | product.py → medicine.py | 🔵 진행 중 |
| EDK-02 | kiosk_controller.py → drug_controller.py | ⬜ 대기 |
| EDK-03 | data_manager.py 데이터 구조 전환 | ⬜ 대기 |
| EDK-04 | main.py 초기화 로직 교체 | ⬜ 대기 |
| EDK-05 | cli_view.py 증상 탐색 → 구매 → 결제 흐름 | ⬜ 대기 |

### GUI (신규/수정)

| 작업 | 파일 | 상태 |
|------|------|------|
| GUI-EDK-01 | main_window.py 네비게이션 교체 | ⬜ 대기 |
| GUI-EDK-02 | main_menu.py → symptom_select.py | ⬜ 대기 |
| GUI-EDK-03 | product_list.py → medicine_list.py | ⬜ 대기 |
| GUI-EDK-04 | customize.py → medicine_detail.py | ⬜ 대기 |
| GUI-EDK-05 | (신규) emergency.py | ⬜ 대기 |
| GUI-EDK-06 | admin_menu.py 의약품 관리로 수정 | ⬜ 대기 |

---

## 목표 파일 구조 (전환 후)

```
src/app/
├── main.py
├── drug_controller.py
├── cli_view.py
├── medicine.py              # 신규 (product.py 교체)
├── ingredient.py            # 재활용
├── cart.py                  # 재활용
├── payment.py               # 재활용
├── data_manager.py
├── exceptions.py            # 재활용
└── gui/
    ├── app.py               # 재활용
    ├── main_window.py       # 수정
    ├── voice_service.py     # 재활용
    └── screens/
        ├── idle.py              # 재활용
        ├── symptom_select.py    # 신규
        ├── medicine_list.py     # 신규
        ├── medicine_detail.py   # 신규
        ├── cart.py              # 재활용
        ├── payment_method.py    # 재활용
        ├── cash_payment.py      # 재활용
        ├── receipt.py           # 재활용
        ├── emergency.py         # 신규
        ├── admin_auth.py        # 재활용
        └── admin_menu.py        # 수정
```

---

## 데이터 파일 구성

| 파일 | 내용 |
|------|------|
| `medicines.json` | 제품 목록 (이름, 효능, 복용법, 주의사항, 가격, 재고, 증상 카테고리) |
| `symptoms.json` | 증상 카테고리 정의 |
| `change_reserve.json` | 잔돈 보유량 (재활용) |
| `admin_config.json` | 관리자 비밀번호 (재활용) |

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
