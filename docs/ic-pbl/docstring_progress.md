# ic-pbl 주석 인수인계 작업 진행 상황

> 목적: 주니어 개발자 인수인계용 상세 주석 작성
> 원칙: 거의 매 줄 / 매 기능에 주석. WHY 위주. 의존성 설명 포함. 시행착오 이력 포함.
> 작성 언어: 한국어
> **상태: 전체 완료 (2026-06-05). 파일 단위 헤더 블록 전체 파일 추가 완료.**

## 2026-06-05 추가 작업

**파일 레벨 헤더 블록** — 전체 25개 소스 파일에 공통 패턴으로 추가 (branch: `chore/add-file-headers`):

```
# ──────────────────────────────────────────────────────
# filename.py — 한 줄 역할
# [역할]   ...
# [설계 원칙 / 버그 수정 이력]   ...
# [의존성]  import: / 이 파일을 사용하는 곳:
# ──────────────────────────────────────────────────────
```

인라인 주석만으로는 파일 전체 위치를 파악하기 어려워, 파일 진입 시 역할·의존성을 한눈에 파악할 수 있도록 추가.

**QPushButton 렌더링 버그 수정** — `customize.py` 수량 버튼 (branch: `fix/qty-btn-padding`):
글로벌 스타일시트 `padding: 10px 20px`이 `setFixedSize(44, 44)` 버튼에 적용되어 텍스트 영역이 4px로 압축됨.
`setStyleSheet("padding: 2px; font-size: 20px; font-weight: bold;")` 인라인 재정의로 해결.

---

## 파일 순서 (의존성 낮은 것부터)

| # | 파일 | 상태 | 비고 |
|---|------|------|------|
| 1 | `exceptions.py` | ✅ 완료 | 모든 파일이 import |
| 2 | `ice_cream.py` | ✅ 완료 | 상품 도메인 |
| 3 | `ingredient.py` | ✅ 완료 | 재고 도메인 |
| 4 | `option.py` | ✅ 완료 | 옵션 도메인 |
| 5 | `cart.py` | ✅ 완료 | 장바구니 |
| 6 | `payment.py` | ✅ 완료 | 결제 + 잔돈 |
| 7 | `stats.py` | ✅ 완료 | 통계 |
| 8 | `password_utils.py` | ✅ 완료 | 관리자 인증 |
| 9 | `data_manager.py` | ✅ 완료 | JSON 영속성 |
| 10 | `kiosk_controller.py` | ✅ 완료 | 비즈니스 로직 통합 |
| 11 | `main.py` | ✅ 완료 | 진입점 |
| 12 | `gui/app.py` | ✅ 완료 | GUI 진입점 |
| 13 | `gui/voice_service.py` | ✅ 완료 | TTS |
| 14 | `gui/main_window.py` | ✅ 완료 | 화면 전환 허브 |
| 15 | `gui/widgets/colors.py` | ✅ 완료 | 색상 팔레트 |
| 16 | `gui/widgets/stick_preview.py` | ✅ 완료 | 스틱 미리보기 |
| 17 | `gui/widgets/scoop_preview.py` | ✅ 완료 | 스쿱 미리보기 |
| 18 | `gui/screens/idle.py` | ✅ 완료 | 대기 화면 |
| 19 | `gui/screens/main_menu.py` | ✅ 완료 | 상품 목록 |
| 20 | `gui/screens/customize.py` | ✅ 완료 | 옵션 커스터마이징 |
| 21 | `gui/screens/cart.py` | ✅ 완료 | 장바구니 화면 |
| 22 | `gui/screens/payment_method.py` | ✅ 완료 | 결제 수단 선택 |
| 23 | `gui/screens/cash_payment.py` | ✅ 완료 | 현금 결제 |
| 24 | `gui/screens/receipt.py` | ✅ 완료 | 영수증 |
| 25 | `gui/screens/admin_auth.py` | ✅ 완료 | 관리자 인증 화면 |
| 26 | `gui/screens/admin_menu.py` | ✅ 완료 | 관리자 메뉴 |

---

## 주석 작성 원칙

1. **WHY 위주**: "이렇게 했다"가 아니라 "왜 이렇게 했는가"
2. **의존성 명시**: "이 클래스는 X.py의 Y를 쓴다" 방식으로 파일 이동 없이 이해 가능
3. **시행착오 포함**: management repo의 process.md 기반으로 도메인 전환, 버그 수정 이력 언급
4. **경계값 설명**: 예외가 발생하는 조건을 항상 명시
5. **코드 블록 단위 설명**: 함수 전체 의도 + 각 줄 세부 설명 병행

---

## 시행착오 핵심 이력 (주석에 반영할 것)

- **도메인 전환**: 처음에는 의약품(EDK) 키오스크로 구현. `Medicine`, `SymptomGroup` 등이 있었음.
  `IceCreamProduct`, `OptionGroup`으로 리팩터링 (commit: `7654c35`).
- **현금 버그 (98770e0)**: `CashPayment.process()` 에서 투입한 지폐를 `ChangeReserve`에 먼저 더한 후
  잔돈을 뺴야 하는데, 권종별 카운트(`inserted_bills`)가 reserve에 반영되지 않았던 버그.
  Gemini AI 코드 리뷰가 지적해서 발견.
- **GUI 재설계**: 초기에 tkinter + CLI 파싱 방식 계획 → PyQt6 QStackedWidget 방식으로 전면 재설계.
  (참고: `gui_architecture.md`)
- **scoop3 숨김 로직**: 스쿱 2개에서 멈추면 3번째 슬롯을 숨기는 로직이 customize.py에 있음.
  `scoop_stop` 옵션 ID 규칙으로 처리.
