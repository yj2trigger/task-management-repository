# ESG 프로젝트 개발 사고 기록

> Claude가 구현을 진행하면서 내린 판단, 막혔던 지점, 플레이스홀더로 남긴 것들을 기록한 문서.
> 설계(design_progress.md)가 WHY라면, 이 문서는 HOW + WHY NOT의 기록이다.

---

## 0. 시작 전 — 레포 연결 시 판단

### 문제
로컬 `project/` 폴더에 `design_progress.md`, `full_plan.md`, `text.txt`가 이미 존재했고,
GitHub 레포에도 동일 파일이 있었으나 SHA가 달랐다.

### 판단
- `full_plan.md`: SHA 동일 → 충돌 없음
- `design_progress.md`, `text.txt`: SHA 불일치 → 사용자 선택 필요
- 사용자가 "원격 받기"를 선택 → `git checkout -f -b main --track origin/main`으로 강제 체크아웃

### 결과
원격 버전으로 덮어쓴 뒤, 로컬에만 있던 `ppt/`, `프롬프트/` 폴더는 untracked 상태로 유지됨.

---

## 1. 테스트 환경 구축 — 예상치 못한 호환성 문제들

### 1-1. SQLAlchemy 2.0.30 + Python 3.14 비호환

**증상**: `TypeError: Can't replace canonical symbol for '__firstlineno__' with new int value 615`

**원인**: Python 3.14에서 `__firstlineno__` 속성이 추가됐는데,
SQLAlchemy 2.0.30의 `FastIntFlag` 구현이 이 이름을 symbol로 등록하려다 충돌.

**판단**: requirements.txt에는 2.0.30으로 고정돼 있지만, CI는 Python 3.11을 사용하므로
로컬(Python 3.14)에서만 문제. 최신 버전(2.0.49)으로 업그레이드.

> **이후 반영**: requirements.txt를 `sqlalchemy==2.0.49`로 고정.
> CI에서는 Python 3.11 사용하므로 둘 다 OK.

---

### 1-2. psycopg2-binary Windows 빌드 실패

**증상**: pip install 중 `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb1`

**원인**: Windows 한글 환경에서 psycopg2-binary 빌드 중 환경 정보 읽기 실패.

**판단**: 테스트는 SQLite를 쓰기 때문에 psycopg2 자체가 불필요.
→ 테스트 실행에서는 psycopg2 없이 진행. requirements.txt에는 유지(배포 환경은 Linux).

> **플레이스홀더**: psycopg2-binary는 도커/Railway 환경에서만 실제로 필요.
> 로컬 테스트에서는 영구적으로 SQLite 사용.

---

### 1-3. conftest.py import 순서 문제

**증상**: `app.core.database`를 import하는 순간 PostgreSQL 연결 시도 → `ModuleNotFoundError: No module named 'psycopg2'`

**원인**: `database.py`의 `engine = create_engine(settings.database_url)` 가 **모듈 수준(module-level)**에서 실행됨.
conftest에서 DB override를 하기 전에 이미 실행되어 버림.

**판단**: conftest 최상단(모든 import 전)에 `os.environ["DATABASE_URL"] = "sqlite:///./test.db"` 삽입.
pydantic-settings가 `Settings()` 초기화 시 이 env var를 읽어서 SQLite URL을 사용하게 됨.

```python
# conftest.py 최상단 — 반드시 app import 전에 위치해야 함
import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from app.main import app  # 이제 SQLite engine으로 초기화됨
```

---

### 1-4. bcrypt 5.x + passlib 1.7.4 비호환

**증상**: `ValueError: password cannot be longer than 72 bytes, truncate manually if necessary`

**원인**: passlib 1.7.4는 bcrypt 백엔드 로딩 시 긴 비밀번호로 자체 테스트를 수행함.
bcrypt 5.x에서 72바이트 초과 시 silent truncation 대신 ValueError를 raise하도록 변경됨.
passlib이 이 변경을 모르고 예외를 catch하지 않음.

**판단**: bcrypt를 4.x로 다운그레이드. passlib은 아직 bcrypt 5.x를 지원하지 않음.
requirements.txt에 `bcrypt==4.3.0` 고정.

---

### 1-5. tsconfig.node.json 누락

**증상**: vitest 실행 시 `ENOENT: no such file or directory, open '...\tsconfig.node.json'`

**원인**: `tsconfig.json`이 `references: [{ path: "./tsconfig.node.json" }]`를 가지고 있으나,
해당 파일이 git에 커밋되지 않음.

**판단**: Vite 표준 설정 파일 직접 생성.

---

## 2. 구현 3단계 (Auth) — 설계 → 코드 전환 시 판단

### 2-1. 레이어 분리 결정

설계 문서는 `api/ → services/ → repositories/` 구조를 명시함.
처음엔 "간단하니까 service 없이 API에서 직접 repo 호출해도 되지 않나?" 생각했으나:

