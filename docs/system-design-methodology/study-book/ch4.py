"""4장 ppa4 — 아키텍처 원칙·View 속성·NavHost·ViewModel·온도 변환기·과학적 표기법."""
from qbook2 import s as _s, quote, table, fill, slide


def s(*n):
    return _s(*n, deck="ppa4")


INTRO = """
<div class="note">소문제를 풀고 → 바로 아래 <b>답·해설</b>. 이중선(옅은 배경) = 문제, 가는 실선 = 답·해설, 굵은 실선 = 원문(원본 ppa4 슬라이드 번호·쪽 위/아래), 점선 = 해설 정리.
앞 장에서 이미 물은 지식은 다시 묻지 않고 "→ N장 문제 M"으로 잇습니다.</div>
<h2>4장. ppa4 — 아키텍처 원칙·View 속성·NavHost·ViewModel·온도 변환기·과학적 표기법</h2>
"""

ITEMS = []
P = ITEMS.append

# 1
P(dict(kind=["name", "mc"], title="Android Studio 화면 구성과 기본 설정 (○)",
parts=[
 dict(q="Android Studio 초기 화면의 영역 이름: 맨 위 메뉴 / 그 아래 버튼 줄 / 왼쪽 프로젝트 창 / 가운데 코드 창 / 오른쪽 Device Manager 창 / 아래 문제 창 / 맨 아래 상태 줄. 화면 배치를 바꾸는 메뉴 경로는?",
      a="menu bar(메뉴바) / tool bar(툴바) / tool window(프로젝트 창) / Editor(코드 에디터 창) / Emulator(Device manager 창) / tool window(problem 창) / status bar(스테이터스 바). [View] → [Appearance]"),
 dict(q="Android Studio의 툴 윈도우: ⓐ 프로젝트의 트리 계층 구조와 각 구성 파일 ⓑ 프로젝트 창에서 선택한 파일의 내부 구성을 계층적으로 ⓒ 실행 중인 프로세스 목록과 내부에서 발생하는 로그 메시지를 표시해 디버깅에 자주 씀",
      a="ⓐ Project ⓑ Structure ⓒ Problem &amp; Logcat (툴 윈도우는 스튜디오를 열 때 대개 자동으로 열림)"),
 dict(q="Android Studio에서 코드 수정 시 필요한 라이브러리 import가 자동으로 추가되게 하는 설정의 경로와 체크 항목은?",
      a="[File] → [Settings...] → [Editor] → [General] → [Auto Import], \"<b>Add unambiguous imports on the fly</b>\"",
      why="<p>unambiguous = <b>모호하지 않은</b> import만 자동으로 넣는다는 뜻(보충: 같은 이름의 클래스가 여러 패키지에 있으면 사람이 골라야 함). 2장 문제 14의 Ctrl+Shift+Enter는 툴팁에 뜬 import를 손으로 넣는 방법.</p>"),
 dict(q="Android Studio의 프로젝트 관리에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("프로젝트를 처음 열 때는 초기화면에서 오른쪽의 프로젝트를 선택하고 'Open'을 클릭한다.", True, "Android Studio 프로젝트를 처음 열 때는 초기화면(Welcome to Android Studio)의 Projects 목록에서 프로젝트를 고르고 Open을 누른다."),
            ("다른 프로젝트를 추가로 열려면 [File] → [Open]으로 선택한다.", True, "Android Studio에서 프로젝트가 열린 상태로 다른 프로젝트를 추가로 열 때는 [File] → [Open]을 쓴다."),
            ("프로젝트를 닫으려면 [File] → [Close project]를 클릭한다.", True, "Android Studio에서 프로젝트를 닫는 메뉴는 [File] → [Close project]다."),
            ("프로젝트를 연 채로 폴더 위치를 통째로 옮기는 것이 안전한 백업 방법이다.", False, "Android Studio 프로젝트는 <b>닫은 뒤에</b> 폴더의 위치를 통째로 옮기거나 압축(zip)해서 백업할 수 있다.")],
      a="ⓐ ⓑ ⓒ")],
fig=slide("ppa4", 2, 85),
quote=quote("[File] -> [Settings...]-> [Editor] -> [General] -> [Auto Import] 을 클릭해서, “adds unambiguous imports on the fly” 를 선택하면, 코드 수정시 요구되는 라이브러리들이 추가되어 편리하게 사용할 수 있다.", s(2, 3, 4, 5))))

# 2
P(dict(kind=["diag", "mc"], title="Live Edit로 되는 수정, 안 되는 수정",
parts=[
 dict(q="Live Edit가 없던 때 UI를 고치면 거쳐야 했던 과정 4단계와, Android Studio의 Live Edit가 바꾼 점은?",
      a="코드 수정 → 재빌드 → 앱 재설치/재시작 → 원하는 화면까지 재이동 후 확인. Live Edit: 앱을 에뮬레이터나 실제 기기에 실행해 둔 상태에서 코드를 수정하면, 재빌드·재시작 없이 변경 사항이 실행 중인 앱에 <b>즉시 반영</b>."),
 dict(q="앱을 에뮬레이터에 실행해 둔 채 다음을 고쳤다. Live Edit로 즉시 반영되는 것을 모두 고르시오.",
      opts=[("TurtleScreen 안 Text의 문자열을 바꿈", True, "Text의 문자열을 바꾸는 것은 Composable 함수의 <b>본문</b> 수정이라 Live Edit로 실시간 반영된다."),
            ("Direction3DButton에 파라미터 하나를 추가", False, "Direction3DButton에 파라미터를 추가하는 것은 함수의 <b>Method 시그니처 변경</b>이라 Live Edit가 지원하지 않는다."),
            ("새 컴포저블 함수 Footprint()를 추가", False, "새 컴포저블 함수 Footprint()를 추가하는 것은 <b>method의 추가</b>라 Live Edit가 지원하지 않는다."),
            ("거북이 tween 시간을 500에서 300으로 바꿈", True, "거북이 tween 시간 값을 바꾸는 것은 Composable 함수 본문 안의 세부 값 변경이라 Live Edit로 실시간 반영된다."),
            ("TurtleViewModel이 상속하는 클래스를 바꿈", False, "TurtleViewModel이 상속하는 클래스를 바꾸는 것은 <b>클래스 계층 구조의 변경</b>이라 Live Edit가 지원하지 않는다.")],
      a="ⓐ ⓓ",
      why="<p>기준은 하나: <b>Composable 함수의 본문만</b>. 함수 안의 값·로직 세부 = 반영 / 함수의 모양(파라미터 = 시그니처, 2장 문제 11)이나 새 함수·클래스 = 구조 변경 → 반영 안 됨.</p>")],
quote=quote("단, Composable 함수의 본문에만 변경을 적용할 수 있으며, Method 시그니처 변경이나 method 의 추가, 클래스 계층 구조의 변경은 지원하지 않습니다.", s(6))))

# 3
l4_q, l4_a = fill(["ppa4판 계층(바깥 → 안)", "하는 일(원문)"], [
    [("?", "Linux kernel"), "하드웨어(카메라, 디스플레이, 메모리, 프로세서 등)를 직접 제어하는 드라이버, 프로세스 관리, 메모리 관리, 보안(권한, 샌드박싱). 컴퓨터의 OS 커널과 같은 역할"],
    [("?", "HAL (Hardware Abstraction Layer)"), "카메라, 블루투스, 센서 등 제조사마다 다르게 구현된 부분을 표준화된 인터페이스로 감싸 상위 계층이 하드웨어 종류에 상관없이 동일한 방식으로 접근하게 함"],
    [("?", "ART + Native C/C++ Libraries"), "ART: Kotlin 또는 Java로 작성된 후 컴파일된 바이트 코드를 실제로 실행하는 런타임 / Native Libraries: SQLite, WebKit, OpenGL 등 C/C++로 작성된 시스템 라이브러리"],
    [("?", "Java API Framework"), "개발자가 직접 다루는 시스템 서비스의 집합: Activity Manager(Activity 생명주기 관리), Window Manager(화면 창 관리), View System, Content Providers, Notification Manager"],
    [("?", "System Apps / Application"), "전화나 카메라 같은 기본 앱부터 사용자가 직접 실행하는 앱 모두"]])
