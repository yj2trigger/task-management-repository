#  Task Management Repository (Meta-Repo)

> Claude와 연동하여 여러 프로젝트를 AI로 관리하는 메타-리포지토리입니다.

---

##  AI가 이 레포를 처음 읽는다면

**`AI_HANDOVER.md`를 먼저 읽으세요.** 현재 진행 중인 작업, 다음 할 일, 설계 결정 사항이 모두 정리되어 있습니다.

---

## 📁 구조

```
task-management-repository/
├── README.md                        ← 이 파일 (인덱스)
├── AI_HANDOVER.md                   ← AI 인계 문서 (필독) · 운영 원칙 SSOT
├── COLLABORATION_RULES.md           ← AI 협업 규칙
├── .gitmodules
│
├── projects/                        ← Git Submodule (코드만)
│   ├── ic-pbl/                      → yj2trigger/pmg-ic-pbl
│   └── ESG/                         → yj2trigger/ESG
│
├── docs/                            ← 모든 프로젝트 문서 통합 관리 (가변)
│   ├── CLAUDE_PLUGINS.md            ← Claude Code 플러그인/스킬(user scope) SSOT
│   ├── ic-pbl/
│   │   ├── CURRENT_STATE.md         ← 진행 상태 · 재활용 확정 유닛 SSOT
│   │   ├── requirements.md          ← 클래스/모듈 재활용 전략 SSOT (§ 2.4)
│   │   ├── scope.md                 ← 데이터 파일 구성 SSOT (§ 7)
│   │   ├── architecture.md          ← 목표 파일 구조 SSOT (§ 2)
│   │   ├── gui_architecture.md      ← 구 계획서 (역사적 참고용)
│   │   ├── system_flow.md
│   │   ├── terminology.md
│   │   └── test_strategy.md
│   ├── ESG/
│   │   ├── CURRENT_STATE.md         ← 진행 상태 · 이슈 이력 SSOT
│   │   └── full_plan.md
│   └── MAP/
│       ├── VPS_AR_SPEC.md           ← VPS·AR 앵커 기능 스펙 SSOT (MAP 전체)
│       ├── visitor_log/
│       │   └── ENVIRONMENT_SETUP.md ← Python 3.12 가상환경 설정 (open3d spike)
│       └── map-service-user/
│           ├── CURRENT_STATE.md     ← 진행 상태 · 보안 수정 SSOT
│           ├── API_DOCS_STANDARDS.md
│           ├── DEMO_SCRIPT.md
│           ├── ENVIRONMENT_SETUP.md
│           ├── security-review-2026-05-28.md
│           └── conventions/         ← jemu 분석·워크플로우
│
├── portfolio/                       ← 완료 프로젝트 회고 (불변)
│   └── ESG/
│       ├── README.md
│       ├── architecture.md          ← API · 파일 구조 · 배포 SSOT
│       ├── problem_statement.md
│       ├── security.md
│       ├── decisions/               ← ADR-001~006
│       └── postmortems/             ← 사고 상세 분석
│
└── tasks/                           ← 전체 태스크 트래킹
    ├── backlog.md                   ← 태스크 목록 SSOT
    ├── in-progress.md
    └── done.md
```

---

##  등록된 프로젝트

| 프로젝트 | 레포지토리 | 현재 상태 |
|---------|-----------|---------|
| ic-pbl (EDK) | [yj2trigger/pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl) | 🔵 EDK 전체 구현 완료, PR #16 main 머지 대기 |
| ESG | [yj2trigger/ESG](https://github.com/yj2trigger/ESG) | 🟢 핵심 기능 완료 + 운영 중 |
| MAP (map-service-user) | [we-meet-trip/map-service-user](https://github.com/we-meet-trip/map-service-user) | 🔵 인증 도메인 완료 |
| MAP (visitor_log) | 로컬 `c:\onedrive\_대학교\MAP\git\visitor_log` | 🟡 VPS·AR 씬 서비스 — spike 단계 |

---

##  운영 원칙

→ [AI_HANDOVER.md § 운영 원칙](./AI_HANDOVER.md) 참고

---

##  협업 방식 요약

```
새 대화 시작 시:
1. AI_HANDOVER.md 읽기
2. docs/<프로젝트>/CURRENT_STATE.md 읽기
3. tasks/in-progress.md 읽기
4. COLLABORATION_RULES.md 따르기
```

상세 규칙은 `COLLABORATION_RULES.md` 참고.
