# 📦 Task Management Repository (Meta-Repo)

> Claude와 연동하여 여러 프로젝트를 한눈에 관리하는 메타-리포지토리입니다.

---

## 📁 구조

```
task-management-repository/
├── .gitmodules
├── README.md
│
├── projects/                        # Git Submodule (코드만)
│   ├── ic-pbl/                      → yj2trigger/pmg-ic-pbl
│   └── ESG/                         → yj2trigger/ESG
│
├── docs/                            # 📋 모든 프로젝트 문서 통합 관리
│   ├── ic-pbl/
│   │   ├── CURRENT_STATE.md         # 진행 상태 (single source of truth)
│   │   ├── requirements.md
│   │   ├── scope.md
│   │   ├── architecture.md
│   │   ├── gui_architecture.md
│   │   ├── system_flow.md
│   │   ├── terminology.md
│   │   └── test_strategy.md
│   └── ESG/
│       ├── CURRENT_STATE.md
│       └── full_plan.md
│
└── tasks/                           # 전체 태스크 트래킹
    ├── backlog.md
    ├── in-progress.md
    └── done.md
```

---

## 🔗 등록된 프로젝트

| 프로젝트 | 레포지토리 | 상태 |
|---------|-----------|------|
| ic-pbl (EDK) | [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl) | 🔵 EDK 도메인 전환 진행 중 |
| ESG | [yj2trigger/ESG](https://github.com/yj2trigger/ESG) | 🔵 CI/CD 자동화 단계 |

---

## 📌 운영 원칙

- **모든 문서는 `docs/` 에서만 관리합니다** — 하위 레포의 docs는 더 이상 업데이트하지 않음
- Claude는 항상 이 레포의 `docs/`를 읽고 씁니다
- 코드 변경은 하위 레포에서, 문서/태스크 관리는 여기서

---

## 🤖 Claude와의 협업 방식

1. **상태 파악**: `docs/<프로젝트>/CURRENT_STATE.md` 읽기
2. **태스크 관리**: `tasks/` 파일 업데이트
3. **문서 업데이트**: `docs/<프로젝트>/` 직접 수정
4. **리포트**: 요청 시 `reports/`에 종합 리포트 생성
