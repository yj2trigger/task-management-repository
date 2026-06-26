# GUI 초기 설계 계획서 (구 버전 — 역사적 참고용)

> 작성일: 2026-05-12 00:00
> ⚠️ 상태: **실제 구현과 다름** — 아래 내용은 초기 계획이며, 실제로는 PyQt6 QStackedWidget 기반으로 구현됨
> 실제 구현 내용은 `architecture.md` 참고

---

## 초기 계획 (tkinter 기반 — 미채택)

### 화면 분할 구조

```
┌────────────────────────────────────────────────────────┐
│                    메인 윈도우 (tkinter)                 │
│                                                        │
│  ┌──────────────────┐  ┌───────────────────────────┐  │
│  │   GUI 영역 (1/3) │  │  CLI 로그 영역 (2/3)       │  │
│  │                  │  │                           │  │
│  │  터치 버튼        │  │  기존 print() 출력이       │  │
│  │  메뉴 카드        │  │  실시간으로 표시됨         │  │
│  │  입력 패드        │  │  (Read-only ScrolledText) │  │
│  │                  │  │                           │  │
│  └──────────────────┘  └───────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

### 초기 계획 모듈 구조 (미채택)

```
gui/
├── app.py           # GUIApp
├── log_panel.py     # stdout 리다이렉터 + ScrolledText
├── control_panel.py # 버튼/카드 패널
├── state_machine.py # CLI 출력 파싱 → 화면 전환
└── widgets/
    ├── numpad.py
    ├── menu_card.py
    └── yn_dialog.py
```

---

## 실제 구현 (PyQt6 기반)

초기 tkinter + CLI 파싱 방식 대신 PyQt6 QStackedWidget 방식으로 전면 재설계됨.

실제 구현된 screens/: `idle`, `main_menu`, `product_list`, `customize`, `cart`,
`payment_method`, `cash_payment`, `receipt`, `admin_auth`, `admin_menu` + `voice_service`

→ 상세 내용: `architecture.md` 참고