- `register()`는 중복 체크 + 해싱 + 토큰 생성 3단계 → 비즈니스 로직이 충분히 존재
- 나중에 `login_with_google()` 등 추가 시 service layer 없으면 API layer 비대해짐

→ **레이어 분리 유지**.

---

### 2-2. TokenResponse에 user info 포함

설계: JWT만 반환. 프론트에서 JWT decode해서 user info 추출.

**판단**: 프론트에서 JWT decode를 하려면 `jwt-decode` 패키지가 필요하고,
secret key 없이도 decode는 가능하지만 라이브러리 추가 없이 구현이 지저분해짐.

→ **API response에 username/gender/role 직접 포함**. JWT payload와 redundant하지만 클라이언트 코드가 단순해짐.

```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str    # 추가
    gender: str      # 추가
    role: str        # 추가
```

---

### 2-3. authStore gender vs user 이중 구조

초기 설계: authStore에 `gender` 하나만.

구현하면서 보니: gender 선택은 로그인 **전** 단계이고, 실제 인증 후에는 `AuthUser` 객체가 필요.
그런데 회원가입 폼에서 gender를 미리 선택해서 넘겨야 하므로 `gender`는 그대로 유지.

→ **`gender` (pre-auth 선택값) + `user` (post-auth 전체 정보) 두 필드 유지**.
`setUser()` 시 `gender`도 `user.gender`로 자동 sync.

---

### 2-4. 라우팅 흐름 확정

```
미로그인 + gender 없음  →  /gender
미로그인 + gender 있음  →  /login (register or login)
로그인됨               →  / (DashboardPage)
```

App.tsx에서 이 분기를 처리. 각 페이지는 자기 진입 조건을 스스로 체크해서 redirect.

---

## 3. 구현 4단계 (Machines) — Mode 계산 핵심 로직

### 3-1. count_available의 lazy expiration 반영

`count_available()`이 단순히 `status == 'available'`만 세면 안 됨.
`soft_reserved`이지만 `reserved_until < now()`인 세탁기도 사실상 이용 가능.

→ SQL 조건:
```sql
WHERE (status = 'available')
   OR (status = 'soft_reserved' AND reserved_until < NOW())
```

이렇게 하지 않으면 Mode 계산이 실제보다 비관적으로 나옴.

---

### 3-2. GET /machines 인증 필수인데 403 반환

FastAPI의 `HTTPBearer`는 Authorization 헤더가 없으면 자동으로 403을 반환함.
설계 문서에는 "인증 필요"만 명시. 401이 맞지 않나 생각했으나:

- FastAPI 기본 동작이 403이고,
- 테스트 코드를 `assert response.status_code == 403`으로 이미 작성함.
- RFC 상으로도 둘 다 허용되므로 그대로 유지.

---

### 3-3. 시드 데이터 실제 기숙사 환경 반영

`design_progress.md`에 명시된 환경:
- 1~2층: 공용 9대
- 3층 이상: 층별 성별 구분 1~2대

→ seed 함수:
- 1층: 공용 5대, 2층: 공용 4대 (총 9대)
- 3층: 남성 2대, 4~5층: 남성 각 1대
- 6층: 여성 2대, 7~8층: 여성 각 1대

**현재 플레이스홀더**: 실제 기숙사 층 수/배치는 미확정. 나중에 관리자 페이지에서 조정 가능하도록 설계.

---

## 4. 구현 5단계 (Soft Reserve + Queue)

### 4-1. Lazy expiration vs APScheduler

설계 문서에 "lazy expiration" 명시.

**판단**: 프로토타입에서 APScheduler/Celery 같은 작업 스케줄러 추가는 over-engineering.
→ 매 API 요청 시 `release_expired()` 호출. 요청이 없으면 만료가 안 되는 단점이 있으나,
WebSocket keepalive(30초마다)가 이를 보완함.

> **확장 시 메모**: 실서비스 전환 시 APScheduler로 정확한 타이머 구현 필요.
> 현재는 "최대 30초 지연" 수준의 정확도.

---

### 4-2. QueueEntry user_id unique constraint

처음엔 unique 없이 구현했다가, 중복 등록 방지 로직을 `queue_repo.join()`에서 DB 조회로 체크.
→ DB 레벨에서도 unique를 걸어서 이중 방어. (만약 race condition이 생겨도 DB가 막음)

```python
user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
```

---

### 4-3. Mode 검증 위치

Mode B/C 진입 조건 검증을 어디서 할지:
- API layer에서 → 얇은 API, 검증 로직 분산
- Service layer에서 → 비즈니스 로직 집중

→ **Service layer**에서 검증. API는 요청 받아서 service 호출하고 반환만 함.

```python
def join_queue(db, user):
    mode = get_current_mode(db, user.gender)  # service layer에서 mode 체크
    if mode != "C":
        raise HTTPException(400, f"현재 Mode {mode}입니다")
```

