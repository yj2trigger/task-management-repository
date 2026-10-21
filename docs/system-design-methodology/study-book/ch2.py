"""2장 ppa2 — 프로젝트 구조·Jetpack·Compose 기초·Turtle Screen."""
from qbook2 import s as _s, quote, table, fill, slide


def s(*n):
    return _s(*n, deck="ppa2")


INTRO = """
<div class="note">소문제를 풀고 → 바로 아래 <b>답·해설</b>. 이중선(옅은 배경) = 문제, 가는 실선 = 답·해설, 굵은 실선 = 원문(원본 ppa2 슬라이드 번호·쪽 위/아래), 점선 = 해설 정리.
<span class="fix">빨간 글씨</span> = 원본 오탈자. 1장에서 이미 물은 지식은 다시 묻지 않고 "→ 1장 문제 N"으로 잇습니다.</div>
<h2>2장. ppa2 — 프로젝트 구조·Jetpack·Compose 기초·Turtle Screen</h2>
"""

ITEMS = []
P = ITEMS.append

# 1
P(dict(kind=["name", "mc"], title="안드로이드 프로젝트의 4구분과 매니페스트",
parts=[
 dict(q="안드로이드 프로젝트를 4가지로 구분하시오. 매니페스트에 담기는 것 두 종류와, 매니페스트 파일 이름에 관한 규칙은?",
      a="(1) 매니페스트 (2) 코드 (3) 리소스 (4) 설정 파일(Gradle Scripts). 매니페스트 = 앱의 구성 요소들을 담고 있는 목록(Activity, 서비스, 브로드캐스트 수신기, 콘텐츠 제공자 목록) + 시스템에 전달할 요구사항. 파일 이름은 <code>AndroidManifest.xml</code>로 <b>고정</b>.",
      why="<p>매니페스트는 시스템에 내는 <b>신고서</b>: 무엇이 들어 있는지(구성요소 목록) + 무엇이 필요한지(요구사항, 예: 6장 INTERNET 권한).</p>"),
 dict(q="안드로이드 프로젝트의 코드 부분(kotlin+java)에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("현재 안드로이드 개발은 Kotlin이 사실상 표준이다.", True, "현재 안드로이드 개발은 Kotlin이 사실상 표준이라, 프로젝트 템플릿의 기본 언어도 Kotlin이다(1장)."),
            ("메인 코드는 com.example.hello처럼 패키지명 뒤에 괄호가 붙지 않는다.", True, "패키지명 뒤에 괄호가 없는 com.example.hello는 실제 앱을 구동하는 메인 코드다. 그 안의 MainActivity.kt가 앱이 실행될 때 처음 켜지는 메인 소스."),
            ("com.example.hello (test)는 에뮬레이터에서 UI나 화면 흐름을 검증한다.", False, "com.example.hello (test)는 <b>컴퓨터 CPU 자체에서 순수 로직</b>을 검증하는 공간이다."),
            ("com.example.hello (androidTest)는 컴퓨터 CPU 자체에서 순수 로직을 검증한다.", False, "com.example.hello (androidTest)는 <b>에뮬레이터에서 UI나 화면 흐름</b>을 검증한다."),
            ("테스트 코드는 패키지명 뒤 괄호에 용도가 적혀 있다.", True, "테스트 코드는 패키지명 뒤 괄호에 (androidTest), (test)처럼 용도를 표시한다.")],
      a="ⓐ ⓑ ⓔ",
      why="<p>괄호 이름으로 판단: <b>android</b>Test에는 \"android\"가 들어 있다 → 안드로이드(기기·에뮬레이터)가 필요 → UI 검증. 1장 문제 22의 계측 테스트와 같은 것.</p>")],
fig=slide("ppa2", 2, 85),
quote=quote("매니페스트(manifest) 앱의 구성 요소들을 담고 있는 목록입니다.", s(2, 3))))

# 2
P(dict(kind=["diag", "mc"], title="리소스 폴더의 규칙 (res vs assets, View vs Compose)",
parts=[
 dict(q="리소스를 정의하시오. 안드로이드 프로젝트의 <code>res/drawable/</code>에 <code>Dog-3.PNG</code>를 넣었더니 빌드 오류가 났다. 이유는? 같은 파일을 이름·종류 제약 없이 두고 싶다면 어느 폴더에 두나? 그 폴더는 처음 프로젝트에 있나?",
      a="리소스 = 응용프로그램이 사용할 자원. res 폴더의 리소스 파일 이름은 <b>a~z, 0~9, _, .</b> 으로만 구성되어야 한다(대문자 D·P·N·G와 하이픈 - 위반). <b>assets</b> 폴더(리소스 파일의 이름이나 종류에 제약 없음). 초기 프로젝트에는 res 폴더만 있고, assets는 개발자가 따로 생성.",
      why="<p>res와 assets는 \"<b>시스템이 관리하나</b>\"로 구분: res는 R 클래스로 등록되므로(1장 문제 13 가로줄 폴더) 이름 규칙이 엄격하고, assets는 그냥 파일 묶음이라 자유롭다. 6장에서 배경 사진 파일 이름을 \"영어 소문자와 숫자\"로 바꾸는 이유도 이 규칙.</p>"),
 dict(q="res 폴더의 하위 폴더 이름(drawable, mipmap, values, xml)이 정하는 것은?",
      a="그 하위 폴더에 넣을 수 있는 <b>파일의 종류</b>(제약)."),
 dict(q="View 방식과 Compose 방식의 res 구조 비교로 옳은 것을 모두 고르시오.",
      opts=[("View 방식의 res/layout/activity_main.xml은 Compose 프로젝트에도 그대로 있다.", False, "Compose 프로젝트에는 res/layout/activity_main.xml이 <b>없고</b>, MainActivity.kt 안의 <b>@Composable 함수</b>가 대신한다."),
            ("values/(strings.xml, colors.xml, themes.xml)는 Compose에서도 그대로 사용된다.", True, "values/는 Compose에서도 그대로 쓰이지만, res/values/themes.xml은 <b>창 테마용으로 축소</b>되고 색은 <b>ui/theme/Theme.kt</b>로 대응."),
            ("drawable/의 벡터 드로어블은 Compose에서도 그대로 사용된다.", True, "drawable/의 벡터 드로어블(그림 재료)은 Compose에서도 그대로 사용된다."),
            ("mipmap-*/의 런처 아이콘은 Compose에서 쓰지 않는다.", False, "mipmap-*/의 런처 아이콘도 Compose에서 <b>그대로 사용</b>된다."),
            ("xml/의 백업 규칙 등은 Compose에서도 그대로 사용된다.", True, "xml/의 백업 규칙 같은 설정도 Compose에서 그대로 사용된다.")],
      a="ⓑ ⓒ ⓔ",
      why="<p>Compose에서 바뀐 것은 \"<b>화면을 그리는 것</b>\"(layout XML → @Composable)뿐이고, 문자열·그림·아이콘·백업 규칙 같은 재료는 그대로다.</p>")],
quote=quote("res 폴더의 리소스 파일들은 a~z,0~9, _,. 으로만 구성되어야 하며, 하위 폴더(drawable..)의 이름에 따라, 넣을 수 있는 파일의 종류에 제약이 있다.", s(4, 30))))

# 3
P(dict(kind=["name", "diag"], title="XML 문법과 매니페스트 읽기",
parts=[
 dict(q="XML 용어: <code>&lt;color name=\"black\"&gt;#FF000000&lt;/color&gt;</code>에서 ⓐ 짝을 이루는 태그 쌍 전체 ⓑ name ⓒ #FF000000 의 이름은? ⓓ AndroidManifest.xml에 자주 보이는 <code>android:</code> 는 무엇인가?",
      a="ⓐ element ⓑ 속성 ⓒ text data ⓓ 안드로이드 시스템의 고유 속성임을 알리는 <b>namespace의 접두사</b>",
      why="<p>colors.xml은 &lt;resources&gt;라는 상위 element 안에 &lt;color&gt; element가 있고, 그 안에 text data, 속성은 name. 객관식에서 \"속성\"과 \"text data\"를 바꾸는 선지에 대비.</p>"),
 dict(q="XML 문법: ⓐ 한 XML 파일에 최상위 element를 두 개 두었다. 허용되나? ⓑ text data가 없는 element를 짧게 쓰는 법은? ⓒ XML이 HTML보다 확장성이 높은 이유와, XML의 장점 두 가지는?",
      a="ⓐ 불가. 최상위 element는 <b>1개</b>로 제약이 있다. ⓑ <code>&lt;태그명&gt;&lt;/태그명&gt;</code> 대신 <code>&lt;태그명 /&gt;</code> 단축형 ⓒ 개발자가 <b>자신만의 tag를 정의</b>할 수 있어서. 이식성이 높고, 구조가 엄격해 자동화 처리가 용이하다."),
 dict(q="AndroidManifest.xml의 최상위 element는? 그 안 activity의 intent-filter에 MAIN 액션과 LAUNCHER 카테고리가 있으면 무슨 뜻인가?",
      a="<code>&lt;manifest&gt;</code>. 그 액티비티가 앱을 실행했을 때 처음 뜨는 <b>진입점</b>이라는 뜻(1장 문제 17: 시스템이 매니페스트에서 MAIN + LAUNCHER 액티비티를 찾아 실행).")],
fig=slide("ppa2", 6, 85),
quote=quote("보통 &lt;mainfest&gt;&lt;/mainfest&gt;, &lt;resources&gt;&lt;/resources&gt; 처럼 짝을 이루는 것을 element 라고 한다. 최상위 element 는 1개로 제약이 있다.", s(5, 6))
 + "<p><span class='fix'>원본 s5 \"mainfest\" → manifest</span></p>"))

# 4
gr_q, gr_a = fill(["Gradle 설정 파일", "무엇을 지시하나"], [
    ["settings.gradle.kts", ("?", "프로젝트에 사용되는 모듈")], ["build.gradle.kts (Project)", ("?", "모든 모듈에 공통 적용되는 플러그인 버전")],
    ["build.gradle.kts (Module: app)", ("?", "이 앱 모듈만의 SDK/의존성 설정(navigation, viewmodel 등 라이브러리)")], ["libs.versions.toml", ("?", "위에서 사용할 라이브러리 이름–버전 사전")],
    ["gradle-wrapper.properties", ("?", "빌드 도구(Gradle) 자체의 버전")], ["gradle.properties", ("?", "빌드 도구의 동작 옵션(JVM 메모리 크기, AndroidX 사용 여부 등)")],
    ["local.properties", ("?", "local 컴퓨터에만 해당하는 경로(SDK 로컬 경로 등), Git에서 제외")]])
