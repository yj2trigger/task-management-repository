# ADR-004: 이메일 인증 방식 — Gmail SMTP + 6자리 OTP

## 상태
채택됨 (Resend에서 전환, 2025-05-25)

## 컨텍스트

기숙사 세탁기 서비스는 **재학생만 사용** 가능해야 함.
username/password만으로는 외부인 가입을 막을 수 없음.

요구사항:
1. @hanyang.ac.kr 도메인 이메일만 허용
2. 실제 이메일 소유자임을 검증 (OTP)
3. 이메일 발송 인프라 필요

## 검토한 선택지

### 이메일 도메인 제한만 (OTP 없음)

```python
if not email.endswith("@hanyang.ac.kr"):
    raise HTTPException(400, "한양대학교 이메일만 가능합니다")
```

| 항목 | 내용 |
|------|------|
| 장점 | 구현 단순 |
| 단점 | 타인의 학교 이메일 입력 가능, 실제 소유 확인 불가 |
| 결론 | 보안 불충분 → **탈락** |

### OTP 이메일 발송 서비스 비교

| 서비스 | 무료 한도 | 외부 도메인 발송 | 결론 |
|--------|-----------|-----------------|------|
| **Resend** | 100통/일 | 무료 플랜 불가 (`resend.dev` 도메인 전용) | **탈락** |
| SendGrid | 100통/일 | 가능 | 가입 절차 복잡 |
| **Gmail SMTP** | 500통/일 (앱 비밀번호) | 가능 | **채택** |
| AWS SES | 200통/일 (샌드박스) | 샌드박스 제한 | 과도함 |

### Resend 탈락 이유 (실제 경험)

초기 Resend 선택 → 배포 후 실제 이메일 발송 시 실패 확인.
원인: Resend 무료 플랜은 `@resend.dev` 도메인에서만 발송 가능.
`@hanyang.ac.kr` 수신자에게 발송하려면 커스텀 도메인 인증 필요 (유료).

→ Gmail SMTP로 전환.

## 결정

**Gmail SMTP (smtplib) + 6자리 OTP, 10분 만료.**

```python
def send_verification_email(email: str, code: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[ESG] 이메일 인증 코드"
    msg["From"] = settings.gmail_user
    msg["To"] = email
    # HTML 이메일 본문
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(settings.gmail_user, settings.gmail_app_password)
        server.sendmail(settings.gmail_user, email, msg.as_string())
```

```python
# OTP 생성 및 저장
code = "".join(random.choices(string.digits, k=6))
expires_at = datetime.utcnow() + timedelta(minutes=10)

# 기존 인증 요청 삭제 후 신규 저장 (재발송 대응)
db.query(EmailVerification).filter(EmailVerification.email == email).delete()
verification = EmailVerification(email=email, code=code, expires_at=expires_at)
```

인증 흐름:
```
1. POST /auth/register → User 생성(is_verified=False) → OTP 발송
2. POST /auth/verify-email → 코드+만료 검증 → is_verified=True → JWT 발급
3. POST /auth/login → is_verified=False 시 403 반환
```

## 트레이드오프

| 포기한 것 | 얻은 것 |
|-----------|---------|
| 전용 이메일 서비스 안정성 | 외부 도메인 발송 즉시 가능 |
| 고급 이메일 분석/추적 | Gmail 하루 500통 무료 |
| | 구글 계정 앱 비밀번호로 간단 설정 |

## 결과 (사후)

- Gmail SMTP 발송 정상 동작 확인 (@hanyang.ac.kr 수신)
- 재발송 시 기존 OTP 삭제 후 신규 생성 → 중복 코드 문제 없음
- 환경변수: `GMAIL_USER`, `GMAIL_APP_PASSWORD` → Fly.io Secrets 저장
