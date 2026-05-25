# ✅ Done

> 완료된 태스크 목록입니다.

---

## [ic-pbl] Core 구현 완료 (2026-05-12)

- [x] UNIT-01: exceptions.py — 16/16 PASS
- [x] UNIT-02: ingredient.py — 12/12 PASS
- [x] UNIT-03: product.py — 5/5 PASS
- [x] UNIT-04+05: cart.py (recipe 통합) — 35/35 PASS
- [x] UNIT-06: payment.py — 35/35 PASS
- [x] UNIT-08: stats.py — 12/12 PASS
- [x] UNIT-09: data_manager.py — 8/8 PASS
- [x] UNIT-10: kiosk_controller.py — 15/15 PASS
- [x] UNIT-11: cli_view.py — 수동 테스트 완료
- [x] UNIT-12: main.py — 임포트 검증 완료
- [x] 시나리오 테스트: test_scenarios.py — 29/29 PASS

## [ic-pbl] GUI 구현 완료 (PyQt6, 2026-05-22)

- [x] gui/app.py — QApplication 진입점
- [x] gui/main_window.py — KioskWindow, 네비게이션 API, 글로벌 스타일시트
- [x] gui/voice_service.py — TTS 음성 안내
- [x] gui/screens/idle.py — 대기 화면
- [x] gui/screens/main_menu.py — 메인 메뉴
- [x] gui/screens/product_list.py — 상품 목록
- [x] gui/screens/customize.py — 옵션 커스터마이징
- [x] gui/screens/cart.py — 장바구니
- [x] gui/screens/payment_method.py — 결제 수단 선택
- [x] gui/screens/cash_payment.py — 현금 결제
- [x] gui/screens/receipt.py — 영수증
- [x] gui/screens/admin_auth.py — 관리자 인증
- [x] gui/screens/admin_menu.py — 관리자 메뉴

## [ic-pbl] CI 인프라 (2026-05-26)

- [x] Gemini PR 자동 리뷰 워크플로 구축
- [x] Gemini 모델: `gemini-2.5-flash` → `gemini-2.0-flash-lite`
- [x] `develope` 브랜치 오타 → `develop` 이름 변경
- [x] 브랜치 전략: `feature/edk-XX` → `develop` → `main`

## [ic-pbl] EDK 도메인 전환 완료 (2026-05-26)

- [x] EDK-01: `medicine.py`, `symptom.py`, `test_medicine.py` 신규 + `product.py` 삭제 (PR #6)
- [x] EDK-03: `data_manager.py` — `medicines.json` / `symptoms.json` 로드, 샘플 데이터 5의약품 + 8증상 (PR #7)
- [x] EDK-02: `drug_controller.py` — 증상→의약품 매핑 4메서드, 테스트 11개 (PR #8)

---

## [ESG] 설계 완료

- [x] 1~7단계: 서비스 정의 → 배포 전략

## [ESG] 구현 완료

- [x] 구현 1~10단계 (2026-05-23~25)

## [ESG] 기능 추가 / 버그 수정 / 기술부채 (2026-05-25)

- [x] 대기순번 실시간, PWA, 관리자 페이지, 설정, IoT 엔드포인트
- [x] 로딩 버그, 모바일 UI, WS 타입, 대기열 상태, 어드민 알림 수정
- [x] datetime/Alembic/pytest/GitHub 협업 설정/CI·CD 워크플로 정비