P(dict(kind=["table", "name"], title="안드로이드 5계층 — ppa4판(HAL 포함)과 ppa1판 비교",
parts=[
 dict(q="ppa4의 안드로이드 시스템 5계층을 바깥(아래)에서 안(위)으로 쓰시오." + l4_q, a=l4_a,
      why="<p>원본 그림(아래)은 겹친 타원이다: 가장 바깥 Linux Kernel 안에 HAL, 그 안에 ART + Native C++ Libraries, 그 안에 Java API Framework, 가장 안쪽 System Apps.</p>"),
 dict(q="ppa1판 5계층(1장 문제 1)과 ppa4판의 구성 차이 두 가지는?",
      a="① ppa4판에는 <b>HAL</b>이 있다(ppa1판에는 없음) ② ppa1판은 <b>라이브러리</b>와 <b>안드로이드 런타임</b>을 별개 계층(같은 높이에 나란히)으로 두지만, ppa4판은 ART와 Native C/C++ Libraries를 <b>한 계층으로 묶는다</b>.",
      why="<p>문제에 <b>HAL</b>이나 \"Native C/C++\"가 보이면 ppa4판, \"라이브러리 계층이 가장 크다\"·\"Bionic\"·\"미디어 프레임 워크\"가 보이면 ppa1판으로 판단. 공통: 맨 아래 리눅스 커널, 맨 위 앱, 그 아래 프레임워크(액티비티 관리자 = Activity Manager). 추상화(Abstraction) = 차이를 감추고 같은 모양으로 보이게 하는 것 → HAL의 역할 그대로(보충).</p>")],
fig=slide("ppa4", 7, 92),
quote=quote("HAL (Hardware Abstraction Layer): 카메라, 블루투스, 센서 등 하드 웨어마다 제조사가 다르게 구현된 부분을 표준화된 인터페이스로 감싸서 상위 계층이 하드웨어 종류에 상관없이 동일한 방식으로 접근할 수 있도록 합니다.", s(7, 8))
 + "<p><span class='fix'>원본 s8 \"C/C++ fh로\" → C/C++로</span></p>"))

# 4
P(dict(kind=["name", "essay"], title="안드로이드의 핵심 아키텍처 원칙과 private",
parts=[
 dict(q="구글의 안드로이드 아키텍처 원칙에서 설명에 맞는 이름은? ⓐ UI(화면 구성), ViewModel(화면에 보여 줄 데이터를 관리하고 가공), Repository/데이터 layer(서버나 데이터베이스에서 데이터 가져오기)의 역할을 철저히 분리 ⓑ 데이터 모델이 먼저 변하면 화면이 그 변화를 감지하고 자동으로 그려져야(구독) 함 ⓒ 앱 안에서 특정 데이터의 실주인(진실)은 한곳에만 ⓓ 실주인(ViewModel)만 데이터를 수정하도록 숨겨 두고(private), 외부는 제공된 안전한 통로인 함수로만 변경을 요청",
      a="ⓐ 관심사 분리(Separation of Concerns) ⓑ 데이터 모델에서 UI 도출(Drive UI from Data Models) ⓒ 단일 진실 공급원(SSOT, Single Source of Truth) ⓓ 데이터 캡슐화(Data Encapsulation)",
      why="<p>원문은 \"<b>2가지 원칙</b>\"(관심사 분리 / 데이터 모델에서 UI 도출)이라 하고, SSOT와 데이터 캡슐화는 \"데이터 모델에서 UI 도출\"의 <b>하위 항목</b>이다. \"원칙이 몇 가지냐\"를 물으면 2.</p>"),
 dict(q="Kotlin에서 접근 제한자를 생략하면 무엇이 되나? ViewModel의 데이터에 private을 붙이는 이점 3가지를 쓰시오(각 키워드 포함).",
      a="public. ① <b>UI는 읽기만 하고, 변경은 ViewModel만</b> 하도록 구현 → 단방향 데이터 흐름(UDF) 강제 ② <b>데이터 오염 방지(안전성)</b>: ViewModel 내부의 비즈니스 로직(값은 0 이하로 내려갈 수 없다, 로그인 상태일 때만 더할 수 있다 등)을 거치지 않은 임의 조작을 막음 ③ <b>유지 보수의 편리함</b>: 데이터가 바뀌는 지점이 ViewModel 내부의 특정 함수(IncreaseCount() 등)로 제한되어, 디버깅·로그 확인 때 그 함수만 보면 됨"),
 dict(q="UDF를 풀어 쓰고, 데이터와 이벤트가 흐르는 방향을 쓰시오.",
      a="Unidirectional Data Flow(단방향 데이터 흐름). 데이터는 <b>위에서 아래로</b>(ViewModel → UI), 이벤트는 <b>아래에서 위로</b>(UI → ViewModel).",
      why="<p>코드로는 <code>var offsetX by mutableFloatStateOf(0f) private set</code> 한 줄이 SSOT·캡슐화·UDF를 모두 구현한다: 읽기는 밖에서, 쓰기는 ViewModel 안에서만(문제 13).</p>")],
quote=quote("데이터 캡슐화 (Data Encapsulation) : 진짜 데이타를 갖는 실질적인 주인 (ViewModel)만 데이터를 수정할 수 있도록 숨겨두는(private) 기술입니다.", s(9, 10))))

# 5
P(dict(kind=["table", "order"], title="ViewModel의 역할과 UI · UI 상태 · UI 로직",
parts=[
 dict(q="ViewModel은 무엇의 일부이며, 무엇을 위해 설계된 클래스인가? 얼마나 오래 유지되나? 사용 목적 2가지는? Activity와 Fragment를 각각 정의하시오.",
      a="Android Architecture Components의 하나. UI 관련 데이터를 화면 회전이나 configuration 변경에도 유지되도록 설계된 클래스. Activity나 Fragment의 생명주기와 <b>독립적으로</b>, 화면이 실제로 완전히 종료되기 전까지 유지. 목적: UI 상태와 UI 로직을 UI 자체(Activity, Composable)와 <b>분리</b> / configuration 변경 시에도 데이터를 다시 불러올 필요 없이 유지. Activity = 하나의 화면 단위를 구성하는 시스템 컴포넌트 / Fragment = Activity 내부에 포함되어 재사용 가능한 UI 조각(module)을 구성하는 컴포넌트."),
 dict(q="온도 변환기 화면에서 다음은 UI / UI 상태 / UI 로직 중 무엇인가? ⓐ 입력창을 화면 위쪽에, 결과 글자를 40sp로 ⓑ 지금 입력된 문자열 \"34\" ⓒ 입력이 비었거나 숫자인지 검사 ⓓ 섭씨로 화씨를 계산 ⓔ 지금 결과 칸에 보여야 할 \"93.2 °F\" ⓕ 온도에 따라 배경색 결정",
      a="ⓐ UI(무엇이 어떻게 그려질지: 레이아웃과 스타일) ⓑ UI 상태(특정 시점에 UI가 실제로 보여줘야 하는 데이터 값) ⓒ UI 로직(유효성 검사) ⓓ UI 로직(여러 상태를 조합해 파생 상태 계산) ⓔ UI 상태 ⓕ UI 로직",
      why="<p>구분 질문: \"<b>모양인가</b>(UI) / <b>지금 값인가</b>(UI 상태) / <b>값을 바꾸거나 만드는 규칙인가</b>(UI 로직)\". UI 상태가 바뀌면 recomposition이 일어난다.</p>"),
 dict(q="UI 로직 · UI 상태 · UI 자체 사이의 흐름을 화살표로 쓰시오. Composable이 값을 직접 바꾸지 않을 때 대신 하는 일은?",
      a="UI 로직(ViewModel) → UI 상태(State/StateFlow) → UI 자체(Composable), 사용자 이벤트는 위로 전달(Composable → ViewModel). Composable은 사용자 이벤트를 <b>콜백</b>으로 UI 로직(ViewModel)에 올려 보낸다.")],
fig=slide("ppa4", 12, 85),
quote=quote("UI 로직은 UI 상태값을 어떻게 바꿀 지를 결정하는 규칙 또는 연산으로. 유효성 검사, 네트워크 요청 결과를 상태에 반영하는 처리, 여러 상태를 조합해서 파생 상태를 계산하는 것 등이 포함됩니다.", s(11, 12))))

