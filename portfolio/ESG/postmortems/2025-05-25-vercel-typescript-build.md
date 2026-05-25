# Postmortem: Vercel TypeScript 빌드 에러 → 백엔드 배포 차단

**날짜:** 2025-05-25  
**심각도:** CD 파이프라인 중단 (프론트+백엔드 배포 불가)  
**해결 소요 시간:** 분석 10분, 수정 5분

---

## 증상

GitHub Actions CD 파이프라인에서:
1. `test-frontend` 잡 실패 (TypeScript 빌드 에러)
2. `deploy-backend` 잡 **실행 안 됨** (백엔드 코드 변경만 했는데)
3. 결과: 백엔드 수정사항이 배포되지 않음

---

## 원인 분석

### 5 Whys

**왜** 백엔드가 배포되지 않는가?  
→ `deploy-backend` 잡에 `needs: [test-backend, test-frontend]` 의존성이 있기 때문

**왜** `test-frontend`가 실패하는가?  
→ 프론트엔드에 TypeScript 타입 에러 존재

**왜** TypeScript 에러가 있는가?  
→ `DashboardPage`에서 `ModeBView`의 props 인터페이스 변경 시 (`onDone` → `onAssigned`) 프론트엔드 코드 업데이트 누락

**왜** 백엔드 배포가 프론트엔드 테스트에 의존하는가?  
→ CD 설계 시 "모든 테스트 통과 후 배포" 원칙으로 `needs` 설정

**루트 코즈:**  
CD 파이프라인의 `needs` 의존성이 의도적 설계였으나,  
백엔드 배포가 프론트엔드 빌드 성공에 묶여 있어 독립 배포 불가.

### 코드 레벨

```yaml
# .github/workflows/cd.yml — 문제가 된 설계
deploy-backend:
  needs: [test-backend, test-frontend]  # ← test-frontend 실패 시 백엔드 배포 차단
  steps:
    - run: flyctl deploy --remote-only
```

```typescript
// 에러 원인: props 타입 불일치
// ModeBView 인터페이스 변경됨:
// 변경 전: onDone: () => void
// 변경 후: onAssigned: (res: MachineRequestResponse) => void

// DashboardPage에서 여전히 이전 props 사용 중
<ModeBView token={...} onDone={() => refresh()} />
//                      ^^^^^^ TypeScript: Property 'onDone' does not exist
```

---

## 해결 과정

### 즉각 조치: TypeScript 에러 수정

```typescript
// 수정 후
<ModeBView
  token={...}
  onAssigned={(res) => { setModeBResult(res); refresh() }}
/>
```

### CD 파이프라인 설계 재검토

**현행 유지 결정** (변경 안 함):

```yaml
deploy-backend:
  needs: [test-backend, test-frontend]
```

**이유:**
- 프론트/백엔드 타입 계약(API 스키마)이 어긋난 상태에서 배포 시
  → 런타임 버그 발생 가능
- 빌드 에러 = "타입 계약 위반" 시그널
- 프론트엔드 빌드 성공이 타입 호환성의 가장 빠른 검증 수단

다만 트레이드오프 인지:
> "프론트엔드 빌드 에러가 있을 때 백엔드 hotfix 배포가 차단됨"

---

## 예방 조치

1. **컴포넌트 인터페이스 변경 시 즉시 호출부 업데이트** (TypeScript 덕에 빌드타임에 잡힘)
2. `onDone` → `onAssigned` 같은 props 이름 변경 시 전체 파일 내 사용처 확인

---

## 학습

**CD 파이프라인 `needs` 설계 원칙:**

| 시나리오 | 권장 접근 |
|----------|----------|
| 타입 계약 위반 (props 변경 등) | 빌드 에러로 차단 — **의도적** |
| 순수 백엔드 변경 (DB 스키마 등) | 프론트 테스트 불필요 → 독립 파이프라인 고려 |
| Hotfix 긴급 배포 | `workflow_dispatch` + skip 조건 별도 설계 |

**이번 케이스:** 의도된 차단. 빌드 에러 수정이 맞는 대응.

**면접 활용 포인트:**  
"CI/CD 파이프라인 설계에서 trade-off를 경험한 사례"로 활용 가능.  
`needs` 의존성의 장단점, 상황별 선택 기준 서술 가능.
