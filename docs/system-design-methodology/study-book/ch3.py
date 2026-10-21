"""3장 ppa3 — More Compose: rememberSaveable·발자국·리컴포지션."""
from qbook2 import s as _s, quote, table, fill, slide


def s(*n):
    return _s(*n, deck="ppa3")


INTRO = """
<div class="note">소문제를 풀고 → 바로 아래 <b>답·해설</b>. 이중선(옅은 배경) = 문제, 가는 실선 = 답·해설, 굵은 실선 = 원문(원본 ppa3 슬라이드 번호·쪽 위/아래), 점선 = 해설 정리.
앞 장에서 이미 물은 지식은 다시 묻지 않고 "→ N장 문제 M"으로 잇습니다.</div>
<h2>3장. ppa3 — More Compose: rememberSaveable·발자국·리컴포지션</h2>
"""

ITEMS = []
P = ITEMS.append

ar_q, ar_a = fill(["Turtle Screen에서 다룬 항목", "Compose 영역"], [
    ["Scaffold, Box, Column, Row, Modifier, Chaining과 순서", ("?", "Layout 기초")], ["remember, mutableStateOf, by 위임, 상태 호이스팅 개념", ("?", "상태 관리 기초")],
    ["animateDpAsState, tween", ("?", "애니메이션")], ["Canvas, DrawScope, drawCircle/drawOval, 좌표 비율 계산", ("?", "그리기")],
    ["MaterialTheme, colorScheme, typography, shapes, CompositionLocal", ("?", "테마")], ["clickable, MutableInteractionSource, collectIsPressedAsState", ("?", "상호작용")],
    ["@Composable, trailing lambda, 함수 타입 파라미터", ("?", "함수형 UI 문법")], ["@Preview, Material Icons, Gradle 의존성 관리", ("?", "도구")]])
P(dict(kind=["table"], title="Turtle Screen에서 다룬 Compose 영역 (○)",
parts=[
 dict(q="Turtle Screen(2장)에서 다룬 항목들이 속하는 Compose 영역을 쓰시오. 이 영역들이 포함하는 범위 세 가지는?" + ar_q,
      a=ar_a + "범위: <b>정적 UI 그리기, local 상태, 애니메이션</b>(추가로 실제로 많이 쓰이는 영역을 더 알아볼 필요가 있다).",
      why="<p>2장의 목차다. 영역별로 2장 문제를 되짚으면 복습이 된다: Layout(2장 16·24), 상태(18), 애니메이션(19), 그리기(20·21), 테마(12), 상호작용(23), 문법(9), 도구(14·22). \"상태 호이스팅\", \"CompositionLocal\"은 이 목록에만 이름이 나오고 정의는 원문에 없다.</p>")],
quote=quote("위의 내용은 정적 UI 그리기, local 상태 및 애니메이션을 포함하고 있다.", s(2))))

rs_q, rs_a = fill(["상황", "remember", "rememberSaveable"], [
    ["버튼 클릭으로 리컴포지션", ("?", "유지"), ("?", "유지")], ["화면 회전", ("?", "초기화"), ("?", "유지")], ["다크 모드 전환", ("?", "초기화"), ("?", "유지")],
    ["시스템 언어 변경", ("?", "초기화"), ("?", "유지")], ["멀티 윈도우 크기 조정", ("?", "초기화"), ("?", "유지")],
    ["백그라운드에서 시스템이 프로세스를 종료한 뒤 복귀", ("?", "초기화"), ("?", "유지(완전한 프로세스 킬 이후 복원까지)")]])
