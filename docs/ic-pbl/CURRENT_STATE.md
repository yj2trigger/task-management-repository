# CURRENT_STATE — EDK (ic-pbl)

> Last Update: 2026-05-29
> 원본 레포: [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl)
> 현재 통합 PR: [#16 develop → main](https://github.com/yj2trigger/pmg-ic-pbl/pull/16)

---

## 현재 단계

**EDK 도메인 전환, PyQt6 GUI 전환, 테스트 재작성, 패키징, 관리자 비밀번호 해시 완료.**

gemini-review.yml 수정 완료 (commit `ec72104`). PR #17 소규모 테스트로 워크플로 정상 동작 확인.
PR #16 re-run 대기 중.

---

## Current Active Unit

PR #16 check re-run 결과 확인 → 통과 시 main 머지.

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
| gemini-review.yml 수정 | 완료 | ARG_MAX 우회 + API key 보안 헤더 전환 |

---

## 마지막 검증

- 레포: `yj2trigger/pmg-ic-pbl`
- 브랜치: `develop`
- 커밋: `ec72104` (head — gemini-review.yml 수정)
- `python -m pytest` 결과: `198 passed, 6 subtests passed` (2026-05-27 기준)
- gemini-review 워크플로: PR #17 소규모 테스트에서 정상 동작 확인

---

## gemini-review.yml 장애 기록

### 증상
PR #16 `mergeable_state: blocked` — check `review` failure (exit 126, 2026-05-27)

### 근본 원인: Linux ARG_MAX 초과

```bash
# 문제 코드
DIFF=$(cat diff.txt)
PROMPT="...${DIFF}"
PAYLOAD=$(jq -n --arg text "$PROMPT" ...)
#                ^^^^^^^^^^^^^^^^^^^^ diff 전체를 shell argument로 전달
```

`jq --arg`는 값을 프로세스 argv로 전달한다. Linux `ARG_MAX` 한계 약 2MB.
PR #16 diff: +2107/-3838, 56 files → 초과 → `Argument list too long` (exit 126).

소규모 PR (PR #17, diff 1줄)은 문제없이 통과 → ARG_MAX 확인.

### 수정 내용 (commit `ec72104`)

```bash
# 수정 후 — 파일로 읽어 ARG_MAX 우회
printf 'You are a senior code reviewer...\n\nDiff:\n' > prompt.txt
cat diff.txt >> prompt.txt
jq -n --rawfile text prompt.txt '...' > payload.json
curl -s "https://...generateContent" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \  # API key URL 노출 → 헤더로 이동
  -d @payload.json                            # curl도 파일로 읽어 동일 문제 차단
```

---

## PR #16 현재 상태

| 항목 | 값 |
|------|-----|
| state | open |
| head commit | `ec72104` (gemini-review 수정 포함) |
| behind main | 0 |
| check: review | re-run 대기 중 |

---

## 다음 권장 작업

1. PR #16 gemini-review check 통과 확인.
2. 통과 시 `main`으로 머지.
3. PR #17 (`test/gemini-review` → `develop`) close.
4. 머지 후 이 문서와 `tasks/done.md`에 PR #16 머지 완료 반영.
