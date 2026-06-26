# jemu(@Ryu-Jemu) 작업 패턴 — 완전 레퍼런스

> **SSOT**: 이 파일이 jemu 컨벤션의 단일 진실 공급원.
> 분석 근거: PR #2~#18 전체 diff·body·review, Issue #1~#8, develop 브랜치 전체 커밋 타임라인 전수 조사.
> skeleton 초기화 작업 제외.

> ⚠️ **미확인 항목** (→ [`jemu-analysis-plan.md`](./jemu-analysis-plan.md)):
> - PR body 산문 내 클래스명 백틱: 대다수 사용, 일부 미사용 — 의도/스타일 여부 불명확 (실용 기준: 백틱 권장)

---

## 0. 전체 워크플로우 순서

```
[pre-feature]
  1. chore 이슈 생성 → chore 브랜치 → 커밋(들) → PR → 리뷰어 지정 → 봇 리뷰 대응 follow-up 커밋 → 머지

[feature]
  2. feat 이슈 생성 (대이슈 1개)
  3. 관심사별 브랜치 분리 → 각 브랜치 커밋 1개 → 각각 PR 오픈 (배치)
     순서: DTO → Config → Client → Store → Consumer → API → Domain → ErrorHandler → DLQ

[post-feature]
  4. docs 브랜치 → 모든 파일 Javadoc + PoC HTML → PR → 머지
```

---

## 1. 기능 구현 전 작업 (pre-feature chore)

### 목적

기능 개발이 가능한 프로젝트 골격을 먼저 갖춘다.

pre-feature chore PR은 **프로젝트 최초 skeleton 1회만** 수행. 이후 기능 추가 시 chore 없이 바로 feat 브랜치 생성. hub·agent 레포 동일 패턴으로 확인.

### 실제 작업 내용 (PR #5 기준)

```
브랜치: chore/InitialSetting → develop
커밋 수: 2개 (본 작업 1 + 봇 리뷰 대응 1)
리뷰어: dmlwjds2 지정
```

커밋 1 (`2026-05-17T06:29:11Z`):
```
chore: user Spring Boot BFF + Flyway 골격 추가
```
— 도메인별 placeholder 패키지 생성, Flyway V001 baseline, application.yml 통일, dev_deploy.yml 폐기

커밋 2 (`2026-05-17T07:26:56Z`, 봇 리뷰 대응):
```
chore: JWT 미설정 안전 종료 및 Docker build 레이어 캐싱 활용
```
— Gemini 봇이 PR #5에서 지적한 ① JWT secret 빈 기본값(보안), ② Dockerfile 레이어 캐싱을 수정

### chore PR body (섹션 템플릿)

```markdown
## 변경 사항
- [항목1]
- [항목2]

## 체크리스트
- [x] 로컬 테스트 확인
- [x] 불필요한 코드/주석 제거
```

- `## 관련 이슈` 섹션: 연결된 이슈가 있을 때만 추가 (`closes #N`)
- 체크리스트는 제출 시 `[x]` 완료 상태
- 항목은 bullet list, 기술 용어는 원문

### chore 커밋 제목 규칙

```
chore: [레포/서비스] [작업내용] [추가|통일|정렬|보강|폐기]
```

예시:
```
chore: user Spring Boot BFF + Flyway 골격 추가
chore: JWT 미설정 안전 종료 및 Docker build 레이어 캐싱 활용
chore: .gitignore 보강
chore: initial skeleton — templates, license, readme, docker only
```

em dash(`—`) 패턴: 나열할 기술 항목이 여럿일 때 (`— a, b, c`)

---

## 2. 기능 구현 순서

### 이슈 먼저 (대이슈 1개)

```
[FEAT] 에이전트 파이프라인 구현  ← 기능 전체를 커버하는 이슈 1개
```

