# MAP 프로젝트 API 문서화 표준

> 적용 범위: `map-service-user` (Spring Boot 3.x, JDK 21)
> 갱신일: 2026-05-28
> 라이브러리: **Spring REST Docs** (Swagger/springdoc 제거 완료)

---

## 핵심 원칙

Swagger는 코드에 어노테이션이 침투해 가독성을 저하시킨다.  
**Spring REST Docs는 테스트 코드가 문서를 생성** — 테스트가 통과해야만 문서가 생성된다.

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
test → build/generated-snippets/auth/*/
asciidoctor → build/asciidoc/index.html
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
@MockitoSettings(strictness = Strictness.LENIENT)
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

## 스니펫 경로 주의사항

- `JUnitRestDocumentation` 기본 경로: **`build/generated-snippets`** (project-root 기준)
- `layout.buildDirectory.dir(...)` 사용 시 Gradle `buildDir` 경로(`C:/tmp/...`)로 이동해 불일치 발생
- 반드시 `file('build/generated-snippets')` (상대 경로) 사용

---

## 문서 관리 이력

| 날짜 | 변경 내용 |
|------|---------|
| 2026-05-26 | Swagger/springdoc-openapi 기반으로 작성 |
| 2026-05-28 | Spring REST Docs로 전환 완료, 문서 전면 갱신 |