P(dict(kind=["table", "name"], title="Gradle 설정 파일 7개의 층위",
parts=[
 dict(q="Gradle이 무엇을 하는 도구인지 한 줄로 쓰고, 안드로이드 프로젝트의 Gradle Scripts 7개 파일이 각각 무엇을 지시하는지 표를 채우시오." + gr_q,
      a="Gradle = 안드로이드 프로젝트를 빌드(컴파일 및 패키징)하는 도구. Gradle Scripts의 파일들은 모두 Gradle이 프로젝트를 어떻게 빌드할지를 <b>다른 층위에서</b> 지시하는 설정 파일." + gr_a,
      why="<p>층위로 외운다: <b>무엇을 묶나</b>(settings) → <b>공통으로</b>(Project) → <b>이 모듈만</b>(app) → 그 안에서 쓰는 <b>버전 사전</b>(toml). 도구 자체에 관한 셋: <b>어떤 Gradle</b>(wrapper = 버전) / <b>어떻게 돌릴지</b>(gradle.properties = 동작 옵션, 라이브러리·코드와 무관) / <b>내 PC 경로</b>(local.properties, Git에 절대 올리지 않음). wrapper와 gradle.properties를 바꾸는 선지가 함정.</p>"),
 dict(q="settings.gradle.kts가 가리키는 모듈 3종은? ⓐ MainActivity, NavHost만 있는 실행의 진입점 ⓑ 여러 화면이 공통으로 쓰는 유틸리티, 테마 ⓒ 자체로 실행되지는 않지만 특정 기능 코드만 따로 컴파일되는 코드 전체",
      a="ⓐ app 모듈 ⓑ core 모듈 ⓒ feature 모듈. (모듈 = Project 단위에서 독립적으로 빌드될 수 있는 코드 전체)"),
 dict(q="앱을 빌드할 때 코드를 압축하고 이름을 바꾸는 과정에서, 특정 파일이나 클래스의 이름이 바뀌지 않도록 보호하는 설정의 이름과 파일 이름은? 그 과정을 무엇이라 부르나?",
      a="KeepRules, <code>rules.keep</code>. 코드 난독화(Obfuscation) — KeepRules는 난독화 방지 기능.")],
fig=slide("ppa2", 8, 85),
quote=quote("KeepRules 도 일종의 설정 파일인데, 앱을 빌드할 때, 코드를 압축하고 이름을 바꾸는 과정에서, 특정 파일이나 클래스의 이름이 바뀌지 않도록 보호해 주는 코드 난독화(Obfuscation) 방지 기능을 rules.keep 로 설정한다", s(7, 8, 9, 10))))

# 5
P(dict(kind=["mc", "name"], title="APK의 정체와 앱의 4대 구성요소",
parts=[
 dict(q="안드로이드 앱 설치 파일(.apk)에 대한 설명으로 옳지 <b>않은</b> 것을 모두 고르시오.",
      opts=[(".apk는 내부적으로 표준 zip 형식이라, 확장자를 .zip으로 바꾸면 zip 프로그램으로 내용을 볼 수 있다.", True, "안드로이드 최종 설치 형식인 .apk는 표준 zip 형식이라, 확장자를 .zip으로 바꾸면 zip 프로그램으로 내용을 볼 수 있다."),
            ("디버그 빌드의 app-debug.apk는 난독화되어 있고, 릴리스 빌드의 app-release.apk는 난독화되어 있지 않다.", False, "반대다. 디버그 빌드의 app-debug.apk는 <b>난독화 안 됨</b>, 릴리스 빌드의 app-release.apk는 <b>난독화됨</b>."),
            (".apk는 manifest + code + resource로 구성되고, 개발자가 누구인지 알 수 있도록 디지털 서명이 되어 있다.", True, ".apk는 manifest + code + resource 세 가지로 구성되고, 개발자를 알 수 있도록 디지털 서명이 되어 있다(1장 문제 16)."),
            (".apk 안의 코드는 .class 확장자로 들어 있다.", False, ".apk 안의 코드는 .class가 아니라 <b>.dex(dalvik executable)</b> 확장자다(1장 문제 14의 D8/R8이 만든 결과물)."),
            ("디버그 빌드 결과는 '프로젝트/app/build/outputs/apk/debug' 폴더에 생긴다.", True, "디버그 빌드 결과는 '프로젝트/app/build/outputs/apk/debug', 릴리스 빌드 결과는 '…/apk/release' 폴더에 생긴다. .apk를 우클릭 → Open In → Explorer로 열어 볼 수 있다.")],
      a="ⓑ ⓓ",
      why="<p>난독화 = 남이 읽기 어렵게 — 사용자에게 나가는 release에만 적용한다고 추론. 빌드 흐름(바이트코드 → DEX → 패키징 → 서명)을 알면 APK 안에 무엇이 있는지가 자동으로 나온다.</p>"),
 dict(q="안드로이드 앱의 4대 구성요소는? 화면이 5개인 앱의 Activity 수는? Activity를 안드로이드 시스템이 인식하려면? 앱의 전체 Activity 목록을 보려면 어느 파일을 보나?",
      a="액티비티, 서비스, 브로드캐스트 수신기, 콘텐트 제공자. 5개(Activity는 앱의 화면에 <b>1:1</b>로 대응). <b>Manifest에 등록</b>해야 인식. Manifest 파일.")],
quote=quote(".apk 는 manifest + code +resource 로 구성되어 있으며, 개발자가 누구인지 알 수 있도록, 디지털 서명이 되어 있다. 여기서 코드는 .dex (dalvik executable) 의 확장자로 나타난다.", s(11, 12))))

# 6
P(dict(kind=["diag", "order"], title="IDE에선 되는데 터미널 ./gradlew는 실패 (JAVA_HOME)",
parts=[
 dict(q="Android Studio에서는 빌드와 Gradle Sync가 잘 되는데, PowerShell에서 <code>./gradlew</code>를 실행하니 Java를 찾을 수 없다는 오류가 난다. ⓐ Android Studio에서는 왜 환경 변수 없이 되나? ⓑ gradlew는 무엇이며, 왜 Android Studio의 설정을 모르나?",
      a="ⓐ IDE 자체가 실행될 때 내장된 <b>jbr</b>을 JVM으로 쓰고, Gradle Sync도 <b>Gradle Tooling API</b>를 통해 IDE 프로세스 안에서 직접 Gradle을 호출하므로, jbr 경로를 IDE가 이미 안다. ⓑ 단순한 shell script/배치 파일. 이것이 실행되는 PowerShell 창은 Android Studio와 <b>별개의 운영체제 프로세스</b>라서.",
      why="<p>\"어디서 실행되나(프로세스)\"가 열쇠. 같은 PC라도 IDE 프로세스가 아는 것을 별개 프로세스(터미널)는 모른다. 1장 문제 4(JBR 동봉)와 이어진다 — JBR은 있지만 IDE 안에서만 쓰이는 셈.</p>"),
 dict(q="gradlew 스크립트가 Java를 찾는 순서 3단계는?",
      a="환경 변수 <b>JAVA_HOME</b>이 설정되어 있는지 확인 → 없다면 시스템 <b>PATH</b>에서 java 명령을 찾음 → 둘 다 없으면 오류 출력"),
 dict(q="해결: Windows 환경 변수에 만들 시스템 변수의 이름과 값은? Path에 추가할 항목은?",
      a="변수 이름 <b>JAVA_HOME</b>, 값 <code>C:\\Program Files\\Android\\Android Studio\\jbr</code>. Path에 <code>%JAVA_HOME%\\bin</code> 추가.")],
quote=quote("gradlew 는 단순한 shell script/ 배치 파일이며, 이 스크립트가 실행되는 Powershell 창은 Android studio 와는 별개의 운영체제 프로세스입니다.", s(13, 14, 31))))

# 7
jp_q, jp_a = fill(["Jetpack 분류", "구성요소와 역할"], [
    ["아키텍처(Architecture): 앱의 구조를 만들고 유지 보수 및 테스트를 돕는 로직 중심", ("?", "Compose: UI 및 상태관리, 로직 흐름을 선언형 인터페이스 구조로 연결하는 핵심 아키텍처 패러다임 / ViewModel: 데이터의 수명 주기 관리 / LiveData: 데이터 변경 관찰 / Hilt: 의존성 주입(클래스가 필요한 객체를 외부에서 가져와 사용하는 방식)")],
    ["화면의 구성 요소: 사용자가 보고 상호작용하는 시각적인 화면 레이어", ("?", "XML 템플릿: 화면 layout을 정의하는 정적 마크업 파일 구조 / UI 구성 요소: 화면의 일부분을 담당하는 Fragment나 Material Design 컴포넌트 툴킷(기기별 화면 크기에 맞춤)")],
    ["시스템 전체의 구성요소(Data 및 Infrastructure): 데이터를 안전하게 저장하고 로컬·외부 네트워크와 연결하는 백엔드 데이터 레이어", ("?", "Data: SQLite 기반의 Room 데이터베이스, 가벼운 Key-value 저장을 위한 DataStore / Infrastructure: 백그라운드에서 예약된 작업을 안정적으로 실행하는 WorkManager")]])
P(dict(kind=["table", "mc"], title="Android Jetpack의 3분류",
parts=[
 dict(q="Android Jetpack과 AndroidX의 관계를 쓰시오. Jetpack은 언제, 누가 만들었나?",
      a="Jetpack = <b>2018년</b> 구글이 안드로이드 개발에 필요한 구성요소들을 모아 놓은 <b>제품군</b>. AndroidX = Jetpack을 구성하는 <b>실제 라이브러리 이름</b>."),
 dict(q="Jetpack 3분류 표를 채우시오(Compose, ViewModel, LiveData, Hilt, XML 템플릿, Fragment, Material Design 컴포넌트, Room, DataStore, WorkManager)." + jp_q, a=jp_a,
      why="<p>함정 1순위: <b>Compose는 \"화면의 구성 요소\"가 아니라 \"아키텍처\"</b>에 있다 — 원문이 Compose를 \"UI·상태관리·로직 흐름을 잇는 아키텍처 패러다임\"으로 정의했기 때문. Data와 Infrastructure: 저장하면 Data(Room·DataStore), 작업을 돌리면 Infrastructure(WorkManager).</p>")],
quote=quote("Compose: 최신 안드로이드 가이드에서, UI 및 상태관리, 로직 흐름을 선언형 인터페이스 구조로 연결하는 핵심 아키텍처 패러다임 입니다.", s(15, 16, 17))))