# 6
P(dict(kind=["table", "mc"], title="View의 두 종류: layout과 widget",
parts=[
 dict(q="View를 정의하시오. Activity가 setContent()로 지정하는 루트는 보통 무엇이며 몇 개인가?",
      a="View class 또는 subclass로 만들어진 객체. 보통 <b>1개의 ViewGroup</b>(그 내부에 여러 자식들을 트리 구조로 포함하는 1개 이상의 View로 구성)."),
 dict(q="View의 두 종류 layout과 widget을 정의하고(무엇의 subclass이며 자식을 담을 수 있나), 다음을 나누시오: LinearLayout, TextView, RelativeLayout, Button, ConstraintLayout, ImageView, EditText",
      a="layout = <b>ViewGroup의 subclass</b>, 여러 개의 자식 뷰를 규칙에 의해 화면에 배치(자식을 담을 수 있음): LinearLayout, RelativeLayout, ConstraintLayout / widget = <b>View의 subclass</b>로 단독으로 사용해 고유한 모양이나 기능을 가지는 요소(자식을 담을 수 없음): TextView, Button, ImageView, EditText",
      why="<p>Compose로 옮기면 layout ↔ Layout Composable(Column, Row, Box …, 2장 문제 10), widget ↔ Text, Button, Image. 판정 기준은 \"자식을 담을 수 있나\".</p>"),
 dict(q="View에 대한 설명으로 옳지 <b>않은</b> 것은?",
      opts=[("레이아웃과 위젯은 모두 View이므로 View class의 속성을 공통으로 적용할 수 있다.", True, "레이아웃(ViewGroup)과 위젯은 모두 View라서, alpha·padding·visibility 같은 View 공통 속성(문제 7)을 둘 다에 쓸 수 있다."),
            ("ViewGroup은 View의 subclass다.", True, "ViewGroup은 최상위 클래스 View를 상속한 subclass이고, layout들은 다시 ViewGroup의 subclass다."),
            ("Button은 자식 View를 담을 수 있다.", False, "Button은 widget(TextView의 subclass)이라 <b>자식을 담을 수 없다</b>.")],
      a="ⓒ")],
fig=slide("ppa4", 13, 90),
quote=quote("layout은 ViewGroup 의 subclass 를 의미하며, 여러 개의 자식 뷰를 규칙에 의해 화면에 배치하는 것을 의미한다.", s(13))))

# 7
P(dict(kind=["diag"], title="View 공통 속성: 상황에 맞는 XML 속성 고르기",
parts=[
 dict(q="View를 안 보이게 하거나 흐리게: ⓐ 버튼을 안 보이게 하되 그 자리(공간)는 그대로 ⓑ 안 보이게 하고 공간도 차지하지 않게 ⓒ 화면에 보이지만 누를 수 없는 비활성 상태로 ⓓ 레이아웃 공간은 그대로 두고 반투명하게(값 범위는?)",
      a="ⓐ android:visibility = INVISIBLE(View.INVISIBLE: 화면에 안 보이게) ⓑ visibility = GONE(View.GONE: 보이지 않으면서 공간 차지도 없게) ⓒ android:enabled = false(클릭 등 사용자 상호작용이 막혀 비활성화, 보이기는 하지만 조작 안 됨) ⓓ android:alpha: 0.0(완전 투명) ~ 1.0(완전 불투명), visibility와 달리 layout 공간은 그대로 차지하면서 시각적 투명도만",
      why="<p>안 보이기 세 단계: alpha(투명도만, 공간 O) / INVISIBLE(안 보임, 공간 O) / GONE(안 보임, 공간 X).</p>"),
 dict(q="여백·정렬·크기: ⓐ 버튼 테두리와 안쪽 글자 사이 여백 ⓑ 버튼과 옆 버튼 사이의 바깥 여백 ⓒ 버튼 <u>안의 글자</u>를 오른쪽 정렬 ⓓ 버튼 <u>자체</u>를 부모 ViewGroup 안에서 오른쪽에 ⓔ 모든 View에 필수로 들어가는 크기 속성과 값 3종",
      a="ⓐ android:padding(View의 내부 여백, paddingLeft·paddingRight·paddingTop·paddingBottom처럼 개별 지정 가능) ⓑ android:layout_margin(바깥 여백) ⓒ android:gravity(View 안의 내용물을 정렬) ⓓ android:layout_gravity(이 View가 부모 ViewGroup 안에서 어느 위치에 배치될지) ⓔ android:layout_width / layout_height: match_parent(부모만큼 채움), wrap_content(내용물만큼만), 100dp 같은 고정값",
      why="<p>\"layout_\"이 붙으면 <b>부모 기준</b>: gravity = 내 안의 내용물, layout_gravity = 부모 안의 나. padding = 안쪽, margin = 바깥.</p>"),
 dict(q="입력·식별·접근성: ⓐ View가 클릭 이벤트 자체를 받을 수 있는지(onClick·setOnClickListener가 동작하려면?) ⓑ 키보드 탐색·D-pad 포커스를 줄 수 있는지(값 3가지, Button은?) ⓒ Java 코드나 XML에서 이 View를 참조할 고유 이름 ⓓ 텍스트 없는 이미지 버튼을 스크린 리더가 읽어 주게 ⓔ 클릭 시 호출될 메서드를 지정하는 속성과, 요즘 더 표준적인 방식",
      a="ⓐ android:clickable(true여야 onClick·setOnClickListener가 동작) ⓑ android:focusable = true / false / auto, Button은 기본적으로 포커스 가능 ⓒ android:id ⓓ android:contentDescription(접근성 도구가 읽어 주는 설명 문구, 시각 장애인 접근성에 필수) ⓔ android:onClick, setOnClickListener()",
      why="<p>enabled · clickable · focusable 구분: enabled=false는 <b>보이지만 조작 불가</b>, clickable은 <b>클릭 이벤트를 받을 자격</b>, focusable은 <b>키보드 포커스</b>.</p>"),
 dict(q="화면·텍스트: ⓐ 동영상 재생·네비게이션 화면이 떠 있는 동안 자동으로 꺼지지 않게 ⓑ View를 중심점 기준으로 시계 방향 30도 ⓒ 다국어 지원을 위해 문자열을 지정하는 권장 형태 ⓓ 사용자의 시스템 폰트 크기 설정에 비례해 커지는 글자 크기 단위와, 그 설정과 무관하게 고정되는 단위",
      a="ⓐ android:keepScreenOn = true ⓑ android:rotation = 30(각도 단위, 양수는 시계방향) ⓒ android:text = \"@string/…\"(하드코딩보다 리소스 참조) ⓓ <b>sp</b>(textSize의 관례) / dp")],
fig=slide("ppa4", 17, 85),
quote=quote("android:enabled : View 가 사용자 입력에 반응할 지 여부를 결정합니다. false 이면, 클릭등의 사용자 상호작용이 막혀 비활성화되는 상태를 표현할 때 사용하는데, 즉, 보이기는 하지만, 조작은 안되도록 하므로, visibility 나 focusable 과는 다릅니다.", s(14, 15, 16, 17))))

# 8
md_q, md_a = fill(["XML 속성", "Compose Modifier", "비고"], [
    ["android:alpha", ("?", "Modifier.alpha(float)"), "0f~1f, 값 그대로"], ["android:background", ("?", "Modifier.background(color)"), "Color 또는 Brush 전달"],
    ["android:focusable", ("?", "Modifier.focusable()"), "포커스 가능 여부"], ["android:onClick", ("?", "Modifier.clickable { }"), "람다로 클릭 로직 직접 작성"],
    ["android:padding", ("?", "Modifier.padding()"), "내부 여백, 동일 개념"], ["android:rotation", ("?", "Modifier.rotate(degrees)"), "각도 단위 동일"],
    ["android:layout_width/height", ("?", "Modifier.width()/height()/fillMaxSize()"), "match_parent → fillMaxWidth() 등"],
    ["android:layout_margin", ("?", "Modifier.padding()"), ("?", "바깥 여백 용도로 사용, margin 전용 API 없음")],
    ["android:clickable", ("?", "Modifier.clickable(enabled = …)"), "클릭 가능 여부 자체를 제어"], ["android:layout_gravity", ("?", "Modifier.align()"), "부모 Scope 내에서 자신의 위치 지정"],
    ["android:contentDescription", ("?", "Modifier.semantics { contentDescription = .. }"), "Icon/Image는 별도 파라미터로도 제공"]])
