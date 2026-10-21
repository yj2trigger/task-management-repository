"""6장 ppa6 — Activity: 이벤트 로깅·생명주기·상태 저장·리소스·대체 리소스·Coil."""
from qbook2 import s as _s, quote, table, fill, slide


def s(*n):
    return _s(*n, deck="ppa6")


INTRO = """
<div class="note">소문제를 풀고 → 바로 아래 <b>답·해설</b>. 이중선(옅은 배경) = 문제, 가는 실선 = 답·해설, 굵은 실선 = 원문(원본 ppa6 슬라이드 번호·쪽 위/아래), 점선 = 해설 정리.
앞 장에서 이미 물은 지식은 다시 묻지 않고 "→ N장 문제 M"으로 잇습니다. Logcat 기초는 1장 문제 21, 회전 생명주기는 1장 문제 18·19, remember/rememberSaveable은 3장 문제 2.</div>
<h2>6장. ppa6 — Activity: 이벤트 로깅·생명주기·상태 저장·리소스·대체 리소스·Coil</h2>
"""

ITEMS = []
P = ITEMS.append

# 1
P(dict(kind=["name", "order"], title="이벤트 로깅과 Log 클래스의 동작 원리",
parts=[
 dict(q="이벤트 로깅을 정의하고, 원문이 든 비유와 이벤트 로깅의 가치를 쓰시오. 안드로이드 앱 테스트 중 문제가 생기면 무엇을 최우선으로 관찰하나?",
      a="이벤트 로깅은 발생하는 이벤트(사건)를 어딘가에 <b>기록</b>하는 행위다. 항공기 사고 때 <b>블랙박스</b>로 원인을 밝히듯, 기록을 나중에 언제든 살펴볼 수 있어 문제점을 찾을 수 있다(액티비티 내부 동작 파악, 문제 원인 찾기). 앱 테스트 중 문제가 생기면 <b>로그 메시지</b>를 최우선으로 관찰한다."),
 dict(q="안드로이드에서 로그 메시지가 저장되고 읽히는 경로를 순서대로 쓰시오: logcat 명령 / Log 버퍼 / 안드로이드 앱 / Log 클래스의 메서드. 로그 버퍼는 누가 무엇을 통해 제공하나?",
      a="안드로이드 앱 → Log 클래스의 메서드 → Log 버퍼 → logcat 명령(으로 읽음). 로그 버퍼는 리눅스 커널이 <b>로그 드라이버</b>를 통해 제공하는 메모리 영역이다.",
      why="<p>로그 버퍼가 리눅스 커널에 있다는 것은 1장 문제 1의 5계층에서 가장 아래 계층이라는 뜻이다. 앱은 맨 위에서 기록하고, logcat이 아래에서 꺼내 읽는다.</p>"),
 dict(q="로그 버퍼에 로그가 계속 쌓이면 어떻게 되나? 로그 버퍼에 저장된 내용을 보거나 지우려면? Log 클래스의 메서드는 어떤 종류의 메서드라서 <code>Log.e(\"my tag\", …)</code>처럼 바로 부를 수 있나? Log 메서드의 첫째·둘째 인자에 주로 넣는 것은?",
      a="로그 버퍼는 크기가 한정되어 있어 새 내용이 기록되면 <b>오래된 내용부터 덮어쓴다</b>. 로그 버퍼의 내용을 보거나 지우려면 Logcat 명령을 쓴다. Log 클래스의 메서드는 모두 <b>정적 메서드</b>라 객체를 만들지 않고 클래스 이름으로 호출한다. 첫째 인자에는 앱 이름이나 자바 클래스 이름(tag), 둘째 인자에는 로그 메시지 자체를 넣는다.",
      why="<p>로그 버퍼를 덮어쓴다(순환 버퍼)는 것은 1장 문제 21에서 이미 나왔다. 이 문제에서 새로운 것은 <b>누가 로그 버퍼를 제공하나</b>(커널의 로그 드라이버)와 Log 메서드가 <b>정적 메서드</b>라는 점이다.</p>")],
fig=slide("ppa6", 3, 80),
quote=quote("안드로이드 시스템의 기반 OS 인 리눅스 커널은 로그 드라이버를 통해 로그 메시지를 저장하는 메모리영역인 로그 버퍼(Log buffer)를 제공한다.", s(2, 3, 4))))

# 2
lv_q, lv_a = fill(["우선순위", "Log 메서드", "레벨"], [
    ["1(가장 높음)", ("?", "wtf"), ("?", "assert")], ["2", ("?", "e"), ("?", "error")], ["3", ("?", "w"), ("?", "warn")],
    ["4", ("?", "i"), ("?", "info")], ["5", ("?", "d"), ("?", "debug")], ["6(가장 낮음)", ("?", "v"), ("?", "verbose(상세 정보)")]])
P(dict(kind=["order", "name"], title="로그 레벨의 우선순위",
parts=[
 dict(q="Log 메서드 6개(d, e, i, v, w, wtf)를 우선순위가 높은 것부터 나열하고 각 레벨 이름을 쓰시오." + lv_q, a=lv_a,
      why="<p>로그 레벨 순서 기억법: \"<b>심각할수록 위</b>\" — 단언 실패(assert) &gt; 오류 &gt; 경고 &gt; 정보 &gt; 디버그 &gt; 상세. 개발 중 확인(d)과 상세 추적(v)이 가장 아래인 이유는 배포 때 지워도 되는 로그라서다(1장 문제 21의 BuildConfig.DEBUG로 지우는 Log.d).</p>"),
 dict(q="원본 s5에 \"wrf\"로 적힌 Log 메서드의 바른 이름과 레벨은?",
      a="Log 메서드의 바른 이름은 <b>wtf</b>이고 레벨은 assert다 <span class=\"fix\">(원본 \"wrf\"는 오타)</span>."),
 dict(q="Android Studio에서 Logcat 창을 여는 두 가지 방법은? Logcat 화면에서 메시지의 우선순위를 보여 주는 열과, 로그를 지우는 버튼은?",
      a="Logcat 창은 View &gt; Tool Windows &gt; Logcat 또는 왼쪽 하단 사이드 바의 고양이 아이콘으로 연다. Logcat 화면의 우선순위 열은 W, E, D, I 같은 한 글자로 표시되고, 로그는 휴지통 모양의 로그 메시지 지우기 버튼으로 지운다.")],
quote=quote("wrf(string tag, string message) : assert 메시지를 로그 버퍼에 보내는 기능을 한다. e(string tag, string message): error 메시지를 로그 버퍼에 보내는 기능을 한다", s(5, 6))))