# 8
vc_q, vc_a = fill(["비교 항목", "명령형: View 시스템(XML)", "선언형: Compose"], [
    ["무엇을 지시하나", ("?", "어떻게(How) 바꿀지 순서대로 명령 — 'TextView 객체를 찾아서 Text()를 바꿔'"), ("?", "무엇을(What) 보여 줄지만 선언 — '현 상태가 이렇다면 화면은 이런 모습이어야 해'")],
    ["화면 객체", ("?", "화면에 만들어진 View 객체가 메모리에 살아 있음"), ("?", "따로 객체를 관리할 필요가 없음(렌더링은 내부 처리)")],
    ["관리 방식", ("?", "객체 트리(View Hierarchy)를 참조해 객체의 속성을 하나씩 명령으로 바꿈"), ("?", "Text() 등 필요한 함수를 호출, 실행될 때마다 UI를 표현하는 가벼운 설명(구조)을 새로 만듦")],
    ["상태가 바뀌면", ("?", "개발자가 직접 객체 속성을 변경"), ("?", "Compose 런타임이 '다시 그려야 할 부분만' 알아서 다시 실행(리컴포지션)")]])
P(dict(kind=["table", "essay"], title="명령형(View) vs 선언형(Compose) — 내부에서 다른 점",
parts=[
 dict(q="View와 Compose를 비교하는 표를 채우시오." + vc_q, a=vc_a,
      why="<p>1장 문제 9에서는 \"누가 고치나\"만 물었다. 여기서는 그 결과다: 명령형은 객체가 <b>계속 살아 있어서</b> 찾아가 고쳐야 하고, 선언형은 매번 <b>새 설명을 만들고</b> 바뀐 부분만 다시 실행한다.</p>"),
 dict(q="리컴포지션을 정의하시오.",
      a="상태가 바뀌었을 때 Compose 런타임이 <b>다시 그려야 할 부분만</b> 알아서 다시 실행해 화면을 갱신하는 것.")],
quote=quote("Compose 에서는 상태가 바뀌면, Compose 런 타임이 '다시 그려야 할 부분만' 을 알아서 다시 실행 (리컴포지션)해서 화면을 갱신합니다.", s(18))))

# 9
P(dict(kind=["name", "diag"], title="Compose의 부모·자식과 람다",
parts=[
 dict(q="Compose 코드 <code>Scaffold(topBar = { TurtleTopBar() }) { innerPadding -&gt; Box { … } }</code>에서 부모와 자식을 모두 쓰시오. 크기와 위치의 결정 규칙은 어느 방향으로 흐르나? <code>fillMaxSize()</code>의 기준은?",
      a="부모: Scaffold / 자식: TurtleTopBar(), Box(). Layout은 트리 구조이고, 결정 규칙은 부모와 자식 관계에 맞춰 <b>위에서 아래로</b> 흐른다. fillMaxSize()는 <b>부모가 허용하는 최대 크기</b>를 기준으로 계산하므로 부모의 크기가 자식의 크기에 영향을 준다."),
 dict(q="Kotlin 람다: ⓐ 정의와 쓰임 ⓑ Compose에서 { }로 둘러싸인 코드 블록의 정체 ⓒ = 와 -&gt; 의 역할 ⓓ 함수의 마지막 파라미터가 람다일 때 Kotlin이 허용하는 표기",
      a="ⓐ 이름 없는 함수. 나중에 실행할 코드 뭉치를 변수처럼 다른 함수에 값으로 전달할 때 사용 ⓑ 대부분 람다 ⓒ <code>=</code>: 파라미터에 값 또는 람다를 대입 / <code>-&gt;</code>: 람다 안에서 파라미터 목록과 실행할 코드를 구분 ⓓ 괄호 밖으로 빼서 { }로 쓸 수 있다(trailing lambda)"),
 dict(q="<code>Button(onClick = { println(\"클릭됨\") }) { Text(\"누르세요\") }</code>에 람다는 몇 개이고, 각각 어느 파라미터에 넘어가나? <code>val greet = { println(\"Hello\") }</code>를 실행하려면?",
      a="2개: <code>{ println(…) }</code> → onClick, <code>{ Text(…) }</code> → <b>content</b>. <code>greet()</code>로 나중에 호출.",
      why="<p>괄호 밖 <code>{ Text(...) }</code>도 람다다. \"마지막 파라미터면 괄호 밖으로\" 규칙 때문에 모양이 달라 보일 뿐. Scaffold의 <code>{ innerPadding -&gt; … }</code>도 같은 규칙: content 파라미터에 넘기는 trailing lambda이고, -&gt; 왼쪽이 파라미터 이름(문제 16).</p>")],
quote=quote("아래 코드는 첫줄 뿐아니라, {Text(“누르세요”)} 도 content 라는 파라미터에 넘기는 람다입니다.", s(19, 20))))

# 10
lz_q, lz_a = fill(["비교 항목", "LazyColumn", "Column"], [
    ["항목 생성", ("?", "화면에 보이는 항목만 만들고, 화면 밖으로 나간 것은 버림"), ("?", "항목 생성을 전부 미리(한번에 composition)")],
    ["스크롤", ("?", "내장"), ("?", "없음 → verticalScroll()이 따로 필요")], ["항목 수", ("?", "무제한"), ("?", "유한 개로 지정, 나열하는 방식")],
    ["자식 지정", ("?", "items { … } — 중괄호 안은 LazyListScope라는 별도 영역"), ("?", "자식을 그대로 나열")]])
P(dict(kind=["diag", "table"], title="레이아웃 컴포저블 5종과 LazyColumn",
parts=[
 dict(q="Composable과 Layout Composable을 각각 정의하시오.",
      a="Composable = <code>@Composable</code> 어노테이션이 붙은 함수 전체(TurtleScreen 실습의 Text(), Button(), Turtle() 모두) / Layout Composable = 다른 Composable들을 <b>어떻게 배치할지</b> 담당하는 Composable."),
 dict(q="상황에 맞는 Layout Composable은? ⓐ 버튼 4개를 가로로 ⓑ 아이콘 아래에 글자를 세로로 ⓒ 거북이 위에 발자국을 겹쳐서 ⓓ topBar/bottomBar/content 정해진 자리에 ⓔ 학생 1만 명의 목록",
      a="ⓐ Row(자식들을 가로로 나열) ⓑ Column(자식들을 한번에 생성하고 세로로 나열, 스크롤 없음) ⓒ Box(자식들을 겹쳐서 배치) ⓓ Scaffold(정해진 슬롯에 배치) ⓔ LazyColumn(화면에 보이는 자식들만 세로로, 스크롤 내장)"),
 dict(q="LazyColumn과 Column을 비교하는 표를 채우시오. 학생 1만 명의 목록을 Column으로 만들면? LazyColumn은?" + lz_q,
      a=lz_a + "Column: 만 개의 text가 한꺼번에 생성되어 <b>앱이 멈춤</b> / LazyColumn: 화면에 보이는 <b>15개 정도만</b> 유지.",
      why="<p>Lazy = \"필요할 때까지 미룬다\". 미루니까 보이는 것만 만들고, 그래서 무제한이 가능하고, 스크롤로 새로 보일 때 만들어야 하니 스크롤이 내장. 4장 끝에서 LazyColumn이 View의 RecyclerView에 대응한다는 것을 본다.</p>")],
quote=quote("만약 학생 만명의 목록을 Column 으로 만들면 만 개의 text 가 한꺼번에 생성되어 앱이 멈추지만, LazyColumn 은 화면에 보이는 15개 정도만 유지합니다.", s(21, 22))))

# 11
P(dict(kind=["table", "name"], title="어노테이션(@)과 파라미터·시그니처",
parts=[
 dict(q="Kotlin·Java의 어노테이션(@)의 정체를 한 문장으로 쓰시오.",
      a="실행되는 것이 아니라, Compiler나 도구에게 그것이 <b>어떤 역할을 하는 것인지 알려 주는 표식</b>."),
 dict(q="어노테이션을 쓰시오. ⓐ 이 함수를 편집기에서 도구가 읽고 미리보기를 생성 ⓑ 이 함수가 UI를 그리는 함수, Compose compiler Plugin이라 컴파일러가 코드를 변형 ⓒ 상위 클래스의 메서드를 재정의 ⓓ 해당 클래스가 데이터베이스 테이블 ⓔ 해당 메서드가 이 SQL을 실행 ⓕ 해당 함수가 테스트 ⓖ Kotlin 표준 라이브러리 문법으로 \"명시적 동의\", 컴파일러 경고 해제 ⓗ Lint에 최소 API 수준을 알려 줌",
      a="ⓐ @Preview ⓑ @Composable ⓒ @Override ⓓ @Entity ⓔ @Query(\"SELECT …\") ⓕ @Test ⓖ @OptIn ⓗ @RequiresApi <span class='fix'>(원본 표기 @RequireApi)</span>",
      why="<p>Turtle Screen 코드에서 실제로 쓰인 것: <code>@OptIn(ExperimentalMaterial3Api::class)</code>(TopAppBar가 실험적 API라 동의 필요), <code>@Composable</code>, <code>@Preview(showBackground = true)</code>, <code>override fun onCreate</code>. @Entity·@Query는 Room(문제 7), @Test는 테스트(1장 문제 22)와 연결.</p>"),
 dict(q="함수의 파라미터와 시그니처를 정의하시오. Composable 함수의 파라미터를 확인하는 방법 3가지는?",
      a="파라미터 = 함수를 정의할 때 <b>괄호 안에 선언하는 값의 이름표</b> / 시그니처 = <code>함수이름(파라미터1:타입, 파라미터2:타입, …)</code> 형태 전체. 확인: ① Text나 Scaffold 같은 함수 이름에서 Ctrl+클릭(Mac은 cmd+클릭)으로 함수 정의로 이동 ② Text( 까지만 쳐도 파라미터를 팝업으로 보여 줌 ③ 시그니처 개념으로 이해")],
quote=quote("@는 Kotlin 과 Java 의 코드에 붙이는 표식으로 실행되는 것이 아니라, Compiler 나 도구에게 어떤 역할을 하는 것인지를 알려주는 표식입니다.", s(23, 24))))

