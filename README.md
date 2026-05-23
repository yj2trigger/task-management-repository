# 📦 Task Management Repository (Meta-Repo)

> Claude와 연동하여 여러 프로젝트를 AI로 관리하는 메타-리포지토리입니다.

---

## 🚀 AI가 이 레포를 처음 읽는다면

**`AI_HANDOVER.md`를 먼저 읽으세요.** 현재 진행 중인 작업, 다음 할 일, 설계 결정 사항이 모두 정리되어 있습니다.

---

## 📁 구조

```
task-management-repository/
├── README.md                        ← 이 파일
├── AI_HANDOVER.md                   ← AI 인계 문서 (필독)
├── COLLABORATION_RULES.md           ← AI 협업 규칙
├── .gitmodules
│
├── projects/                        ← Git Submodule (코드만)
│   ├── ic-pbl/                      → yj2trigger/pmg-ic-pbl
│   └── ESG/                         → yj2trigger/ESG
│
├── docs/                            ← 모든 프로젝트 문서 통합 관리
│   ├── ic-pbl/
│   │   ├── CURRENT_STATE.md         ← 진행 상태 (single source of truth)
│   │   ├── requirements.md
│   │   ├── scope.md
│   │   ├── architecture.md
│   │   ├── gui_architecture.md
│   │   ├── system_flow.md
│   │   ├── terminology.md
│   │   └── test_strategy.md
│   └── ESG/
│       └── CURRENT_STATE.md         ← 진행 상태 (single source of truth)
│
└── tasks/                           ← 전체 태스크 트래킹
    ├── backlog.md
    ├── in-progress.md
    └── done.md
```

---

## 🔗 등록된 프로젝트

| 프로젝트 | 레포지토리 | 현재 상태 |
|---------|-----------|---------|
| ic-pbl (EDK) | [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl) | 🔵 EDK-01 진행 중 (medicine.py 리팩터링) |
| ESG | [yj2trigger/ESG](https://github.com/yj2trigger/ESG) | 🔵 구현 2단계 승인 대기 (성별 선택) |

---

## 📌 운영 원칙

- **모든 문서는 `docs/`에서만 관리** — 하위 레포의 docs는 업데이트하지 않음
- **코드 변경은 하위 레포에서, 문서/태스크는 여기서**
- **단계가 끝날 때마다 `CURRENT_STATE.md`와 `tasks/`를 업데이트**

---

## 🤖 협업 방식 요약

```
새 대화 시작 시:
1. AI_HANDOVER.md 읽기
2. docs/<프로젝트>/CURRENT_STATE.md 읽기
3. tasks/in-progress.md 읽기
4. COLLABORATION_RULES.md 따르기
```

상세 규칙은 `COLLABORATION_RULES.md` 참고.