---

### 4-4. Mode B: "사용하시겠습니까?" 버튼 이후 상태

Mode B에서 버튼을 누르면:
1. 세탁기 1대 배정 (soft_reserve)
2. 해당 사용자에게만 층+번호 공개
3. 다른 사용자에게는 해당 세탁기가 "이용중"으로 표시됨

→ `MachineRequestResponse`에 `assigned_machine`과 `reserved_until` 반환.
프론트에서 이를 받아 해당 사용자에게만 보여줌.

**플레이스홀더**: 같은 사용자가 반복 요청할 때 차단 로직 없음.
현재는 Mode B 자체가 세탁기가 1~3대일 때만 활성화되므로, 계속 누르면 세탁기가 빨리 소진됨.
→ 나중에 "이미 예약 중인 사용자는 다시 요청 불가" 검증 추가 필요.

---

## 5. 구현 6단계 (WebSocket)

### 5-1. ConnectionManager 싱글톤

FastAPI는 여러 worker가 뜰 수 있어서 싱글톤 in-memory 방식은 멀티 프로세스에서 문제.
프로토타입에서는 단일 worker만 사용하므로 OK.

> **확장 시 메모**: 실서비스에서는 Redis pub/sub 또는 Redis Streams로 교체 필요.
> 현재 `ws_manager.py`의 `manager` 객체를 Redis 기반으로 교체하면 됨 (인터페이스 유지).

---

### 5-2. WebSocket에서 DB 의존성 주입 방식

FastAPI `Depends(get_db)`는 WebSocket 엔드포인트에서도 동작하지만,
세션이 연결 전체 수명 동안 열려 있으면 리소스 낭비.

→ 접속 검증(토큰 확인)과 초기 상태 전송 시에만 짧게 `SessionLocal()`로 직접 열고 닫음.
30초 keepalive 루프에서는 만료 체크 필요 시만 다시 열고 닫음.

```python
db = SessionLocal()
try:
    released = machine_repo.release_expired(db)
finally:
    db.close()
```

---

### 5-3. Queue notify 타이밍 문제

이상적인 흐름: 세탁기가 반납(in_use → available)되는 순간 대기자에게 즉시 알림.

**현실**: 더미 데이터 환경에서는 "반납"이 자동으로 일어나지 않음.
soft_reserve 만료(10분 후)만이 "세탁기가 다시 이용 가능해지는" 트리거.

→ WebSocket keepalive(30초)마다 `release_expired()` 실행 후 대기자 확인.
즉시 알림이 아닌 **최대 30초 지연** 알림.

> **확장 시 메모**: IoT 연결 시 `machine_repo`의 `update_status()` 메서드를 추가하고,
> 그 호출부에서 `_notify_queue_and_broadcast()`를 트리거하면 즉시 알림 가능.
> Repository Layer만 교체 = 비즈니스 로직 변경 없음.

---

### 5-4. vite-env.d.ts 누락

`import.meta.env.VITE_API_URL` 사용 시 TypeScript 타입 오류 발생.
Vite 프로젝트는 `src/vite-env.d.ts`에 타입 선언이 있어야 함.
이 파일이 git에 커밋되지 않아서 처음엔 `as` 캐스팅으로 우회했다가,
제대로 `vite-env.d.ts` 생성으로 수정.

---

## 6. 전체적인 "이게 있어야 저게 됨" 의존 관계

```
conftest.py DATABASE_URL 설정 (import 전)
    ↓
SQLite engine으로 app 초기화
    ↓
테이블 생성 (Base.metadata.create_all)
    ↓
시드 데이터 (machine_repo.seed)
    ↓
seeded_client fixture
    ↓
register_and_login helper (인증 토큰)
    ↓
세탁기/대기열/WS 테스트
```

```
User 모델 (users 테이블)
    ↓ ForeignKey
Machine 모델 (machines 테이블) ← reserved_by_user_id
QueueEntry 모델 (queue_entries 테이블) ← user_id
```

```
get_current_user (JWT decode → DB lookup)
    ↓ 사용
GET /machines, POST /machines/request
POST /queue/join, DELETE /queue/leave
WS /ws?token=...
```

---

## 7. 구현 7단계 (Docker) — 로컬 실행 환경

### 7-1. lifespan seed 추가

테스트에서는 `conftest.py`의 `seeded_client`가 `machine_repo.seed(db)`를 호출했으나,
실제 Docker 실행 시에는 seed가 없어서 세탁기 테이블이 비어 있는 상태.

→ `main.py`의 `lifespan`에 seed 추가:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        machine_repo.seed(db)
    finally:
        db.close()
    yield