# 12
tab_q, tab_a = fill(["TopAppBar 종류", "높이", "특징"], [
    ["TopAppBar", ("?", "64dp"), ("?", "제목 좌측 정렬, 기본형")], ["CenterAlignedTopAppBar", ("?", "64dp"), ("?", "제목 중앙 정렬")],
    ["MediumTopAppBar", ("?", "112dp"), ("?", "화면을 아래로 스크롤하면 높이가 축소")], ["LargeTopAppBar", ("?", "152dp"), ("?", "제목을 강조")]])
P(dict(kind=["name", "table"], title="MaterialTheme, TopAppBar와 BottomBar 꾸미기",
parts=[
 dict(q="Material Design 3 스펙이 정의한 MaterialTheme의 세 범주와 각 예시는?",
      a="colorScheme(색상 팔레트: primary, secondary, background, onSurface 등) / typography(글꼴 크기·굵기·자간 스타일: headlineLarge, bodyMedium 등) / shapes(버튼·카드 등의 기본 모서리 둥글기: small, medium, large)"),
 dict(q="Compose TopAppBar 4종의 높이와 특징 표를 채우시오. TopAppBar는 예전의 무엇과 같은 역할이며 그것은 언제 나왔나? 한 화면에 TopAppBar를 여러 개 넣을 수 있나?" + tab_q,
      a=tab_a + "API 11(2011)의 <b>ActionBar</b>. 가능하다(ComponentActivity를 쓰며 Compose tree 안에 위치하는 @Composable 함수로, 파라미터로 지정됨).",
      why="<p>높이는 64 → 64 → 112 → 152로 커지고, 이름(CenterAligned/Medium/Large)이 특징을 말해 준다. 1장 문제 23의 \"앱 바 높이 56(모바일)/64(데스크톱)dp\"는 dp 실무 값 목록이고, 이것은 Compose TopAppBar의 높이다.</p>"),
 dict(q="Turtle Screen의 TopAppBar를 꾸민다. ⓐ 배경을 테마의 기본 컨테이너 색으로, 제목 글자는 그 위에 잘 보이는 색으로 하려면 어떤 객체·파라미터에 어떤 두 색을 주나? ⓑ 제목 Text를 22sp, 굵게, Serif, 기울임으로 만드는 파라미터 4개는?",
      a="ⓐ <code>colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.primaryContainer, titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer)</code> ⓑ fontSize = 22.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Serif, fontStyle = FontStyle.Italic",
      why="<p>\"on○○\" 색 이름 규칙: <b>onPrimaryContainer = primaryContainer 위에 올라가는 글자색</b>. 배경과 글자를 짝으로 고른다.</p>"),
 dict(q="Turtle Screen의 BottomBar(Row)에서 버튼 4개를 균등한 간격으로 배치하는 파라미터와 값은? Row가 가로 폭을 꽉 채우게 하는 Modifier는?",
      a="<code>horizontalArrangement = Arrangement.SpaceEvenly</code>, <code>Modifier.fillMaxWidth()</code>(여기에 background 색과 padding(horizontal = 12.dp, vertical = 10.dp)을 이어 붙임)")],
quote=quote("TopAppBar : 높이가 64dp 로 제목은 좌측 정렬하여 나타내는 기본형입니다.", s(25, 35, 41, 42))
 + "<p><span class='fix'>원본 s25 MaterialTheme 슬라이드의 \"3 가지 방법을 통해 파라미터를 확인\" 문장은 앞 슬라이드에서 복사된 것으로 보임</span></p>"))

# 13
pad_q, pad_a = fill(["Modifier 함수", "포함하는 영역"], [
    ["systemBarsPadding()", ("?", "상태 표시줄 + 네비게이션 바")], ["safeDrawingPadding()", ("?", "상태 표시줄 + 네비게이션 바 + 컷아웃 + IME")],
    ["statusBarsPadding()", ("?", "상태 표시줄")], ["navigationBarsPadding()", ("?", "네비게이션 바")],
    ["displayCutoutPadding()", ("?", "컷아웃")], ["imePadding()", ("?", "키보드")]])
P(dict(kind=["diag", "table"], title="Edge-to-Edge 렌더링과 시스템 영역 패딩",
parts=[
 dict(q="Edge to Edge 렌더링을 정의하시오. 어떤 앱부터 적용되나? Turtle Screen의 MainActivity에서 이것을 켜는 함수와 그 역할은?",
      a="앱 콘텐츠가 상태 표시줄과 네비게이션 바 <b>뒤까지</b> 그려지는 것(화면을 끝까지 쓰고, 시스템 바는 그 위에 반투명하게). <b>Android 15(API 35)</b>부터 targetSDK를 35 이상으로 올린 앱. <code>enableEdgeToEdge()</code>: 상태 표시줄까지 화면을 확장해서 그려, 상태 표시줄 영역까지 앱이 관리."),
 dict(q="Edge-to-Edge에서 콘텐츠가 시스템 바에 가려지지 않게 여백을 계산하는 수단 3가지는?",
      a="① <b>Scaffold의 innerPadding</b>으로 앱 바와 시스템 영역을 합친 값 ② <b>WindowInsets.statusBars</b>로 개별 영역의 크기를 직접 조회 ③ <b>Modifier.safeDrawingPadding()</b>으로 안전 영역만큼 여백"),
 dict(q="safeDrawing = ? display cutout은 무엇이고, 세로와 가로에서 어떻게 다르게 나타나나?",
      a="시스템바(status + navigation) + display cutout(노치, 펀치홀) + IME(keyboard) — 그 뒤에 콘텐츠를 그리면 가려질 수 있는 <b>모든 영역의 합집합</b>. display cutout = 카메라 구멍이나 노치가 화면을 파고든 영역으로, 세로 상태에서는 상태 표시줄에 흡수되지만 <b>가로 회전 시 화면 옆쪽에 별도로</b> 나타난다.",
      why="<p>cutout의 이 성질이 6장 강아지 배경 실습(가로로 돌리면 카메라 쪽이 비는 현상)의 원인이 된다.</p>"),
 dict(q="Compose의 시스템 영역 패딩 함수 6개가 포함하는 영역을 쓰시오." + pad_q, a=pad_a,
      why="<p>WindowInsets 이름이 곧 답: system<b>Bars</b> = 바 두 개, <b>safe</b>Drawing = 가려질 수 있는 전부. \"safe가 가장 크다\"만 기억하면 다음 소문제도 풀린다.</p>"),
 dict(q="입력 화면에서 키보드가 올라올 때 화면 <b>전체</b>가 밀려 올라간다. 원인과 고치는 조합은?",
      a="safeDrawingPadding()이 키보드(IME)를 포함하고 있어서. <b>systemBarsPadding()</b>을 쓰고, 입력창에만 <b>imePadding()</b>을 넣는다."),
 dict(q="에뮬레이터의 Device setting에서 고를 수 있는 네비게이션 바 두 모드의 모양과 두께는?",
      a="Gestures: 막대가 얇고 반투명하게 처리되어 앱의 색이 비쳐 보임(24dp 정도) / (three) Button: Back(뒤로), Home(홈), Recents(최근 앱) 버튼, 48dp")],
fig=slide("ppa2", 28, 80),
quote=quote("safeDrawingPadding()은 키보드를 포함하고 있어서, 키보드가 올라올 때, 화면 전체가 밀려 올라갑니다.", s(26, 27, 28, 33))))

# 14
imp_q, imp_a = fill(["import 패키지", "들어 있는 것"], [
    ["android.*", ("?", "안드로이드 프레임워크(Bundle, Log)")], ["androidx.activity.*", ("?", "Activity 관련 함수: ComponentActivity, 컴포저 영역의 경계가 되는 setContent")],
    ["androidx.compose.material3.*", ("?", "Material3 컴포넌트(Scaffold, TopAppBar, Text)")], ["androidx.compose.foundation.layout.*", ("?", "배치 관련(padding, fillMaxSize)")],
    ["androidx.compose.runtime.*", ("?", "compose 실행 엔진: Composable, 바뀐 값을 기억하는 remember, 값이 바뀌면 해당 함수만 다시 실행시키는 mutableStateOf")],
    ["androidx.compose.ui.*", ("?", "기반: 크기·여백·배경·테두리·스크롤 등을 담는 객체 Modifier, 색상을 지정하는 Color")], ["com.example.hello.ui.theme.*", ("?", "com.example.hello의 테마")]])
P(dict(kind=["table", "diag"], title="import 패키지와 dependency 오류",
parts=[
 dict(q="Turtle Screen의 MainActivity.kt에서 import하는 패키지별로 들어 있는 것을 쓰시오. Compose에서는 왜 Text, Column, Modifier, Scaffold를 각각 import해야 하나?" + imp_q,
      a=imp_a + "Compose의 Text, Column, Modifier, Scaffold 등은 <b>개별 함수</b>라서 각각 선언해야 한다. 툴팁에 import가 뜨면 <b>Ctrl+Shift+Enter</b>로 추가.",
      why="<p>패키지 이름이 역할을 말한다: <b>runtime</b> = 상태를 기억·추적하는 실행 엔진, <b>ui</b> = 기반 객체, <b>foundation.layout</b> = 배치, <b>material3</b> = 디자인 컴포넌트, <b>activity</b> = Activity와 Compose의 경계(setContent).</p>"),
 dict(q="벡터 아이콘 패키지를 import하는데 dependency 오류가 났다. ⓐ 어느 파일의 어디에 무엇을 넣나(문자열 형식)? ⓑ <code>implementation(libs.androidx.material.icons.extended)</code> 형식이라면 추가로 확인할 파일과 눌러야 할 버튼은?",
      a="ⓐ <code>build.gradle.kts (Module:app)</code>의 dependencies에 <code>implementation(\"androidx.compose.material:material-icons-extended\")</code> ⓑ <code>libs.versions.toml</code>을 열어 해당 package의 version catalog가 등록되어 있는지 확인 → 상단 메뉴의 'Sync Now'로 Gradle 동기화",
      why="<p>1장 문제 12(\"라이브러리 없음 → build.gradle.kts\")의 실전판. toml 형식의 흐름(등록 → libs.xxx 참조 → Sync)은 4장 문제 10.</p>"),
 dict(q="MainActivity.kt 맨 위의 <code>package com.example.hello</code>는 무엇과 같아야 하나? 이 파일의 실제 위치는?",
      a="설정 파일 build.gradle.kts(app)의 <b>namespace</b>. App의 Location으로 지정한 폴더의 <code>src/main/java/com/example/hello/</code>.")],
quote=quote("androidx.compose.runtime.* : compose 실행 엔진으로 Composable, 바뀐 값을 기억하고 실행시 돌려주는 remember, 값이 바뀌면 해당되는 함수만 다시 실행시키는 mutableStateOf등이 해당됩니다.", s(29, 33, 36, 37))))

