# ESG 기숙사 세탁기 예약 시스템

한양대학교 기숙사 세탁기 실시간 현황 조회 및 대기열 예약 서비스.

**기간:** 2025년 5월  
**역할:** 풀스택 단독 개발  
**상태:** 운영 중 — SmartThings 전력 수집 포함

---

## 문제 정의

기숙사 세탁기가 사용 가능한지 알려면 직접 세탁실에 가야 한다.  
모두 사용 중이면 → 허탕, 반복 방문, 세탁실 앞 대기.

→ [상세 문제 정의](problem_statement.md)

---

## 핵심 기능

### 3단계 모드 시스템

| 모드 | 상황 | 동작 |
|------|------|------|
| **Mode A** | 여유 (available 多) | 층별 이용 가능 세탁기 수 표시, 직접 이동 |
| **Mode B** | 경쟁 (available 少) | 시스템이 세탁기 자동 배정, 10분 소프트 예약 |
| **Mode C** | 만원 (available 0) | 대기열 등록 → 빈 세탁기 발생 시 **5분 수락 대기** → 수락 시 10분 소프트 예약 |

### 5분 수락 대기 (Mode C)

세탁기가 비면 즉시 배정이 아닌 **수락 요청**을 전송.  
- 5분 이내 수락 → 10분 소프트 예약 확정  
- 미수락 → 대기열 맨 뒤로 이동, 다음 대기자에게 offer  
- 이유: 알림을 놓친 사용자에게 10분을 낭비하지 않도록

### 실시간 업데이트

WebSocket으로 세탁기 상태 변경 즉시 반영.  
성별별 채널 분리 (남자/여자 기숙사 구역).

### SmartThings IoT 전력 수집

SmartThings powerMeter 센서를 주기적으로 polling → 전력값 DB 누적 → 관리자 전력 그래프.  
ADR-007: 이용 가능 세탁기가 적을수록 polling 빈도 높임 (Mode C=60s, B=120s, A=480s).

### 관리자 전력 그래프

어드민 페이지에서 세탁기별 24h 전력 이력 그래프 (recharts).  
60초 자동 갱신, 00:00~23:59 전체 X축, 측정 없는 미래 구간 선 없음.

### 소프트 예약 복원

페이지 새로고침 후에도 `GET /machines/my-reservation`으로 활성 예약을 복원.

### 이메일 인증

@hanyang.ac.kr 이메일 + 6자리 OTP 인증 → 재학생만 접근 가능.

### 어드민 패널

세탁기 상태 수동 관리, 대기열 알림 트리거, 전력 그래프, 전력 임계값 설정.

---

## 기술 스택

```
Frontend  React 18 + TypeScript + Zustand         → Vercel
Backend   FastAPI (Python 3.12) + SQLAlchemy       → Fly.io (Docker)
Database  PostgreSQL                               → Supabase
실시간    WebSocket (FastAPI native)
인증      JWT (7일) + bcrypt + Gmail SMTP OTP
IoT       SmartThings Cloud API (httpx, asyncio polling)
```

---

## 아키텍처 결정 기록 (ADR)

| ADR | 결정 | 선택 이유 |
|-----|------|----------|
| [ADR-001](decisions/ADR-001-websocket.md) | WebSocket | SSE/폴링 대비 양방향 실시간, 대기열 알림 |
| [ADR-002](decisions/ADR-002-deployment.md) | Fly.io + Supabase + Vercel | WS 장기 연결 안정성, Railway 탈락 |
| [ADR-003](decisions/ADR-003-lazy-expiration.md) | Lazy Expiration | Celery/Redis 없이 WS keepalive 재활용 |
| [ADR-004](decisions/ADR-004-auth-email.md) | Gmail SMTP | Resend 무료 플랜 외부 도메인 발송 불가 |
| [ADR-005](decisions/ADR-005-iot-design.md) | REST Webhook 선설계 | 장치 없이도 엔드포인트 완성, curl 테스트 가능 |
| [ADR-006](decisions/ADR-006-queue-acceptance-window.md) | 5분 수락 대기 | 즉시 배정 시 알림 놓친 사용자 10분 낭비 방지 |
| [ADR-007](decisions/ADR-007-smartthings-adaptive-polling.md) | SmartThings 적응형 polling | 수요 높을수록 빈도 높임, 야간 절전 |

---

## 사고 기록 (Postmortem)