P(dict(kind=["table", "diag"], title="XML 속성은 Compose에서 무엇이 되나",
parts=[
 dict(q="View(XML)의 공통 특성을 Compose에서 처리하는 방식 4가지와 각 예시는?",
      a="① Composable 하나의 외형/레이아웃/동작 → <b>Modifier 체이닝</b>(alpha, rotation …) ② Composable 고유의 데이터 또는 상태 → <b>Composable 함수의 파라미터</b>(Text(text=…)) ③ 자식들을 담는 컨테이너의 배치 규칙 → <b>컨테이너 Composable의 자체 파라미터</b>(Column(horizontalAlignment=…)) ④ Composable 범위를 넘어서는 화면이나 시스템 설정 → <b>Activity, Window, Effect 계열의 함수</b>(keepScreenOn …)",
      why="<p>\"<b>누구의 일인가</b>\": 나 하나의 모양 → Modifier, 나의 내용 → 파라미터, 내 자식들 배치 → 컨테이너 파라미터, 나를 넘어선 화면 → Activity/Window.</p>"),
 dict(q="XML 속성의 Compose Modifier 대응표를 채우시오." + md_q, a=md_a,
      why="<p>margin이 없다는 것이 단골 함정: Compose에서는 padding을 <b>바깥 여백 용도로</b> 쓴다(Modifier 순서에 따라 바깥/안쪽처럼 보임 — 2장 문제 24, 보충).</p>"),
 dict(q="Modifier로 대응되지 않는 XML 속성 3가지(android:id, android:keepScreenOn, android:visibility=\"gone\")를 Compose는 각각 어떻게 처리하나? 이유는?",
      a="id: View 방식은 view tree를 만든 뒤 findViewById(R.id.xxx)로 찾아가는 구조였지만, Compose는 코드 안에서 <b>변수를 직접 참조</b>하므로 id가 필요 없다 / keepScreenOn: Composable 하나의 속성이 아닌 <b>화면 전체의 설정</b>이라 Activity의 window.addFlags()처럼 window에 <b>FLAG_KEEP_SCREEN_ON</b> flag를 건다 / visibility=\"gone\": 화면에 그리지도 않고 공간도 차지하지 않는 것이라 <b>if 문</b>으로 처리(아예 호출하지 않음)"),
 dict(q="Composable 함수의 파라미터로 대응되는 것: ⓐ android:text, textSize, textColor는 Text()의 무엇인가? 같은 스타일이 반복되면? ⓑ android:gravity는? ⓒ android:enabled는?",
      a="ⓐ text, fontSize, color. 여러 Text()에서 같은 스타일이 반복되면 TextStyle()에서 정의 ⓑ 내용물을 담아 배치하는 Box(), Column(), Row()가 자체적으로 갖는 파라미터 ⓒ Button, TextField, IconButton 같은 상호작용 컴포저블이 내장한 enabled: Boolean 파라미터")],
fig=slide("ppa4", 19, 95),
quote=quote("android:visibility ='gone' 의 경우, 화면에 그리지도 않고 공간을 차지 하지도 않는 조항이라, Compose 에서는 if 문을 사용하여, 처리합니다.", s(18, 19, 20, 21))))

# 9
P(dict(kind=["name", "mc"], title="NavHost와 Navigation",
parts=[
 dict(q="NavHost를 정의하시오(제공 라이브러리, 무엇에 따라 무엇을 하나). 앱이 여러 화면일 때 화면을 등록하고 호출하는 방식은?",
      a="Navigation Compose 라이브러리가 제공하는 컴포저블 함수로, 지금 어떤 화면을 보여 줄지를 <b>route(경로 문자열)</b>에 따라 전환해 주는 컨테이너. \"화면 = route 문자열\"의 형식으로 등록해 두고, <code>navigate(\"route이름\")</code>으로 호출."),
 dict(q="NavHost가 표준 방법으로 지원하는 것: ⓐ 특정 데이터를 유지하면서 다음 화면으로 이동할 때 route 표기 예 ⓑ 알림 등을 눌러 특정 화면으로 즉시 이동 ⓒ 다른 화면이 밀리며 들어오는 듯한 전환 효과",
      a="ⓐ route에 인자를 포함: \"detail/{index}\" ⓑ 딥링크 ⓒ 슬라이드 애니메이션"),
 dict(q="Navigation(Navigation-Compose)에 대한 설명으로 옳지 <b>않은</b> 것은?",
      opts=[("앱 내의 화면(destination)은 고유한 경로(route) 문자열로 등록되고, 화면 전환은 등록된 경로를 이용한다.", True, "Navigation은 화면(destination)을 고유한 route 문자열로 등록하고, route로 화면 간 이동, 뒤로 가기(back stack) 등을 관리."),
            ("여러 화면을 동시에 렌더링해 전환 속도를 높인다.", False, "Navigation은 여러 화면을 동시에 그리지 않는다. Navigation은 여러 화면 중 어느 화면이 활성 상태인지 관리하고, <b>한 번에 하나의 목적지만</b> 렌더링되도록 보장한다."),
            ("시스템 백 버튼과 popBackStack()의 뒤로 가기 동작을 자동으로 처리한다.", True, "Navigation은 시스템 백 버튼과 popBackStack()의 뒤로 가기를 백 스택(문제 15)으로 자동 처리한다."),
            ("화면 간 인자 전달을 경로에 포함시켜 처리할 수 있다.", True, "Navigation은 \"detail/{index}\"처럼 route에 인자를 포함시켜 화면 간에 값을 전달한다."),
            ("외부 URL이나 알림에 의해 특정 화면으로 바로 진입하는 딥링크 기능이 지원된다.", True, "Navigation은 외부 URL이나 알림을 눌러 특정 화면으로 바로 진입하는 딥링크를 지원한다.")],
      a="ⓑ")],
quote=quote("NavHost 는 Navigation Compose 라이브러리가 제공하는 컴포저블 함수로 지금 어떤 화면을 보여줄 지를 route(경로 문자열)에 따라서 전환해 주는 컨테이너 입니다.", s(22, 42))))

# 10
P(dict(kind=["order", "name"], title="toml(Version Catalog)로 라이브러리 추가하기",
parts=[
 dict(q=".toml 파일 형식의 특징은? Version catalog가 의존성 지정의 기본 방식이 된 시점과, Gradle이 카탈로그를 찾는 파일 이름은?",
      a="key = value와 [섹션] 위주로 사람이 직접 읽고 쓰기 편하게 되어 있는 최소한의 설정 파일 형식. 안드로이드 스튜디오 <b>Canary 12</b>부터(새 프로젝트를 만들면 루트 디렉토리에 .toml 파일이 자동 생성). <code>libs.versions.toml</code>(이 기본 이름을 쓰는 것이 권장)."),
 dict(q="toml로 navigation-compose 라이브러리를 추가해 코드에서 쓰기까지의 4단계를 순서대로 쓰시오.",
      a="libs.versions.toml에 라이브러리 등록 → build.gradle.kts의 dependencies {}에 libs.xxx로 참조 → Gradle Sync(오른쪽 상단 코끼리 아이콘) → MainActivity.kt 등의 코드에서 라이브러리 import 가능"),
 dict(q="libs.versions.toml에 <code>[versions] navigationCompose = \"2.9.8\"</code>, <code>[libraries] androidx-navigation-compose = { group = \"androidx.navigation\", name = \"navigation-compose\", version.ref = \"navigationCompose\" }</code>를 등록했다. ⓐ version.ref는 무엇을 가리키나? ⓑ build.gradle.kts(:app)에서 이 라이브러리를 부르는 표기는?",
      a="ⓐ [versions] 섹션의 navigationCompose 항목(= \"2.9.8\") ⓑ <code>implementation(libs.androidx.navigation.compose)</code>",
      why="<p>toml 이름 <code>androidx-navigation-compose</code>의 <b>하이픈이 점으로</b> 바뀌어 <code>libs.androidx.navigation.compose</code>가 된다(원문 두 코드를 맞대어 보면 확인됨). 버전을 [versions]에 한 번만 적고 ref로 참조하는 구조는 6장 Coil 설치에서도 반복된다.</p>")],
fig=slide("ppa4", 23, 85),
quote=quote("안드로이드 스튜디오 Canary 12 부터 새프로젝트를 만들 때, Version catalog 가 의존성을 지정하는 기본 방식이 되었고, 프로젝트를 생성하면, 루트 디렉토리에 .toml 파일이 자동으로 생성되고", s(23, 24, 25))))

