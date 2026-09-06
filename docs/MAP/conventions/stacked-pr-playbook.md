# 단계별 PR(스택 PR) 플레이북 — MAP 전체

> **SSOT**: MAP 6개 레포의 PR 분할·플래그 운용 기준 단일 진실 공급원.
> 적용 범위: we-meet-trip 조직의 map-service-user / -client / -hub / -agent / -infra / -admin 전부.
> 빠른 참조 → [`stacked-pr-cheatsheet.md`](./stacked-pr-cheatsheet.md)
> 도입 근거 데이터 → [`pr-baseline-2026-09.md`](./pr-baseline-2026-09.md)
> 개인(jemu) 커밋·이슈 컨벤션과는 별개 문서. 그쪽은 [`../map-service-user/conventions/jemu-workflow.md`](../map-service-user/conventions/jemu-workflow.md).

---

## 0. 이 문서를 처음 읽는 사람/AI를 위한 전제

이 전제가 틀렸다면 아래 규칙 전체를 다시 검토해야 한다.

| 항목 | 사실 |
|------|------|
| 조직 | GitHub org `we-meet-trip`, 서비스명 MAP (위치 기반 여행 계획) |
| 레포 | user(Spring Boot/Java/Gradle), client(Flutter), hub(Python/FastAPI), agent(Python), infra(Docker Compose/스크립트), admin(Python) |
| 기본 브랜치 | 6개 전부 `develop` |
| CI | 6개 전부 `.github/workflows/ci.yml`, 트리거가 `on: push: branches: ["**"]` + `pull_request` |
| CI 내용 | user `./gradlew clean test` / hub·agent `python -c "import app.main"` → `pytest -q` → `docker build` / admin `pytest -q` / client `flutter test` → `flutter analyze` / infra `unittest` + `compose-isolation-check.sh` |
| 배포 환경 | test(GitHub environment `gcp-test`, `docker-compose.test.yml`) / prod(`docker-compose.yml`, client는 `v*` 태그 빌드) |
| DB 마이그레이션 | user 레포 Flyway, `src/main/resources/db/migration/V0NN__*.sql` |

**중요**: CI가 `branches: ["**"]`이므로 **CI는 PR을 열어야 도는 게 아니라 브랜치를 push하면 이미 돈다.** 따라서 PR은 "검증을 시작하는 행위"가 아니라 "이미 초록인 것을 합류시키는 행위"다. 이 문서의 규칙은 전부 이 사실 위에 세워져 있다.

---

## 1. 왜 바꾸는가

기존 기준은 **"호출자까지 배선돼 실제로 도달 가능해지면 PR"** 이었다. 이 조건을 걸면 스키마·리포지토리·서비스·컨트롤러·화면이 한 PR에 전부 들어갈 수밖에 없다.

측정 결과(상세는 baseline 문서):

| | MAP | caddy | flask | bloc | spring-boot |
|---|---|---|---|---|---|
| PR당 추가 줄 중앙값 | **754** | 30 | 9 | 9 | 1 |
| 90분위 | ~7,300 | 233 | 138 | 518 | 137 |
| 파일 수 중앙값 | 11 | 2 | 2 | 2 | 1 |

우리 중앙값이 저쪽 90분위의 3~5배다. Google 가이드는 100줄이 적당, 1,000줄은 보통 너무 크다고 본다.

**해결 방향**: "머지"와 "사용자 노출"을 분리한다. 머지 조건을 *도달 가능*이 아니라 *기존 동작을 안 깨뜨림*으로 바꾸고, 노출은 설정 플래그로 따로 켠다.

---

## 2. 판정 규칙

### 2.1 PR을 여는 조건 (전부 참일 때)

1. **머지해도 기존 동작이 안 바뀐다.** 새 코드가 아무도 안 부르거나, 부르더라도 플래그가 기본 off라 분기를 안 탄다. 마지막 단계(플래그 on)만 예외.
2. **브랜치 push 후 CI가 초록이다.** PR 열기 전에 Actions 결과를 확인한다.
3. **서버 코드면 테스트 파일이 같은 브랜치에 있다.** (user/hub/agent/admin) client는 생략 가능.
4. **develop과 충돌이 없다.** 충돌 나면 `merge: develop을 받는다` 커밋 하나 찍고 PR.

### 2.2 PR을 열지 않고 develop 직접 push 해도 되는 것

CI 설정, `.env`/compose/Dockerfile 조정, 배포 직후 핫픽스, 문서. infra 레포는 사실상 전부 여기 해당한다. (현행 관행이며 유지한다.)

### 2.3 크기 상한

**한 PR당 추가 400줄 / 10파일.** 넘으면 아래 3장대로 스택으로 쪼갠다. 예외는 자동 생성 파일과 대량 이동/이름 변경뿐이며, PR 본문에 이유를 적는다.

---

## 3. 분할 규칙

### 3.1 서버(user/admin — Spring, hub/agent — Python)

