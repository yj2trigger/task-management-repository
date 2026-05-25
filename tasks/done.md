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
  - src/types/user.ts — Gender 타입
  - src/store/authStore.ts — Zustand + localStorage persist
  - src/pages/GenderSelectPage.tsx — 남/여 선택 UI + 구역 안내 문구
  - src/App.tsx — /gender 라우트, 미선택 시 자동 redirect
- [x] 구현 3단계: Auth — JWT register/login (2026-05-24)
  - app/models/user.py, app/core/security.py, app/api/auth.py
  - app/schemas/auth.py — TokenResponse에 username/gender/role 포함
  - 테스트: test_auth.py — 전체 PASS
- [x] 구현 4단계: Machines + Mode A/B/C (2026-05-24)
  - app/models/machine.py, app/repositories/machine_repo.py (seed 17대)
  - app/services/machine_service.py — get_current_mode, get_dashboard
  - app/api/machines.py — GET /machines, POST /machines/request
  - 테스트: test_machines.py, test_machine_request.py — 전체 PASS
- [x] 구현 5단계: SoftReserve + Queue (2026-05-24)
  - app/models/queue_entry.py, app/repositories/queue_repo.py
  - app/services/queue_service.py — join, leave
  - app/api/queue.py — POST /queue/join, DELETE /queue/leave
  - Lazy expiration: release_expired() — 스케줄러 없이 매 요청 시 처리
  - 테스트: test_queue.py — 전체 PASS
- [x] 구현 6단계: WebSocket (2026-05-24)
  - app/core/ws_manager.py — gender 채널 분리, user_id 타겟 알림
  - app/api/ws.py — JWT 검증 → 초기 상태 전송 → 30s keepalive loop
  - src/hooks/useWebSocket.ts — 3s 자동 재연결
  - src/pages/DashboardPage.tsx — machines_updated / queue_notify 처리
  - 테스트: test_ws.py — 전체 PASS
- [x] 구현 7단계: Docker Compose 로컬 실행 (2026-05-24)
  - main.py lifespan에 machine_repo.seed(db) 추가
  - .env 생성 (git 제외)
  - docker compose up --build 동작 확인
- [x] 구현 8단계: CI/CD (2026-05-24~25)
  - .github/workflows/ci.yml — push/PR 시 pytest + vitest 자동 실행 (main, develope 브랜치)
  - .github/workflows/cd.yml — main push 시 Fly.io + Vercel 자동 배포
  - Fly.io: `flyctl deploy --remote-only`, fly.toml 루트 위치
  - Vercel: vercel.json SPA rewrites, working-directory 제거로 경로 이중 적용 방지
  - Fly.io Secrets: DATABASE_URL(Supabase), SECRET_KEY, CORS_ORIGINS, GMAIL_USER, GMAIL_APP_PASSWORD
  - Vercel Env: VITE_API_URL, VITE_WS_URL
- [x] 구현 9단계: 운영 고려사항 (2026-05-24)
  - slowapi rate limiting: /auth/register 5/min, /machines/request 3/min
  - soft_reserve 재요청 방지: get_active_reserve() + 409 반환
  - CORS allow_origins: env var화
- [x] 구현 10단계: 이메일 인증 (2026-05-25)
  - @hanyang.ac.kr 도메인 제한 + 6자리 OTP (10분 만료)
  - Gmail SMTP 발송 (Resend 무료 플랜 외부 도메인 불가로 전환)
  - app/models/email_verification.py, app/core/email.py
  - src/pages/VerifyEmailPage.tsx
  - 테스트: test_auth.py 32/32 PASS

## [ESG] 기능 추가 (2026-05-25)

- [x] 대기 순번 실시간 표시
  - WS queue_position_updated 이벤트 (누군가 취소/알림받을 때 전원 갱신)
  - QueueJoinResponse에 total 필드 추가
  - DashboardPage: 현재 N번째 / 전체 M명 표시
- [x] 모바일 PWA (standalone 모드)
  - public/manifest.json (display: standalone, theme_color: #333)
  - index.html: manifest link + iOS/Android 메타 태그
  - App.tsx: 첫 터치 시 Fullscreen API 요청

## [ESG] 버그/UI 수정 (2026-05-25)

- [x] 대시보드 loading 무한 버그 수정 — data 있을 때는 loading/error 화면으로 교체하지 않음
- [x] GenderSelectPage — 성별에 따라 다른 구역 세탁기 안내 문구 추가
- [x] LoginPage — 비밀번호 표시/숨기기 토글 버튼 (👁/🙈)
