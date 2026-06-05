# 📋 Backlog

> 아직 시작하지 않은 태스크 목록입니다.

---

## [ESG] IoT 구현

> 설계 상세: [ADR-007 — Adaptive Polling 전략](../portfolio/ESG/decisions/ADR-007-iot-polling-strategy.md)
> Tuya 연동 계획: [full_plan.md 13단계](../docs/ESG/full_plan.md)

- [ ] IoT-01: Tuya WiFi 플러그 실물 연결 + Device ID 확보
- [ ] IoT-02: `tuya_client.py` 구현 (Sign Algorithm + access_token + polling)
- [ ] IoT-03: Adaptive polling 로직 구현 (ADR-007)
- [ ] IoT-04: Admin 패널 polling 통계 표시
- [ ] IoT-05: Phase 2 자동 interval 조절

---

## [ESG] DB Quota 관리

> 계획 상세: [full_plan.md 14단계](../docs/ESG/full_plan.md)
> 배경: Supabase 무료 500MB 한도 — IoT 연동 후 machine_status_logs 급증 예상

- [ ] QUOTA-01: `maintenance_service.py` — 30일/7일 자동 데이터 정리
- [ ] QUOTA-02: `GET /admin/system/stats` — DB 사용량 API
- [ ] QUOTA-03: Background Task — 24시간마다 quota 체크 + Gmail 이메일 알림
- [ ] QUOTA-04: `AdminPage` — DB 사용량 게이지 + 시스템 현황 UI
- [ ] QUOTA-05: WebSocket `quota_warning` 이벤트 (관리자 채널 확장)

---

## [ESG] 운영 개선

- [ ] 기술부채 #4: `ConnectionManager` 다중 서버 WS 브로드캐스트 누락

---

## [ESG] 향후 기능

- [ ] PWA Push Notification
- [ ] 통계 — `machine_status_logs` + 시간대별 혼잡도 API
