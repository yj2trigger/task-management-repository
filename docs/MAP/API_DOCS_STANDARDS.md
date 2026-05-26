# MAP 프로젝트 API 문서화 표준

> 적용 범위: `map-service-user` (Spring Boot 3.x, JDK 21)  
> 작성일: 2026-05-26  
> 라이브러리: `springdoc-openapi-starter-webmvc-ui`

---

## 핵심 원칙 3가지

### A. 코드 오염 방지 — 인터페이스 기반 문서화

비즈니스 로직 Controller에 Swagger 어노테이션이 섞이면 가독성이 떨어진다.  
**Swagger 어노테이션은 API 인터페이스에만 작성, Controller는 인터페이스를 구현만 한다.**

#### 구조

```
domain/auth/
├── api/
│   └── AuthApi.java          ← @Operation, @ApiResponse 등 모든 Swagger 어노테이션
└── controller/
    └── AuthController.java   ← implements AuthApi, 비즈니스 로직만
```

#### 예시

```java
// AuthApi.java — Swagger 어노테이션 전담
@Tag(name = "Auth", description = "인증 API")
@RequestMapping("/api/v1/auth")
public interface AuthApi {

    @Operation(summary = "이메일 회원가입")
    @ApiResponse(responseCode = "201", description = "회원가입 성공")
    @ApiResponse(responseCode = "409", description = "이메일 중복")
    @PostMapping("/signup")
    ResponseEntity<AuthResponse> signUp(@Valid @RequestBody EmailSignUpRequest request);
}

// AuthController.java — 로직만
@RestController
@RequiredArgsConstructor
public class AuthController implements AuthApi {

    private final AuthService authService;

    @Override
    public ResponseEntity<AuthResponse> signUp(EmailSignUpRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(authService.signUp(request));
    }
}
```

---

### B. 보안 — 환경별 프로파일 분리

운영 환경에서 Swagger UI 노출은 보안 위험이다.  
**코드를 수정하지 않고 프로파일로 활성화/비활성화를 제어한다.**

#### 설정 파일 구조

| 파일 | Swagger | 용도 |
|------|---------|------|
| `application.yaml` | 비활성 (기본값) | 공통 설정 |
| `application-dev.yaml` | **활성** | 로컬 개발 + 팀 시연 |
| `application-staging.yaml` | **활성** | 임시 배포 서버 |
| `application-prod.yaml` | 비활성 | 실제 운영 |

#### SwaggerConfig 설정

```java
@Configuration
@ConditionalOnProperty(
    name = "springdoc.api-docs.enabled",
    havingValue = "true",
    matchIfMissing = false
)
public class SwaggerConfig {

    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("map-service-user API")
                .version("v1")
                .description("MAP 여행 서비스 사용자/인증 도메인 API"));
    }
}
```

#### 서버 실행 방법

```bash
# 개발/시연용 (Swagger 활성)
./gradlew bootRun --args='--spring.profiles.active=dev'

# 운영 (Swagger 비활성)
SPRING_PROFILES_ACTIVE=prod java -jar app.jar
```

#### CI/CD 환경 변수 설정

```yaml
# GitHub Actions (배포 시)
env:
  SPRING_PROFILES_ACTIVE: prod   # 운영 서버
  # 또는
  SPRING_PROFILES_ACTIVE: staging # 시연 서버
```

---

### C. 코드-문서 싱크 — Code-First 방식

수동 YAML 편집 없이 **Java 코드 구조에서 자동으로 Swagger UI가 생성**된다.

- DTO 필드에 `@Schema(description = "...", example = "...")` 추가
- 코드 변경 시 Swagger UI 자동 반영 — 별도 문서 작업 불필요

#### DTO 예시

```java
@Schema(description = "이메일 회원가입 요청")
public record EmailSignUpRequest(

    @Schema(description = "이메일", example = "user@example.com")
    @Email @NotBlank
    String email,

    @Schema(description = "비밀번호 (8자 이상)", example = "password123!")
    @NotBlank @Size(min = 8)
    String password,

    @Schema(description = "닉네임", example = "여행자")
    @NotBlank @Size(max = 50)
    String nickname
) {}
```

---

## Swagger UI 접근 URL

| 환경 | URL |
|------|-----|
| 로컬 | `http://localhost:8080/swagger-ui.html` |
| 시연 서버 | `https://{staging-host}/swagger-ui.html` |
| API JSON | `{host}/v3/api-docs` |

---

## 규칙 요약

1. Swagger 어노테이션 → `api/` 인터페이스에만. Controller에는 절대 작성 금지.
2. `@ConditionalOnProperty`로 활성화 제어 — 코드 삭제/주석처리 금지.
3. `application-prod.yaml`에서 `springdoc.api-docs.enabled: false` 필수.
4. DTO에 `@Schema` 추가로 자동 문서화 유지.