P(dict(kind=["table", "name", "diag"], title="remember vs rememberSaveable",
parts=[
 dict(q="Compose 상태 저장 함수 remember와 rememberSaveable로 만든 값이 각 상황에서 유지되는지 쓰시오." + rs_q, a=rs_a,
      why="<p>remember가 지키는 범위 = <b>리컴포지션 사이</b>. Activity가 부서지는 순간(설정 변경)이나 프로세스가 죽는 순간에는 같이 사라진다. rememberSaveable은 remember와 동일하게 리컴포지션 사이에 값을 유지하면서, 추가로 <b>Activity/Process 재생성 시에도</b> 값을 보존한다.</p>"),
 dict(q="화면 회전·다크 모드 전환·시스템 언어 변경·멀티 윈도우 크기 조정을 묶어 부르는 이름과, 그때 Activity에 일어나는 일은?",
      a="configuration change(설정 변경). <b>Activity 자체가 파괴되고 다시 생성</b>되는 상황."),
 dict(q="rememberSaveable은 값을 어디에 저장해 두었다가 복원하나? 그 저장소를 정의하시오. 그대로 저장할 수 있는 타입 예 4가지와, 복잡한 custom 타입을 저장하려면 필요한 것은?",
      a="<b>Bundle</b>(안드로이드가 Activity 재생성 시에 데이터를 임시 보관하는 저장소). Bundle = 안드로이드 OS에서 시스템이 프로세스 간 또는 컴포넌트 간에 데이터를 안전하게 주고받을 수 있도록 설계된 <b>Key-value 쌍</b>의 형태로 데이터를 담는 컨테이너 클래스. Int, String, Boolean, Float. <b>Saver 인터페이스</b>로 직렬화/역직렬화 규칙을 정의.",
      why="<p>rememberSaveable이 프로세스 킬에서도 살아남는 이유 = Bundle은 시스템이 보관한다. 1장 문제 19(프로세스 재생성 시 onCreate(savedInstanceState)가 null이 아님)가 바로 이 Bundle이고, 6장 onSaveInstanceState와도 같은 저장소다. 상태 보존 장치 비교: remember(리컴포지션) / rememberSaveable(설정 변경 + 프로세스 킬, Bundle) / ViewModel(설정 변경, 객체 자체가 살아남음 — 4장).</p>")],
quote=quote("화면 회전, 다크 모드 전환, 시스템 언어 변경, 멀티 윈도우 크기 조정 등 configuration change (설정 변경) 상황은 Activity 자체가 파괴되고 다시 생성되는 상황이고, 이 상태에서도 UI 상태가 유지되도록 합니다.", s(3, 4))))

P(dict(kind=["order", "diag"], title="회전하면 거북이가 가운데로 돌아가는 버그 고치기",
intro="버그: Turtle Screen의 <code>var offsetX by remember { mutableStateOf(0.dp) }</code>로 만든 거북이 위치가 화면을 회전하면 초기화된다.",
parts=[
 dict(q="Turtle Screen 회전 버그의 수정 4단계를 원본 순서대로 쓰시오.",
      a="① remember{} 대신 <b>rememberSaveable{}</b> ② mutableStateOf(0.dp) 대신 <b>mutableFloatStateOf(0f)</b> ③ step과 range의 단위도 dp 대신 <b>f</b>(24f, 140f) ④ animateDpAsState{} 안은 dp 기준으로 애니메이션이 일어나므로, Float 변수 offsetX·offsetY 뒤에 <b>.dp</b>를 붙여 Dp로 변환",
      why="<p>하나의 원인에서 연쇄된다: 저장소가 Bundle로 바뀜 → 타입이 Bundle 지원 타입(Float)이어야 함 → 그 변수와 계산하는 step·range도 Float → 화면(애니메이션)에 줄 때만 Dp로 변환. \"<b>저장은 Float, 그릴 때만 Dp</b>\".</p>"),
 dict(q="remember를 rememberSaveable로 바꾸기만 하면 왜 안 되나? <code>animateDpAsState(targetValue = offsetX.dp, …)</code>의 .dp는 왜 붙이나? 1.dp 안에 들어 있는 Float 값은?",
      a="rememberSaveable은 Bundle에 저장하므로 <b>Bundle이 지원하는 타입</b>이어야 하는데 Dp는 아니다 → (0.dp)를 (0f)로 함께 바꿔야 한다. 순수 계산값인 Float를 dp 기준 애니메이션에 넘기려고. 정확히 <b>1.0f</b>(Dp 타입은 그 안에 든 숫자를 그대로 보관)."),
 dict(q="앱 코드를 고친 뒤 에뮬레이터에서 빌드해도 앱 로딩이 제대로 되지 않는 등 먹통이 됐다. 해결 방법의 이름과 절차는? 그 방법을 평소의 부팅 방식과 비교해 정의하시오.",
      a="<b>Cold Boot</b>. X 버튼으로 에뮬레이터를 완전히 정지 → 오른쪽 사이드 바의 디바이스 매니저 → 드롭다운에서 앱(AVD) 선택 → 오른쪽 점 세 개 메뉴 → 처음에 있는 \"Cold Boot\". 평소 에뮬레이터는 직전 종료 시 상태를 snapshot으로 저장했다 다음 부팅 때 빠르게 띄우는 <b>quick boot</b>를 쓰고, cold boot는 에뮬레이터의 이전 상태를 <b>전혀 참고하지 않고 완전히 처음부터</b> 새로 부팅한다.",
      why="<p>Quick/Cold의 기본 정의는 1장 문제 25. 여기서 새로운 것은 \"<b>먹통이 되면 Cold Boot</b>\"라는 쓰임새.</p>")],
fig=slide("ppa3", 6, 85),
quote=quote("Solution: remember{} 대신 rememberSaveable{} 로 수정하시면 됩니다. 단, 을 사용할 때는 Dp 대신 Bundle 이 지원하는 타입이어야 하므로, (0.dp) 를 (0.f) 로 함께 변환해야 합니다.", s(4, 5, 6, 7, 8))))

