# 데일리 루틴 프롬프트

> 작성일: 2026-05-23
> 용도: 매일 아침 Claude Desktop에서 대화 시작 시 붙여넣기

---

## 사용 방법

1. Claude Desktop 실행
2. 새 대화 시작
3. 아래 프롬프트 전체를 복사해서 붙여넣기

---

## 프롬프트

```
오늘의 데일리 루틴을 시작합니다.

다음 순서로 진행하세요.

## 1. 문서 읽기 (자동)

아래 레포지토리들을 읽으세요.

**관리 레포 (읽기 + 쓰기 가능)**
- yj2trigger/task-management-repository
  - COLLABORATION_RULES.md
  - AI_HANDOVER.md
  - tasks/in-progress.md
  - tasks/backlog.md
  - tasks/done.md
  - docs/ic-pbl/CURRENT_STATE.md
  - docs/ESG/CURRENT_STATE.md

**프로젝트 레포 (읽기 + 쓰기 가능)**
- yj2trigger/pmg-ic-pbl : 최근 커밋 확인
- yj2trigger/ESG : 최근 커밋 확인

**팀 레포 (읽기 전용 — 절대 쓰기 금지)**
- we-meet-trip/map-service-user : open PR 목록
- we-meet-trip/map-service-hub : open PR 목록
- we-meet-trip/map-service-agent : open PR 목록
- we-meet-trip/map-service-client : open PR 목록
- we-meet-trip/map-service-infra : open PR 목록

## 2. 현황 요약 보고

읽은 내용을 바탕으로 아래 형식으로 보고하세요.

---

### 📋 전체 현황 요약 (YYYY-MM-DD)

#### [ic-pbl]
- 현재 단계:
- 진행 중인 작업:
- 블로커:

#### [ESG]
- 현재 단계:
- 진행 중인 작업:
- 블로커:

#### [MAP — 팀 프로젝트]
- 리뷰 대기 중인 PR: (yj2trigger가 리뷰어로 지정된 것만)
- 기타 확인 사항:

---

### 🎯 오늘의 할 일 제안

우선순위 기준:
1. 블로커가 있는 항목 먼저
2. in-progress 항목 완료 우선
3. 팀 PR 리뷰 (리뷰어로 지정된 것)
4. backlog 항목 순서대로

| 우선순위 | 프로젝트 | 작업 | 예상 소요 | 근거 |
|---------|---------|------|---------|------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| ... | | | | |

---

### ⚠️ 놓치면 안 되는 사항

오늘 반드시 확인해야 할 사항이 있으면 여기에 기술하세요.
(예: 오래된 미머지 PR, 오랫동안 진행 없는 작업 등)

---

## 3. 대기

보고 후 제 지시를 기다리세요.
작업을 시작하기 전 COLLABORATION_RULES.md의 규칙을 따르세요.
```

---

## 참고사항

- 매일 아침 실행을 권장합니다
- 보고 내용이 실제와 다르면 직접 수정 후 알려주세요
- 루틴 실행 후 특정 작업을 바로 이어서 진행할 수 있습니다
