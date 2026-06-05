# EDK — 증상 기반 OTC 의약품 키오스크

한양대학교 ERICA 캠퍼스 약국 셀프 처방 키오스크 시뮬레이터.  
IC-PBL 수업 과제로 시작, Coffee/Gummy 도메인에서 EDK(Erica Drug King)로 전환.

**기간:** 2026년 5월  
**역할:** 팀 프로젝트 (IC-PBL) — 설계·구현·테스트 주도  
**상태:** 완료 (EDK 전체 구현 + 테스트 + 패키징)

---

## 문제 정의

캠퍼스 약국 방문 없이 가벼운 증상에 맞는 OTC(일반의약품)를 스스로 확인하고 구매할 수 있는가?

**핵심 제약:**
- 약학 지식 없는 일반 학생도 직관적으로 사용 가능해야 함
- 키오스크 형태 — 터치 기반 GUI, 자동 복귀(idle)
- TTS로 의약품 복용 안내 자동 음성 출력

---

## 핵심 기능

### 증상 기반 의약품 추천

증상 선택 그리드 → 매핑된 의약품 목록 필터링 → 상세 정보 및 장바구니 추가.  
증상 없이 전체 목록 탐색도 가능.

### 3단계 스크린 내비게이션 (PyQt6)

```
Idle → 증상 선택 → 의약품 목록 → 상세 → 장바구니 → 결제 수단 → 현금 결제 → 영수증
                                   ↘ 응급 증상 안내
                                          ↑
                              Admin 인증 → Admin 메뉴
```

KioskWindow가 스크린 전환 전담. 각 스크린은 window 참조만 보유.

### TTS 안내

edge-tts + pygame으로 의약품 상세 화면 진입 시 복용 안내 자동 음성 출력.

### 현금 결제 + 잔돈 계산

권종별 투입 누적 → 그리디 알고리즘으로 최적 잔돈 반환.  
잔돈 부족 시 거래 중단, 투입 금액 전액 반환.  
**모든 가격 최소 1,000원 단위** — 잔돈 시스템이 1,000원+ 권종만 보유하므로 100/500원 단위 제거.

### 관리자 기능

scrypt 해시 PIN 인증 → 의약품 재고 관리, 비밀번호 변경.  
평문 레거시 비밀번호는 첫 실행 시 자동 마이그레이션.

---

## 기술 스택

```
GUI        PyQt6 — KioskWindow + 11개 스크린
TTS        edge-tts + pygame
언어       Python 3.10+
테스트     pytest + pytest-qt
패키징     pyproject.toml (setuptools)
빌드       build_windows.ps1 / build_mac.sh
```

---

## 아키텍처

### 파일 구조

```
project/
├── src/
│   ├── app/
│   │   ├── main.py                  # 진입점 — 의존성 생성, 관리자 비밀번호 마이그레이션
│   │   ├── password_utils.py        # scrypt 해시 / verify (레거시 평문 호환)
│   │   ├── controller/
│   │   │   └── drug_controller.py   # 의약품/증상 조회 비즈니스 로직
│   │   ├── model/
│   │   │   ├── medicine.py          # Medicine (id, name, price, symptoms)
│   │   │   ├── symptom.py           # Symptom, SymptomGroup
│   │   │   ├── cart.py              # Cart (add/remove/clear/update)
│   │   │   ├── order_item.py        # OrderItem
│   │   │   └── cash_payment.py      # CashPayment (투입/완료/잔돈 계산)
│   │   ├── gui/
│   │   │   ├── kiosk_window.py      # KioskWindow — 메인 윈도우, 스크린 전환
│   │   │   └── screens/             # 11개 스크린 (idle, symptom, list, detail, ...)
│   │   ├── cli/
│   │   │   └── cli_view.py          # 관리자 전용 터미널 뷰
│   │   ├── service/
│   │   │   └── voice_service.py     # edge-tts + pygame TTS
│   │   └── data/
│   │       ├── medicines.json       # 의약품 데이터 (가격 1,000원 단위)
│   │       ├── options.json         # 옵션 추가금 (최소 1,000원)
│   │       ├── symptoms.json
│   │       └── admin_config.json    # scrypt 해시 비밀번호 저장
│   └── main.py
└── tests/                           # 12개 테스트 파일
```

### 의존성 방향

```
model/ (Medicine, Symptom, Cart, CashPayment)
    ↑
controller/drug_controller.py
    ↑
gui/kiosk_window.py ← gui/screens/*
    ↑
main.py
```

cli/cli_view.py와 gui/는 controller만 참조 — 모델 직접 접근 금지.

### KioskWindow 핵심 설계

- 생성자 서명: `KioskWindow(controller, cart, change_reserve)`
- `cart`, `change_reserve`는 window 필드 (controller 외부 상태)
- `__init__`에서 `go_to_idle()` 호출 → 장바구니 초기화
- `window._active_payment`: CashPayment 인스턴스 저장 위치

---

## 보안 — 관리자 비밀번호 해시

