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

---

## [ESG] 설계 완료

- [x] 1단계: 서비스 정의
- [x] 2단계: 전체 시스템 아키텍처
- [x] 3단계: 프론트엔드 구조 설계

## [ESG] 구현 완료

- [x] 구현 1단계: 프로젝트 골격 + Docker (2026-05-23)
- [x] 구현 2단계: 성별 선택 UI (2026-05-24)
  - src/types/user.ts — Gender 타입
  - src/store/authStore.ts — Zustand + localStorage persist
  - src/pages/GenderSelectPage.tsx — 남/여 선택 UI
  - src/App.tsx — /gender 라우트, 미선택 시 자동 redirect
  - src/__tests__/authStore.test.ts — 단위 테스트 5개
  - vite.config.ts — jsdom 환경 추가
