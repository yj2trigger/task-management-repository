"""1장 ppa1 — 안드로이드 개요·개발 절차·빌드·실행·생명주기·디버깅·AVD·dp."""
from qbook2 import s, quote, table, fill, slide

B = "<span class='blank'></span>"

INTRO = """
<h2>읽는 법</h2>
<div class="note">
<b>이 책은 문제가 본문입니다.</b> 소문제를 풀고 → 바로 아래 <b>답·해설</b>을 확인하세요(풀 때는 종이로 가리기).
해설은 "문제의 어떤 단서를 보고 → 어떤 개념을 떠올려 → 어떻게 판정하는지"를 적었습니다. 객관식은 선지마다 옳고 그른 이유를 순서대로 적었습니다.<br>
한 문제에 여러 지식을 묶었고 <b>같은 지식은 두 번 묻지 않습니다</b>. 장 끝의 <b>키워드 사전·키워드 빈칸</b>은 용어 단답형(주관식) 대비, <b>범위 대조표</b>는 빠진 슬라이드 확인용입니다.
</div>
<div class="qbody">이중선 왼쪽 막대(옅은 배경) = 문제</div>
<div class="ans">가는 실선 왼쪽 막대 = 답·해설</div>
<div class="quote">굵은 실선 왼쪽 막대 = 강의자료 원문 그대로(오타 포함, 줄임은 …)<span class="src">원본 ppa1 s25(p13 위) = ppa1 파일 13쪽 위쪽 슬라이드(슬라이드 번호 25)</span></div>
<div class="note">점선 상자 = 해설 정리. <span class="fix">빨간 글씨</span> = 원본 오탈자·주의. "보충" = 원문에 없는 설명(시험 근거로 쓰지 말 것).</div>
<h2>1장. ppa1 — 안드로이드 개요·개발 절차·빌드·실행·생명주기·AVD</h2>
"""

ITEMS = []
P = ITEMS.append

# 1 ----------------------------------------------------------------
lay_q, lay_a = fill(["계층(아래 → 위)", "구성요소(원문 표기)"], [
    ["리눅스 커널", ("?", "하드웨어 장치 드라이버(디스플레이, USB, 카메라, 블루투스, Wi-Fi, 오디오 등), 공유 메모리, 바인더")],
    ["라이브러리 ‖ 안드로이드 런타임 <b>(같은 높이에 나란히)</b>", ("?", "라이브러리: Bionic, Webkit, SQLite, SSL, FreeType, 미디어 프레임 워크, SGL, Open GL ES ‖ 안드로이드 런타임: 핵심 자바 라이브러리, Dalvik 또는 ART")],
    ["애플리케이션 프레임워크", ("?", "액티비티 관리자, 패키지 관리자, 윈도우 관리자, 위치 관리자 등")],
    ["애플리케이션", ("?", "내장 앱, 사용자 앱")]])
P(dict(kind=["table", "name"], title="안드로이드 시스템 구조 (ppa1 판 5계층)",
parts=[
 dict(q="안드로이드 시스템 구조의 5개 계층 이름을 쓰고, 원본 그림에서 어떻게 쌓여 있는지(아래 → 위) 쓰시오.",
      a="리눅스 커널 → <b>[라이브러리 ‖ 안드로이드 런타임]</b> → 애플리케이션 프레임워크 → 애플리케이션. 5개 층이지만 그림에서는 4줄 — <b>라이브러리와 안드로이드 런타임이 같은 높이에 나란히</b> 있다(어느 한쪽이 위가 아님).",
      why="<p>\"5개 층\"만 보고 다섯 칸을 위아래로 쌓으면 틀린다. 라이브러리와 안드로이드 런타임은 둘 다 커널 위·프레임워크 아래의 <b>형제</b>다. \"라이브러리는 안드로이드 런타임보다 아래 계층이다\" 같은 선지는 ✕.</p>"),
 dict(q="다음을 안드로이드 5계층에 배정하시오: 바인더 / 공유 메모리 / 하드웨어 장치 드라이버 / Bionic / Webkit / SQLite / SSL / FreeType / 미디어 프레임 워크 / SGL / Open GL ES / 핵심 자바 라이브러리 / Dalvik 또는 ART / 액티비티 관리자 / 패키지 관리자 / 윈도우 관리자 / 위치 관리자 / 내장 앱 / 사용자 앱" + lay_q,
      a=lay_a,
      why="<p><b>각 항목의 원문 설명까지 그대로 외울 것:</b></p>" + table(["계층", "항목: 원문 설명", "보충(원문 밖)"], [
        ["리눅스 커널", "하드웨어 장치 드라이버: 디스플레이, USB, 카메라, 블루투스, Wi-Fi, 오디오 등 / 공유 메모리: 프로세스간 데이터 공유 기능 제공 / 바인더: 프로세스간의 통신 기능 제공", "운영체제의 주요 기능(메모리 관리, 파일시스템, 장치 제어 등)을 리눅스 커널에 의존(원문 s7)"],
        ["라이브러리", "Bionic: C 라이브러리 / Webkit: 웹엔진 / SQLite: 데이터베이스 엔진 / SSL: 보안통신 / FreeType: 폰트 처리 엔진 / 미디어 프레임 워크: 다양한 멀티미디어 형식 지원 / SGL: 2D 그래픽스 / Open GL ES: 3D 그래픽스", "SQLite는 2장 Room(SQLite 기반 DB)의 바탕"],
        ["안드로이드 런타임", "핵심 자바 라이브러리 / Dalvik 또는 ART", "Dalvik은 ART 이전의 실행 엔진. ART는 APK 안의 DEX를 기계어로 바꿔 실행하고 메모리 할당·가비지 컬렉션도 담당(문제 17)"],
        ["애플리케이션 프레임워크", "액티비티 관리자, 패키지 관리자, 윈도우 관리자, 위치 관리자 등", "액티비티 관리자 = 앱의 구동과 상태 관리, 패키지 관리자 = 앱 설치 및 삭제(원문 s8)"],
        ["애플리케이션", "내장 앱: 전화, 연락처, 메시지, 일정, 카메라, 웹브라우저 등의 제조사가 미리 설치한 앱 / 사용자 앱: 앱 마켓(구글 플레이 스토어)을 통해 사용자가 선택하여 설치한 앱", ""]])
        + "<p>판정 단서: \"관리자\" → 프레임워크 / \"엔진·C 라이브러리·그래픽스·멀티미디어·보안통신\" → 라이브러리 / \"프로세스간\" → 커널(공유 메모리 = <u>데이터 공유</u>, 바인더 = <u>통신</u>, 서로 바꾼 선지 주의) / \"자바·Dalvik·ART\" → 안드로이드 런타임.</p>"),
 dict(q="안드로이드 시스템 구조에서 <b>가장 큰</b> 계층과 <b>두 번째로 큰</b> 계층은? 라이브러리 계층은 어떤 두 종류로 구성되나? 최상위 계층의 응용 프로그램은 주로 무슨 언어로 개발되나?",
      a="가장 큼: 라이브러리 / 두 번째: 애플리케이션 프레임워크. 라이브러리 = 오픈 소스로 개발된 라이브러리 + 안드로이드 전용 라이브러리. Java(특수한 경우 C/C++를 일부).",
      why="<p class='trap'>ppa4에는 HAL이 들어간 다른 5계층(Linux Kernel / HAL / ART + Native C/C++ Libraries / Java API Framework / System Apps)이 나온다(4장 문제 3). 문제에 HAL·Native 단서가 있으면 ppa4판으로 답한다. 또 Android 12부터 ART는 모듈로 분리되어 시스템 업데이트로 갱신될 수 있다(s8).</p>")],
fig=slide("ppa1", 9, 92),
quote=quote("안드로이드는 무료 운영 체제인 Linux 를 기반으로 여러 소프트웨어 계층으로 구성됩니다.", s(7, 8, 9))))

# 2 ----------------------------------------------------------------
ver_q, ver_a = fill(["연도", "버전", "이름", "API", "대표 특징(원문)"], [
    ["2015", "5.1/5.1.1", "Lollipop", "22", ("?", "둘 이상의 sim 카드를 공식 지원하기 시작")],
    ["2015", "6.0/6.0.1", ("?", "Marshmallow"), "23", "지문 인식 공식 지원, USB C-type 지원, 외장 메모리를 내장 메모리처럼 사용가능"],
    ["2017", "7.0/7.1/7.1.2", "Nougat", "24/25", ("?", "다중 창 모드(두개 앱 동시 사용 가능), 3D API Vulkan 지원, 전원 절약 모드 도입")],
    ["2017", "8.0", ("?", "Oreo"), "26", "PIP(picture in picture) 모드 지원, 백그라운드 최적화"],
    ["2018", "9.0", "Pie", "28", ("?", "제스처 네비게이션, 디스플레이 노치 공식지원, HEIF 지원")],
    ["2019", "10.0", "Quince Tart", "29", ("?", "시스템 전역 다크 테마, 위치 권한 세분화")],
    ["2020", "11", "Red Velvet Cake", "30", ("?", "내장 화면 녹화, 미사용 앱 권한 자동 초기화")],
    ["2021", "12/12L", ("?", "Snow Cone"), "31/32", "프라이버시 대시보드, 마이크/카메라 사용 표시기"],
    ["2022", "13", "Tiramisu", "33", ("?", "앱별 언어 설정, 알림 권한을 런타임 권한으로 전환")],
    ["2023", "14", "Upside Down Cake", ("?", "33 <span class='fix'>(원본 표기, 실제 34)</span>"), "사진/동영상 부분 접근 권한, 글꼴 200% 확대 지원, 잠금화면 커스터마이즈, Health Connect 기본 탑재"],
    ["2024", "15", ("?", "Vanilla Ice Cream"), "35", "프라이빗 스페이스(앱 격리 보관 공간), 부분 화면 공유, 도난 감지 잠금, edge-to-edge 화면 표시 기본"],
    ["2025", "16", "Baklava", "36", ("?", "라이브 업데이트(진행 상황 실시간 알림), 데스크톱 모드 및 대화면 적응형")],
    ["2026", "17", "Cinnamon Bun", ("?", "37"), "대화면(sw 600dp 이상)에서 크기 조정 및 방향전환 거부 불가, 로컬 네트워크 접근 런타임 권한 신설, 기기 간 상태 연속성을 위한 Handoff API"]])
P(dict(kind=["mc", "table"], title="안드로이드 개요와 버전별 특징 (○)",
parts=[
 dict(q="안드로이드에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("안드로이드는 2005년에 구글이 개발을 시작했다.", False, "안드로이드의 개발 시작은 <b>2003년</b>이고, 2005년은 구글이 안드로이드를 직접 <b>인수</b>한 해다."),
            ("버전마다 디저트 이름이 붙고, 시스템 내부에서 사용되는 API level에 따라 숫자가 부여된다.", True, "안드로이드 버전의 이름은 디저트 이름(Lollipop, Oreo …)이고, 시스템 내부 번호는 API level(22, 26 …)이다."),
            ("API level이 바뀌어도 앱 프로그래밍 관점에서는 바뀐 것이 없다고 보면 된다.", False, "반대다. 안드로이드의 API level이 바뀌면 앱 프로그래밍 관점에서도 <b>변경된 사항이 있다</b>고 생각해도 무방하다."),
            ("보통 1년에 최소 1번 정도 새 버전이 나온다.", True, "안드로이드는 보통 1년에 최소 1번 정도 새 버전이 나오며, 현재도 빠르게 발전하고 있다."),
            ("안드로이드는 전 세계에서 가장 많이 사용되는 모바일 운영 체제다.", True, "안드로이드는 전 세계에서 가장 많이 사용되는 모바일 운영 체제다(원문 첫 문장).")],
      a="ⓑ ⓓ ⓔ"),
 dict(q="안드로이드 버전 표의 빈칸을 채우시오." + ver_q, a=ver_a,
      why="<p>특징 → 버전으로 기억: PIP는 Pie가 아니라 <b>Oreo(8.0, 26)</b> / 다크 테마 10(29) / 알림 런타임 권한 13(33) / edge-to-edge 기본 15(35) — 2장의 \"targetSdk 35 이상이면 Edge-to-Edge 적용\"과 같은 숫자. 2026년 17 Cinnamon Bun(API 37)은 원본이 굵게 강조했고, 6장 AVD 실습 이미지(API 37.1)도 이 버전이다.</p>")],
quote=quote("2003년에 안드로이드에서 개발을 시작하면서, 2005년 구글이 직접 인수해 … 보통 API level 이 바뀌면, 앱 프로그래밍 관점에서도 변경된 사항이 있다고 생가해도 무방", s(4, 5, 6))
 + "<p><span class='fix'>원본 s4 \"생가해도\" → 생각해도</span></p>"))

