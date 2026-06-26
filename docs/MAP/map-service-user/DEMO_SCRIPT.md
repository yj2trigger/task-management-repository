# MAP Auth 도메인 시연 스크립트

> 목적: 기능 정상 동작 확인 + 입출력 캡처 → 문서화  
> 대상: 팀원 개발자  
> 서비스: `map-service-user` (Auth 도메인)

---

## 사전 준비

### Docker 컨테이너란?

컨테이너 = 내 컴퓨터 안에서 돌아가는 **격리된 미니 컴퓨터**.  
PostgreSQL, Redis 같은 서버 프로그램을 로컬에 설치하지 않고 실행할 수 있게 해준다.

```
docker-compose up -d
↓
[PostgreSQL 컨테이너] → 앱이 DB로 사용 (포트 5432)
[Redis 컨테이너]     → 앱이 토큰 저장소/캐시로 사용 (포트 6379)
```

`-d` 옵션 = 백그라운드 실행. 없으면 터미널이 점유되고, 터미널 종료 시 컨테이너도 종료된다.  
컨테이너가 없으면 앱이 DB에 연결하지 못해 시작 실패한다.

### 환경 상세

| 컴포넌트 | 이미지 | 포트 | 비고 |
|---|---|---|---|
| PostgreSQL | postgres:16-alpine | 5432 | DB명: `map_user`, 비밀번호: `localdev` |
| Redis | redis:7-alpine | 6379 | 비밀번호 없음 |

---

## 시작 순서

```powershell
# 1. 컨테이너 시작 (PostgreSQL + Redis)
docker-compose up -d

# 2. 컨테이너 상태 확인 (healthy 상태여야 함)
docker-compose ps

# 3. 앱 서버 시작
./gradlew bootRun --args='--spring.profiles.active=dev,local'

# 4. Swagger UI 접속
# http://localhost:8080/swagger-ui.html
```

> `application-local.yaml` 파일이 없으면 [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) 참고

---

## 시연 순서

### 1. 이메일 회원가입

**엔드포인트**: `POST /api/v1/auth/signup`

| 케이스 | 요청 바디 | 기대 응답 |
|---|---|---|
| 정상 가입 | `{ "email": "test@example.com", "password": "Test1234!", "nickname": "테스터" }` | `201` + `AuthResponse` (accessToken, refreshToken 포함) |
| 중복 이메일 | 동일 이메일로 재요청 | `409 Conflict` |
| 유효성 오류 | `{ "email": "not-email", "password": "123" }` | `400 Bad Request` |

캡처: 요청 바디 + 응답 전체

---

### 2. 이메일 로그인

**엔드포인트**: `POST /api/v1/auth/login`

| 케이스 | 요청 바디 | 기대 응답 |
|---|---|---|
| 정상 로그인 | `{ "email": "test@example.com", "password": "Test1234!" }` | `200` + `AuthResponse` |
| 비밀번호 틀림 | `{ "email": "test@example.com", "password": "wrong" }` | `401 Unauthorized` |
| 존재하지 않는 계정 | `{ "email": "none@example.com", "password": "Test1234!" }` | `401 Unauthorized` |

캡처: 정상 응답에서 `accessToken`, `refreshToken` 값 확인

---

### 3. 토큰 재발급

**엔드포인트**: `POST /api/v1/auth/token/refresh`

| 케이스 | 요청 바디 | 기대 응답 |
|---|---|---|
| 정상 재발급 | `{ "refreshToken": "<로그인에서 받은 토큰>" }` | `200` + 새 `accessToken` + 새 `refreshToken` |
| 만료/잘못된 토큰 | `{ "refreshToken": "invalid-token" }` | `401 Unauthorized` |
| 이미 사용한 토큰 | 재발급 전 토큰으로 재시도 | `401 Unauthorized` (Refresh Token Rotation) |

> **Refresh Token Rotation**: 재발급 시 기존 토큰은 즉시 무효화됨

---

### 4. 로그아웃 + 블랙리스트 확인

**엔드포인트**: `POST /api/v1/auth/logout`

**Swagger UI에서 Bearer 토큰 등록 방법:**
1. 상단 **Authorize** 버튼 클릭
2. `Bearer {accessToken}` 입력 후 Authorize

| 케이스 | 조건 | 기대 응답 |
|---|---|---|
| 정상 로그아웃 | 유효한 Bearer 토큰 | `200 OK` |
| 토큰 없이 요청 | Authorization 헤더 없음 | `401 Unauthorized` |
| 로그아웃 후 재사용 | 로그아웃한 토큰으로 다른 API 호출 | `401 Unauthorized` (Redis 블랙리스트) |

캡처: 로그아웃 후 블랙리스트 적용된 응답

---

### 5. Kakao OAuth URL 확인

**엔드포인트**: `GET /api/v1/auth/kakao`

| 케이스 | 기대 응답 |
|---|---|
| URL 반환 | `200` + 카카오 인증 페이지 URL 문자열 |

> 실제 카카오 로그인 흐름(`/api/v1/auth/kakao/callback`)은 카카오 개발자 콘솔 설정 필요

---

## 캡처 체크리스트

- [ ] 회원가입 정상 응답 (201 + AuthResponse)
- [ ] 중복 가입 오류 (409)
- [ ] 로그인 정상 응답 (200 + 토큰 두 개)
- [ ] 로그인 실패 응답 (401)
- [ ] 토큰 재발급 정상 응답 (200 + 새 토큰)
- [ ] Refresh Token Rotation 오류 (401)
- [ ] 로그아웃 정상 응답 (200)
- [ ] 블랙리스트 적용 확인 (401)
- [ ] Kakao URL 반환 확인

---

## 종료

```powershell
# 컨테이너 중지 (데이터 유지)
docker-compose stop

# 컨테이너 + 데이터 완전 삭제 (초기화 시)
docker-compose down -v
```
