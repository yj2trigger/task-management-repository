# ic-pbl — 개발 과정 (Process)

> 작성일: 2026-06-03 00:00
> 대상: 발표 준비 완료 기준, 팀 "안산ic"

---

## 1. 제품 선택 과정

### 1.1 핵심 질문

micro-factory kiosk 형태에서 가장 이익을 낼 수 있는 종목은?

조건: **사용자가 제품을 직접 커스터마이즈할 수 있는 키오스크**

### 1.2 후보 검토

| 후보 | 검토 내용 | 결정 |
|------|----------|------|
| 의약품 키오스크 | 증상 선택 기반 판매. 조합으로 개인 취향 표현 어렵고, 커스터마이즈 특성 활용 불가. 첫 구현 도메인. | 탈락 |
| 커피 키오스크 | 커스터마이징 가능하나 카페 포화 시장, 선택 유인 부족. | 탈락 |
| 아이스크림 키오스크 | 형태/코팅/토핑/맛 자유 조합. SNS 업로드 가치 있는 비주얼. 배스킨라빈스 완제품 대비 차별화. | **채택** |

### 1.3 선택 근거

인스타그램 등 SNS에서 음식 소비가 자기 표현 수단으로 기능하는 문화적 맥락:
- *'내가 고른 조합 = 나라는 사람'*을 보여줄 수 있어야 한다.
- 조합 결과물이 SNS에 올릴 만한 비주얼이어야 한다.

아이스크림은 이 두 조건을 동시에 충족한다.

---

## 2. 도메인 전환 이력

| 단계 | 내용 | 커밋 기준 |
|------|------|---------|
| 초기 | 의약품 키오스크 (EDK) 구현 — 증상 선택, Medicine 클래스, 관리자 메뉴 | `13857d4 Merge main into develop` |
| 전환 결정 | 의약품 → 아이스크림 도메인으로 리팩터링 결정 | `7654c35 refactor: 의약품 도메인 → 아이스크림 키오스크 전환` |
| 데이터 갱신 | products.json / options.json 아이스크림 데이터로 교체 | `cc30210 data: 아이스크림 도메인 데이터 파일 갱신` |
| UI 구현 | 커스터마이즈 화면 + stick/scoop 미리보기 위젯 | `d6e31bd feat: 커스터마이즈 화면 UI + stick/scoop 미리보기 위젯 추가` |
| 버그 수정 | 결제/장바구니/재고/관리자 버그 다수 수정 | `9104dbf fix: 결제/장바구니/재고/관리자 버그 다수 수정` |
| TTS 추가 | 음성 안내, 스크롤 UX 개선 | `848d9d9 feat: tts 추가, 스크롤 UX 개선` |
| 현금 버그 수정 | 현금 투입 시 권종별 카운트 reserve에 반영 | `98770e0 fix: 현금 투입 시 권종별 카운트 reserve에 반영` |

---

## 3. 협업 방식

### 3.1 GitHub 브랜치 전략

```
feature/* → develop → main
```

- `main` 브랜치: PR 생성 + 승인 + 체크 통과 3가지 모두 충족 시에만 merge 허용
- 어느 한 쪽이 검토 없이 직접 push하거나 merge하는 상황을 구조적으로 차단
- 기능 단위로 브랜치를 분리하여 PR을 각각 제출

### 3.2 Gemini AI 자동 코드 리뷰

모든 PR에 Gemini가 자동으로 코드 리뷰 댓글을 작성한다:
- 코드 품질, 잠재 버그를 한국어로 분석
- 사람이 놓친 부분을 AI가 보완하는 구조

실제로 현금 투입 버그(`98770e0`)는 Gemini 리뷰가 지적한 항목에서 발견됨.

> CI 구현 이력: Gemini review 워크플로 제거 후 재구현 (`c00523e` → `efba9b3` → `f6ab97d`)

---

## 4. 설계 결정 이력

| 결정 | 이유 |
|------|------|
| Business Layer / GUI Layer 분리 | GUI가 비즈니스 로직을 전혀 모르게 함 — 화면 변경이 비즈니스 로직에 영향 없음 |
| Cart / Payment 재활용 | 도메인 전환에도 장바구니/결제 로직 변경 없음 |
| QStackedWidget 유지 | 아이스크림 화면 흐름이 EDK 흐름과 동일 구조 |
| scrypt 비밀번호 해시 | 단방향 해시, 레거시 평문 PIN 자동 마이그레이션 지원 |
| JSON 파일 영속성 | DB 없이 로컬 단독 실행 — 키오스크 재시작 후 상태 유지 |
| tkinter → PyQt6 | 초기 tkinter 계획 폐기, QStackedWidget 기반 전면 재설계 (→ `gui_architecture.md` 참고) |
| exe 단독 배포 | AppData 경로 기반 PyInstaller 빌드 (`3f44e7c build: exe 단독 배포 구현`) |