# 3 ----------------------------------------------------------------
lang_q, lang_a = fill(["언어", "쓰이는 곳", "파일 확장자"], [
    ["Kotlin", ("?", "앱 로직, Compose UI"), ".kt"], ["Java", ("?", "앱 로직(선택 사항, 레거시)"), ".java"],
    ["XML", ("?", "매니페스트, 리소스, Views 레이아웃"), ".xml"], ["Kotlin DSL", "Gradle 빌드 스크립트", ("?", ".gradle.kts")],
    ["Groovy", "Gradle 빌드 스크립트(구식)", ("?", ".gradle")], ["TOML", ("?", "의존성 버전 카탈로그"), ("?", "libs.versions.toml")],
    ["Properties", ("?", "빌드 설정값"), ".properties"], ["SQL", "Room의 쿼리 문자열", ("?", ".kt 안의 어노테이션")],
    ["C/C++", ("?", "NDK 네이티브 모듈(선택)"), ".c, .cpp"], ["셸 명령", ("?", "adb, gradlew 실행"), "터미널"]])
P(dict(kind=["table", "diag"], title="안드로이드 스튜디오 안의 언어들",
parts=[
 dict(q="안드로이드 스튜디오에서 쓰이는 언어 표를 채우시오." + lang_q, a=lang_a,
      why="<p>\"<b>누가 읽는가</b>\"로 나누면 외우기 쉽다: 기기의 ART가 실행 → Kotlin·Java / 안드로이드 시스템이 읽음 → XML(매니페스트·리소스) / <b>개발 PC의 Gradle이 읽음</b> → Kotlin DSL·Groovy·TOML·Properties / 개발자가 터미널에서 → 셸 명령.</p>"),
 dict(q="팀원 A: \"<code>build.gradle.kts</code>도 Kotlin 문법이니까 앱에 포함되어 폰에서 실행되겠지.\" 무엇이 틀렸는지 설명하시오.",
      a="Kotlin DSL은 <b>문법만</b> Kotlin을 따른다. 앱에 포함되어 실행되는 코드가 아니라 <b>빌드 도구 Gradle에게 지시를 내리는 스크립트</b>이고, 앱이 설치될 <b>기기에는 그 내용이 들어가지 않는다</b>.",
      why="<p>\"문법이 같다 ≠ 실행 위치가 같다\". 빌드 스크립트는 개발 PC에서 빌드할 때만 쓰인다(문제 14의 \"Gradle은 build.gradle.kts에 적힌 내용에 따라 결정\").</p>")],
quote=quote("주의: Kotlin DSL 은 문법은 Kotlin 을 따르지만, 앱에 포함되 실행을 시키는 코드가 아니고, 빌드 도구인 Gradle 에게 지시를 내리는 script 일 뿐 앱이 설치될 기기에는 그 내용이 들어가지 않습니다.", s(10))))

# 4 ----------------------------------------------------------------
loc_q, loc_a = fill(["안드로이드 스튜디오 설치 후 위치", "들어 있는 것"], [
    ["설치 때 지정한 폴더", ("?", "IDE 본체")], ["%LOCALAPPDATA%\\Android\\Sdk", ("?", "SDK와 시스템 이미지")],
    ["%USERPROFILE%\\.gradle", ("?", "Gradle 캐시")], ["%USERPROFILE%\\.android\\avd", ("?", "AVD 디스크 이미지")]])
P(dict(kind=["mc", "table"], title="개발 방식과 안드로이드 스튜디오 설치",
parts=[
 dict(q="안드로이드 앱 개발 방식과 안드로이드 스튜디오 설치에 대한 설명으로 옳지 <b>않은</b> 것을 모두 고르시오.",
      opts=[("안드로이드 앱 개발 방식은 여러 가지지만 Android SDK는 모든 방식에 필수다.", True, "Android SDK(Software Development Kit)는 소프트웨어 개발에 필요한 라이브러리와 각종 도구 모음이라, 안드로이드 앱 개발 방식이 어느 것이든 필수다."),
            ("Android SDK + Visual Studio + Xamarin 플러그인 방식은 주로 C#을 기반으로 한다.", True, "Visual Studio + Xamarin 방식은 마이크로소프트의 개발 도구로 C#이 기반이며, 다른 세 방식(Eclipse, IntelliJ IDEA, 안드로이드 스튜디오)이 Java가 주언어인 것과 다르다."),
            ("안드로이드 스튜디오 방식은 Java를 주언어로 쓰므로, 스튜디오와 별도로 JDK를 반드시 따로 설치해야 한다.", False, "안드로이드 스튜디오 방식은 Java가 주언어라 JDK가 <u>필요</u>한 것은 맞지만, 안드로이드 스튜디오에는 OpenJDK를 확장한 JDK인 <b>JBR(JetBrains Runtime)</b>이 함께 배포되어 <u>따로 설치할 필요가 없다</u>."),
            ("안드로이드 스튜디오 설치 프로그램은 IDE와 SDK를 함께 설치한다.", False, "안드로이드 스튜디오 설치 프로그램은 <b>IDE만</b> 배치한다. Android SDK는 <b>첫 실행 시 설정 마법사</b>가 인터넷으로 내려받고, 그 위치는 사용자가 변경할 수 있다."),
            ("안드로이드 스튜디오는 IntelliJ IDEA 기반의 소스코드 편집기, Gradle 빌드 도구, Android SDK를 하나로 묶어서 제공한다.", True, "안드로이드 스튜디오는 편집기(IntelliJ IDEA 기반) + 빌드 도구(Gradle) + Android SDK를 한 묶음으로 제공한다(여기에 JBR까지 함께 배포)."),
            ("개발자가 stable과 canary를 동시에 설치하거나 여러 SDK를 병행하는 일이 흔해서, 안드로이드 스튜디오는 자기 설치 경로와 SDK 경로를 자체 설정 파일에 기록한다.", True, "안드로이드 스튜디오는 여러 버전(stable·canary)과 여러 SDK를 함께 쓰는 개발자가 많아, 자기 설치 경로와 SDK 경로를 자체 설정 파일에 따로 기록해 둔다."),
            ("프로젝트 단위 파일 local.properties의 sdk.dir은 IDE 안에서 adb를 호출하거나 Gradle을 실행할 때 쓰인다.", True, "local.properties의 sdk.dir은 그 PC의 Android SDK 경로다. 그래서 local.properties는 내 PC에만 해당하는 값이라 Git에 올리지 않는다(문제 12). <span class='fix'>원본 표기 \"abd\" → adb</span>"),
            ("구글이 공식적으로 제시하는 최소 요구 사항은 IDE와 Android SDK, Android Emulator를 합한 경우 8GB 정도다.", True, "구글이 제시하는 안드로이드 스튜디오 최소 요구 사항은 IDE + Android SDK + Android Emulator를 합해 8GB 정도다.")],
      a="ⓒ ⓓ",
      why="<p>ⓒ는 두 슬라이드를 엮은 함정이다: \"①~③ 방식은 Java가 주언어라 JDK가 필요하다\"(s11)와 \"스튜디오에는 JBR이 함께 배포되어 따로 설치할 필요가 없다\"(s14). <b>필요하다 ≠ 따로 설치해야 한다</b>. 개발 방식 4가지: ① SDK + 이클립스 + ADT 플러그인 ② SDK + IntelliJ IDEA + 안드로이드 플러그인 ③ SDK + 안드로이드 스튜디오 + 안드로이드 플러그인 ④ SDK + 비주얼 스튜디오 + Xamarin 플러그인(C#).</p>"),
 dict(q="안드로이드 스튜디오 설치가 끝난 뒤, 각 위치에 설치되는 구성요소를 쓰시오." + loc_q, a=loc_a,
      why="<p>기억법: SDK는 <u>LOCALAPPDATA</u>, 사용자별 숨김 폴더(.gradle / .android)는 <u>USERPROFILE</u>.</p>"),
 dict(q="안드로이드 스튜디오 IDE 본체를 저장할 지정 폴더를 바꿀 때 지킬 규칙은?", a="폴더명은 <b>공백 없이 영어로</b>(그래야 오류가 없음).")],
quote=quote("안드로이드 스튜디오의 설치 프로그램은 IDE 만 배치됩니다. SDK 는 첫 실행 시 설정 마법사가 내려 받기를 하고, 그 위치는 사용자가 변경할 수 있습니다.", s(11, 14, 15, 21))))

# 5 ----------------------------------------------------------------
P(dict(kind=["order", "name"], title="안드로이드 앱 개발 절차",
parts=[
 dict(q="안드로이드 앱 개발 절차의 단계를 순서대로 나열하고, <b>반복되는 구간</b>을 표시하시오: 배포 / 코드 작성 / 개발 환경 설정 / release 서명 / 디버깅 &amp; 테스팅 / 프로젝트 생성 / 빌드 &amp; 실행",
      a="개발 환경 설정 → 프로젝트 생성 → <b>[코드 작성 → 빌드 &amp; 실행 → 디버깅 &amp; 테스팅]</b>(디버깅 &amp; 테스팅에서 코드 작성으로 되돌아가며 반복) → release 서명 → 배포",
      why="<p>반복 구간은 \"고치고 → 돌려 보고 → 확인\"이 계속 도는 곳이다. 원본 도식(아래 그림)에서 디버깅 &amp; 테스팅에서 코드 작성으로 되돌아가는 화살표가 있다.</p>"),
 dict(q="안드로이드 앱 개발 절차 중 어느 단계인가? ⓐ JDK·안드로이드 스튜디오·Android SDK 및 플랫폼 도구를 설치하고 실제 기기 또는 에뮬레이터(AVD)를 준비 ⓑ 템플릿·패키지명·언어(Kotlin/Java)·최소 및 대상 API 수준을 지정해 프로젝트의 골격을 만듦 ⓒ 로그캣·디버거·프로파일러로 이미 발생한 문제의 원인을 찾음 ⓓ 문제가 발생했는지 자동으로 확인",
      a="ⓐ 개발 환경 설정 ⓑ 프로젝트 생성 ⓒ 디버깅 ⓓ 테스팅",
      why="<p>디버깅과 테스팅의 차이는 <b>시점</b>: 디버깅은 <u>이미 발생한</u> 문제의 원인 찾기, 테스팅은 문제가 발생했는지 <u>자동으로</u> 확인.</p>"),
 dict(q="프로젝트 생성 단계에서 함께 생성되는 것 3가지는?", a="매니페스트, Gradle 빌드 스크립트, 리소스 디렉토리 구조"),
 dict(q="\"앱의 서명은 release 서명 단계에서 처음 일어난다.\" 옳은가?",
      a="틀림. 반복(개발) 단계에서도 서명은 일어난다 — 개발 중 빌드는 안드로이드 스튜디오가 자동 생성한 <b>디버그 키</b>로 서명된다. 다이어그램의 서명은 정확히는 <b>릴리스 서명</b>을 가리킨다.",
      why="<p>서명되지 않은 APK는 설치 자체가 안 된다(문제 16). 실행 버튼으로 에뮬레이터에 설치되는 debug 빌드도 서명되어 있어야 한다고 추론할 수 있다.</p>")],
fig=slide("ppa1", 12, 85),
quote=quote("서명은 반복 단계에서도 이미 일어납니다. 개발 중 빌드는 Android Studio가 자동 생성한 디버그 키로 서명되므로, 다이어그램의 \"앱 서명\"은 정확히는 릴리스 서명을 가리킵니다.", s(12, 13, 24, 50, 54, 55))))