# 3
so_q, so_a = fill(["System.out / System.err", "Java", "Android"], [
    ["출력이 가는 곳", ("?", "실행 중인 터미널·명령 프롬프트·IDE 콘솔 창에 직접 텍스트로"), ("?", "기본 상태에서는 /dev/null로 버려져 화면에 안 보임, 런타임이 가로채 Logcat에 stdout, stderr 태그로 남김")],
    ["주로 쓰는 곳", ("?", "콘솔 앱, 서버 백엔드, 간단한 테스트의 표준 입출력·에러 확인"), "—"],
    ["권장되는 방법", "System.out / System.err", ("?", "표준 입출력 대신 android.util.Log(레벨별 Log.v/d/i/w/e, tag로 필터링)")]])
P(dict(kind=["table", "diag"], title="System.out / System.err: Java와 Android",
parts=[
 dict(q="System.out / System.err를 Java와 Android에서 비교하시오." + so_q, a=so_a),
 dict(q="안드로이드 앱에서 <code>System.out.println(\"hi\")</code>를 했더니 화면 어디에도 안 보인다. 그 출력은 어디로 갔고, 어디서 찾을 수 있나?",
      a="안드로이드 앱의 System.out 출력은 /dev/null로 버려지지만 런타임이 가로채 Logcat에 stdout 태그로 남긴다 → Logcat에서 tag stdout으로 찾는다.",
      why="<p>/dev/null은 유닉스 계열의 \"버리는 곳\"이다(보충). 안드로이드 앱에는 콘솔 창이 없다는 점에서 출발하면 표가 풀린다: 콘솔이 없으니 표준 출력은 갈 곳이 없고, 그래서 Logcat이 대신 받는다.</p>")],
quote=quote("Android(system.out/system.err): 기본 상태에서는 출력이 /dev/null 로 버려져 화면에 보이지 않지만, 런타임이 이를 가로채어 Logcat 에 stdout, stderr 태그로 남겨집니다.", s(7))))

# 4
st_q, st_a = fill(["상황", "액티비티 상태"], [
    ["앱을 보며 버튼을 누르는 중", ("?", "Resumed")], ["반투명 대화상자가 화면 전체를 덮었지만 뒤의 화면이 비쳐 보임", ("?", "Paused(반투명이라 보임)")],
    ["다른 앱이 화면을 완전히 가림", ("?", "Stopped")], ["다른 액티비티가 화면 일부만 가림", ("?", "Paused")]])
P(dict(kind=["table", "diag"], title="Activity의 세 가지 상태",
parts=[
 dict(q="액티비티의 생명주기를 정의하시오. 액티비티의 상태 3가지 이름(영문)과 뜻을 쓰시오.",
      a="액티비티의 생명주기는 액티비티가 생성에서 종료까지 가지는 여러 상태 전체다. Resumed(실행 재개): 액티비티가 화면 맨 앞에서 사용자와 상호작용하는 상태 / Paused(일시 정지): 다른 액티비티가 부분만 가리거나 반투명 액티비티가 부분 또는 전체를 가려 <b>현재 액티비티가 보이는</b> 상태 / Stopped(중단): 다른 액티비티가 완전히 가려 현재 액티비티가 <b>보이지 않는</b> 상태"),
 dict(q="상황에 맞는 액티비티 상태를 쓰시오." + st_q, a=st_a,
      why="<p>Paused와 Stopped의 경계는 \"<b>현재 액티비티가 보이나?</b>\"다. 가린 정도(일부/전체)가 아니라 보이는지로 판단한다 — 반투명이 전체를 덮어도 비쳐 보이면 Paused(두 번째 줄이 함정).</p>"),
 dict(q="시스템 메모리가 부족할 때 강제 종료될 수 있는 액티비티 상태는? 원문이 Paused 상태에 붙인 조건은?",
      a="Paused와 Stopped 둘 다 강제 종료될 수 있다. 원문은 Paused 상태가 가용 메모리가 <b>매우</b> 부족할 때 강제 종료될 수 있다고 조건을 붙였다.",
      why="<p>액티비티가 덜 보일수록 강제 종료 가능성이 크다: Paused는 메모리가 \"매우\" 부족할 때만, Stopped는 \"부족하면\".</p>")],
quote=quote("일시 정지 (Paused): 다른 액티비티가 부분만 가리거나, 반투명 액티비티가 부분 혹은 전체를 가려서, 현재 액티비티가 보이는 상태이다.", s(8))))

# 5
lf_q, lf_a = fill(["생애", "시작 ~ 끝 콜백", "대응하는 상태"], [
    ["전체 생애(entire lifetime)", ("?", "onCreate() ~ onDestroy()"), ("?", "생성부터 종료까지 전부")],
    ["가시 생애(visible lifetime)", ("?", "onStart() ~ onStop()"), ("?", "보이는 동안(Resumed + Paused)")],
    ["전면 생애(foreground lifetime)", ("?", "onResume() ~ onPause()"), ("?", "맨 앞에서 상호작용(Resumed)")]])
P(dict(kind=["table", "name"], title="콜백 메서드와 세 가지 생애",
parts=[
 dict(q="액티비티의 콜백 메서드를 원문의 표현으로 정의하시오.",
      a="액티비티의 상태가 변할 때마다 안드로이드 시스템이 액티비티 클래스의 <b>약속된 메서드를 호출</b>하는데, <b>운영체제가 응용 프로그램 코드를 호출</b>한다고 해서 이 메서드를 콜백 메서드라고 부른다.",
      why="<p>1장 문제 20의 콜백 일반 정의(개발자가 함수를 넘기면 시스템이 적절한 때 호출)와 같은 말을 운영체제 관점에서 한 것이다.</p>"),
 dict(q="액티비티의 세 생애의 시작·끝 콜백과, 각 생애가 대응하는 액티비티 상태를 쓰시오." + lf_q, a=lf_a,
      why="<p>생명주기 콜백 짝 맞추기: Create↔Destroy, Start↔Stop, Resume↔Pause. 이름이 반대말끼리 짝이라 바로 외워진다. \"가시(visible)\"는 보이는 동안이라 Paused까지 포함, \"전면(foreground)\"은 맨 앞이라 Resumed만이다(문제 4의 \"보이나?\" 기준).</p>"),
 dict(q="\"액티비티의 가시 생애가 전면 생애보다 길다\"는 옳은가?",
      a="옳다. 전체 생애 ⊃ 가시 생애 ⊃ 전면 생애로, 가시 생애(onStart~onStop) 안에 전면 생애(onResume~onPause)가 들어 있다.")],
quote=quote("안드로이드 시스템은 액티비티의 상태가 변할 때 마다, 액티비티 클래스의 약속된 메서드를 호출한다. 이를 운영체제가 응용 프로그램 코드를 호출한다고 해서, 콜백 메서드(callback method)라고 부른다.", s(9))))

