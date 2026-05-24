# 📋 Backlog

> 아직 시작하지 않은 태스크 목록입니다.

---

## [ic-pbl] EDK 도메인 전환 — Core

- [ ] EDK-02: kiosk_controller.py → drug_controller.py — 증상→의약품 매핑 로직 전환
- [ ] EDK-03: data_manager.py — medicines.json / symptoms.json 데이터 구조 적용
- [ ] EDK-04: main.py — 의약품 데이터 초기화 로직으로 교체
- [ ] EDK-05: cli_view.py — 증상 선택 → 제품 탐색 → 결제 흐름으로 교체

> ℹ️ cart.py / payment.py / ChangeReserve 는 **실제 판매이므로 그대로 재활용** (제거 불필요)

## [ic-pbl] EDK 도메인 전환 — GUI (신규/수정만)

- [ ] GUI-EDK-01: main_window.py — 네비게이션 API를 EDK 화면 흐름으로 교체
- [ ] GUI-EDK-02: main_menu.py → symptom_select.py — 증상 카테고리 선택 화면
- [ ] GUI-EDK-03: product_list.py → medicine_list.py — 제품 목록 화면
- [ ] GUI-EDK-04: customize.py → medicine_detail.py — 제품 상세 + 장바구니 담기 화면
- [ ] GUI-EDK-05: (신규) emergency.py — 응급 상황 안내 화면 추가
- [ ] GUI-EDK-06: admin_menu.py — 의약품 정보/재고 관리로 수정

> ℹ️ cart.py / payment_method.py / cash_payment.py / receipt.py 는 **그대로 재활용**

## [ic-pbl] 마무리

- [ ] 테스트 재작성 — EDK 도메인 기준 단위 테스트 (cart/payment 테스트는 재활용 가능)
- [ ] pyproject.toml + README.md — 패키징 설정

---

## [ESG] 버그 수정

- [ ] 대시보드 loading 무한 버그 — `machineStore.setData` + `DashboardPage` 수정 후 브라우저 확인 필요

## [ESG] 구현 8단계: CI/CD — 수동 설정 (사용자)

- [ ] Supabase: PostgreSQL 프로젝트 생성 → DATABASE_URL 확보
- [ ] Fly.io: 가입 → `fly launch` (backend/) → `fly secrets set DATABASE_URL SECRET_KEY CORS_ORIGINS`
- [ ] Vercel: GitHub 레포 연결 (Root: frontend/) → VITE_API_URL, VITE_WS_URL 환경변수 설정
- [ ] GitHub Secrets: FLY_API_TOKEN, VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID 등록

## [ESG] 구현 9단계: 운영 고려사항

- [ ] Alembic 마이그레이션 — `create_all()` 대체

## [ESG] 향후 기능 (프로토타입 이후)

- [ ] 카카오 OAuth — 1인 다계정 방지 (`authlib`, `/auth/kakao`, `User.kakao_id`)
- [ ] 관리자 페이지 — `/admin/machines/{id}` PATCH
- [ ] PWA Push Notification — 백그라운드 알림
- [ ] 통계 — `machine_status_logs` 테이블 + 시간대별 혼잡도 API