# 6 ----------------------------------------------------------------
P(dict(kind=["name"], title="개발 도구 이름 맞히기",
parts=[
 dict(q="설명에 해당하는 이름을 쓰시오. ⓐ 자바 프로그램을 작성·컴파일·실행하는 도구 모음. 컴파일러·프로파일러·아카이브 생성기 같은 도구이며, 소스에서 호출할 수 있는 API를 담은 라이브러리이기도 하고, 자바 애플리케이션을 실행하는 가상 머신이기도 함 ⓑ 컴파일·리소스 처리·의존성 해결·테스트 실행·패키징·서명·배포를 하나의 흐름으로 자동화하는 JVM 기반의 안드로이드 스튜디오 공식 빌드 도구 ⓒ 대상 API 수준별 android.jar를 담은 SDK 구성요소 ⓓ adb 등이 들어 있는 SDK 구성요소 ⓔ 시스템 이미지를 통해 기기 프로파일과 RAM 및 저장 공간 설정 명세를 반영한, 가상 기기의 정의와 그것을 실행하는 인스턴스 ⓕ ⓔ를 실행하려면 함께 필요한 것 ⓖ OpenJDK를 확장한 JDK로, 안드로이드 스튜디오와 함께 배포되어 JDK를 따로 설치할 필요가 없게 해 주는 것",
      a="ⓐ JDK(Java Development Kit) ⓑ Gradle ⓒ SDK Platform ⓓ SDK Platform-Tools ⓔ AVD(Android Virtual Device) ⓕ AVD를 실행하는 에뮬레이터 실행 파일(Android Emulator) ⓖ JBR(JetBrains Runtime)",
      why="<p>SDK 구성요소 5개(첫 실행 설정 마법사가 내려받음): SDK <b>Platform</b>(대상 API 수준별 android.jar) / SDK <b>Build-Tools</b> / SDK <b>Platform-Tools</b>(adb 등) / Android <b>Emulator</b> / 에뮬레이터용 <b>시스템 이미지</b>. Platform과 Platform-Tools를 바꾼 선지가 함정이다. AVD는 \"정의 + 인스턴스\" 둘 다이고, 실행에는 에뮬레이터 실행 파일이 따로 필요하다.</p>")],
quote=quote("AVD (Android Virtual Device) 는 시스템 이미지를 통해 기기 프로파일과, RAM 및 저장 공간 설정을 담은 명세 사항을 반영하여, 가상 기기의 정의와 그것을 실행하는 인스턴스입니다.", s(13, 14, 21))))

# 7 ----------------------------------------------------------------
adb_q, adb_a = fill(["adb 계층", "실행 위치", "역할"], [
    [("?", "클라이언트(안드로이드 스튜디오의 안드로이드 플러그인)"), "개발 PC", ("?", "명령을 발행하는 주체. 터미널의 adb install, adb logcat 같은 명령도 클라이언트")],
    ["adb 서버", ("?", "개발 PC(백그라운드 상주)"), ("?", "클라이언트의 요청을 받아 적절한 기기로 중계, 연결된 기기 목록 관리. localhost TCP 5037번 포트 점유")],
    ["adbd", ("?", "기기 측(에뮬레이터·실제 디바이스 양쪽에 각각)"), ("?", "서버에서 전달받은 명령을 기기 안에서 실제로 수행: APK 설치, 로그 전송, 셸 명령 실행, 파일 전송")]])
P(dict(kind=["table", "diag"], title="Android Debug Bridge(adb)의 3계층",
parts=[
 dict(q="adb의 3계층 표를 채우시오." + adb_q, a=adb_a),
 dict(q="ⓐ 개발자가 adb 서버를 켠 적이 없는데 <code>adb install</code>이 동작했다. 왜인가? ⓑ 에뮬레이터와 adb 서버, 실제 디바이스와 adb 서버 사이의 통신 방식은 각각?",
      a="ⓐ 클라이언트 명령이 <b>처음 발행되는 순간</b> 그 클라이언트가 스스로 서버 프로세스를 띄운다. ⓑ 에뮬레이터: TCP/IP 통신 / 디바이스: USB 또는 TCP/IP 통신",
      why="<p>스튜디오의 Logcat 창도 adb 서버를 통해 기기에서 내용을 받아 오고(문제 21), 앱 실행 때도 \"adb 서버가 adbd에게 명령을 전달\"한다(문제 17). 같은 경로가 여러 곳에 다시 나온다.</p>"),
 dict(q="daemon을 정의하시오. adbd의 끝 글자 d는 무엇을 뜻하나?",
      a="배경(Background)에서 계속 실행되면서, 요청이 들어올 때 정해진 서비스를 제공하는 유닉스 계열 운영체제의 프로세스. d = daemon.")],
fig=slide("ppa1", 22, 85),
quote=quote("adb 서버는 개발자가 의식적으로 서버를 켜지 않아도 클라이언트 명령이 처음 발행되는 순간 그 클라이언트가 스스로 서버 프로세스를 띄우게 됩니다", s(22, 23))))

# 8 ----------------------------------------------------------------
P(dict(kind=["table", "diag"], title="minSdk · targetSdk · compileSdk",
parts=[
 dict(q="다음 상황과 관련된 API 수준은? (minSdk / targetSdk / compileSdk / IDE 버전의 API 수준) ⓐ 더 많은 구형 기기에 앱이 설치되게 하고 싶다 ⓑ 알림의 런타임 권한, 대화형 적응형 UI 의무화 같은 동작 변경이 적용되는 기준 ⓒ 컴파일할 때 어떤 android.jar를 쓸지 ⓓ AGP 9.3을 쓰면 최대 37로 제한되는 값 ⓔ 프로젝트에서 선택 가능한 상한 ⓕ 앱이 어느 버전을 기준으로 동작을 검증했는지, 즉 배포 요건 ⓖ 보통 API 26~30 사이에서 고르는 값",
      a="ⓐ minSdk ⓑ targetSdk ⓒ compileSdk ⓓ compileSdk ⓔ IDE 버전의 API 수준 ⓕ targetSdk ⓖ minSdk (<span class='fix'>본문 \"26~30\", 같은 슬라이드 왼쪽 손글씨 \"26-34\"</span> — 둘 다 기억)",
      why="<ol><li>세 값은 질문으로 구분한다: <b>min</b> = \"어디까지 <u>설치</u>되나?\" / <b>target</b> = \"어느 버전 <u>규칙으로 동작</u>하나?(배포 요건)\" / <b>compile</b> = \"무엇으로 <u>컴파일</u>하나?(android.jar)\".</li><li>\"선택한 IDE나 AGP에 의해 제약을 받는 <b>유일한</b> 값\" = compileSdk.</li><li>세 값이 들어 있는 파일은 <code>app/build.gradle.kts</code>(s36, \"많이 혼동하기 때문에 차이를 구분할 필요가 있습니다\").</li></ol>"),
 dict(q="새 프로젝트 마법사에서 Minimum SDK의 기본값은? minSdk를 낮게 잡을 때의 장점과 단점은?",
      a="API 24 (Nougat, Android 7.0). 장점: 더 많은 기기 지원 / 단점: 최신 API와 호환성 문제")],
quote=quote("compileSdk(컴파일 API 수준): compile 시 사용할 android.jar 의 버전을 지정합니다.선택한 IDE 나 AGP 에 의해 제약을 받는 유일한 값으로, AGP 9.3 이 지원하는 최대 API 수준은 37로 제한됩니다.", s(25, 32, 36))))

# 9 ----------------------------------------------------------------
P(dict(kind=["diag", "name"], title="템플릿과 UI 방식",
parts=[
 dict(q="Android Studio에서 새 프로젝트를 만들 때 고르는 시작 틀(템플릿) 중, 다음 설명에 해당하는 템플릿 이름은? ⓐ Jetpack Compose로 액티비티 하나·최소 화면 ⓑ Compose 대신 XML layout(View 체계)으로 최소 화면 ⓒ Activity 두 개, 화면 간 이동(Navigation) 설정, 앱 바와 플로팅 버튼까지 XML layout으로",
      a="ⓐ Empty Activity(현재 기본 선택) ⓑ Empty Views Activity ⓒ Basic Views Activity",
      why="<p>템플릿 이름 해독법: <b>\"Views\"가 붙으면 XML</b>, 안 붙으면 Compose. \"Basic\"은 화면 2개·내비게이션·앱 바·FAB까지 들어간 큰 틀.</p>"),
 dict(q="템플릿 이름의 \"Views\"는 무엇을 가리키나? Empty Views Activity에서 XML을 View 객체로 변환해 화면에 올리는 함수는?",
      a="전통적인 안드로이드(XML layout + View 클래스 계층)를 사용한다는 뜻으로, <b>UI 구성 방식</b>을 가리킨다. <code>setContentView()</code>"),
 dict(q="안드로이드 UI 구성 방식 중 무엇인가(명령형/선언형, XML layout/Compose)? ⓐ 화면의 초기 모습을 XML로 정의해 두고, 상태가 바뀌면 개발자가 해당 View 객체를 찾아내 직접 속성을 변경 ⓑ 상태에 따른 화면을 함수로 기술해 두고, 상태가 바뀔 때 프레임워크가 해당 함수를 재호출해 화면을 갱신",
      a="ⓐ 명령형(imperative) — XML layout ⓑ 선언형(declarative) — Compose",
      why="<p>\"<b>누가</b> 화면을 고치나\"로 구분: 개발자가 직접(명령형) vs 프레임워크가 다시 그림(선언형). 2장 문제 8에서 리컴포지션으로 이어진다.</p>"),
 dict(q="\"실행 시점에 화면을 구성하는 객체 계층으로, 실제 측정·배치·그리기를 수행하는 실체\"의 이름과 예는? 액티비티를 정의하시오.",
      a="View 체계. android.view.View, android.view.ViewGroup과 그 하위의 TextView, Button, LinearLayout 등. 액티비티 = 창(Window)을 제공하고, 그 안에 UI를 배치하며, 사용자 입력을 받아 사용자와 상호작용하는 <b>하나의 화면</b>을 담당하는 앱의 구성요소. 코드로는 android.app.Activity 또는 그 하위 클래스를 상속한 클래스.",
      why="<p>액티비티 정의 채점 키워드: <b>창(Window)·UI 배치·사용자 입력·하나의 화면·Activity 상속</b>.</p>")],
quote=quote("XML layout: 명령형 (imperative) 방식입니다. 화면의 초기 모습을 XML 로 정의해 두고, 이후 상태가 바뀌면, 개발자가 해당 View 객체를 찾아내어, 직접 객체의 속성을 변경해 줍니다.", s(26, 27))))

