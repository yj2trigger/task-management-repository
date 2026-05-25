# Postmortem: Mode B 소프트 예약 결과 즉시 사라짐

**날짜:** 2025-05-25  
**심각도:** 사용자 경험 중단 (배정 결과 미표시)  
**해결 소요 시간:** 분석 15분, 수정 10분

---

## 증상

Mode B에서 "사용하시겠습니까?" 클릭 시:
1. 세탁기 배정 API 호출 성공
2. 배정 결과(N층 N번) 화면에 표시됨
3. **0.x초 만에 화면이 사라지고 다시 "사용하시겠습니까?" 버튼으로 돌아감**

---

## 원인 분석

### 5 Whys

**왜** 배정 결과가 사라지는가?
→ `ModeBView` 컴포넌트가 언마운트되어 로컬 `result` 상태가 소멸하기 때문

**왜** `ModeBView`가 언마운트되는가?
→ 부모 컴포넌트의 렌더 조건이 `data.mode === 'B'`인데, 이 조건이 `false`가 되기 때문

**왜** `data.mode`가 `'B'`에서 바뀌는가?
→ `onDone()` 호출 → `refresh()` → `getMachines()` → 서버에서 새 모드 반환

**왜** 서버가 다른 모드를 반환하는가?
→ 배정으로 `soft_reserved` 기기 수 증가 → available 수 감소 → Mode B→C 전환 가능

**루트 코즈:**
배정 결과(`result`)가 모드에 종속된 컴포넌트(`ModeBView`) 내부 로컬 상태로 저장됨.
모드 변경 → 컴포넌트 언마운트 → 상태 소멸.

### 코드 레벨 추적

```typescript
// 문제가 된 코드
function ModeBView({ token, onDone }) {
  const [result, setResult] = useState<MachineRequestResponse | null>(null)

  const handleRequest = async () => {
    const res = await requestMachine(token)
    setResult(res)   // ← 로컬 상태에 저장
    onDone()         // ← 즉시 refresh() 트리거
    // onDone() → refresh() → data.mode 변경 → ModeBView 언마운트
    // 언마운트 시 result 상태 소멸
  }
  ...
}

// 부모
{data.mode === 'B' && <ModeBView ... />}  // mode 변경 시 언마운트
```

---

## 해결 과정

**접근 1 (기각):** `onDone()` 호출 지연 (결과 확인 후 호출)
→ WebSocket `machines_updated` 이벤트도 `refresh()`를 트리거하므로
   사용자가 "확인" 버튼을 누르기 전에 WS 이벤트로 모드가 바뀔 수 있음.

**접근 2 (채택):** `result` 상태를 부모(`DashboardPage`)로 lift up.
모드 변경과 무관하게 `modeBResult`가 유지됨.

```typescript
// 수정 후
export default function DashboardPage() {
  const [modeBResult, setModeBResult] = useState<MachineRequestResponse | null>(null)

  // 모드와 무관하게 렌더
  {modeBResult && (
    <div style={styles.queueAlert}>
      <strong>세탁기가 배정되었습니다!</strong>
      <span>{modeBResult.assigned_machine.floor}층 {modeBResult.assigned_machine.machine_number}번</span>
      <button onClick={() => setModeBResult(null)}>확인</button>
    </div>
  )}

  // ModeBView는 결과 없을 때만 렌더 (중복 방지)
  {data.mode === 'B' && !modeBResult && (
    <ModeBView
      token={...}
      onAssigned={(res) => { setModeBResult(res); refresh() }}
    />
  )}
}
```

---

## 예방 조치

같은 패턴 재발 방지를 위해 Mode C 대기열 상태도 동일하게 점검.

발견: `queueInfo` 상태도 `ModeCView` 내부 로컬 상태 → Mode C→B 전환 시 소멸.
→ 동일한 방식으로 `DashboardPage`로 lift up.

---

## 학습

**React 상태 설계 원칙:**
> "이 상태가 어떤 조건에서 살아있어야 하는가"를  
> 컴포넌트 트리 구조보다 먼저 정의해야 한다.

- 컴포넌트 언마운트 = 로컬 상태 소멸
- 비즈니스 상태(배정 결과, 대기 현황)는 UI 구조(모드)에 종속되면 안 됨
- 상태의 생명주기가 컴포넌트 생명주기를 초과해야 하면 → 상위로 lift up

**면접 활용 포인트:**
"React에서 어려웠던 버그"로 활용 가능.
원인 분석 → 접근법 비교 → 근본 해결 서사가 명확함.
