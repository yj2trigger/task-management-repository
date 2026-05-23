# AI 인계 문서 (AI Handover Guide)

> 작성일: 2026-05-23
> 목적: 이 문서를 읽은 AI가 현재 진행 중인 작업을 즉시 이어받을 수 있도록 합니다.

---

## 이 레포지토리의 역할

`task-management-repository`는 여러 프로젝트를 AI와 함께 관리하는 **메타-리포지토리**입니다.
코드는 각 하위 레포에 있고, 이 레포는 **문서, 태스크 트래킹, 협업 규칙**만 관리합니다.

---

## 현재 관리 중인 프로젝트

| 프로젝트 | 레포 | 현재 상태 |
|---------|------|---------|
| ic-pbl (EDK) | [pmg-ic-pbl](https://github.com/yj2trigger/pmg-ic-pbl) | EDK-01 진행 중 (medicine.py 리팩터링) |
| ESG | [ESG](https://github.com/yj2trigger/ESG) | 구현 1단계 완료, 2단계(성별 선택) 승인 대기 |

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

## ESG 프로젝트 인계 정보

### 다음에 할 작업: 구현 2단계 — 성별 선택 (프론트엔드 only)

**작업 내용:**
- `project/frontend/src/types/user.ts` — Gender 타입 정의
- `project/frontend/src/store/authStore.ts` — Zustand + localStorage
- `project/frontend/src/pages/GenderSelectPage.tsx` — 남/여 선택 UI
- `project/frontend/src/App.tsx` 수정 — 라우팅 연결
- `project/frontend/src/__tests__/authStore.test.ts` — store 단위 테스트

**설계 결정 사항 (변경 불가):**
- 인증 없음 — gender를 localStorage에 저장
- 백엔드 API 요청 시 쿼리 파라미터(`?gender=male`)로 전달
- 프로토타입이므로 로그인/회원가입 구현하지 않음

**파일 위치:** `ESG 레포 > project/frontend/`

**전체 구현 순서:**

| 순서 | 기능 | 백엔드 | 프론트엔드 |
|------|------|--------|-----------|
| 1 | 프로젝트 골격 + Docker | ✅ | ✅ |
| 2 | 성별 선택 | — | ⏳ 다음 작업 |
| 3 | 세탁기 상태 조회 (Mode A/B/C) | ⏳ | ⏳ |
| 4 | Mode B — 소프트 예약 | ⏳ | ⏳ |
| 5 | Mode C — 대기열 | ⏳ | ⏳ |
| 6 | WebSocket 실시간 연결 | ⏳ | ⏳ |

**설계 문서 위치:** `ESG 레포 > project/design_progress.md` (1~9단계 전체 설계 포함)

---

## ic-pbl (EDK) 프로젝트 인계 정보

### 다음에 할 작업: EDK-01 — medicine.py 리팩터링

**작업 내용:**
- `pmg-ic-pbl/project/src/app/product.py`의 `Coffee`, `Gummy` 클래스를
  `medicine.py`의 `Medicine` 클래스로 교체
- `product_type` → `symptom_category` 개념으로 전환
- `symptom_category`: `두통`, `감기`, `소화불량`, `피로`, `외상` 중 하나

**설계 결정 사항:**
- 결제 시스템(payment.py, cart.py) 유지 — 실제 판매 서비스이므로 필수
- 전문의약품 제외, 일반의약품 + 영양제만 취급

**설계 문서 위치:** `docs/ic-pbl/` 전체

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

```
task-management-repository/
├── COLLABORATION_RULES.md   ← AI 협업 규칙 (필독)
├── AI_HANDOVER.md           ← 이 문서
├── README.md                ← 레포 개요
├── .gitmodules
│
├── docs/
│   ├── ic-pbl/              ← ic-pbl 설계 문서 전체
│   │   ├── CURRENT_STATE.md
│   │   ├── requirements.md
│   │   ├── scope.md
│   │   ├── architecture.md
│   │   ├── system_flow.md
│   │   ├── terminology.md
│   │   ├── test_strategy.md
│   │   └── gui_architecture.md
│   └── ESG/
│       └── CURRENT_STATE.md
│
└── tasks/
    ├── backlog.md
    ├── in-progress.md
    └── done.md
```