# 10 ---------------------------------------------------------------
dsl_q, dsl_a = fill(["비교 항목", "Kotlin DSL", "Groovy DSL"], [
    ["파일 이름", ("?", "build.gradle.kts"), ("?", "build.gradle")],
    ["오류를 아는 시점", ("?", "컴파일 시점에 오류를 잡음"), ("?", "빌드를 실행해야 오류를 알 수 있음")],
    ["편의·특징", ("?", "자동 완성 및 힌트 기능, 탐색이 쉬움"), ("?", "문법이 유연하고 가벼움")],
    ["장점·위상", ("?", "앱 소스(Kotlin)와 같은 언어라 학습 부담이 적음, 구글 공식 권장(새 프로젝트 기본값)"), ("?", "기존에 오랫동안 사용, 오래된 오픈 소스 프로젝트나 튜토리얼에 많이 등장")]])
P(dict(kind=["table"], title="빌드 구성 언어: Kotlin DSL vs Groovy DSL",
parts=[
 dict(q="안드로이드 스튜디오의 빌드 구성 언어(Build configuration language)는 무엇을 설정하는 스크립트 언어인가?",
      a="앱의 빌드 방식, 라이브러리 의존성, 버전 등을 설정하는 스크립트 언어(두 가지 옵션)."),
 dict(q="두 빌드 구성 언어를 비교하는 표를 채우시오." + dsl_q, a=dsl_a,
      why="<p>결정적 차이는 \"<b>오류를 언제 아나</b>\": Kotlin DSL은 컴파일 시점에 잡아 코딩 오류를 줄여 주고, Groovy는 빌드를 돌려 봐야 안다.</p>")],
quote=quote("Kotlin DSL (build.gradle.kts): 컴파일 시점에 오류를 잡아서 코딩오류를 줄여주고, 코드 작성시 자동 완성 및 힌트 기능이 있어 탐색이 쉽습니다.", s(28, 32))))

# 11 ---------------------------------------------------------------
P(dict(kind=["diag"], title="새 프로젝트의 Name · package name · 저장 위치",
parts=[
 dict(q="새 프로젝트 설정에서 Name에 \"My Hello\"를 넣었다. package name의 기본값은? Name은 프로젝트의 어디에 적용되나(2곳)? 사용자 기기에서는 어디에 보이나?",
      a="<code>com.example.myhello</code>(com.example. + Name을 소문자화하고 공백을 제거한 값). <code>res/values/strings.xml</code>의 <b>app_name 문자열</b>과 <b>프로젝트 폴더명</b>. 사용자 기기의 앱 아이콘 아래 이름."),
 dict(q="package name에 대한 설명으로 옳지 <b>않은</b> 것을 모두 고르시오.",
      opts=[("package name은 구글 스토어 전체에서 유일해야 하는 식별자다.", True, "package name은 구글 스토어 전체에서 유일한 식별자라서, 스토어가 앱을 구분하는 기준이 된다."),
            ("한 번 배포한 앱의 package name은 나중에 바꿀 수 있다.", False, "앱의 package name은 한 번 배포하면 <b>영구히 변경할 수 없다</b>."),
            ("이름(Name)이 같아도 package name이 다르면 다른 앱으로 취급되어 같은 기기에 동시 설치된다.", True, "앱을 구분하는 기준이 이름(Name)이 아니라 package name이라서, package name이 다르면 같은 기기에 동시 설치된다."),
            ("소속 기관 도메인이 없으면 GitHub 계정을 이용해 io.github.사용자명.앱이름 형태를 많이 쓴다.", True, "package name에는 소속 기관 도메인이 있으면 그 도메인을 쓰고, 없으면 io.github.사용자명.앱이름 관례를 쓴다."),
            ("com.example로 시작하는 package name도 구글 Play에 그대로 업로드할 수 있다.", False, "com.example은 <b>예약 접두사</b>라 구글 Play가 이 접두사로 시작하는 패키지의 업로드를 <b>거부</b>한다. 배포 계획이 있다면 반드시 바꿔야 한다.")],
      a="ⓑ ⓔ",
      why="<p>package name의 성질은 \"<b>식별자</b>\" 하나에서 나온다: 유일해야 함 → 스토어 전체 유일 / 식별자가 바뀌면 다른 앱 → 배포 후 변경 불가, 이름이 같아도 package가 다르면 다른 앱. Name은 \"보이는 이름\", package name은 \"구분하는 이름\".</p>"),
 dict(q="새 프로젝트를 <code>C:\\OneDrive\\대학교\\내 앱</code>에 만들려 한다. 안드로이드 스튜디오의 save location 규칙 중 어긋나는 3가지와, 경로 길이에 관한 제한은?",
      a="경로에 <b>한글</b>이 없어야 함, <b>공백</b>이 없어야 함, <b>OneDrive 등의 동기화 폴더</b>는 피해야 함. 경로 길이는 윈도우의 <b>260자</b> 길이 제한을 따른다."),
 dict(q="새 프로젝트를 만든 직후 하단에 진행 표시가 돈다. 무엇이 자동으로 실행 중이고, 끝나면 무엇이 완성되나? 그 뒤 안드로이드 스튜디오가 곧바로 하는 일은?",
      a="Gradle 동기화가 자동으로 실행되고, 끝나면 프로젝트 트리가 완성된다. 이어서 곧바로 빌드를 진행한다(오류가 없으면 앱을 바로 설치해 테스트 가능, 기기가 없으면 에뮬레이터 사용).")],
quote=quote("package name … 구글 스토어 전체에서 유일해야 하는 식별자이며, 한 번 배포하면 영구히 변경할 수 없습니다. 이름이 같아도 package name 이 다르면, 다른 앱으로 취급되어 같은 기기에 동시 설치됩니다.", s(31, 32, 33))))

# 12 ---------------------------------------------------------------
P(dict(kind=["diag", "table"], title="안드로이드 프로젝트에서 어느 파일을 열어야 하나",
parts=[
 dict(q="안드로이드 프로젝트에서 각 상황에 열어야 할 파일·폴더를 쓰시오. ⓐ \"라이브러리가 없다\"는 오류 ⓑ 권한이 거부되거나 앱이 실행되지 않음 ⓒ 리소스를 찾을 수 없다는 오류 ⓓ 라이브러리를 추가하려 함 ⓔ 새 액티비티를 등록하거나 권한을 추가하려 함 ⓕ 매번 사용하는 메인 소스 ⓖ 문자열·아이콘·layout을 넣을 곳",
      a="ⓐ <code>app/build.gradle.kts</code> ⓑ <code>AndroidManifest.xml</code> ⓒ <code>res/</code> 폴더 아래 위치와 파일명 ⓓ <code>app/build.gradle.kts</code>의 dependencies ⓔ <code>AndroidManifest.xml</code> ⓕ <code>MainActivity.kt</code> ⓖ <code>res/</code> 하위 구조",
      why="<p>교수님 강조: \"프로젝트의 구조는 폴더 자체의 구조보다, <b>오류가 났을 때 관련 있는 폴더를 찾는 것</b>이 중요\". 오류 문장의 명사로 판단한다: 라이브러리 → 의존성 → build.gradle.kts / 권한·실행 → 시스템에 신고하는 목록 → Manifest / 리소스 → res.</p>"),
 dict(q="Hello 프로젝트 트리의 각 파일·폴더 설명을 쓰시오: app/build.gradle.kts / src/test/ / src/androidTest/ / (루트) build.gradle.kts / settings.gradle.kts / gradle.properties / gradle/libs.versions.toml / local.properties",
      a="모듈 빌드 설정 / 로컬 단위 테스트(JVM) / 계측 테스트(기기 필요) / 프로젝트 전역 설정 / 모듈 목록, 저장소 / 빌드 옵션 / 의존성 버전 카탈로그 / SDK 경로(Git에 올리지 않음)",
      why="<p>build.gradle.kts가 <b>두 개</b>: 루트 = 프로젝트 전역, app = 모듈. minSdk·targetSdk·compileSdk와 dependencies는 <u>app</u> 쪽. 각 Gradle 파일의 역할은 2장 문제 4에서 더 자세히.</p>")],
fig=slide("ppa1", 36, 90),
quote=quote("프로젝트의 구조는 폴더 자체의 구조보다, 오류가 났을 때, 관련있는 폴더를 찾는 것이 중요합니다.", s(36, 37))))

# 13 ---------------------------------------------------------------
P(dict(kind=["mc"], title="안드로이드 스튜디오의 프로젝트 보기 모드 (○)",
parts=[
 dict(q="안드로이드 스튜디오 프로젝트 창의 보기 모드에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("Android 보기는 디스크의 실제 디렉토리 구조를 그대로 보여 준다.", False, "Android 보기는 실제 디렉토리 구조가 <b>아니라</b> 자주 쓰는 파일만 재배치한 화면이다."),
            ("Project 보기는 디스크의 실제 폴더 구조를 나타낸다.", True, "Project 보기는 디스크의 실제 폴더 구조를 그대로 보여 준다."),
            ("Packages 보기는 패키지 계층 중심으로 소스만 표시한다.", True, "Packages 보기는 패키지 계층 중심으로 소스만 표시한다."),
            ("Project Files 보기는 IntelliJ 설정을 포함해 프로젝트 폴더의 모든 파일을 표시한다.", True, "Project Files 보기는 IntelliJ 설정 파일까지 프로젝트 폴더의 모든 파일을 표시한다."),
            ("Scratches and Consoles는 프로젝트에 속하지 않는 임시 파일들을 표시한다.", True, "Scratches and Consoles는 프로젝트에 속하지 않는 임시 파일을 표시한다."),
            ("Project 보기에서 색 표시가 붙은 폴더는 리소스 루트로, R 클래스로 등록된다.", False, "Project 보기에서 색 표시가 붙은 폴더는 <b>소스 루트</b>로 컴파일 대상이다(app, main, androidTest, unitTest). R 클래스로 등록되는 것은 가로줄 폴더(res)다."),
            ("가로줄이 그어진 폴더(res)는 소스 루트로, 컴파일 대상이다.", False, "Project 보기에서 가로줄 폴더(res)는 <b>리소스 루트</b>로 R 클래스로 등록된다. 컴파일 대상인 소스 루트는 색 표시 폴더다."),
            ("표식 없는 파란 폴더(manifests, kotlin+java, keepRules)는 특별한 역할이 없는 일반 디렉터리다.", True, "표식 없는 파란 폴더(manifests, kotlin+java, keepRules)는 특별한 역할이 없는 일반 디렉터리다.")],
      a="ⓑ ⓒ ⓓ ⓔ ⓗ",
      why="<p>Project 보기 아이콘 3종은 \"<b>컴파일되나(소스 루트) / R로 등록되나(리소스 루트) / 아무것도 아님(일반)</b>\"으로 정리한다. Production/Tests 보기는 운영 코드만/테스트 코드만, Open Files는 편집기에 열린 파일만 표시한다.</p>")],
fig=slide("ppa1", 35, 90),
quote=quote("IntelliJ IDE 는 content root 표시를 두어, 빌드시에 각 폴더의 역할을 구분하여 표기한다.", s(34, 35))))

