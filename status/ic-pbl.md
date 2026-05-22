# 📊 ic-pbl 프로젝트 상태

> 마지막 업데이트: 2026-05-23  
> 원본 레포: [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl)

---

## ✅ 현재 단계

**GUI 구현 완료 — 패키징 / 마무리 단계**  
PyQt6 기반 10개 화면 + VoiceService 전체 구현 완료

---

## ✅ 완료된 Core 유닛

| Unit | 파일 | 테스트 결과 | 완료일 |
|------|------|------------|--------|
| UNIT-01 | exceptions.py | 16/16 PASS | 2026-05-11 |
| UNIT-02 | ingredient.py | 12/12 PASS | 2026-05-12 |
| UNIT-03 | product.py | 5/5 PASS | 2026-05-12 |
| UNIT-04+05 | cart.py (recipe 통합) | 35/35 PASS | 2026-05-12 |
| UNIT-06 | payment.py | 35/35 PASS | 2026-05-12 |
| UNIT-08 | stats.py | 12/12 PASS | 2026-05-12 |
| UNIT-09 | data_manager.py | 8/8 PASS | 2026-05-12 |
| UNIT-10 | kiosk_controller.py | 15/15 PASS | 2026-05-12 |
| UNIT-11 | cli_view.py | 수동 테스트 완료 | 2026-05-12 |
| UNIT-12 | main.py | 임포트 검증 완료 | 2026-05-12 |
| 시나리오 | test_scenarios.py | 29/29 PASS | 2026-05-12 |

**총 테스트: 167/167 PASS** ✅

---

## ✅ 완료된 GUI 유닛 (PyQt6 기반)

| Unit | 파일 | 설명 | 상태 |
|------|------|------|------|
| GUI-APP | gui/app.py | QApplication 진입점 | ✅ 완료 |
| GUI-WIN | gui/main_window.py | KioskWindow, 네비게이션 API, 글로벌 스타일시트 | ✅ 완료 |
| GUI-VOICE | gui/voice_service.py | TTS 음성 안내 | ✅ 완료 |
| GUI-S01 | gui/screens/idle.py | 대기 화면 | ✅ 완료 |
| GUI-S02 | gui/screens/main_menu.py | 메인 메뉴 | ✅ 완료 |
| GUI-S03 | gui/screens/product_list.py | 상품 목록 | ✅ 완료 |
| GUI-S04 | gui/screens/customize.py | 옵션 커스터마이징 | ✅ 완료 |
| GUI-S05 | gui/screens/cart.py | 장바구니 | ✅ 완료 |
| GUI-S06 | gui/screens/payment_method.py | 결제 수단 선택 | ✅ 완료 |
| GUI-S07 | gui/screens/cash_payment.py | 현금 결제 | ✅ 완료 |
| GUI-S08 | gui/screens/receipt.py | 영수증 | ✅ 완료 |
| GUI-S09 | gui/screens/admin_auth.py | 관리자 인증 | ✅ 완료 |
| GUI-S10 | gui/screens/admin_menu.py | 관리자 메뉴 | ✅ 완료 |

---

## ⏭ 보류 중

- UNIT-07: discount.py — 할인 정책 (후순위)
- UNIT-13: pyproject.toml + README.md — 패키징 설정

---

## 🚨 현재 리스크

없음
