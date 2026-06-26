# jemu 워크플로우 치트시트

> 빠른 참조용. 예시·엣지케이스 → [`jemu-workflow.md`](./jemu-workflow.md)

---

## 전체 순서

```
[skeleton 1회] chore 이슈 → chore/브랜치 → 커밋(들) → PR(섹션 템플릿) → 리뷰어 지정 → 머지
[feat]         feat 이슈 1개 → 관심사별 브랜치 → 커밋 1개씩 → PR 배치 오픈 → 머지
[post-feat]    chore/[서비스]Docstring → 모든 파일 Javadoc + PoC HTML → PR → 머지
```

---

## 이슈

```
[CHORE] 동작 (기술스택)          → Task 타입 (노란색)
[FEAT]  기능명                   → Feature 타입 (파란색)
[FEAT]  외부기술 기반 기능명      → 핵심 외부기술 있으면 앞에 포함 (예: KMA, GEMINI)
```

**본문:**
```markdown
## Description
CHORE: [레포명]에 [대상]을 [동작]한다. [추가 맥락].
FEAT:  기능 목적 설명 (레포명 없음)

## TODO
- [ ] 동사 시작 항목, `파일명`은 백틱

## 참고 자료 (선택)
```

---

## 브랜치

```
feature/[서비스명][관심사PascalCase]   예) feature/UserRecommendDto
chore/[PascalCase]                     예) chore/UserDocstring
ci/[이슈번호]                          예) ci/1
```

**분리 순서** (없는 관심사 skip):
```
DTO → Config → Client → Store → Consumer → API → Domain → ErrorHandler → DLQ
```

모든 브랜치 베이스: `develop`

---

## 커밋

```
1 브랜치 = 1 커밋 (제목 줄만, body 없음)
커밋 메시지 = PR 제목
```

**공식:**
```
feat:  [도메인] [설명] 추가|처리|격리|차단
chore: [레포/대상] [동작] 추가|통일|보강|폐기
docs:  [범위] 주석 추가
```

**동사 선택:**

| 동사 | 조건 |
|------|------|
| 추가 | 새 파일·기능 |
| 처리 | 수신·소비·핸들링 |
| 격리 | 외부 오류 차단 |
| 차단 | 무한 루프·재시도 방지 |
| 보강 | 기존 파일 보완 |

---

## PR body

**feat / docs → 산문 (섹션 헤더 없음):**
- 백틱: 메서드명·설정키·스트림명 강조 (클래스명은 권장)
- 종결: `"~한다"`, `"~를 받도록 한다"`
- 설정값 인라인: `(connectTimeout 5s)`, `EX 3600`
- 설계 의도 포함: `"실패 시 PEL 잔류로 재처리되도록 한다"`
- `closes #N` 없음 — 이슈는 수동 close

**chore / ci / develop→main → 섹션 템플릿:**
```markdown
## 변경 사항
- 항목

## 관련 이슈
closes #N

## 체크리스트
- [x] 로컬 테스트 완료
- [x] 불필요한 코드/주석 제거
```
- `## 관련 이슈`: 이슈 없으면 생략

**리뷰어:**
- 중요 chore → `dmlwjds2` 지정
- feat 배치 → 없음

**머지**: GitHub web UI Merge commit

---

## Javadoc (post-feat docs 작업 시)

**Java 클래스:**
```java
/**
 * 클래스명 — 한 줄 요약
 *
 * 본문 설명.
 *
 * 소제목:
 * - 항목
 *
 * {@link 패키지.클래스}  ← 교차참조 (선택)
 */
```

**Java 메서드:**
```java
/**
 * 한 문장 동작 설명.
 *
 * @param args  설명  ← 파라미터 있을 때만
 */
```

**비-Java (yml/SQL/Dockerfile/gradle):**
```
# =============================================================================
# 파일명 — 설명
#
# 책임:
# - 항목
# =============================================================================
```
언어별: `#`(yml/Dockerfile/properties), `//`(groovy), `--`(SQL)