# 14 ---------------------------------------------------------------
P(dict(kind=["order", "name", "essay"], title="빌드: 무엇을, 누가, 어떤 순서로",
parts=[
 dict(q="안드로이드 앱의 빌드를 정의하시오(어디서 · 누가 · 무엇을 · 무엇으로 만드나).",
      a="개발용 컴퓨터 안에서, <b>Gradle</b>이 프로젝트의 소스 코드·리소스·매니페스트·라이브러리를 <b>설치 가능한 하나의 꾸러미</b>로 전환하는 과정. 결과는 APK 또는 AAB."),
 dict(q="안드로이드 앱 빌드의 단계를 순서대로 나열하시오: 패키징 / DEX 변환 / 서명 / 리소스 처리 / 컴파일",
      a="리소스 처리 → 컴파일 → DEX 변환 → 패키징 → 서명 (JDK 위에서 Gradle과 Android SDK가 차례로)",
      why="<p>순서는 산출물로 추론한다: 리소스가 R 클래스를 만들어야 코드가 컴파일되고 → 컴파일된 바이트코드를 DEX로 → 묶고 → 마지막에 서명(서명 뒤에 내용이 바뀌면 안 되므로 맨 끝).</p>"),
 dict(q="안드로이드 빌드에서 역할에 맞는 도구는? ⓐ 리소스를 이진 형식으로 변환하고 R 클래스를 생성 ⓑ 자바 바이트코드를 안드로이드용 DEX 형식으로 변환(2개) ⓒ 완성된 꾸러미에 서명 ⓓ 어떤 작업을 어떤 순서로 할지, 어떤 라이브러리를 내려받을지, 어떤 설정값을 적용할지를 build.gradle.kts에 적힌 내용에 따라 결정 ⓔ 코드에서 Activity나 Log 같은 클래스를 참조할 수 있게 해 주는 것",
      a="ⓐ AAPT2 ⓑ D8, R8 ⓒ apksigner ⓓ Gradle ⓔ compileSdk에서 지정한 API 정의(SDK에 포함). ⓐⓑⓒ는 모두 <b>Android SDK에 포함</b>된 개별 도구.",
      why="<p>\"Gradle이 DEX로 변환한다\" 같은 선지는 지휘와 수행을 섞은 함정 — 변환하는 것은 D8/R8이고, Gradle은 그 도구를 <b>호출</b>한다.</p>"),
 dict(q="빌드 과정 3층 그림의 빈칸과 각 역할을 쓰시오: [ ⓐ ] → 호출 → [ Kotlin 컴파일러, D8/R8, apksigner ] / 바닥 [ ⓑ ]",
      a="ⓐ <b>Gradle(지휘)</b>: 순서를 정하고 도구를 호출 / 가운데: 수행(Android SDK의 실제 작업 도구 D8/R8, apksigner 등) / ⓑ <b>JDK/JVM(토대)</b>: 위의 것들이 돌아가는 토대이며, 컴파일 시 참조되는 표준 라이브러리의 출처")],
fig=slide("ppa1", 41, 80),
quote=quote("JDK 위에서 Gradle, Android SDK가 리소스 처리, 컴파일, DEX 변환, 패키징, 서명이 차례로 이루어지면, APK 또는 AAB 가 완성되는 과정입니다.", s(38, 41))))

# 15 ---------------------------------------------------------------
P(dict(kind=["table", "essay"], title="JVM · JRE · JDK와 빌드에 JDK가 필요한 이유",
parts=[
 dict(q="JVM, JRE, JDK를 정의하고 포함 관계를 기호로 쓰시오.",
      a="JVM: 바이트 코드를 실행하는 엔진(.class를 읽어 실행) / JRE: JVM + 실행에 필요한 표준 라이브러리 / JDK: JRE + 필요한 개발도구. <b>JVM ⊂ JRE ⊂ JDK</b>"),
 dict(q="학생 B: \"안드로이드 앱을 빌드할 때는 프로그램을 돌리기만 하면 되니 JRE만 있으면 된다.\" 원문의 근거 4가지로 반박하시오.",
      a="① 빌드는 실행이 아니라 <b>컴파일</b>을 하는 것이다 ② JDK가 <b>컴파일러</b>를 갖고 있다 ③ Kotlin 컴파일러가 JDK의 <b>플랫폼 클래스</b>를 참조한다 ④ <b>Android Gradle Plugin</b>이 명시적으로 JDK를 요구한다",
      why="<p>핵심 단어는 \"<b>빌드 ≠ 실행</b>\". JRE는 실행까지만 담는다. 컴파일러가 필요한 순간 JDK가 필요하다.</p>"),
 dict(q="안드로이드 빌드에서 JDK의 세 가지 역할은? Gradle을 실행하려면 왜 자바 가상 머신이 필요한가? Kotlin 컴파일러의 결과물은?",
      a="빌드 도구들이 돌아가는 <b>토대</b> / 컴파일 시 참조되는 <b>표준 라이브러리의 출처</b> / 결과물의 <b>형식을 규정하는 기준</b>(스튜디오는 JDK를 내장). Gradle 자체가 자바로 작성된 프로그램이라서. Kotlin 컴파일러도 JVM 위에서 동작하며 결과물을 <b>JVM 바이트코드</b>로 내놓는다(이것을 D8/R8이 DEX로 바꿈)."),
 dict(q="Gradle의 toolchain으로 무엇을 할 수 있나?",
      a="Gradle 프로세스 자체가 도는 JVM과 컴파일을 하는 JDK를 <b>다르게 지정</b>할 수 있다.")],
fig=slide("ppa1", 42, 85),
quote=quote("빌드는 실행이 아니라 컴파일을 하는 것입니다.", s(39, 42))))

# 16 ---------------------------------------------------------------
dr_q, dr_a = fill(["비교 항목", "Debug 빌드", "Release 빌드"], [
    ["언제 생성되나", ("?", "개발자가 실행 버튼을 누를 때마다"), ("?", "배포 준비 시 명시적으로: Build &gt; Generate Signed App Bundle /APK 또는 ./gradlew assembleRelease")],
    ["서명 키", ("?", "자동 생성된 디버그 키"), ("?", "개발자의 업로드 키")],
    ["디버거 연결", ("?", "가능"), ("?", "불가(사용자가 받게 되므로)")],
    ["결과물", ("?", "app-debug.apk"), ("?", "app-release.apk / .aab")]])
P(dict(kind=["table", "diag"], title="APK vs AAB, Debug vs Release, 릴리스 서명",
parts=[
 dict(q="안드로이드 앱의 Debug 빌드와 Release 빌드를 비교하는 표를 채우시오." + dr_q, a=dr_a,
      why="<p>\"누가 쓰나\"로 판단: 개발자용(Debug)이면 디버거 연결 가능, 사용자용(Release)이면 불가.</p>"),
 dict(q="APK와 AAB를 각각 한 줄로 정의하시오. 현재 Play 스토어가 신규 앱에 요구하는 형식은?",
      a="APK(Android Package, .apk): 기기에 바로 설치할 수 있는 <b>완성된 앱</b> / AAB(Android App Bundle, .aab): Play 스토어에 올리는 <b>중간 산출물</b>(Play App Signing 과정 필요). 신규 앱은 APK 대신 <b>AAB</b>."),
 dict(q="AAB를 Play 스토어로 배포할 때 ⓐ 개발자가 Play Console에 올릴 때 쓰는 키 ⓑ 구글 서버가 보관하는 키와 그 이유는? 이 과정의 이름과 적용 범위는?",
      a="ⓐ 업로드 키 ⓑ 앱 서명 키 — 구글 서버가 AAB를 받아 <b>기기별로 APK를 다시 만들어 배포</b>하기 위해. Play App Signing(Play 스토어에 한정).",
      why="<p>AAB가 \"중간\"인 이유를 알면 키 두 개가 풀린다: 최종 APK는 구글이 만든다 → 구글이 서명해야 한다 → 구글이 <b>앱 서명 키</b>를 보관 → 개발자는 \"내가 올렸다\"만 증명 → <b>업로드 키</b>.</p>"),
 dict(q="릴리스 서명이 보증하는 두 가지는? 서명되지 않은 APK는? 서명 다음 최종 단계 2가지는?",
      a="앱의 <b>동일성과 무결성</b>. 설치할 수 없다. Google Play Console 업로드 또는 자체 배포.")],
fig=slide("ppa1", 40, 85),
quote=quote("AAB (Android App Bundle:.aab) : Play 스토어에 올리는 중간 산출물로, Play App Signing 과정이 필요합니다.", s(39, 40, 55))))

# 17 ---------------------------------------------------------------
P(dict(kind=["order", "diag"], title="실행 버튼부터 onCreate까지",
parts=[
 dict(q="빌드된 Hello 앱을 실행할 때 일어나는 일을 순서대로 나열하시오. ⓐ Zygote 프로세스를 복제해 앱 프로세스 생성 ⓑ <code>adb install app-debug.apk</code>로 APK를 기기에 전송 ⓒ MainActivity 인스턴스 생성 ⓓ 패키지 관리자가 서명을 검증하고 applicationId로 기존 앱과 충돌 검사 ⓔ 매니페스트에서 MAIN 액션 + LAUNCHER 카테고리를 가진 액티비티를 찾음 ⓕ <code>onCreate()</code> 호출 ⓖ ART가 APK 안의 DEX를 읽어 들여 기계어로 변환 ⓗ <code>adb shell am start -n com.example.hello/.MainActivity</code>",
      a="ⓑ → ⓓ → ⓗ → ⓔ → ⓐ → ⓖ → ⓒ → ⓕ",
      why="<p>두 덩어리: <b>설치</b>(adb install → 패키지 관리자 검증·설치) / <b>실행</b>(am start → 진입점 찾기 → 프로세스 → 코드 적재 → 객체 → 콜백). 실행 덩어리는 \"그릇 → 내용물\" 순서: 프로세스(그릇)가 있어야 ART가 DEX(코드)를 올리고, 코드가 있어야 MainActivity 객체를 만들고, 객체가 있어야 onCreate를 부른다.</p>"),
 dict(q="앱 아이콘을 눌렀을 때 어느 액티비티가 처음 뜰지는 무엇으로 정해지나? ART가 DEX 실행 외에 담당하는 두 가지는? 이때 PC에서 기기로 명령이 전달되는 경로는?",
      a="매니페스트에서 <b>MAIN 액션과 LAUNCHER 카테고리</b>를 가진 Activity. 메모리 할당, 가비지 컬렉션. 개발용 컴퓨터의 <b>adb 서버</b>가 기기의 <b>adbd</b> 데몬에게 명령을 전달(문제 7).",
      why="<p>패키지 관리자는 문제 1의 애플리케이션 프레임워크 구성요소이고, ART는 안드로이드 런타임 계층이다 — 실행 흐름이 계층 그림 위를 지나간다.</p>")],
fig=slide("ppa1", 44, 80),
quote=quote("adb install 은 APK를 기기로 전송하여 패키지 관리자에게 넘기고, 패키지 관리자는 서명을 검증한 후, applicationId 를 기준으로 기존 앱과 충돌하지 않는 지 확인하고 설치를 완료합니다.", s(43, 44))))

# 18 ---------------------------------------------------------------
life_q, life_a = fill(["상황", "Activity", "Application", "프로세스"], [
    ["화면 회전", ("?", "소멸 후 재생성"), ("?", "유지"), ("?", "유지")], ["다른 Activity로 이동", ("?", "onStop"), ("?", "유지"), ("?", "유지")],
    ["홈 버튼", ("?", "onStop"), ("?", "유지"), ("?", "유지")], ["뒤로 가기(마지막 화면)", ("?", "onDestroy"), ("?", "유지"), ("?", "잠시 유지")],
    ["최근 앱에서 밀어 제거", ("?", "콜백 없음"), ("?", "콜백 없음"), ("?", "종료")], ["메모리 부족으로 시스템 회수", ("?", "콜백 없음"), ("?", "콜백 없음"), ("?", "종료")],
    ["종료 후 다시 실행", ("?", "재생성"), ("?", "onCreate 재호출"), ("?", "새로 생성")]])