아래 순서로 아래에서 위로 쌓는다. 각 단계가 독립 PR이고, 각 단계는 그 아래 단계까지만 알면 컴파일·테스트가 된다.

```
① 스키마      Flyway V0NN__*.sql, Entity, Repository, 조회용 dto
② 순수 로직    Rule/Policy 클래스 + 단위 테스트, 값 객체 dto
③ 서비스      Service, 외부 클라이언트, 스케줄러/워처  (플래그 기본 off)
④ 배선        Controller, 라우터 등록, 예외 핸들러, 플래그 on
```

①②는 호출자가 없다. 단위 테스트만 그 코드를 부른다. ③은 빈/객체는 존재하지만 플래그가 off라 안 돈다. ④에서 처음으로 동작이 바뀐다.

### 3.2 client(Flutter)

```
① 모델        model/dto, 직렬화
② API 계층     api/service 클라이언트 + 목 테스트
③ 상태         provider/notifier
④ 화면         screen/widget, 라우트 등록
```

라우트를 등록하기 전까지는 화면 파일이 있어도 앱에서 도달 불가다. ④가 노출 단계.

### 3.3 레포 횡단 기능

`feat/transit-integrated-routing`처럼 client·hub·user 3곳에 같은 이름 브랜치를 파는 기능은 **레포별로 각각 스택을 만들고, 서버 → 클라 순으로 머지**한다. 클라가 먼저 머지되면 아직 없는 API를 부르게 된다.

---

## 4. 플래그

### 4.1 원리

if문의 조건을 코드 밖(설정/환경변수)으로 빼서, 재배포 없이 동작을 바꾸고 준비 안 된 코드를 꺼둔 채 배포하는 장치.

### 4.2 기본값 규칙 — 이게 핵심

| 용도 | 기본값 | 예시 |
|------|--------|------|
| **운영 스위치** (완성된 기능을 상황 따라 끔) | **true** | `weather-watch.enabled: ${WEATHER_WATCH_ENABLED:true}` |
| **미완성 머지용** (이 플레이북에서 쓰는 것) | **false** | `training.capture.enabled: ${TRAINING_CAPTURE_ENABLED:false}` |

두 사례 모두 user 레포 `application.yml`에 이미 존재한다. 스택 ③단계에서 다는 플래그는 **반드시 기본 false**여야 한다. 기본 true로 달면 머지 즉시 prod에서 돌아버려서 스택을 쪼갠 의미가 사라진다.

### 4.3 레포별 구현

**user / admin (Spring)** — 추가 의존성 0

```java
@Component
@ConditionalOnProperty(
        prefix = "weather-replan", name = "enabled",
        havingValue = "true", matchIfMissing = false)   // ← 기본 꺼짐
public class ScheduleWeatherWatcher { ... }
```

```yaml
weather-replan:
  enabled: ${WEATHER_REPLAN_ENABLED:false}
```

`@ConditionalOnProperty`가 off면 **빈 자체가 생성되지 않는다.** `@Scheduled`도 안 걸리고 DB 조회도 안 나간다. 기존 동작 교체형이면 빈은 만들되 서비스 안에서 `if (props.isEnabled())`로 분기해 옛 경로를 남긴다.

**hub / agent (Python)** — settings에 필드 추가 후 라우터를 조건부 등록

```python
if settings.transit_v2_enabled:
    app.include_router(transit_v2.router)
```

**infra** — `.env` 템플릿에 키 추가. test/prod 값을 따로 관리한다.

**client (Flutter)** — `--dart-define`은 빌드 시점에 고정되어 앱 재배포가 필요하므로 쓰지 않는다. 서버가 내려주는 값으로 분기한다.

### 4.4 수명주기

```
1. 코드 머지, 모든 환경 off      → 배포해도 아무 일 없음
2. test 환경만 on               → gcp-test / docker-compose.test.yml 쪽 .env 에만 true
3. prod on                      → 운영 .env 에 true
4. 플래그와 옛 경로를 지우는 PR   ← 반드시 별도 PR로 수행
```

3번을 하는 날 4번 이슈를 같이 연다. 안 하면 죽은 분기가 쌓인다. (현재 머지된 PR에 TODO 45개, `UnimplementedError` 16개가 남아 있는 관행이 있으므로 특히 주의.)

### 4.5 플래그로 못 막는 것 — 마이그레이션

Flyway는 부팅 시 무조건 실행되므로 `V0NN__*.sql`은 플래그 뒤에 숨길 수 없다.

- ①단계 마이그레이션은 **추가만** 한다. 새 테이블, nullable 컬럼, 인덱스.
- `NOT NULL`, 컬럼 삭제, 타입 변경, 이름 변경은 금지. 기능이 완전히 켜지고 안정된 뒤 별도 PR로 뺀다.
- 이유: ①만 머지된 시점의 구버전 애플리케이션이 그 스키마에서 그대로 떠야 한다.

---

## 5. 실행 절차

### 5.1 브랜치와 PR 만들기 (도구 없이)

