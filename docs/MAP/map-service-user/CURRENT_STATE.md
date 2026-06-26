# MAP map-service-user — 현재 상태

> 최종 갱신: 2026-06-26
> 레포: [we-meet-trip/map-service-user](https://github.com/we-meet-trip/map-service-user)
> 작업 디렉토리: `c:\onedrive\_대학교\MAP\git\map-service-user`

---

## 프로젝트 개요

Spring Boot 3.4.2 / JDK 21 Virtual Threads 기반 사용자·인증 마이크로서비스.

**기술 스택:**

| 영역 | 기술 |
|------|------|
| 프레임워크 | Spring Boot 3.4.2, JDK 21 |
| 보안 | Spring Security, RS256 JWT |
| Token | Access 30분, Refresh 14일 (Rotation + SHA-256 해시 저장) |
| Redis | JWT Blacklist, Rate Limiting (DB1) |
| DB | PostgreSQL + Flyway 마이그레이션 |
| OAuth | Kakao OAuth2 (인가 코드 플로우) |
| API 문서 | Spring REST Docs + AsciiDoc |
| 빌드 | Gradle, asciidoctor 플러그인 |

---

## 현재 구현 상태

### 완료된 기능

| 기능 | 상태 |
|------|------|
| 이메일 회원가입/로그인 | ✅ |
| Kakao OAuth2 로그인 (신규/기존/이메일 연동) | ✅ |
| RS256 JWT 발급 (Access + Refresh) | ✅ |
| Refresh Token Rotation (재사용 탐지 포함) | ✅ |
| Redis Access Token Blacklist (로그아웃) | ✅ |
| Redis Rate Limiting (Lua 원자 스크립트) | ✅ |
| Flyway DB 마이그레이션 (V1 초기 스키마, V2 device_id 제거) | ✅ |
| Spring REST Docs (Swagger 제거 완료) | ✅ |
| GlobalExceptionHandler (5종 핸들러) | ✅ |
| CORS 외부화 (CorsProperties + 환경변수) | ✅ |
| Kakao 토큰 AES-256-GCM 암호화 | ✅ |

### 보안 수정 완료 (2026-05-28)

| ID | 내용 | 파일 |
|----|------|------|
| 1-A | 미인증 요청 401 반환 (기존 403) | `SecurityConfig.java` |
| 1-B | CORS wildcard + credentials 조합 금지 | `SecurityConfig.java` |
| 1-C | Redis 장애 시 fail-open 처리 (기존 500) | `RateLimitService.java` |
| 1-D | XFF 마지막 IP 사용 확정 (신뢰 프록시 아키텍처 기준) | `RateLimitFilter.java` |
| 1-E | Kakao 토큰 AES-256-GCM 암호화 | `OAuthAccount.java`, `AesEncryptionConverter.java` |
| 2-A | ObjectMapper.registerModule 생성자 이동 | `RateLimitFilter.java` |
| 2-B | buildAuthResponse @Transactional 명시 | `AuthService.java` |

### 미완료 / 백로그

| 항목 | 비고 |
|------|------|
| CORS 운영 도메인 확정 | `CORS_ALLOWED_ORIGINS` 환경변수 설정 필요 |
| Apple OAuth2 | 미구현 |
| 프로덕션 배포 | `.ebextensions-dev`, `.platform` 디렉토리 미존재 — 배포 시 실패 |
| VPS·AR 앵커 기능 구현 | 설계 완료 → [VPS_AR_SPEC.md](../VPS_AR_SPEC.md) |

---

## 운영 배포 전 필수 환경변수

| 변수명 | 설명 | 필수 여부 |
|--------|------|----------|
| `DB_URL` | PostgreSQL JDBC URL | 운영 필수 |
| `DB_USERNAME` / `DB_PASSWORD` | DB 인증 | 운영 필수 |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_PASSWORD` | Redis 연결 | 운영 필수 |
| `JWT_PRIVATE_KEY` / `JWT_PUBLIC_KEY` | RS256 RSA 키 (Base64 PKCS8/X509) | 운영 필수 |
| `KAKAO_CLIENT_ID` / `KAKAO_CLIENT_SECRET` / `KAKAO_REDIRECT_URI` | 카카오 OAuth | 운영 필수 |
| `CORS_ALLOWED_ORIGINS` | 허용 오리진 | 운영 필수 |
| `ENCRYPTION_OAUTH_TOKEN_KEY` | Kakao 토큰 AES-256 키 (Base64 32바이트), 미설정 시 암호화 비활성화 | 운영 필수 |

---

## 아키텍처 핵심 결정사항

### JWT: RS256 비대칭키

- Private key: 서명 (서버만 보유)
- Public key: 검증 (다른 서비스에 배포 가능)
- `JwtParser` 생성자에서 단 1회 생성 (캐싱)

### Refresh Token

- DB에 SHA-256 해시만 저장, raw token은 클라이언트에만 전달
- 회전(Rotation): 사용 시 기존 토큰 revoke + 신규 발급
- 재사용 탐지: revoked 토큰 재사용 시 해당 유저 모든 토큰 폐기

### Rate Limiting

- Redis `INCR` + `EXPIRE` 두 명령 → **Lua 스크립트 원자 실행** (race condition 제거)
- `DefaultRedisScript<Long>` 사용, 추가 의존성 없음

### X-Forwarded-For (클라이언트 IP 추출)

- 배포 환경: **AWS Elastic Beanstalk → ALB(Application Load Balancer) 앞단 고정**
- ALB는 기존 XFF를 보존하고 실제 클라이언트 IP를 **마지막에 추가**
  - 클라이언트가 `X-Forwarded-For: fake` 전송 → ALB가 `X-Forwarded-For: fake, real-ip` 로 변환
- 따라서 `xff.split(",")[마지막]` 이 신뢰 가능한 IP
- `xff.split(",")[0]` (첫 번째)은 클라이언트가 조작 가능 → rate limit 완전 우회 취약점
- **`RateLimitFilter.extractClientIp()`는 마지막 값을 사용하도록 수정 완료**

### CORS

- dev/staging: `allowedOriginPatterns("*")` (credentials 허용)
- prod: `allowedOrigins(list)` — `CORS_ALLOWED_ORIGINS` 환경변수로 주입

---

## 알려진 버그 (미수정)

| # | 위치 | 내용 | 심각도 |
|---|------|------|--------|
| 1 | `KakaoOAuthService:72` | 카카오 재로그인 시 `refresh_token` null 응답으로 기존 값 덮어쓰기 | 높음 |
| 2 | `SecurityConfig` | `/api/v1/auth/logout` 미인증 요청(만료 토큰) → 403, refresh token DB 잔존 | 중간 |
| 3 | `KakaoOAuthService:59` | `exchangeCodeForToken()` null 반환 시 NPE (빈 바디 응답 경로) | 낮음 |

---

## PR 시 언급 필요 사항

- Docker DB 포트 5432 → 5433 변경 (로컬 PostgreSQL 서비스 충돌 방지)
- 이메일 가입 후 동일 이메일로 카카오 로그인 시 자동 계정 연동, `authProvider`는 최초 가입 방식(EMAIL) 유지
- `.ebextensions-dev`, `.platform` 디렉토리 미존재 — 배포 워크플로우 실행 전 생성 필요

---

## Flyway 마이그레이션 이력

| 버전 | 내용 |
|------|------|
| V1 | 초기 스키마 (users, oauth_accounts, user_devices, refresh_tokens, stub 테이블) |
| V2 | `refresh_tokens.device_id` 컬럼 제거 (상시 NULL이었음) |

---

## 테스트 구조

| 테스트 | 방식 |
|--------|------|
| `AuthControllerTest` | `@WebMvcTest` + `@AutoConfigureMockMvc(addFilters = false)` |
| `AuthControllerRestDocsTest` | `@WebMvcTest` + `@AutoConfigureRestDocs` — 스니펫 생성 |
| `KakaoOAuthServiceTest` | `@ExtendWith(MockitoExtension.class)` — 분기 로직만 검증 |
| `JwtServiceTest` | 직접 `new JwtService(keyPair, props, redis)` 생성 |

> `OncePerRequestFilter.doFilter()`는 `final`이므로 Mockito로 stub 불가.
> Controller 테스트는 반드시 `addFilters = false`로 필터 계층 우회.

---

## 주의사항

- **git push 금지** — 사용자 명시적 승인 후에만 push
- `절대 push는 하지 마세요` (사용자 원문)
- git user: `yj2trigger`, org: `we-meet-trip`