---

## 5. 발표 이후 추가 작업 (2026-06-03)

### 5.1 주니어 인수인계용 주석 작성

전체 26개 소스 파일에 상세 주석 작성. 원칙:
- WHY 위주 (왜 이렇게 했는가)
- 의존성 명시 (어떤 파일의 어떤 메서드를 쓰는지)
- 시행착오 이력 포함 (도메인 전환, 버그 수정 경위)
- 파일 이동 없이 이해 가능한 수준

진행 상황: `docstring_progress.md` 참고.

---

### 5.2 코드 검토 및 버그 수정

전체 코드 의존성 추적 검토 후 발견된 문제 수정. `federated-imagining-pearl.md` 계획서 기반.

**수정된 버그:**

| ID | 위치 | 문제 | 수정 |
|----|------|------|------|
| B-01 | `kiosk_controller._save_products()` | `list[dict]`를 `DataManager.save_products()`에 전달 → `AttributeError`. 관리자 ON/OFF, 가격 변경 시 크래시 | `self.data_manager.save_products(self.products)` 직접 전달 |
| B-02 | `main_window`, `cash_payment` 3곳 | `cart.get_subtotal()` 직접 사용 → 할인 정책 추가 시 결제 금액 불일치 | `controller.get_final_amount()` 통일 |
| P-01 | `Cart.update_quantity()` | `qty=0` 입력 시 수량 0짜리 항목이 리스트에 남음 | `qty <= 0`이면 `ValueError` raise |
| P-02 | `CashPayment.process()` | 이중 호출 시 `inserted_bills`가 reserve에 두 번 추가됨 | `process()` 성공 후 `inserted_bills = {}` 초기화 |
| P-03 | `VoiceService._generate_and_play()` | 네트워크 없으면 예외가 asyncio 루프로 전파 | `except Exception: pass` 추가 |
| E-01 | `main.py` AppData 경로 | `"EDK"` (구 프로젝트명) 하드코딩 | `"IceCreamKiosk"` 변경 |
| T-02 | `test_data_manager.py` | admin_config 키 `"admin_password"` → 실제 코드는 `"password"` 사용 | 키 수정 |
| S-01 | `admin_menu._change_password()` | 빈 문자열 입력 시 아무 피드백 없이 조용히 무시 | `QMessageBox.warning` 추가 |

**제거된 코드:**

| ID | 항목 | 이유 |
|----|------|------|
| D-01 | `stats.py`, `test_stats.py` | 결제 흐름 미연결 미완성 기능. 유지보수 부담 대비 가치 없음. |
| D-02 | `kiosk_controller.cancel_payment()` | GUI가 직접 `_active_payment.inserted_amount`를 읽어서 미호출. `cancel_cash_payment()`로 대체. |
| D-03 | `_get_selected_options(include_hidden)` | `include_hidden=True`로 호출하는 코드 없는 dead parameter. 제거 후 단순화. |

---

### 5.3 의존성 분리 리팩터링

**배경:** 발표 대본에서 "화면이 어떻게 생겼는지 전혀 모른다"는 원칙을 제시했으나, 실제 코드에서 GUI가 도메인 객체를 직접 생성·접근하는 위반이 다수 존재했음.

**제거된 위반:**

| 위반 | 이전 | 이후 |
|------|------|------|
| GUI가 CashPayment/CardPayment 직접 생성 | `CashPayment(amount, reserve)` | `controller.start_cash_payment()` |
| GUI가 결제 완료 로직 직접 조합 | `pmt.process()` + `cart.items = []` + `_save_after_payment()` | `controller.process_cash_payment() → tuple` |
| GUI가 private 메서드 직접 호출 | `controller._save_ingredients()` | `controller.clear_cart()` |
| ChangeReserve 직접 조작 | `reserve.add_cash()` + `data_manager.save_change_reserve()` | `controller.admin_add_cash()` |
| Ingredient 직접 순회 | `ctrl.ingredients.values()` | `controller.get_stock_status() → list[dict]` |
| Cart 직접 접근 | `_window.cart.items`, `cart.get_subtotal()` | `controller.get_cart_items()`, `is_cart_empty()` |
| KioskWindow가 change_reserve 보유 | `KioskWindow(controller, cart, change_reserve)` | `KioskWindow(controller, cart)` |

