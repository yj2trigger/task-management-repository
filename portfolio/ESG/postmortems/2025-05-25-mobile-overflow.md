# Postmortem: 모바일 화면 가로 스크롤 오버플로우

**날짜:** 2025-05-25  
**심각도:** UX 저하 (모바일 레이아웃 깨짐)  
**해결 소요 시간:** 분석 5분, 수정 10분

---

## 증상

모바일 브라우저(375px 뷰포트)에서:
- 화면 우측으로 가로 스크롤 발생
- 일부 카드/버튼이 화면 밖으로 삐져나옴
- 데스크탑(1280px)에서는 정상

---

## 원인 분석

### 원인 1: 고정 픽셀 너비 사용

```typescript
// 문제 코드
const styles = {
  card: {
    width: '400px',        // ← 375px 모바일에서 초과
    padding: '24px',
  },
  actionBox: {
    minWidth: '320px',     // ← 좁은 화면에서 overflow 유발
  }
}
```

CSS에서 `px` 고정값은 뷰포트보다 클 경우 부모를 벗어남.

### 원인 2: `min-width` + `padding` 합산 미고려

```
minWidth: 320px + padding: 24px * 2 = 368px
뷰포트: 375px — 가까스로 들어가지만 body margin 포함 시 초과
```

### 원인 3: `overflow: hidden` 미설정

최상위 컨테이너에 `overflow-x: hidden`이 없어 자식의 overflow가 그대로 노출.

---

## 해결 과정

### 수정 1: 고정 너비 → 상대 단위

```typescript
// 수정 후
const styles = {
  card: {
    width: '100%',
    maxWidth: '400px',     // 데스크탑에서 최대 400px
    padding: '20px',
    boxSizing: 'border-box' as const,
  },
  container: {
    width: '100%',
    maxWidth: '600px',
    margin: '0 auto',
    padding: '0 16px',    // 좌우 여백 보장
    boxSizing: 'border-box' as const,
  }
}
```

### 수정 2: `actionBox` 상대화

```typescript
actionBox: {
  width: '100%',           // minWidth 제거
  padding: '16px',
  boxSizing: 'border-box' as const,
}
```

### 수정 3: 전역 overflow 방어

```css
/* index.css */
body {
  overflow-x: hidden;
}
```

---

## 예방 조치

**레이아웃 작성 체크리스트 추가:**
- [ ] `px` 고정 너비 사용 시 → `max-width`로 대체 검토
- [ ] `minWidth` 사용 시 → 모바일 최소 뷰포트(320px)와 비교
- [ ] padding/margin 합산 시 → `box-sizing: border-box` 확인
- [ ] 새 컴포넌트 추가 시 → 375px 뷰포트에서 확인

---

## 학습

**모바일 레이아웃 원칙:**

```
px 고정 → % 또는 max-width
minWidth → 주의 (overflow 주범)
padding 합산 → box-sizing: border-box
전체 너비 → width: 100% + box-sizing
```

React inline styles는 CSS-in-JS 없이 `box-sizing`을 명시해야 함:
```typescript
boxSizing: 'border-box' as const  // TypeScript에서 literal type 필요
```
