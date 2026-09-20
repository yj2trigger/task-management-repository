# AI 인계 문서 (AI Handover Guide)

> 작성일: 2026-05-23 00:00
> 최종 갱신: 2026-06-26 20:53
> 목적: 이 문서를 읽은 AI가 현재 진행 중인 작업을 즉시 이어받을 수 있도록 합니다.

---

## 이 레포지토리의 역할

`task-management-repository`는 여러 프로젝트를 AI와 함께 관리하는 **메타-리포지토리**입니다.
코드는 각 하위 레포에 있고, 이 레포는 **문서, 태스크 트래킹, 협업 규칙**만 관리합니다.

---

## 운영 원칙

- **모든 문서는 `docs/`에서만 관리** — 하위 레포의 docs는 업데이트하지 않음
- **코드 변경은 하위 레포에서, 문서/태스크는 여기서**
- **단계가 끝날 때마다 `CURRENT_STATE.md`와 `tasks/`를 업데이트**

---

## 현재 관리 중인 프로젝트

| 프로젝트 | 레포 | 현재 상태 |
|---------|------|----------|
| ic-pbl (EDK) | [pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl) | EDK 전체 구현 완료, PR #16 gemini-review 실패로 blocked |
| ESG | [ESG](https://github.com/yj2trigger/ESG) | 핵심 기능 완료 + 운영 중 |
| MAP (map-service-user) | [we-meet-trip/map-service-user](https://github.com/we-meet-trip/map-service-user) | recommend/schedule/trip 도메인 구현됨(develop). 인증은 미병합(`feat/login-dev`). 재사용캐시 설계 진행 중 |
| MAP (visitor_log) | 로컬 전용 `c:\onedrive\_대학교\MAP\git\visitor_log` | VPS·AR 씬 저장·블렌딩 서비스 — spike 단계 |
| 수어 번역 (sign-language) | 코드 레포 없음. 문서 `docs/sign-language/` | 설계 브레인스토밍 중(스펙·코드 전). 진입 문서: `docs/sign-language/README.md` |
| MAP (map-yoloservice) | `c:\onedrive\_대학교\MAP\git\map-yoloservice` | 카메라 실시간 인식(YOLO+Gemini Vision). 2026-08-14 infra 컨테이너 편입 + 실기 WebSocket 연결 검증 완료. 상세: `docs/MAP/map-yoloservice/DEV_LOG.md` |

---

## 반드시 먼저 읽어야 할 문서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | `COLLABORATION_RULES.md` | AI가 따라야 할 협업 규칙 |
| 2 | `docs/ic-pbl/CURRENT_STATE.md` | ic-pbl 현재 진행 상태 |
| 3 | `docs/ESG/CURRENT_STATE.md` | ESG 현재 진행 상태 |
| 4 | `docs/MAP/map-service-user/CURRENT_STATE.md` | MAP(map-service-user) 현재 진행 상태 |
| 5 | `docs/MAP/conventions/stacked-pr-playbook.md` | **MAP 작업이면 필수** — PR 분할·플래그 기준 SSOT (요약: 같은 폴더 `stacked-pr-cheatsheet.md`) |
| 6 | `tasks/in-progress.md` | 현재 진행 중인 태스크 |
| 7 | `tasks/backlog.md` | 대기 중인 태스크 |
| 8 | `docs/sign-language/README.md` | **수어 번역 작업이면 필수** — 문서 지도·데이터 위치·진행 상태. SSOT는 같은 폴더 `키포인트-설계-기록-2026-09-20.md` |

---

## 협업 규칙 핵심 요약

작업 전 반드시 `COLLABORATION_RULES.md`를 읽고 따릅니다. 요약:

1. **모호한 점은 먼저 질문** — 추측으로 진행하지 않습니다
2. **작업 전 계획 설명 + 승인** — 무엇을 어떻게 할지 먼저 설명합니다
3. **작업 후 결과 정리 + 승인** — 완료 후 요약하고 다음 단계 승인을 받습니다
4. **기능 구현 시 테스트 동시 작성** — 코드 + 테스트가 함께 완료 기준입니다

---

## ic-pbl (EDK) 프로젝트 인계 정보

### 현재 상태: PR #16 — gemini-review check 실패로 blocked

`pmg-ic-pbl`의 `develop` 브랜치에 EDK 전체 구현이 올라가 있으며, `main` 대상 PR #16이 열려 있습니다.

**GitHub 상태:**
- PR: https://github.com/yj2trigger/pmg-ic-pbl/pull/16
- Head: `develop` commit `6fc283c`
- Base: `main`
- 상태: `mergeable_state: blocked` — `.github/workflows/gemini-review.yml` check 실패
- `develop` behind 0
- 로컬 검증: `project/`에서 `python -m pytest` → `198 passed, 6 subtests passed` (2026-05-27)

**block 원인:**
`gemini-review.yml` 워크플로가 Gemini API를 호출해 PR 코멘트를 게시하는 구조인데, check run `review`가 `failure`로 완료됨.
가능한 원인: `GEMINI_API_KEY` secret 만료/미설정, 또는 diff 크기 초과 (PR #16: +2107/-3838, 56 files).

**포함된 작업:**
- `Medicine`, `Symptom`, `SymptomGroup` 도메인 전환
- `DrugController` 및 `DataManager` 의약품/증상 JSON 전환
- CLI 증상 선택 → 의약품 탐색 → 결제 흐름
- PyQt6 GUI 증상 선택, 의약품 목록/상세, 응급 안내, 관리자 화면
- EDK 기준 테스트 전면 재작성
- `project/pyproject.toml`, `project/README.md` 패키징/문서화
- 관리자 비밀번호 scrypt 해시 및 평문 자동 마이그레이션
- 가격 정책 1000원 단위 정규화
- `stats.py`와 `test_stats.py` Medicine 기준 수정

**다음 작업:**
1. `GEMINI_API_KEY` secret 유효 여부 확인 (GitHub repo settings → Secrets)
2. 유효하다면 diff 크기 문제 — 워크플로에 diff 크기 제한 로직 추가 후 re-run
3. check 통과 후 PR #16 → main 머지
4. 머지 후 `docs/ic-pbl/CURRENT_STATE.md`와 `tasks/done.md`에 PR #16 머지 완료 반영

**주의:**
- `pmg-ic-pbl/docs/`는 이 관리 레포로 이전되어 삭제 유지가 맞습니다.
- 프로젝트 문서 SSOT는 `task-management-repository/docs/ic-pbl/`입니다.

---

## ESG 프로젝트 인계 정보

### 현재 상태: 핵심 기능 완료 + 운영 중

상세 상태는 `docs/ESG/CURRENT_STATE.md`를 기준으로 확인합니다.

**향후 주요 작업:**
- IoT 실물 연동: Tuya WiFi 플러그 연결 + Device ID 확보
- DB Quota 관리: 자동 정리, 관리자 시스템 통계, 이메일 알림
- 운영 개선: 다중 서버 WebSocket 브로드캐스트 보완

---

## MAP 프로젝트 인계 정보

> **MAP 6개 레포 공통 작업 규약**: [`docs/MAP/conventions/stacked-pr-playbook.md`](./docs/MAP/conventions/stacked-pr-playbook.md)
> 브랜치를 어디서 끊고 언제 PR을 여는지, 플래그 기본값, 마이그레이션 제약이 여기에 있다.
> 코드 작업 전에 읽는다. 아래 「주의사항」의 **AI가 직접 push하지 않는 원칙은 그대로 유효**하며,
> 플레이북은 사용자가 브랜치·PR을 만들 때의 기준이다.

### 현재 상태 (2026-07-07 재검증): 인증 미병합, recommend/schedule/trip 구현됨, 재사용캐시 설계 중

레포: `we-meet-trip/map-service-user` (Spring Boot 3.4.2, JDK 21)

**⚠️ 2026-06-26 이전 버전은 "인증 도메인 구현 완료"라고 적혀 있었으나 틀렸음.** 실제로는:
- develop엔 `AuthPlaceholder.java`만 있음(빈 클래스). PR#7은 CLOSED(폐기). 실제 auth 구현은 `feat/login-dev` 브랜치(PR 미생성, develop 미반영).
- develop엔 대신 recommend/schedule/trip 3개 도메인이 PR #9~#20으로 이미 구현되어 있음(이전 문서에 전혀 언급 안 됐던 부분).

**완료된 작업 (develop, ~PR #20):**
- recommend: 생성/폴링/편집/재생성 4개 엔드포인트, agent 연동(`AgentClient`), Redis Streams 비동기 수신(`RecommendJobsConsumer`, ack/재시도/DLQ)
- schedule: 저장 API(`ScheduleService.persist`), Flyway `schedules` 테이블
- trip: `POST /api/v1/trip/generate` 동기 facade (client가 실제로 쓰는 엔드포인트)

**진행 중 (2026-07-07 시작, 브랜치 `feature/UserRecommendReuseCache`):**
- 추천 재사용/idempotency 설계 — client 재시도로 인한 agent 중복호출 방지가 핵심 목표
- **실제 위험 지점은 `/api/v1/trip/generate`**: 서버 내부 120초 동기 폴링(`TripService.awaitDraft`) vs 클라이언트 타임아웃 미설정 → 배포 시(ALB 등) 조기 연결종료+재시도로 agent/LLM 이중호출 가능. 아직 방어 로직 없음.
- SSOT 문서(`소프트웨어_아키텍처_설계서_ver_5.0.pdf` §7.1) 재확인 결과 recommend/schedule 흐름이 문서 의도(schedule 먼저 생성 → `(schedule_id, stage)`로 추천 누적)와 다르게 구현돼 있음을 발견 — 다른 팀원 작성 코드라 임의 수정 안 하고 팀 논의 필요 상태로 보류.
- user_id(auth) 의존 여부는 재사용캐시 최종 범위 확정 후 결정 예정(현재 결정 안 됨).

**미완료 / 다음 작업:**
- `feat/login-dev` develop 병합 (auth 도메인) — `trips`/`trip_recommendations`/`trip_segments` 명명이 SSOT의 `schedules` 통일 방침과 충돌, 병합 전 정리 필요
- 재사용캐시 최종 스코프 확정 → user_id 필요 여부 결정
- Apple OAuth2, 프로덕션 배포(CI/CD), VPS·AR 앵커 (`docs/MAP/VPS_AR_SPEC.md`)

**주의사항:**
- **git push 절대 금지** — 사용자 명시적 승인 후에만 push (`절대 push는 하지 마세요`)
- 로컬 작업 디렉토리: `c:\onedrive\_대학교\MAP\git\map-service-user`
- git user: `yj2trigger`, org: `we-meet-trip`
- **recommend/schedule 도메인은 다른 팀원 작성분 — SSOT 불일치 발견해도 팀 논의 없이 임의로 고치지 않는다**
- 상세 상태: `docs/MAP/map-service-user/CURRENT_STATE.md`

---

## GitHub MCP 사용 방법

이 레포와 하위 프로젝트 레포는 GitHub MCP로 직접 파일을 읽고 쓸 수 있습니다.

```
owner: yj2trigger / we-meet-trip
repos:
  - task-management-repository  (이 레포)
  - pmg-ic-pbl                  (ic-pbl 코드)
  - ESG                         (ESG 코드)
  - map-service-user            (MAP 코드, org: we-meet-trip)
```

**작업 흐름:**
1. `docs/<프로젝트>/CURRENT_STATE.md` 읽기 → 현재 상태 파악
2. 관련 설계 문서 읽기
3. 코드 작업 (해당 레포에 직접 커밋)
4. `CURRENT_STATE.md`, `tasks/` 업데이트
5. 사용자 승인 후 다음 단계

---

## 문서 구조

→ [README.md](./README.md) 참고