이슈 설정:
- **Type**: GitHub Issue Type 드롭다운 → `[CHORE]` = Task(노란색), `[FEAT]` = Feature(파란색)
- **Assignee**: 별도 지정 없음
- **Milestone**: 별도 지정 없음
- **Label**: 별도 라벨 없음 (Type으로 대체)

이슈 TODO는 구현 방향·제약 중심 (세부 파일명 아님):
```markdown
## TODO
- [ ] API 호출은 제미나이와 KMA 날씨 Polling
- [ ] FastAPI와 BFF-Gateway 중심으로 구현
- [ ] PoC 기준으로 최소 구현
```

**`[FEAT]` 제목 기준 (hub·agent 이슈 추가 확인으로 확정):**
- 핵심 외부 기술/서비스 있으면 포함: `[FEAT] KMA 시간대별 Polling 구현`, `[FEAT] GEMINI 기반 Fast API 기반 Agent연결`
- 일반 기능이면 기능명만: `[FEAT] 에이전트 파이프라인 구현`

**Description 구조 (확정):**
- CHORE: `"[레포명]에 [대상]을 [동작]한다. [추가 맥락]."` — 레포명 포함
- FEAT: 레포명 없이 기능/목적 설명만. 예: `"사용자 입력값과 Hub 서비스에 저장되어 있는 데이터기반 장소 및 경로 추천 서비스 파이프라인 구현"`

### 브랜치·PR 생성 순서 (실제 타임스탬프)

| 순서 | PR | 브랜치 | 생성 시각 (UTC) | 관심사 |
|------|----|----|------|--------|
| 1 | #9 | `feature/UserRecommendDto` | 05:03 | DTO 계층 |
| 2 | #10 | `feature/UserRedisConfig` | 05:05 | 인프라 설정 |
| 3 | #11 | `feature/UserAgentClient` | 05:33 | 외부 클라이언트 |
| 4 | #12 | `feature/UserDraftStore` | 05:34 | 저장소 컴포넌트 |
| 5 | #13 | `feature/UserStreamsConsumer` | 05:35 | 메시지 소비자 |
| 6 | #14 | `feature/UserRecommendApi` | 05:36 | API + 서비스 레이어 |
| 7 | #15 | `feature/UserScheduleDomain` | 05:42 | 도메인 영속화 |
| 8 | #16 | `feature/UserAgentErrorHandler` | 05:43 | 오류 격리 |
| 9 | #17 | `feature/UserConsumerDlq` | 05:44 | DLQ + 재시도 설정 |
| 10 | #18 | `chore/UserDocstring` | 05:45 | 문서 + PoC HTML |

### 구현 순서 원칙

```
하위 인프라 (DTO → Config → Client → Store → Consumer)
  →  상위 API·도메인 (API/Service → Domain)
    →  횡단 관심사 (ErrorHandler → DLQ)
      →  문서·PoC (Docs)
```

- **DTO 먼저**: 모든 계층이 공유하는 데이터 계약을 먼저 확정
- **Config 다음**: 외부 의존성(Redis, RestClient) 빈 구성
- **Client → Store → Consumer**: 외부 호출 → 임시 저장 → 비동기 수신 순
- **API 마지막 feat**: 하위 계층이 모두 갖춰진 후 엔드포인트 노출
- **ErrorHandler·DLQ**: 정상 흐름 완성 후 예외 경로 처리
- **Docs**: 전체 코드가 안정된 후 문서화

**브랜치 분리 일반 원칙 (hub·agent 레포 추가 확인으로 확정):**

hub 레포 분리 패턴:
- `feature/HubKmaCodes` — 상수·매핑 모듈
- `feature/HubForecastRepo` — 데이터 조회 레이어 (쿼리·RegionLookup)
- `feature/HubWeatherEndpoint` — API 엔드포인트

agent 레포 분리 패턴:
- `feature/AgentSchemas` — 스키마·DTO
- `feature/AgentClients` — 외부 클라이언트
- `feature/AgentNodes` — 비즈니스 로직 노드
- `feature/AgentLifespan` — 진입점·설정·엔드포인트

