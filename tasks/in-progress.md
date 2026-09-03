# 🔄 In Progress

> 현재 진행 중인 태스크 목록입니다.

---

## ✅ MAP (map-service-client) — 비전 화면 전면/후면 카메라 전환 *(2026-09-03 머지 완료)*

> **완료** — client PR #76 머지(2026-09-03). 아래는 작업 당시 기록이며, 요약은
> `tasks/done.md` 참조. 다음 정리 때 이 절은 done 으로 옮겨도 된다.

- **시작**: 2026-08-07
- **배경**: 배포된 앱에서 "전면 카메라만 작동"하는 버그 제보 — 원인 확인 결과
  `lib/features/vision/screens/vision_screen.dart`의 `_initCamera()`가 `availableCameras()`
  목록의 **`cameras.first`를 무조건 사용**하고 있었음(전환 로직 자체가 없었음). 기기별로
  이 목록의 0번이 항상 후면이라는 보장이 없어서, 특정 기기에선 전면이 0번으로 나와 버그처럼
  보였던 것.
- **수정 완료**(`vision_screen.dart` 1개 파일만 변경, 새 패키지/의존성 없음):
  - `_backCamera`/`_frontCamera` 필드 추가(전체 목록 대신 필요한 두 개만 보관)
  - `_initCamera()`: `cameras.first` → `CameraLensDirection.back`/`front`로 명시적 탐색(버그 수정 겸함)
  - `_switchCamera()` 신규 — 현재 컨트롤러 dispose 후 반대쪽 렌즈로 재생성
  - 상단바의 빈 여백(`SizedBox(width: 34)`, 왼쪽 뒤로가기 버튼과 균형 맞추던 용도)을
    전환 버튼(`Icons.cameraswitch`)으로 교체 — 새 레이아웃 안 만들고 기존 자리 재사용
- **검증 완료(2026-08-07)**: 실제 기기(Galaxy S24 Ultra, 무선 디버깅)에 설치해 실기 확인 —
  전환 버튼이 상단바에 정상 노출되고, 탭하면 전면/후면이 실제로 전환됨. 사용자 직접 확인.
- **검증 과정에서 겪은 빌드환경 이슈(전부 이번 기능 코드와 무관, 참고용 기록)**:
  1. `flutter analyze`가 레포 경로의 한글(`_대학교`) 때문에 분석 서버가 JSON-RPC 파싱
     단계에서 크래시 — 수동 코드 리뷰로 대체.
  2. Gradle(AGP)이 같은 이유로 빌드 자체를 거부 — `android/gradle.properties`에
     `android.overridePathCheck=true` 추가로 우회(공식 문서화된 옵션).
  3. 그래도 `aapt`(APK 매니페스트 추출 도구)는 한글 경로를 못 읽어 "Illegal byte sequence"로
     실패 — `subst`/NTFS junction 둘 다 안 통함(Flutter가 내부적으로 실제 경로로 재귀함) →
     결국 프로젝트 폴더 자체를 `C:\dev\map-service-client`로 실제 이동해서 해결.
  4. `phosphor_flutter` 2.1.0(아이콘 패키지, 최신판 없음)이 Flutter 3.44부터 `IconData`가
     `final`로 막힌 것과 충돌해 클린빌드 불가 — FVM으로 프로젝트를 Flutter 3.41.9(Dart
     3.11.5, 이 변경 이전 버전)에 고정(`.fvmrc` 생성)해 우회. **근본 해결책은 별개 팀 작업으로
     필요**: `phosphor_flutter` → 공식 후속판 `phosphoricons_flutter`로 교체(API가 함수호출
     방식에서 상수접근 방식으로 바뀌어서 단순 치환 아님, `app_icons.dart` 등 3개 파일·12줄
     영향받음 — 정확한 상수명은 실제 설치해서 확인 필요).
  5. Android 에뮬레이터(Pixel 8)는 이 PC의 GPU(Intel Arc 듀얼 GPU 구성) 드라이버와 계속
     충돌·행/크래시 반복 — headless+swiftshader(`-no-window -gpu swiftshader_indirect
     -no-snapshot-load`)로 겨우 부팅은 시켰으나 소프트웨어 렌더링이 너무 느려서(프레임당
     4~5초) 실사용 불가 수준 — **최종적으로 무선 디버깅으로 실제 폰 연결해 검증함**(에뮬레이터
     아님).
