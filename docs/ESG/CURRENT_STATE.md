# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-25
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)
> 전체 설계 문서: [full_plan.md](./full_plan.md)
> 상세 기술 명세 (API · 파일 구조 · 배포): [portfolio/ESG/architecture.md](../../portfolio/ESG/architecture.md)

---

## 🟢 현재 단계

**핵심 기능 전체 완료 + 운영 중 (Fly.io + Supabase + Vercel)**

---

## 핵심 비즈니스 로직: 3-Mode State Machine

| 모드 | 조건 | 동작 |
|------|------|------|
| Mode A | 4대 이상 | 층별 이용 가능 세탁기 수 표시 |
| Mode B | 1~3대 | 버튼 누르면 1:1 세탁기 위치 안내 + 10분 소프트 예약 |
| Mode C | 0대 | 대기열 등록 → 빈 자리 발생 시 순서대로 알림 + 실시간 순번 표시 |

---

## 구현 진행 현황

| 기능 | 백엔드 | 프론트엔드 |
|------|--------|----------|
| 1. 프로젝트 골격 + Docker | ✅ | ✅ |
| 2. 성별 선택 | — | ✅ |
| 3. 인증 (JWT register/login) | ✅ | ✅ |
| 4. 세탁기 상태 조회 (Mode A/B/C) | ✅ | ✅ |
| 5. Mode B 소프트 예약 + Mode C 대기열 | ✅ | ✅ |
| 6. WebSocket 실시간 연결 | ✅ | ✅ |
| 7. Docker Compose 로컬 실행 | ✅ | ✅ |
| 8. CI/CD (GitHub Actions → Fly.io + Vercel) | ✅ | ✅ |
| 9. 운영 고려사항 (rate limit, soft_reserve 중복 방지) | ✅ | — |
| 10. 이메일 인증 (@hanyang.ac.kr + 6자리 OTP) | ✅ | ✅ |
| 11. 대기 순번 실시간 표시 (WS queue_position_updated) | ✅ | ✅ |
| 12. 모바일 PWA (standalone + Fullscreen API) | — | ✅ |
| 13. 관리자 페이지 (세탁기 상태 변경) | ✅ | ✅ |
| 14. 비밀번호 / 아이디 변경 (설정 페이지) | ✅ | ✅ |
| 15. IoT 신호 수신 엔드포인트 | ✅ | — |

---

## 알려진 이슈 / 해결된 버그

| 이슈 | 상태 |
|------|------|
| 대시보드 로딩 무한 (WS 업데이트마다 깜박임) | ✅ data 있으면 loading 화면 미표시 |
| Resend 무료 플랜 외부 도메인 발송 불가 | ✅ Gmail SMTP 전환 |
| Vercel working-directory 이중 적용 | ✅ 제거로 해결 |
| WsMessage TypeScript 타입 누락 (queue_position_updated) | ✅ 수정 |
| 모바일 horizontal overflow | ✅ boxSizing: border-box 적용 |
| Mode B 배정 후 결과 즉시 사라짐 | ✅ modeBResult 상위 상태로 올림 |
| Mode C 대기 중 모드 B 전환 시 대기 상태 소멸 | ✅ queueInfo 상위 상태로 올림 |
| Mode B/C 뷰 동시 표시 (대기 중 + 사용 버튼) | ✅ queueInfo 있으면 Mode B/A 뷰 숨김 |
| 어드민 available 전환 시 큐 알림 미발송 | ✅ _notify_queue_and_broadcast 연결 |
| React StrictMode WS 1006 disconnect | 미해결 (두 번째 연결 정상 동작) |

주요 사고 상세 분석 → [portfolio/ESG/postmortems/](../../portfolio/ESG/postmortems/)

---

## 알려진 제약 / 향후 과제

| 항목 | 내용 |
|------|------|
| `in_use` 자동 해제 | 없음 — 어드민 수동 또는 IoT 연동 필요 |
| IoT 실제 연동 | 엔드포인트 준비 완료, 장치 연결 대기 |
| PWA Push Notification | WebSocket 인앱 알림만 — 백그라운드 미지원 |
| 통계 | `machine_status_logs` 미구현 |