| 사고 | 원인 | 해결 |
|------|------|------|
| [Mode B 배정 결과 즉시 사라짐](postmortems/2025-05-25-mode-b-result-disappear.md) | 모드 변경 → 컴포넌트 언마운트 → 로컬 상태 소멸 | `modeBResult` 부모로 lift up |
| [Vercel TS 빌드 에러 → 백엔드 배포 차단](postmortems/2025-05-25-vercel-typescript-build.md) | `needs` 의존성으로 프론트 실패 시 백엔드도 차단 | props 타입 수정 |
| [모바일 가로 스크롤 오버플로우](postmortems/2025-05-25-mobile-overflow.md) | 고정 픽셀 너비 + `box-sizing` 미설정 | `max-width` + `box-sizing: border-box` |
| [소프트 예약 배너 즉시 소멸](postmortems/2025-05-26-reservation-banner-invisible.md) | timezone-naive datetime → JS 로컬 해석 → 9시간 차이 | `asUtc()` 헬퍼 + TIMESTAMPTZ 마이그레이션 |
| [대기열 notified 상태 새로고침 소멸](postmortems/2025-05-26-queue-notified-status-lost.md) | `/queue/status`가 `waiting`만 조회 | `get_entry()` 변경 + `is_notified` 필드 추가 |
| SmartThings polling INFO 로그 미표시 | Python root logger 기본값 WARNING → `logger.info()` 무시 | `logging.getLogger("app").setLevel(INFO)` |
| SmartThings polling 루프 중단 | DB 오류 시 `while True` 전체 중단 | 각 단계 독립 try/except |
| Fly.io 시크릿 자동 전파 실패 | `flyctl secrets deploy` 머신 없을 때 오류 | `flyctl secrets set` + GitHub Actions 전파 |

---

## 상세 문서

- [아키텍처](architecture.md) — 전체 구성, 데이터 모델, WS 이벤트 흐름, SmartThings polling
- [보안 설계](security.md) — JWT, OTP, IoT Device Key, CORS
- [문제 정의](problem_statement.md) — 배경, 사용 시나리오, 제약

---

## 로컬 실행

```bash
# Backend
cd project/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd project/frontend
npm install
npm run dev
```

환경변수: `project/backend/.env.example` 참고.

---

## 협업 인프라

혼자 개발했지만 팀 확장을 고려해 초기부터 협업 구조를 갖춤.

| 항목 | 내용 |
|------|------|
| **브랜치 전략** | `feature/* → main` (GitHub Flow) |
| **Branch Protection** | main PR 필수, CI 통과 필수, 관리자 bypass 허용 |
| **CI** | pytest + vitest — PR마다 자동 실행 |
| **CD** | main push 시 Fly.io + Vercel 자동 배포 + Fly.io 시크릿 자동 전파 |
| **ONBOARDING.md** | 환경 구성, API 명세, WebSocket 이벤트, 브랜치 전략 문서화 |
| **Alembic** | DB 스키마 변경 이력 관리, Supabase 적용 완료 |

---

## 배운 것

**React 상태 설계:**  
"이 상태가 어떤 조건에서 살아있어야 하는가"를 컴포넌트 트리 구조보다 먼저 정의.  
컴포넌트 언마운트 = 로컬 상태 소멸. 생명주기 초과 필요 시 → 상위로 lift up.

**FastAPI BackgroundTask:**  
요청 db 세션은 응답 후 닫힘. BackgroundTask에서는 반드시 별도 `SessionLocal()` 사용.

**Datetime timezone 계약:**  
백엔드-프론트 간 datetime 교환 시 항상 `Z` 또는 `+00:00` 명시 필요.  
SQLAlchemy `DateTime(timezone=True)` → PostgreSQL TIMESTAMPTZ → ISO 8601 직렬화.  
테스트 DB(SQLite)와 프로덕션 DB(PostgreSQL)의 timezone 처리 방식 차이 → naive/aware guard 필수.

**IoT 선설계 패턴:**  
장치 없이 엔드포인트 먼저 설계 → curl로 검증 → 장치 연결 시 URL+Key만 설정.

**Python logging 레벨:**  
`logging.basicConfig()` 없으면 root logger가 WARNING → `logger.info()` 전부 무시.  
프로덕션 진단 로그가 필요하면 앱 시작 시 명시적으로 레벨 설정 필수.

**SmartThings polling 내결함성:**  
`while True` 루프에서 DB 오류 한 번이 전체 루프를 중단시킴.  
각 단계(mode 조회, threshold 조회, 전력 조회, DB 저장, 상태 변경)를 독립 try/except로 격리.

**상태 복원 패턴:**  
React state는 새로고침 시 소멸 → 서버 API로 복원 (`GET /machines/my-reservation`).

**엔티티 상태 추가 시 3-step 체크리스트:**  
① status API에 새 상태 노출 ② 마운트 시 복원 경로 구현 ③ 상태별 UI 분기 확인.

**DB 마이그레이션 설계:**  
`create_all()`은 테이블 생성만, 컬럼 변경은 추적 불가 → Alembic 필수.  
Supabase는 Direct URL(IPv6)과 Session Pooler URL(IPv4 지원) 두 개 제공.