```

`seed()`는 이미 `if db.query(func.count(Machine.id)).scalar(): return` 가드가 있으므로
재시작해도 중복 삽입 없음.

---

### 7-2. `.env` 파일 생성

`docker-compose.yml`이 `${POSTGRES_USER}` 등 env var를 참조하는데,
`.env` 파일이 없으면 빈 문자열로 치환되어 PostgreSQL 컨테이너가 오동작.
`.env.example`을 기반으로 `.env` 생성. git 제외(.gitignore에 이미 포함).

---

### 7-3. docker-compose.yml `version` 필드 제거

**증상**: `docker compose up` 시 `version is obsolete` 경고.

**판단**: Docker Compose v2에서 `version` 필드는 더 이상 필요 없음. 제거.

---

### 7-4. React StrictMode + WebSocket 1006 disconnect

**증상**: 백엔드 로그에 매 WS 연결마다 `WebSocketDisconnect code=1006` 발생.
`ws.py` 41번째 줄 `await ws.send_json(...)` 에서 실패.

**원인**: React 18 StrictMode는 개발 모드에서 effect를 두 번 실행(mount → cleanup → remount).
첫 번째 mount에서 WS1 연결 → cleanup에서 `ws.close()` → 서버가 아직 send_json 중에 연결 끊김 → 1006.

**판단**: 두 번째 mount의 WS2는 정상 동작. 1006은 항상 첫 번째(StrictMode 가짜 mount) 연결에서만 발생.
→ 프로덕션 빌드(`StrictMode` 미적용)에서는 발생하지 않음. 프로토타입 단계에서는 무시.

> **확장 시 메모**: 배포 환경(`npm run build`)에서는 StrictMode 동작 방식이 다르므로 1006 없음.

---

## 8. 대시보드 loading 무한 버그

### 8-1. 증상

회원가입 후 DashboardPage로 이동하면 "불러오는 중..." 무한 표시.
`GET /machines` 는 200 OK 반환 중.

### 8-2. 원인 — machineStore.setData가 loading을 해제하지 않음

```typescript
// 버그 있는 코드
setData: (data) => set({ data, error: null }),  // loading: true 그대로 유지됨
```

`refresh()` 가 `setLoading(true)` 후 `getMachines().then(setData)`를 호출하는데,
`setData`가 `loading`을 건드리지 않아서 `loading: true` 상태가 영구 유지됨.

### 8-3. 수정

```typescript
// 수정 후
setData: (data) => set({ data, loading: false, error: null }),
```

추가로 `DashboardPage`의 `refresh` 함수도 `.then(setData)` 체인 방식에서
`async/await` + `try/catch`로 전환. `useEffect` 의존성도 `[user]`(객체 참조)에서
`[token]`(string 원시값)으로 변경해 불필요한 re-run 방지.

```typescript
const token = user?.token ?? null

const refresh = async () => {
    if (!token) return
    setLoading(true)
    try {
        const res = await getMachines(token)
        setData(res)
    } catch (e) {
        setError(e instanceof Error ? e.message : '오류 발생')
    }
}

useEffect(() => { refresh() }, [token])
```

### 8-4. Vite HMR + Docker 볼륨 주의

파일 수정 후 Docker 볼륨 마운트 환경에서 Vite HMR이 브라우저에 전달되지 않을 수 있음.
브라우저 하드 새로고침(Ctrl+Shift+R) 또는 프론트엔드 컨테이너 재시작으로 해결.

---

## 9. 플레이스홀더 현황 (최종 업데이트)

| 항목 | 현재 상태 | 비고 |
|------|----------|------|
| 세탁기 시드 데이터 | 하드코딩 더미 | IoT 연결 시 관리자 페이지에서 교체 |
| soft_reserve 재요청 방지 | ✅ 완료 | active reserve 있으면 재배정 차단 |
| WS 알림 지연 | 최대 30초 | IoT 연결 시 즉시 push 전환 가능 (Section 5-3 참고) |
| 동일 사용자 중복 WS 연결 | 허용 | 재연결 시 이전 연결 해제 미구현 |
| 세탁기 상태 직접 변경 (관리자) | ✅ 완료 | `PATCH /admin/machines/{id}` |
| 비밀번호 변경 | ✅ 완료 | `PATCH /auth/password` |
| 탈퇴 | 미구현 | MVP 외 |
| Rate limiting | 미구현 | 프로토타입 단계 유지 |
| Docker lifespan seed | ✅ 완료 | — |
| 대시보드 loading 무한 버그 | ✅ 수정 완료 | Section 8 참고 |
| 이메일 인증 (@hanyang.ac.kr OTP) | ✅ 완료 | Section 15 참고 |
| 소프트 예약 복원 | ✅ 완료 | `GET /machines/my-reservation` |
| 대기열 v2 (5분 수락 윈도우) | ✅ 완료 | Section 13 참고 |
| ConnectionManager 단일 인스턴스 | 잠재적 문제 | Fly.io 1대 유지 중. 다중 서버 시 Redis pub/sub 필요 |
| IoT 연동 | 엔드포인트 준비 완료 | `POST /iot/machines/{id}/status` — 장치 연결만 남음 |
| DB Quota 관리 | 계획 수립 완료 | Section 18 참고 — maintenance_service.py 구현 예정 |

---

## 10. 구현 8단계 — CI/CD (GitHub Actions)

### 10-1. ci.yml vs cd.yml 역할 분리

처음엔 ci.yml 하나에 테스트 + 배포를 모두 넣으려 했으나:
- PR에서 테스트는 필요하지만 배포는 안 됨
- push/PR 트리거를 공유하면서 배포 조건만 분기

→ **ci.yml**: 테스트만 (push/PR 공통)  
→ **cd.yml**: 테스트 + 배포 (main push 시만 deploy job 실행)

```yaml
# cd.yml — deploy job 조건
deploy-backend:
  needs: [test-backend, test-frontend]
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