# 6
lc_q, lc_a = fill(["상황", "호출되는 콜백(순서대로)"], [
    ["앱을 처음 실행해 화면이 뜰 때까지", ("?", "onCreate → onStart → onResume")],
    ["다른 액티비티가 맨 앞으로 나왔다가(일부만 가림) 사용자가 다시 돌아옴", ("?", "onPause → (돌아옴) onResume")],
    ["다른 앱이 화면을 완전히 가렸다가 사용자가 다시 돌아옴", ("?", "onPause → onStop → (돌아옴) onRestart → onStart → onResume")],
    ["가려진(Stopped) 동안 우선순위가 높은 앱이 메모리를 요구해 앱 프로세스가 강제 종료되었고, 그 뒤 사용자가 돌아옴", ("?", "(onPause → onStop) → 프로세스 강제 종료(콜백 없음) → (돌아옴) onCreate → onStart → onResume(처음부터 다시)")],
    ["실행 중인 액티비티가 스스로 종료하거나 시스템이 강제 종료시킬 때", ("?", "onPause → onStop → onDestroy")]])
P(dict(kind=["order", "diag"], title="생명주기 도식 따라가기",
parts=[
 dict(q="액티비티 생명주기 도식(아래 그림)의 경로를 따라 호출되는 콜백을 순서대로 쓰시오." + lc_q, a=lc_a,
      why="<ol><li>액티비티가 돌아오는 지점은 \"<b>어디까지 내려갔었나</b>\"로 정해진다: onPause까지만 → onResume으로 복귀 / onStop까지 → onRestart → onStart / 프로세스가 죽음 → onCreate부터.</li>"
          "<li>프로세스 강제 종료 후 복귀는 1장 문제 19와 같은 사건이다(그때 onCreate의 savedInstanceState가 null이 아님) — 그래서 문제 8의 상태 저장이 필요하다.</li></ol>"),
 dict(q="액티비티 생명주기에서 \"Stopped였다가 다시 돌아올 때만\" 불리는 콜백은?",
      a="<b>onRestart()</b> — 액티비티가 onStop까지 내려갔다가 사용자가 돌아올 때만 onStart 앞에서 호출된다.")],
fig=slide("ppa6", 10, 75)))

# 7
P(dict(kind=["mc"], title="안드로이드가 액티비티를 자동으로 재생성하는 경우",
parts=[
 dict(q="원문이 든 \"안드로이드가 액티비티를 자동으로 재생성하는 경우\"가 <b>아닌</b> 것을 모두 고르시오.",
      opts=[("기기를 회전해 화면 방향을 전환", True, "기기 회전으로 화면 방향이 바뀌면 안드로이드가 액티비티를 자동으로 재생성한다(원문 목록에 있음)."),
            ("시스템의 언어·글꼴 크기·디스플레이 크기 변경", True, "시스템 언어·글꼴 크기·디스플레이 크기를 바꾸면 액티비티가 자동 재생성된다(원문 목록에 있음)."),
            ("배터리 잔량이 20% 아래로 떨어짐", False, "배터리 잔량 변화는 화면 구성을 바꾸지 않아 원문의 자동 재생성 목록에 없다."),
            ("기기 출력을 TV 같은 외부 디스플레이로 보냄", True, "외부 디스플레이로 출력을 보내면 액티비티가 자동 재생성된다(원문 목록에 있음)."),
            ("도킹 장치에 연결하거나 제거", True, "도킹 장치를 연결·제거하면 액티비티가 자동 재생성된다(원문 목록에 있음)."),
            ("Wi-Fi 연결이 끊김", False, "Wi-Fi(네트워크) 연결 변화는 화면 구성을 바꾸지 않아 원문의 자동 재생성 목록에 없다."),
            ("외장 키보드 연결", True, "외장 키보드를 연결하면 액티비티가 자동 재생성된다(원문 목록에 있음)."),
            ("슬라이드 자판을 꺼내거나 집어넣음", True, "슬라이드 자판을 꺼내거나 넣으면 액티비티가 자동 재생성된다(원문 목록에 있음)."),
            ("기기가 켜진 상태에서 SIM 카드를 교체해 통신사 변경", True, "켜진 기기에서 SIM 카드를 바꿔 통신사가 바뀌면 액티비티가 자동 재생성된다(원문 목록에 있음)."),
            ("알림이 도착함", False, "알림 도착은 화면 구성을 바꾸지 않아 원문의 자동 재생성 목록에 없다.")],
      a="ⓒ ⓕ ⓙ",
      why="<p>자동 재생성 목록의 공통점은 화면·입력·언어처럼 <b>리소스를 다시 골라야 하는 구성(configuration) 변화</b>라는 것이다(문제 11의 대체 리소스와 같은 이유, 3장 문제 2의 configuration change). 배터리·네트워크·알림은 화면 구성을 바꾸지 않는다.</p>"),
 dict(q="백 버튼으로 액티비티를 끝낼 때와 회전으로 액티비티가 재생성될 때, 사용자가 기대하는 것의 차이는? 그래서 필요한 두 가지 작업은?",
      a="백 버튼은 앱을 <b>완전히 종료</b>하는 것이지만, 회전은 액티비티가 <b>일시적으로</b> 종료 후 재생성되는 것이라 사용자는 상태가 유지되기를 바란다. 그래서 액티비티 상태를 <b>저장</b>하고 <b>복원</b>해야 한다.")],
quote=quote("안드로이드가 액티비티를 자동으로 재생성하는 경우를 알아보면 보통 다음과 같다.", s(11))))