# 15
P(dict(kind=["order", "name"], title="MainActivity와 setContent",
parts=[
 dict(q="Turtle Screen의 MainActivity 코드 각 부분의 역할을 쓰시오. ⓐ <code>class MainActivity : ComponentActivity()</code> ⓑ <code>override fun onCreate(savedInstanceState: Bundle?)</code>의 override와 onCreate의 성격 ⓒ <code>super.onCreate(savedInstanceState)</code> ⓓ <code>setContent { }</code> ⓔ 그 안의 <code>MaterialTheme { }</code> ⓕ 가장 안쪽의 <code>TurtleScreen()</code>",
      a="ⓐ 시스템이 인스턴스를 생성하고 생명 주기를 관리하는 화면 단위. Compose용 기반 클래스 ComponentActivity를 상속 ⓑ override = 상위 클래스에 이미 정의된 함수를 재정의, onCreate = Callback 함수 ⓒ 상위 클래스의 처리를 우선 실행 ⓓ Compose의 시작, Activity 화면에 그릴 <b>UI 트리의 시작점(루트)</b> ⓔ @Composable 함수로 테마의 적용 범위 ⓕ 실제 화면(이 Activity의 시작 함수)",
      why="<p>바깥에서 안으로 \"그릇의 크기\" 순서: Activity(화면 단위) → setContent(UI 트리 루트) → MaterialTheme(테마 범위) → TurtleScreen(실제 내용). 4장에서 이 자리에 TurtleScreen 대신 TurtleApp(NavHost)이 들어간다.</p>"),
 dict(q="MainActivity가 앱이 시작될 때 호출되는 이유는? TurtleScreen 함수 위에 <code>@OptIn(ExperimentalMaterial3Api::class)</code>가 붙는 이유는?",
      a="부모 클래스인 ComponentActivity에서 상속받고, <b>manifest에 등록된 대표 클래스</b>라서. TopAppBar 등 Material3의 실험적 API를 쓰는 데 대한 \"명시적 동의\"로 컴파일러 경고를 해제하려고(문제 11).")],
quote=quote("setContent{} 는 Activity 화면에 그릴 UI 트리의 시작점(루트)를 지정하는 역할을 합니다.", s(38, 39, 40))))

# 16
P(dict(kind=["diag"], title="Turtle Screen의 Scaffold·innerPadding·Box 증상",
intro="Turtle Screen 본문: <code>Box(modifier = Modifier.fillMaxSize().padding(innerPadding), contentAlignment = Alignment.Center) { Turtle(…) }</code>",
parts=[
 dict(q="Turtle Screen 화면을 위에서 아래로 5개 영역으로 나누고, 시스템이 그리는 것과 앱이 그리는 것을 구분하시오.",
      a="상태 표시줄(시스템) / TopAppBar(앱) / content — 선택에 따라 거북이 위치 이동(앱) / bottomBar(앱) / 제스처 막대(시스템)"),
 dict(q="Turtle Screen 본문 Box에서 ⓐ <code>.fillMaxSize()</code>를 빼면 거북이는 어디에 그려지나? ⓑ <code>.padding(innerPadding)</code>을 빼면? ⓒ <code>contentAlignment = Alignment.Center</code>를 빼면 거북이는 어디에(기본 정렬의 이름)?",
      a="ⓐ 거북이 사이즈만큼만 영역이 할당되어 <b>TopAppBar 쪽(본문 맨 위)에 붙는다</b>(원문 표현: \"TopAppBar 위로 붙게 됩니다\") — fillMaxSize가 Scaffold에서 계산된 본문 영역의 최대를 차지하게 하기 때문 ⓑ 본문이 topBar/bottomBar와 겹친다 ⓒ 왼쪽 위, <code>Alignment.TopStart</code>(Box의 기본)",
      why="<p>증상 → 빠진 것: \"붙는다/작다\" → 크기(fillMaxSize), \"가려진다\" → 여백(padding(innerPadding)), \"구석에 있다\" → 정렬(contentAlignment).</p>"),
 dict(q="innerPadding의 정체: 누가 무엇을 계산해 어떤 타입으로 어디에 넘겨주나? Scaffold의 어느 파라미터인가? <code>-&gt;</code> 왼쪽과 오른쪽은?",
      a="Scaffold가 TopAppBar와 BottomBar의 높이를 계산한 결과값을 <b>PaddingValues</b>로, <b>innerPadding</b>이라는 이름으로 넘겨준다. 마지막 파라미터 <code>content: @Composable (PaddingValues) -&gt; Unit</code>에 전달되는 람다. -&gt; 왼쪽 innerPadding = 이 람다가 받는 파라미터 이름, 오른쪽 = 그 파라미터를 사용하는 본문."),
 dict(q="ⓐ 지금은 자식이 Turtle 하나뿐인데 Box를 쓴 이유는? ⓑ <code>modifier = Modifier</code>에서 왼쪽 modifier와 오른쪽 Modifier는 각각 무엇인가? ⓒ 코드에 회색으로 보이는 <code>paddingValues =</code>는? ⓓ 파라미터가 여러 개면 무엇으로 구분하나?",
      a="ⓐ Box는 자식들을 겹쳐서 스택 형태로 배치하는 layout이라, 나중에 화면에 추가할 경우를 대비(3장의 발자국) ⓑ 왼쪽 = Box 함수의 <b>파라미터 이름</b>, 오른쪽 = 설정이 없는 <b>'빈 수식자' 객체</b>(여기에 .fillMaxSize()처럼 .으로 함수를 연결) ⓒ Android Studio가 보여 주는 파라미터 <b>이름 힌트</b> ⓓ 쉼표(콤마)")],
fig=slide("ppa2", 32, 80),
quote=quote("fillMaxSize()는 Scaffold 에서 계산된 본문 영역의 최대를 차지하도록 하는데, 만약 이 함수가 없으면, 중앙 거북이는 거북이 사이즈 만큼만 영역이 할당되어 TopAppBar 위로 붙게 됩니다.", s(32, 33, 40, 44, 45, 46))))

# 17
P(dict(kind=["calc", "diag"], title="거북이 이동 버튼과 범위 제한, offset vs padding",
intro="Turtle Screen 이동 코드: <code>onUp = { offsetY = (offsetY - step).coerceAtLeast(-range) }</code>, <code>onDown = { offsetY = (offsetY + step).coerceAtMost(range) }</code>, step = 24.dp, range = 140.dp, 시작 0.dp. 거북이는 Box 중앙에서 offset만큼 떨어져 그려진다.",
parts=[
 dict(q="거북이가 0.dp에서 시작해 위 버튼을 6번 누르면 offsetY는? 7번 누르면?",
      a="한 번 누를 때마다 0 → −24 → −48 → −72 → −96 → −120 → (6번째: −144가 될 차례지만) <b>−140</b>. 7번째도 <b>−140</b>(이미 경계).",
      why="<p>coerceAtLeast(−140) = \"적어도 −140은 된다\" = 최솟값 보장. 그래서 −144가 −140으로 잘린다.</p>"),
 dict(q="거북이의 offsetY가 음수면 화면의 위쪽인가 아래쪽인가? coerceAtLeast와 coerceAtMost는 각각 무엇을 보장하나?",
      a="위쪽(좌표는 아래로 갈수록 커지므로 −는 위, 문제 20 Offset 좌표계와 같은 원리). coerceAtLeast(−range): −140보다 <b>작아지지 않게</b>(최솟값) / coerceAtMost(range): 140보다 <b>커지지 않게</b>(최댓값) → 중앙 기준 ±140dp로 제한해 화면 밖으로 나가지 않게."),
 dict(q="거북이를 옮길 때 .padding()이 아니라 .offset()을 쓰는 이유는?",
      a=".offset()은 layout이 차지하는 공간의 변화 없이 <b>보이는 위치만</b> 변화시킨다(.padding()은 공간 자체를 바꿈).")],
quote=quote(".offset()은 .padding()과 달리 layout 이 차지하는 공간의 변화없이 시간적 위치만 변화시킵니다.", s(43, 47, 50))
 + "<p><span class='fix'>원본 s47 \"시간적 위치\" → 문맥상 \"시각적 위치\"로 보임</span></p>"))

# 18
P(dict(kind=["name", "diag"], title="Compose 상태: remember · mutableStateOf · by · var/val",
intro="Turtle Screen 상태 코드: <code>var offsetX by remember { mutableStateOf(0.dp) }</code>, <code>val step = 24.dp</code>",
parts=[
 dict(q="<code>mutableStateOf(0.dp)</code>가 Compose에 요청하는 것과, 그 값이 바뀌면 일어나는 일은?",
      a="\"0.dp라는 초기값을 가진 <b>변경 가능한 상태</b> 하나를 만들어 달라\". 값이 바뀌면 그 값을 <b>읽는 컴포저블이 자동으로 다시 그려진다</b>."),
 dict(q="Turtle Screen 상태 코드에서 <code>remember { }</code>를 빼면 버튼을 눌러도 거북이가 제자리로 돌아오는 이유는?",
      a="리컴포지션이 일어날 때마다 상태 객체가 새로 만들어져 offsetX가 매번 <b>0.dp로 reset</b>되기 때문. remember{}는 mutableStateOf로 만든 상태 객체를 <b>리컴포지션이 일어나도 초기화되지 않고 계속 유지되도록 기억</b>한다.",
      why="<p>두 겹: <b>mutableStateOf = 바뀌면 알린다</b>(다시 그리게 함), <b>remember = 다시 그려져도 잊지 않는다</b>. 둘 중 하나만 있으면 안 된다. remember도 못 버티는 경우(화면 회전 = Activity 재생성)는 3장 rememberSaveable.</p>"),
 dict(q="<code>by</code>는 어떤 Kotlin 문법이며, 없으면 offsetX 값을 어떻게 읽고 써야 하나? <code>remember { mutableStateOf(0.dp) }</code>가 반환하는 타입은?",
      a="위임(delegation). 없으면 <code>offsetX.value = 10.dp</code>처럼 <b>.value</b>를 통해서만 읽고 쓴다(by를 쓰면 .value 접근을 생략하고 Dp 타입 변수처럼 바로 읽고 씀). 반환 타입 <code>State&lt;Dp&gt;</code>."),
 dict(q="Turtle Screen에서 offsetX는 왜 var이고 step은 왜 val인가? range = 140.dp는 무엇을 위한 값인가? 함수 위의 @Composable이 허락하는 것은?",
      a="offsetX는 클릭 시 값이 변경되는 것을 허용해야 하므로 재할당 가능한 <b>var</b>. step은 한 번 정해지면 바뀌지 않는 값(한 번에 움직이는 거리)이라 <b>val</b>. range는 거북이가 움직이는 최대 범위를 중앙 기준 ±140dp로 제한하는 상수. @Composable = 이 함수에서 다른 Composable 함수(Box, Scaffold …)를 호출할 수 있다는 표시.")],
quote=quote("remember{ ... }: mutableStateOf(0.dp) 로 만든 상태 객체를, 리컴포지션이 일어나도 값이 초기화되지 않고 계속 유지되도록 기억하게 하는 함수 입니다.", s(48, 49, 50))))

