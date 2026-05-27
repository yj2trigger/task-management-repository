# MAP map-service-user — 현재 상태

> 최종 갱신: 2026-05-28
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

### 미완료 / 백로그

| 항목 | 비고 |
|------|------|
| CORS 운영 도메인 확정 | `CORS_ALLOWED_ORIGINS` 환경변수 설정 필요 |
| OAuth access_token DB 암호화 | AES-256-GCM 적용 필요, 현재 평문 저장 |
| Apple OAuth2 | 미구현 |
| 프로덕션 배포 | CI/CD 파이프라인 구성 필요 |

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

### CORS

- dev/staging: `allowedOriginPatterns("*")` (credentials 허용)
- prod: `allowedOrigins(list)` — `CORS_ALLOWED_ORIGINS` 환경변수로 주입

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
