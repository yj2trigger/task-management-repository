# ✅ Done

> 완료된 태스크 목록입니다.

---

## [MAP] map-service-user 인증 도메인 + 코드 개선 (2026-05-28)

- [x] Swagger/OpenAPI 완전 제거 → Spring REST Docs 마이그레이션
  - springdoc 의존성 제거, `AuthApi` 인터페이스 삭제, `SwaggerConfig` 삭제
  - `build.gradle`: asciidoctor 플러그인 + `spring-restdocs-mockmvc` 추가
  - `AuthControllerRestDocsTest` 신규 작성 (5개 엔드포인트)
  - `src/docs/asciidoc/index.adoc` 신규 작성
- [x] 테스트 수정
  - `AuthControllerTest`: `@AutoConfigureMockMvc(addFilters = false)` 추가 → 전원 403 수정
  - `KakaoOAuthServiceTest`: stub ID 오류 수정 (`eq(999L)` → `eq(9999999999L)`)
- [x] `JwtService`: `@PostConstruct` 제거 → 생성자에서 `JwtParser` 초기화 (단위 테스트 직접 생성 지원)
- [x] `KakaoOAuthService`: `RestClient` 필드 초기화 → `@Bean` 주입으로 변경 (테스트 가능), `parseConnectedAt` timezone 파싱 fix (`OffsetDateTime.parse`)
- [x] `GlobalExceptionHandler`: `HttpMessageNotReadableException` / `MissingRequestHeaderException` / `HttpRequestMethodNotSupportedException` 핸들러 추가
- [x] `RateLimitService`: `INCR+EXPIRE` 두 명령 → `DefaultRedisScript` Lua 스크립트 원자 실행 (race condition 제거)
- [x] `RefreshToken`: `device` 필드 제거 + `V2__remove_device_id_from_refresh_tokens.sql` Flyway 마이그레이션 생성
- [x] `CorsProperties` 신설, `SecurityConfig` CORS 외부화 (prod.yaml: `CORS_ALLOWED_ORIGINS` 환경변수)

---

## [ic-pbl] Core 구현 완료 (2026-05-12)

- [x] UNIT-01~12: 전체 테스트 PASS
- [x] 시나리오 테스트: 29/29 PASS

## [ic-pbl] GUI 구현 완료 (PyQt6, 2026-05-22)

- [x] gui/app.py, main_window.py, voice_service.py
- [x] 화면 7종: idle, main_menu, product_list, customize, cart, payment_method, cash_payment, receipt
- [x] 관리자 화면: admin_auth, admin_menu

## [ic-pbl] CI 인프라 (2026-05-26)

- [x] Gemini PR 자동 리뷰 워크플로 (`gemini-2.5-flash-lite`)
- [x] `develope` → `develop` 이름 수정, 브랜치 전략 수립

## [ic-pbl] EDK 도메인 전환 완료 (2026-05-26)

- [x] EDK-01: `medicine.py`, `symptom.py`, `test_medicine.py` 신규 + `product.py` 삭제 (PR #6)
- [x] EDK-03: `data_manager.py` — `medicines.json` / `symptoms.json`, 샘플 5의약품 + 8증상 (PR #7)
- [x] EDK-02: `drug_controller.py` — 증상→의약품 매핑 4메서드 (PR #8)
- [x] EDK-04: `main.py` — `DrugController` + `DataManager` 초기화로 교체, Coffee/Gummy 제거 (PR #9)
- [x] EDK-05: `cli_view.py` — 증상 선택 → 의약품 탐색 → 결제 흐름, CLI 실행 가능 (PR #10)

## [ic-pbl] GUI-EDK 도메인 GUI 전환 (PR #11 머지, 2026-05-26)

- [x] GUI-EDK-01: `main_window.py` — `KioskWindow(controller, cart, change_reserve)`, EDK 네비게이션 API
- [x] GUI-EDK-02: `symptom_select.py` 신규 — 증상 그리드, 응급 빨간색, 장바구니 요약
- [x] GUI-EDK-03: `medicine_list.py` 신규 — 증상별 의약품 카드
- [x] GUI-EDK-04: `medicine_detail.py` 신규 — 의약품 상세 + 수량 스피너 + 장바구니
- [x] GUI-EDK-05: `emergency.py` 신규 — 응급 경고 + 119 안내
- [x] GUI-EDK-06: `admin_menu.py` 재작성 — 의약품 ON/OFF 및 가격, 재료 관련 기능 제거
- [x] 개편 화면: `idle.py`, `cart.py`, `payment_method.py`, `cash_payment.py`, `admin_auth.py`, `app.py`, `main.py`

## [ic-pbl] 테스트 재작성 (PR #13 제출, 2026-05-26)

- [x] 삭제: `test_product.py`, `test_ingredient.py`, `test_controller.py`, `test_scenarios.py`, `test_cli_integration.py`
- [x] `conftest.py` 재작성: EDK fixtures (Medicine/Symptom/Cart/ChangeReserve), pygame mock
- [x] `test_cart.py` 재작성: Medicine 기반, 재고 차감 테스트 제거
- [x] `test_gui_app.py` 재작성: EDK KioskWindow 시그니처, 화면 전환 검증
- [x] `test_gui_screens.py` 재작성: SymptomSelect/MedicineList/Detail/Emergency/Cart 등
- [x] `test_admin_cash.py` 업데이트: subprocess → mock stdin/stdout 직접 호출
- [x] `test_edk_integration.py` 신규: 증상선택 → 장바구니 → 결제 통합 시나리오

## [ic-pbl] 보안 강화 — 관리자 비밀번호 해시 (PR #15, 2026-05-26)

- [x] 관리자 비밀번호 평문 → scrypt 해시 저장 (`hashlib.scrypt`, stdlib)
- [x] 저장 형식: `scrypt$<salt_hex>$<hash_hex>`, `hmac.compare_digest` 타이밍 안전 비교
- [x] `main.py` 최초 실행 시 평문 감지 → 자동 해시 마이그레이션 (사용자 개입 없음)
- [x] 잔돈 보유 데이터(`change_reserve.json`) 1000원+ 단위만 유지 확인

## [ic-pbl] 가격 정책 정규화 (2026-05-26)

- [x] 의약품 가격 1000원 단위 정규화
  - 타이레놀 500mg: 5,500 → 6,000원
  - 베아제: 3,500 → 4,000원
  - 훼스탈플러스: 4,500 → 5,000원
- [x] 옵션 추가금 최소 1,000원 단위 정규화 (10개 항목)
  - 200~300원 → 1,000원 (Medium, 2샷, 당도 많이, 크림 있음, 레몬, 오메가3, 파우치)
  - 500원 → 1,000원 (Large, 콜라겐, 10알)
- [x] 잔돈 시스템 호환 확인 — `change_reserve.json` 이미 1,000원+ 단위만 보유

---

## [ESG] 설계 완료

- [x] 1~7단계 전체

## [ESG] 구현 완료

- [x] 구현 1~10단계 (2026-05-23~25)

## [ESG] 기능 추가 / 버그 수정 / 기술부체 (2026-05-25)

- [x] 대기순번 실시간, PWA, 관리자, 설정, IoT 엔드포인트 등
- [x] 로딩 버그, 모바일 UI, WS 타입, 대기열 상태, 어드민 알림 수정
- [x] datetime/Alembic/pytest/GitHub 협업 설정/CI·CD
