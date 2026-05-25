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

- [x] Gemini PR 자동 리뷰 워크플로 구축 (`gemini-review.yml`)
  - SHA 기반 immutable diff, 안전한 JSON 구성, 개행 처리
  - `opened` / `synchronize` / `reopened` 트리거
  - `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`
- [x] Gemini 모델: `gemini-2.5-flash` → `gemini-2.0-flash-lite` (지출 한도 초과 대응)
- [x] `develope` 브랜치 오타 → `develop` 이름 변경
- [x] 브랜치 전략: `feature/edk-XX` → `develop` → `main`

## [ic-pbl] EDK-01 완료 (2026-05-26)

- [x] `medicine.py` 신규: `Medicine` 클래스 (`symptom_categories: list[str]`, `description`, `dosage`, `caution`)
- [x] `symptom.py` 신규: `Symptom`, `SymptomGroup` 클래스 (`is_emergency`, O(1) dict 룩업)
- [x] `tests/test_medicine.py` 신규: 11개 단위 테스트
- [x] `product.py` 삭제 (Coffee/Gummy 도메인 제거, git history 보존)
- [x] PR #6 `feature/edk-01-medicine` → `develop` merge 완료

---

## [ESG] 설계 완료

- [x] 1단계: 서비스 정의
- [x] 2단계: 전체 시스템 아키텍처
- [x] 3단계: 프론트엔드 구조 설계
- [x] 4단계: 백엔드 구조 설계
- [x] 5단계: DB 및 데이터 흐름 설계
- [x] 6단계: Docker 환경 구성
- [x] 7단계: 배포 전략 (Railway → Fly.io + Supabase + Vercel 전환)

## [ESG] 구현 완료

- [x] 구현 1단계: 프로젝트 골격 + Docker (2026-05-23)
- [x] 구현 2단계: 성별 선택 UI (2026-05-24)
- [x] 구현 3단계: Auth — JWT register/login (2026-05-24)
- [x] 구턄 4단계: Machines + Mode A/B/C (2026-05-24)
- [x] 구현 5단계: SoftReserve + Queue (2026-05-24)
- [x] 구현 6단계: WebSocket (2026-05-24)
- [x] 구현 7단계: Docker Compose 로컬 실행 (2026-05-24)
- [x] 구현 8단계: CI/CD — GitHub Actions → Fly.io + Vercel (2026-05-24~25)
- [x] 구현 9단계: 운영 고려사항 — rate limit, soft_reserve 중복 방지 (2026-05-24)
- [x] 구현 10단계: 이메일 인증 — @hanyang.ac.kr + 6자리 OTP + Gmail SMTP (2026-05-25)

## [ESG] 기능 추가 (2026-05-25)

- [x] 대기 순번 실시간 표시 — WS queue_position_updated 이벤트
- [x] 모바일 PWA — standalone manifest + Fullscreen API
- [x] 관리자 페이지 — 층별 세탁기 상태 토글 (role=admin 필요)
- [x] 비밀번호 / 아이디 변경 (설정 페이지)
- [x] IoT 신호 수신 엔드포인트

## [ESG] 버그/UI 수정 (2026-05-25)

- [x] 대시보드 loading 무한 버그
- [x] GenderSelectPage 성별별 구역 안내
- [x] LoginPage 비밀번호 표시 토글
- [x] WsMessage TypeScript 타입 누락
- [x] 모바일 horizontal overflow
- [x] 대기열 상태 복원
- [x] Mode B/C 상태 관리 버그
- [x] 어드민 available 전환 시 큐 알림 미발송

## [ESG] 기술부채 해결 + 협업 인프라 (2026-05-25)

- [x] 기술부채 #1~3: datetime, DateTime timezone, Alembic 마이그레이션
- [x] pytest 커버리지 32 → 42 cases
- [x] GitHub 협업 설정 — branch protection, PR 템플릿, ONBOARDING.md
- [x] CI/CD workflow 정비, 브랜치 전략 수립