# 11
P(dict(kind=["order", "diag"], title="TurtleApp과 NavHost: 직접 호출에서 간접 호출로",
intro="TurtleApp.kt: <code>fun TurtleApp() { val navController = rememberNavController(); NavHost(navController = navController, startDestination = \"turtle\") { composable(route = \"turtle\") { TurtleScreen() } } }</code>",
parts=[
 dict(q="TurtleApp의 <code>rememberNavController()</code>, <code>startDestination</code>, <code>composable(route = \"turtle\") { … }</code>는 각각 무엇인가? 새 Kotlin 파일 TurtleApp.kt를 만드는 메뉴와 선택 항목은?",
      a="화면 이동을 맡을 내비게이션 컨트롤러를 만들어 기억 / 처음 보여 줄 목적지의 route / \"turtle\"이라는 route에 TurtleScreen 화면을 등록. [File] → [New] → New Kotlin Class/File에서 'File' 선택, 이름 TurtleApp.kt (보충: 각 항목 설명은 코드에서 읽은 것)"),
 dict(q="NavHost를 도입하면서 MainActivity의 setContent 안에서 바뀐 한 줄은? 바뀌기 전과 후의 호출 트리를 쓰시오.",
      a="<code>TurtleScreen()</code> → <code>TurtleApp()</code>. 전: MainActivity.setContent{} └ TurtleScreen()(<b>직접 호출</b>) / 후: MainActivity.setContent{} └ TurtleApp() └ NavHost └ TurtleScreen()(<b>NavHost에 의해 간접 호출</b>)",
      why="<p>화면 호출의 주인이 MainActivity에서 <b>NavHost</b>로 바뀐다. 그래서 화면을 추가해도 MainActivity는 그대로 두고 composable(route)만 늘리면 된다(온도 변환기·과학적 표기법이 그렇게 추가됨, 문제 18).</p>")],
fig=slide("ppa4", 28, 85),
quote=quote("이렇게 NavHost 를 설정하게 되면, 이전에는 TurtleScreen()을 직접 호출하던 것이 NavHost 에 의해서 간접적으로 호출하는 방식으로 변경됩니다.", s(25, 26, 27, 28))))

# 12
P(dict(kind=["mc", "diag"], title="ViewModel을 붙이는 이유와 Home 버튼의 역할 분담",
parts=[
 dict(q="Turtle Screen에 ViewModel을 연결하는 이점으로 옳은 것을 모두 고르시오.",
      opts=[("UI 관련 데이터를 UI 컨트롤러(Activity/화면)의 생명주기와 분리해서 보관한다.", True, "ViewModel은 AAC(Android Architecture Component)의 일부로, UI 관련 데이터를 Activity/화면의 생명주기와 분리해 보관하도록 설계된 클래스다."),
            ("여러 화면(Fragment/Composable)이 같은 ViewModel을 공유해 상태를 함께 사용할 수 있다.", True, "여러 화면(Fragment/Composable)이 같은 ViewModel을 공유하면 상태를 함께 쓸 수 있다."),
            ("UI 없이 ViewModel의 로직만 독립적으로 테스트할 수 있어 단위 테스트가 쉬워진다.", True, "ViewModel의 로직은 UI와 분리되어 있으므로 UI 없이 단독 테스트할 수 있다(1장 문제 22의 로컬 단위 테스트로 가능)."),
            ("화면 회전으로 Activity가 파괴되면 ViewModel 객체도 함께 파괴된다.", False, "반대다. UI와 비즈니스 로직/상태 관리 로직을 분리하므로, 화면 회전 시 (내부적으로 Activity가 파괴되어도) ViewModel 객체는 <b>살아 있다</b>."),
            ("앱 프로세스가 종료되어도 ViewModel의 값은 Bundle에 자동 보관된다.", False, "ViewModel 값이 Bundle에 자동 보관된다는 것은 원문에 없는 내용이다. 프로세스 종료 후 복원은 3장 <b>rememberSaveable(Bundle)</b>·6장 onSaveInstanceState의 영역이고, ViewModel은 설정 변경(회전)에 살아남는 것까지만 원문에 있다.")],
      a="ⓐ ⓑ ⓒ"),
 dict(q="UI와 ViewModel을 결합하는 경우가 많은 세 가지 상황은?",
      a="상태와 로직이 복잡해지는 화면 / 여러 화면이 데이터를 공유하는 경우 / 네트워크·데이터베이스 접근이 필요한 화면"),
 dict(q="Turtle Screen에 Home 버튼(누르면 거북이 위치 초기화)을 추가했다. UI(Composable)와 ViewModel은 각각 무엇을 하나? TurtleApp에서 TurtleViewModel 객체를 얻는 함수와 넘기는 방법은?",
      a="UI: 클릭을 감지하고 ViewModel의 함수를 호출 / ViewModel: 함수가 호출되면 offsetX를 0으로 바꿀지, trail을 어떻게 지울지 <b>판단과 실행</b>(판단 logic 전담). <code>val turtleViewModel: TurtleViewModel = viewModel()</code>(androidx.lifecycle.viewmodel.compose.viewModel), <code>TurtleScreen(viewModel = turtleViewModel)</code>로 인자 전달.",
      why="<p>문제 4의 캡슐화·UDF가 실제로 적용된 모습: 이벤트(클릭)는 위로, 판단은 ViewModel.</p>")],
quote=quote("UI 와 비즈니스 로직/상태 관리 로직을 분리하기 때문에, 화면 회전 시에도 (내부적으로 Activity 가 파괴되도) ViewModel 의 객체는 살아있다.", s(29, 30, 31, 32))))

# 13
P(dict(kind=["diag", "name"], title="TurtleViewModel로 옮긴 코드 읽기",
intro="TurtleViewModel: <code>var offsetX by mutableFloatStateOf(0f) private set</code> / <code>private val _trail = mutableStateListOf&lt;FootprintData&gt;()</code> / <code>val trail: List&lt;FootprintData&gt; get() = _trail</code> / <code>private fun leaveFootprint()</code> / <code>private val step = 24f</code> / <code>fun moveUp() …</code> / <code>fun resetToOrigin() { offsetX = 0f; offsetY = 0f; rotationAngle = 0f; _trail.clear() }</code>",
parts=[
 dict(q="TurtleScreen에서 <code>viewModel.offsetX = 50f</code>라고 쓰면? 읽는 것은?",
      a="컴파일 오류 — <b>private set</b>이라 쓰기(재할당)는 ViewModel 내부에서만 가능. 읽기(viewModel.offsetX)는 밖에서 가능."),
 dict(q="TurtleViewModel에서 발자국 리스트를 _trail과 trail 두 개로 나눈 이유는? trail의 타입이 MutableList가 아니라 List인 이유는? leaveFootprint와 step을 private로 둔 이유는?",
      a="바꿀 수 있는 진짜 리스트(_trail)는 private으로 숨기고, 밖에는 <b>읽기 전용</b> 통로(trail: List)만 공개 → UI가 목록을 직접 추가·삭제하지 못하게(캡슐화). List는 읽기 전용 인터페이스라서(보충). 밖에서 부를 필요가 없는 내부 로직·상수라서, 외부는 moveUp 같은 공개 함수로만 변경을 요청.",
      why="<p>\"밑줄(_) 붙은 private 진짜 + 밑줄 없는 public 읽기 전용\"은 SSOT·캡슐화(문제 4)의 정석 패턴. ViewModel 안에서는 remember/rememberSaveable을 쓰지 않는다 — ViewModel 객체 자체가 리컴포지션·회전에도 살아 있으므로(보충).</p>"),
 dict(q="ViewModel로 옮긴 뒤 TurtleScreen은 어떻게 바뀌나? ⓐ animateDpAsState의 targetValue ⓑ BottomBar 콜백(onUp, onHome) ⓒ 발자국을 그릴 때 순회하는 것 ⓓ TurtleBottomBar에 추가된 파라미터와 다섯 번째 버튼의 label·icon",
      a="ⓐ <code>viewModel.offsetX.dp</code>(viewModel. 뒤에 체이닝) ⓑ <code>onUp = { viewModel.moveUp() }</code> … <code>onHome = { viewModel.resetToOrigin() }</code> ⓒ <code>viewModel.trail.forEach { … }</code> ⓓ <code>onHome: () -&gt; Unit</code>, label \"Home\", icon <code>Icons.Default.Home</code>")],
quote=quote("TurtleScreen 컴포저블 안에서 TurtleViewModel 클래스의 변수나 함수를 받는 경우, viewModel. 뒤에 체이닝을 시켜, 코드를 수정해 준다.", s(33, 34, 35, 36, 37, 38, 39))))

# 14
em_q, em_a = fill(["비교 항목", "이모지 Text(\"🏠\")", "벡터 아이콘 Icon(imageVector = Icons.Filled.Home, …)"], [
    ["정체", ("?", "유니코드 문자"), ("?", "ImageVector 객체 = 그래픽 데이터(좌표·경로)")],
    ["누가 그림으로 바꾸나", ("?", "폰트 엔진이 문자를 그림으로 변환해 렌더링"), ("?", "Compose가 좌표/경로 데이터를 직접 그림(앱에 내장된 그래픽)")],
    ["기기별 모양", ("?", "기기별(삼성/구글/애플 등)로 다를 수 있음"), ("?", "기기에 관계없이 항상 완전히 동일")],
    ["색", ("?", "고정, 변경 불가"), ("?", "tint 파라미터로 자유롭게 변경")]])
