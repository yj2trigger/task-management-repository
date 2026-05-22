# 📊 ic-pbl 프로젝트 상태

> 마지막 업데이트: 2026-05-23  
> 원본 레포: [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl)

---

## 🔵 현재 단계

**STEP 10 — GUI 확장 시작**  
현재 활성 유닛: `GUI-01` — 레이아웃 뼈대 + StdoutRedirector (승인 대기)

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

## 🔵 GUI 개발 진행 현황

| 순서 | Unit | 파일 | 상태 |
|------|------|------|------|
| GUI-01 | 레이아웃 + stdout 리다이렉터 | gui/log_panel.py | 🔵 대기 |
| GUI-02 | CLI 출력 파싱 상태 머신 | gui/state_machine.py | ⬜ 대기 |
| GUI-03 | 숫자패드 위젯 | gui/widgets/numpad.py | ⬜ 대기 |
| GUI-04 | 메뉴 카드 위젯 | gui/widgets/menu_card.py | ⬜ 대기 |
| GUI-05 | 컨트롤 패널 (상태별 렌더) | gui/control_panel.py | ⬜ 대기 |
| GUI-06 | 메인 앱 통합 | gui/app.py | ⬜ 대기 |
| GUI-07 | GUI 진입점 | gui/gui_main.py | ⬜ 대기 |

---

## ⏭ 보류 중

- UNIT-07: discount.py (할인 정책) — 시간 여유 시 구현
- UNIT-13: pyproject.toml + README.md (패키징 설정) — 대기

---

## 🚨 현재 리스크

없음