**신규 controller 메서드 (의존성 분리를 위해 추가):**
`get_inserted_amount()`, `cancel_cash_payment()`, `clear_cart()`,
`get_cash_status()`, `get_stock_status()`, `is_cart_empty()`, `get_cart_items()`

**현재 상태 (2026-06-03 기준):**
- 쓰기(변경): controller 단일 진입점 ✅
- 읽기(도메인 구조 의존): Cart 구조 변경이 GUI에 전파되지 않음 ✅
- 결제 금액: `get_final_amount()` 통일 ✅

---

## 6. 현재 상태 요약

→ `CURRENT_STATE.md` 참고 (149 tests passing, 기능 완료 + 리팩터링 완료)

---

## 7. 발표 PPT 아키텍처 설명 — 비판적 분석 메모

### 7.1 슬라이드 10 구성

**왼쪽**: 디렉터리 트리 (`data/`는 `data_manager.py` 하위 아님, `src/app/` 같은 레벨)

**오른쪽**: 코드 두 블록
- `process_cash_payment()` — kiosk_controller.py:215-238
- `DataManager._save()` — data_manager.py:63-70
- 슬라이드 연결 표기: `process_cash_payment() → DataManager._save()`

### 7.2 대본 전용 설명 (슬라이드에 안 씀)

**`_save_after_payment()` 경유 체인**
```
process_cash_payment()
  └→ _save_after_payment()               ← KioskController
       ├→ _save_ingredients()
       └→ data_manager.save_change_reserve()  ← DataManager
              └→ _save("change_reserve.json") ← JSON 실제 쓰기
```

**`save_change_reserve()`가 `_save()` 래퍼인 이유**
- `_save`는 private(언더스코어) → 외부 직접 호출 관례 위반 방지
- 파일명 문자열 DataManager 내부 격리
- 나중에 전처리 로직 추가 여지

---

## 8. 버그 수정 이력 (2026-06-05)

### 8.1 QPushButton 수량 버튼 렌더링 깨짐

**증상**: `customize.py` 수량 버튼이 실제 문자 대신 `|`, `.`, 기타 이상한 기호로 표시됨.

**원인**: 글로벌 스타일시트(`main_window.py` `STYLESHEET`)의 `QPushButton { padding: 10px 20px }`가
`setFixedSize(44, 44)` 버튼에 그대로 적용되어 텍스트 렌더링 영역이 44 − 2×20 = 4px로 압축됨.
Unicode 특수문자(`－`, `＋`, `▼`, `▲`) → `|` 렌더링. ASCII(`-`, `+`) → 점(`.`) 렌더링.

**해결**: `setFont()` 제거. 버튼별 `setStyleSheet("padding: 2px; font-size: 20px; font-weight: bold;")`로 인라인 재정의.
Qt에서 위젯 개별 `setStyleSheet()`는 부모 stylesheet보다 우선 적용되어 padding 충돌 해소.

**교훈**: 글로벌 QSS에 고정 padding이 있을 때 소형 고정 크기 위젯은 인라인으로 재정의 필요.

**`_save_after_payment()` 별도 메서드로 분리한 이유 — 재사용성**
- `process_cash_payment()`(232번)·`process_card_payment()`(287번) 두 곳에서 호출
- 직접 썼다면 현금·카드 두 곳에 중복. 저장 항목 추가 시 두 곳 모두 수정 필요
- `_save_after_payment()` 한 곳만 수정하면 현금·카드 결제 모두 반영 → DRY(중복 제거)

**`self._active_payment = None` 의도**
- 이중 처리 방지 (process() 두 번 호출 시 잔돈 두 번 차감 버그 방어)
- `can_complete_payment()` 가드 연동 → 결제 완료 후 버튼 자동 비활성화
- 다음 주문 사이클 클린 상태 준비

### 7.3 "의존성 분리" 용어 비판적 검토

**실제로 한 것 (정확한 용어: 파사드 패턴 + 레이어 격리)**
- GUI가 `Cart`, `CashPayment`, `Ingredient`를 직접 import하지 않음
- `KioskController` 메서드만 호출 → GUI ↔ 도메인 결합도 감소
- `process.md` § 5.3의 7개 위반 제거가 이것

