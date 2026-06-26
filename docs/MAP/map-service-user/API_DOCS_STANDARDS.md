# MAP 프로젝트 API 문서화 표준

> 적용 범위: `map-service-user` (Spring Boot 3.x, JDK 21)
> 갱신일: 2026-05-28
> 라이브러리: **Spring REST Docs** (Swagger/springdoc 제거 완료)

---

## 핵심 원칙

Swagger는 코드에 어노테이션이 침투해 가독성을 저하시킨다.  
**Spring REST Docs는 테스트 코드가 문서를 생성** — 테스트가 통과해야만 문서가 생성된다.

---

## 비침투성 (Non-Invasive) 검증 결과

`src/main/` 전체에 REST Docs 관련 코드 **0개** (2026-05-28 grep 확인).

| 영역 | REST Docs 흔적 |
|------|--------------|
| `src/main/` (프로덕션) | **없음** |
| `src/test/` (테스트) | `AuthControllerRestDocsTest.java` 1개 |
| `build.gradle` | `testImplementation` / `asciidoctorExt` — 프로덕션 jar 미포함 |

Swagger 시절엔 프로덕션 코드에 직접 침투:
```java
// 삭제된 AuthApi.java — 프로덕션 코드에 문서 어노테이션이 섞여 있었음
@Tag(name = "Auth")
@Operation(summary = "회원가입")
@ApiResponse(responseCode = "201", ...)
public interface AuthApi { ... }
```

현재 `AuthController.java`에는 Spring MVC 어노테이션만 존재, 문서 관련 코드 없음.

---

## 구조

```
src/
├── test/java/.../controller/
│   └── AuthControllerRestDocsTest.java   ← @AutoConfigureRestDocs, 스니펫 생성
└── docs/asciidoc/
    └── index.adoc                        ← include::{snippets}/... 으로 스니펫 삽입
```

빌드 시:
```
./gradlew test        → build/generated-snippets/auth/*/  (스니펫)
./gradlew asciidoctor → C:/tmp/map-service-user-build/asciidoc/index.html
```

---

## Gradle 설정

```groovy
plugins {
    id 'org.asciidoctor.jvm.convert' version '3.3.2'
}

configurations { asciidoctorExt }

ext { snippetsDir = file('build/generated-snippets') }

dependencies {
    testImplementation 'org.springframework.restdocs:spring-restdocs-mockmvc'
    asciidoctorExt 'org.springframework.restdocs:spring-restdocs-asciidoctor'
}

tasks.named('test') {
    outputs.dir snippetsDir
    useJUnitPlatform()
}

tasks.named('asciidoctor') {
    inputs.dir snippetsDir
    configurations 'asciidoctorExt'
    dependsOn test
}
```

---

## 테스트 작성 방법

```java
@WebMvcTest(AuthController.class)
@AutoConfigureMockMvc(addFilters = false)   // Security 필터 우회
@AutoConfigureRestDocs                       // 스니펫 자동 생성
class AuthControllerRestDocsTest {

    @Autowired MockMvc mockMvc;

    @Test
    void signUp() throws Exception {
        mockMvc.perform(post("/api/v1/auth/signup")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{...}"))
            .andExpect(status().isCreated())
            .andDo(document("auth/signup",
                requestFields(
                    fieldWithPath("email").description("이메일"),
                    fieldWithPath("password").description("비밀번호"),
                    fieldWithPath("nickname").description("닉네임")
                ),
                responseFields(
                    fieldWithPath("accessToken").description("Access JWT"),
                    ...
                )
            ));
    }
}
```

---

## 스니펫 경로 주의사항 (Windows 한글 경로 환경)

이 프로젝트는 한글 경로(`c:\onedrive\_대학교\...`) 문제를 우회하기 위해  
`build.gradle`에 `layout.buildDirectory = file("C:/tmp/map-service-user-build")` 설정.

| | 경로 |
|--|------|
| Gradle buildDir | `C:/tmp/map-service-user-build/` |
| 스니펫 실제 생성 위치 | `(프로젝트 루트)/build/generated-snippets/` |
| HTML 출력 위치 | `C:/tmp/map-service-user-build/asciidoc/index.html` |

`JUnitRestDocumentation`은 `org.gradle.project.buildDir` 시스템 프로퍼티 또는 기본값 `build/`를 사용해 스니펫 경로를 결정한다.  
Gradle이 buildDir를 `C:/tmp/...`으로 바꿔도 테스트 워커의 기본값은 프로젝트 루트 기준 `build/`이므로 스니펫은 항상 `(프로젝트 루트)/build/generated-snippets/`에 생성된다.

**결론:** `snippetsDir = file('build/generated-snippets')` (절대 경로 아닌 프로젝트 루트 상대 경로)로 설정해야 asciidoctor `inputs.dir`와 실제 스니펫 경로가 일치한다.  
`layout.buildDirectory.dir('generated-snippets')`을 쓰면 `C:/tmp/map-service-user-build/generated-snippets`를 가리켜 스니펫을 못 찾음.

---

## 문서 관리 이력

| 날짜 | 변경 내용 |
|------|------------|
| 2026-05-26 | Swagger/springdoc-openapi 기반으로 작성 |
| 2026-05-28 | Spring REST Docs로 전환 완료, 문서 전면 갱신 |
| 2026-05-28 | 비침투성 검증 결과 추가, 스니펫 경로 문제 상세 기록 |