**일반화 규칙: 하위 데이터 계층 → 상위 API 계층 순. 존재하지 않는 관심사(DLQ, Consumer 등)는 그냥 skip.**

브랜치 접두어:
- user 레포: `feature/User[관심사]`
- hub 레포: `feature/Hub[관심사]`
- agent 레포: `feature/Agent[관심사]`
- 공식: `feature/[서비스명PascalCase][관심사PascalCase]`

---

## 3. 커밋 제목 규칙 — 코드 변경 유형별 전수 매핑

### 원칙

```
1 브랜치 = 1 커밋 (feature PR 전부 commits: 1)
커밋 메시지 = PR 제목과 동일
```

### feat 커밋 제목 공식

```
feat: [도메인/대상] [설명] [추가|구성|처리|격리|차단]
```

### 코드 변경 → 커밋 제목 전수 매핑

**PR #9 → `feat: 추천 도메인 record DTO 추가`**
- 변경: `recommend/dto/` 하위 8개 신규 Java 파일 (Mobility enum, DateRange/Place/Leg/RecommendRequest/RecommendResponse/JobAccepted/EditRequest record)
- 패턴: `@JsonValue/@JsonCreator`, `@JsonProperty` snake_case, `@NotBlank/@Size/@NotNull/@Valid`
- 규칙: `feat: [도메인] [계층] 추가`

**PR #10 → `feat: Redis 멀티 DB 연결 의존성 추가`**
- 변경: `config/RedisConfig.java` 신규 (LettuceConnectionFactory 3개, StringRedisTemplate 2개) + `build.gradle` jackson-datatype-jsr310 추가
- 규칙: `feat: [기술명] [구성내용] 추가`

**PR #11 → `feat: agent 호출용 RestClient 빈과 AgentClient 추가`**
- 변경: `config/AgentClientConfig.java` 신규 (JdkClientHttpRequestFactory 기반 RestClient 빈) + `recommend/AgentClient.java` 신규 (POST /v1/recommend 어댑터)
- 규칙: `feat: [외부서비스] 호출용 [구성 + 클라이언트] 추가`

**PR #12 → `feat: 추천 결과 임시저장 컴포넌트 추가`**
- 변경: `recommend/DraftStore.java` 신규 (Redis SET/GET/EXPIRE/DEL 4메서드, key prefix "recommend:result:")
- 규칙: `feat: [저장 대상] [컴포넌트 역할] 추가`

**PR #13 → `feat: agent:jobs:done Streams 구독 컨테이너와 명시적 ack 처리`**
- 변경: `config/StreamsConsumerConfig.java` 신규 (StreamMessageListenerContainer 빈, @PostConstruct XGROUP CREATE) + `recommend/RecommendJobsConsumer.java` 신규 (StreamListener, DraftStore.save 후 ack, PEL 재처리)
- 규칙: `feat: [스트림 이름] [역할] 처리` — 스트림 이름(`agent:jobs:done`)을 제목에 직접 포함

**PR #14 → `feat: 추천 BFF 4개 엔드포인트와 서비스 레이어 추가`**
- 변경: `recommend/RecommendController.java` 신규 (POST/GET/{id}/POST/{id}/edit/POST/{id}/research 4개) + `recommend/RecommendService.java` 신규
- 규칙: `feat: [도메인] [N개 엔드포인트]와 [서비스 레이어] 추가` — 엔드포인트 수 명시

**PR #15 → `feat: 일정 도메인과 user_service.schedules 영속화 추가`**
- 변경: `schedule/` 패키지 6파일 신규 (Controller/Entity/Service/Repository/SaveRequest/NotFoundException) + `V002__schedules.sql` (JSONB 컬럼, 인덱스 2개)
- 규칙: `feat: [도메인] 도메인과 [DB 테이블 전체명] 영속화 추가`

