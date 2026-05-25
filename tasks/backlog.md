# 📋 Backlog

> 아직 시작하지 않은 태스크 목록입니다.

---

## [ic-pbl] EDK 도메인 전환 — Core

> EDK-01은 PR #6 리뷰 중 → `in-progress.md` 참고

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

## [ESG] IoT 구현

> 설계 상세: [ADR-007 — Adaptive Polling 전략](../portfolio/ESG/decisions/ADR-007-iot-polling-strategy.md)

- [ ] IoT-01: Tuya WiFi 플러그 실제 연동 — IOT_DEVICE_KEY 설정 + 장치 페어링
- [ ] IoT-02: Adaptive polling 구현 — Batch API + Mode별 interval + 심야 감소 (ADR-007 하이브리드)
- [ ] IoT-03: Admin 패널 — polling 통계 섹션 추가 (현재 interval · 각 요소 기여 · 월 API 사용량)
- [ ] IoT-04: 사용자 화면 — 현재 polling 빈도 공개 (DashboardPage 하단)
- [ ] IoT-05: Phase 2 — 4주 데이터 수집 후 요일×시간대 통계 기반 interval 자동 조절

## [ESG] 운영 개선

- [ ] 기술부채 #4: `ConnectionManager` 단일 인스턴스 — 다중 서버 인스턴스 시 WS 브로드캐스트 누락 (현재 Fly.io 1대라 잠재적 문제)

## [ESG] 향후 기능 (프로토타입 이후)

- [ ] PWA Push Notification — 백그라운드 알림 (현재 인앱 WS만)
- [ ] 통계 — `machine_status_logs` 테이블 + 시간대별 혼잡도 API
