# CURRENT_STATE — EDK (ic-pbl)

> Last Update: 2026-05-29
> 원본 레포: [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl)

---

## 현재 단계

**EDK 전체 구현 완료. PR #16 `develop → main` 머지 완료 (2026-05-29).**

`main` 브랜치에 EDK 전체 구현이 반영됨. 현재 진행 중인 작업 없음.

---

## Current Active Unit

없음.

---

## 구현 완료 요약

| 영역 | 상태 | 비고 |
|------|------|------|
| Medicine/Symptom 도메인 | 완료 | `product.py` 제거, `medicine.py`/`symptom.py` 추가 |
| DataManager 전환 | 완료 | `medicines.json`, `symptoms.json` 로드/저장 |
| DrugController | 완료 | 증상별 의약품 조회, 판매 가능 필터링 |
| CLI | 완료 | 증상 선택 → 의약품 상세 → 장바구니 → 결제 |
| PyQt6 GUI | 완료 | 증상 선택, 의약품 목록/상세, 응급 안내, 관리자 화면 |
| 테스트 | 완료 | 198 passed, 6 subtests passed |
| 패키징/문서 | 완료 | `project/pyproject.toml`, `project/README.md` |
| 관리자 보안 | 완료 | scrypt 해시, 레거시 평문 자동 마이그레이션 |
| 가격 정책 | 완료 | 의약품/옵션 가격 1000원 단위 정규화 |
| 통계 테스트 잔여 전환 | 완료 | `stats.py`/`test_stats.py` Medicine 기준 수정 |
| gemini-review.yml | 완료 | ARG_MAX 우회 + API key 헤더 전환 + maxOutputTokens 8192 |

---

## PR #16 머지 기록

| 항목 | 값 |
|------|-----|
| PR | [#16 develop → main](https://github.com/yj2trigger/pmg-ic-pbl/pull/16) |
| 머지 커밋 | `e4801d0` |
| 머지 일시 | 2026-05-29 |
| 포함 작업 | EDK 도메인, PyQt6 GUI, 테스트 재작성, 패키징, 관리자 비밀번호 해시, CI 수정 |

---

## gemini-review.yml 장애 기록

### 증상
PR #16 `mergeable_state: blocked` — check `review` failure (exit 126, 2026-05-27)

### 근본 원인: Linux ARG_MAX 초과

```bash
# 문제 코드
PAYLOAD=$(jq -n --arg text "$PROMPT" ...)  # diff 전체를 argv로 전달 → ARG_MAX 초과
```

`jq --arg`는 값을 프로세스 argv로 전달. PR #16 diff (+2107/-3838, 56 files) → `Argument list too long` (exit 126).

### 수정 (commit `ec72104`, `f6ab97d`)

- `--rawfile text prompt.txt` — 파일로 읽어 ARG_MAX 우회
- `-d @payload.json` — curl도 파일 읽기
- `x-goog-api-key` 헤더 — API key URL 노출 차단
- `maxOutputTokens` 2048 → 8192

PR #17 소규모 테스트로 수정 검증 완료.
