# 보안 검토 — map-service-user

> 검토일: 2026-05-28
> 대상 브랜치: main
> 검토 범위: 인증/인가, JWT, Rate Limiting, CORS, 데이터 암호화

---

## 수정 완료 항목

### 1-A. 미인증 요청 401 반환

**파일**: `global/config/SecurityConfig.java`

**문제**: JWT 검증 실패 시 `SecurityContext`를 비운 채 필터 체인 통과 → Spring Security 기본 동작이 403 반환.
401(미인증)과 403(권한 없음)은 의미가 다름.

**수정**:
```java
.exceptionHandling(e -> e.authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED)))
```

---

### 1-B. CORS wildcard + credentials 조합 금지

**파일**: `global/config/SecurityConfig.java`

**문제**: `application.yaml` 기본값 `cors.allowed-origins: "*"`. 이 경우 `setAllowedOriginPatterns("*")` + `setAllowCredentials(true)` 조합 → 모든 오리진이 인증 포함 CORS 요청 가능. CORS 스펙 위반이자 보안 취약.

**수정**: wildcard origins 감지 시 `allowCredentials(false)` 분기 처리.

```java
if (isWildcard) {
    config.setAllowedOriginPatterns(List.of("*"));
    config.setAllowCredentials(false);   // wildcard + credentials 조합 금지
} else {
    config.setAllowedOrigins(origins);
    config.setAllowCredentials(true);
}
```

**운영 영향 없음**: `application-prod.yaml`에서 `CORS_ALLOWED_ORIGINS`를 실제 도메인으로 설정하면 wildcard 분기 미진입.

---

### 1-C. Redis 장애 시 Rate Limit 500 → fail-open

**파일**: `global/ratelimit/RateLimitService.java`

**문제**: `redisTemplate.execute()`가 `RedisConnectionFailureException` 발생 시 try/catch 없음 → 로그인, 회원가입, 토큰 갱신 엔드포인트 전체 500 응답.

**수정**: `isAllowed()` try/catch 추가, Redis 장애 시 `true`(허용) 반환 + warn 로그.

**정책 결정**: **fail-open** (가용성 우선). Redis 장애 시 rate limit 비활성화 허용.
대안인 fail-closed(503)는 Redis 장애가 전체 인증 서비스 중단으로 이어지므로 부적절.

---

### 1-D. X-Forwarded-For 마지막 IP 사용 확정

**파일**: `global/ratelimit/RateLimitFilter.java`

**결론**: `parts[parts.length - 1]` (마지막 IP) 유지.

**근거**:
- 신뢰할 수 있는 단일 역방향 프록시(LB) 아키텍처에서 LB는 클라이언트 실제 IP를 XFF 끝에 **추가(append)**
- 공격자가 `X-Forwarded-For: fake-ip` 전송 → LB가 `fake-ip, real-ip` 생성 → `parts[0]` = 스푸핑 가능
- `parts[parts.length - 1]` = LB가 기록한 값 → 클라이언트 통제 불가

**주의**: 다중 프록시 레이어 도입 시 이 정책 재검토 필요. LB가 XFF를 덮어쓰거나 다른 프록시가 추가되는 경우 "rightmost trusted proxy" 방식으로 변경해야 함.

---

### 1-E. Kakao 토큰 AES-256-GCM 암호화

**파일**: `global/crypto/AesEncryptionConverter.java` (신규), `domain/user/entity/OAuthAccount.java`, `src/main/resources/application.yaml`

**문제**: `oauth_accounts.access_token`, `oauth_accounts.refresh_token` 컬럼에 Kakao API 토큰 평문 저장. DB 탈취 시 Kakao 계정 직접 접근 가능. 기존 코드에도 `// 암호화 권장` 주석 존재.

**수정**:
- AES-256-GCM (96-bit IV, 128-bit auth tag) JPA `AttributeConverter` 구현
- 저장 형식: `base64(IV):base64(ciphertext+tag)`
- 환경변수 `ENCRYPTION_OAUTH_TOKEN_KEY` 미설정 시 암호화 비활성화 (로컬 개발 편의)
- `OAuthAccount.accessToken`, `refreshToken` 필드에 `@Convert` 적용

**운영 배포 전 필수**: `ENCRYPTION_OAUTH_TOKEN_KEY` = Base64-encoded 32바이트 키 주입.
기존 데이터 있는 경우 평문 → 암호화 마이그레이션 스크립트 별도 작성 필요.

---

### 2-A. ObjectMapper.registerModule 생성자 이동

**파일**: `global/ratelimit/RateLimitFilter.java`

**문제**: `writeErrorResponse()` 호출마다 공유 빈인 `ObjectMapper`에 `registerModule()` 호출. 동시 요청 시 공유 상태 변경 → 레이스 컨디션 가능성.

**수정**: `@RequiredArgsConstructor` → 명시적 생성자로 변경. `objectMapper.copy()`로 복사 후 한 번만 모듈 등록.

```java
public RateLimitFilter(RateLimitService rateLimitService, ObjectMapper objectMapper) {
    this.rateLimitService = rateLimitService;
    this.objectMapper = objectMapper.copy().registerModule(new JavaTimeModule());
}
```

---

### 2-B. buildAuthResponse @Transactional 명시

**파일**: `domain/auth/service/AuthService.java`

**문제**: 클래스 레벨 `@Transactional(readOnly = true)`, `buildAuthResponse()`에 별도 어노테이션 없음. 메서드 내부에서 `refreshTokenRepository.save()` 호출(쓰기 작업). 현재 모든 호출자가 write 트랜잭션을 가지고 있어 동작하지만, 새 호출자 추가 시 readOnly 트랜잭션에서 저장 실패 위험.

**수정**: `buildAuthResponse()`에 `@Transactional` 명시.

---

## 검토 시 false positive로 판단한 항목

| 항목 | 이유 |
|------|------|
| SHA-256 refresh token 비교 — 타이밍 공격 우려 | DB 인덱스 조회(hash lookup), 앱 코드에서 직접 문자열 비교 없음. 타이밍 공격 무관 |
| logout 엔드포인트 `permitAll()` | 만료된 토큰으로도 로그아웃 처리 가능하도록 의도적 설계. `blacklistAccessToken`이 만료 토큰 gracefully 처리 |
| `blacklistAccessToken`이 만료 토큰 무시 | 만료된 토큰은 이미 무효. blacklist 불필요, 올바른 처리 |
| 이메일 null 유저 다중 허용 | PostgreSQL UNIQUE 제약은 NULL 다중 허용. `User.java` 주석에 명시. 카카오 이메일 동의 거부 정상 케이스 |
| Access token에 email 클레임 포함 | BFF 패턴에서 다운스트림 서비스 DB 조회 없이 유저 정보 사용. 의도적 설계 |
| `FilterRegistrationBean`으로 RateLimitFilter disabled | Spring Boot `@Component` 필터 자동 등록 방지 (이중 등록 차단). 정상 패턴 |
| `JwtParser` 인스턴스 변수 | JJWT `JwtParser`는 `build()` 후 immutable → 스레드 안전 |
| refresh token 재사용 시 전체 폐기 | Refresh Token Rotation 표준 보안 패턴 |