**없는 것 (진짜 의존성 역전 DIP)**
- `KioskController`가 `DataManager` 구체 클래스에 직접 의존
- 인터페이스/Protocol 없음 → `SQLiteManager`로 교체 시 KioskController 수정 필요
- 인터페이스란: "이 메서드들 반드시 구현해라"는 계약서. 구현 없이 메서드 목록만 선언.
  교체 시 계약서대로만 구현하면 KioskController 수정 불필요.

**발표 권장 표현**
- ❌ "의존성 분리를 구현했습니다"
- ✅ "GUI는 KioskController만 바라봅니다 — 도메인 구현이 바뀌어도 화면은 수정 불필요"

### 7.4 GUI ↔ 비즈니스 로직 결합도 낮춤의 이점 (대본 그대로 사용)

**1. 도메인 전환 시 화면 재활용**
의약품 → 아이스크림 전환 때 `cart.py`, `payment_method.py`, `cash_payment.py`, `receipt.py` 화면 코드 그대로 재사용. GUI가 `Cart`·`Payment` 내부를 직접 건드렸다면 전부 재작성 필요했음.

**2. 비즈니스 로직 단독 테스트 가능**
GUI 띄우지 않고 `KioskController`만 테스트 가능 → 198개 테스트가 이것. GUI가 결제 로직을 직접 갖고 있었다면 PyQt6 앱 실행 없이 테스트 불가.

**3. 버그 격리**
GUI 버그(버튼 위치, 색상 등)가 결제 계산에 영향 없음. 반대로 결제 로직 수정이 화면 레이아웃에 영향 없음. 실제로 B-01·B-02 버그 수정 시 GUI 코드 수정 없이 `kiosk_controller.py`만 고침.

### 7.5 결합도를 낮추는 기법 검토 및 미채택 이유 (대본)

**단방향 의존 — 비판적으로 봐도 사실**
import 방향: `gui/screens/*` → `KioskController` → 도메인. 역방향 import 없음. 단방향 의존은 확인된 사실.

**각 기법 미채택 이유**

| 기법 | 필요한 상황 | 미채택 이유 |
|---|---|---|
| 인터페이스/DI 컨테이너 | 구현체가 여러 개, 교체 필요 | DataManager 구현체 하나뿐. 교체 계획 없음 |
| 마이크로서비스 | 서비스별 독립 배포·확장, 팀 분리 | 한 대 키오스크, 한 팀, 한 프로세스 |
| Kafka / MQ | 물리적으로 분리된 서비스 간 비동기 통신 | 네트워크 없음. 통신할 상대 서비스 없음 |
| FastAPI | HTTP로 외부 요청 수신 | 서버 없음. 클라이언트 없음 |
| PyQt6 시그널 | Controller가 GUI에 역방향 통지 필요 | 아래 트레이드오프 참고 |

→ 결합도를 낮추는 기법은 특정 문제를 해결하기 위해 존재. 그 문제가 없는 곳에 적용하면 불필요한 복잡도 추가.

**FastAPI 미채택 보충 문구 (대본용)**
"키오스크 10대가 재고를 공유해야 한다면 그때 서버가 필요합니다. 저희는 한 대이므로 해당 없습니다."

**PyQt6 시그널(이벤트 기반) 고려했으나 미채택 — 트레이드오프**

시그널로 결합도를 더 낮출 수 있으나 `KioskController`가 `QObject` 상속 필요 → 두 가지 문제:

1. **단위 테스트에 QApplication 초기화 필요**
   - QApplication: PyQt6의 모든 객체(`QObject` 포함)가 실행 전 반드시 필요한 인스턴스. 이벤트 루프 전체가 여기에 의존.
   - 현재 198개 테스트: PyQt6·QApplication 없이 순수 Python으로 즉시 실행 가능
   - `QObject` 상속 시: 모든 테스트마다 `QApplication([])` 초기화 필요 → PyQt6 미설치 환경에서 테스트 불가, 테스트 복잡도 증가

2. **GUI 프레임워크 교체 불가**
   - 현재: PyQt6를 다른 프레임워크로 교체해도 `KioskController` 수정 불필요
   - `QObject` 상속 시: 비즈니스 로직이 PyQt6 생명주기에 종속 → 프레임워크 교체 시 `KioskController` 전면 수정

→ 결합도를 낮추려다 PyQt6 의존이라는 다른 결합이 생기는 트레이드오프. 현재 규모에서 미채택 합리적.
