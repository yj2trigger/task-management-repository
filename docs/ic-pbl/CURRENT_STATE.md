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

PR #16 — gemini-review check 실패 원인 파악 및 해결.

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

워크플로 동작:
1. `git diff base...head` → `diff.txt`
2. Gemini 2.5 Flash Lite API 호출 (`GEMINI_API_KEY` secret 필요)
3. 리뷰 결과를 PR 코멘트로 게시

가능한 실패 원인:
- `GEMINI_API_KEY` secret 미설정 또는 만료
- diff 크기 초과 (PR #16: +2107/-3838, 56 files — Gemini 요청 본문 너무 큼)

---

## 알려진 상태

- PR #16은 열려 있고 코드 자체는 머지 가능하나, gemini-review check 실패로 `mergeable_state: blocked`.
- `pmg-ic-pbl/docs/`는 관리 레포 문서로 이전되어 삭제 유지가 맞다.

---

## 다음 권장 작업

1. gemini-review 실패 원인 확인 (`GEMINI_API_KEY` secret 유효 여부, diff 크기 제한).
2. 필요 시 워크플로 수정 후 re-run, 또는 branch protection에서 해당 check를 required 해제.
3. check 통과 후 `main`으로 머지.
4. 머지 후 이 문서와 `tasks/done.md`에 PR #16 머지 완료를 반영.