# 19
P(dict(kind=["calc", "name"], title="거북이 애니메이션: animateDpAsState와 tween",
intro="Turtle Screen 애니메이션 코드: <code>val animatedX by animateDpAsState(targetValue = offsetX, animationSpec = tween(durationMillis = 500), label = \"turtleX\")</code>, animatedY는 같은 꼴에 <code>tween(durationMillis = 200)</code>, label \"turtleY\". 거북이 위치: <code>Turtle(modifier = Modifier.offset(x = animatedX, y = animatedY))</code>",
parts=[
 dict(q="animateDpAsState는 무엇을 하는 함수인가? offsetX가 0.dp → 24.dp로 바뀌면 animatedX는 어떻게 변하나? 이 과정을 무엇이라 부르나?",
      a="Dp 타입 값을 부드럽게 애니메이션 처리하는 Compose 함수. targetValue가 바뀔 때마다 그 값까지 중간값들(1.dp, 2.dp, … 24.dp)을 시간에 따라 순차적으로 계산해 반환 — <b>보간</b>(거북이가 미끄러지듯 이동)."),
 dict(q="거북이를 오른쪽으로 한 칸, 위로 한 칸 움직일 때 이동이 끝나는 데 걸리는 시간은 각각? 어느 쪽이 더 빠른가? tween은 어떤 방식이고, animationSpec은 무엇을 정하나?",
      a="가로(X) <b>500ms = 0.5초</b>, 세로(Y) <b>200ms = 0.2초</b> → 세로 이동이 더 빠르다. tween = 지정한 시간 동안 일정하게 값이 변해 가는 방식. animationSpec = 애니메이션이 어떤 속도와 방식으로 진행될지.",
      why="<p>500과 200이 <u>비대칭</u>인 것이 숫자 함정: X = 500, Y = 200.</p>"),
 dict(q="label = \"turtleX\"는 어디에 쓰나? animatedX는 왜 var가 아니라 val이고, by를 쓴 이유는? 화면에서 실제 거북이 위치로 쓰이는 값은 offsetX인가 animatedX인가?",
      a="Android Studio의 애니메이션 디버깅 도구(Animation Preview)에서 어떤 애니메이션인지 구분하기 위한 이름표. animatedX는 개발자가 아닌 animateDpAsState가 갱신하는 값이라 val. 반환값이 State&lt;Dp&gt; 타입이라 by로 .value 없이 Dp처럼 쓰려고. <b>animatedX</b>(offsetX는 목표 좌표).",
      why="<p><b>offsetX = 목적지(버튼이 바꿈), animatedX = 지금 위치(애니메이션이 바꿈)</b>. 그래서 var/val이 갈린다.</p>")],
quote=quote("animationSpec = tween(durationMillis =500) 에서 animationSpec 은 애니메이션이 어떤 속도와 방식으로 진행될 지를 지정하는 부분으로, tween 은 지정한 시간동안 일정하게 값이 변해가는 방식이고", s(47, 48, 51))))

# 20
dr_q, dr_a = fill(["DrawScope 그리기 함수", "필요한 값", "그리는 것"], [
    ["drawCircle", ("?", "color, radius, center"), ("?", "중심값과 반지름으로 원")], ["drawRect", ("?", "color, topLeft, size"), ("?", "왼쪽 위 좌표와 높이·넓이로 사각형")],
    ["drawOval", ("?", "color, topLeft, size"), ("?", "왼쪽 위 좌표와 장축·단축으로 타원")], ["drawLine", ("?", "color, start, end, strokeWidth"), ("?", "시작점과 끝점으로 직선")],
    ["drawArc", ("?", "color, startAngle, sweepAngle, useCenter"), ("?", "각을 통한 호(부채꼴)")], ["drawPath", ("?", "path, color"), ("?", "여러 점을 연결한 임의의 복잡한 도형")]])
P(dict(kind=["name", "table"], title="Canvas와 DrawScope로 그리기",
parts=[
 dict(q="<code>Canvas(modifier = Modifier.size(80.dp)) { … }</code>에서 Canvas와 { } 블록의 역할은? drawCircle 같은 그리기 함수는 어디서만 바로 호출할 수 있나?",
      a="Canvas = 그림을 그릴 수 있는 영역을 만드는 컴포저블(크기는 modifier로 지정). { } 람다 블록 = <b>DrawScope</b>라는 특수 영역으로, <b>이 안에서만</b> drawCircle, drawRect 같은 그리기 함수를 바로 호출할 수 있다."),
 dict(q="DrawScope의 좌표: ⓐ 자동으로 제공되는 size에 들어 있는 것 ⓑ Offset(x, y)의 원점과 증가 방향 ⓒ 40f 같은 절대 픽셀 대신 <code>w * 0.5f</code> 같은 비율로 좌표를 쓰는 이유",
      a="ⓐ 캔버스 전체의 픽셀 크기(Size 타입: width, height) ⓑ 왼쪽 위가 (0,0), 오른쪽 아래로 내려갈수록 값이 커짐 ⓒ Canvas의 크기가 바뀌어도 그림의 비율이 그대로 유지되도록"),
 dict(q="DrawScope 그리기 함수 6개의 필요한 값과 그리는 것을 표로 쓰시오. 기본으로 색을 채워 그리는데, 테두리 선만 그리려면?" + dr_q,
      a=dr_a + "테두리만: <code>style = Stroke(width = 4f)</code>처럼 style 파라미터에 Stroke()",
      why="<p>drawRect와 drawOval은 같은 값(topLeft, size)을 받는다 — 타원은 \"그 사각형 안에 꽉 차게 그린 둥근 모양\"이기 때문(보충). 3장 발자국은 drawOval + drawCircle.</p>")],
quote=quote("Offset(x,y) 는 좌표 하나늘 나타내는 데이터 타입으로 왼쪽 위가 (0,0) 로 지정되며, 오른쪽 아래로 내려갈 수록 값이 커집니다.", s(52, 53, 54))))

# 21
P(dict(kind=["order", "calc", "diag"], title="Canvas로 거북이 그리기: 순서와 비율",
intro="<code>fun Turtle(modifier: Modifier = Modifier) { Canvas(modifier = modifier.size(80.dp)) { val w = size.width; val h = size.height; … } }</code> — 다리 4개 → 얼굴 → 눈 → 등껍질(큰 원 → 테두리 → 중앙 무늬) 순서로 그린다.",
parts=[
 dict(q="Turtle()에서 다리를 등껍질보다 <b>먼저</b> 그리는 이유는? Canvas의 일반 규칙은?",
      a="Canvas에서는 <b>먼저 그린 그림이 아래, 나중에 그린 그림이 위</b>로 겹쳐 보인다. 다리가 등껍질 아래로 살짝 나와 보이게 하려고."),
 dict(q="Turtle()의 다리 4개 중심 (x 비율, y 비율)과 반지름 비율, 다리 색은 어떻게 정했나? 거북이 크기를 80dp에서 120dp로 바꾸면 다리 위치는?",
      a="왼쪽 위 (0.22, 0.25), 오른쪽 위 (0.78, 0.25), 왼쪽 아래 (0.22, 0.75), 오른쪽 아래 (0.78, 0.75), 반지름 w × 0.12. legColor로 색을 고정해 두고 drawCircle을 4번 호출. 몸통 대비 <b>같은 비율로 유지</b>된다.",
      why="<p>비율은 대칭으로 외운다: 0.22 ↔ 0.78, 0.25 ↔ 0.75(1에서 뺀 값).</p>"),
 dict(q="Turtle()의 얼굴, 눈, 등껍질 세 원을 쓰시오(중심, 반지름 비율, 색·역할).",
      a="얼굴: 노란색, 중심 (0.92, 0.5) — 세로 중앙, 가로 92% 지점, 반지름 0.18 / 눈: 얼굴보다 작은 비율로 offset 조정(검정, 반지름 0.03) / 등껍질(공통 중심 (0.45, 0.5)): 진한 녹색 반지름 0.42 큰 원 → 같은 위치·같은 반지름에 <code>style = Stroke(width = 4f)</code>로 두께 4픽셀 테두리 → 밝은 연녹색 반지름 0.18로 한가운데 하이라이트"),
 dict(q="ⓐ <code>modifier: Modifier = Modifier</code>로 기본값을 둔 이점 2가지는? ⓑ <code>Canvas(modifier = modifier.size(80.dp))</code>에서 왼쪽 modifier와 오른쪽 modifier는 각각 무엇이고, .size를 이어 붙인 효과는? ⓒ <code>val w = size.width</code>의 size는?",
      a="ⓐ Turtle을 호출할 때 modifier를 넘기지 않아도 기본값으로 컴파일됨 / 개발자가 Modifier.offset(…)을 넘겨 외부에서 거북이를 이동시킬 수 있음 ⓑ 왼쪽 = Canvas 함수의 파라미터, 오른쪽 = Turtle 함수가 파라미터로 받은 modifier. 외부에서 받은 위치 설정에 size()를 이어 붙여 Turtle 내부에서 크기를 고정 ⓒ DrawScope 안에서 자동 제공되는 Canvas 영역의 픽셀 크기(size.width = 가로폭, size.height = 세로폭)",
      why="<p>거북이의 위치는 바깥(TurtleScreen의 offset)이, 크기는 안쪽(Turtle)이 정하는 역할 분담이다. 문제 19의 <code>Turtle(modifier = Modifier.offset(…))</code>이 이 통로로 들어온다.</p>")],
quote=quote("단, Canvas 안에서는 먼저 그린 그림이 아래에, 나중에 그린 그림이 위로 겹쳐 보이기 때문에 거북이의 구조를 고려하셔서 순서를 정하시면 좋습니다.", s(55, 56, 57, 58, 59, 60))))