- **별개로 발견한 이슈(이번 범위 밖) → 2026-08-13~14 해결 완료**: 같은 화면의
  WebSocket(`/ws/vision`, 대상은 `map-yoloservice`)이 연결 실패하던 문제.
  당시 추정 원인은 (a) `map-yoloservice`가 `map-service-infra` 오케스트레이션에 통합
  안 돼있음, (b) 클라이언트 `.env`의 `VISION_SERVER_HOST=localhost:8001`가 실기기 기준
  "폰 자기 자신"을 가리킴 — 둘 다 처리됨.
  - (a)는 **추정이 틀렸음**: compose에 `yolo` 서비스가 `vision` 프로파일로 이미 정의돼
    있었고, 실제로는 "정의는 있으나 한 번도 기동해본 적이 없어 깨진 걸 몰랐던" 상태였음.
    띄워보니 빌드 컨텍스트 경로 불일치·torch가 CUDA 휠로 잡히는 문제·Dockerfile 포트
    불일치(8001 vs 나머지 전부 8000) 3건이 순차로 드러나 전부 수정.
  - (b)는 `VISION_SERVER_HOST`를 아예 안 쓰고 `API_BASE_URL`을 infra proxy(8090)로
    지정하는 방식으로 해결 — proxy가 `/ws/vision`을 넘겨주므로 client는 주소를 하나만 알면 됨.
  - **검증(2026-08-14)**: 실기(Galaxy S24 Ultra)에서 컨테이너 7개 전부 healthy,
    yolo 로그에 `"WebSocket /ws/vision" [accepted]` 연결 수립 확인, STT 실동작 확인.
    Gemini 식별 응답까지의 전체 왕복은 미검증(adb로 마이크/카메라 입력 주입 불가).
  - 상세 경위와 남은 팀 논의 항목은 **`docs/MAP/map-yoloservice/DEV_LOG.md`가 정본**.
- **팀 논의 필요**: `.fvmrc`(Flutter 3.41.9 고정)를 커밋해서 팀 전체에 적용할지, 아니면
  로컬 임시조치로만 둘지 — 3.44+ 필요해지는 시점(phosphoricons_flutter 마이그레이션 완료 전)
  까지는 팀 전체가 3.41.9로 맞추는 게 "나만 되고 남은 안 되는" 상황을 막을 수 있음.

---

## MAP (map-service-user) — 추천 재사용/Idempotency 설계

- **시작**: 2026-07-07
- **브랜치**: `feature/UserRecommendReuseCache`
- **상태 (2026-07-17 갱신)**: 1차 구현 완료 + 로컬 end-to-end 검증 완료(아래 시연 항목 참고).
  단, 히트율 낮은 문제 확인됨 — 우선순위상 다른 기능 개발 먼저 진행하기로 하고 개선은 보류.
- **목표**: client(`map-service-client`)의 "생성" 버튼 재시도/네트워크 재전송으로 agent(LLM) 호출이 중복 발생하는 것 방지. 실제 위험 지점은 `/api/v1/trip/generate`(120초 동기 폴링, `TripService`).
- **시연/검증 방법 (2026-07-17)**: `docs/MAP/map-service-user/DEMO_SCRIPT_RECOMMEND_CACHE.md` —
  agent 스텁(`fake_agent.py`, 문서에 전문 포함)으로 실제 agent 없이 캐시 히트/미스를
  end-to-end로 재현하는 절차. 같은 입력 2회 제출 → 1차 `X-Recommend-Cache: MISS`,
  2차 `HIT` 확인. 인프라(Docker Redis/Postgres) 기동부터 정리까지 이 문서 하나로 재현 가능.
- **알려진 이슈(보류)**: 캐시 키가 province/city/theme/mobility/date(완전일치)/time(라운딩)/
  budget(내림) 전부 일치해야 히트라 실사용 히트율이 낮을 것으로 예상. date 완화 매칭 아이디어는
  `tasks/map-service-user-recommend-cache-date-match-idea.md`에 보류 사유와 함께 기록돼있음.
  지금은 다른 기능 개발 우선이라 착수 안 함.
- **재탐색(research) 로직 현황 — SSOT 대비 갭 (기존 추적 항목, 재확인만 함)**:
  현재 `RecommendService.research(jobId, request)`는 `draftStore.delete(jobId)` 후
  `agentClient.requestRecommend(request)`만 호출 — 재사용 캐시를 전혀 거치지 않고
  매번 무조건 agent 재호출(모드 구분/제외장소 전달/횟수 제한 없음). 이는 새로 발견한 게
  아니라 `tasks/map-verification-plan.md`의 **V-F-07~12**(SSOT §7.1/requirements §3.3 기준,
  2026-07-07 "전부 미구현 확정")가 이미 추적 중인 항목 그대로임 — 여기서는 임의로 고치거나
  판단을 바꾸지 않고, 지금 코드가 정확히 그 문서가 말하는 "미구현" 상태와 일치함만 재확인.
  SSOT가 요구하는 모드 1(제외장소+3회 카운터+KST 자정 차단)/모드 2·3(LLM 미호출) 분기를
  구현하려면 PRE-05(생성 순서 불일치, `CURRENT_STATE.md` 참고)부터 팀 논의로 정리해야 함.
