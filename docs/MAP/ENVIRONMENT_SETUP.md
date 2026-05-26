# MAP 환경 분리 구조 및 로컬 개발 설정

> 적용 서비스: `map-service-user` (Spring Boot 3.x)  
> 작성일: 2026-05-27

---

## 핵심 원칙

**코드는 하나, 환경변수와 프로파일로 동작이 달라진다.**  
로컬 docker-compose DB와 실제 운영 DB는 완전히 분리된 별개의 인스턴스다.  
코드를 수정하지 않고 서버에 환경변수만 등록하면 실제 서비스로 전환된다.

---

## 환경별 동작 요약

| 환경 | 프로파일 | DB | Redis | Swagger UI |
|------|----------|----|-------|------------|
| **로컬 개발** | `dev,local` | docker-compose (localhost:5432) | docker-compose (localhost:6379) | ✅ 활성 |
| **시연 서버** | `staging` | 환경변수 `DB_URL` | 환경변수 `REDIS_HOST` | ✅ 활성 |
| **운영 서버** | `prod` | 환경변수 `DB_URL` | 환경변수 `REDIS_HOST` | ❌ 비활성·차단 |

---

## 로컬 개발 환경 설정

### 1. 사전 준비

[Docker Desktop](https://www.docker.com/products/docker-desktop) 설치 필요.

### 2. DB + Redis 컨테이너 시작

```bash
# map-service-user 레포 루트에서
docker-compose up -d
```

다음 컨테이너가 시작된다:
- `map-user-postgres` — PostgreSQL 16, 포트 5432
- `map-user-redis` — Redis 7, 포트 6379

### 3. `application-local.yaml` 생성

`src/main/resources/application-local.yaml` 파일을 직접 생성한다.  
이 파일은 `.gitignore`에 등록되어 있어 **절대 커밋되지 않는다**.

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/map_user
    username: postgres
    password: localdev        # docker-compose의 POSTGRES_PASSWORD와 동일

  data:
    redis:
      host: localhost
      port: 6379
      password:               # 로컬 Redis는 비밀번호 없음

kakao:
  client-id: "your-kakao-client-id"
  client-secret: "your-kakao-secret"
```

### 4. 앱 실행

```bash
./gradlew bootRun --args='--spring.profiles.active=dev,local'
```

### 5. Swagger UI 접속

```
http://localhost:8080/swagger-ui.html
```

---

## 설정 파일 역할 구조

```
application.yaml          ← 공통 설정 (환경변수 플레이스홀더, Swagger 기본 비활성)
application-local.yaml    ← 로컬 전용 (gitignored, DB 비밀번호 등 실제 값)
application-dev.yaml      ← 개발 환경 (Swagger 활성, SQL 로그 ON)
application-staging.yaml  ← 시연 서버 (Swagger 활성)
application-prod.yaml     ← 운영 서버 (Swagger 비활성·차단)
```

`application.yaml`의 DB 연결 설정 예시:
```yaml
url: ${DB_URL:jdbc:postgresql://localhost:5432/map_user}
```
→ `DB_URL` 환경변수가 있으면 환경변수 사용, 없으면 localhost 기본값 사용.

---

## 실제 서비스 배포 시

코드 수정 없음. 서버(Render, GCP Cloud Run 등)에 환경변수만 등록:

```
SPRING_PROFILES_ACTIVE = prod
DB_URL                 = jdbc:postgresql://{실제-서버-주소}/map_user
DB_USERNAME            = postgres
DB_PASSWORD            = {실제-비밀번호}
REDIS_HOST             = {실제-레디스-주소}
REDIS_PORT             = 6379
REDIS_PASSWORD         = {실제-비밀번호}
KAKAO_CLIENT_ID        = {카카오-앱-키}
KAKAO_CLIENT_SECRET    = {카카오-시크릿}
JWT_PRIVATE_KEY        = {Base64-RSA-개인키}
JWT_PUBLIC_KEY         = {Base64-RSA-공개키}
```

---

## Swagger는 DB와 별개

Swagger UI는 API 문서 화면일 뿐이다. 자체 DB가 없다.  
같은 Spring Boot 앱에 포함되어 있지만 `prod` 프로파일에서는 두 가지 방식으로 차단된다:

1. `SwaggerConfig` — `@Profile("!prod")` 로 Bean 자체가 메모리에 올라가지 않음
2. `SecurityConfig` — `/swagger-ui/**` 경로에 `denyAll()` 적용

즉 운영 서버에서는 Swagger URL에 접근해도 403이 반환된다.

---

## 자주 묻는 질문

**Q. docker-compose를 내리면 로컬 데이터가 사라지나요?**  
A. 아니다. `postgres_data`, `redis_data` named volume에 데이터가 유지된다.  
완전히 초기화하려면 `docker-compose down -v`.

**Q. 로컬 docker-compose DB가 운영 DB에 영향을 주지 않나요?**  
A. 없다. 로컬 컨테이너는 본인 PC에서만 동작한다. 운영 서버는 환경변수로 지정된 별도 DB 인스턴스에만 연결된다.

**Q. 팀원마다 `application-local.yaml`을 따로 만들어야 하나요?**  
A. 그렇다. gitignored 파일이라 공유되지 않는다. 위의 3번 단계를 참고해서 각자 생성한다.
