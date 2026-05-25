# ADR-002: 배포 플랫폼 — Fly.io + Supabase + Vercel

## 상태
채택됨 (Railway에서 전환, 2025-05-25)

## 컨텍스트

초기 배포 계획은 Railway 단일 플랫폼이었음.
개발 진행 중 WebSocket 장기 연결 요구사항이 확정되면서 플랫폼 재검토 필요.

핵심 제약:
- 백엔드: WebSocket 장기 연결 유지 필수 (30초 keepalive 루프)
- 프론트엔드: 정적 파일 배포 (SPA)
- DB: 관리 오버헤드 최소화

## 검토한 선택지

### 단일 플랫폼: Railway

| 항목 | 내용 |
|------|------|
| 장점 | 설정 단순, DB 내장, 단일 대시보드 |
| 단점 | WebSocket 장기 연결 불안정 확인, 무료 플랜 제한 |
| 결론 | WS 안정성 미확보 → **탈락** |

### 단일 플랫폼: Render

| 항목 | 내용 |
|------|------|
| 장점 | WebSocket 지원, 무료 티어 |
| 단점 | 무료 플랜 Cold Start (15분 비활성 시 슬립) → WS 연결 끊김 |
| 결론 | WS 상시 가동 불가 → **탈락** |

### 분리 배포: Vercel (FE) + 백엔드 옵션들

Vercel은 WebSocket 미지원 → 프론트엔드 전용.
백엔드 후보: Fly.io vs AWS ECS vs Heroku.

| 플랫폼 | WS 지원 | Cold Start | 비용 | 결론 |
|--------|---------|------------|------|------|
| **Fly.io** | ✅ | 없음 (설정 가능) | 무료 티어 | **채택** |
| AWS ECS | ✅ | 없음 | 복잡한 과금 | 과도함 |
| Heroku | ✅ | 있음 (무료 폐지) | 유료만 | 비용 문제 |

DB 후보: Supabase vs PlanetScale vs Neon.

| 플랫폼 | 특징 | 결론 |
|--------|------|------|
| **Supabase** | PostgreSQL 완전 관리형, 연결 풀링 내장, 무료 500MB | **채택** |
| PlanetScale | MySQL 기반, 브랜치 기능 | PostgreSQL 필요로 탈락 |
| Neon | PostgreSQL, Serverless | 연결 풀 별도 설정 필요 |

## 결정

```
Frontend  → Vercel      (CDN, SPA rewrites, GitHub 연동 자동 배포)
Backend   → Fly.io      (Docker, auto_stop_machines=false, WS 유지)
Database  → Supabase    (PostgreSQL, 연결 풀링, 관리 오버헤드 없음)
```

## 구현 핵심

```toml
# fly.toml
[vm]
  memory = "256mb"

[[services]]
  auto_stop_machines = false   # WS 장기 연결을 위해 슬립 방지
  auto_start_machines = true
```

```yaml
# .github/workflows/cd.yml
deploy-backend:
  needs: [test-backend, test-frontend]  # 양쪽 테스트 통과 후 배포
  steps:
    - uses: superfly/flyctl-actions/setup-flyctl@master
    - run: flyctl deploy --remote-only
```

## 트레이드오프

| 포기한 것 | 얻은 것 |
|-----------|---------|
| 단일 플랫폼 단순성 | WS 장기 연결 안정성 |
| Railway 내장 DB | Supabase 관리형 PostgreSQL |
| 단일 대시보드 | 플랫폼별 최적화 |

## 결과 (사후)

- Fly.io WS 장기 연결: 30초 keepalive 루프 안정적 동작 확인
- Vercel SPA rewrites: `{"source": "/(.*)", "destination": "/index.html"}` 설정으로 React Router 정상 동작
- CD pipeline `needs` 설계 주의: `test-frontend` 실패 시 백엔드 배포도 차단됨
  → TypeScript 빌드 에러로 실제 경험한 문제 (→ ADR 아닌 Postmortem 참고)

---

## 추가 결정: Fly.io 배포 전략 — rolling → immediate

### 문제

CD 파이프라인에서 `flyctl deploy --remote-only` (기본값: rolling 전략) 실행 시:

```
✖ Failed to acquire lease for d8d5940b032178: machine not found
```

rolling 전략은 기존 machine ID를 직접 참조해서 업데이트. Fly.io가 내부적으로 machine을 교체하면 stale ID가 남아 lease 획득 실패.

### 해결

```yaml
run: flyctl deploy --remote-only --strategy=immediate
```

`immediate`: 기존 machine ID 참조 없이 새 machine 생성 → 헬스체크 통과 → 트래픽 전환 → 구버전 삭제.

### 트레이드오프: WebSocket 동시 실행

`immediate` 전략은 배포 순간 구버전/신버전 instance가 수초간 동시 존재할 수 있음.

REST API는 stateless → 무관.  
**WebSocket은 stateful** → 문제 발생 가능:

- `ConnectionManager`가 in-memory로 연결 목록 관리
- instance 2개 동시 실행 시 각자 다른 연결 목록 보유
- 신버전이 구버전 연결 사용자에게 브로드캐스트 불가 (수초간)

**허용 판단 근거:**
1. 단일 instance 앱 → 동시 실행 구간 수초에 불과
2. 프론트엔드 WS 자동 재연결 로직 (3초) → 끊겨도 즉시 복구
3. 세탁기 서비스에서 수초 브로드캐스트 지연은 허용 범위

**근본 해결 방향 (미적용):**  
WS 연결 상태를 Redis Pub/Sub으로 외부화 → instance 수 무관하게 브로드캐스트 가능.  
현재 규모에서 오버엔지니어링으로 판단, 보류.
