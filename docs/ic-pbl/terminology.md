# ic-pbl 아이스크림 키오스크 — 용어 사전 (Terminology)

> 작성일: 2026-06-03
> 상태: 아이스크림 키오스크 완성 기준

---

## 1. 상품 도메인

| 한국어 | 변수명 | 클래스명 | 정의 |
|--------|--------|---------|------|
| 아이스크림 상품 | `product` | `IceCreamProduct` | 판매 가능한 아이스크림 1종 (stick 또는 scoop) |
| 상품 유형 | `product_type` | — | `"stick"` (스틱) 또는 `"scoop"` (스쿱) |
| 기본 가격 | `base_price` | — | 옵션 미적용 가격 (stick ₩3,000, scoop ₩4,000) |
| 판매 가능 여부 | `is_available` | — | False 시 UI에서 선택 불가 |

---

## 2. 옵션 도메인

| 한국어 | 변수명 | 클래스명 | 정의 |
|--------|--------|---------|------|
| 옵션 | `option` | `Option` | 단일 선택 항목 (추가 금액 포함) |
| 옵션 그룹 | `option_group` | `OptionGroup` | 형태/코팅/토핑/용기/맛 등 카테고리 |
| 추가 금액 | `extra_price` | — | 해당 옵션 선택 시 base_price에 가산 |
| 활성 상품 유형 | `active_for` | — | 이 옵션 그룹이 활성화되는 product_type 목록 |
| 필요 재료 | `required_ingredients_dic` | — | 옵션 1회 선택 시 차감되는 재료와 수량 |

---

## 3. 재고 도메인

| 한국어 | 변수명 | 클래스명 | 정의 |
|--------|--------|---------|------|
| 재료 | `ingredient` | `Ingredient` | 옵션에 사용되는 원재료 1종 |
| 재고 | `stock` | — | 현재 보유 수량 |
| 최대 용량 | `max_capacity` | — | 최대 보유 가능 수량 |
| 품절 | `out_of_stock` | — | stock = 0, UI에서 해당 옵션 비활성화 |

---

## 4. 장바구니 / 결제 도메인

| 한국어 | 변수명 | 클래스명 | 정의 |
|--------|--------|---------|------|
| 장바구니 | `cart` | `Cart` | 구매 전 담은 항목 목록 |
| 주문 항목 | `order_item` | `OrderItem` | 상품 1종 + 선택 옵션 + 수량 + 소계 |
| 결제 금액 | `final_amount` | — | 최종 청구 금액 |
| 잔돈 | `change_amount` | — | 투입 금액 - 결제 금액 |
| 잔돈 보유량 | `change_reserve` | `ChangeReserve` | 키오스크 내 권종별 보유 수량 |

---

## 5. 관리자 도메인

| 한국어 | 변수명 | 정의 |
|--------|--------|------|
| 관리자 | `admin` | 상품/재고/현금/설정 접근 권한자 |
| 관리자 PIN | `admin_password` | JSON에 scrypt 해시로 저장 |
| 판매 통계 | `revenue` | 결제 완료 금액 누적 합산 |

---

## 6. 예외 도메인

| 예외 | 발생 조건 |
|------|---------|
| `StockOverflowException` | 재고 보충 시 max_capacity 초과 |
| `InsufficientChangeException` | 잔돈 반환 불가 (보유 잔돈 부족) |
| `PaymentException` | 결제 처리 실패 |
| `InsufficientStockException` | 재고 차감 시 부족 |
| `AdminAuthException` | 관리자 비밀번호 불일치 |
| `InvalidRecipeException` | 데이터 JSON 형식 오류 |

---

## 7. 데이터 파일 구성

| 파일 | 내용 | 갱신 시점 |
|------|------|---------|
| `products.json` | 상품 목록, 가격, 판매 가능 여부 | 관리자 수정 시 |
| `ingredients.json` | 재료 재고 (stock, max_capacity) | 주문 완료 / 관리자 보충 시 |
| `options.json` | 옵션 그룹 및 옵션 항목 | 관리자 수정 시 |
| `change_reserve.json` | 권종별 현금 보유량 | 결제 완료 / 관리자 추가 시 |
| `admin_config.json` | 관리자 PIN 해시 (scrypt$...) | 관리자 변경 시 |
