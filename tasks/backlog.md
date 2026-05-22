# 📋 Backlog

> 아직 시작하지 않은 태스크 목록입니다.

---

## [ic-pbl] EDK 도메인 전환 — Core

- [ ] EDK-02: kiosk_controller.py → drug_controller.py — 증상→의약품 매핑 로직 전환
- [ ] EDK-03: data_manager.py — medicines.json / symptoms.json 데이터 구조 적용
- [ ] EDK-04: main.py — 의약품 데이터 초기화 로직으로 교체
- [ ] EDK-05: cli_view.py — 증상 선택 → 제품 탐색 → 결제 흐름으로 교체

> ℹ️ cart.py / payment.py / ChangeReserve 는 **실제 판매이므로 그대로 재활용** (제거 불필요)

## [ic-pbl] EDK 도메인 전환 — GUI (신규/수정만)

- [ ] GUI-EDK-01: main_window.py — 네비게이션 API를 EDK 화면 흐름으로 교체
- [ ] GUI-EDK-02: main_menu.py → symptom_select.py — 증상 카테고리 선택 화면
- [ ] GUI-EDK-03: product_list.py → medicine_list.py — 제품 목록 화면
- [ ] GUI-EDK-04: customize.py → medicine_detail.py — 제품 상세 + 장바구니 담기 화면
- [ ] GUI-EDK-05: (신규) emergency.py — 응급 상황 안내 화면 추가
- [ ] GUI-EDK-06: admin_menu.py — 의약품 정보/재고 관리로 수정

> ℹ️ cart.py / payment_method.py / cash_payment.py / receipt.py 는 **그대로 재활용**

## [ic-pbl] 마무리

- [ ] 테스트 재작성 — EDK 도메인 기준 단위 테스트 (cart/payment 테스트는 재활용 가능)
- [ ] pyproject.toml + README.md — 패키징 설정

---

## [ESG]

- [ ] 3단계: 프론트엔드 구조 설계
- [ ] 4단계: 백엔드 구조 설계
- [ ] 5단계: DB 및 데이터 흐름 설계
- [ ] 6단계: Docker 환경 구성
- [ ] 7단계: Railway 배포 전략
- [ ] 8단계: CI/CD 자동화
- [ ] 9단계: 운영 고려사항