P(dict(kind=["name", "calc", "diag"], title="발자국 목록을 회전에도 살리기: data class와 listSaver",
intro="<code>data class FootprintData(val x: Float, val y: Float, val angle: Float)</code> / <code>val trailSaver = listSaver&lt;MutableList&lt;FootprintData&gt;, Float&gt;(save = { trailList -&gt; trailList.flatMap { data -&gt; listOf(data.x, data.y, data.angle) } }, restore = { savedFloats -&gt; val restored = mutableStateListOf&lt;FootprintData&gt;(); savedFloats.chunked(3).forEach { chunk -&gt; restored.add(FootprintData(x = chunk[0], y = chunk[1], angle = chunk[2])) }; restored })</code> / <code>val trail = rememberSaveable(saver = trailSaver) { mutableStateListOf&lt;FootprintData&gt;() }</code>",
parts=[
 dict(q="FootprintData는 무엇을 담나? 이것을 rememberSaveable에 그냥 넣을 수 없는 이유는? trailSaver는 무엇이고 무엇을 알려 주나?",
      a="발자국 하나의 x, y와 회전 각도(angle). FootprintData는 Bundle에 직접 저장되지 않는 <b>복합 형태</b>라서(원문 설명의 Pair&lt;Float, Float&gt;도 마찬가지). trailSaver = rememberSaveable과 함께 쓸 <b>커스텀 Saver</b>(listSaver)로, 저장할 때 원시 리스트로 어떻게 바꾸고 복원할 때 어떤 타입으로 되돌릴지를 알려 준다."),
 dict(q="발자국 두 개 (x = 0, y = −10, angle = 0)과 (x = 24, y = 10, angle = 180)이 있을 때, trailSaver의 save가 Bundle에 넣는 값의 모양은? 어떤 함수로 그렇게 만드나? restore는 그 값을 어떻게 되돌리나?",
      a="하나의 평평한 Float 리스트 <b>[0, −10, 0, 24, 10, 180]</b> — 각 FootprintData를 listOf(x, y, angle) 3개로 푼 뒤 <code>flatMap</code>으로 이어 붙임. restore는 <code>chunked(3)</code>으로 3개씩 묶어 인덱스 0, 1, 2를 x, y, angle에 매핑해 FootprintData 객체를 새로 만들고 restored 리스트에 추가.",
      why="<p>Saver의 원리 = \"<b>Bundle이 아는 모양으로 납작하게 → 다시 부풀리기</b>\". 3이라는 숫자는 FootprintData의 필드 수(x, y, angle).</p>"),
 dict(q="restore가 결과를 담을 리스트를 <code>mutableStateListOf</code>로 만드는 이유는? 그 리스트 타입 이름은? 처음 만든 trail에도 mutableStateListOf를 쓴 이유는?",
      a="이 리스트가 <b>관찰되어야</b> 하므로 — 값이 바뀔 때 UI가 자동으로 다시 그려진다. <b>SnapshotStateList</b>. mutableStateListOf는 리스트 자체가 Compose의 state가 되도록 만들어 주는 특수한 리스트라서(발자국이 추가되면 화면이 다시 그려짐).",
      why="<p>2장 문제 18(mutableStateOf = 바뀌면 알린다)의 리스트판이 mutableStateListOf.</p>")],
fig=slide("ppa3", 11, 90),
quote=quote("save ={...} 는 저장 로직이다. trailList 의 FootprintData (x,y, angle)을 3개의 list 로 푼 후에 flatMap 으로 하나의 평평한 Float 리스트로 이어 붙인다.", s(10, 11, 13))))

