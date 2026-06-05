# ic-pbl 아이스크림 키오스크 — 구현 범위 (Scope)

> 상태: 아이스크림 키오스크 완성 (2026-05-29)

---

## 1. 레이어 구조

```
┌──────────────────────────────────────────────────────┐
│              Business Logic Layer                    │
│  (IceCreamProduct / Option / Cart / Payment / ...)   │
│  → View가 무엇인지 절대 모름                           │
│  → optional logger 콜백만 수신                        │
└─────────────┬────────────────────────────────────────┘
              │ 함수 호출
    ┌─────────▼──────────────────────┐
    │       GUI View (PyQt6)         │
    │  idle → main_menu → customize  │
    │  → cart → payment → receipt    │
    └────────────────────────────────┘
```

---

## 2. 구현 기능 (Must-Have) — 전체 완료

| # | 기능 | 설명 |
|---|------|------|
| 1 | 상품 목록 표시 | stick / scoop 두 상품, 품절 시 선택 불가 |
| 2 | 옵션 커스터마이징 | 형태, 코팅, 토핑, 용기, 맛 — 옵션별 추가 금액 |
| 3 | 재고 기반 주문 | 옵션 선택 시 재고 차감, 부족 시 비활성화 |
| 4 | 장바구니 | 여러 상품 담기, 수량 변경, 재고 연동 |
| 5 | 현금 결제 | 권종 누적 투입 + 잔돈 반환 (그리디 알고리즘) |
| 6 | 카드 결제 | 시뮬레이션 처리 |
| 7 | 영수증 | 주문 내역, 결제 수단, 잔돈 표시 |
| 8 | TTS 음성 안내 | edge-tts + pygame (각 화면 전환 시 안내) |
| 9 | JSON 영속성 | products / ingredients / options / change_reserve / admin_config |
| 10 | 관리자 모드 | PIN 인증 (scrypt), 상품 ON/OFF, 가격 변경, 현금 확인/추가, PIN 변경 |
| 11 | 예외 처리 | 잔돈 부족, 재고 부족, 관리자 인증 실패 등 |

---

## 3. 데이터 파일 구성

| 파일 | 내용 |
|------|------|
| `products.json` | 상품 목록 (product_id, name, base_price, is_available, product_type) |
| `ingredients.json` | 재료 재고 (ingredient_id, name, stock, max_capacity, unit) |
| `options.json` | 옵션 그룹 (group_id, name, active_for, options[]) |
| `change_reserve.json` | 잔돈 보유량 (권종별 수량) |
| `admin_config.json` | 관리자 PIN 해시 (scrypt$...) |

---

## 4. 제외 범위

| 항목 | 이유 |
|------|------|
| 실제 카드 결제 API | 시뮬레이션 대체 |
| 네트워크 통신 / 서버 | 로컬 단독 실행 |
| DB (SQLite 등) | JSON 대체 |
| 번들 할인 정책 | 미구현 |
| CLI 주문 모드 | GUI 전용 (--gui 필수) |