# 22
pv_q, pv_a = fill(["비교 항목", "AVD", "@Preview"], [
    ["확인 범위", ("?", "애니메이션을 포함한 전체 앱"), ("?", "클릭 외의 정적인 부분만")],
    ["색을 바꾼 뒤 다시 보기", ("?", "빌드 → 재실행 과정이 필요"), ("?", "IDE 안에서 바로 렌더링, 저장 즉시 자동 갱신")],
    ["특정 요소만 확인", ("?", "불가능"), ("?", "원하는 Composable만 선택해서 확인 가능")]])
P(dict(kind=["calc", "diag", "table"], title="@Preview로 잡은 거북이 얼굴 잘림",
parts=[
 dict(q="Android Studio IDE는 컴파일 오류를 실시간으로 잡아 준다. 그런데도 @Preview가 필요한 이유는? AVD와 @Preview를 비교하는 표를 채우시오." + pv_q,
      a="문법적으로는 맞지만 <b>개발자의 의도와 다르게 시각적으로 나타나는 것</b>은 IDE가 못 잡으므로." + pv_a),
 dict(q="TurtlePreview(<code>@Preview(showBackground = true)</code>)에서 거북이 얼굴이 오른쪽에서 잘려 보였다. 얼굴 center x = w × 0.92, radius = w × 0.18일 때 얼굴 오른쪽 끝은 캔버스의 몇 % 지점인가? 왜 안 보이나?",
      a="0.92 + 0.18 = <b>1.10 → 110%</b>. 캔버스 밖으로 뻗은 부분이 <b>clip에 의해 잘려</b> 화면에 안 보인다.",
      why="<p>원의 오른쪽 끝 = 중심 x + 반지름. 비율끼리 바로 더하면 된다.</p>"),
 dict(q="거북이 얼굴을 radius = w × 0.17, center x = w × 0.83, 눈 center x = w × 0.91로 고쳤다. 얼굴 오른쪽 끝은 몇 %인가? 눈(반지름 w × 0.03)의 오른쪽 끝은?",
      a="얼굴: 0.83 + 0.17 = <b>1.00 → 100%</b>(캔버스 끝에 딱 맞음). 눈: 0.91 + 0.03 = <b>0.94 → 94%</b>(얼굴 안).")],
fig=slide("ppa2", 71, 85),
quote=quote("Turtle 의 얼굴의 중심부분이 w*0.92f 로 갠버스의 92% 지점에 있고, 0.92+0.18 =1.10으로 얼굴의 오른쪽 끝이 Canvas 110% 지점까지 뻗어 clip 에 의해서 잘려 화면에 안보이게 됩니다.", s(70, 71, 72))))

# 23
P(dict(kind=["name", "diag"], title="3D 버튼: 눌림을 감지하고 모양을 미리 계산",
intro="<code>fun Direction3DButton(label: String, icon: ImageVector, onClick: () -&gt; Unit)</code> 안: <code>val interactionSource = remember { MutableInteractionSource() }</code> / <code>val isPressed by interactionSource.collectIsPressedAsState()</code> / <code>val elevation = if (isPressed) 1.dp else 6.dp</code> / <code>val gradient = if (isPressed) Brush.verticalGradient(…) else Brush.verticalGradient(…)</code>",
parts=[
 dict(q="Direction3DButton의 세 파라미터는 각각 무엇을 받나? <code>() -&gt; Unit</code>인 onClick은 컴포저블을 호출하나?",
      a="label: 화면에 표시될 캡션 / icon: Icons.Filled.KeyboardArrowUp 같은 아이콘 모양의 데이터(ImageVector) / onClick: 버튼이 클릭됐을 때 실행할 동작(로직). 컴포저블을 호출하는 게 아니라 상태 변경 같은 <b>일반 로직</b>만 수행."),
 dict(q="<code>MutableInteractionSource()</code>가 추적하는 것은? 그것을 remember와 val로 만든 이유는 각각?",
      a="이 버튼에 대한 모든 상호작용(눌림, 포커스, 호버 등)의 <b>이벤트 스트림</b>을 추적·관리하는 객체. remember = 리컴포지션 사이에도 계속 유지 / val = 객체 상태는 바뀌지만 나중에 다른 객체로 바뀔 일이 없어서."),
 dict(q="<code>collectIsPressedAsState()</code>로 만든 isPressed는 어떤 값이 되나? 무엇을 골라 어떤 타입으로 바꾸나? 왜 val인가?",
      a="사용자가 버튼을 누르고 있으면 true, 아니면 false. interactionSource가 추적하는 이벤트 중 현재 <b>눌려 있는(Pressed)</b> 상태만 선택해 <code>State&lt;Boolean&gt;</code>로 변환(by로 .value 없이 Boolean처럼). 누르고 뗄 때마다 collectIsPressedAsState()가 내부적으로 갱신해 주는 값을 <b>읽기만</b> 해서."),
 dict(q="<code>val elevation = if (isPressed) 1.dp else 6.dp</code>에서 이 if의 쓰임새 이름과 일반형은? 눌렸을 때 그림자는 얕아지나 깊어지나? Brush와 <code>verticalGradient(colors = listOf(색1, 색2))</code>는 무엇이며, 눌림/안 눌림 색은?",
      a="if 문을 <b>식(expression)</b>으로 사용: <code>if (조건) 값A else 값B</code>(값이 여러 줄 코드 블록 { }이어도 됨). 눌리면 6dp → 1dp로 얕아짐(눌려 들어간 느낌). Brush = 단색이 아닌 그라데이션·패턴 등 '칠하는 방식'을 표현하는 Compose 타입, verticalGradient = 위에서 아래로 색이 점점 변하는 세로 그라데이션. 눌림: 진한 회색 → 밝은 회색 / 안 눌림: 흰색 → 회색.",
      why="<p>Direction3DButton의 이 부분 전체는 두 역할: interactionSource·isPressed = 눌림 상태 <b>감지</b> / elevation·gradient = 어떤 그림자와 색을 쓸지 <b>미리 계산</b>. val이 세 번 나오지만 이유가 다르다(객체 자체는 안 바뀜 / 남이 갱신하고 읽기만 / 매번 다시 계산되는 값).</p>")],
quote=quote("val elevation = if (isPressed) 1.dp else 6.dp 는 if 문을 식(expression)으로 사용한 것입니다.", s(61, 62, 63, 64))
 + "<p><span class='fix'>원본 표기: 제목 \"Direct3DButton\" ↔ 코드 Direction3DButton / \"MutableIntersectionSource\"·\"intersectionSource\"·\"collectPressedAsState\" → 정확히는 MutableInteractionSource·interactionSource·collectIsPressedAsState</span></p>"))

# 24
P(dict(kind=["order", "diag"], title="3D 버튼의 Modifier 순서와 빠뜨렸을 때",
parts=[
 dict(q="Direction3DButton의 Column에 적용되는 Modifier를 원본의 적용 순서대로 나열하시오: clickable(interactionSource, indication = null, onClick) / padding(horizontal = 14.dp, vertical = 8.dp) / shadow(elevation, RoundedCornerShape(14.dp), clip = false) / background(brush = gradient) / clip(RoundedCornerShape(14.dp))",
      a="shadow → clip → background → clickable → padding (둥근 모서리 그림자 → 같은 모양으로 자르기 → 그라데이션 배경 → 눌림 감지를 연결한 클릭 가능 영역 → 내부 여백)",
      why="<p>Modifier는 <b>위에서 아래로 순서대로</b> 적용된다 — 바깥 껍데기부터 만들고 안으로 들어간다: 그림자(가장 바깥) → 자르기 → 칠하기 → 누를 수 있게 → 안쪽 여백.</p>"),
 dict(q="3D 버튼의 증상과 원인을 짝지으시오. ⓐ 그림자는 둥근데 버튼 배경이 사각형 ⓑ 버튼을 눌러도 그림자·색이 전혀 안 바뀜(isPressed가 항상 false) ⓒ 누를 때 물결(ripple)이 퍼짐 ⓓ 그림자가 도형 경계에서 잘려 뭉툭함 ⓔ 아이콘과 글자가 왼쪽에 쏠림",
      a="ⓐ <code>.clip()</code>이 없음(Column의 실제 내용물 — 배경색, 클릭 영역 — 을 둥근 모양대로 잘라 그림자와 모양을 일치시키는 역할) ⓑ clickable에 <code>interactionSource</code>를 연결하지 않음 ⓒ <code>indication = null</code>이 없음(기본 물결 효과를 꺼서 elevation/gradient 눌림 효과만 남김) ⓓ shadow의 <code>clip = true</code>(false면 그림자가 도형 모양 밖으로도 부드럽게 퍼짐) ⓔ <code>horizontalAlignment = Alignment.CenterHorizontally</code>가 없음(Column의 기본은 Alignment.Start, 왼쪽 정렬)",
      why="<p>원문에 \"~이 없으면\" 반례가 4개 적혀 있다(clip, interactionSource, indication, padding 순서). 객관식 \"이유로 옳은 것\"의 재료.</p>"),
 dict(q="3D 버튼에서 padding을 맨 앞에 두면 의도와 달라지는 이유는? padding(horizontal = 14.dp, vertical = 8.dp)로 만든 버튼 비율은?",
      a="shadow, clip, background, clickable은 버튼 전체 모양인 <b>바깥 영역</b>에 적용되고, padding은 그 이후 내용물이 배치될 <b>안쪽 여백</b>을 정하는 것이라, 가장 나중에 넣어야 버튼 전체를 크게 한 뒤 내용물을 안쪽으로 밀어 넣는 의도대로 동작한다. 좌우 14dp·상하 8dp → 가로로 넓적한 비율."),
 dict(q="3D 버튼에서 background()의 두 버전은? 여기서는 어느 쪽인가? <code>onClick = onClick</code>의 왼쪽과 오른쪽은? Column 안의 Icon과 Text는 각각 무엇을 어떤 색으로 그리나?",
      a="단색(Color)을 받는 버전 / 그라데이션 같은 <b>Brush</b>를 받는 버전 — 여기서는 Brush(<code>background(brush = gradient)</code>). 왼쪽 = clickable의 파라미터, 오른쪽 = Direction3DButton이 파라미터로 받은 onClick(외부에서 전달된 람다가 클릭 시 실행됨). Icon: 받은 imageVector를 tint로 진한 회색(0xFF555555) / Text: 아이콘 아래 캡션(12.sp), 같은 진한 회색 — Column이 둘을 위아래로 쌓음.")],
fig=slide("ppa2", 65, 90),
quote=quote("interactionSource 는 앞에서 만든 interactionSource 를 연결시켜서, 이 연결이 없으면, isPressed 는 항상 false 로 고정되어 눌림효과가 동작하지 않습니다.", s(65, 66, 67, 68, 69))))

