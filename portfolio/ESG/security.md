# 보안 설계

## 인증 / 인가

### JWT (JSON Web Token)

```
로그인 성공 → JWT 발급 (sub=username, exp=7일)
모든 보호 엔드포인트 → Authorization: Bearer <token>
```

- `sub` 클레임에 username 저장
- username 변경 시 → 새 토큰 재발급 (기존 토큰 즉시 무효화 아님 — 7일 만료 대기)
- 토큰 저장: 프론트엔드 `localStorage` (SPA 특성상 httpOnly 쿠키 대신)

### 역할 분리 (RBAC)

```python
# 어드민 전용 엔드포인트
def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(403, "관리자 권한이 필요합니다")
    return current_user
```

| 역할 | 접근 가능 |
|------|----------|
| 비인증 | `POST /auth/register`, `POST /auth/login`, `POST /auth/verify-email` |
| 인증 사용자 | 대시보드, 예약, 설정 |
| 어드민 | `/admin/*` — 기기 상태 변경, 기기 추가/삭제 |
| IoT 장치 | `POST /iot/machines/{id}/status` (Device Key 인증) |

---

## 이메일 인증

### @hanyang.ac.kr 도메인 제한

```python
@field_validator("email")
def email_must_be_hanyang(cls, v):
    if not v.endswith("@hanyang.ac.kr"):
        raise ValueError("한양대학교 이메일(@hanyang.ac.kr)만 가능합니다")
    return v.lower()
```

### OTP 흐름

```
1. 회원가입 → 6자리 랜덤 OTP 생성 → DB 저장 (만료 10분) → 이메일 발송
2. OTP 입력 → 코드 + 만료시간 검증 → is_verified=True → JWT 발급
3. 미인증 상태 로그인 시 403
```

- OTP 재발송 시 기존 코드 삭제 후 신규 생성 (중복 방지)
- Gmail SMTP + 앱 비밀번호 (계정 비밀번호 노출 없음)

---

## IoT 장치 인증

JWT 방식 불가 (장치는 로그인 흐름 없음) → **Shared Secret (Device Key)**

```python
def _verify_device_key(x_device_key: str = Header(...)):
    if not settings.iot_device_key:
        raise HTTPException(503, "IoT 연동이 설정되지 않았습니다")
    if x_device_key != settings.iot_device_key:
        raise HTTPException(403, "인증 실패")
```

- `IOT_DEVICE_KEY` 환경변수 미설정 시 503 (비활성화 상태)
- `X-Device-Key` 헤더로 전달

---

## 비밀번호 보안

```python
# bcrypt 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

- DB에 평문 비밀번호 저장 안 함
- 비밀번호 변경 시 현재 비밀번호 재확인 필요

---

## 환경변수 관리

| 변수 | 저장 위치 | 용도 |
|------|-----------|------|
| `DATABASE_URL` | Fly.io Secrets | Supabase PostgreSQL 연결 |
| `SECRET_KEY` | Fly.io Secrets | JWT 서명 |
| `GMAIL_USER` | Fly.io Secrets | OTP 이메일 발신 계정 |
| `GMAIL_APP_PASSWORD` | Fly.io Secrets | Gmail 앱 비밀번호 |
| `IOT_DEVICE_KEY` | Fly.io Secrets | IoT 장치 인증 키 |

모든 비밀값 → Fly.io Secrets (환경변수 암호화 저장, `fly secrets set`)  
코드베이스에 하드코딩 없음

---

## CORS 설정

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://esg-laundry.vercel.app"],  # 프로덕션 도메인만
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

개발 환경에서는 `localhost:5173` 추가.

---

## 알려진 한계 (프로토타입)

| 항목 | 현재 | 개선 방향 |
|------|------|----------|
| JWT 만료 전 강제 무효화 | 미지원 (7일 대기) | Redis 블랙리스트 |
| Rate limiting | 미적용 | OTP 엔드포인트에 우선 적용 필요 |
| HTTPS | Fly.io + Vercel 기본 제공 | ✅ |
| SQL Injection | SQLAlchemy ORM (파라미터 바인딩) | ✅ |