P(dict(kind=["table"], title="상황별로 무엇이 살아남나 (프로세스 · Application · Activity)",
parts=[
 dict(q="앱 프로세스, Application 객체, Activity의 관계를 쓰시오(무엇 안에 무엇이 있고, 수명은 어떻게 다른가, Activity는 Application을 어떻게 참조하나).",
      a="앱마다 별도의 프로세스가 만들어지고 그 안에서 ART 인스턴스가 작동. Application은 프로세스 시작 시 만들어지며 Activity와 <b>같은 힙 위에 나란히 놓인 별개의 객체</b>. Activity가 <code>getApplication()</code>으로 참조. Application은 <b>프로세스와 동일한 수명</b>, Activity는 짧고 반복적."),
 dict(q="상황별 표를 채우시오(Activity: 소멸 후 재생성 / onStop / onDestroy / 콜백 없음 / 재생성, Application: 유지 / 콜백 없음 / onCreate 재호출, 프로세스: 유지 / 잠시 유지 / 종료 / 새로 생성)." + life_q, a=life_a,
      why="<p>원리 하나로 표 전체가 나온다: <b>Application은 프로세스와 수명이 같다</b>. 프로세스가 살아 있으면 Application은 \"유지\", 프로세스가 죽으면 둘 다 \"콜백 없음\"(SIGKILL로 강제 제거되어 아무것도 호출되지 않음). Activity만 짧고 반복적이다. 함정: \"뒤로 가기로 마지막 화면을 닫으면 프로세스도 종료\" — 틀림, <u>잠시 유지</u>.</p>")],
fig=slide("ppa1", 45, 90),
quote=quote("Application 은 프로세스와 동일한 수명을 지니지만, Activity 는 짧고 반복적입니다.", s(45, 49))))

# 19 ---------------------------------------------------------------
P(dict(kind=["diag", "essay"], title="Activity 생명주기로 생기는 문제들",
parts=[
 dict(q="화면을 회전할 때 호출되는 Activity 콜백 6개를 순서대로 쓰시오. 이때 onDestroy가 호출되었다면 앱 프로세스는 죽은 것인가?",
      a="onPause → onStop → onDestroy(기존 Activity 소멸) → onCreate → onStart → onResume(새 Activity 생성). 아니다 — onDestroy가 호출되어도 앱과 프로세스는 살아 있다."),
 dict(q="\"앱이 끝날 때 호출되는 종료 콜백에서 데이터를 저장하겠다.\" 무엇이 문제이고, 어디서 저장해야 하나?",
      a="앱에는 onCreate()에 대응되는 <b>'종료 콜백'이 없다</b>. 실제 기기에서 앱이 끝나는 방식은 프로세스가 <b>SIGKILL로 강제 제거</b>되는 것이다. 데이터 저장은 <b>onPause 또는 onStop</b> 시점에."),
 dict(q="\"Activity의 onStop이 오면 앱이 백그라운드로 갔다고 판단하겠다.\" 무엇이 문제이고, 무엇을 써야 하나?",
      a="Activity A에서 B로 이동할 때도, 홈 버튼으로 앱 전체가 백그라운드로 갈 때도 똑같이 onStop이 호출되어 <b>콜백으로는 구분되지 않는다</b>. 앱 수준의 생명주기를 제공하는 <b>ProcessLifecycleOwner</b>(개별 Activity의 전환은 무시하고 앱 전체가 보이는지 여부만 알려 줌).",
      why="<p>두 경우 모두 \"콜백에 기대면 안 되는\" 경우지만 이유가 다르다: 종료는 콜백이 <u>아예 없음</u>, 백그라운드는 콜백이 <u>있지만 구분이 안 됨</u>.</p>"),
 dict(q="사용자가 홈 버튼 → 다른 앱 사용 → (메모리 부족으로 우리 앱 프로세스 종료) → 최근 앱에서 우리 앱을 다시 선택했다. 내부에서 일어나는 4단계와, 이때 onCreate가 받는 인자의 특징은? 사용자에게는 어떻게 보이나?",
      a="새 프로세스 생성 → Application.onCreate() 다시 호출 → 마지막에 보던 Activity 재생성 → onCreate(savedInstanceState). 인자가 <b>null이 아님</b>. 사용자는 앱을 계속 쓰고 있는 것처럼 보이지만, 내부적으로는 프로세스가 완전히 새로 만들어진 것.",
      why="<p>savedInstanceState가 null이 아니라는 것은 \"저장해 둔 상태(Bundle)가 있다\"는 신호다 — 3장 rememberSaveable, 6장 onSaveInstanceState가 바로 이 상황을 위한 장치다.</p>")],
quote=quote("앱에는 onCreate()이 있지만, 대응되는 '종료 콜백' (종료시 시스템이 함수 호출)이 없습니다. 실제 기기에서 앱이 끝나는 방식은 프로세스가 SIGKILL 로 강제로 제거되는 것입니다.", s(46, 47))))

# 20 ---------------------------------------------------------------
P(dict(kind=["name"], title="콜백 · 리스너 · 핸들러 · 훅",
parts=[
 dict(q="설명에 맞는 용어를 쓰시오. ⓐ 시스템 흐름 중간에 끼워 넣는 지점 ⓑ 개발자가 함수를 만들어 시스템에 넘기면 시스템이 적절한 때에 그 함수를 호출하는 것 — 나중에 호출될 것을 전제로 등록해 두는 함수 ⓒ 사건을 처리하는 콜백(ⓓ와 혼용됨) ⓓ 클릭·스크롤 같은 특정 사건을 기다리는 콜백. 그리고 Activity의 onCreate는 넷 중 무엇의 예인가?",
      a="ⓐ 훅(hook) ⓑ 콜백(Callback) ⓒ 핸들러(handler) ⓓ 리스너(listener). onCreate는 콜백(시스템이 생명주기에 맞춰 호출).",
      why="<p>포함 관계로 기억: <b>콜백이 가장 넓고</b>, 그중 사건을 <u>기다리면</u> 리스너, 사건을 <u>처리하면</u> 핸들러(둘은 혼용). 훅은 함수가 아니라 <b>지점</b>이라는 점이 다르다.</p>")],
quote=quote("콜백 (Callback): 개발자가 함수를 만들어 시스템에 넘기면, 시스템이 적절한 때에 그 함수를 호출하는 경우를 의미합니다.", s(48))))

# 21 ---------------------------------------------------------------
P(dict(kind=["diag", "name"], title="Logcat과 Log",
parts=[
 dict(q="Logcat의 정체는?(누가 기록하나, 저장 방식) 안드로이드 스튜디오 왼쪽 탭의 Logcat 창은 무엇인가?",
      a="기기가 켜져 있는 동안 커널·시스템 서비스·설치된 <b>모든 앱</b>이 태그와 수준을 지정해 계속 기록을 남기는 <b>시스템 전체의 로그 저장소</b>. 크기가 정해져 오랜 기록부터 덮어쓰는 <b>순환버퍼</b>. Logcat 창은 adb 서버를 통해 기기로부터 내용을 받아 와 그 저장소를 보여 주는 창."),
 dict(q="Log 클래스의 메서드 v / d / i / w / e는 각각 어떤 용도이고, Logcat 검색어는? 개발 중 경고만 걸러 보려면?",
      a="Log.v: 상세 추적, level:verbose / Log.d: 개발 중 확인, level:debug / Log.i: 일반정보, level:info / Log.w: 경고, level:warn / Log.e: 오류, level:error. 경고만: <code>level:warn</code>"),
 dict(q="<code>Log.d(\"MainActivity\", \"count=$count\")</code>에서 첫째 인자와 둘째 인자의 이름과 성질, Logcat에서의 표시 위치는?",
      a="첫째 = <b>tag</b>(\"MainActivity\"): 고정된 분류 이름표로 여러 로그가 그 값을 공유, Logcat에서 별도의 열로 표시 / 둘째 = <b>message</b>(msg, \"count=…\"): 호출 때마다 달라지는 자유 서술, 본문의 열로 표시. 둘 다 필터로 검색 가능."),
 dict(q="Logcat 검색어 <code>package:mine</code>은 무엇을 보여 주며, mine은 무엇으로 해석되나? 패키지를 직접 지정하는 검색어는?",
      a="현재 프로젝트의 앱만. mine은 현재 열려 있는 안드로이드 앱을 가리키는 특수한 값으로, 안드로이드 스튜디오가 <b>applicationId</b>로 해석. <code>package:com.example.hello</code>"),
 dict(q="개발 중에 사용자 아이디·인증토큰을 Log.d로 찍었다. 배포 후 생길 문제와 로그의 다른 단점은? 릴리스 빌드에서 Log.d를 없애는 두 방법과, <code>if (BuildConfig.DEBUG) { Log.d(\"Tag\", \"message\") }</code>에서 조건문 <u>자체</u>가 사라지는 이유는?",
      a="개발자 옵션을 켠 기기를 컴퓨터에 연결하고 <code>adb logcat</code>을 실행하면 <b>누구든</b> 앱의 로그를 읽을 수 있어, 배포된 앱에서도 계속 기록되며 외부로 드러난다. 로그는 문자열을 만들고 시스템 호출을 하므로 <b>성능에도 부담</b>. 방법: R8 규칙으로 제거 / 조건부로 감싸기. BuildConfig는 빌드할 때 자동 생성되는 클래스이고 DEBUG는 <b>컴파일 시점에 값이 확정되는 상수</b>(Debug 빌드 true, Release 빌드 false)라서.",
      why="<p>\"컴파일 시점 상수\"는 5장 const val(컴파일 시점에 값이 확정)과 같은 개념. 로그 레벨의 우선순위(wtf &gt; e &gt; w &gt; i &gt; d &gt; v)는 6장 문제 2.</p>")],
quote=quote("Logcat 은 기기가 켜져있는 동안 커널, 시스템 서비스, 설치된 모든 앱이 계속해서 태그와 수준을 지정하여 기록을 남기는 시스템 전체의 로그 저장소로 크기가 정해져 오랜 기록부터 덮어쓰는 순환버퍼 입니다.", s(50, 51, 52, 53))))

# 22 ---------------------------------------------------------------
test_q, test_a = fill(["비교 항목", "로컬 단위 테스트", "계측 테스트"], [
    ["폴더", ("?", "app/src/test"), ("?", "app/src/androidTest")], ["실행 위치", ("?", "개발용 PC의 JVM"), ("?", "기기 또는 에뮬레이터")],
    ["Gradle 태스크", ("?", "testDebugUnitTest"), ("?", "connectedDebugAndroidTest")], ["대상", ("?", "순수 로직, 계산, 변환"), ("?", "UI, DB, 시스템 연동")],
    ["속도", ("?", "매우 빠름"), ("?", "설치가 필요해 느림")], ["제약", ("?", "안드로이드가 없어 Context나 Log를 쓰지 못함"), ("?", "기기 필요")]])
P(dict(kind=["table", "diag"], title="로컬 단위 테스트 vs 계측 테스트",
parts=[
 dict(q="안드로이드 테스트 두 종류를 비교하는 표를 채우시오." + test_q, a=test_a,
      why="<p>모든 칸이 \"<b>안드로이드가 있나?</b>\"에서 나온다. PC의 JVM(없음) → 빠르지만 순수 로직만 / 기기(있음) → UI·DB 가능하지만 설치 때문에 느림. 태스크 이름에 <u>connected</u>(기기 연결)가 들어가면 계측 테스트.</p>"),
 dict(q="안드로이드 앱에서 어느 테스트로 확인하나? ⓐ 온도 변환 공식이 맞는지 ⓑ 버튼을 누르면 화면이 바뀌는지 ⓒ Room DB 저장 ⓓ <code>Log</code>를 쓰는 테스트를 src/test에 넣었더니 실패했다. 이유는?",
      a="ⓐ 로컬 단위 테스트 ⓑ 계측 테스트 ⓒ 계측 테스트 ⓓ 로컬 단위 테스트는 개발용 PC의 JVM에서 돌아 안드로이드가 없으므로 Log·Context를 쓸 수 없다.")],
fig=slide("ppa1", 54, 85),
quote=quote("안드로이드가 없기 떄문에, Context 나 Log 같은 것을 쓰지 못합니다.", s(54))
 + "<p><span class='fix'>원본 s54 \"떄문에\" → 때문에</span></p>"))