P(dict(kind=["table"], title="이모지 vs 벡터 아이콘",
parts=[
 dict(q="Turtle Screen의 Home 버튼 위 집 그림은 무엇이 제공하는 무엇인가? 이모지 방식과 벡터 아이콘 방식을 비교하시오." + em_q,
      a="이모지가 아닌 <b>Material Icons</b> 라이브러리가 제공하는 <b>vector icon</b>." + em_a,
      why="<p>모든 칸이 \"<b>문자냐 그림 데이터냐</b>\"에서 나온다: 문자는 글꼴이 그리니 기기에 따라 다르고 색도 글꼴 그림 그대로, 그림 데이터는 앱이 직접 그리니 어디서나 같고 칠할 색도 정할 수 있다(2장 문제 24의 tint = Color(0xFF555555)가 그 예).</p>")],
quote=quote("ImageVector 객체는 그래픽 데이터입니다.", s(40))))

# 15
P(dict(kind=["order", "name", "diag"], title="백 스택과 ViewModel의 수명",
parts=[
 dict(q="스택의 구조 이름(약어 포함)은? Turtle Screen에서 상단의 온도계 버튼을 눌러 온도 변환기로 들어갔다가 백 버튼을 누를 때 스택에서 일어나는 일 2가지(동사)는? 온도 변환기에서 뒤로 가기를 코드로 실행하는 함수는?",
      a="LIFO(Last-in, First-Out, 가장 나중에 들어온 데이터가 가장 먼저 나감). 진입: 시스템(네비게이션 컨트롤러)이 온도 변환 화면을 스택의 최상단(Top)에 <b>push</b> / 백 버튼: 최상단 화면이 <b>pop</b>(제거)되면서 바로 아래 Turtle Screen이 나타남. <code>navController.popBackStack()</code>"),
 dict(q="Navigation-Compose와 ViewModel의 연결: ⓐ 상태 홀더로서 ViewModel과 Composable의 분담 ⓑ 화면이 백 스택에 숨겨지거나 잠시 가려졌다가 사용자가 돌아올 때 ViewModel은? ⓒ 각 목적지마다 만들어져 viewModel() 호출과 연동되는 것 ⓓ ViewModel의 자원이 정리되는 시점과 호출되는 함수",
      a="ⓐ ViewModel = 화면 상태(State)와 비즈니스 로직, Composable = 그 상태를 읽고 그리는 UI 렌더링 ⓑ 파괴되지 않고, 저장되어 있던 이전 상태가 그대로 유지(수명 주기 분리) ⓒ <b>NavBackStackEntry</b> ⓓ 해당 화면이 네비게이션 그래프에서 <b>완전히 제거될 때만</b>, <code>onCleared()</code>",
      why="<p>ViewModel의 수명은 Composable이 아니라 <b>NavBackStackEntry</b>에 묶인다 → 화면이 가려져도(스택 아래에 있어도) entry가 남아 있으니 ViewModel도 산다. pop되어 entry가 사라질 때 onCleared.</p>")],
quote=quote("해당 화면이 네비게이션 그래프에서 완전히 제거될 때만, ViewModel 의 onCleared()가 호출되어 자원이 정리됩니다.", s(43, 44, 53))))

# 16
P(dict(kind=["table", "diag"], title="Kotlin의 ?와 custom getter",
parts=[
 dict(q="Kotlin에서 ?의 세 가지 쓰임의 이름을 쓰고, 예를 하나씩 해석하시오: <code>var name: String? = null</code> / <code>var length = name?.length</code> / <code>val c = celsiusInput.toDoubleOrNull() ?: return Color.LightGray</code>",
      a="① 타입 뒤 ? = <b>nullable type marker</b>: name은 문자열 타입인데 null을 가질 수 있다 ② 변수나 함수 호출 뒤 ? = <b>안전 호출 연산자(safe call)</b>: name이 null이 아니면 name.length를 실행하고, null이면 전체 식이 null ③ 식1 ?: 식2 = <b>엘비스 연산자(Elvis operator)</b>: 식1의 결과가 null이 아니면 그 값을 쓰고, null이면 식2를 실행 → 숫자로 바뀌면 c에 담고, 안 되면 바로 Color.LightGray를 반환",
      why="<p>판별법: <b>타입 뒤</b>(String?) = 널 허용, <b>점 앞</b>(?.) = 안전 호출, <b>콜론과 붙음</b>(?:) = 엘비스.</p>"),
 dict(q="<code>toDoubleOrNull()</code>은 어떤 함수인가?",
      a="문자열을 Double로 변환하되, 실패하면 null 값을 반환하는 확장 함수."),
 dict(q="온도 변환기 ViewModel의 <code>val backgroundColor: Color get() { … }</code> 같은 custom getter는 일반 속성(<code>val x = …</code>)과 무엇이 다른가? backing field란?",
      a="일반 속성은 = 로 연결된 값이 계산된 후 그 값이 <b>backing field(내부 저장 공간)</b>에 저장된다. get() { … }으로 정의하면 backgroundColor에 <b>접근할 때마다 get() 블록 전체가 실행</b>되어 그 값으로 Color가 정해진다.",
      why="<p>custom getter를 쓰는 이유: 배경색·화씨값은 입력에서 <b>파생</b>되는 값이라 입력이 바뀔 때마다 새로 계산돼야 한다 → 저장해 두면 낡은 값이 남는다(보충).</p>")],
quote=quote("get() {..} 으로 정의되는 경우, backgroundColor 에 접근할 때마다 get() 블록 전체가 실행되서, 그 값을 통해 Color가 정해 집니다.", s(45, 46, 47))
 + "<p><span class='fix'>원본 s47: 번호가 ①①①로 표기, 예시 설명의 \"num.length\" → name.length</span></p>"))

# 17
t4_q, t4_a = fill(["입력", "결과 글자", "배경색", "입력창 오류 표시"], [
    ["\"\"(처음 화면)", ("?", "-- °F"), ("?", "LightGray(회색)"), ("?", "없음(빈 입력은 유효)")], ["34", ("?", "93.2 °F"), ("?", "노랑(0xFFFFF9C4)"), ("?", "없음")],
    ["800", ("?", "1472.0 °F"), ("?", "분홍(0xFFFFCDD2)"), ("?", "없음")], ["0", ("?", "32.0 °F"), ("?", "하늘색(0xFFB3E5FC)"), ("?", "없음")],
    ["-40", ("?", "-40.0 °F"), ("?", "하늘색"), ("?", "없음")], ["100", ("?", "212.0 °F"), ("?", "분홍"), ("?", "없음")], ["abc", ("?", "-- °F"), ("?", "LightGray"), ("?", "있음")]])
P(dict(kind=["calc", "diag"], title="온도 변환기(기본형)의 결과와 숨은 색",
intro="TemperatureViewModel(기본형): FREEZING_C = 0.0, BOILING_C = 100.0. fahrenheit = 입력이 숫자면 c × 9/5 + 32, 아니면 null. 배경색: 입력이 숫자가 아니면 Color.LightGray, c ≤ 0이면 0xFFB3E5FC, c ≥ 100이면 0xFFFFCDD2, 그 사이 0xFFFFF9C4. 결과 글자: <code>viewModel.fahrenheit?.let { \"%.1f °F\".format(it) } ?: \"-- °F\"</code>. isValidInput = 입력이 비었거나 숫자로 바뀌면 true(초기값 true). 입력창은 isError = !isValidInput.",
parts=[
 dict(q="온도 변환기(기본형)에 다음을 입력했을 때 결과 글자, 배경색, 입력창 오류 표시를 쓰시오." + t4_q, a=t4_a,
      why="<ol><li>계산: 34 × 9/5 = 61.2, + 32 = 93.2 / 800 × 1.8 = 1440, + 32 = 1472.0 / −40 × 1.8 = −72, + 32 = −40.0.</li><li>경계값: 0은 \"≤ 0\"이라 하늘색, 100은 \"≥ 100\"이라 분홍. 등호가 어느 쪽에 붙었는지가 함정.</li><li>isValidInput 초기값이 true인 이유 = 처음 열자마자 빈 입력창에 빨간 오류가 뜨지 않게(빈 입력을 유효로 취급). \"abc\"는 toDoubleOrNull이 null → 엘비스로 LightGray, 결과도 \"-- °F\".</li></ol>"),
 dict(q="원본 온도 변환기 마지막 화면의 \"숨어있는 색상을 찾아보세요!\"의 답은?",
      a="섭씨 0도 이하일 때의 <b>하늘색</b>(0xFFB3E5FC). 원본 실행 캡처에는 회색(빈 입력), 노랑(34), 분홍(800)만 나와 있다.")],
fig=slide("ppa4", 54, 90),
quote=quote("섭씨 온도를 넣어 실행시켜 보고, 백버튼을 눌러, 화면이 전환되는 지 확인하고, 배경색 변화를 찾아보자.", s(45, 46, 49, 54))))