- **미결정 사항**:
  1. 조건 매칭 재사용("장소 5개 중 3개 캐시, 2개 신규")까지 이번에 구현할지 — user_id(auth) 의존성 있어 보류 중
  2. `feat/login-dev`(인증) develop 병합 시점/순서 — "병합이 필요 없을 수도 있다"는 전제로 재사용캐시 스코프 먼저 확정 후 결정하기로 함
  3. SSOT 문서(§7.1)가 요구하는 "schedule 먼저 생성 → (schedule_id, stage) 누적" 구조와 현재 코드(agent 먼저 호출 → 저장은 최후)가 다름 — 이 구조 차이를 재사용캐시 설계에 어떻게 반영할지 팀 논의 필요
- **결정 (2026-07-17)**: 재사용 캐시 전용 Redis DB를 5→6으로 변경. `map-service-infra`의
  `.env.example` DB 매핑 주석(DB5=채팅, 2026-07-16 제무 커밋으로 예약)과 충돌해서 발견함.
  `application.yml`(`redis.db-cache`) + `RedisConfig.cacheConnectionFactory` 기본값 6으로 수정 완료.
- **후속 작업(미완료)**: `map-service-infra`의 `.env.example` Redis DB 매핑 주석 표에 "DB6=재사용 캐시(map-service-user)"
  줄 추가 필요 — 이 브랜치가 develop에 머지되는 시점에 맞춰 infra 레포에도 반영(PR 또는 제무 조율).
  현재는 map-service-user 쪽 코드만 6으로 바꿔둔 상태라, infra 표는 아직 DB6을 모른다.
- **상세**: `docs/MAP/map-service-user/CURRENT_STATE.md`, `tasks/map-verification-plan.md` PRE-05/V-F 항목

---

## MAP (map-service-user + map-service-client) — GPS 좌표 수신 기능 (원샷 → 연속추적)

- **시작**: 2026-07-22 — **팀 회의에서 구현 확정** (기존 "SSOT 미반영, 논의 필요" 상태 해소됨)
- **설계 메모**: [docs/MAP/plans/2026-07-22-gps-location-tracking.md](../docs/MAP/plans/2026-07-22-gps-location-tracking.md) — 상단 "요약(TL;DR)" 절에 전체 계획 압축돼있음
- **개발 로그**: [docs/MAP/map-service-user/DEV_LOG.md](../docs/MAP/map-service-user/DEV_LOG.md) — 상황/판단/결론 형식으로 재사용캐시+GPS 전체 히스토리(DB번호 충돌 2건, 범위축소 결정, 신원문제 조사 등) 기록
- **순서**: 원샷 구현 → (스토어 출시가 필요하다면) 심사 빠른 버전 먼저 출시 → 연속추적은 **나중 업데이트**로 추가 (staged rollout/internal testing 활용 — 설계 메모 "출시 전략" 절)
- **⚠️ 미확인(2026-07-22)**: **Google Play Store 공개 출시가 실제로 필요한지 확정 안 됨.**
  "출시 전략"/"Google Play 백그라운드 위치 승인 절차" 절 전체가 이 전제 위에 세운 것 —
  스토어 출시 불필요로 판명되면(사내/시연/사이드로드 배포 등) 두 절 다 무효, 연속추적 일정에서
  심사 대기(~2주) 리스크도 사라짐. 착수 전 확인 필요
- **전송 방식**: REST 폴링 고정, **WebSocket/MQTT는 로드맵에 없음**(조건부 재검토 항목일 뿐) — 본인전용이든 동행자공유(소규모)든 폴링으로 충분하다고 결론남
- **저장 패턴(연속추적)**: `location:{scheduleId}:userId` 최신값 덮어쓰기+TTL 키(히스토리 안 쌓음) — 설계 메모 "구체 저장 패턴" 절
- **확장 전략**: 지금 규모는 대응 불필요. 필요해지면 수직확장 → 기능별 수동분리(이미 코드상 가능) → Redis Cluster 순 — 설계 메모 "확장 전략" 절
- **진행 상황**:
  - [x] GPS-01: SSOT 반영 여부 팀 논의 — **완료, 구현 확정** (2026-07-22)
  - [ ] GPS-00: **Google Play Store 공개 출시 필요 여부 확인** (2026-07-22 추가, 미확인)
  - [ ] GPS-02: 활용처 확정(도착 인식 / 지역 자동채움 / 경로기록 / **동행자 위치 공유** 중 — 아직 후보만 있고 미확정, 다음 결정 필요)
  - [ ] GPS-03: 원샷 구현 — 요청 DTO(lat/lng/accuracy/timestamp) + 서버 검증 + 저장 스키마 + `POST` 단발 엔드포인트 + 위치 권한(When In Use)
  - [ ] GPS-04: 연속추적 구현 — 원샷 엔드포인트 재사용(호출 주기 조정) + 권한 승격(Always/Background) + (**GPS-00에서 스토어 출시 필요로 확정될 경우만**) Google Play 백그라운드 위치 승인 절차(심사 대기 ~2주, 데모 영상 필요 — 설계 메모 참고) 출시 일정에 반영
