# ic-pbl 아이스크림 키오스크 — 시스템 흐름 (System Flow)

> 상태: 아이스크림 키오스크 완성 (2026-05-29)

---

## 1. 전체 상태 머신

```
                    ┌─────────┐
               ┌───►│  IDLE   │◄──────────────────┐
               │    └────┬────┘                   │
               │         │ 화면 터치               │
               │    ┌────▼──────────┐             │ go_to_idle()
               │    │  MAIN_MENU    │             │ (결제 완료/취소)
               │    │  (상품 목록)  │             │
               │    └──┬────────────┘             │
               │       │ 상품 선택                 │
               │    ┌──▼──────────┐               │
               │    │  CUSTOMIZE  │               │
               │    │  (옵션 선택) │               │
               │    └──┬──────────┘               │
               │       │ 장바구니 담기             │
               │    ┌──▼──────────┐               │
               │    │    CART     │               │
               │    └──┬──────────┘               │
               │       │ 결제 진행                 │
               │    ┌──▼──────────────┐           │
               │    │ PAYMENT_SELECT  │           │
               │    └──┬──────────┬───┘           │
               │  현금 │          │ 카드           │
               │  ┌────▼───┐ ┌────▼──────────┐   │
               │  │  CASH  │ │     CARD      │   │
               │  │PAYMENT │ │   PAYMENT     │   │
               │  └────┬───┘ └───────┬───────┘   │
               │       └─────────────┘            │
               │            │ 완료               │
               │    ┌────────▼───────┐           │
               └────┤    RECEIPT     ├───────────┘
                    └────────────────┘

               관리자 진입 (IDLE 화면에서 관리자 버튼)
          ┌────┴──────────┐
          │  ADMIN_AUTH   │
          └──────┬────────┘
                 │ PIN 인증
          ┌──────▼────────┐
          │  ADMIN_MENU   │──→ IDLE (종료 버튼)
          └───────────────┘
```

---

## 2. 고객 주문 흐름

```
[IDLE] 화면 터치
  │
[MAIN_MENU] 상품 목록 표시
  - stick 아이스크림 (₩3,000 ~)
  - scoop 아이스크림 (₩4,000 ~)
  - 품절 상품 → 선택 불가
  │
  상품 선택
  │
[CUSTOMIZE] 옵션 커스터마이징
  - 형태 / 코팅 / 토핑 / 용기 / 맛
  - 재고 부족 옵션 → 비활성화
  - stick/scoop 미리보기 위젯
  │
  장바구니 담기 → [CART]
  (또는 계속 쇼핑 → [MAIN_MENU])
  │
[CART] 장바구니 확인
  - 수량 변경 (재고 연동)
  - 항목 삭제 (재고 복원)
  │
  결제 진행 → [PAYMENT_SELECT]
  │
  ├── 현금 선택 → [CASH_PAYMENT]
  │     권종 버튼 (1,000 / 5,000 / 10,000 / 50,000)
  │     투입액 누적 표시
  │     투입액 >= 결제 금액 → [완료] 활성화
  │     잔돈 계산 (그리디) → 실패 시 투입금 반환
  │
  └── 카드 선택 → 즉시 시뮬레이션 처리
  │
[RECEIPT] 영수증
  - 주문 내역, 결제 수단, 잔돈 표시
  - 일정 시간 후 자동 → [IDLE]
```

---

## 3. 결제 흐름 상세

```
[현금 결제]
  insert_cash(denomination)
    → CashPayment.insert(amount)
    → 유효 권종 검증 (1,000 / 5,000 / 10,000 / 50,000)
    → 누적 투입액 갱신
  
  [완료] 클릭
    → CashPayment.process()
    → ChangeReserve.dispense(change_amount) — 그리디
    → InsufficientChangeException → 투입금 반환, 장바구니 복귀
    → 성공 → go_to_receipt()

[카드 결제]
  go_to_card_payment()
    → CardPayment(amount).process()
    → 성공 → go_to_receipt()
    → 실패 → PaymentException → go_to_payment_method()
```

---

## 4. 관리자 흐름

```
[IDLE] → 관리자 버튼 → [ADMIN_AUTH]
  PIN 입력 (verify_password, scrypt)
  인증 성공 → [ADMIN_MENU]

[ADMIN_MENU] 기능:
  - 상품 ON/OFF (is_available 토글 + DataManager.save_products)
  - 가격 변경 (base_price + save_products)
  - 현금 보유량 확인 (권종별 수량 표시)
  - 현금 추가 (_AddCashDialog → ChangeReserve.add_cash + save_change_reserve)
  - 비밀번호 변경 (hash_password + save_admin_config)
  - 종료 → go_to_idle()
```

---

## 5. 예외 흐름

| 예외 | 발생 위치 | 처리 |
|------|---------|------|
| `InsufficientChangeException` | 현금 잔돈 계산 | 투입금 반환, 장바구니 복귀 |
| `PaymentException` | 카드 결제 | 결제 수단 선택으로 복귀 |
| `InsufficientStockException` | 재고 차감 | UI 비활성화로 선제 방지 |
| `StockOverflowException` | 관리자 재고 보충 | 오류 메시지, 보충 취소 |
| `AdminAuthException` | 관리자 인증 | 재입력 대기 |
| `InvalidRecipeException` | 데이터 로드 | 로드 실패 알림 |
