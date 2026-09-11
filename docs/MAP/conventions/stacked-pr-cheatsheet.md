# 단계별 PR 치트시트

> 빠른 참조용. 근거·예외·상세 → [`stacked-pr-playbook.md`](./stacked-pr-playbook.md)

---

## 한 줄 원칙

**머지 조건 = "도달 가능"이 아니라 "기존 동작을 안 깨뜨림".** 노출은 플래그로 따로 켠다.

---

## 분할 순서

```
서버(user/admin/hub/agent)
  ① 스키마   Flyway sql · Entity · Repository · 조회 dto
  ② 로직     Rule/Policy + 단위 테스트 · 값 dto
  ③ 서비스   Service · 클라이언트 · 워처   ← 플래그 기본 false
  ④ 배선     Controller · 라우터 · 예외핸들러 · 플래그 on

client(Flutter)
  ① 모델 → ② api/service → ③ provider → ④ screen/widget + 라우트 등록

레포 횡단 기능: 레포별로 각각 스택, 머지는 서버 → 클라 순
```

---

## 크기 상한

**추가 400줄 / 10파일.** 초과 시 스택 분할, 못 쪼개면 PR 본문에 이유.

---

## 명령

```bash
# 스택 쌓기
git checkout -b feat/b feat/a
git push -u origin feat/b
gh pr create --base feat/a

# 머지는 반드시 아래부터: feat/a → feat/b → feat/c
# a 머지되면 b의 base는 GitHub이 develop으로 자동 변경

# 아래 PR 수정 시 연쇄 리베이스
git checkout feat/b && git rebase feat/a && git push --force-with-lease
```

---

## 플래그

```java
// Spring — 기본 꺼짐. matchIfMissing=false 를 빠뜨리지 말 것
@ConditionalOnProperty(prefix="weather-replan", name="enabled",
        havingValue="true", matchIfMissing=false)
```
```yaml
weather-replan:
  enabled: ${WEATHER_REPLAN_ENABLED:false}
```
```python
# hub/agent
if settings.transit_v2_enabled:
    app.include_router(transit_v2.router)
```

**기본값 규칙**: 미완성 머지용 = `false` / 운영 스위치 = `true`
**client**: `--dart-define` 금지(빌드 시점 고정). 서버가 내려주는 값으로 분기.

**수명주기**: 머지(전부 off) → test만 on → prod on → **플래그 제거 PR**

---

## 마이그레이션

①단계 sql은 **추가만**. 새 테이블 / nullable 컬럼 / 인덱스.
`NOT NULL`, 컬럼 삭제, 타입·이름 변경은 기능 안정화 후 별도 PR.

---

## 직접 push 허용 (PR 불필요)

CI 설정 · `.env`/compose/Dockerfile · 배포 직후 핫픽스 · 문서. infra 레포 대부분.

---

## PR 열기 전 확인

```
[ ] 400줄/10파일 이하
[ ] 이것만 머지해도 동작 그대로
[ ] 새 플래그 기본값 false
[ ] 마이그레이션은 추가만
[ ] push 후 CI 초록  (CI는 branches:["**"] 라 PR 없이도 돎)
[ ] 서버면 테스트 포함
[ ] base 브랜치 확인
[ ] 플래그 on 했으면 제거 이슈 생성
```