# 18
P(dict(kind=["name", "order"], title="sealed class로 화면 경로 묶고 화면 잇기",
intro="<code>sealed class Screen(val route: String) { object Turtle : Screen(\"turtle\"); object Temperature : Screen(\"temperature\"); object Calculate : Screen(\"scientific\") }</code>",
parts=[
 dict(q="Turtle Screen 앱의 화면 경로를 sealed class Screen으로 묶는 이점은? Turtle을 class가 아닌 object로 선언한 이유는? <code>: Screen(\"turtle\")</code>과 route는 각각 무엇인가?",
      a="앱의 <b>전체 화면 구성을 한눈에</b> 파악할 수 있다. 거북이 화면(Turtle)은 앱에서 <b>유일한</b> 화면이므로 object. <code>Screen()</code> = Screen이라는 부모 클래스의 성질을 상속받는다는 의미, route = \"turtle\"은 거북이 화면의 <b>문자열 주소</b>."),
 dict(q="NavHost에서 문자열 \"turtle\" 대신 쓰는 표기는? TurtleScreen에서 온도 변환기로 가는 콜백 이름과, TurtleApp에서 그 콜백에 넘기는 동작은? TemperatureScreen의 뒤로 가기(onBack)에 넘기는 동작은?",
      a="<code>startDestination = Screen.Turtle.route</code>, <code>composable(Screen.Turtle.route)</code>. <code>onNavigateToTemperature</code> → <code>{ navController.navigate(Screen.Temperature.route) }</code>. onBack → <code>{ navController.popBackStack() }</code>",
      why="<p>화면 이동의 3요소: <b>주소</b>(sealed class의 route) / <b>등록</b>(NavHost의 composable(route)) / <b>호출</b>(navigate(route) 또는 popBackStack()). 새 화면(과학적 표기법)을 추가할 때도 이 세 군데를 고친다.</p>"),
 dict(q="TopAppBar 파라미터: ⓐ TemperatureScreen의 왼쪽 뒤로 가기 화살표는 어느 파라미터에 무엇을 두나? ⓑ TurtleScreen의 오른쪽 온도계·계산기 버튼은 어느 파라미터에, 아이콘 이름은?",
      a="ⓐ <code>navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = \"뒤로가기\") } }</code> ⓑ <code>actions = { … }</code>, Icons.Default.Thermostat(온도계, contentDescription \"온도설정\"), Icons.Default.Calculate(계산기, \"과학적 표기법 변환기\")",
      why="<p>왼쪽 = navigationIcon(뒤로), 오른쪽 = actions(기능) — 1장 문제 26의 앱 바 구성요소(네비게이션 아이콘/액션 아이템)와 같은 배치.</p>"),
 dict(q="TurtleApp에서 TemperatureViewModel은 어디서 얻나? TurtleViewModel을 얻는 곳과 비교하시오.",
      a="<code>composable(Screen.Temperature.route) { val temperatureViewModel: TemperatureViewModel = viewModel(); … }</code> — <b>그 화면의 composable 블록 안</b>에서. TurtleViewModel은 TurtleApp 맨 위(NavHost 밖)에서 얻었다.",
      why="<p>composable 블록 안에서 viewModel()을 부르면 그 목적지의 NavBackStackEntry에 연동된다(문제 15).</p>")],
quote=quote("위와 같이 sealed class 를 만들면, 앱의 전체 화면 구성을 한 눈에 파악할 수 있습니다.", s(48, 50, 51, 52, 53, 60, 61))))

# 19
sci_q, sci_a = fill(["입력", "숫자 문자 개수", "화면에 보이는 결과"], [
    ["123", ("?", "3"), ("?", "123(그대로)")], ["12345677889", ("?", "11"), ("?", "1.2e10")], ["1234567890", ("?", "10"), ("?", "1234567890(10 초과가 아니라 그대로)")],
    ["98765432100", ("?", "11"), ("?", "9.9e10")], ["-12345678901", ("?", "11('-'는 숫자 문자가 아님)"), ("?", "-1.2e10")],
    ["00000000000(0이 11개)", ("?", "11"), ("?", "0.0 × 10⁰")], ["12a", ("?", "—"), ("?", "12a(숫자로 바뀌지 않아 그대로)")]])
P(dict(kind=["calc", "diag"], title="과학적 표기법 변환기",
intro="NumberFormatViewModel의 displayText 규칙: 입력이 숫자로 바뀌지 않으면 입력을 그대로 보여 준다. 숫자이면 입력 문자열에서 <b>숫자 문자의 개수</b>(digitCount)를 세어 <b>10 초과</b>(<code>digitCount &gt; 10</code>)일 때만 과학적 표기법으로, 아니면 입력 그대로. 변환: 값이 0.0이면 \"0.0 × 10⁰\", 아니면 exponent = floor(log10(|값|))(정수), mantissa = 값 / 10^exponent, 결과 \"%.1fe%d\"(가수부 소수 첫째 자리, 지수부 정수).",
parts=[
 dict(q="과학적 표기법 변환기에 다음을 입력했을 때 결과를 쓰시오." + sci_q, a=sci_a,
      why="<p>지수 = \"소수점을 몇 칸 옮겨야 1~10 사이가 되나\": 12345677889 → 1.2345677889로 10칸 → e10. %.1f는 반올림: 9.876… → 9.9, 1.234… → 1.2. 음수는 abs로 지수를 구하고 가수에 부호가 남는다.</p>"),
 dict(q="과학적 표기법 변환에서 0을 따로 처리하는 이유는?",
      a="입력값이 0이면 log10(0)을 계산할 수 없어 연산 과정에서 불능 현상이 생기므로, 조건문으로 먼저 0.0에 대한 표기값을 문자열로 처리."),
 dict(q="원본 본문은 \"숫자의 자리수가 10 이상이면\" 변환한다고 했다. 코드·실행 화면과 비교하면 무엇이 다르고, 정확히 10자리 숫자에서 결과가 어떻게 갈리나?",
      a="코드는 <code>digitCount &gt; 10</code>(10 <b>초과</b>), 실행 캡처도 \"10자리 초과 경우\". 본문 기준(10 이상)이면 10자리도 변환되지만, 코드·실행 기준이면 <b>10자리는 그대로</b>. 시험에서는 근거(코드 &gt; 10)를 함께 적는 것이 안전.",
      why="<p>본문과 코드의 불일치는 이 교재에서 정답 기준이 흔들리는 대표 지점 — 문제에 \"코드 기준\"인지 단서가 있는지 확인.</p>"),
 dict(q="NumberScreen 입력창의 <code>singleLine = true</code>는 무엇을 하나? 이 화면을 앱에 붙이기 위해 고친 곳 4가지는?",
      a="입력창의 높이를 <b>1줄로 제한</b>. ① NumberFormatViewModel 작성 ② NumberScreen(UI) 작성 ③ TurtleScreen에 onNavigateToScientific 파라미터와 actions의 계산기 버튼 추가 ④ Screen에 object Calculate(route \"scientific\")를 등록하고 NavHost에 composable(Screen.Calculate.route) 추가")],
fig=slide("ppa4", 62, 90),
quote=quote("숫자의 자리수가 10 이상이면, 10진수의 과학적 표기법으로 변환해서 화면에 보여주는 간단한 화면을 구성해 보자.", s(55, 56, 57, 59, 60, 61, 62))
 + "<p><span class='fix'>원본 s55 \"10 이상\" ↔ 코드 s56 \"digitCount &gt; 10\" ↔ 캡처 s62 \"10자리 초과\" 불일치</span></p>"))

# 20
P(dict(kind=["name"], title="LazyColumn이 대신하는 것",
parts=[
 dict(q="Compose의 LazyColumn은 안드로이드 View 시스템의 어떤 컴포넌트에 대응하나? 화면 밖으로 나간 항목은 어떻게 처리하나? 주로 쓰이는 UI 예를 쓰시오. 리스트에서 추가로 제어할 수 있는 것은?",
      a="<b>RecyclerView</b>(원본 표기 RecycleView). Column과 달리 실제로 화면에 보이는 항목만 컴포지션(생성)하고, 스크롤되어 화면 밖으로 나간 항목은 <b>재사용</b>. 채팅 목록, 상품 목록, 뉴스 피드, 설정 항목 리스트 등 항목 수가 가변적이거나 많은 세로 스크롤 UI. 리스트의 전체 여백/간격.",
      why="<p>Recycler = 재활용. 이름 그대로 \"화면 밖 항목을 재활용\"하는 View 방식의 리스트가 Compose에서 LazyColumn이다. 2장 문제 10(LazyColumn vs Column)의 마지막 조각.</p>")],
quote=quote("안드로이드 View 시스템의 RecycleView 에 대응하는 Compose 컴포넌트", s(63))))

