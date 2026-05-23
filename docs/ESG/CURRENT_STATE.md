# CURRENT_STATE — ESG (기숙사 세탁기 예약 서비스)

> Last Update: 2026-05-23
> 원본 레포: [yj2trigger/ESG](https://github.com/yj2trigger/ESG)

---

## 🔵 현재 단계

**구현 1단계 완료 (골격 + Docker) → 구현 2단계(성별 선택) 승인 대기**

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 서비스명 | 기숙사 세탁기 예약 서비스 |
| 한 줄 정의 | 기숙사생들이 세탁기 사용 가능 여부를 원격으로 보고 합리적으로 판단할 수 있도록 하는 앱 |
| 기술 스택 | React + TypeScript / FastAPI / PostgreSQL / Docker / Railway |
| 목적 | 과제 프로토타입 + 실제 배포 + 포트폴리오 |
| 인증 방식 | 성별 선택 화면 (localStorage 저장) — 프로토타입용 |

---

## 핵심 비즈니스 로직: 3-Mode State Machine

| 모드 | 조건 | 동작 |
|------|------|------|
| Mode A | 4대 이상 | 층별 이용 가능 세탁기 수 표시 |
| Mode B | 1~3대 | 버튼 누르면 1:1 세탁기 위치 안내 + 10분 소프트 예약 |
| Mode C | 0대 | 대기열 등록 → 빈 자리 발생 시 순서대로 알림 |

---

## 구현 진행 현황

| 기능 | 백엔드 | 프론트엔드 |
|------|--------|-----------|
| 1. 프로젝트 골격 + Docker | ✅ 완료 | ✅ 완료 |
| 2. 성별 선택 | — | ⏳ 승인 대기 |
| 3. 세탁기 상태 조회 (Mode A/B/C) | ⏳ 대기 | ⏳ 대기 |
| 4. Mode B — 소프트 예약 | ⏳ 대기 | ⏳ 대기 |
| 5. Mode C — 대기열 | ⏳ 대기 | ⏳ 대기 |
| 6. WebSocket 실시간 연결 | ⏳ 대기 | ⏳ 대기 |

---

## 생성된 파일 구조

```
project/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py         ← FastAPI 앱 + CORS + /health
│       ├── config.py       ← 환경변수
│       ├── core/database.py ← DB 연결 + get_db()
│       ├── api/            ← (기능별 router 추가 예정)
│       ├── models/         ← (기능별 ORM 모델 추가 예정)
│       ├── schemas/        ← (기능별 Pydantic 스키마 추가 예정)
│       ├── services/       ← (기능별 비즈니스 로직 추가 예정)
│       └── repositories/   ← (기능별 DB 접근 추가 예정)
└── frontend/
    ├── Dockerfile
    ├── package.json        ← React + TS + Zustand + React Router
    ├── tsconfig.json
    ├── vite.config.ts
    ├── index.html
    └── src/
        ├── main.tsx        ← BrowserRouter 래핑
        └── App.tsx         ← 라우터 뼈대 (페이지 추가 예정)
```

---

## 🚨 현재 리스크

- IoT(LG 세탁기) 연동 방식 미확정 → 더미데이터로 우선 진행

---

## 상세 설계 문서

- `design_progress.md` (ESG 레포) ← 1~9단계 설계 전체 포함