**PR #16 → `feat: agent upstream 오류 격리`**
- 변경: `common/GlobalExceptionHandler.java` 신규 (AgentRequestException→502, ResourceAccessException→504) + `recommend/AgentRequestException.java` 신규
- 규칙: `feat: [외부서비스] [오류 유형] 격리` — "격리"는 외부 오류가 내부로 전파되지 않음을 표현

**PR #17 → `feat: Consumer DLQ와 max-retry 설정으로 무한 재시도 차단`**
- 변경: `application.yml` streams 섹션 DLQ 설정 추가 (recommend-dlq-stream/recommend-max-retry/dlq-maxlen) + `RecommendJobsConsumer.java`에 ConcurrentHashMap 카운터, DLQ XADD 로직
- 규칙: `feat: [컴포넌트] [기능]으로 [방지할 문제] 차단` — "차단"은 무한 루프 방지를 표현

**PR #18 → `docs: user의 모든 컨트롤러/서비스/설정/리소스에 대해 다중 라인 주석 추가`**
- 변경: 전체 파일 Javadoc 추가 + `static/visualizer.html` 신규 (454줄 SPA)
- 규칙: `docs: [레포] [범위] [주석 유형] 추가 + [추가 산출물]`

### 동사 선택 기준

| 동사 | 사용 조건 | 예시 |
|------|---------|------|
| `추가` | 새 파일·클래스·기능 생성 | `DTO 추가`, `빈과 클라이언트 추가` |
| `구성` | 설정·빈 정의 (주로 Config 클래스) | `Redis 멀티 DB 연결 의존성 추가` (의존성도 추가로 표현) |
| `처리` | 수신·소비·핸들링 | `Streams 구독 컨테이너와 명시적 ack 처리` |
| `격리` | 외부 오류가 내부로 전파 차단 | `agent upstream 오류 격리` |
| `차단` | 무한 루프·무한 재시도 방지 | `무한 재시도 차단` |
| `보강` | 기존 설정 파일 보완 | `chore: .gitignore 보강` |
| `폐기` | 파일·설정 삭제 | (변경사항 목록 내 항목으로) `dev_deploy.yml 폐기` |

---

## 4. PR 분리 기준

### 원칙: 아키텍처 관심사 하나 = 브랜치 하나 = PR 하나

파일 수·라인 수 무관. 책임(responsibility)이 기준.

### 실제 분리 사례 전수

| 브랜치 | 관심사 | 파일 수 | 추가 라인 |
|--------|-------|---------|---------|
| `feature/UserRecommendDto` | 데이터 계약 (DTO·enum) | 8 | 238 |
| `feature/UserRedisConfig` | 인프라 설정 빈 (Redis 멀티DB) | 2 | 197 |
| `feature/UserAgentClient` | 외부 서비스 HTTP 클라이언트 | 2 | 129 |
| `feature/UserDraftStore` | Redis 저장소 컴포넌트 | 1 | 98 |
| `feature/UserStreamsConsumer` | 비동기 메시지 소비자 + ack | 2 | 320 |
| `feature/UserRecommendApi` | HTTP 엔드포인트 + 서비스 레이어 | 2 | 238 |
| `feature/UserScheduleDomain` | JPA 도메인 + Flyway 마이그레이션 | 7 | 381 |
| `feature/UserAgentErrorHandler` | 오류 변환 + 글로벌 핸들러 | 2 | 155 |
| `feature/UserConsumerDlq` | DLQ 설정 + 재시도 로직 | 2 | 111 |
| `chore/UserDocstring` | 전체 Javadoc + PoC SPA | 12 | 644 |

### 브랜치명 공식

```
feature/User[PascalCase관심사명]   — user 레포 feature 작업
chore/[PascalCase]                 — 설정·정리·문서
ci/[이슈번호]                      — CI 파이프라인
feat/[kebab-case]                  — 소규모 feat
```