ang_q, ang_a = fill(["Turtle Screen 버튼", "rotationAngle", "발자국이 옆으로 비키는 축"], [
    ["위(onUp)", ("?", "−90f"), ("?", "x (세로로 걸으므로 가로로 비킴)")], ["아래(onDown)", ("?", "90f"), ("?", "x")],
    ["왼쪽(onLeft)", ("?", "180f"), ("?", "y (가로로 걸으므로 세로로 비킴)")], ["오른쪽(onRight)", ("?", "0f"), ("?", "y")]])
P(dict(kind=["table", "diag"], title="발자국 남기기 로직 leaveFootprint()",
intro="TurtleScreen 상태 변수: rotationAngle(오른쪽 기준 각도), isLeftFoot(처음 true), maxTrailSize = 100, footprintOffset = 10f, step = 24f, range = 140f. leaveFootprint()의 규칙: 왼발이면 옆 오프셋 −10, 오른발이면 +10. 가로로 걸을 때(각도 0 또는 180)는 y를, 세로로 걸을 때는 x를 옆 오프셋만큼 비킨다. 발자국 각도는 가로면 왼발 0°·오른발 180°, 세로면 왼발 −90°·오른발 90°. 기록한 뒤 isLeftFoot를 뒤집고, 목록이 maxTrailSize를 넘으면 맨 앞을 지운다.",
parts=[
 dict(q="TurtleScreen의 isLeftFoot, maxTrailSize, footprintOffset는 각각 무엇인가?",
      a="isLeftFoot: 왼발인지 여부 / maxTrailSize: 발자국 리스트의 길이(최대 100개) / footprintOffset: 양쪽 발자국 사이의 거리(10f)"),
 dict(q="Turtle Screen의 각 방향 버튼이 rotationAngle에 넣는 값과, 그 방향으로 걸을 때 발자국이 옆으로 비키는 축을 쓰시오." + ang_q, a=ang_a,
      why="<p>\"옆으로 비킨다\" = <b>진행 방향과 수직</b>: 가로로 걸으면 세로(y)로, 세로로 걸으면 가로(x)로 비켜야 양발 모양이 된다. 각도는 화면 좌표 기준(아래가 +)이라 위가 −90, 아래가 +90 — 2장 문제 17(위로 가면 offsetY 감소)과 같은 원리.</p>"),
 dict(q="거북이가 오른쪽으로 계속 걸으면 발자국은 어떤 모양으로 찍히나? 101번째 발자국이 찍힐 때 trail에서 무슨 일이 일어나나?",
      a="x는 거북이의 이동 직전 위치 그대로, y가 −10, +10으로 번갈아 → 진행 방향 양옆으로 왼발·오른발이 교대로 찍힘(isLeftFoot가 매번 반전). trail.size가 100을 넘으므로 <code>trail.removeAt(0)</code> — 가장 오래된(맨 앞) 발자국이 지워짐."),
 dict(q="Turtle Screen의 onUp 콜백 안에서 <code>rotationAngle = -90f; leaveFootprint(); offsetY = …</code> 순서로 쓴 이유는? 세 문장을 무엇으로 구분했나? leaveFootprint를 TurtleScreen 안의 함수 하나로 만든 이유는?",
      a="발자국을 <b>먼저</b> 남기고(거북이가 이동하기 직전의 위치를 리스트에 추가) 거북이가 이동해야 하므로. 세미콜론(;). 위·아래·왼쪽·오른쪽 버튼이 눌릴 때마다 반복될 로직을 한곳에 모아 <b>재사용</b>하려고.")],
fig=slide("ppa3", 17, 90),
quote=quote("발자국이 찍히려면, 거북이가 이동하기 직전의 위치를 리스트에 추가하기 위한 로직이 필요합니다.", s(12, 14, 17, 18, 19))))