KEYWORDS = [
 ("매니페스트 (manifest)", "앱의 구성 요소(Activity, 서비스, 브로드캐스트 수신기, 콘텐츠 제공자) 목록과 시스템에 전달할 요구사항. 파일명 AndroidManifest.xml 고정", s(2)),
 ("리소스", "응용프로그램이 사용할 자원. res 폴더(이름 a~z, 0~9, _, . 만)와 assets 폴더(제약 없음)", s(4)),
 ("element", "XML에서 <태그></태그>처럼 짝을 이루는 것. 최상위 element는 1개", s(5)),
 ("namespace 접두사 (android:)", "안드로이드 시스템의 고유 속성임을 알리는 접두사", s(6)),
 ("KeepRules (rules.keep)", "빌드 시 코드를 압축하고 이름을 바꾸는 과정에서 특정 파일·클래스 이름이 바뀌지 않도록 보호하는 코드 난독화(Obfuscation) 방지 설정", s(7)),
 ("Gradle", "안드로이드 프로젝트를 빌드(컴파일 및 패키징)하는 도구", s(8)),
 ("settings.gradle.kts", "프로젝트에 사용되는 모듈(app, core, feature)", s(8, 9)),
 ("gradle-wrapper.properties", "프로젝트가 어떤 버전의 Gradle 엔진으로 빌드되어야 하는지", s(10)),
 ("gradle.properties", "Gradle 빌드 과정 자체의 동작 방식(JVM 메모리 크기, AndroidX 사용 여부 등)", s(10)),
 ("local.properties", "개발자 본인의 local 환경 값(SDK 로컬 경로). Git에 올리지 않음", s(10)),
 (".dex (dalvik executable)", ".apk 안에 들어 있는 코드의 확장자", s(11)),
 ("앱의 4대 구성요소", "액티비티, 서비스, 브로드캐스트 수신기, 콘텐트 제공자", s(12)),
 ("JAVA_HOME", "gradlew가 Java를 찾을 때 가장 먼저 확인하는 환경 변수(없으면 PATH, 둘 다 없으면 오류)", s(13)),
 ("Android Jetpack", "2018년 구글이 안드로이드 개발에 필요한 구성요소들을 모아 놓은 제품군", s(15)),
 ("AndroidX", "Jetpack을 구성하는 실제 라이브러리 이름", s(15)),
 ("ViewModel", "데이터의 수명 주기를 관리(Jetpack 아키텍처)", s(15)),
 ("LiveData", "데이터 변경을 관찰(Jetpack 아키텍처)", s(15)),
 ("Hilt", "클래스가 필요한 객체를 외부에서 가져와 사용하는 방식인 의존성 주입(Dependency Injection)", s(15)),
 ("Fragment", "화면의 일부분을 담당하는 UI 구성 요소", s(16)),
 ("Room", "SQLite 기반의 기기 내 데이터베이스(Jetpack Data)", s(17)),
 ("DataStore", "가벼운 Key-value 저장(Jetpack Data)", s(17)),
 ("WorkManager", "백그라운드에서 예약된 작업을 안정적으로 실행(Jetpack Infrastructure)", s(17)),
 ("리컴포지션", "상태가 바뀌면 Compose 런타임이 다시 그려야 할 부분만 알아서 다시 실행해 화면을 갱신하는 것", s(18)),
 ("View Hierarchy", "View 시스템에서 메모리에 살아 있는 View 객체들의 객체 트리", s(18)),
 ("람다 (Lambda)", "이름 없는 함수. 나중에 실행할 코드 뭉치를 변수처럼 다른 함수에 값으로 전달할 때 사용", s(20)),
 ("Composable", "@Composable 어노테이션이 붙은 함수 전체", s(21)),
 ("Layout Composable", "다른 Composable들을 어떻게 배치할지 담당(LazyColumn, Column, Row, Box, Scaffold)", s(21)),
 ("LazyListScope", "LazyColumn의 중괄호 안, 어떤 항목들을 넣을지 선언하는 별도 영역", s(22)),
 ("@OptIn", "Kotlin 표준 라이브러리 문법으로 \"명시적 동의\"를 의미, 컴파일러 경고를 해제", s(23)),
 ("파라미터 (Parameter)", "함수를 정의할 때 괄호 안에 선언하는 값의 이름표", s(24)),
 ("시그니처 (Signature)", "함수이름(파라미터1:타입, 파라미터2:타입, …) 형태 전체", s(24)),
 ("MaterialTheme", "Material Design 3 스펙에서 정의한 색상/글꼴/도형의 세 범주(colorScheme, typography, shapes)", s(25)),
 ("Edge to Edge 렌더링", "앱 콘텐츠가 상태 표시줄과 네비게이션 바 뒤까지 그려지는 것. Android 15(API 35)부터 targetSDK 35 이상 앱에 적용", s(26)),
 ("safeDrawing", "시스템바(status + navigation) + display cutout(노치, 펀치홀) + IME(keyboard). 가려질 수 있는 모든 영역의 합집합", s(26)),
 ("display cutout", "카메라 구멍이나 노치가 화면을 파고든 영역. 세로에서는 상태 표시줄에 흡수, 가로 회전 시 옆쪽에 별도로", s(26)),
 ("Scaffold", "Material 디자인의 기본 화면 골격. topBar, bottomBar, content slot을 인자로 받음", s(33)),
 ("innerPadding", "content 람다가 받는 PaddingValues. topBar/bottomBar와 겹치지 않도록 .padding(innerPadding)으로 적용", s(33)),
 ("modifier (Modifier)", "크기, 위치, 여백, 배경 등 모양과 동작을 정의하는 chaining 가능한 설정 객체", s(33)),
 ("TopAppBar", "Activity 상단에 제목과 동작 아이콘 등을 배치하는 띠. API 11의 ActionBar와 같은 역할. 기본 64dp", s(35)),
 ("setContent{}", "Activity 화면에 그릴 UI 트리의 시작점(루트)을 지정", s(39)),
 ("remember", "상태 객체를 리컴포지션이 일어나도 초기화되지 않고 계속 유지되도록 기억하게 하는 함수", s(49)),
 ("mutableStateOf", "초기값을 가진 변경 가능한 상태를 만들어 달라는 요청. 값이 바뀌면 읽는 컴포저블이 다시 그려짐", s(49)),
 ("by (위임, delegation)", "State 객체를 .value 없이 일반 변수처럼 바로 읽고 쓰게 하는 Kotlin 문법", s(49)),
 ("animateDpAsState", "Dp 값을 targetValue까지 중간값을 순차 계산(보간)해 부드럽게 애니메이션 처리하는 함수", s(50)),
 ("tween", "지정한 시간 동안 일정하게 값이 변해 가는 애니메이션 방식(durationMillis)", s(51)),
 ("Canvas / DrawScope", "그림을 그릴 수 있는 영역을 만드는 컴포저블 / 그 람다 블록, 그리기 함수를 바로 호출할 수 있는 특수 영역", s(52)),
 ("Stroke", "그리기 함수에서 테두리 선만 그리게 하는 style 값(style = Stroke(width = 4f))", s(54)),
 ("MutableInteractionSource", "버튼에 대한 모든 상호작용(눌림, 포커스, 호버 등)의 이벤트 스트림을 추적·관리하는 객체", s(62)),
 ("collectIsPressedAsState()", "interactionSource의 이벤트 중 눌려 있는 상태만 골라 State<Boolean>으로 변환", s(63)),
 ("Brush", "단색이 아닌 그라데이션, 패턴 등 '칠하는 방식'을 표현하는 Compose 타입", s(64)),
 ("indication = null", "클릭 시 기본으로 나타나는 물결효과(ripple)를 끔", s(67)),
 ("@Preview", "편집기에서 도구가 읽고 미리보기를 생성. IDE 안에서 바로 렌더링, 저장 즉시 갱신, 원하는 Composable만 확인", s(70)),
]

OUTRO = """
<h3>2장 범위 대조표 — 슬라이드 → 문제</h3>
""" + table(["슬라이드", "내용", "문제"], [
 ["s2~3", "4구분·매니페스트·코드", "1"], ["s4, 30", "res/assets·Compose res", "2"], ["s5~6", "XML", "3"], ["s7~10", "Gradle 파일·KeepRules", "4"],
 ["s11~12", "APK·4대 구성요소", "5"], ["s13~14, 31", "JAVA_HOME", "6"], ["s15~17", "Jetpack", "7"], ["s18", "명령형/선언형", "8"],
 ["s19~20", "부모·자식·람다", "9"], ["s21~22", "레이아웃·LazyColumn", "10"], ["s23~24", "어노테이션·파라미터", "11"],
 ["s25, 35, 41~42", "MaterialTheme·TopAppBar·BottomBar", "12"], ["s26~28, 33", "Edge-to-Edge·내비 바", "13"], ["s29, 33, 36~37", "import·dependency·package", "14"],
 ["s38~40", "MainActivity·setContent", "15"], ["s32~33, 44~46", "Scaffold·Box 증상", "16"], ["s43, 47", "이동·offset", "17"],
 ["s48~50", "remember·by", "18"], ["s47~48, 51", "animateDpAsState", "19"], ["s52~54", "Canvas", "20"], ["s55~60", "거북이 그리기", "21"],
 ["s70~72", "@Preview·잘림", "22"], ["s61~64", "3D 버튼 상태", "23"], ["s65~69", "Modifier 순서", "24"]]) + """
<div class="note"><b>뺀 슬라이드</b>: s1 표지 / s34 s33과 같은 내용 / s73~74 버튼 Preview·최종 화면 캡처(내용은 문제 22·24에 포함).</div>
<div class="note"><b>원본 오탈자</b>: s5 "mainfest" <span class="fix">→ manifest</span> / s23 "@RequireApi" <span class="fix">→ @RequiresApi</span> / s25 MaterialTheme 슬라이드의 "3 가지 방법으로 파라미터를 확인" 문장은 앞 슬라이드에서 복사된 것으로 보임 / s47 "시간적 위치" <span class="fix">→ 시각적</span> / s61~63 Direct3DButton·Intersection·collectPressedAsState 표기.</div>
"""
