# 📋 Backlog

> 아직 시작하지 않은 태스크 목록입니다.

---

## [MAP] 단계별 PR(스택) 방식 첫 적용

> 기준: [`docs/MAP/conventions/stacked-pr-playbook.md`](../docs/MAP/conventions/stacked-pr-playbook.md)
> 측정 기준선: [`pr-baseline-2026-09.md`](../docs/MAP/conventions/pr-baseline-2026-09.md)
> 배경: 현재 PR 추가 줄 중앙값 754 / 파일 11개. 목표는 400줄 / 10파일 이하.

- [x] STACK-01: 다음 서버 기능 1개를 대상으로 선정 (user 또는 hub)
      — hub 대중교통 실제 노선 좌표(hub#16). hub 만 400줄을 넘어(605줄) 스택 대상, user·client 는 레포당 PR 1개
- [x] STACK-02: 플레이북 3장대로 ①스키마 ②로직 ③서비스(플래그 off) ④배선 4단 분할
      — DB 스키마가 없어 ①②를 합친 3단(`parse` / `client` / `wire`), 플래그 `TRANSIT_LANE_ENABLED` 기본 false
- [ ] STACK-03: `gh pr create --base <앞 브랜치>` 로 스택 오픈, 아래부터 순차 머지 (①=hub#18 열림)
      — 머지는 Merge commit, 아래 머지 후 위 PR base 를 develop 으로 직접 변경(플레이북 5.2, 2026-09-16 개정)
- [ ] STACK-04: 플래그 기본값 false 확인 → test 환경만 on → prod on
- [ ] STACK-05: 플래그·옛 경로 제거 PR 별도 생성
- [ ] STACK-06: 적용 후기 기록 — 연쇄 병합·base 재지정 부담이 크면 Graphite 도입 검토 (플레이북 6장)

**미결**: 브랜치 명명이 client는 이슈번호형(`feat/#45-...`), 서버는 기능명형으로 갈려 있음.
스택을 쓰면 브랜치 수가 늘어나므로 이때 통일 여부를 결정한다.

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

---

## [MAP] AI 루키 본선 제안서 완성

> 초안: [2026-08-09-ai-rookie-final-proposal-draft.md](../docs/MAP/plans/2026-08-09-ai-rookie-final-proposal-draft.md) (v4)
> Artifact: https://claude.ai/code/artifact/bbd3cfa4-53d1-4195-90de-048758abcd8a

**리서치 (AI 웹서치로 채울 수 있음)**
- [ ] ROOKIE-01: 1.4 기술동향 — 자유여행/개인형모빌리티 시장 트렌드, AI 여행플래너 붐 근거자료 조사
- [ ] ROOKIE-02: 1.5 경쟁사분석 — 네이버지도·카카오맵·Life360 최신기능 재확인, "국내 최초 시도" 주장 검증(반박사례 유무)

**코드 작업 (착수 여부 팀 결정 필요)**
- [ ] ROOKIE-03: 🚧 모빌리티 반경 필터 완성 — `RecommendRequest`/`AgentRequest`에 출발지 좌표 필드 추가 + `rules_filter` origin을 후보평균→출발지로 교체. 본선 전 고칠지 2차로 미룰지 먼저 결정
- [ ] ROOKIE-04: 3.3.1 정량 성능지표 — 실제 응답시간·추천 정확도 측정. Docker Desktop 데몬 미기동 상태 확인함(2026-08-09) — 데몬 기동 후 `map-service-infra`의 기존 `.env`로 스택 올려서 벤치마크 가능할 것

**팀만 답 가능 (AI가 못 채움)**
- [ ] ROOKIE-05: 3.3.3 팀 학습성과 — 교육 참석여부/인원/성명
- [ ] ROOKIE-06: 5.3/5.4 — 팀 개인 성장목표, 향후 활동계획
- [ ] ROOKIE-07: 6.1/6.2/6.4 — 시연가능여부, 방식, 영상(촬영 필요)
- [x] ROOKIE-08: 1.6표 "팀 확인 필요" 항목 — 완료(2026-08-09). 지도SDK: 카카오 사업자등록 필요해 네이버로 전환(팀 답변). API 8→6종: 관광빅데이터·관광지집중률예측·Google Places 3종 미구현, ODsay 신규 추가 확인. Gemini 2.0→2.5: "2.0 API 안 됐다"는 팀 기억은 오답(2025-02 GA), Gemini 2.1은 존재하지 않음, 실제로는 Gemini 2.0 Flash/Flash-Lite가 2026-06-01 서비스 종료돼 강제 마이그레이션했을 가능성 큼(웹 조사, 출처는 문서 1.6 참고)
- [ ] ROOKIE-09: 4장 GPU/토큰 사용량 — Gemini API 콘솔 로그(팀 계정)에서 확인