P(dict(kind=["name", "order"], title="회전하는 거북이와 발자국 그리기",
parts=[
 dict(q="거북이 몸을 rotationAngle만큼 돌리는 Modifier는? 몇 ms 동안 부드럽게 도나? 그 애니메이션 함수는 2장의 animateDpAsState와 무엇이 다른가?",
      a="<code>.graphicsLayer(rotationZ = animatedRotation)</code>. tween 200ms. Dp가 아니라 <b>Float</b>를 애니메이션하는 <code>animateFloatAsState</code>(targetValue = rotationAngle, label \"turtleRotation\")."),
 dict(q="발자국 모양을 그리는 Footprint() 컴포저블은 몇 dp Canvas에 무엇으로 그리나(발바닥/발가락)? 발자국마다 다른 방향은 어떻게 주나?",
      a="<b>16dp</b> Canvas에 <b>drawOval</b>(발바닥 타원) + <b>drawCircle 3개</b>(발가락, 반지름 w × 0.12). Canvas의 modifier에 <code>.graphicsLayer(rotationZ = angle)</code> — FootprintData의 angle을 넘김."),
 dict(q="화면에 여러 발자국을 그리는 방법: 무엇을 순회하며, 각 발자국의 위치는 어떤 Modifier로 정하나? Box 안에 발자국들과 Turtle을 어떤 순서로 써야 하나? 이유는?",
      a="trail 리스트를 <code>trail.forEach { data -&gt; Footprint(…) }</code>로 순회, 위치는 <code>Modifier.offset(x = data.x.dp, y = data.y.dp)</code>(Turtle을 이동시킬 때와 같은 방법). 발자국을 <b>먼저</b>, Turtle을 나중에 — Box는 먼저 쓴 자식이 아래, 나중에 쓴 자식이 위에 겹쳐 그려지므로 거북이가 발자국 위에 보이게.",
      why="<p>2장 문제 21의 Canvas 규칙(먼저 그린 것이 아래)과 <b>같은 원리가 Box에도</b> 적용된다. 2장 문제 16에서 \"나중에 추가할 경우를 대비해 Box를 썼다\"던 것이 여기서 발자국으로 회수된다.</p>"),
 dict(q="TurtleScreen에서 rotationAngle과 isLeftFoot도 rememberSaveable로 만든 이유는?",
      a="화면 회전(설정 변경)에도 거북이의 방향과 왼발/오른발 순서가 유지되도록.")],
fig=slide("ppa3", 22, 85),
quote=quote("Box() 는 여러개의 자식 중, 먼저 쓴 자식이 아래에 나중에 쓴 자식이 위에 겹쳐서 그려지기 때문에, 발자국들을 Turtle() 보다 먼저 나열해서 거북이가 발자국 위에 겹쳐 보이게 만듭니다.", s(9, 15, 16, 20, 21))))

P(dict(kind=["order"], title="버튼 하나가 화면을 바꾸기까지 (리컴포지션 5단계)",
parts=[
 dict(q="Turtle Screen에서 'Up' 버튼을 눌렀을 때 일어나는 일을 순서대로 나열하시오. ⓐ Compose runtime이 방금 바뀐 상태(trail, offsetY)를 읽고 있던 컴포저블을 감지 ⓑ 화면 갱신 완료 ⓒ onUp 콜백 실행: leaveFootprint() 호출로 trail에 새 항목 추가, offsetY 변경 ⓓ 'Up' 버튼 클릭 ⓔ 해당 컴포저블만 다시 실행(리컴포지션)",
      a="ⓓ → ⓒ → ⓐ → ⓔ → ⓑ"),
 dict(q="위 ⓔ 단계에서 다시 실행되는 것 3가지는?",
      a="offsetY를 읽는 <b>animateDpAsState</b>(animatedY 재계산) / trail을 읽는 <b>trail.forEach{}</b>(Footprint들 다시 그림) / animatedY를 읽는 <b>Turtle()</b>(새 위치에서 다시 그림)",
      why="<p>\"<b>읽는 쪽만</b> 다시 실행된다\"가 핵심. offsetY를 읽지 않는 TopAppBar나 버튼은 다시 실행되지 않는다(2장 문제 8의 \"다시 그려야 할 부분만\"). 연쇄를 따라가면 순서가 나온다: offsetY → (읽는) animateDpAsState → animatedY → (읽는) Turtle.</p>")],
quote=quote("해당 컴포저블만 다시 실행시키는 리컴포지션이 시행됩니다.", s(23))))