# 8
ss_q, ss_a = fill(["SaveState 앱 실험", "결과"], [
    ["count++의 뜻", ("?", "count = count + 1")],
    ["remember로 10번 누른 뒤 가로로 회전하면 표시되는 수", ("?", "0(초기화)")],
    ["rememberSaveable로 바꾸고 같은 실험", ("?", "10(유지)")],
    ["버튼과 글자를 한 줄에 두고 세로 가운데로 맞추는 컨테이너와 파라미터", ("?", "Row(verticalAlignment = Alignment.CenterVertically)")],
    ["이 줄을 화면 왼쪽 위에 두는 Modifier", ("?", "Modifier.align(Alignment.TopStart)")]])
P(dict(kind=["diag", "calc"], title="액티비티 상태 저장: 무엇이 자동이고 무엇을 직접 하나",
parts=[
 dict(q="화면을 회전하면 EditText에 입력한 글자는 그대로 남는다. 왜인가? 위젯 상태 자동 복원의 조건은? 위젯 상태 외의 데이터는?",
      a="액티비티가 재생성되면 화면을 유지하는 대부분의 위젯 상태를 안드로이드 시스템이 저장했다가 자동으로 복원해 준다. 레이아웃의 위젯에 <b>id를 부여</b>해야 위젯 상태가 유지된다. 위젯 상태 외의 데이터는 저장·복원 코드를 직접 작성해야 한다.",
      why="<p>위젯에 id를 줘야 자동 복원되는 이유: 다시 만들어진 위젯 중 \"누가 누구인지\" 짝을 맞출 이름이 필요하기 때문이다(보충 추론).</p>"),
 dict(q="시스템이 회전 등으로 액티비티를 종료하기 <b>전에</b> 자동으로 호출하는 메서드와, 그 인자로 데이터를 저장하는 방법은? 그 인자 객체가 제공하는 메서드의 형태는?",
      a="<code>onSaveInstanceState()</code>. 인자로 전달된 <b>Bundle</b> 객체에 put() 메서드를 호출해 데이터를 저장한다. Bundle은 키와 값을 주어 저장하거나 키를 주고 값을 읽는 다양한 유형의 메서드를 제공한다.",
      why="<p>Bundle이 이 과목에 세 번 나온다: 1장 문제 19(프로세스 재생성 시 savedInstanceState), 3장 문제 2(rememberSaveable의 저장소), 이 문제(onSaveInstanceState의 put). <b>모두 같은 Bundle</b>이다 — View 방식은 onSaveInstanceState로 직접 넣고, Compose는 rememberSaveable이 대신 넣어 준다.</p>"),
 dict(q="SaveState 앱(<code>var count by remember { mutableStateOf(0) }</code>, 버튼 <code>onClick = { count++ }</code>, 글자 \"클릭한 수: $count\")으로 실험한 결과를 채우시오." + ss_q, a=ss_a)],
quote=quote("안드로이드 시스템은 화면 회전 등으로 액티비티가 종료되기 전에 onSaveInstanceState() 메서드를 자동으로 호출한다. 이 때, 인자로 전달된 Bundle 객체에 대해 put() 메서드를 호출하면, 데이터를 저장할 수 있다.", s(12, 13, 14, 15, 16, 17))))

# 9
rs_q, rs_a = fill(["res 기본 리소스", "용도·Compose에서의 쓰임"], [
    ["string / string array", ("?", "다국어 지원(번역)·텍스트 중앙 관리. res/values/strings.xml에 저장, stringResource(R.string.text_id)로 사용")],
    ["XML-drawable", ("?", "vector graphic: 앱 내 아이콘·도형 등 그래픽 요소")],
    ["animation", ("?", "화면 전환·컴포넌트 애니메이션을 Compose 자체 애니메이션 API로")],
    ["menu", ("?", "Composable에서는 dropdown 메뉴나 layout 컴포넌트로 직접 구현")]])
nl_q, nl_a = fill(["설명", "이름"], [
    ["XML drawable 아이콘 대신 구글의 최신 벡터 아이콘 팩을 코드 한 줄로", ("?", "Google Material Symbols &amp; Icons")],
    ["After Effects로 만든 애니메이션을 JSON 파일 하나로 내보내 앱에서 그대로 재생(로딩 화면, 축하 폭죽)", ("?", "Lottie")],
    ["브랜드 메인 색 하나로 다크·라이트 모드 색 조합을 코드로 뽑아 Color.kt/Theme.kt로 받는 구글 공식 도구", ("?", "Material Theme Builder")],
    ["Web URL 이미지나 로컬 리소스를 비동기로 최적화해 로딩하는 최신 이미지 로딩 라이브러리", ("?", "Coil(Compose Extension)")],
    ["구글 안드로이드 팀이 관리하는 Jetsnack, Jetchat 같은 샘플 앱 모음", ("?", "Google Compose Samples(GitHub 공식 저장소)")]])
P(dict(kind=["table", "name"], title="기본 리소스와 새 리소스·라이브러리",
parts=[
 dict(q="res의 기본 리소스의 용도와 Compose에서의 쓰임을 채우시오. 최근 잘 쓰지 않는 기본 리소스 두 가지는?" + rs_q,
      a=rs_a + "최근 잘 쓰지 않는 기본 리소스: bitmap drawable, 9-patch drawable"),
 dict(q="설명에 맞는 새 리소스·라이브러리 이름을 쓰시오." + nl_q, a=nl_a,
      why="<p>새 리소스·라이브러리는 \"<b>무엇을 대신하나</b>\"로 구분한다: 아이콘 파일 → Material Icons, 애니메이션 파일 → Lottie(JSON), 색 정의 → Theme Builder, 이미지 로딩 → Coil, 코드 예제 → Samples.</p>"),
 dict(q="Material Icons 확장 팩과 Lottie를 쓰려면 build.gradle.kts에 넣는 implementation 문자열은 각각?",
      a="Material Icons 확장: <code>\"androidx.compose.material:material-icons-extended\"</code> / Lottie: <code>\"com.airbnb.android:lottie-compose:6.4.0\"</code>",
      why="<p>Material Icons 확장의 implementation 문자열은 2장 문제 14(dependency 오류 해결)에서 넣은 줄과 같다.</p>")],
quote=quote("Lottie 라이브러리: 시각 전문 프로그램인 에펙 (After Effect)로 만든 화려한 애니메이션을 JSON 파일 하나로 내보내면, 앱에서 그대로 재생성해주는 리소스 환경으로, 앱의 로딩화면이나 축하 폭죽 등에 필수 적입니다.", s(18, 19, 20, 21))))

