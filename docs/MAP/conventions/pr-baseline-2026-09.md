# MAP PR 관행 측정 — 2026-09 기준선

> 측정일 2026-09-07. [`stacked-pr-playbook.md`](./stacked-pr-playbook.md) 도입 직전 상태.
> 목적: 6개월 뒤 같은 방법으로 재측정해 개선 여부를 판단한다. 재현 스크립트는 부록.
> 측정 대상: we-meet-trip 6개 레포 전체 원격 히스토리 (2026-04-05 ~ 2026-09-06, 커밋 931개, PR 머지 커밋 75개).

---

## 1. PR 크기

| 지표 | 값 |
|------|-----|
| PR당 추가 줄 — 중앙값 | 754 |
| PR당 추가 줄 — 평균 | 1,648 |
| PR당 추가 줄 — 최대 | 11,319 (admin #1) |
| PR당 파일 수 — 중앙값 | 11 |
| PR당 커밋 수 — 중앙값 | 4 |
| 2,000줄 초과 PR | 22 / 75 |
| 100줄 이하 PR | 24 / 75 (32%) |

크기 분포가 양극단이다. 50줄 미만 14개, 2,000줄 초과 22개, 중간대가 얇다. 한 줄짜리 오타 수정 아니면 기능 통째로 둘 중 하나.

## 2. 외부 비교 (같은 방법, 봇·버전범프 제외, 최근 커밋 기준)

| 레포 | 추가 줄 중앙값 | 90분위 | 파일 중앙값 | 100줄 이하 비율 |
|------|---------------|--------|------------|----------------|
| caddyserver/caddy | 30 | 233 | 2 | 76% |
| pallets/flask | 9 | 138 | 2 | 88% |
| felangel/bloc | 9 | 518 | 2 | 79% |
| spring-projects/spring-boot | 1 | 137 | 1 | 88% |
| **we-meet-trip/MAP** | **754** | ~7,300 | 11 | 32% |

참고 문헌 수치: Google 내부 코드 리뷰 수정 라인 중앙값 24줄, GitHub 전체 PR 중앙값 20줄, Google 가이드 "100줄이 적당, 1,000줄은 보통 너무 큼".

## 3. 시간

| 지표 | 값 |
|------|-----|
| 브랜치 수명 (첫 커밋→마지막 커밋) 중앙값 | 4.5시간 |
| 마지막 커밋 → 머지 중앙값 | 9.8시간 |
| 마지막 커밋 → 머지 최대 | 652시간 (27일, client #72) |

작업 자체는 짧게 끝내는데 머지가 밀린다. 머지가 **배치로 몰린다**: 7/29 02:12–03:41에 6개 레포 9개 PR, 7/31 18:15–19:10에 8개, 8/7 10:16–11:12에 7개, 6/24 05:45–09:44에 7개.

## 4. 리뷰

- 셀프머지(작성자 == 머저, 단독 작성): **51 / 75 (68%)**
- CI가 `on: push: branches: ["**"]`라 브랜치 push 시점에 이미 검증이 끝난다. PR은 실질적으로 통보 절차.

## 5. 테스트

| 구분 | 테스트 파일 포함 PR |
|------|-------------------|
| 서버(user/hub/agent/infra/admin) | 21 / 26 (80%) |
| client | 6 / 39 (15%) |

서버 80%는 caddy(42%), flask(33%)보다 높다. **유지해야 할 강점.**

## 6. PR 없이 develop 직접 push

| 레포 | PR 머지 : 직접 커밋 |
|------|-------------------|
| infra | 8 : 23 |
| user | 8 : 22 |
| hub | 8 : 15 |
| agent | 5 : 10 |
| admin | 2 : 4 |
| client | 36 : 14 |

직접 push되는 내용: CI 워크플로 수정, `.env`/compose/Dockerfile, 배포 직후 핫픽스, 문서. 의도적 관행으로 판단해 플레이북에서도 유지.

## 7. 코드 상태

- 머지된 PR에 남아 있는 마커: `TODO` 45, `UnimplementedError` 16, `debugPrint` 22, `print(` 5
- 마커가 하나도 없는 PR은 48/75
- 즉 **"TODO 제거"는 PR 조건이 아니었다.** 정리 PR을 따로 여는 습관이 없다 → 플래그 도입 시 플래그 제거 PR도 같은 식으로 빠질 위험이 있음

## 8. 레이어 구성 (플레이북 분할 규칙의 근거)

서버 PR 중 **레이어 하나만 들어 있는 PR은 0개**. user 레포 기능 PR은 예외 없이 controller/service/repository/entity/dto/config/test가 한 덩어리로 들어온다. 이것이 크기를 키운 직접 원인이며, 플레이북 3장의 ①~④ 분할이 겨냥하는 지점.

브랜치 명명은 레포별로 갈린다. client는 이슈번호형(`feat/#45-chat-room`), 서버는 기능명형(`feat/weather-replan-trigger`). 통일 여부는 미결.

## 9. 개인 기록 (yj2trigger)

커밋 55개, 작성 PR 6개(client #76·#77, hub #14, user #30·#32, client #80). 그중 5개가 테스트 포함으로 팀 평균보다 높다. 커밋 시간대는 오전 36%로 팀에서 가장 낮 시간대에 몰려 있다. 팀 전체는 0~5시가 36%.

---

## 부록 — 재측정 방법

```bash
# 1) 전 레포 클론
for r in map-service-user map-service-client map-service-hub \
         map-service-agent map-service-infra map-service-admin; do
  git clone https://github.com/we-meet-trip/$r.git full-$r
done

# 2) PR 머지 커밋과 그 diff 규모
for r in full-*; do
  git -C $r log --all --merges --format='%H %P %s' | grep 'Merge pull request' |
  while read h base head rest; do
    n=$(git -C $r diff --numstat $base...$head | awk '{a+=$1} END {print a}')
    f=$(git -C $r diff --name-only $base...$head | wc -l)
    echo -e "$r\t$rest\t$f파일\t+$n"
  done
done

# 3) 직접 push 비율
for r in full-*; do
  git -C $r log --first-parent origin/develop --format='%s' |
  awk '{if ($0 ~ /^Merge pull request/) m++; else if ($0 !~ /^Merge/) d++}
       END {print FILENAME, "PR:"m, "직접:"d}'
done

# 4) 셀프머지: 머지 커밋 author 와 브랜치 커밋 author 비교
# 5) 시간대: git log --all --format='%aI' 의 시각 히스토그램
```

PR 생성 시각·리뷰 코멘트 수는 git 히스토리에 없다. GitHub 토큰이 있으면 `/repos/{o}/{r}/pulls?state=all`로 생성→머지 실제 간격과 리뷰 수를 추가로 잴 수 있다. 이번 측정에서는 익명 API 레이트리밋으로 미측정.