KEYWORDS = [
 ("rememberSaveable", "remember와 동일하게 recomposition 사이에 값을 유지하되, 추가로 Activity/Process 재생성 시에도 값을 보존하는 Compose 상태 저장 함수", s(3)),
 ("configuration change (설정 변경)", "화면 회전, 다크 모드 전환, 시스템 언어 변경, 멀티 윈도우 크기 조정 등 Activity 자체가 파괴되고 다시 생성되는 상황", s(3)),
 ("Bundle", "시스템이 프로세스 간 또는 컴포넌트 간에 데이터를 안전하게 주고받을 수 있도록 설계된 Key-value 쌍 형태의 컨테이너 클래스", s(3)),
 ("Saver", "Bundle이 기본 지원하지 않는 복잡한 custom 타입의 직렬화/역직렬화 규칙을 정의하는 인터페이스", s(3)),
 ("mutableFloatStateOf", "Float 값을 담는 변경 가능한 상태(Bundle 지원 타입이라 rememberSaveable에 쓸 수 있음)", s(5)),
 ("Cold boot", "에뮬레이터의 이전 상태를 전혀 참고하지 않고 완전히 처음부터 새로 부팅하는 방식. 먹통이 된 상태를 정리할 때", s(8)),
 ("quick boot", "직전 종료 시 상태를 snapshot으로 저장했다가 다음 부팅 시 빠르게 띄우는 방식", s(8)),
 ("data class FootprintData", "발자국 하나의 x, y와 회전 각도(angle)를 담는 데이터 클래스", s(13)),
 ("listSaver (trailSaver)", "rememberSaveable과 함께 쓸 커스텀 Saver. 저장할 때 원시 리스트로 바꾸고 복원할 때 어떤 타입으로 되돌릴지 알려 줌", s(13)),
 ("flatMap", "각 FootprintData를 3개의 list로 푼 뒤 하나의 평평한 Float 리스트로 이어 붙임(save)", s(13)),
 ("chunked(3)", "평평한 Float 리스트를 3개짜리 묶음(chunk)으로 나눔(restore)", s(13)),
 ("mutableStateListOf / SnapshotStateList", "리스트 자체가 Compose의 state가 되도록 만들어 주는 특수한 리스트 / 그 타입. 값이 바뀔 때 UI가 자동으로 다시 그려짐", s(10, 13)),
 ("leaveFootprint()", "거북이가 이동하기 직전의 위치를 trail에 추가하는 함수. 네 버튼의 반복 로직을 한곳에 모아 재사용", s(12)),
 ("rotationAngle", "거북이의 방향. 오른쪽 기준 0f, 위 −90f, 아래 90f, 왼쪽 180f", s(14)),
 ("graphicsLayer(rotationZ = …)", "컴포저블을 지정한 각도만큼 회전시키는 Modifier(거북이·발자국 방향)", s(15, 21)),
 ("animateFloatAsState", "Float 값을 부드럽게 애니메이션하는 함수(animateDpAsState의 Float판)", s(16)),
 ("trail.forEach{}", "발자국 위치 리스트를 순회하며 Footprint를 하나씩 그림", s(20)),
]

OUTRO = """
<h3>3장 범위 대조표 — 슬라이드 → 문제</h3>
""" + table(["슬라이드", "내용", "문제"], [["s2", "다룬 영역", "1"], ["s3~4", "rememberSaveable·Bundle", "2"], ["s4~8", "Dp→Float 수정·Cold Boot", "3"],
 ["s10~13", "data class·listSaver", "4"], ["s12, 14, 17~19", "leaveFootprint·변수", "5"], ["s9, 15~16, 20~22", "회전·Footprint·Box 순서", "6"], ["s23", "리컴포지션 5단계", "7"]]) + """
<div class="note"><b>뺀 슬라이드</b>: s1 표지.</div>
<div class="note"><b>원본 주의</b>: s10·s20 설명은 발자국을 Pair&lt;Float, Float&gt; 리스트로 말하지만, 실제 코드(s11·s21)는 FootprintData(x, y, angle)를 쓴다(이전 판 설명이 남은 것으로 보임). s4 "(0.f)"는 0f, "단, 을 사용할 때는"은 원문 그대로(rememberSaveable이 빠진 것으로 보임).</div>
"""