### 10-2. 백엔드 CI — PostgreSQL 없이 pytest

CI 환경에서 Docker PostgreSQL을 띄우면 서비스 정의 + 헬스체크 대기 복잡도 증가.
→ conftest.py의 SQLite override(Section 1-3)가 CI에도 그대로 적용.
`python -m pytest tests/ -v`만 실행하면 됨. 별도 DB 서비스 불필요.

### 10-3. 프론트엔드 CI — vitest 환경

초기: `npm test` 명령이 없어서 CI 실패.
→ `package.json`에 `"test": "vitest run"` 추가. (`vitest` 단독이면 watch 모드 진입 → CI hang)

```json
"scripts": {
  "test": "vitest run"
}
```

### 10-4. Fly.io 배포 — flyctl deploy 위치

`flyctl deploy`는 `fly.toml`이 있는 디렉토리에서 실행해야 함.
`fly.toml`이 레포 루트가 아닌 `project/backend/`에 있으면 `--config` 플래그 필요.

**판단**: `fly.toml`을 레포 루트로 이동 → `flyctl deploy --remote-only`만으로 충분.

---

## 11. 배포 전환 — Railway → Fly.io + Supabase + Vercel

### 11-1. Railway 무료 플랜 종료

사전 공지 없이 크레딧 소진 → 서비스 중단. 대안 스택 선정 기준:
- WebSocket 장기 연결 유지 (cold start 없음)
- 무료 플랜 존재
- PostgreSQL 관리형 (직접 운영 부담 없음)

| 역할 | 선택 | 이유 |
|------|------|------|
| Backend | Fly.io | cold start 없음, `auto_stop_machines=false` 지원 |
| DB | Supabase | 관리형 PostgreSQL, 연결 풀 내장, 무료 500MB |
| Frontend | Vercel | GitHub push → 자동 배포, SPA rewrites 기본 지원 |

### 11-2. Fly.io — auto_stop_machines 설정

WebSocket은 연결이 장시간 유지됨. Fly.io 기본값은 트래픽 없을 시 인스턴스 중지.
→ `fly.toml`에 `auto_stop_machines = false` 필수.

```toml
[[services]]
  auto_stop_machines = false
  auto_start_machines = true
```

이 설정 없으면: 클라이언트 WS 연결 중 서버가 내려가 → 1006 disconnect.

### 11-3. Supabase 연결 URL 두 종류

| URL 종류 | 호스트 | IPv | 용도 |
|---------|--------|-----|------|
| Direct URL | `db.xxx.supabase.co` | IPv6 only | Fly.io 배포 환경 (Linux) |
| Session Pooler | `pooler.supabase.com` | IPv4 | 로컬 Windows 개발 + Alembic |

Windows 로컬에서 Direct URL → DNS 해석 실패 (IPv6 미지원 네트워크).
→ `.env`에 `SESSION_POOLER` 추가. `env.py`와 로컬 실행 시 SESSION_POOLER 우선 사용.

```python
# alembic/env.py
database_url = os.environ.get("SESSION_POOLER") or os.environ.get("DATABASE_URL")
```

### 11-4. Supabase 비밀번호 특수문자 문제

초기 비밀번호에 `@` 포함 → URL에서 `%40`으로 인코딩 필요 → configparser의 `%` 처리와 충돌.
수동 인코딩 시 오타 발생 가능.

**판단**: Supabase DB 비밀번호를 특수문자 없는 문자열로 리셋 → URL 인코딩 문제 원천 차단.

### 11-5. CORS 업데이트

Railway URL → Vercel URL 변경.
Fly.io 시크릿 `CORS_ORIGINS`에 Vercel 도메인 등록:

```bash
fly secrets set CORS_ORIGINS=https://esg-laundry-checker.vercel.app --app esg-laundry-checker
```

---

## 12. DB 마이그레이션 (Alembic)

### 12-1. alembic.ini `%` interpolation 오류