```bash
# ① 스키마
git checkout develop && git pull
git checkout -b feat/weather-schema
# ...작업, 커밋, push
git push -u origin feat/weather-schema
# Actions 초록 확인 후
gh pr create --base develop --title "feat(user): 날씨 재계획 스키마"

# ② 순수 로직 — ①을 base로
git checkout -b feat/weather-rule feat/weather-schema
git push -u origin feat/weather-rule
gh pr create --base feat/weather-schema --title "feat(user): 날씨 변화 판정 규칙"

# ③ 서비스 — ②를 base로
git checkout -b feat/weather-watcher feat/weather-rule
gh pr create --base feat/weather-rule --title "feat(user): 날씨 감시 워처 (플래그 off)"
```

PR #②의 diff에는 #①의 내용이 나타나지 않는다. 리뷰어는 해당 단계만 본다.

### 5.2 머지 순서

**반드시 아래부터.** ① 머지 → GitHub이 ②의 base를 자동으로 `develop`으로 바꿔줌 → ② 머지 → ③ …

### 5.3 아래 PR이 수정되면 (연쇄 리베이스)

```bash
git checkout feat/weather-rule
git rebase feat/weather-schema
git push --force-with-lease
git checkout feat/weather-watcher
git rebase feat/weather-rule
git push --force-with-lease
```

`--force-with-lease`를 쓴다(`--force` 금지). 이 연쇄 작업이 귀찮아지는 시점이 도구 도입 시점이다.

---

## 6. 도구

| 도구 | 언제 |
|------|------|
| `gh pr create --base` | **지금 이걸로 시작한다.** 3단 정도까지 충분 |
| Graphite (`gt`) | 스택이 4단 이상, 연쇄 리베이스가 잦아질 때. `gt submit`으로 스택 전체 푸시·base 재지정. 소규모 팀 무료 티어 |
| ghstack | 로컬 커밋 1개 = PR 1개 매핑. PyTorch가 사용 |
| git-spr (ejoffe/spr) | 위와 같은 개념의 Go 구현 |
| Sapling / jj (Jujutsu) | VCS를 갈아엎는 쪽. 팀 전체 학습 비용 때문에 현 규모에는 과함 |
| Gerrit | Google식 CL 체인. 별도 서버 운영 필요, 현 규모에 부적합 |

플래그 관리 도구(Unleash 셀프호스트, Flagsmith, LaunchDarkly)는 플래그가 10개를 넘고 런타임 토글이 필요해질 때 검토한다. 그전까지는 `application.yml` + `.env`로 충분하다.

---

## 7. 적용 예시 — user PR #32 재분할

실제 머지된 `feat/weather-replan-trigger` (34파일, +2,161줄)을 이 규칙으로 쪼개면:

| 단계 | 브랜치 | 파일 | 대략 |
|------|--------|------|------|
| ① | `feat/weather-schema` | `db/migration/V0NN__weather_replan.sql`, `ScheduleEntity`, `ScheduleRepository`, `ScheduleSummary`, `ScheduleDetailResponse` | ~110줄 |
| ② | `feat/weather-rule` | `WeatherChangeRule` + `WeatherChangeRuleTest`, `WeatherAlert`, `WeatherSnapshotItem` | ~260줄 |
| ③ | `feat/weather-watcher` | `ScheduleWeatherService`, `ScheduleWeatherWatcher` + 각 테스트, `application.yml` 플래그(기본 false) | ~620줄 |
| ④ | `feat/weather-replan-wire` | `ScheduleController`, `TripController`, `ScheduleService`, `TripReplanRequest`, `GlobalExceptionHandler`, `ScheduleReplanSpec`, 플래그 on | ~400줄 |

④가 늦어져도 ①~③은 이미 develop에 있고, 배포 결과는 그대로다.

---

## 8. PR 체크리스트

- [ ] 추가 400줄 / 10파일 이하인가 (초과 시 본문에 이유)
- [ ] 이 PR만 머지해도 기존 동작이 그대로인가
- [ ] 새 플래그를 달았다면 기본값이 `false`인가
- [ ] 마이그레이션이 있다면 추가만 하는가 (NOT NULL·삭제·타입 변경 없음)
- [ ] 브랜치 push 후 CI가 초록인가
- [ ] 서버 레포면 테스트 파일이 포함됐는가
- [ ] base 브랜치가 맞는가 (스택이면 아래 단계, 아니면 develop)
- [ ] 플래그를 on 한 PR이라면 제거 이슈를 열었는가

---

## 9. 이 문서를 갱신해야 하는 때

- CI 트리거가 `branches: ["**"]`에서 바뀌었을 때 (0장 전제가 깨짐)
- 기본 브랜치가 `develop`이 아니게 됐을 때
- 스택 도구를 실제로 도입했을 때 (6장 갱신 + 5장 명령 교체)
- 6개월쯤 뒤 baseline 재측정 시 (측정 방법은 baseline 문서 부록에 스크립트로 남겨둠)
