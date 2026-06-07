# CURRENT_STATE — 아이스크림 키오스크 (ic-pbl)

> Last Update: 2026-06-06
> 원본 레포: [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl)

---

## 현재 단계

**아이스크림 키오스크 도메인 전환 + 문서/주석/UI 정비 완료. main 최신.**

PR #18(도메인 전환)부터 PR #27(CI 개선)까지 머지 완료. 발표 준비(대본, TTS, 시연 영상, 코드 제출) 진행 단계.

---

## ⚠️ 도메인 전환 이력 (중요 — 구버전 문서 주의)

이전 `CURRENT_STATE.md` (Last Update: 2026-05-29)는 **의약품(EDK/Medicine) 도메인**을 "완료" 상태로 기술했으나, 같은 날 commit `7654c35` (refactor: 의약품 도메인 → 아이스크림 키오스크 전환, PR #18)로 **전면 전환**됨.

| 이전 (Medicine/EDK) | 현재 (IceCream) |
|---|---|
| `Medicine`, `SymptomGroup` | `IceCreamProduct`, `OptionGroup` |
| `medicines.json`, `symptoms.json` | `products.json`, `ingredients.json`, `options.json` |
| 증상 선택 → 의약품 상세 → 결제 | 메뉴 선택 → 커스터마이징 → 결제 |
| `DrugController` | `KioskController` |

`pyproject.toml`의 `description = "EDK — Erica Drug King: 아이스크림 커스터마이징 키오스크"` 문구는 이 전환의 흔적으로 아직 남아 있음 (불일치 — 정리 후보).

---

## 구현 완료 요약

| 영역 | 상태 | 비고 |
|------|------|------|
| 아이스크림 도메인 전환 | 완료 | PR #18 (`7654c35`, `cc30210`) |
| KioskController / Cart / Payment | 완료 | 즉시 재고 차감, 그리디 잔돈 계산 |
| PyQt6 GUI | 완료 | 메뉴, 커스터마이징, 장바구니, 결제, 영수증, 관리자 |
| 테스트 | 완료 | pytest 전체 통과 (CI `gemini-review.yml` 포함) |
| 파일 헤더 주석 | 완료 | 전 소스 25개 파일 + 인라인 WHY 주석 (`docstring_progress.md`) |
| UML/시퀀스 다이어그램 | 완료 | README에 클래스/시퀀스 다이어그램 코드 기준 동기화 |
| 버그 수정 | 진행 누적 | 수량 버튼 패딩, admin_toggle_product 앱 종료, 현금 잔돈 검증, mutable default arg 등 |
| 발표 준비 | 진행 중 | 대본 작성/검증, TTS 시간 측정, 시연 영상, 코드 제출 zip |

---

## 최근 주요 커밋 (2026-06-06 기준 main 최신)

| 커밋 | 내용 |
|---|---|
| `32c77f8` | fix: test_stats.py mutable default argument 수정 |
| `a98b865` | docs: can_complete()에 현금 투입 차단 불가 이유 주석 추가 |
| `86d31d4` | chore: 발표용 초기 데이터 설정 (재고 ~50개, 현금 ~10장) |
| `04c2a57` | fix: admin_toggle_product/set_price 호출 시 앱 종료 버그 수정 |
| `3953c57` | docs: 클래스 다이어그램 실제 코드 기준 전체 동기화 |
| `5892224` | docs: README 시퀀스 다이어그램 두 버전 병기 |
| `097d953` | Merge develop into main: 전체 기능 완성 + 파일 헤더 주석 + 수량 버튼 렌더링 수정 |
| `83c1865` | chore: 전체 소스 파일 헤더 주석 추가 + 수량 버튼 글리프 수정 |
| `5baf090` | fix(payment): ChangeReserve.add_cash() denomination/count 유효성 검증 추가 |

---

## Current Active Unit

**발표대본 작성 + TTS 시간 측정 + 코드 제출용 zip 패키징**
- `발표대본_초안.md` (23슬라이드, 시간 어노테이션 제거)
- `c:\tmp\presentation.mp3` (1.5배속 TTS)
- `c:\tmp\kiosk_submit.zip` (.py 전체, 폴더 구조 유지, 약 62KB — 가상환경/dist/__pycache__ 제외)

---

## gemini-review.yml 장애 기록 (과거 — 해결됨)

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

PR #17 검증 완료. 이후 도메인 전환·CI 개선 작업에서 안정 동작 확인.