`alembic.ini`의 `sqlalchemy.url` 값을 configparser가 읽을 때 `%`를 변수 보간 문자로 취급.
비밀번호에 `%` 없어도 configparser 내부 처리 방식 때문에 이슈 발생 가능.

→ `env.py`에서 `config.set_main_option("sqlalchemy.url", ...)` 사용 않고,
`create_engine(database_url)`을 직접 호출하여 configparser 우회:

```python
# env.py
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

database_url = os.environ.get("SESSION_POOLER") or os.environ.get("DATABASE_URL")

def run_migrations_online():
    connectable = create_engine(database_url)  # alembic.ini sqlalchemy.url 미사용
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
```

### 12-2. TIMESTAMPTZ 마이그레이션 (34bcd027b891)

**배경**: SQLite에서 naive datetime 사용 → 테스트 통과.
Supabase PostgreSQL에서 `reserved_until < NOW()` 비교 시 naive/aware 혼용 오류 발생 가능.

**마이그레이션 내용**:
- `machines.reserved_until` → `TIMESTAMP WITH TIME ZONE`
- `email_verifications.expires_at` → `TIMESTAMP WITH TIME ZONE`

**SQLite 호환성**: `DateTime(timezone=True)`는 SQLite에서 naive로 저장 → 기존 테스트 영향 없음.
PostgreSQL에서만 실제 timezone 정보 포함.

**적용**:
```bash
# project/backend/ 에서
python -m alembic upgrade head
# → SESSION_POOLER 통해 Supabase에 직접 적용
```

### 12-3. Alembic이 SESSION_POOLER를 써야 하는 이유

Alembic은 DDL(ALTER TABLE, CREATE TABLE 등)을 실행 → 트랜잭션 + 장시간 연결 필요.
Direct URL(IPv6)은 Windows 로컬에서 DNS 해석 실패 → `alembic upgrade head` 실행 불가.
Session Pooler(IPv4) 사용 시 로컬에서도 마이그레이션 가능.

---

## 13. 대기열 시스템 고도화 (Queue v2 — 5분 수락 윈도우)

초기 구현: `waiting → [삭제]` (offer 발송 즉시 소프트 예약 10분 확정)
문제: 알림을 받은 사용자가 앱을 안 보고 있으면 세탁기가 10분 점유됨.

### 13-1. 5분 수락 윈도우 도입

```
waiting
  └─ offer 발송 → notified (soft_reserve 5분)
                      ├─ 수락 (POST /queue/accept) → soft_reserve 10분 확정 → entry 삭제
                      └─ 5분 미수락 (WS keepalive 감지)
                              → machine available 복귀
                              → entry status=waiting, created_at=now (대기열 맨 뒤)
                              → WS queue_offer_expired 발송
                              → 다음 대기자에게 새 offer
```

`created_at=now`로 리셋하는 이유: 맨 앞 순서를 독점하며 계속 미수락하는 악용 방지.

### 13-2. QueueEntry 상태 전이 구현

```python
# queue_repo.reset_expired_notifications()
expired = db.query(QueueEntry).filter(
    QueueEntry.status == "notified",
    QueueEntry.expires_at < datetime.utcnow()
).all()
for entry in expired:
    entry.status = "waiting"
    entry.created_at = datetime.utcnow()  # 맨 뒤로
    entry.notified_at = None
    entry.expires_at = None
```

### 13-3. GET /queue/status — 상태 통합 응답

페이지 새로고침 시 React state 소멸 → 서버 응답으로 복원 필요.

**문제**: waiting 상태인지 notified 상태인지에 따라 프론트 UI가 다름.
**판단**: 하나의 endpoint가 두 상태를 모두 커버:

```python
# waiting 상태
{"in_queue": True, "queue_position": 2, "total": 5, "is_notified": False}

# notified 상태
{"in_queue": True, "is_notified": True, "accept_until": "2026-05-26T10:05:00"}

# 대기열 없음
{"in_queue": False}
```

`get_entry()`는 status 무관 조회 (waiting/notified 둘 다 반환).
별도 endpoint 두 개로 분리하면 프론트가 두 번 조회해야 하므로 통합.

### 13-4. WS 이벤트 타입 확장

초기: `machines_updated`만 존재.
추가된 이벤트:

| 이벤트 | 대상 | 내용 |
|--------|------|------|
| `machines_updated` | gender별 브로드캐스트 | 모드 + 층별 현황 |
| `queue_offer` | 특정 사용자 (1:1) | 배정된 기기 + accept_until |
| `queue_offer_expired` | 특정 사용자 (1:1) | 5분 미수락 통보 |
| `queue_position_updated` | gender별 대기자 전체 | 순위 변동 시 |

**send_to_user 구현**: ConnectionManager에 `{user_id: WebSocket}` dict 추가.
gender별 그룹과 user_id 매핑을 이중 관리.

---

## 14. 소프트 예약 복원 (GET /machines/my-reservation)