### 브랜치 베이스 및 머지 전략

- 모든 `feature/*` / `chore/*` / `ci/*` 브랜치: **`develop`에서 생성**, PR base도 `develop`
- `develop` → `main` PR: feat 이슈 TODO 전부 `[x]` 체크 완료 시 오픈
- 머지 전략: **GitHub web UI Merge commit** — squash / rebase 사용 안 함 (`web-flow` committer로 확인)

### 관심사 분리가 애매할 때 판단 기준

- Config 빈 정의 (RedisConfig, AgentClientConfig) → 별도 Config 브랜치
- 외부 API 호출 어댑터 → Client 브랜치
- 저장소 메서드 (Redis/DB CRUD) → Store/Domain 브랜치
- HTTP 엔드포인트 + 그것을 호출하는 Service → 하나의 API 브랜치
- 예외 클래스 + 그것을 처리하는 Handler → ErrorHandler 브랜치로 묶음
- application.yml 수정만으로는 브랜치 분리 안 함 → 해당 기능 브랜치에 포함

---

## 5. PR body 작성 규칙

### 5a. 섹션 템플릿 — chore / ci / develop→main PR

```markdown
## 변경 사항
- [항목]
- [항목]

## 관련 이슈
closes #N

## 체크리스트
- [x] 로컬 테스트 완료
- [x] 불필요한 코드/주석 제거
```

사용 조건:
- `chore/*` 브랜치의 PR
- `ci/*` 브랜치의 PR
- `develop` → `main` 통합 PR

세부 규칙:
- `## 관련 이슈` 섹션: 연결 이슈 없으면 생략
- 체크리스트 완료 여부: 정상 제출 시 `[x]`, CI PR처럼 긴급 제출 시 `[ ]` 그대로도 허용
- `## 변경 사항` 항목: bullet list, 파일명보다 작업 내용 중심

### 5b. 산문 스타일 — feat / docs PR

섹션 헤더 없음. 구현 내용을 서술형 산문으로.

**원칙:**

1. **백틱으로 코드 요소 강조**
   - 클래스명: `` `StreamMessageListenerContainer` ``
   - 메서드명: `` `AgentClient.requestRecommend` ``
   - 설정 키: `` `redis.draft-ttl-seconds` ``
   - 스트림/그룹명: `` `agent:jobs:done` ``, `` `bff-result` ``
   > ⚠️ TBD (부분 확정) — hub·agent PR 대다수는 백틱 사용. user PR #9, agent PR #7·#8은 plain text. 스타일 미적용인지 의도인지 불명확. **실용 기준: 백틱 사용 권장, 없어도 오류 아님.**

2. **서술형 종결어미**
   - `"~한다"`, `"~를 받도록 한다"`, `"~를 구성한다"`, `"~를 수행한다"`

3. **설정값 인라인 명시**
   - `(connectTimeout 5s, readTimeout 60s)`
   - `(DB2)`, `(DB3)`, `(DB4)`
   - `EX 3600`, `maxlen 2000`

4. **빈 줄로 단락 구분** — 연관된 설명끼리 묶어 개행

5. **설계 의도 포함**
   - `"실패 시 PEL 잔류로 재처리되도록 한다"`
   - `"BUSYGROUP 응답은 무시한다"`
   - `"시크릿 누출을 방지하고 로그에는 full body를 기록한다"`

6. **HTTP 상태·헤더 명시**
   - `202 + Retry-After:3`
   - `502 Bad Gateway`, `504 Gateway Timeout`

7. **예외·엣지케이스 명시**
   - `"malformed 메시지는 즉시 ack"`
   - `"draft 부재 시 ScheduleNotFoundException으로 404"`

**실제 PR body 예시 (원문)**

