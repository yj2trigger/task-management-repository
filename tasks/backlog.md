# 📋 Backlog

> 아직 시작하지 않은 태스크 목록입니다.

---

## [ic-pbl] EDK 도메인 전환 — Core

- [ ] EDK-01: product.py → medicine.py — Medicine 클래스 (Coffee/Gummy 제거, symptom_category 추가)
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

## [ESG] 운영 개선

- [ ] IoT 실제 장치 연결 — SmartThings polling 구현 완료, 실제 세탁기에 센서 부착 필요
- [ ] 기술부채 #4: `ConnectionManager` 단일 인스턴스 — 다중 서버 인스턴스 시 WS 브로드캐스트 누락 (현재 Fly.io 1대라 잠재적 문제)

## [ESG] 향후 기능 (프로토타입 이후)

- [ ] 통계 UI — machine_status_logs + machine_power_logs 시간대별 혼잡도 그래프 (데이터 누적 중)
- [ ] 통계 기반 적응형 polling 개선 — machine_power_logs 이력으로 시간대별 평균 전력 변화 분석 → 야간/주간 경계 자동 보정, power_threshold_w 자동 제안 (ADR-007 확장)
- [ ] 전력 임계값 어드민 UI — 현재 API만 존재 (`PATCH /admin/settings`)
- [ ] PWA Push Notification — 백그라운드 알림 (현재 인앱 WS만)