# 10
P(dict(kind=["diag", "name"], title="문자열 리소스 strings.xml",
parts=[
 dict(q="문자열을 코드에 직접 넣는 대신 문자열 리소스를 쓰는 이점 두 가지는? 문자열 리소스를 정의하는 파일의 위치와 파일 이름 규칙은?",
      a="문자열 리소스를 쓰면 문자열 값을 바꾸기 편하고, 다국어 지원을 표현하기 편하다. 문자열 리소스는 <code>res/values/파일명.xml</code>에 정의한다(파일명은 자유지만 관례상 strings)."),
 dict(q="strings.xml 작성: ⓐ <code>&lt;string&gt;Hello&lt;/string&gt;</code>처럼 썼더니 오류가 났다. 빠진 것은? ⓑ 프로젝트를 만들 때 자동으로 생기는 문자열 이름은? ⓒ <code>I'll be back!</code>과 <code>This is a \"good thing\"</code>을 넣으려면? ⓓ 굵게·밑줄·기울임을 주는 태그는? ⓔ XML에서 string_example1을 참조하는 형식과 Compose 코드에서 참조하는 형식은?",
      a="ⓐ string 요소에 반드시 필요한 <b>name 속성</b>이 빠졌다. ⓑ app_name ⓒ 따옴표 앞에 백슬래시를 붙인다: <code>I\\'ll be back!</code>, <code>This is a \\\"good thing\\\"</code> ⓓ 굵게 &lt;b&gt;&lt;/b&gt; / 밑줄 &lt;u&gt;&lt;/u&gt; / 기울임 &lt;i&gt;&lt;/i&gt; ⓔ XML: <code>@string/string_example1</code>(리소스명 = string의 name), Compose: <code>stringResource(R.string.string_example1)</code>",
      why="<p>문자열 리소스 하나는 <code>&lt;string name=\"이름\"&gt;값&lt;/string&gt;</code>이다. 2장 문제 3의 XML 용어로 쓰면 element(string), 속성(name), text data(값).</p>"),
 dict(q="Android Studio 프로젝트 창에서 strings.xml이 패키지(com.example.savestate) 아래에 있는 것처럼 보였다. 무엇 때문이며, strings.xml의 실제 경로는? Android 뷰 모드는 이 경로를 어떻게 보여 주나?",
      a="프로젝트 창의 드롭다운이 <b>Packages</b> 뷰 모드라서, 실제 폴더와 관계없이 패키지 구조 중심으로 재구성해 보여 준 것이다. strings.xml의 실제 경로는 <code>app/src/main/res/values/strings.xml</code>이다. Android 뷰 모드는 복잡한 경로를 숨기고 res &gt; values &gt; strings.xml로 압축해 보여 준다(실제 디스크 구조와 다름).",
      why="<p>Android 보기가 실제 구조가 아니라는 것은 1장 문제 13에서 나왔고, 이 문제에서 새로운 지식은 Packages 뷰 모드가 일으키는 착각이다.</p>")],
quote=quote("만약 문자열에 작은 따옴표나 큰 따옴표가 있다면, 백슬래시(\\)를 붙여 주어야 한다.", s(22, 23, 24))))

# 11
q_q, q_a = fill(["상황", "대체 리소스 폴더 이름(수식어)"], [
    ["한국어 사용자에게 한국어 문자열", ("?", "values-ko")], ["한국어 + 대한민국 지역에만", ("?", "values-ko-rKR")],
    ["가로 화면 전용 이미지", ("?", "drawable-land")], ["세로 화면 전용 이미지", ("?", "drawable-port")],
    ["화면 밀도와 관계없이 비트맵을 원래 크기로", ("?", "drawable-nodpi")], ["고밀도(hdpi) 화면용 이미지", ("?", "drawable-hdpi")],
    ["화면 폭이 820dp 이상인 기기", ("?", "-w820dp(원본 표기 \"-820dp\")")], ["안드로이드 2.2(플랫폼 버전)", ("?", "-v8")]])
P(dict(kind=["table", "diag"], title="대체 리소스와 수식어(한정자)",
parts=[
 dict(q="대체 리소스를 정의하시오. 대체 리소스에서 개발자가 할 일과 시스템이 하는 일은?",
      a="대체 리소스는 시스템의 구성 변화(화면 회전, 언어 변경 등)에 대응하도록 기본 리소스 외에 준비하는 리소스다. 개발자는 리소스 이름(폴더)에 <b>특별한 수식어</b>를 붙여 정의만 하고, 어떤 리소스를 고를지는 <b>안드로이드 시스템이 자동으로</b> 처리한다."),
 dict(q="상황에 맞는 대체 리소스 폴더 이름(수식어)을 쓰시오." + q_q, a=q_a,
      why="<p>대체 리소스 폴더 이름 = <b>리소스 종류-수식어</b>(values-ko, drawable-land). 2장 문제 2의 \"res 하위 폴더 이름이 넣을 수 있는 리소스 종류를 정한다\"에 수식어가 하나 더 붙은 꼴이다.</p>"),
 dict(q="언어·지역 수식어의 규칙(글자 수, r의 역할, 생략)은? 밀도 수식어의 가장 낮은 것과 가장 높은 것은? 버전 수식어 -v7은 안드로이드 몇 버전인가?",
      a="언어·지역 수식어는 두 글자 언어 코드 + 두 글자 지역 코드이고, 지역 코드 앞에 r을 붙이며, 지역은 생략할 수 있다(일치하면 그 리소스 선택). 밀도 수식어는 가장 낮은 -ldpi ~ 가장 높은 -xxxhdpi. -v7은 안드로이드 2.1이다.",
      why="<p>-v7 = 2.1, -v8 = 2.2: 버전 수식어의 숫자는 API 레벨이다(보충: API 7 = 2.1). 1장 문제 2의 API level 체계와 같다.</p>"),
 dict(q="drawable/, drawable-port/, drawable-land/에 dog3.jpg를 하나씩 두었다. 거의 정사각형인 폴더블 화면이라 시스템이 방향을 판별하지 못하면 어느 dog3.jpg를 쓰나? 그 폴더의 역할 이름은?",
      a="수식어가 붙지 않은 <code>drawable/dog3.jpg</code>를 쓴다. 이 기본 폴더의 역할은 <b>폴백(fallback)</b> — 예외 상황을 대비한 기본값이다.",
      why="<p>폴백이 반드시 있어야 하는 이유: 어떤 수식어에도 맞지 않는 기기가 와도 쓸 리소스가 있어야 앱이 깨지지 않는다. 그래서 같은 파일을 기본 폴더에도 둔다.</p>")],
quote=quote("시스템의 구성 변화에 대응하려면, 기본 리소스 외에 대체 리소스 (alternative resource)를 준비해야 한다. 특히, 리소스 이름에 특별한 수식어를 붙이고, 리소스를 정의하기만 하면, 나머지는 안드로이드 시스템이 자동으로 처리한다.", s(25, 26, 27, 41))))

