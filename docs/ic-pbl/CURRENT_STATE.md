# CURRENT_STATE — EDK (ic-pbl)

> Last Update: 2026-05-29
> 원본 레포: [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl)
> 현재 통합 PR: [#16 develop → main](https://github.com/yj2trigger/pmg-ic-pbl/pull/16)

---

## 현재 단계

**EDK 도메인 전환, PyQt6 GUI 전환, 테스트 재작성, 패키징, 관리자 비밀번호 해시 완료.**

`develop` 브랜치는 `main` 최신 커밋을 병합해 뒤처짐 0 상태이며, PR #16은 열려 있으나 **CI 실패로 blocked** 상태다.

---

## Current Active Unit

PR #16 — gemini-review.yml 워크플로 수정 후 re-run.

---

## 구현 완료 요약

| 영역 | 상태 | 비고 |
|------|------|------|
| Medicine/Symptom 도메인 | 완료 | `product.py` 제거, `medicine.py`/`symptom.py` 추가 |
| DataManager 전환 | 완료 | `medicines.json`, `symptoms.json` 로드/저장 |
| DrugController | 완료 | 증상별 의약품 조회, 판매 가능 필터링 |
| CLI | 완료 | 증상 선택 → 의약품 상세 → 장바구니 → 결제 |
| PyQt6 GUI | 완료 | 증상 선택, 의약품 목록/상세, 응급 안내, 관리자 화면 |
| 테스트 | 완료 | Coffee/Gummy 테스트를 EDK 기준으로 재작성 |
| 패키징/문서 | 완료 | `project/pyproject.toml`, `project/README.md` |
| 관리자 보안 | 완료 | scrypt 해시, 레거시 평문 자동 마이그레이션 |
| 가격 정책 | 완료 | 의약품/옵션 가격 1000원 단위 정규화 |
| 통계 테스트 잔여 전환 | 완료 | `stats.py`와 `test_stats.py`를 Medicine 기준으로 수정 |

---

## 마지막 검증

- 레포: `yj2trigger/pmg-ic-pbl`
- 브랜치: `develop`
- 커밋: `6fc283c` (head)
- 실행 위치: `project/`
- 명령: `python -m pytest`
- 결과: `198 passed, 6 subtests passed` (2026-05-27 기준)

---

## PR #16 현재 상태

| 항목 | 값 |
|------|-----|
| state | open |
| mergeable_state | **blocked** |
| head commit | `6fc283c` |
| behind main | 0 |
| check: review | ❌ failure (2026-05-27T21:41:22Z) |

**block 원인:** `.github/workflows/gemini-review.yml` — `review` check 실패.

### 실패 원인 분석

`GEMINI_API_KEY`는 기존에 정상 동작한 기록 있음 → API 키 문제 아님.

**근본 원인: Linux `ARG_MAX` 초과.**

워크플로 문제 코드:
```bash
DIFF=$(cat diff.txt)
PROMPT="...${DIFF}"
PAYLOAD=$(jq -n --arg text "$PROMPT" ...)  # ← 여기서 실패
```

`--arg text "$PROMPT"` 는 diff 전체를 shell argument로 전달한다.
Linux `ARG_MAX` 한계는 약 2MB인데, PR #16은 +2107/-3838 lines, 56 files — 이 크기면 초과 가능.
`jq` 가 `Argument list too long` 오류로 exit 1 → check failure.

**수정 방법:** `jq --rawfile`로 파일 직접 읽기 (ARG_MAX 우회):
```bash
# 변경 전
PAYLOAD=$(jq -n --arg text "$PROMPT" '{"contents":[{"parts":[{"text":$text}]}],...}')

# 변경 후
printf '%s\n\nDiff:\n' "You are a senior code reviewer. ..." > prompt.txt
cat diff.txt >> prompt.txt
PAYLOAD=$(jq -n --rawfile text prompt.txt '{"contents":[{"parts":[{"text":$text}]}],...}')
```

---

## 알려진 상태

- PR #16은 열려 있고 코드 자체는 머지 가능하나, gemini-review check 실패로 `mergeable_state: blocked`.
- `pmg-ic-pbl/docs/`는 관리 레포 문서로 이전되어 삭제 유지가 맞다.

---

## 다음 권장 작업

1. `pmg-ic-pbl/.github/workflows/gemini-review.yml` — `--arg text "$PROMPT"` → `--rawfile text prompt.txt` 방식으로 수정.
2. `develop` 브랜치에 커밋 → PR #16 자동 re-run.
3. check 통과 후 `main`으로 머지.
4. 머지 후 이 문서와 `tasks/done.md`에 PR #16 머지 완료 반영.
