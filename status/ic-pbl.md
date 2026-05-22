# 📊 ic-pbl 프로젝트 상태 (EDK)

> 마지막 업데이트: 2026-05-23
> 원본 레포: [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl)

---

## ⚠️ 도메인 전환 진행 중

**기존**: Micro-Factory Kiosk (커피/영양구미)
**변경**: EDK — Erica Drug King (증상 선택 기반 일반의약품 정보 제공 키오스크)

기존 PyQt6 아키텍처를 재활용하고 도메인만 교체하는 전략으로 진행.

---

## 🔵 현재 단계

**EDK-01 진행 중**: `product.py` → `medicine.py` 리팩터링

---

## ✅ 재활용 확정 유닛

| 파일 | 재활용 방식 |
|------|-----------|
| exceptions.py | 그대로 재활용 |
| ingredient.py | 의약품 재고 수량으로 재활용 |
| data_manager.py | 의약품 JSON 데이터 관리로 재활용 |
| gui/app.py | 그대로 재활용 |
| gui/voice_service.py | 그대로 재활용 |
| gui/screens/admin_auth.py | 그대로 재활용 |

---

## 🔄 EDK 전환 작업 목록 (Core)

| 작업 | 파일 | 상태 |
|------|------|------|
| EDK-01 | product.py → medicine.py | 🔵 진행 중 |
| EDK-02 | cart.py 단순화 (결제 제거) | ⬜ 대기 |
| EDK-03 | payment.py 제거 | ⬜ 대기 |
| EDK-04 | kiosk_controller.py → drug_controller.py | ⬜ 대기 |
| EDK-05 | data_manager.py 데이터 구조 전환 | ⬜ 대기 |
| EDK-06 | main.py 초기화 로직 교체 | ⬜ 대기 |
| EDK-07 | cli_view.py 증상 탐색 흐름으로 교체 | ⬜ 대기 |

## 🔄 EDK 전환 작업 목록 (GUI)

| 작업 | 기존 → 신규 | 상태 |
|------|-----------|------|
| GUI-EDK-01 | main_window.py 네비게이션 교체 | ⬜ 대기 |
| GUI-EDK-02 | main_menu.py → symptom_select.py | ⬜ 대기 |
| GUI-EDK-03 | product_list.py → medicine_list.py | ⬜ 대기 |
| GUI-EDK-04 | customize.py → medicine_detail.py | ⬜ 대기 |
| GUI-EDK-05 | receipt.py → caution.py | ⬜ 대기 |
| GUI-EDK-06 | (신규) emergency.py | ⬜ 대기 |
| GUI-EDK-07 | admin_menu.py 수정 | ⬜ 대기 |
| GUI-EDK-08 | cart.py / payment_method.py / cash_payment.py 제거 | ⬜ 대기 |

---

## 🚨 현재 리스크

- 기존 테스트(test_*.py)가 구 도메인 기반 — EDK 전환 후 재작성 필요
- payment.py 관련 테스트 전체 폐기 예정