# 12
P(dict(kind=["order", "diag"], title="Coil 설치와 이미지 넣기",
parts=[
 dict(q="Coil을 쓰기 위한 3단계를 순서대로 쓰고, 각 단계에서 무엇을 어디에 넣는지 쓰시오.",
      a="① AndroidManifest.xml: 네트워크 접근 권한과 평문 통신 허용 ② libs.versions.toml: coil 버전과 coil-compose, coil-network-okhttp 라이브러리 등록 ③ build.gradle.kts(Module: app)의 dependencies: <code>implementation(libs.coil.compose)</code>, <code>implementation(libs.coil.network.okhttp)</code> → Sync Now",
      why="<p>Coil 설치 3단계는 4장 문제 10(toml → build.gradle.kts → Sync → import) 앞에 <b>매니페스트 권한</b>이 붙은 것이다. Coil은 이미지를 인터넷에서 받아 올 수 있는 라이브러리라서 권한이 필요하다(1장 문제 12의 \"권한 거부 → Manifest\"와 연결).</p>"),
 dict(q="Coil을 위해 AndroidManifest.xml에 넣는 두 줄은 각각 무엇을 허용하나? 하나는 &lt;manifest&gt; 아래, 하나는 &lt;application&gt; 아래다.",
      a="&lt;manifest&gt; 아래 <code>&lt;uses-permission android:name=\"android.permission.INTERNET\" /&gt;</code>는 인터넷(네트워크) 접근 권한을, &lt;application&gt; 아래 <code>android:usesCleartextTraffic=\"true\"</code>는 암호화되지 않은(http) 통신을 허용한다(보충 설명)."),
 dict(q="libs.versions.toml의 [versions] coil = \"3.0.4\"와 [libraries]의 version.ref = \"coil\"의 관계는? 라이브러리를 toml에 등록하는 목적은?",
      a="[libraries]의 coil 라이브러리들이 쓰는 버전을 version.ref로 [versions]의 coil 항목(3.0.4)에서 참조한다. toml 등록의 목적은 여러 모듈에서 같은 라이브러리를 쓸 때 <b>버전을 한곳에서</b> 쉽게 관리하는 것이다."),
 dict(q="Coil 실습에서 배경 사진 파일을 넣는 절차(파일 이름 규칙, 넣을 폴더, 지원 형식)와, 그 폴더로 빨리 가는 방법은? 실습에서 비교한 두 가상 기기 Medium Phone과 Pixel 7의 화면 크기·해상도·밀도는?",
      a="배경 사진 파일 이름을 <b>영어 소문자와 숫자</b> 조합으로 바꿔 app/src/main/res/<b>drawable</b>에 복사·붙여넣는다(png, jpg, webp 지원). res/drawable 우클릭 → Open in → Explorer로 폴더에 빨리 간다. Medium Phone은 6.7인치(구글 UI 테스트용 표준 가상 기기), Pixel 7은 6.3인치(실제 하드웨어 모방)이고, 두 기기 모두 1080×2400(FHD+), 420dpi다.",
      why="<p>배경 사진 파일 이름 규칙은 2장 문제 2의 res 파일 이름 규칙(a~z, 0~9, _, .)과 같은 이유다.</p>")],
quote=quote("TOML 파일은 여러 모듈에서 같은 라이브러리를 쓸 때 버전을 한곳에서 쉽게 관리하는 것이 목적입니다.", s(28, 29, 30, 31, 32))
 + "<p><span class='fix'>원본 s29 \"AndroidMainfest.xml\" → AndroidManifest.xml / s28 \"Nexus 7(pixel 7)\" — 실습 기기는 Pixel 7</span></p>"))

# 13
cf_q, cf_a = fill(["비교", "ContentScale.Fit", "ContentScale.Crop"], [
    ["비율", ("?", "원본 비율 유지"), ("?", "원본 비율 유지")],
    ["채우는 방식", ("?", "이미지 전체가 다 보이도록 축소"), ("?", "컨테이너를 완전히 채울 때까지 확대, 넘치는 부분은 잘라냄")],
    ["여백", ("?", "남는 공간이 검은 여백(레터박스)으로 생김"), ("?", "생기지 않음")]])
