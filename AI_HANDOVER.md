# AI 인계 문서 (AI Handover Guide)

> 작성일: 2026-05-23
> 최종 갱신: 2026-05-27
> 목적: 이 문서를 읽은 AI가 현재 진행 중인 작업을 즉시 이어받을 수 있도록 합니다.

---

## 이 레포지토리의 역할

`task-management-repository`는 여러 프로젝트를 AI와 함께 관리하는 **메타-리포지토리**입니다.
코드는 각 하위 레포에 있고, 이 레포는 **문서, 태스크 트래킹, 협업 규칙**만 관리합니다.

---

## 운영 원칙

- **모든 문서는 `docs/`에서만 관리** — 하위 레포의 docs는 업데이트하지 않음
- **코드 변경은 하위 레포에서, 문서/태스크는 여기서**
- **단계가 끝날 때마다 `CURRENT_STATE.md`와 `tasks/`를 업데이트**

---

## 현재 관리 중인 프로젝트

| 프로젝트 | 레포 | 현재 상태 |
|---------|------|---------|
| ic-pbl (EDK) | [pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl) | EDK 전체 구현 완료, PR #16 main 머지 대기 |
| ESG | [ESG](https://github.com/yj2trigger/ESG) | 핵심 기능 완료 + 운영 중 |

---

## 반드시 먼저 읽어야 할 문서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | `COLLABORATION_RULES.md` | AI가 따라야 할 협업 규칙 |
| 2 | `docs/ic-pbl/CURRENT_STATE.md` | ic-pbl 현재 진행 상태 |
| 3 | `docs/ESG/CURRENT_STATE.md` | ESG 현재 진행 상태 |
| 4 | `tasks/in-progress.md` | 현재 진행 중인 태스크 |
| 5 | `tasks/backlog.md` | 대기 중인 태스크 |

---

## 협업 규칙 핵심 요약

작업 전 반드시 `COLLABORATION_RULES.md`를 읽고 따릅니다. 요약:

1. **모호한 점은 먼저 질문** — 추측으로 진행하지 않습니다
2. **작업 전 계획 설명 + 승인** — 무엇을 어떻게 할지 먼저 설명합니다
3. **작업 후 결과 정리 + 승인** — 완료 후 요약하고 다음 단계 승인을 받습니다
4. **기능 구현 시 테스트 동시 작성** — 코드 + 테스트가 함께 완료 기준입니다

---

## ic-pbl (EDK) 프로젝트 인계 정보

### 현재 상태: PR #16 main 머지 대기

`pmg-ic-pbl`의 `develop` 브랜치에 EDK 전체 구현이 올라가 있으며, `main` 대상 PR #16이 열려 있습니다.

**GitHub 상태:**
- PR: https://github.com/yj2trigger/pmg-ic-pbl/pull/16
- Head: `develop` commit `13857d4`
- Base: `main`
- 상태: `mergeable: true`, `develop` behind 0
- 로컬 검증: `project/`에서 `python -m pytest` → `198 passed, 6 subtests passed`

**포함된 작업:**
- `Medicine`, `Symptom`, `SymptomGroup` 도메인 전환
- `DrugController` 및 `DataManager` 의약품/증상 JSON 전환
- CLI 증상 선택 → 의약품 탐색 → 결제 흐름
- PyQt6 GUI 증상 선택, 의약품 목록/상세, 응급 안내, 관리자 화면
- EDK 기준 테스트 전면 재작성
- `project/pyproject.toml`, `project/README.md` 패키징/문서화
- 관리자 비밀번호 scrypt 해시 및 평문 자동 마이그레이션
- 가격 정책 1000원 단위 정규화
- `stats.py`와 `test_stats.py` Medicine 기준 수정

**다음 작업:**
1. PR #16 최종 확인
2. 이상 없으면 main으로 머지
3. 머지 후 `docs/ic-pbl/CURRENT_STATE.md`와 `tasks/done.md`에 PR #16 머지 완료 반영

**주의:**
- `pmg-ic-pbl/docs/`는 이 관리 레포로 이전되어 삭제 유지가 맞습니다.
- 프로젝트 문서 SSOT는 `task-management-repository/docs/ic-pbl/`입니다.

---

## ESG 프로젝트 인계 정보

### 현재 상태: 핵심 기능 완료 + 운영 중

상세 상태는 `docs/ESG/CURRENT_STATE.md`를 기준으로 확인합니다.

**향후 주요 작업:**
- IoT 실물 연동: Tuya WiFi 플러그 연결 + Device ID 확보
- DB Quota 관리: 자동 정리, 관리자 시스템 통계, 이메일 알림
- 운영 개선: 다중 서버 WebSocket 브로드캐스트 보완

---

## GitHub MCP 사용 방법

이 레포와 하위 프로젝트 레포는 GitHub MCP로 직접 파일을 읽고 쓸 수 있습니다.

```
owner: yj2trigger
repos:
  - task-management-repository  (이 레포)
  - pmg-ic-pbl                  (ic-pbl 코드)
  - ESG                         (ESG 코드)
```

**작업 흐름:**
1. `docs/<프로젝트>/CURRENT_STATE.md` 읽기 → 현재 상태 파악
2. 관련 설계 문서 읽기
3. 코드 작업 (해당 레포에 직접 커밋)
4. `CURRENT_STATE.md`, `tasks/` 업데이트
5. 사용자 승인 후 다음 단계

---

## 문서 구조

→ [README.md](./README.md) 참고