PR #11 (`feat: agent 호출용 RestClient 빈과 AgentClient 추가`):
```
`JdkClientHttpRequestFactory`(connectTimeout 5s, readTimeout 60s)
기반 RestClient 빈을 정의하고 `AgentClient.requestRecommend` 가
`POST /v1/recommend 로 JobAccepted`를 받도록 한다.
```

PR #13 (`feat: agent:jobs:done Streams 구독 컨테이너와 명시적 ack 처리`):
```
`StreamMessageListenerContainer`를 `streamsConnectionFactory` 위에
구성하고 `group bff-result, consumer user-1`로 `lastConsumed offset`부터
receive 한다.

@PostConstruct 에서 XGROUP CREATE 를 시도하고 BUSYGROUP 응답은 무시한다.

`RecommendJobsConsumer` 는 onMessage에서 `DraftStore.save` 성공 시에만
acknowledge 를 호출하여 실패 시 PEL 잔류로 재처리되도록 한다.
malformed 메시지는 즉시 ack.
```

PR #16 (`feat: agent upstream 오류 격리`):
```
RestClient.onStatus(HttpStatusCode::isError, ...) 로 4xx/5xx 응답을
AgentRequestException 으로 변환한다. body 는 100자 truncate 하여
시크릿 누출을 방지하고 로그에는 full body 를 기록한다.

GlobalExceptionHandler 가 AgentRequestException 을 502 Bad Gateway,
ResourceAccessException 을 504 Gateway Timeout 으로 매핑하고
{error, upstream_status, detail} 단일 포맷을 반환한다.
```

**docs PR body 스타일 (파일별 bullet)**

PR #18:
```
ServiceUserApplication / auth / common / config placeholder:
- RedisRepositoriesAutoConfiguration 제외 의도, 각 패키지의 책임
  한 줄 요약 + 향후 확장 지점 명시
recommend 패키지 (Controller, Service, AgentClient,
  AgentRequestException, DraftStore, RecommendJobsConsumer):
- 4개 엔드포인트의 입력/응답, RestClient onStatus 4xx/5xx 처리,
  EditRequest shallow merge, research 시 이전 키 DEL, DLQ + max-retry
  흐름과 deliveryCounts 추적을 표준 형식으로 정리
...
```

패턴: `[패키지/클래스그룹]:` 다음 줄에 `- [주석 내용 설명]` (2칸 들여쓰기)

---

## 6. 기능 구현 후 작업 (post-feature docs)

### 타이밍