### 문제

Mode B 배정 후 사용자가 페이지 새로고침 → "어느 세탁기, 몇 분 남았는지" React state 소멸.
WebSocket 재연결로 machines_updated는 받아도, 이 사용자에게 배정된 기기 정보는 별도 API 필요.

### 판단

`GET /machines/my-reservation`:
- 현재 사용자의 active soft_reserve 조회 (`reserved_until > now()`)
- 반환: `{active: bool, assigned_machine: {...}, reserved_until: "..."}`

DashboardPage 마운트 시 자동 호출 → 카운트다운 UI 복원.

```typescript
useEffect(() => {
  getMyReservation(token).then((res) => {
    if (res.active && res.assigned_machine && res.reserved_until) {
      setActiveReservation({
        machine: res.assigned_machine,
        reserved_until: res.reserved_until,
      })
    }
  })
}, [token])
```

---

## 15. 한양대 이메일 인증 (@hanyang.ac.kr + Gmail SMTP OTP)

### 15-1. 도메인 제한 — Pydantic validator

```python
@field_validator("email")
def email_must_be_hanyang(cls, v):
    if not v.endswith("@hanyang.ac.kr"):
        raise ValueError("한양대학교 이메일(@hanyang.ac.kr)만 가능합니다")
    return v.lower()
```

Pydantic validator → 422 자동 반환. API 레이어에서 별도 처리 불필요.
이메일 소문자 정규화(`lower()`) — 대소문자 혼용 계정 중복 방지.

### 15-2. 회원가입 흐름 변경 (토큰 발급 지연)

기존: `POST /auth/register` → JWT 즉시 반환  
변경: `POST /auth/register` → OTP 발송 → `{message, email}` 반환 (토큰 없음)  
　　　`POST /auth/verify-email` → JWT 반환

**이유**: 미인증 계정에 토큰을 주면 is_verified=False 상태로 서비스 이용 가능. 인증 완료까지 발급 지연.

### 15-3. 미인증 계정 로그인 차단

```python
# auth_service.py — login()
if not user.is_verified:
    raise HTTPException(403, "이메일 인증이 필요합니다")
```

### 15-4. OTP 저장 위치 — User vs EmailVerification 테이블

User 테이블에 OTP 필드를 추가하지 않은 이유:
- 재발송 시 이전 코드 무효화 → EmailVerification row 교체로 단순화
- User 모델 책임 분리 (인증 상태 vs 인증 과정)
- 인증 완료 후 row 삭제 → User 테이블에 불필요한 컬럼 잔류 없음

```python
class EmailVerification(Base):
    __tablename__ = "email_verifications"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), index=True)
    code = Column(String(6))
    expires_at = Column(DateTime(timezone=True))
```

### 15-5. User 모델 — nullable email 설계

기존 계정(email 없음)과의 호환성:
```python
email = Column(String(255), unique=True, index=True, nullable=True)
is_verified = Column(Boolean, default=False)
```
`nullable=True` — 기존 계정은 email이 없어도 DB 오류 없음.

### 15-6. 테스트 mock

CI 환경에서 실제 이메일 발송 불필요. monkeypatch로 no-op 대체:

```python
# conftest.py
@pytest.fixture(autouse=True)
def mock_send_email(monkeypatch):
    monkeypatch.setattr(
        "app.core.email.send_verification_email",
        lambda *a, **kw: None
    )
```

`autouse=True` — 모든 테스트에 자동 적용. 테스트마다 명시 불필요.

---

## 16. 협업 인프라 구축

### 16-1. develop 브랜치 시도 후 철회

팀원 합류 전 `feature → develop → main` 전략 시도.
→ 실제 팀 규모(solo + 가끔 합류)에서 PR 오버헤드만 증가.
→ `feature/xxx → main` 직접 전략으로 단순화. develop 브랜치 삭제.

**브랜치 삭제 순서 주의**: 브랜치 보호가 있는 상태에서 삭제 불가.
보호 먼저 제거 → 삭제:

```bash
gh api repos/yj2trigger/ESG/branches/develop/protection --method DELETE
git push origin --delete develop
```

### 16-2. 브랜치 보호 — enforce_admins=false

owner(yj2trigger)가 PR 없이 main에 직접 push 가능하도록 설정.