P(dict(kind=["name", "table", "diag"], title="AsyncImage로 배경 깔기: Crop과 Fit",
intro="<code>AsyncImage(model = ImageRequest.Builder(LocalContext.current).data(R.drawable.dog3).build(), contentDescription = \"강아지 배경\", contentScale = ContentScale.Crop, modifier = modifier.fillMaxSize())</code> 다음에 <code>Box(Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.2f)))</code>, 그다음 <code>Box(Modifier.fillMaxSize().statusBarsPadding().padding(32.dp), contentAlignment = Alignment.TopCenter) { Text(\"환영합니다!\", color = White, fontSize = 24.sp, fontWeight = Bold) }</code>",
parts=[
 dict(q="강아지 배경 코드의 각 부분의 역할: ⓐ AsyncImage ⓑ ImageRequest.Builder(LocalContext.current) ⓒ .data(R.drawable.dog3) ⓓ .build() ⓔ modifier = modifier.fillMaxSize()",
      a="ⓐ AsyncImage는 Coil이 제공하는, 이미지를 <b>비동기로</b> 로드하고 화면에 그려 주는 컴포저블 ⓑ ImageRequest.Builder(LocalContext.current)는 화면의 context 정보를 가져와 이미지를 요청할 빌더 객체를 만든다 ⓒ .data(R.drawable.dog3)는 drawable에 넣은 이미지 파일명을 명시한다 ⓓ .build()는 설정한 요청 조건(context, 데이터 경로 등)을 조립해 AsyncImage가 읽을 요청 객체로 완성한다 ⓔ modifier = modifier.fillMaxSize()는 외부에서 넘겨받은 modifier 규칙을 이어받아 이미지가 화면 전체를 채우게 한다"),
 dict(q="Image의 ContentScale.Crop과 ContentScale.Fit을 비교하시오." + cf_q, a=cf_a,
      why="<p>Fit/Crop은 \"<b>무엇을 포기하나</b>\"로 구분한다: Fit은 화면을 일부 포기(여백), Crop은 사진을 일부 포기(잘림). 배경은 빈틈이 없어야 하므로 강아지 배경은 Crop을 쓴다.</p>"),
 dict(q="강아지 배경 위의 두 번째 Box(검은색 alpha 0.2)는 왜 넣나? 세 번째 Box의 statusBarsPadding(), padding(32.dp), contentAlignment의 효과는?",
      a="두 번째 Box는 화면 전체를 투명도 0.2의 검은색으로 덮어(overlay), 배경 사진 위에 넣는 글자의 <b>가독성</b>을 높인다. 세 번째 Box는 상태 표시줄 높이만큼 여백을 준 뒤 32dp를 더 띄우고, 그 영역의 위쪽 가운데(TopCenter)에 \"환영합니다!\" 글자를 놓는다.",
      why="<p>Box 세 개는 아래부터 겹친다(3장 문제 6: 먼저 쓴 자식이 아래) → 사진 → 어둡게 덮기 → 글자. statusBarsPadding은 2장 문제 13의 패딩 함수 중 하나다.</p>")],
quote=quote("ContentScale.Crop: 이미지 비율을 유지하되, 컨테이너를 완전히 채울 때까지 확대하고, 넘치는 부분은 잘라냅니다. 즉, 여백이 생기지 않게 됩니다.", s(33, 34, 35, 36, 37))))

# 14
P(dict(kind=["diag", "order"], title="가로로 돌리면 카메라 쪽이 비는 문제",
intro="처음 코드: <code>setContent { CoilExampleTheme { Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding -&gt; DogBackgroundScreen(modifier = Modifier.padding(innerPadding)) } } }</code>",
parts=[
 dict(q="강아지 배경 앱을 가로로 회전하자 카메라 부분에서 배경 사진이 화면 끝(edge)까지 채워지지 않았다. topBar도 bottomBar도 없는데 왜 생겼나? (2장의 display cutout 성질과 연결해 설명)",
      a="Scaffold는 topBar나 bottomBar가 없어도 edge-to-edge 환경에서 시스템 바(카메라 컷아웃 등)를 침범하지 않도록 <b>innerPadding을 계산해서 넘겨준다</b>. 이 innerPadding을 DogBackgroundScreen에 그대로 씌우니, 함수에 들어가는 순간 이미 시스템 영역만큼 안쪽으로 줄어든 좁은 영역이 전달됐다. 가로로 돌리면 display cutout이 상태 표시줄에 흡수되지 않고 화면 옆쪽에 따로 나타나므로(2장 문제 13) 카메라 쪽이 비었다.",
      why="<p>세로와 가로에서 증상이 다른 이유가 바로 display cutout의 위치 변화다 — 2장 지식이 6장 실습에서 원인으로 회수된다.</p>"),
 dict(q="원본은 카메라 쪽 여백 문제를 어떻게 해결했나(setContent 안을 어떻게 바꿨나)? 그러면 왜 해결되나?",
      a="Scaffold를 제거하고 <code>CoilExampleTheme { DogBackgroundScreen() }</code>만 남겼다. 그러면 배경 이미지가 시스템 영역까지 포함한 화면 전체를 받는다(\"환영합니다!\" 글자는 따로 statusBarsPadding으로 시스템 영역을 피함).",
      why="<p>\"<b>배경은 끝까지, 내용은 안전하게</b>\"가 edge-to-edge의 원칙이다: 배경(사진)에는 패딩을 주지 않고, 가려지면 안 되는 내용(글자)에만 statusBarsPadding 같은 패딩을 준다. Scaffold의 innerPadding은 내용용인데 배경에 씌워서 문제가 생겼다.</p>"),
 dict(q="Android Studio에서 방향별 대체 리소스 폴더를 만드는 절차를 순서대로 쓰시오(메뉴, Resource type, qualifier, 결과 폴더 이름). 가로용 폴더도 같은 방법으로 만든 뒤 할 일은?",
      a="프로젝트 탭의 res에서 우클릭 → New → Android Resource Directory → Resource type에서 drawable → Available qualifiers에서 Orientation을 골라 화살표(&gt;&gt;)로 Chosen qualifiers로 옮김 → Screen orientation에서 Portrait → Directory name이 <b>drawable-port</b>가 된다. 같은 방법으로 drawable-land를 만든 뒤, 두 폴더에 drawable의 dog3.jpg를 복사한다.")],
fig=slide("ppa6", 38, 70) + slide("ppa6", 42, 70),
quote=quote("Scaffold{} 는 topBar 나 bottomBar 가 없어도, edge-to-edge 환경에서 시스템바(카메라 컷아웃 등)을 침범하지 않도록 innerPadding 값을 계산해서 넘겨주는데, 이 innerPadding 값을 DogBackgroundScreen() 함수에 그대로 씌우기 때문에", s(38, 39, 40, 41, 42, 43))))

