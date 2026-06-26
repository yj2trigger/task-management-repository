# jemu 워크플로우 추가 분석 계획

> 목적: `jemu-workflow.md`의 ⚠️ TBD 항목을 실제 데이터로 확정.
> 추측으로 채우지 않음 — 확인된 것만 문서에 반영.

---

## 미확정 항목 목록

| # | 항목 | 상태 |
|---|------|------|
| 1 | `[FEAT]` 이슈 제목 구체성 | ✅ 확정 — 외부 기술명 있으면 포함, 없으면 기능명만 |
| 2 | FEAT Description 문장 구조 | ✅ 확정 — FEAT는 레포명 없이 기능 설명만 |
| 3 | 도메인명 한국어 표현 관례 | ✅ 확정 — 기술명 영어 그대로, 영어 도메인명도 영어 유지 |
| 4 | 브랜치 분리 패턴 일반화 | ✅ 확정 — `feature/[서비스명][관심사]`, 하위→상위 순, 없는 관심사 skip |
| 5 | PR body 클래스명 백틱 일관성 | ⚠️ 부분 확정 — 대다수 사용, 일부 미사용, 의도 불명확. 백틱 권장 처리 |
| 6 | Javadoc 실제 형식 | ✅ 확정 — PR #18 diff 확인. 클래스/메서드 `/** */`, 비-Java 박스형 헤더 |
| 7 | pre-feature chore 필요 조건 | ✅ 확정 — 최초 skeleton 1회만, 이후 반복 없음 |

---

## 분석 방법 (레포별)

### 항목 1·2·3: 이슈 제목·Description·도메인명

**수집 대상:**
```
we-meet-trip/map-service-hub   — 이슈 #1~#5 전체 body
we-meet-trip/map-service-agent — 이슈 #1~#9 전체 body
```

**확인 포인트:**
- `[FEAT]` 이슈 제목에 기술명(JWT, FastAPI 등) 포함 여부
- Description 첫 문장 패턴 (레포명 포함 여부, 종결어미)
- 커밋/PR 제목에서 도메인명을 어떻게 한국어로 표현하는지

**판단 기준:**
- 3개 이상 FEAT 이슈에서 동일 패턴 → 규칙으로 확정
- 불일치 → 케이스별로 기록, 규칙 확정 보류

---

### 항목 4: 브랜치 분리 패턴 일반화

**수집 대상:**
```
we-meet-trip/map-service-hub   — 전체 PR 목록 + 브랜치명
we-meet-trip/map-service-agent — 전체 PR 목록 + 브랜치명
```

**확인 포인트:**
- hub/agent 레포의 `feature/*` 브랜치명 패턴
- 각 PR이 어떤 관심사를 담는지 (Client/Store/Consumer 없는 기능에서 어떻게 분리했는지)
- 관심사 분리 기준이 "레이어"인지 "컴포넌트"인지 "도메인"인지

**판단 기준:**
- 추천 파이프라인과 다른 구조에서도 동일 분리 원칙이 보이면 → 일반 규칙 확정
- 달리 분리했으면 → 그 기능 특화 패턴으로 기록

---

### 항목 5: PR body 클래스명 백틱

**수집 대상:**
```
we-meet-trip/map-service-hub   — PR body 전체 (method="get")
we-meet-trip/map-service-agent — PR body 전체 (method="get")
we-meet-trip/map-service-user  — PR #9 body 원문 재확인 (클래스명 백틱 여부)
```

**확인 포인트:**
- PR #9 body에서 `Mobility`, `DateRange` 등이 백틱 없이 쓰인 게 의도적인지 아니면 스타일 미적용인지
- 다른 레포 PR body에서 클래스명 처리 방식

**판단 기준:**
- 대다수 PR에서 백틱 없음 → 백틱은 설정 키·스트림명에만, 클래스명은 plain text
- 대다수 PR에서 백틱 있음 → PR #9가 예외

---

### 항목 6: Javadoc 실제 형식

**수집 대상:**
```
we-meet-trip/map-service-user — PR #18 get_diff (실제 코드)
```

**확인 포인트:**
- `/** */` 블록 내부 줄 수
- `@param`/`@return` 태그 사용 여부
- 메서드 레벨 Javadoc 작성 여부 (클래스만인지 메서드도인지)
- application.yml 주석 실제 형식 (인라인 `#` vs 블록 헤더)

**판단 기준:**
- diff에서 직접 확인 → 즉시 확정

---

### 항목 7: pre-feature chore 필요 조건

**수집 대상:**
```
we-meet-trip/map-service-hub   — 전체 PR 타임라인 (feat 이전 chore 유무)
we-meet-trip/map-service-agent — 전체 PR 타임라인
```

**확인 포인트:**
- feat PR 이전에 chore PR이 있었는지
- 없었다면 → chore는 최초 세팅 1회만
- 있었다면 → 어떤 내용이었는지

**판단 기준:**
- chore PR이 feat 직전에 없으면 → "최초 세팅 1회만" 확정
- 있으면 → 해당 chore PR 내용으로 판단 기준 추출

---

## 실행 순서

1. **항목 6 먼저** (PR #18 diff 1건 — 빠르고 확실)
2. **항목 4·7** (hub/agent PR 목록 — 브랜치·타임라인 파악)
3. **항목 1·2·3** (hub/agent 이슈 body)
4. **항목 5** (PR body 원문 비교)

---

## 확정 후 처리

각 항목 확정 시:
1. `jemu-workflow.md`의 해당 `⚠️ TBD` 마커 제거
2. 확정된 내용으로 교체
3. 이 파일의 해당 행에 `[완료]` 표시