# 23 ---------------------------------------------------------------
P(dict(kind=["calc", "name"], title="dp와 화면 밀도",
parts=[
 dict(q="AVD 하드웨어 프로필(Select Hardware) 항목 Size, Resolution, Density는 각각 무엇인가(예시값 포함)? 하드웨어 선택은 결국 무엇을 고르는 과정인가?",
      a="Size: 화면의 물리적 대각선 길이(인치) / Resolution: 픽셀 해상도(예: 1080 x 2400) / Density: 화면 밀도, 1인치 안에 들어가는 pixel 수(예: 420 dpi = dot per inch). 'Pixel 8 모양의 껍데기'를 선택하는 과정."),
 dict(q="dp의 정식 이름과 목적은? 1dp = 1px가 되는 기준 밀도는? px를 구하는 식과, DisplayMetrics.density로 얻는 값의 식을 쓰시오.",
      a="density independent pixel. 밀도와 무관하게 <b>물리적 크기를 일정하게</b> 유지하기 위한 논리 단위. 160dpi(medium density; mdpi). <b>px = dp × density = dp × (dpi / 160)</b>. density = dpi / 160."),
 dict(q="계산하시오. ⓐ 320dpi(xhdpi)에서 48dp는 몇 px? ⓑ 480dpi(xxhdpi)에서 48dp는? ⓒ 420dpi 기기에서 16dp는? ⓓ 48dp 버튼의 물리적 크기는 기기마다 달라지나?",
      a="ⓐ 48 × (320/160) = 48 × 2.0 = <b>96px</b> ⓑ 48 × 3.0 = <b>144px</b> ⓒ 16 × (420/160) = 16 × 2.625 = <b>42px</b> ⓓ 달라지지 않는다: 48 / 160 = <b>0.3인치</b>로 모두 같다.",
      why="<p>식은 정의에서 만든다: 160dpi에서 1dp = 1px → dpi가 2배(320)면 같은 dp를 2배 px로 그려야 같은 크기. 검산: dpi &gt; 160이면 px가 dp보다 커야 한다.</p>"),
 dict(q="실무에서 많이 쓰는 dp 값의 쓰임은? 48dp / 16dp / 8dp / 4dp / 56dp·64dp. 여백과 크기를 8의 배수로 맞추라는 근거는?",
      a="48dp: 최소 터치 영역, 버튼과 아이콘 버튼의 기본 크기 / 16dp: 화면 가장자리 기본 여백 / 8dp: 요소간 기본 간격 / 4dp: 촘촘한 간격(8dp 격자의 절반) / 56dp·64dp: 모바일·데스크톱 앱 바의 높이. Material Design이 <b>8dp 격자(grid)</b>를 권장 → 화면 전체 정렬이 자연스럽게 구현됨.")],
fig=slide("ppa1", 69, 80),
quote=quote("dp(density independent pixel) 는 밀도와 무관하게, 물리적 크기를 일정하게 유지하기 위한 논리 단위이며, 160dpi (=medium density;mdpi) 화면에서 1dp = 1px(pixel)에 해당합니다.", s(67, 68, 69))))

# 24 ---------------------------------------------------------------
P(dict(kind=["diag", "mc"], title="AVD 만들기: 하드웨어 프로필과 시스템 이미지",
parts=[
 dict(q="AVD의 시스템 이미지는 무엇을 결정하나(2가지)? 다음 경우 어떤 시스템 이미지를 고르나? ⓐ Play 스토어 앱이 필요 ⓑ 위치·지도 같은 Google 서비스만 필요 ⓒ 루트 권한(adb root)이 필요",
      a="안드로이드 버전(API 레벨)과 Google 서비스 포함 여부. ⓐ Google Play 이미지 ⓑ Google APIs ⓒ AOSP(Android open source project, 표기가 없는) 이미지",
      why="<p>AVD = <b>몸(하드웨어 프로필: 'Pixel 8 모양의 껍데기')</b> + <b>운영체제(시스템 이미지: 'Android 15')</b>. 이미지 선택은 포함된 것의 양으로: Play 스토어까지 포함 → Google APIs(구글 서비스만) → AOSP(구글 것 없음, 대신 루트 권한).</p>"),
 dict(q="AVD에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("같은 Pixel 8 모양의 프로필에 API 24부터 36까지 여러 시스템 이미지를 각각 씌운 AVD를 여러 개 만들 수 있다.", True, "AVD의 기기 프로파일(Pixel 8 모양)과 시스템 이미지(API 24~36)는 서로 <b>독립적</b>이라, 한 프로파일에 여러 이미지를 각각 씌울 수 있다."),
            ("Verify configuration 단계에서는 AVD의 이름, 화면의 방향, RAM 등을 최종 확인한다.", True, "Verify configuration은 AVD의 기기 프로파일과 시스템 이미지 선택이 끝난 뒤 이름·화면 방향·RAM 등 환경 구성을 확인하는 단계다."),
            ("생성된 AVD는 Device Manager의 Virtual 탭에만 나타나고 실행 대상 목록에는 나타나지 않는다.", False, "생성된 AVD는 Device Manager의 Virtual 탭과 <b>도구 모음의 실행 대상(target device) 드롭다운 메뉴</b>에 모두 나타난다."),
            ("Device 탭의 Name은 AVD의 이름으로, Device Manager 목록과 툴바의 실행 대상 드롭다운에 표시된다.", True, "AVD의 Name은 Device Manager 목록과 툴바의 실행 대상 드롭다운에 표시된다. 실습 AVD는 Phone → Medium phone, System image API level 37.1, Service는 Google API를 선택했다."),
            ("새 AVD는 Welcome 화면의 More Actions → Virtual Device Manager → create virtual device로 만들 수 있다.", True, "새 AVD는 Welcome(Project) 화면 아래 More Actions에서 Virtual Device Manager를 바로 선택해 만들 수 있다.")],
      a="ⓐ ⓑ ⓓ ⓔ")],
quote=quote("기기 프로파일과 시스템 이미지는 두 개가 독립적이기 때문에, 같은 Pixel 8 모양의 프로필에 API 24 부터 API 36까지 여러 시스템 이미지를 각각 씌운 AVD 를 여러개 만들 수 있습니다.", s(56, 57, 67, 71, 72))))

# 25 ---------------------------------------------------------------
P(dict(kind=["diag"], title="AVD 추가 설정(Additional Settings) 고르기 (○)",
parts=[
 dict(q="AVD 카메라(Camera Front / Rear) 설정에서 무엇을 고르나? ⓐ QR 코드 스캔을 테스트 ⓑ 카메라 앱이 실행 시 오류가 남 — 원인 설정은? ⓒ AR 기능을 3D로 구성된 가상의 방에서 마우스로 둘러보며(보통 후면) ⓓ 소프트웨어로 생성한 단순한 애니메이션 패턴(보통 전면)",
      a="ⓐ Webcam0(호스트 PC의 실제 웹캠 영상) ⓑ None(카메라가 없음) ⓒ VirtualScene ⓓ Emulated",
      why="<p>\"무엇을 흉내 내야 하나\"로 고른다: 실제 영상이 필요(웹캠) / 3D 공간(VirtualScene) / 뭔가 찍히기만 하면 됨(Emulated) / 아무것도 없음(None → 카메라 앱 오류).</p>"),
 dict(q="AVD 설정에서 무엇을 쓰나? ⓐ 에뮬레이터의 네트워크를 일부러 느리게 만드는 설정과 두 값의 뜻, 'Full/None'의 뜻 ⓑ 이전 종료 시점 상태를 스냅샷에서 복원해 수 초 만에 켜짐(앱 설치·로그인 상태 유지) ⓒ 스냅샷이 손상되었거나, 권한 요청 대화상자·온보딩 화면을 매번 초기 상태에서 보고 싶음 ⓓ 화면이 검거나 graphic이 깨짐 ⓔ 실기기 외형 프레임을 씌우지 않고 화면만",
      a="ⓐ Network – Speed/Latency: Speed = 대역폭, Latency = 응답 지연, 'Full/None' = 제한 없음(호스트 PC의 인터넷 속도 그대로) ⓑ Quick boot ⓒ Cold boot(매번 처음부터, 수십 초~수 분) ⓓ Graphics를 Software-GLES 2.0(CPU로 렌더링, 호환성 좋음)으로. 기본은 Hardware(호스트 GPU), Automatic은 환경에 따라 자동 ⓔ Device skin: None"),
 dict(q="AVD의 성능·저장 설정 권장값은? ⓐ Multi-Core CPU(전부 할당하면?) ⓑ RAM(호스트 16GB 이상 / 8GB) ⓒ VM heap(무엇이고 기본값을 두면?) ⓓ Preferred ABI를 optimal로 ⓔ Internal storage(무엇이 어디에, 보통 크기) ⓕ Expanded storage 3가지",
      a="ⓐ 호스트 코어 수의 절반 정도(보통 4). 전부 할당하면 Android Studio 자체가 느려져 역효과 ⓑ 4096MB / 2048MB ⓒ 앱 프로세스 하나에 허용되는 자바 힙 상한. 기본값을 유지하면 실기기와 가까운 조건 ⓓ 네이티브 코드의 명령어 집합 중 호스트 환경에서 가장 빠른 방식을 에뮬레이터가 선택 ⓔ 앱과 앱 데이터가 저장되는 공간, 호스트 디스크에 이미지 파일로 만들어짐(보통 10GB) ⓕ None(외부 저장소 없음) / Custom(기본, 512MB, Android Studio가 관리하는 가상 SD 카드) / 외부 파일 지정(이미 만들어 둔 이미지 파일, 여러 AVD가 공유 가능)"),
 dict(q="AVD 시작 방향(Startup-Orientation)을 정한 뒤 실행 중 화면을 회전하는 단축키는? 회전하면 상태를 저장하지 않은 앱에서 무슨 일이 생기나?",
      a="Ctrl + F11 또는 Ctrl + 왼쪽/오른쪽 화살표. 화면이 회전하면 Activity가 파괴되었다가 다시 만들어지므로 입력값이 사라진다(문제 19, 3장 rememberSaveable).")],
quote=quote("Cold: 매번 처음부터 부팅하므로, 수십초에서 수분까지 걸릴 수 있습니다. (스냅샷이 손상되었거나, 앱 최초 실행 동작을 매번 초기 상태(권한요청 대화상자, 온보딩화면)에서 보여 줄 때에 사용됨)", s(58, 59, 60, 61))))

