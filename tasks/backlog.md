# 📋 Backlog

> 아직 시작하지 않은 태스크 목록입니다.

---

## [ic-pbl] EDK 도메인 전환 — Core

- [ ] EDK-02: cart.py 단순화 — 결제 로직 제거, 관심 의약품 선택 목록으로 변경
- [ ] EDK-03: payment.py 제거 (정보 제공 서비스 — 결제 불필요)
- [ ] EDK-04: kiosk_controller.py → drug_controller.py — 증상→의약품 매핑 로직 전환
- [ ] EDK-05: data_manager.py — medicines.json / symptoms.json 데이터 구조 적용
- [ ] EDK-06: main.py — 의약품 데이터 초기화 로직으로 교체
- [ ] EDK-07: cli_view.py — 증상 선택 → 의약품 정보 탐색 흐름으로 교체

## [ic-pbl] EDK 도메인 전환 — GUI

- [ ] GUI-EDK-01: main_window.py — 네비게이션 API를 EDK 화면 흐름으로 교체
- [ ] GUI-EDK-02: main_menu.py → symptom_select.py — 증상 카테고리 선택 화면
- [ ] GUI-EDK-03: product_list.py → medicine_list.py — 의약품 목록 화면
- [ ] GUI-EDK-04: customize.py → medicine_detail.py — 의약품 상세 정보 화면
- [ ] GUI-EDK-05: receipt.py → caution.py — 복용 주의사항 안내 화면
- [ ] GUI-EDK-06: (신규) emergency.py — 응급 상황 안내 화면 추가
- [ ] GUI-EDK-07: admin_menu.py — 의약품 정보/재고 관리로 수정
- [ ] GUI-EDK-08: cart.py / payment_method.py / cash_payment.py 제거

## [ic-pbl] 마무리

- [ ] 테스트 재작성 — EDK 도메인 기준 단위 테스트
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