모든 feature PR 오픈 완료 직후 (PR #17 오픈 후 1분 이내 PR #18 오픈).
기능 코드가 완전히 안정된 시점에 일괄 Javadoc 작업.

### 브랜치

```
chore/UserDocstring → develop
```

- 브랜치 타입: `chore/` (feat 아님 — 기능 변경 없음)
- 브랜치명: `User` 접두어 + `Docstring` (문서화 작업 명시)

### 포함 내용

**1. 모든 파일에 Javadoc 추가**

대상 범위: 진짜 모든 파일 — Controller, Service, Config, Entity, Repository, Exception, DTO, Application, build.gradle, application.yml, Dockerfile, SQL migration

**Javadoc 형식 (PR #18 실제 diff 확인으로 확정):**

**Java 클래스 — `/** */` 블록:**
```java
/**
 * 클래스명 — 한 줄 요약  (em dash 사용)
 *
 * 본문 설명 (한국어 서술)
 *
 * 소제목:           ← "자동 구성 제외:", "실행 흐름:", "본 패키지의 책임:", "검증 범위:" 등
 * - 항목
 * - 항목
 *
 * 관련 설정:        ← 선택적
 * - ...
 *
 * 동일 패턴:        ← 선택적 교차 참조
 * - {@link 패키지.클래스}
 */
```

**Java 메서드 — `/** */` 블록 (짧게):**
```java
/**
 * 한 문장 동작 설명.
 *
 * @param args  설명  ← main/생성자 등 파라미터 있을 때만
 */
```
- 단순 메서드(`contextLoads()` 등)는 한 문장만, `@param` 없음
- 비즈니스 메서드는 `@param`/`@return` 없이 동작 한 문장만

**비-Java 파일 — 박스형 헤더:**
```
# =============================================================================  ← yml/Dockerfile/properties
# 파일명 — 한 줄 설명
#
# 책임:
# - 항목
#
# 키 설명 / 동작 / 관련:  ← 파일 유형에 맞게
# - ...
# =============================================================================

// =============================================================================  ← settings.gradle (groovy)
-- =============================================================================  ← SQL 마이그레이션
```

**인라인 주석**: 단순 한 줄 설명은 해당 줄 옆에 `#`, `//`, `--` 인라인.

**2. PoC 시각화 HTML (`static/visualizer.html`)**

목적: 팀원이 Postman/curl 없이 브라우저에서 추천 파이프라인 전체 테스트 가능하도록.

포함 기능:
- 입력 폼: province, city, mobility, dateRange, budget, theme
- POST /api/v1/recommend 호출 → jobId 수신
- GET /api/v1/recommend/{jobId} long-poll (POLL_INTERVAL_MS=3000, POLL_MAX=50회)
- 결과 표시: places 테이블, visit_order chips, legs 테이블, raw JSON
- 커뮤니케이션 로그 패널 (타임스탬프 포함)
- POST /{jobId}/research 재요청 버튼

### docs PR body 특징

섹션 헤더 없음. 패키지/파일 그룹별로 나열:
```
[패키지명] ([클래스, 클래스, ...]):
- [주석 내용 한 줄 설명]
- [추가 설명]
```

---

## 7. 팀원 소통 패턴

### PR body = 스펙 문서

별도의 설계 문서·API 문서 없음.
feat PR body가 해당 기능의 스펙 역할:

- **무엇을 하는 코드인가**: 클래스·메서드 이름 + 동작 서술
- **어떤 설정값을 쓰는가**: 인라인 명시
- **예외 동작은 무엇인가**: 조건 + 결과 명시
- **설계 결정의 이유는**: "~를 방지하기 위해", "~되도록 한다"

팀원은 PR body만 읽으면 해당 컴포넌트의 인터페이스와 동작을 파악 가능.

### 리뷰어 지정 기준

| 상황 | 리뷰어 |
|------|--------|
| 중요 chore PR (프로젝트 구조 변경) | `dmlwjds2` 지정 |
| feat PR 배치 | 없음 (리뷰어 없이 오픈) |
| 팀원(dmlwjds2)의 CI PR | `yj2trigger` (내 계정) 지정 |

### 팀원(dmlwjds2) PR 제목 형식

jemu와 다른 스타일 — 이슈 번호 접두어 사용:
```
issue/[번호] | [Type]: [설명]
```
예: `issue/1 | Ci: deploy.yml 생성`

- Type이 대소문자 혼용 (`Ci`, `CI`)
- jemu는 항상 소문자 type: (`feat:`, `chore:`, `docs:`)

### PoC HTML = 팀원용 데모 도구

`visualizer.html`은 팀원이 로컬에서 API 동작 확인 가능하도록.
기능 완성 후 docs PR에 포함. 팀원에게 "브라우저로 바로 테스트해"가 가능한 환경 제공.

---

## 8. Gemini 봇 코드리뷰 대응 패턴

### 봇 리뷰 메커니즘

PR 오픈 시 Gemini AI 봇이 자동으로 코드 리뷰 코멘트 생성.
코멘트는 PR별로 1~6개, 심각도 HIGH/MEDIUM으로 분류.

### 대응 방식: follow-up 커밋

PR #5 사례:
- 봇 지적: JWT secret 빈 기본값(보안), Docker 레이어 캐싱, Dockerfile COPY 와일드카드
- 대응: 같은 브랜치에 추가 커밋 push
  ```
  chore: JWT 미설정 안전 종료 및 Docker build 레이어 캐싱 활용
  ```
- 결과: chore PR에 커밋 2개 (1 본 작업 + 1 봇 대응)

### 봇 코멘트 내용 유형 (실제 지적 사항)

보안:
- JWT secret 빈 기본값 → 미설정 시 fail-fast 종료로 대응
- GlobalExceptionHandler detail 노출 → 내부 IP/포트 노출 방지

성능/리소스:
- `LettuceConnectionFactory` 이중 초기화 → `afterPropertiesSet()` 중복 제거
- `readAllBytes()` OOM 위험 → `readNBytes(4096)` 제한
- `Mobility.values()` 반복 호출 → 캐싱

설계:
- `ConcurrentHashMap` 메모리 누수 (Consumer 재시도 카운터) → Redis Streams PEL 활용 권장
- DraftStore null/blank jobId 미검증
- `mkStream=true` 미설정 시 XGROUP CREATE 실패

코드 품질:
- 방어적 복사 (`List.copyOf()`) 누락
- 입력 범위 검증 (`lat/lng`, `@PositiveOrZero`)
- 설정 키 일관성

### 커밋 없이 무시하는 경우

feat PR #9~#17의 봇 코멘트는 전부 unresolved 상태로 남겨둠.
chore PR처럼 즉각 대응하지 않음 — 배치 작업 중에는 follow-up 없이 진행.

---

## 9. 모방 체크리스트

### 기능 구현 전 (chore)

- [ ] 이슈: `[CHORE] 동작 (기술스택)` — Task 타입, TODO에 파일명 백틱
- [ ] 브랜치: `chore/PascalCase`
- [ ] 커밋: `chore: [레포] [작업내용] [추가|통일|보강]`
- [ ] PR body: 섹션 템플릿 (`## 변경 사항` / `## 체크리스트`)
- [ ] 리뷰어: 팀원 지정
- [ ] 봇 리뷰 HIGH 지적 → follow-up 커밋으로 대응

### 기능 구현 (feat)

- [ ] 이슈: `[FEAT] 기능명` — Feature 타입, TODO에 구현 방향/제약
- [ ] 구현 순서: DTO → Config → Client → Store → Consumer → API → Domain → ErrorHandler → DLQ
- [ ] 브랜치: `develop`에서 `feature/User[관심사]` 생성 — 관심사 하나만
- [ ] 1 브랜치 = 1 커밋 (commit body 없이 제목 줄만)
- [ ] 커밋: `feat: [도메인] [설명] [추가|처리|격리|차단]`
- [ ] PR 제목: 1커밋이므로 GitHub이 커밋 제목으로 자동 채움 (수정 불필요)
- [ ] PR body: 산문 스타일 — 백틱 강조, "~한다" 종결, 설정값 인라인, 설계 의도 포함
- [ ] PR body에 `closes #N` 넣지 않음 — 이슈는 develop→main 머지 후 수동 close
- [ ] 리뷰어 미지정 (배치 작업)
- [ ] 머지: GitHub web UI Merge commit (squash/rebase 아님)

### 기능 구현 후 (docs)

- [ ] 브랜치: `chore/UserDocstring`
- [ ] 모든 파일에 Javadoc 추가 (Controller, Service, Config, Entity, DTO, yml, SQL 포함)
- [ ] PoC HTML 작성 (팀원 테스트용 SPA)
- [ ] PR body: 패키지·파일 그룹별 bullet 나열
- [ ] 커밋: `docs: [레포] 모든 [파일범위]에 대해 [주석 유형] 추가`

### 팀원 작업 머지 (협업)

- [ ] 팀원 PR 리뷰어로 지정받으면 → 확인 후 jemu가 머지
- [ ] develop → main 통합: 섹션 템플릿, 리뷰어 없음, 셀프 머지