# 26 ---------------------------------------------------------------
P(dict(kind=["name"], title="앱 바 구성요소와 에뮬레이터 조작 (○)",
parts=[
 dict(q="앱 바(Top App Bar)를 정의하고 구성요소 이름을 쓰시오: 왼쪽 화살표 / 오른쪽 구성 요소 / 점 세 개 / 본문 위에 떠 있는 실행 버튼",
      a="화면 제목, 뒤로 가기 버튼, 검색이나 메뉴 같은 주요 동작을 모아 놓은 띠 모양의 UI 요소. 네비게이션 아이콘 / 액션 아이템 / 오버플로 메뉴 / FAB(Floating Action Button, 부동 실행 버튼)"),
 dict(q="에뮬레이터 상단 메뉴 바의 버튼: ⓐ 최근 사용한 앱 목록 ⓑ Display의 DPI 설정 ⓒ 이전 화면으로 ⓓ 홈 화면으로",
      a="ⓐ Overview 버튼 ⓑ Device setting 버튼 ⓒ Back 버튼 ⓓ Home 버튼 (그 밖에 회전 버튼: 왼쪽 또는 오른쪽으로 화면 회전)"),
 dict(q="에뮬레이터에서 앱을 길게 눌러 앱 정보 → 제거로 지웠다. 프로젝트 원본도 지워졌나? 다시 실행하려면?",
      a="아니다, 원본은 남아 있다. 상단의 녹색 실행 버튼을 누르면 재설치된다.",
      why="<p>\"에뮬레이터 = 설치된 사본, 프로젝트 = 원본\". 실행 버튼이 빌드 → install → 실행을 다시 하므로(문제 17) 재설치된다.</p>")],
fig=slide("ppa1", 70, 80),
quote=quote("에뮬레이터의 앱을 삭제해도 원본은 남아있습니다. 다시 실행하고 싶다면 상단의 녹색 실행 버튼을 누르면 재설치됩니다!", s(70, 73, 77))))

KEYWORDS = [
 ("SDK (Software Development Kit)", "소프트웨어 개발에 필요한 라이브러리와 각종 도구 모음. 안드로이드 앱 개발에 필수", s(11)),
 ("API level", "시스템 내부에서 사용되는 버전 숫자. 바뀌면 앱 프로그래밍 관점에서도 변경된 사항이 있다고 생각해도 무방", s(4)),
 ("리눅스 커널", "운영체제의 주요 기능(메모리 관리, 파일시스템, 장치 제어 등)을 담당. 공유 메모리, 바인더 같은 공유 기능을 추가", s(7)),
 ("바인더", "프로세스간의 통신 기능 제공", s(9)),
 ("공유 메모리", "프로세스간 데이터 공유 기능 제공", s(9)),
 ("라이브러리", "소프트웨어 개발의 생산성을 높이기 위해 미리 작성해 놓은 코드 집합. 시스템에서 가장 큰 계층. 오픈 소스로 개발된 라이브러리 + 안드로이드 전용 라이브러리", s(7)),
 ("Bionic", "C 라이브러리", s(9)), ("Webkit", "웹엔진", s(9)), ("SQLite", "데이터베이스 엔진", s(9)), ("SSL", "보안통신", s(9)),
 ("FreeType", "폰트 처리 엔진", s(9)), ("미디어 프레임 워크", "다양한 멀티미디어 형식 지원", s(9)), ("SGL", "2D 그래픽스", s(9)), ("Open GL ES", "3D 그래픽스", s(9)),
 ("안드로이드 런타임 (ART: Android Runtime)", "Java 언어로 개발된 코드를 실행하기 위한 가상 머신과 핵심 Java 라이브러리. Android 12부터 모듈로 분리되어 시스템 업데이트로 갱신 가능", s(8)),
 ("애플리케이션 프레임워크", "두 번째로 큰 계층. 앱의 구동과 상태 관리를 담당하는 액티비티 관리자, 앱 설치 및 삭제를 담당하는 패키지 관리자 등 시스템 서비스", s(8)),
 ("JDK (Java Development Kit)", "자바 프로그램을 작성하고 컴파일하며 실행하기 위한 도구 모음. 컴파일러·프로파일러·아카이브 생성기 + API 라이브러리 + JVM", s(13)),
 ("JBR (JetBrains Runtime)", "OpenJDK를 확장한 JDK. 안드로이드 스튜디오와 함께 배포되어 JDK를 따로 설치할 필요가 없음", s(14)),
 ("Gradle", "컴파일, 리소스 처리, 의존성 해결, 테스트 실행, 패키징, 서명, 배포를 하나의 흐름으로 자동화하는 JVM 기반의 공식 빌드 도구", s(14)),
 ("AVD (Android Virtual Device)", "시스템 이미지를 통해 기기 프로파일과 RAM 및 저장 공간 설정을 반영한 가상 기기의 정의와 그것을 실행하는 인스턴스", s(21)),
 ("adb 서버", "개발용 PC에서 백그라운드로 상주하며 클라이언트의 요청을 적절한 기기로 중계. localhost TCP 5037번 포트", s(23)),
 ("adbd", "기기 측에서 실행되는 daemon. 서버에서 전달받은 명령을 기기 안에서 실제로 수행(APK 설치, 로그 전송, 셸 명령, 파일 전송)", s(23)),
 ("daemon", "배경(Background)에서 계속 실행되면서, 요청이 들어올 때 정해진 서비스를 제공하는 유닉스 계열 운영체제의 프로세스", s(23)),
 ("minSdk (최소 API 수준)", "앱이 설치 가능한 가장 낮은 안드로이드 버전", s(25)),
 ("targetSdk (대상 API 수준)", "앱이 어느 버전을 기준으로 동작을 검증했는지, 즉 배포 요건", s(25)),
 ("compileSdk (컴파일 API 수준)", "compile 시 사용할 android.jar의 버전. IDE나 AGP에 의해 제약을 받는 유일한 값", s(25)),
 ("액티비티", "창(Window)을 제공하고 그 안에 UI를 배치하며 사용자 입력을 받아 상호작용하는 하나의 화면을 담당하는 앱의 구성요소", s(26)),
 ("명령형 (imperative)", "XML layout. 상태가 바뀌면 개발자가 해당 View 객체를 찾아 직접 속성을 변경", s(27)),
 ("선언형 (declarative)", "Compose. 상태에 따른 화면을 함수로 기술해 두고, 상태가 바뀔 때 프레임워크가 해당 함수를 재호출", s(27)),
 ("View 체계", "실행 시점에 화면을 구성하는 객체 계층으로, 실제 측정, 배치, 그리기를 수행하는 실체", s(27)),
 ("package name", "구글 스토어 전체에서 유일해야 하는 식별자. 한 번 배포하면 영구히 변경 불가. com.example은 예약 접두사", s(31)),
 ("빌드", "Gradle이 소스 코드, 리소스, 매니페스트, 라이브러리를 설치 가능한 하나의 꾸러미로 전환하는 과정", s(38)),
 ("AAPT2", "리소스를 이진 형식으로 변환하고 R 클래스를 생성하는 SDK 도구", s(38)),
 ("D8 / R8", "자바 바이트 코드를 안드로이드용 DEX 형식으로 바꾸는 SDK 도구", s(38)),
 ("apksigner", "완성된 꾸러미에 서명하는 SDK 도구", s(38)),
 ("APK (Android Package)", "기기에 바로 설치할 수 있는 완성된 앱", s(39)),
 ("AAB (Android App Bundle)", "Play 스토어에 올리는 중간 산출물. Play App Signing 과정 필요", s(39)),
 ("JVM / JRE / JDK", "바이트 코드 실행 엔진 / JVM + 실행에 필요한 표준 라이브러리 / JRE + 개발도구", s(42)),
 ("toolchain", "Gradle 프로세스 자체가 도는 JVM과 컴파일을 하는 JDK를 다르게 지정할 수 있게 하는 것", s(42)),
 ("Zygote", "복제하여 앱 프로세스를 생성하는 프로세스", s(44)),
 ("ProcessLifecycleOwner", "앱 수준의 생명주기를 제공. 개별 Activity의 전환은 무시하고 앱 전체가 보이는지 여부만 알려 줌", s(47)),
 ("콜백 (Callback)", "개발자가 함수를 만들어 시스템에 넘기면 시스템이 적절한 때에 호출. 나중에 호출될 것을 전제로 등록해 두는 함수", s(48)),
 ("리스너 (listener)", "특정 사건을 기다리는 콜백(클릭, 스크롤 등)", s(48)),
 ("핸들러 (handler)", "사건을 처리하는 콜백. 리스너와 혼용", s(48)),
 ("훅 (hook)", "시스템 흐름 중간에 끼워 넣는 지점", s(48)),
 ("디버깅", "로그캣, 디버거, 프로파일러를 통해서 이미 발생한 문제의 원인을 찾는 일", s(50)),
 ("Logcat", "커널, 시스템 서비스, 설치된 모든 앱이 태그와 수준을 지정하여 기록을 남기는 시스템 전체의 로그 저장소. 오랜 기록부터 덮어쓰는 순환버퍼", s(50)),
 ("테스팅", "문제가 발생했는지 자동으로 확인하는 단계(로컬 단위 테스트 / 계측 테스트)", s(54)),
 ("Release 서명", "배포용 릴리스 빌드에 개발자의 업로드 키로 서명. 앱의 동일성과 무결성을 보증", s(55)),
 ("Quick boot / Cold boot", "이전 종료 시점의 상태를 스냅샷에서 복원 / 매번 처음부터 부팅", s(59)),
 ("dp (density independent pixel)", "밀도와 무관하게 물리적 크기를 일정하게 유지하기 위한 논리 단위. 160dpi(mdpi)에서 1dp = 1px", s(68)),
 ("Density (dpi)", "화면 밀도. 1인치 안에 들어가는 pixel 수", s(67)),
 ("시스템 이미지 (System image)", "안드로이드의 버전(API 레벨)과 Google 서비스의 포함 여부를 결정", s(71)),
 ("FAB (Floating Action Button)", "부동 실행 버튼", s(70)),
]

OUTRO = """
<h3>1장 범위 대조표 — 슬라이드 → 문제</h3>
""" + table(["슬라이드", "내용", "문제"], [
 ["s4~6", "안드로이드 개요·버전", "2"], ["s7~9", "5계층", "1"], ["s10", "언어 표·Kotlin DSL", "3"],
 ["s11, 14~15, 21", "개발 방식·설치·위치", "4, 6"], ["s12~13, 24, 55", "개발 절차·환경·생성", "5"], ["s22~23", "adb", "7"],
 ["s25, 32", "API 수준", "8"], ["s26~27", "템플릿·UI 방식", "9"], ["s28", "DSL", "10"], ["s31~33", "Name·package·저장 위치", "11"],
 ["s34~35", "보기 모드", "13"], ["s36~37", "구조·오류 폴더", "12"], ["s38~41", "빌드", "14"], ["s39, 42", "JVM/JRE/JDK", "15"],
 ["s39~40, 55", "APK/AAB·Debug/Release·서명", "16"], ["s43~44", "실행", "17"], ["s45, 49", "수명 표", "18"],
 ["s46~47", "생명주기 문제", "19"], ["s48", "용어", "20"], ["s50~53", "Logcat", "21"], ["s54", "테스트", "22"],
 ["s67~69", "dp", "23"], ["s56~57, 67, 71~72", "AVD 프로필·이미지", "24"], ["s58~61", "AVD 추가 설정", "25"], ["s70, 73, 77", "앱 바·버튼·삭제", "26"]]) + """
<div class="note"><b>뺀 슬라이드</b>(시험 무관으로 판단): s1~3 표지·성적·출석·일정 / s16~20 설치 마법사 화면 / s29~30 New Project 클릭 / s62~66 SDK 내려받기·도킹 절차 / s74~76 한국어·맞춤법·시간대·SD 마운트 절차.</div>
<div class="note"><b>원본 오탈자</b>: s4 "생가해도" <span class="fix">→ 생각해도</span> / s6 Android 14 "API level 33" <span class="fix">→ 34로 보임</span> / s15 "abd" <span class="fix">→ adb</span> / s37 "AndroidMainfest" <span class="fix">→ AndroidManifest</span> / s54 "떄문에" <span class="fix">→ 때문에</span>.</div>
"""