KEYWORDS = [
 ("Live Edit", "앱을 실행해 둔 상태에서 코드를 수정하면 재빌드·재시작 없이 변경 사항이 즉시 반영되는 기능. Composable 함수의 본문에만 적용", s(6)),
 ("HAL (Hardware Abstraction Layer)", "제조사마다 다르게 구현된 하드웨어 부분을 표준화된 인터페이스로 감싸 상위 계층이 동일한 방식으로 접근하게 하는 계층", s(7)),
 ("Java API Framework", "개발자가 직접 다루는 시스템 서비스의 집합(Activity Manager, Window Manager, View System, Content Providers, Notification Manager)", s(8)),
 ("관심사 분리 (Separation of Concerns)", "UI, ViewModel, Repository/데이터 layer의 역할을 철저히 분리하는 원칙", s(9)),
 ("데이터 모델에서 UI 도출 (Drive UI from Data Models)", "데이터 모델이 먼저 변하면 화면이 그 변화를 감지하고 자동으로 그려져야(구독) 한다는 원칙", s(9)),
 ("단일 진실 공급원 (SSOT, Single Source of Truth)", "앱 안에서 특정 데이터의 실주인(진실)은 한곳에만 있어야 한다는 원칙", s(9)),
 ("데이터 캡슐화 (Data Encapsulation)", "실질적인 주인(ViewModel)만 데이터를 수정할 수 있도록 숨겨 두는(private) 기술", s(9)),
 ("UDF (단방향 데이터 흐름)", "데이터는 위에서 아래로 흐르고, 이벤트는 아래에서 위로 전달된다", s(10)),
 ("ViewModel", "UI 관련 데이터를 화면 회전이나 configuration 변경에도 유지되도록 설계된 클래스(Android Architecture Components)", s(11)),
 ("Fragment", "Activity 내부에 포함되어 재사용 가능한 UI 조각(module)을 구성하는 컴포넌트", s(11)),
 ("UI 상태", "특정 시점에 UI가 실제로 무엇을 보여줘야 하는지에 대한 데이터 값. 바뀌면 recomposition", s(12)),
 ("UI 로직", "UI 상태값을 어떻게 바꿀지를 결정하는 규칙 또는 연산(유효성 검사, 파생 상태 계산 등)", s(12)),
 ("layout", "ViewGroup의 subclass. 여러 개의 자식 뷰를 규칙에 의해 화면에 배치", s(13)),
 ("widget", "View의 subclass. 단독으로 사용해서 고유한 모양이나 기능을 가지는 요소", s(13)),
 ("android:alpha", "View의 투명도(0.0 완전 투명 ~ 1.0 완전 불투명). layout 공간은 그대로", s(14)),
 ("View.GONE", "보이지 않으면서 공간 차지도 없게(View.INVISIBLE은 안 보이지만 공간은 차지)", s(15)),
 ("android:layout_gravity", "이 View가 부모인 ViewGroup 안에서 어느 위치에 배치될지(gravity는 View 안의 내용물 정렬)", s(16)),
 ("android:contentDescription", "스크린 리더 등 접근성 도구가 View를 읽어 줄 때 사용하는 설명 문구", s(17)),
 ("sp", "사용자의 시스템 폰트 크기 설정에 비례해서 커지는 글자 크기 단위(dp는 고정)", s(17)),
 ("FLAG_KEEP_SCREEN_ON", "Compose에서 keepScreenOn을 구현할 때 Activity의 window에 거는 flag", s(20)),
 ("NavHost", "route(경로 문자열)에 따라 어떤 화면을 보여줄지 전환해 주는 Navigation Compose의 컨테이너", s(22)),
 ("딥링크", "알림 등을 눌러서 특정 화면으로 즉시 이동시키는 기능", s(22)),
 ("libs.versions.toml (Version catalog)", "key = value와 [섹션] 위주의 최소한의 설정 파일 형식. Canary 12부터 의존성 지정의 기본 방식", s(23)),
 ("rememberNavController()", "NavHost에 넘길 내비게이션 컨트롤러를 만들어 기억(보충)", s(26)),
 ("private set", "읽기는 클래스 바깥에서 가능하지만 쓰기(재할당)는 클래스 내부로만 제한", s(33)),
 ("vector icon (ImageVector)", "Material Icons 라이브러리가 제공하는 그래픽 데이터. 기기 무관 동일, tint로 색 변경", s(40)),
 ("Navigation", "화면을 고유한 route로 등록하고, 경로를 이용해 화면 간 이동과 뒤로 가기(back stack)를 관리하는 것", s(42)),
 ("백 스택 (Back Stack)", "LIFO 구조. 새 화면은 최상단에 push, 백 버튼은 최상단을 pop", s(43)),
 ("NavBackStackEntry", "Navigation-Compose가 각 목적지마다 만드는 항목. viewModel()이 여기에 연동되고, 그래프에서 완전히 제거될 때 onCleared() 호출", s(44)),
 ("companion object", "인스턴스마다 존재하지 않고 클래스 자체에 단 하나만 존재하는 값을 담는 블럭", s(45)),
 ("custom getter", "backing field 없이 접근할 때마다 get() 블록 전체가 실행되어 값을 정하는 속성", s(46)),
 ("backing field", "일반 속성의 계산된 값이 저장되는 내부 저장 공간", s(46)),
 ("nullable type marker (?)", "타입 뒤의 ?. 그 타입이 null을 가질 수 있다는 뜻", s(47)),
 ("안전호출연산자 (safe call, ?.)", "null이 아니면 실행하고, null이면 전체 식이 null", s(47)),
 ("엘비스연산자 (Elvis operator, ?:)", "식1이 null이 아니면 그 값, null이면 식2를 실행", s(47)),
 ("toDoubleOrNull()", "문자열을 Double로 변환하되, 실패하면 null을 반환하는 확장 함수", s(47)),
 ("sealed class", "Screen처럼 앱의 화면(route)들을 한곳에 묶어 전체 화면 구성을 한눈에 파악하게 하는 클래스", s(51)),
 ("object (Kotlin)", "앱에서 유일한 하나만 존재하는 것(거북이 화면 등)을 선언", s(51)),
 ("popBackStack()", "navController로 백 스택 최상단 화면을 제거해 이전 화면으로 돌아가기", s(53)),
 ("RecyclerView", "LazyColumn이 대응하는 안드로이드 View 시스템의 리스트 컴포넌트(화면 밖 항목 재사용)", s(63)),
]

OUTRO = """
<h3>4장 범위 대조표 — 슬라이드 → 문제</h3>
""" + table(["슬라이드", "내용", "문제"], [["s2~5", "화면·설정·프로젝트 관리", "1"], ["s6", "Live Edit", "2"], ["s7~8", "5계층(HAL)", "3"], ["s9~10", "아키텍처 원칙·private", "4"],
 ["s11~12", "ViewModel·UI 상태/로직", "5"], ["s13", "layout·widget", "6"], ["s14~17", "XML 공통 속성", "7"], ["s18~21", "Compose 대응", "8"], ["s22, 42", "NavHost·Navigation", "9"],
 ["s23~25", "toml", "10"], ["s25~28", "TurtleApp·간접 호출", "11"], ["s29~32", "ViewModel 연결·Home", "12"], ["s33~39", "TurtleViewModel 코드", "13"], ["s40", "이모지·벡터", "14"],
 ["s43~44, 53", "백 스택·수명", "15"], ["s45~47", "?·custom getter", "16"], ["s45~46, 49, 54", "온도 변환 결과", "17"], ["s48, 50~53, 60~61", "sealed class·화면 잇기", "18"],
 ["s55~62", "과학적 표기법", "19"], ["s63", "LazyColumn·RecyclerView", "20"]]) + """
<div class="note"><b>뺀 슬라이드</b>: s1 표지 / s41 Home 실행 캡처(문제 12에 포함) / s64 빈 쪽.</div>
<div class="note"><b>원본 오탈자·불일치</b>: s8 "C/C++ fh로" <span class="fix">→ C/C++로</span> / s9 "2가지 원칙" 아래 4개 항목(하위 항목 포함) / s47 번호 ①①①, "num.length" <span class="fix">→ name.length</span> / s55·56·62 "10 이상"·"&gt; 10"·"10자리 초과" 불일치 / s63 "RecycleView" <span class="fix">→ RecyclerView</span>.</div>
"""