- **⚠️ GPS-02 후보 중 "동행자 위치 공유"가 선택되면 설계 전제가 바뀜**: "본인 기기 전용,
  pub/sub 불필요" 결론이 무효화되고 다중 구독자(동행자) 시나리오로 됨 — 단, 소규모 그룹이라
  WebSocket 없이 폴링으로 충분할 전망. 동의(옵트인)/공유중단/일정종료 자동만료 요건 추가됨.
  상세: 설계 메모 "후보 상세 — 동행자 위치 공유" 절
- **로직 합의(2026-07-22, "동행자 위치 공유" 채택 시)**: 위치 → 서버 저장 → 다른 동행자가
  일정 주기(예: 5초)마다 조회해서 반영. **실시간 웹소켓/MQTT 불필요로 확정.**
- **다음 결정 필요**: GPS-02(활용처) 확정돼야 GPS-03 DTO/엔드포인트 구체 설계 착수 가능

---

### 2026-07-24 갱신 — 범위 축소 결정 + 구현 착수

**결정**: "동행자 위치 공유"(실시간 조회/공유중단 등)는 **의도적으로 이번 범위에서 제외**함 —
팀원들이 헷갈릴 수 있어서 나중에 한번에 구현하기로 함. 대신 이번엔 **일반 GPS ping 수신
+ 이동경로(폴리라인) 영구 저장**만 먼저 구현.