| 항목 | 내용 |
|------|------|
| 알고리즘 | `hashlib.scrypt` (stdlib, 외부 의존 없음) |
| 파라미터 | n=16384, r=8, p=1, dklen=32 |
| 저장 형식 | `scrypt$<salt_hex>$<hash_hex>` |
| 타이밍 안전 비교 | `hmac.compare_digest` |
| 레거시 마이그레이션 | `main.py` 시작 시 평문 감지 → 자동 해시로 교체 |

scrypt 선택 이유: bcrypt(외부 패키지) · pbkdf2_hmac(메모리 경화 없음) 대비,  
stdlib + memory-hard로 Python 3.10+ 요구사항에 최적.

**보안 한계:** exe 역공학 시 알고리즘·파라미터 노출 → 단방향 해시 특성상 역산 불가(Kerckhoffs 원칙).  
단, 소스에 하드코딩된 기본 비밀번호(`"1234"`)가 노출되므로 최초 실행 후 비밀번호 변경 필수.

---

## 테스트

| 파일 | 대상 |
|------|------|
| test_cart.py | Cart + OrderItem |
| test_medicine.py | Medicine 속성, available 플래그 |
| test_drug_controller.py | DrugController 5개 메서드 |
| test_data_manager.py | DataManager JSON I/O |
| test_payment.py | CashPayment 투입/완료/잔돈 |
| test_stats.py | Statistics |
| test_exceptions.py | 예외 클래스 |
| test_password_utils.py | scrypt hash/verify, 레거시 평문, 유일 salt |
| test_edk_integration.py | 장바구니+증상+결제 통합 플로우 |
| test_gui_app.py | KioskWindow 생성, 화면 전환, 장바구니 초기화 |
| test_gui_screens.py | 11개 스크린 전체 (pytest-qt) |
| test_admin_cash.py | CLIView 관리자 메뉴 (builtins.input mock) |

```bash
cd project
pytest          # 전체 실행
pytest -v       # 상세 출력
```

---

## 개발 이력 — 도메인 전환

| 단계 | 내용 |
|------|------|
| 초기 요구사항 | Micro-Factory Kiosk (커피/구미 커스텀) — IC-PBL 과제 |
| STEP 12까지 | Coffee/Gummy 도메인 CLI 구현 (`백업(__STEP12__)` 보존) |
| 전환 결정 | EDK(Erica Drug King) 도메인으로 전면 재설계 |
| GUI 전환 | CLI → PyQt6 KioskWindow + 11 스크린 |
| 테스트 재작성 | Coffee/Gummy 테스트 → EDK 도메인 전체 재작성 |
| 패키징 | pyproject.toml setuptools, Windows/Mac 빌드 스크립트 |
| 보안 강화 | 관리자 비밀번호 평문 → scrypt 해시 + 자동 마이그레이션 |
| 가격 정규화 | 전 상품 최소 1,000원 단위 — 의약품 3종 + 옵션 10개 조정 |

---

## 배운 것

**PyQt6 스크린 기반 내비게이션:**  
스크린 전환을 KioskWindow 단일 지점에서 관리 → 각 스크린은 `self._window.go_to_*()` 호출만.  
스크린이 다른 스크린을 직접 참조하지 않아 교체/추가 용이.

**pytest-qt GUI 테스트:**  
`QApplication` 인스턴스는 테스트 세션당 1개 — `qtbot` fixture로 관리.  
실제 이벤트 루프 없이 위젯 생성/클릭/상태 검증 가능.

**scrypt 선택 기준:**  
외부 의존 없이 메모리 경화 해시가 필요할 때: `hashlib.scrypt` (Python 3.6+, stdlib).  
bcrypt는 `passlib` 또는 `bcrypt` 패키지 필요, pbkdf2는 메모리 경화 없음.

**레거시 마이그레이션 패턴:**  
`verify_password`가 `scrypt$` prefix 없으면 평문 비교 허용 → 첫 로그인은 기존 비밀번호 그대로 통과.  
`main.py` 시작 시 평문 감지 → 즉시 해시 저장 → 이후부터 항상 해시 검증.  
사용자 개입 없이 보안 수준 자동 업그레이드.

**비밀번호 해시 보안 원칙 (Kerckhoffs):**  
exe 역공학으로 알고리즘·파라미터가 노출돼도 단방향 해시는 역산 불가.  
보안은 알고리즘 비밀이 아니라 해시의 수학적 일방향성에서 온다.  
실제 위협은 소스에 하드코딩된 기본값 노출 — 알고리즘 노출과 기본값 노출은 다른 문제.

**가격 단위 정규화:**  
현금 결제 잔돈 시스템이 1,000원+ 권종만 보유 → 100/500원 단위 가격 존재 시 잔돈 계산 불일치 발생.  
데이터 계층(JSON)에서 강제 → 코드 수정 없이 정책 변경 가능.

**pyproject.toml pythonpath 설정:**  
`[tool.pytest.ini_options] pythonpath = ["src"]` — `PYTHONPATH` 환경변수 없이 pytest 실행 가능.  
`testpaths = ["tests"]`와 조합하면 `cd project && pytest`만으로 전체 실행.