KEYWORDS = [
 ("이벤트 로깅 (event logging)", "발생하는 이벤트(사건)를 어딘가에 기록하는 행위. 항공기 블랙박스에 비유", s(2)),
 ("로그 버퍼 (Log buffer)", "리눅스 커널이 로그 드라이버를 통해 제공하는, 로그 메시지를 저장하는 메모리 영역. 크기가 한정되어 오래된 것부터 덮어씀", s(3)),
 ("정적 메서드", "객체를 만들지 않고 클래스 이름으로 호출하는 메서드(Log 클래스의 메서드들)", s(4)),
 ("wtf / e / w / i / d / v", "Log 메서드 우선순위 순서: assert > error > warn > info > debug > verbose", s(5)),
 ("Logcat 창", "View > Tool Windows > Logcat 또는 왼쪽 하단 고양이 아이콘으로 여는 로그 확인 창", s(6)),
 ("/dev/null", "안드로이드에서 System.out/err 출력이 기본으로 버려지는 곳(런타임이 가로채 Logcat에 stdout·stderr 태그로 남김)", s(7)),
 ("android.util.Log", "안드로이드에서 표준 입출력 대신 권장되는 로그 클래스(레벨별, tag로 필터링)", s(7)),
 ("생명주기 (Life cycle)", "액티비티가 생성에서 종료까지 가지는 여러 상태 전체", s(8)),
 ("Resumed (실행 재개)", "액티비티가 화면 맨 앞에서 사용자와 상호작용하는 상태", s(8)),
 ("Paused (일시 정지)", "다른 액티비티가 부분만 가리거나 반투명 액티비티가 가려 현재 액티비티가 보이는 상태", s(8)),
 ("Stopped (중단)", "다른 액티비티가 완전히 가려 현재 액티비티가 보이지 않는 상태", s(8)),
 ("콜백 메서드 (callback method)", "액티비티 상태가 변할 때 운영체제가 응용 프로그램 코드(약속된 메서드)를 호출하는 것", s(9)),
 ("전체 생애 (entire lifetime)", "onCreate() ~ onDestroy()", s(9)),
 ("가시 생애 (visible lifetime)", "onStart() ~ onStop(). 액티비티가 보이는 동안", s(9)),
 ("전면 생애 (foreground lifetime)", "onResume() ~ onPause(). 액티비티가 맨 앞에서 상호작용하는 동안", s(9)),
 ("onRestart()", "Stopped였던 액티비티로 사용자가 돌아올 때만 onStart 앞에서 호출되는 콜백", s(10)),
 ("onSaveInstanceState()", "시스템이 회전 등으로 액티비티를 종료하기 전에 자동 호출하는 메서드. 인자로 받은 Bundle에 put()으로 저장", s(12)),
 ("Bundle", "키와 값을 주어 저장하거나 키로 값을 읽는 메서드를 제공하는 상태 저장 객체", s(12)),
 ("bitmap drawable / 9-patch drawable", "최근 잘 쓰지 않는 res 기본 리소스", s(18)),
 ("stringResource(R.string.…)", "Compose에서 문자열 리소스를 읽는 함수", s(18)),
 ("Google Material Symbols & Icons", "XML drawable 아이콘 대신 쓰는 구글의 최신 벡터 아이콘 팩", s(19)),
 ("Lottie", "After Effects 애니메이션을 JSON 파일 하나로 내보내 앱에서 그대로 재생하는 라이브러리", s(20)),
 ("Material Theme Builder", "브랜드 메인 색으로 다크·라이트 모드 색 조합을 코드(Color.kt/Theme.kt)로 뽑는 구글 공식 도구", s(19)),
 ("Coil", "Web URL 이미지나 로컬 리소스를 비동기로 최적화해 로딩하는 이미지 로딩 라이브러리", s(19)),
 ("name 속성", "strings.xml의 string 요소에 반드시 필요한 속성(리소스명)", s(22)),
 ("Packages 뷰 모드", "실제 폴더와 관계없이 패키지 구조 중심으로 재구성해 보여 주는 프로젝트 창 보기", s(24)),
 ("대체 리소스 (alternative resource)", "시스템 구성 변화에 대응하려고 리소스 이름에 수식어를 붙여 준비하는 리소스. 선택은 시스템이 자동으로", s(25)),
 ("values-ko-rKR", "한국어 + 대한민국 지역 수식어(지역 코드 앞에 r)", s(26)),
 ("drawable-nodpi", "화면 밀도와 관계없이 비트맵을 원래 크기로 쓰는 수식어", s(26)),
 ("-land / -port", "가로 / 세로 화면 방향 수식어", s(26)),
 ("폴백 (fallback)", "수식어가 붙지 않은 기본 폴더. 예외 상황을 대비한 기본값", s(41)),
 ("android.permission.INTERNET", "AndroidManifest.xml의 인터넷(네트워크) 접근 권한", s(29)),
 ("usesCleartextTraffic", "AndroidManifest.xml에서 암호화되지 않은(http) 통신을 허용하는 속성(보충)", s(29)),
 ("AsyncImage", "Coil이 제공하는, 이미지를 비동기로 로드하고 화면에 그려 주는 컴포저블", s(34)),
 ("ImageRequest.Builder", "context 정보로 이미지 요청 빌더 객체를 만들고 .data()·.build()로 요청 객체를 완성", s(34)),
 ("ContentScale.Crop", "비율을 유지하며 컨테이너를 완전히 채울 때까지 확대, 넘치는 부분은 잘라냄(여백 없음)", s(35)),
 ("ContentScale.Fit", "비율을 유지하며 이미지 전체가 보이도록 축소(검은 여백 생김)", s(35)),
 ("innerPadding", "Scaffold가 edge-to-edge 환경에서 시스템 바를 침범하지 않도록 계산해 넘겨주는 패딩", s(39)),
]

OUTRO = """
<h3>6장 범위 대조표 — 슬라이드 → 문제</h3>
""" + table(["슬라이드", "내용", "문제"], [["s2~4", "이벤트 로깅·Log 구조", "1"], ["s5~6", "로그 레벨·Logcat 창", "2"], ["s7", "System.out/err", "3"], ["s8", "Activity 3상태", "4"],
 ["s9", "콜백·3생애", "5"], ["s10", "생명주기 도식", "6"], ["s11", "자동 재생성 경우", "7"], ["s12~17", "상태 저장·SaveState", "8"], ["s18~21", "기본·새 리소스", "9"],
 ["s22~24", "strings.xml·뷰 모드", "10"], ["s25~27, 41", "대체 리소스·수식어·폴백", "11"], ["s28~32", "Coil 설치·이미지", "12"], ["s33~37", "AsyncImage·Crop/Fit", "13"], ["s38~43", "가로 여백·Scaffold 제거", "14"]]) + """
<div class="note"><b>뺀 슬라이드</b>: s1 표지, s44 빈 쪽.</div>
<div class="note"><b>원본 오탈자</b>: s5 "wrf" <span class="fix">→ wtf</span> / s11 "화전을 회전함으로써" <span class="fix">→ 화면을</span> / s12 "유진된다" <span class="fix">→ 유지된다</span> / s26 "-820dp" <span class="fix">→ -w820dp</span>, 리소스가 "설치된다" <span class="fix">→ 선택된다</span> / s28 "Nexus 7(pixel 7)" / s29 "AndroidMainfest".</div>
"""