**신원(ID→계정) 문제 조사 결과**: 이 기능(여행 종료 후 폴리라인 재생 + 누구 경로인지 특정)은
영구 기록이라 실시간 위치공유(TTL 20초)와 달리 "그 ID가 진짜 그 사람"이 보장돼야 함 — 그래서
`feat/login-dev`(제무님 브랜치, PR #21, OPEN 미병합) 확인함:
- `users` 테이블(BIGSERIAL id, email, nickname, ...) 존재 — 실제 계정 PK 공간
- `JwtAuthenticationFilter`가 `SecurityContextHolder`에 심는 **principal이 정확히 `Long userId`**
  → 지금 설계(`LocationPingRequest.userId: Long`)가 타입이 이미 일치해서, auth 병합 후
  "client가 보낸 user_id 신뢰" → "`@AuthenticationPrincipal Long userId`로 교체"가 쉬움
- `share_sessions`/`share_members` 테이블이 owner+members 구조로 **스키마만 스텁 존재**
  (로직 없음) — 나중에 "동행자 그룹" 만들 때 참고/재활용 가능할 듯
- 경로기록(폴리라인) 관련 기존 로직은 전혀 없음 — 이번에 완전 신규 구현

**구현 완료 (브랜치 `feature/UserLocationSharing`, develop에서 분기, 재사용캐시 브랜치와 무관)**:
- `src/main/java/map/service/user/location/` 신규 패키지: `LocationPingRequest`/`LocationPoint`(DTO),
  `LocationLogEntity`/`LocationLogRepository`(Postgres 영구저장, append-only),
  `LocationService`(검증: 일정존재/종료일컷오프/accuracy100m/타임스탬프신선도 + 저장/경로조회),
  `LocationController`(`POST /{scheduleId}/ping`, `GET /{scheduleId}/{userId}/route`),
  예외 2개(`LocationScheduleNotFoundException` 404, `LocationPingRejectedException` 422)
- `V004__location_logs.sql`: `location_logs(id, schedule_id, user_id, lat, lng, accuracy_m, captured_at, created_at)`
  + `(schedule_id, user_id, captured_at)` 인덱스
- Redis는 이번 범위에서 **안 씀**(동행자 실시간 공유용이었던 `LocationStore` 삭제함) — 순수
  Postgres 누적 저장만으로 폴리라인 재구성 가능
- `LocationServiceTest` 8케이스 작성, 컴파일 통과. 자동 테스트 실행은 이 환경의 기존
  Gradle/OneDrive 한글경로 문제로 안 됨(재사용캐시 브랜치 때와 동일 이슈, 코드 문제 아님) —
  대신 로컬 Postgres/Redis 띄우고 **실제 curl로 end-to-end 수동 검증 완료**:
  ping 2회 저장 → route 조회 시 시간순 정확히 반환 확인, 404(없는 일정)/422(accuracy 초과)/
  400(위경도 범위 위반) 전부 기대대로 응답 확인
- 커밋/push는 아직 안 함(요청 대기)

---

## ✅ MAP (map-service-hub) — 대중교통 내비게이션(ODsay 연동) *(2026-09-03 머지 완료)*

> **완료** — hub PR #14 · client PR #77 · user PR #30 모두 머지(2026-09-03).
> 상세 경과와 정량 수치는 `docs/MAP/map-service-user/DEV_LOG.md` §13~21.
> 아래 "남은 후속 작업" 항목들은 머지와 별개로 여전히 열려 있다.

- **시작**: 2026-07-29
- **목표**: 카카오맵처럼 지하철/버스/기차/시외버스/항공 정보를 반영한 이동 지원 기능
  (자전거·킥보드 제외 — 명시적 지시). 개별 조회(노선/역/시간표) + 통합 길찾기 둘 다.
- **API 조사**: TAGO/KRIC/GTFS+OpenTripPlanner/ODsay 비교 검토 후 **ODsay**(lab.odsay.com,
  상용, 실제 API 키 발급받음) 채택. 전체 23개 엔드포인트 파라미터 확정(공식
  `releaseReference` 문서 기준). 실험용 스크립트 `odsay_playground.py`(스크래치패드,
  로컬 전용, 커밋 안 함)로 실제 키 호출 검증 완료.
- **연동 위치 결정 — hub**: map-service-hub를 origin/develop(당시 로컬 대비 29커밋 앞섬)으로
  pull해서 실제 구조 확인. `POST /v1/directions/batch`(OSRM 도보/자전거 프록시)가 이미
  "hub가 외부 라우팅 API를 캡슐화하고 user(BFF)가 소비"하는 패턴으로 실제 동작 중이고,
  스키마 주석에 "bus/transit은 라우팅 대상이 아니므로 BFF가 호출 자체를 하지 않는다"고
  명시돼 있어 — 대중교통은 의도적으로 비워둔 자리였을 뿐 hub 소관 원칙에는 부합.
  → **hub에 `/v1/transit/*` 라우트 신설, user는 이후 별도 계획으로 소비**.
  (주의: 최초 조사 때는 hub 로컬 체크아웃이 오래 fetch 안 돼 있어서 "hub는 거의 빈 스켈레톤"
  이라고 잘못 판단했었음 — `git fetch` 다시 하니 실제로는 장소/리뷰/룰엔진/OSRM 다 실구현
  돼 있었음. 로컬 체크아웃 최신 여부를 fetch로 먼저 확인 안 하면 이런 오판이 생김.)
- **엔드포인트 선별(23개 중 MVP용 9개 채택)**: 등시선/운수회사별조회/지도화면기반
  주변검색(pointSearch·boundarySearch·pointBusStation)은 카카오맵 고급 UX라 제외.
  선별표·hub 변경 파일 목록은 계획 파일에 상세 기록:
  `C:\Users\rexro\.claude\plans\groovy-painting-journal.md` (Claude Code 로컬 플랜 파일,
  이 레포 밖에 있음 — 참고용, 정식 문서 아님).
- **`loadLane` 사용 불가 발견(2026-07-29)**: 애초 계획은 통합 길찾기의 지도 폴리라인을
  ODsay `loadLane`(mapObject)로 얻으려 했으나, 실제 호출 시 여러 인코딩 방식으로 시도해도
  전부 `-8 mapObject 형식이 잘못되었습니다` 에러 — 공식 문서와 실제 API 버전이 안 맞는 것으로
  추정. **대안 확정**: `searchPubTransPathT` 자체 응답의 `subPath[].passStopList.stations[].
  {x,y}`(지하철/버스 구간 정차역별 좌표) + 도보구간 start/end 좌표로 폴리라인 구성 —
  별도 API 호출 없이 이미 있는 데이터로 해결됨. 따라서 `load_lane`은 최종 구현에서 제외.
- **실시간 버스 도착정보 — 조사 완료, 구현은 보류**: ODsay에는 실시간 도착정보 필드가
  전혀 없음(정적 배차간격만 있음, `busInterval` 등). 국토교통부 TAGO
  (`ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList`, cityCode+nodeId 필요)로
  실제 "몇분 후 도착" 조회 가능함을 확인 — 특히 `BusSttnInfoInqireService/
  getCrdntPrxmtSttnList`(좌표기반근접정류소조회)에 ODsay 정류장 좌표를 그대로 넣으면
  nodeId/cityCode를 별도 매핑 테이블 없이 바로 얻을 수 있어 두 시스템 연결이 생각보다
  단순함을 확인함. **단, 이번 구현 범위에서는 보류**(팀 결정, 2026-07-29) — ODsay만으로
  hub 통합길찾기부터 먼저 구현하고, TAGO 실시간 도착정보는 나중에 별도로 추가.
  후속 착수 시 참고할 설계: TagoClient(nearby_stations/arrivals 2메서드,
  TAGO_SERVICE_KEY 선택값·미설정시 degrade) + 버스 subPath마다 좌표로 근접정류소 조회 →
  ODsay busNo와 TAGO routeno 매칭해 도착정보 필터 → 매칭실패는 null(hub degrade 원칙).
- **진행 상황**:
  - [x] API 비교조사 및 ODsay 채택
  - [x] ODsay 23개 엔드포인트 파라미터 확정 + 실호출 검증(`odsay_playground.py`)
  - [x] 연동 위치 결정(hub) — 실제 코드 구조 근거로 확정
  - [x] MVP 엔드포인트 9개 선별
  - [x] loadLane 대안(passStopList) 확정
  - [x] TAGO 실시간 도착정보 조사(구현은 보류)
  - [x] hub 코드 구현(`config.py`/`hub_clients.py`/`hub_dependencies.py`/`hub_schemas.py`/
        `hub_routers.py`/`.env.example`/`tests/test_transit.py`) — 완료, 테스트 130개 통과
        (기존 113 + 신규 17). `tests/conftest.py`에 `ODSAY_API_KEY` 더미값 추가.
  - [x] 시연용 HTML 시각화 도구(`map-service-hub/static/transit_visualizer.html`) 작성 —
        map-service-user의 `visualizer.html`(Ryu-Jemu PR#18 원작) 관례 그대로: hub에
        `StaticFiles` 마운트해 같은 출처로 서빙(CORS 불필요). 9개 엔드포인트 전부 +
        통합길찾기 결과를 Leaflet 지도에 실제 폴리라인으로 렌더링(지하철/버스/도보 색 구분).
        로컬 hub(venv+uvicorn)로 기동해 실제 키로 검증 — 정류장검색/지하철/항공/통합경로
        전부 실데이터 확인됨(예: 강남→시청 구간 총 38분·환승 3회·1650원).
  - [ ] user(BFF)에서 hub `/v1/transit/*` 소비하는 Client/Service/Controller — 별도 계획(미착수),
        아래 "연동 방식 재검토" 미결정으로 보류
  - [ ] 프론트 지도 렌더링 연동 — 미착수
  - [ ] TAGO 실시간 도착정보 통합 — 보류 중, 위 설계 메모 참고해 착수

### 2026-07-31 갱신 — ODsay 인증 불안정 발견 + 연동 방식 재검토 (미결정)

**프론트 이슈 발견**: map-service-client 레포 Issue #53(seooyoon, "가는 방법 알아보기 -
지하철 경로 탐색 연동") — "가는 방법 알아보기" 화면의 지하철 카드만 우선 ODsay 연동,
나머지(자전거·킥보드/시외버스/항공)는 비활성화. TODO에 `OdsaySubwayService`,
"iOS/Android 별 ODsay API 키 분리 적용"이 있어 **앱이 hub를 거치지 않고 ODsay를 직접
호출하는 걸 전제**하고 있는 것으로 보임 — 이번 hub 작업(서버 경유)과 방향이 다를 수 있음.
착수 전(TODO 체크박스 전부 미완료) 상태라 아직 실제 코드 충돌은 없음.

**ODsay 인증 실패 재현**: 시연 도중 `odsay_playground.py`·hub 양쪽 다 갑자기
`ApiKeyAuthFailed`(-500) 발생 — 이후 재시도 시 다시 정상화됨. 원인: ODsay 콘솔에
"Server(서버 IP)" 플랫폼으로 등록된 IP(`218.235.241.116` 확인됨)가 개발 PC의 **동적
공인 IP**라서, ISP가 IP를 바꾸면 인증이 끊김. 현재 프로젝트엔 고정 IP를 가진 배포
서버가 없음(`map-service-infra`가 "PoC 단일 호스트 오케스트레이션"이라 명시 — 클라우드
서버 자체가 없는 단계).

**연동 방식 트레이드오프 정리** (팀 결정 필요, 미확정):

| | hub 경유(현재 구현) | 앱 직접호출(iOS/Android 키, 이슈#53 TODO 원안) |
|---|---|---|
| 고정 IP 필요 | 필요(클라우드 서버 인프라 작업 필요) | 불필요 |
| 오늘 만든 hub 코드 | 그대로 사용 | 이번 기능엔 미사용(다른 이동수단 붙일 때 재사용 가능) |
| 키 유출 위험 | 없음(서버에만 존재) | 있음(앱 디컴파일로 추출 가능) — 단 스토어 미출시 PoC 단계라 당장 위험도는 낮음 |
| 응답 정규화 로직 | hub(Python)에 이미 구현·검증 완료 | Flutter(Dart)에 재구현 필요 — ODsay 원본은 필드명
  카멜케이스 뒤섞임/좌표 x=경도·y=위도로 뒤집힘/에러가 dict 아닌 list([{"error":[...]}])
  등 그대로 다루기 까다로움. hub가 이미 `TransitPathResponse` 같은 정리된 형태로
  변환해주는 걸 안 쓰게 되는 셈 |
| 검증 방식 확실성 | Server(IP) 방식은 실제로 작동 확인함(단, IP 변경 시 불안정) | Android/iOS 플랫폼
  타입 검증 메커니즘이 ODsay 공식 문서에 명시 안 돼있어 실제로 잘 되는지 미검증 |

**고정 IP 옵션 조사(hub 경유 유지 시)**: Oracle Cloud "Always Free" 인스턴스 추천
(AWS EC2 프리티어는 가입 후 12개월만 무료, 이후 과금 — Oracle Always Free는 기간제한
없음). 대략 1~2시간이면 세팅 가능(계정가입 → VM생성 → Docker설치 → 레포 clone →
`docker compose --profile full up -d` → 그 IP를 ODsay 콘솔에 등록). 주의: Oracle
Always Free 스펙(RAM 1GB급)이 낮아 postgres/redis까지 같이 올리면 빠듯할 수 있음 —
DB는 로컬에 두고 hub만 올리는 것도 검토 필요(단 그러면 hub↔DB가 인터넷 경유 통신).

**URI/Android 플랫폼 타입으로 IP 문제 우회 가능성 검토**: ODsay 공식문서에 각 플랫폼
타입(URI/Server/Android/iOS)의 정확한 검증 메커니즘이 안 나와있음(Referer 헤더 검사인지,
User-Agent인지, SDK 전용 방식인지 불명). 서버가 URI/Android 인 척 위장 요청을 보내는
방식은 확인 안 된 데다, 서버가 아닌 걸 속이는 것이라 ToS 위반 소지가 있어 권장하지 않기로
논의함(대신 정공법인 고정 IP 인프라 또는 진짜 앱 직접호출 둘 중 하나로 결론 내야 함).

**결론(2026-07-31 갱신 — 아래서 해결)**: hub 경유 유지 + 고정IP 서버 구축(a안)으로 진행,
실제로 세팅 완료함. 이슈#53 작성자(seooyoon)와 조율은 아직 안 함 — 다음 액션.

### 2026-07-31 갱신 — GCP 고정 IP 서버로 ODsay 인증 문제 해결

**결정**: Oracle Cloud 대신 **Google Cloud Always Free(e2-micro)**로 진행 — Oracle 가입이
계속 막혀서 대안 채택. GCP도 Oracle과 동일하게 기간제한 없는 상시무료 등급(단, 대상
리전이 us-west1/us-central1/us-east1뿐이라 한국과는 여전히 멂 — 지연시간 트레이드오프는
감수하기로 함, 위 트레이드오프 표의 "고정 IP 인프라" 비용에 해당).

**세팅 완료**:
- VM: e2-micro, us-central1-a, Ubuntu/Debian, 표준 영구 디스크 30GB(전부 무료조건 충족)
- 외부 IP를 고정(정적)으로 예약 — `35.209.70.181`
- 네트워크 서비스 계층은 "표준"으로(프리미엄보다 무료 한도 큼, 월 200GB)
- 방화벽 규칙(`allow-hub-8001`, TCP 8001, 소스 0.0.0.0/0, 대상: 네트워크의 모든 인스턴스)
- Docker 설치 + `map-service-infra`/`map-service-hub`(GitHub 원본, 이번 세션 hub 변경사항은
  아직 push 안 해서 미반영 상태) clone
- **`docker compose --profile infra --profile backend up -d --build hub`로 postgres·redis·hub만
  기동** — `--profile backend`만 켜면 `infra`(postgres·redis)가 별도 프로필이라 안 켜져서
  "undefined service postgres" 에러 남, 두 프로필 같이 켜야 함. hub만 이름 지정했으므로
  agent/user/admin(JWT 등 별도 시크릿 필요)은 안 뜸.
- **`HUB_DATABASE_URL`이 `map-service-infra/.env.example`에 없는 기존 gap 발견** — hub
  Settings는 이 값을 필수로 요구하는데 infra의 `.env.example`엔 POSTGRES_DB/USER/PASSWORD만
  있고 이를 조합한 DSN이 없음. 지금은 VM의 로컬 `.env`에 수동으로
  `HUB_DATABASE_URL=postgresql+psycopg_async://map:<pw>@postgres:5432/map` 추가해서 해결 —
  infra 레포 `.env.example` 자체에도 반영할지는 별도 확인 필요(이번엔 안 건드림).

**검증 완료**: 이 VM에서 `curl -G https://api.odsay.com/v1/api/searchStation ...`으로 실제
데이터 응답 확인(`ApiKeyAuthFailed` 더 이상 안 남) — 고정 IP로 인증 불안정 문제 해결됨.
콘솔에 예전 IP(`218.235.241.116`)는 이제 안 씀, 삭제 가능.

**남은 후속 작업**:
- [ ] hub 포트가 `docker-compose.yml`에 `"127.0.0.1:8001:8000"`(루프백 전용)으로 돼있어서
      VM 안에서만 접근 가능, 외부(프론트/시연)에서 호출하려면 `"8001:8000"`으로 수정 필요
- [ ] 오늘 세션에서 만든 hub `/v1/transit/*` 코드를 push해서 이 VM이 실제 기능 버전으로
      재배포되게 하기(지금 VM엔 GitHub 원본 hub만 있음, 커밋 전이라 반영 안 됨)
- [ ] 이슈#53 작성자(seooyoon)에게 hub 경유 방식 제안 + TODO 수정 요청(OdsaySubwayService/
      iOS·Android별 키분리 항목 제거)
- [ ] ODsay 콘솔 예전 등록 IP(`218.235.241.116`) 정리(선택)

---

## MAP (map-service-client) — 채팅 실시간(WebSocket) 연동

- **기간**: 2026-09-01 ~ 09-03
- **배경**: 서버(`map-service-user`)의 채팅 도메인은 `develop`에 완성돼 있었으나
  (STOMP over WebSocket · Redis 팬아웃 · 프레즌스, 58파일), **클라이언트는 채팅 전체가
  가짜**였다 — `MockChatRepository`가 하드코딩한 방 2개를 돌려주고 있었고 `api/v1/chat`
  호출이 0건. `chat_event_test.dart`가 없는 파일을 import 해 컴파일도 되지 않았다.
- **한 일**: STOMP 1.2 프레임을 라이브러리 없이 직접 구현(서버가 SockJS 미사용).
  REST 계층·저장소·화면 연결까지. 28파일 · +3,472/-290줄 · 커밋 18개
  (브랜치 `feat/chat-websocket`, **로컬만 — 푸시·PR 안 함**).
- **검증**: 시험 50건(장애 시나리오 22 · 화면 5 · 저장소 13 · 프레임 8 · 실서버 2).
  재연결 대기가 최대 30초라 `fake_async`로 시계를 압축해 22건이 0.1초에 끝난다.
  실서버 검증에서는 클라이언트만 끊기 위해 TCP 중계기를 Python 50줄로 작성
  (앱 → 8099 중계기 → 8081 서버) — 서버를 죽이면 "끊긴 사이 상대가 보낸 말"을
  만들 수 없기 때문. 큐 자동 발송이 복구 후 4~8초 내 이뤄짐을 DB seq 대조로 확인.
- **찾은 결함 6건**: 재연결 구간 메시지 유실 / 끊긴 동안 전송 증발 / 좀비 연결
  (하트비트 수신 감시 부재) / 재연결 몰림(지터 부재) / `_teardown()` 의 `await` 교착으로
  **방 전환 자체가 멈춤** / 화면 계층이 소켓 큐를 우회해 REST 로 새어 나감.
  뒤 두 건은 각각 시험과 실기 시연이 아니었으면 못 찾았다.
- **⚠️ 결말 — 대부분 중복이었다**: PR 직전 점검에서 같은 기능이 이미 `develop` 에
  머지된 것을 발견(류제무님 `1b273df`). 작업 중 develop 이 **32커밋** 전진했고 파일
  **15개**가 겹친다. 재연결 백오프·지터·하트비트·오류큐·초대 서버화·목 제거가 전부 중복.
  하트비트는 develop 쪽이 STOMP 규약대로 서버와 주기를 협상해 **더 낫다**.
- **남는 값어치**: develop 에 채팅 **장애 시험이 0건**이다(`chat_wiring_test.dart` 8건은
  전부 주소 파생·응답 매핑). 장애 대응 코드는 평소 실행되지 않아 깨져도 드러나지 않는다.

**남은 후속 작업**:
- [ ] 구현은 develop 것을 채택하고, **그 API 를 대상으로 장애 시험을 다시 작성**
      (22건 → 12건 내외로 정리. 지터 12시드 루프 등 과한 것 정리)
- [ ] develop 워치독의 `DateTime.now()` 판정 → `Stopwatch`(단조시계) 교체.
      절전 복귀·시계 동기화로 시각이 점프하면 멀쩡한 연결을 끊고, `fake_async` 가
      벽시계를 못 속여 **시험 자체가 불가능**하다
- [ ] 말풍선 대기 표시(회색) — 지금은 전송 실패와 성공이 화면에서 구분되지 않는다
- [ ] 망까지 끊겼을 때의 전송 보관(큐) 도입 여부 판단 — develop 의 REST 폴백은
      소켓만 죽은 경우엔 통하지만 터널 등 망 단절에는 함께 실패한다
- [ ] (별건) README 에 `.env` 생성 안내 — 새로 클론하면 에셋 오류로 빌드가 멈추는데
      안내가 0건. 빈 클론에서 재현 확인함. `.env` 자체는 커밋 대상 아님
- [ ] 결정 후 PR 방식 확정 — 디스코드 공지대로 develop 직접 머지할지, PR 로 낼지
