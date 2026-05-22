# 📦 Task Management Repository (Meta-Repo)

> Claude와 연동하여 여러 프로젝트를 한눈에 관리하는 메타-리포지토리입니다.

---

## 📁 구조

```
task-management-repository/
├── .gitmodules                  # Git Submodule 등록 파일
├── README.md                    # 이 파일
│
├── projects/                    # 하위 프로젝트 (Git Submodule)
│   └── ic-pbl/                  → yj2trigger/ic-pbl-----
│
├── status/                      # 프로젝트별 현재 상태 요약
│   └── ic-pbl.md
│
├── tasks/                       # 태스크 트래킹
│   ├── backlog.md
│   ├── in-progress.md
│   └── done.md
│
└── reports/                     # AI 생성 리포트
    └── .gitkeep
```

---

## 🔗 등록된 프로젝트

| 프로젝트 | 레포지토리 | 상태 |
|---------|-----------|------|
| ic-pbl | [yj2trigger/ic-pbl-----](https://github.com/yj2trigger/ic-pbl-----) | 🔵 GUI 개발 진행 중 |

---

## 🤖 Claude와의 협업 방식

1. **상태 파악**: `status/` 파일을 읽어 각 프로젝트의 진행 현황 파악
2. **태스크 관리**: `tasks/` 파일을 통해 할 일 추가/완료 처리
3. **리포트 생성**: 요청 시 `reports/`에 종합 리포트 자동 작성
4. **크로스-프로젝트 조율**: 여러 프로젝트에 걸친 이슈를 메타-리포에서 통합 관리