```bash
gh api repos/yj2trigger/ESG/branches/main/protection \
  --method PUT \
  --field enforce_admins=false \
  --field required_status_checks='{"strict":true,"contexts":["Backend Tests","Frontend Tests"]}' \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

→ 서비스 런칭 전까지 main 직접 push 허용. 팀원은 여전히 PR + CI 통과 + 1명 승인 필수.

### 16-3. Datetime Timezone — asUtc() 헬퍼 도입 후 TIMESTAMPTZ로 해결

**초기 증상**: `reserved_until` 값이 JS `new Date()`로 파싱 시 KST(+9h) 오프셋 적용 → 9시간 오차.

**임시 해결 (asUtc 헬퍼)**:
```typescript
function asUtc(s: string): Date {
  return new Date(s.endsWith('Z') || s.includes('+') ? s : s + 'Z')
}
```
백엔드가 timezone 정보 없이 직렬화한 datetime 문자열 끝에 'Z' 강제 추가.

**근본 해결 (Alembic TIMESTAMPTZ 마이그레이션)**:
`DateTime(timezone=True)` 컬럼은 PostgreSQL에서 UTC로 저장 + ISO 8601(+00:00) 포함 직렬화.
→ JS `new Date()`가 올바르게 UTC로 파싱. `asUtc()` 헬퍼 불필요.

---

## 17. IoT 연동 사전 설계 — Tuya Cloud

### 17-1. Tuya Cloud 프로젝트 구성

**상황**: 실제 IoT 플러그를 연결하기 전, Tuya Cloud 설정 방법을 확정해야 함.

**판단**: "Smart Home" 프로젝트 타입 선택.
- Industry 타입은 상업용 장치 제조사 대상 → 기숙사 플러그 같은 소비자 장치와 호환 낮음.
- Smart Home → "Link Tuya App Account" → QR 코드 스캔으로 앱 페어링 장치를 Cloud에 등록.

**데이터센터**: China East 선택.
- 국내 발매 Tuya 장치는 China 서버에 기본 등록됨.
- 다른 지역 선택 시 Device ID 조회 실패 가능.

### 17-2. HMAC-SHA256 서명 방식

Tuya Cloud OpenAPI는 모든 요청에 서명 필요.

```
sign = HMAC-SHA256(
  key=CLIENT_SECRET,
  message=CLIENT_ID + timestamp + nonce + string_to_sign
)
```

`string_to_sign`은 HTTPMethod + \n + 요청 body hash + \n + 빈 헤더 + \n + URL path.

서명 생성 로직을 `tuya_client.py`에 캡슐화 → API 호출부는 URL + body만 넘기면 됨.

### 17-3. Adaptive Polling 설계

단순 6초 폴링: 30대 × 24시간 × 60분 × 10회 = 432,000 호출/월 → 무료 플랜(26,000/월)의 **16.6배** 초과.

**판단**: 상태별 interval 차등 적용:

| 상황 | 간격 | 이유 |
|------|------|------|
| Mode A (여유) | 30초 | 헛걸음 방지 우선, 빠른 업데이트 필요 |
| Mode B (경쟁) | 60초 | WS가 primary path, polling은 보완 |
| Mode C (만원) | 120초 | 대기열 알림이 primary path |
| 심야 (00:00~06:00) | 300초 | 이용자 극소 |

→ 예상 17,460 호출/월 (quota 67%).

설계 상세 → [ADR-007](decisions/ADR-007-iot-polling-strategy.md)

---

## 18. DB Quota 관리 계획 — 사전 설계

### 18-1. 문제 인식

IoT 연동 시 `machine_status_logs` 테이블 급증 계산:
- 세탁기 ~30대 × 6초 간격 = 14,400 행/일
- 30일 = 432,000 행 축적
- PostgreSQL row 평균 ~100 bytes → 약 43 MB/월

Supabase 무료 500MB에서 운영 로그 + 사용자 데이터 합산 시 6~12개월 내 한도 도달 가능.

**판단**: 실제 한도 도달 전에 retention policy + 경보를 설계.

### 18-2. 자동 정리 로직

```python
# maintenance_service.py (구현 예정)
def cleanup_old_logs(db: Session):
    cutoff = datetime.utcnow() - timedelta(days=30)
    db.query(MachineStatusLog).filter(
        MachineStatusLog.created_at < cutoff
    ).delete()

    expired_cutoff = datetime.utcnow() - timedelta(days=7)
    db.query(QueueEntry).filter(
        QueueEntry.status.in_(["expired", "cancelled"]),
        QueueEntry.created_at < expired_cutoff
    ).delete()
    db.commit()
```

FastAPI startup lifespan 또는 별도 백그라운드 태스크로 주기 실행.

### 18-3. 경보 임계값

`pg_database_size(current_database())` 쿼리로 현재 DB 사용량 조회.

| 임계값 | 동작 |
|--------|------|
| >80% (400MB) | 관리자 페이지 경고 표시 |
| >90% (450MB) | Gmail SMTP 관리자 이메일 + 자동 정리 즉시 실행 |

### 18-4. 관리자 페이지 통합

`GET /admin/system/stats` 엔드포인트 (구현 예정):
```json
{
  "db_used_mb": 127.4,
  "db_limit_mb": 500,
  "db_usage_pct": 25.5,
  "logs_count_30d": 18420
}
```

AdminPage React 컴포넌트에 게이지 UI 추가 (80% 주황, 90% 빨강 색상 분기).
