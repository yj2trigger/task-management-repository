"""5장 ppa5 — Widget과 Compose 대응·온도 변환기 확장(RadioButton·온도계·Slider)."""
from qbook2 import s as _s, quote, table, fill, slide


def s(*n):
    return _s(*n, deck="ppa5")


INTRO = """
<div class="note">소문제를 풀고 → 바로 아래 <b>답·해설</b>. 이중선(옅은 배경) = 문제, 가는 실선 = 답·해설, 굵은 실선 = 원문(원본 ppa5 슬라이드 번호·쪽 위/아래), 점선 = 해설 정리.
앞 장에서 이미 물은 지식은 다시 묻지 않고 "→ N장 문제 M"으로 잇습니다. 온도 변환기 기본형은 4장 문제 16·17.</div>
<h2>5장. ppa5 — Widget과 Compose 대응·온도 변환기 확장(RadioButton·온도계·Slider)</h2>
"""

ITEMS = []
P = ITEMS.append

# 1
tv_q, tv_a = fill(["단계", "클래스", "TextView에 무엇을 더했나"], [
    ["1", "View", "(최상위)"], ["2", "TextView", "텍스트 표시"],
    ["3", ("?", "CheckedTextView"), "체크 표시"], ["3", ("?", "EditText"), "편집"], ["3", ("?", "Button"), "누름(입력용)"],
    ["4", ("?", "CompoundButton(추상 클래스)"), "Button에 선택/비선택 두 상태"],
    ["5", ("?", "CheckBox, RadioButton, ToggleButton"), "CompoundButton의 자식"]])
P(dict(kind=["table", "mc"], title="위젯과 TextView 계층",
parts=[
 dict(q="위젯을 정의하고, 위젯과 GUI의 관계를 쓰시오.",
      a="위젯은 버튼, 체크박스, 스크롤 바, 입력 창처럼 화면을 구성하는 <b>작은 시각적 부품</b>이다. 위젯이 모여 사용자가 보고 만지는 GUI를 완성하므로, 위젯은 <b>GUI의 하위 개념</b>이다."),
 dict(q="TextView 계열 위젯의 계층을 완성하시오." + tv_q, a=tv_a,
      why="<p>TextView 계층은 \"<b>무엇을 더했나</b>\"로 외운다: TextView(표시) → +체크 표시 = CheckedTextView, +편집 = EditText, +누름 = Button → +두 상태 = CompoundButton(추상) → 체크박스·라디오·토글. 이 장의 위젯은 모두 4장 문제 6의 widget(View의 subclass)이다.</p>"),
 dict(q="TextView 계열 위젯에 대한 설명으로 옳지 <b>않은</b> 것을 모두 고르시오.",
      opts=[("TextView는 텍스트를 표시하는 기본 기능을 가지며, 속성을 추가하면 텍스트를 편집할 수 있다.", True, "TextView는 텍스트 표시가 기본 기능이고, 편집 속성을 더하면 편집도 할 수 있다(편집을 기본으로 바꾼 클래스가 EditText)."),
            ("TextView는 자식 위젯에 공통 기능을 제공한다.", True, "TextView는 CheckedTextView·EditText·Button 같은 자식 위젯에 텍스트 관련 공통 기능을 물려준다."),
            ("Button은 TextView에 여러 속성을 추가해 출력용으로 주로 쓴다.", False, "Button은 출력보다 <b>입력</b>을 위해 주로 쓰고, TextView에 <b>추가 속성이 없는</b> 거의 동일한 클래스다."),
            ("CompoundButton은 추상 클래스로, 선택(체크)/비선택(언체크) 두 가지 상태를 추가한 것이다.", True, "CompoundButton은 Button에 선택/비선택 두 상태를 더한 추상 클래스이고, CheckBox·RadioButton·ToggleButton이 이를 상속한다."),
            ("\"텍스트뷰\"라고 하면 XML element나 자바 클래스로서의 TextView와 그 서브클래스 전체를 통틀어 가리킨다.", True, "\"텍스트뷰\"라는 말은 TextView 하나만이 아니라 XML element·자바 클래스로서의 TextView와 그 서브클래스 전체를 가리킨다.")],
      a="ⓒ",
      why="<p>\"추상 클래스\"를 묻는 단답형 후보: CompoundButton(이 문제)과 AbsSeekBar(문제 10). 두 추상 클래스 모두 직접 쓰지 않고 자식 클래스가 쓰는 공통 틀이다.</p>")],
fig=slide("ppa5", 2, 85),
quote=quote("버튼 클래스는 텍스트뷰에 추가 속성이 없는 거의 동일한 클래스이고, CompoundButton 클래스는 추상 클래스로 선택(체크)/비선택(언체크)의 두 가지 상태를 추가한 것이다.", s(2, 3, 10))))

# 2
ta_q, ta_a = fill(["XML 속성", "뜻", "Compose"], [
    ["android:text / textColor / textSize", "문자열·글자색·글자 크기", ("?", "Text(text = \"문자열\"), color(Color.Red, Color(0xFF0000FF) 등), fontSize")],
    ["android:typeface", ("?", "글꼴의 유형(sans-serif, serif …)"), "(원문에 대응 없음)"],
    ["android:textStyle", ("?", "굵게(bold) 또는 기울임(italic)"), "(원문에 대응 없음)"],
    ["android:textAppearance", "여러 스타일을 모은 테마 스타일을 한 번에", ("?", "style 파라미터(TextStyle 또는 MaterialTheme.typography.bodyLarge 등)")],
    ["android:letterSpacing", "글자 간격", ("?", "letterSpacing 파라미터")],
    ["android:lineSpacingExtra / Multiplier", "줄 간격(추가 픽셀·배수)", ("?", "lineHeight 파라미터 하나로 통합 대체")],
    ["android:autoLink", "URL·전화번호를 자동 링크로", ("?", "기본 Text에는 대응 없음 → ClickableText 또는 AnnotatedString + UriHandler 조합")],
    ["android:singleLine", "무조건 한 줄", ("?", "maxLines = 1")],
    ["android:ellipsize", "넘치는 텍스트를 말줄임표로", ("?", "보통 maxLines와 함께 overflow = TextOverflow.Ellipsis")],
    ["android:drawableTop/Bottom/Left/Right", "텍스트 상하좌우에 이미지", ("?", "Text 단독으로는 불가 → Row나 Column 안에 Icon과 Text를 나란히")]])
P(dict(kind=["table"], title="TextView 속성 → Compose",
parts=[
 dict(q="TextView의 XML 속성에 대응하는 Compose 표현을 채우시오." + ta_q, a=ta_a,
      why="<ol><li>\"Compose에서 <b>단독 대응이 없는</b> TextView 속성\"이 객관식 단골: autoLink(기본 Text에 없음), drawableTop(Text 단독 불가). Compose가 <b>작은 함수를 조합</b>하는 방식이라 이미지+글자는 Row/Column으로 조합한다(2장 문제 24의 아이콘+글자 Column이 그 예).</li>"
          "<li>줄 간격 두 속성(lineSpacingExtra, lineSpacingMultiplier)은 Compose에서 lineHeight <b>하나로</b> 합쳐지고, singleLine은 maxLines = 1이라는 \"최대 줄 수\" 개념이 된다.</li></ol>")],
quote=quote("android:drawableTop/drawableBottom/drawableLeft/drawableRight: 텍스트의 상하 좌우에 이미지 (Drawable) 을 배치하는 기능으로, Compose 에서는 Text 단독으로는 불가하며, Row 나 Column 안에 Icon 과 Text 를 나란히 배치하여 구현합니다.", s(3, 4, 5))
 + "<p><span class='fix'>원본 s4 \"letterSapcing\" → letterSpacing, \"킹크\" → 링크</span></p>"))

# 3
P(dict(kind=["diag", "name"], title="체크 계열 위젯: CheckedTextView · CheckBox · RadioButton · ToggleButton",
parts=[
 dict(q="체크 계열 위젯(CheckedTextView, CheckBox, ToggleButton)에서 실행 중에 체크 상태를 확인하는 메서드, 바꾸는 메서드, 단순히 on/off를 뒤집는 메서드는?",
      a="확인: isChecked() / 바꾸기: setChecked(boolean) / 뒤집기: toggle()",
      why="<p>체크 계열 세 메서드는 이름이 역할이다: <b>is</b> = 묻기, <b>set</b> = 정하기, <b>toggle</b> = 뒤집기.</p>"),
 dict(q="CheckedTextView에 대해: ⓐ android:checked의 기본값과 true일 때의 상태, Compose에서의 처리 ⓑ 체크 표시 이미지를 바꾸는 XML 속성과 Compose에서의 방법 2가지",
      a="ⓐ CheckedTextView의 android:checked 기본값은 false(해제된 상태)이고, true면 체크된 상태로 시작한다. Compose에서는 checked 파라미터와 상태를 연동한다. ⓑ CheckedTextView의 체크 표시 이미지는 android:checkMark로 바꾼다. Compose에서는 Icon 컴포저블을 직접 조합하거나, 커스텀 디자인이면 CheckboxDefaults.colors() 파라미터로 색을 바꾼다."),
 dict(q="RadioButton으로 여러 옵션 중 하나만 고르게 하려면 어떻게 묶나? 하나를 고르면 나머지 RadioButton은? CheckBox와 비교한 RadioButton의 추가 속성은? on/off 두 상태에 따라 서로 다른 텍스트와 지시자(indicator)를 보여 주는 위젯은?",
      a="RadioButton들을 라디오 그룹으로 묶어 가로 또는 세로로 배치한다. 하나를 고르면 그룹 안의 나머지 RadioButton은 자동으로 선택 해제된다. RadioButton의 추가 속성은 없다(기본 사용법은 CheckBox와 동일). on/off에 따라 다른 텍스트와 지시자를 보여 주는 위젯은 <b>ToggleButton</b>.",
      why="<p>RadioButton의 \"하나만 선택\"은 XML에서는 라디오 그룹이 보장한다. Compose에서는 그룹 없이 <code>selected = (selectedUnit == …)</code> 비교로 같은 효과를 낸다(문제 7).</p>")],
quote=quote("라디오버튼은 여러 옵션 중 하나만을 선택할 때 사용한다. 보통 라디오 그룹내로 묶어서 활용하며, 그룹 내에서 가로 또는 세로 방향으로 배치할 수 있다.", s(6, 10, 11))
 + "<p><span class='fix'>원본 s11 \"지시자(instructor)\" → indicator로 보임</span></p>"))

# 4
et_q, et_a = fill(["EditText XML 속성", "뜻", "Compose 방법"], [
    ["hint", "입력창이 비었을 때 대신 표시할 글자", ("?", "TextField·OutlinedTextField의 placeholder")],
    ["ems", "입력창의 폭(ems=10이면 글자 10개의 폭)", ("?", "Modifier.width()로 고정 크기, 또는 TextStyle 설정")],
    ["lines", "입력창의 높이를 줄 수로", ("?", "minLines와 maxLines를 같게")],
    ["maxLength", "입력할 수 있는 최대 글자 수", ("?", "onValueChange에서 글자 수를 체크해 넘지 않을 때만 상태 업데이트")],
    ["selectAllOnFocus", "포커스를 받으면 전체 선택", ("?", "TextFieldValue 상태 + Modifier.onFocusChanged로 감지해 전체 범위 TextRange 선택")],
    ["digits", "지정한 문자만 입력 가능(digits=\"12345\"면 1~5만)", ("?", "onValueChange에서 허용된 글자만 남기도록 filtering")]])
P(dict(kind=["table", "diag"], title="EditText 속성 → Compose",
parts=[
 dict(q="EditText는 TextView의 무엇을 바꾼 위젯인가?",
      a="EditText는 텍스트를 편집할 수 있도록 TextView의 기본 속성을 변경한 위젯이다."),
 dict(q="EditText의 XML 속성에 대응하는 Compose 방법을 채우시오." + et_q, a=et_a,
      why="<p>Compose의 입력 제한 원리는 하나: <b>onValueChange에서 걸러서 상태를 업데이트</b>한다. maxLength·digits 둘 다 같은 방법이다. Compose는 화면이 상태를 그대로 그리므로, 상태에 넣지 않은 글자는 화면에도 나타나지 않는다.</p>"),
 dict(q="EditText의 입력 형식(android:inputType)을 Compose로 옮길 때 쓰는 두 파라미터 이름은? ⓐ 일반 텍스트 ⓑ 숫자·전화번호 ⓒ 이메일 ⓓ 비밀번호 각각의 Compose 설정은?",
      a="keyboardOptions, visualTransformation. ⓐ 일반 텍스트: TextField(value = text, …) ⓑ 숫자·전화번호: KeyboardOptions(keyboardType = KeyboardType.Phone) 등 → 숫자 키보드 ⓒ 이메일: keyboardType = KeyboardType.Email ⓓ 비밀번호: 키보드 종류 지정 + 글자를 숨기는 <b>PasswordVisualTransformation()</b>을 함께",
      why="<p>입력 형식 중 비밀번호만 Compose 파라미터가 <b>두 개</b>다: 키보드 종류(keyboardOptions) + 화면에서 글자 숨기기(visualTransformation).</p>")],
quote=quote("android:inputType='textPassword' 면, Compose 에서는 키보드 종류를 지정하는 것 외에 글자를 숨겨주는 PasswordVisualTransformation()을 함께 넣어 주어야 합니다.", s(7, 8, 9))
 + "<p><span class='fix'>원본 s8 \"selectOnAllFocus\" → selectAllOnFocus</span></p>"))

# 5
P(dict(kind=["name", "diag"], title="온도 변환기 ViewModel의 Kotlin 문법",
intro="<code>class TemperatureViewModel : ViewModel() { companion object { private const val FREEZING_C = 0.0; private const val BOILING_C = 100.0 }; enum class TemperatureUnit { CELSIUS, FAHRENHEIT } … }</code>",
parts=[
 dict(q="TemperatureViewModel의 companion object 블록에 담기는 값의 성격은? enum class TemperatureUnit을 쓰면 컴파일러가 무엇을 강제하나? selectedUnit에 \"KELVIN\" 같은 값을 넣을 수 있나?",
      a="companion object에 담긴 값은 인스턴스마다 존재하지 않고 <b>클래스 자체에 단 하나</b> 존재한다. enum class는 가능한 값의 종류가 미리 정해진 유한 집합이라, 컴파일러가 TemperatureUnit 타입 변수가 지정된 값(CELSIUS, FAHRENHEIT) 외에는 가질 수 없도록 <b>타입 차원에서</b> 강제한다. 그래서 selectedUnit에 KELVIN은 넣을 수 없다(컴파일 오류).",
      why="<p>enum은 \"보기가 정해진 객관식 변수\"다. 단위를 문자열(\"C\"/\"F\")로 들고 있으면 오타가 실행 중에야 드러나지만, enum이면 컴파일러가 막는다.</p>"),
 dict(q="Kotlin의 val과 const val의 제약 차이는? FREEZING_C를 const val로 둔 이유는?",
      a="val은 런타임에 한 번 초기화되면 재할당할 수 없다. const val은 <b>컴파일 시점에 이미 값이 확정</b>되어야 하는 더 강한 제약이다. FREEZING_C(0)와 BOILING_C(100)는 실행 전부터 정해진 상수라서 const val로 둔다.",
      why="<p>Kotlin 세 키워드의 \"값이 언제 정해지나\": <b>const val = 컴파일 때</b>, val = 실행 중 한 번, var = 언제든. 1장 문제 21의 BuildConfig.DEBUG(컴파일 시점에 값이 확정되는 상수)와 같은 개념.</p>"),
 dict(q="TemperatureViewModel은 configuration change가 일어날 때 어떻게 되나? 상태 3개 temperatureInput, selectedUnit, isValidInput의 초기값은? 세 상태를 만든 mutableStateOf가 하는 일은? 세 상태가 모두 private set인 이유는? 라디오 버튼의 onClick에 연결되는 함수와 그 함수가 하는 일은?",
      a="TemperatureViewModel은 configuration change 때 인스턴스가 재생성되지 않고 유지되도록 생명주기가 관리된다. 초기값: temperatureInput = \"\", selectedUnit = TemperatureUnit.CELSIUS, isValidInput = true. mutableStateOf는 Compose가 감시하는 상태 홀더를 만든다. private set이라 세 상태의 읽기는 클래스 밖에서 가능하고, 쓰기(재할당)는 클래스 내부로 제한된다. 라디오 버튼의 onClick은 <code>onUnitSelected(unit: TemperatureUnit)</code>을 부르고, 이 함수는 받은 단위 값을 selectedUnit에 그대로 대입한다.",
      why="<p>isValidInput 초기값이 true인 이유(빈 입력을 유효로 취급해 처음부터 빨간 오류가 뜨지 않게)는 4장 문제 17에서 다뤘다.</p>")],
quote=quote("enum class 는 가능한 값의 종류가 미리 정해진 유한한 집합으로 enum 을 적용하면, 컴파일러가 클래스 타입의 변수를 지정된 깂 이외에는 가질 수 없도록 타입 차원에서 강제합니다.", s(12, 13, 14))))

# 6
cv_q, cv_a = fill(["선택 단위, 입력", "결과 글자", "배경색"], [
    ["섭씨, 10", ("?", "50.0°F"), ("?", "노랑(섭씨 10은 0~100 사이)")], ["섭씨, 100", ("?", "212.0°F"), ("?", "분홍(섭씨 100 ≥ 100)")],
    ["화씨, 10", ("?", "-12.2°C"), ("?", "하늘색(섭씨 −12.2 ≤ 0)")], ["화씨, 212", ("?", "100.0°C"), ("?", "분홍(섭씨 100)")],
    ["화씨, 32", ("?", "0.0°C"), ("?", "하늘색(섭씨 0 ≤ 0)")], ["섭씨, 빈 입력", ("?", "값을 입력하세요"), ("?", "LightGray")]])
P(dict(kind=["calc", "diag"], title="섭씨·화씨 두 단위: celsiusValue와 convertedValue",
intro="규칙: celsiusValue(private) = 입력을 숫자로 바꿔, 섭씨 선택이면 그대로, 화씨 선택이면 (v − 32) × 5/9 → <b>섭씨로 통일</b>. convertedValue(공개) = 섭씨 선택이면 v × 9/5 + 32, 화씨 선택이면 (v − 32) × 5/9 → <b>반대 단위</b>. 배경색은 celsiusValue 기준(≤ 0 하늘색, ≥ 100 분홍, 사이 노랑, 숫자 아님 LightGray). 결과 글자 = convertedValue가 있으면 \"%.1f%s\"(숫자 + 반대 단위 기호), 없으면 \"값을 입력하세요\". 반대 단위 기호 resultUnitLabel = 섭씨 선택이면 \"°F\", 아니면 \"°C\".",
parts=[
 dict(q="두 단위 온도 변환기에서 결과 글자와 배경색을 쓰시오." + cv_q, a=cv_a,
      why="<p>계산: 10 × 9/5 + 32 = 50 / (10 − 32) × 5/9 = −22 × 0.555… = −12.2 / (212 − 32) × 5/9 = 100 / (32 − 32) × 5/9 = 0.</p>"),
 dict(q="온도 변환기 배경색을 celsiusValue가 아니라 convertedValue로 판정하면 어떤 문제가 생기나? celsiusValue를 둔 목적은?",
      a="convertedValue는 선택 단위의 <b>반대</b> 단위 값이라, 섭씨를 고르면 화씨 값이 된다 → 판정 기준(0, 100)이 단위마다 달라진다(예: 섭씨 50 입력 → convertedValue 122 → \"≥ 100\"으로 분홍 오판). celsiusValue는 입력 단위와 상관없이 <b>섭씨로 통일한 판정 기준</b>(내부 기준)이다.",
      why="<p>온도 변환기는 \"내부 판정용 하나(celsiusValue, private) + 화면 표시용 하나(convertedValue, 공개)\"로 나눈 설계다. 배경색·온도계(문제 13)·슬라이더(문제 14)는 모두 <b>celsiusValue</b>를 쓰므로, 단위가 바뀌어도 판정 로직은 한 벌이다.</p>"),
 dict(q="celsiusValue와 convertedValue가 둘 다 Double?인 이유는? 두 속성에 backing field가 있나? <code>toDoubleOrNull()?.let</code>의 ?가 하는 일은?",
      a="입력이 숫자로 변환되지 않으면 null이어야 하므로 Double?이다. backing field는 없다 — 두 속성 모두 backing field 없는 custom getter라 접근할 때마다 재계산된다. ?.는 안전 호출로, toDoubleOrNull()의 결과가 null이면 let을 실행하지 않고 null을 반환한다.",
      why="<p>4장 문제 16(?. 와 ?:)·17(기본형 결과)과 연결된다. 배경색의 <code>celsiusValue ?: return Color.LightGray</code>도 엘비스 연산자 패턴이다.</p>"),
 dict(q="결과 글자의 <code>\"%.1f%s\".format(it, resultUnitLabel)</code>에서 %.1f와 %s는 각각 무엇을 하나? resultUnitLabel은 어떤 변수이고 <code>: String</code>은 무엇인가?",
      a="%.1f는 첫 번째 인자(변환된 숫자 it)를 소수 첫째 자리까지, %s는 두 번째 인자(resultUnitLabel)를 문자열 그대로 넣는다. resultUnitLabel은 TemperatureScreen 함수 안에서만 사는 지역 변수로, if~else 식으로 반대 단위 기호를 계산한다. <code>: String</code>은 resultUnitLabel의 타입 명시다.")],
fig=slide("ppa5", 24, 90),
quote=quote("celsiusValue 가 판정 기준을 통일하기 위한 내부 기준이라면, convertedValue 는 화면에 실제로 보여줄 반대의 단위값입니다.", s(15, 16, 17, 23, 24))
 + "<p><span class='fix'>원본 s16 \"celsiusValue와 convertedValue는 private 파생 속성\" — 코드상 convertedValue는 private이 아님(같은 슬라이드 끝에서 직접 접근 가능하다고 함). s17 \"celsivusValue\" → celsiusValue</span></p>"))

# 7
P(dict(kind=["diag", "name"], title="라디오 버튼 줄과 Column 화면 구성",
intro="<code>Row(verticalAlignment = Alignment.CenterVertically) { RadioButton(selected = viewModel.selectedUnit == CELSIUS, onClick = { viewModel.onUnitSelected(CELSIUS) }); Text(\"섭씨 (°C)\"); Spacer(Modifier.width(16.dp)); RadioButton(selected = … == FAHRENHEIT, onClick = { … }); Text(\"화씨 (°F)\") }</code>",
parts=[
 dict(q="온도 변환기의 두 RadioButton이 RadioGroup 없이도 배타적으로 동작하는 이유는?",
      a="각 RadioButton의 selected는 매번 selectedUnit과 <b>비교한 결과</b>(Boolean)인데, 두 버튼의 비교 대상이 서로 다른 TemperatureUnit 값이라 한 버튼이 true면 다른 버튼은 자동으로 false가 된다.",
      why="<p>선언형(2장 문제 8)의 전형이다. \"선택된 버튼을 끄라\"고 <b>명령하지 않고</b> \"selectedUnit과 같으면 선택됨\"이라고 <b>선언</b>만 해 두면, selectedUnit이 바뀔 때 리컴포지션으로 두 RadioButton이 함께 다시 그려진다.</p>"),
 dict(q="라디오 버튼 Row에 verticalAlignment = Alignment.CenterVertically를 준 이유는? Spacer는 무엇이며, 가로 간격과 세로 간격에는 각각 어떤 Modifier를 쓰나?",
      a="가로로 놓인 원형 RadioButton과 Text의 높이가 달라서, 세로 중앙선을 기준으로 정렬하려고. Spacer는 지정된 크기만큼 빈 공간을 차지하는 컴포저블이다. 가로 간격은 Modifier.width(16.dp), 세로 간격은 Modifier.height(16.dp).",
      why="<p>Row는 verticalAlignment, Column은 horizontalAlignment — 쌓는 방향과 <b>수직인</b> 방향으로 정렬한다.</p>"),
 dict(q="온도 변환기 화면 전체를 감싸는 Column에 <code>.padding(padding).padding(16.dp).fillMaxWidth().background(viewModel.backgroundColor)</code>를 줬다. 두 padding은 각각 무엇인가? fillMaxWidth 대신 fillMaxSize를 쓰면? 입력창 label이 단위에 따라 \"섭씨 온도 입력\"/\"화씨 온도 입력\"으로 바뀌게 하는 방법은?",
      a="첫 번째 padding(padding)은 Scaffold가 준 padding(TopAppBar에 가려지지 않게), 두 번째 padding(16.dp)은 추가 여백 16dp다. fillMaxSize면 Column이 가로뿐 아니라 화면 전체 <b>높이까지</b> 채운다. label은 <code>label = { Text(if (viewModel.selectedUnit == CELSIUS) \"섭씨 온도 입력\" else \"화씨 온도 입력\") }</code>처럼 if를 식으로 쓴다.")],
quote=quote("두번째 RadioButton()은 첫번째 RadioButton 과 완전히 동일한 구조입니다. 단, 비교 대상으로 앞쪽과는 다른 TemperatureUnit 값을 비교하기 때문에 하나가 선택되면, 다른 하나는 자동으로 selected=false 가 되어 배타적으로 동작하는 것 처럼 여겨집니다.", s(18, 19, 20, 21))))

# 8
P(dict(kind=["name", "diag"], title="함수 참조 ::와 입력창 색",
intro="<code>OutlinedTextField(value = viewModel.temperatureInput, onValueChange = viewModel::onTemperatureChanged, isError = !viewModel.isValidInput, singleLine = true, colors = OutlinedTextFieldDefaults.colors(focusedContainerColor = Color.White, unfocusedContainerColor = Color.White))</code>",
parts=[
 dict(q="Kotlin의 <code>::</code>는 무엇을 만드는 연산자인가? <code>onValueChange = viewModel::onTemperatureChanged</code>를 람다로 쓰면?",
      a="<code>::</code>는 함수 참조(function reference)를 만든다 — viewModel이 가진 onTemperatureChanged라는 <b>함수 자체를 값으로</b> 참조한다. 람다로 쓰면 <code>onValueChange = { newInput -&gt; viewModel.onTemperatureChanged(newInput) }</code>."),
 dict(q="<code>viewModel::onTemperatureChanged</code>라고 쓴 순간 onTemperatureChanged가 실행되나? 실제 호출은 언제, 누가 하나?",
      a="실행되지 않는다. ::는 함수를 호출하지 않고, 나중에 호출할 수 있는 참조만 만들어 넘긴다. 실제 호출은 OutlinedTextField 내부에서 <b>사용자가 입력값을 넣을 때</b> 일어난다.",
      why="<p>함수 참조 ::와 람다는 둘 다 \"<b>나중에 실행할 함수</b>\"를 값으로 넘긴다(2장 문제 9 람다의 정의와 같음). 차이는 ::가 이미 있는 함수 이름을 그대로 가리키고, 람다는 그 자리에서 이름 없는 함수를 새로 만든다는 것. 4장 과학적 표기법의 <code>viewModel::onNumberInputChange</code>, 이 장 Slider의 <code>viewModel::onSliderChanged</code>도 같은 문법이다.</p>"),
 dict(q="OutlinedTextField의 focusedContainerColor와 unfocusedContainerColor는 각각 어떤 상태의 색인가? 이 코드의 의도는? isError에 !를 붙인 이유는?",
      a="focusedContainerColor는 사용자가 입력창을 탭해 커서가 깜빡이고 키보드가 이 입력창을 향해 열려 있는 상태의 배경색, unfocusedContainerColor는 다른 곳을 탭해 포커스가 해제된 상태의 배경색이다. 두 상태 모두 흰색으로 고정해 온도별 배경색 위에서 입력창이 잘 보이게 했다. isValidInput은 \"유효한가\"이고 isError는 \"오류인가\"라서 뜻이 반대이므로 !로 뒤집는다.")],
quote=quote(":: 을 사용하면, 함수를 호출하지 않고, 함수를 나중에 호출하고 싶을 때 쓸 수 있는 참조만 만들어서 넘깁니다. 실제 호출은 OutlinedTextField 내부에서 사용자가 입력값을 넣을 때 발생합니다.", s(21, 22))))

# 9
im_q, im_a = fill(["ImageView XML 속성", "뜻", "Compose"], [
    ["src", "보여 줄 이미지 리소스(Drawable)", ("?", "painter(Resource)로 전달(painterResource)")],
    ["scaleType", "이미지를 뷰 크기에 맞추는 방식", ("?", "Image의 contentScale에 ContentScale 객체")],
    ["adjustViewBounds", "원래 종횡비를 유지하며 뷰 크기 조절", ("?", "Modifier.aspectRatio() 또는 ContentScale.Fit")],
    ["maxWidth / maxHeight", "뷰가 가질 수 있는 최대 가로/세로", ("?", "Modifier.widthIn(min, max), sizeIn(…)")],
    ["cropToPadding", "내부 padding 안쪽으로 잘라낼지(기본 false, true면 패딩 경계에 맞춰 잘림)", ("?", "Modifier로 자르기(Clip)·도형 지정, Canvas는 Modifier.cropToPadding()(원문 표기)")]])
P(dict(kind=["table", "name"], title="ImageView · ImageButton과 Compose",
parts=[
 dict(q="View → ImageView → ImageButton 계층에서 ImageView 클래스와 ImageButton 클래스는 각각 무엇을 모은/더한 것인가? ImageButton의 추가 속성은? ImageButton에 출력할 대상은 어떻게 지정하나?",
      a="ImageView 클래스는 이미지 출력에 필요한 공통 속성·기능을 모은 것이고, ImageButton 클래스는 이미지가 버튼처럼 동작하는 기능(누르고 떼는 효과)을 추가한 것이다. ImageButton의 추가 속성은 없고, 출력 대상은 ImageView처럼 src 속성으로 지정한다.",
      why="<p>ImageButton : ImageView = Button : TextView. \"보여 주는 것\"에 \"누르는 것\"을 더한 같은 구조다(문제 1).</p>"),
 dict(q="ImageView가 출력할 수 있는 것 4가지는? 그중 \"파일이 아닌 메모리에 존재하는 것\"과 \"안드로이드에서 화면에 그릴 수 있는 것을 대표하는 클래스\"는?",
      a="리소스, 로컬 파일, Bitmap, Drawable. 메모리에 존재하는 비트맵 = <b>Bitmap</b>, 화면에 그릴 수 있는 것을 대표하는 클래스 = <b>Drawable</b>."),
 dict(q="ImageView의 XML 속성에 대응하는 Compose 표현을 채우시오." + im_q, a=im_a,
      why="<p>contentScale의 대표 값 Fit/Crop 차이는 6장 강아지 배경 문제에서 다룬다.</p>")],
fig=slide("ppa5", 25, 80),
quote=quote("이미지뷰는 리소스, 로컬파일, Bitmap (파일이 아닌 메모리에 존재하는 비트맵), 안드로이드에서 화면에 그릴 수 있는 것을 대표하는 클래스인 Drawable 을 출력할 수 있는 다양한 클래스이다.", s(25, 26, 27))
 + "<p><span class='fix'>원본 s26 \"ViewModel 에서 레이아웃의 속성\" → 문맥상 View(레이아웃 XML)로 보임</span></p>"))

# 10
pb_q, pb_a = fill(["클래스", "계층 위치", "한 줄 정의", "용도"], [
    ["ProgressBar", "View의 자식", ("?", "작업의 진행 상태만 표시"), ("?", "출력용")],
    ["AbsSeekBar", "ProgressBar의 자식(추상 클래스)", ("?", "사용자가 끌어 놓는 방식을 추가한 ProgressBar"), "—"],
    ["RatingBar", "AbsSeekBar의 자식", ("?", "별 개수로 점수를 표시하거나 입력"), ("?", "입력용")],
    ["SeekBar", "AbsSeekBar의 자식", ("?", "thumb을 좌우로 끌어 값을 선택"), ("?", "입력용")]])
P(dict(kind=["table", "mc"], title="ProgressBar 계열: 계층과 모드",
parts=[
 dict(q="ProgressBar 계열 클래스의 정의와 용도(출력용/입력용)를 채우시오." + pb_q, a=pb_a,
      why="<p>ProgressBar 계열의 입력용·출력용 판정: 사용자가 <b>끌 수 있으면</b>(AbsSeekBar의 자식) 입력용이다. 그래서 AbsSeekBar(Abs = abstract)가 출력용 ProgressBar와 입력용 RatingBar·SeekBar 사이에 끼어 있다.</p>"),
 dict(q="ProgressBar의 XML 속성 android:max/progress, secondaryProgress, indeterminate의 뜻은? indeterminate가 true면?",
      a="android:max/progress = 최대 진행 값과 현재 진행 값 / secondaryProgress = 주 진행 바 뒤에 표시되는 보조 진행 값 / indeterminate = 진행 상황을 알 수 없을 때 바가 계속 움직이는 애니메이션. indeterminate가 true면 불확정 모드다."),
 dict(q="ProgressBar와 Compose 진행 표시에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("프로그레스 바는 진행 상황을 회전 바퀴나 수평 막대로 보여 준다.", True, "ProgressBar는 진행 상황을 회전 바퀴(원형) 또는 수평 막대로 보여 준다."),
            ("불확정 모드에서는 진행 값을 숫자로 보여 준다.", False, "ProgressBar의 불확정 모드는 진행 값을 보여 주지 않고 애니메이션만 보여 준다."),
            ("수평 막대는 확정 모드에서 최대 두 개의 진행값(기본 진행값, 2차 진행값)을 보여 줄 수 있다.", True, "수평 막대 ProgressBar는 확정 모드에서 progress(기본)와 secondaryProgress(2차) 두 값을 함께 보여 줄 수 있다."),
            ("Compose에서 progress의 최댓값은 항상 1.0f 비율로 계산한다.", True, "Compose의 진행 표시는 max 속성 없이 progress를 0f~1.0f 비율로 받는다."),
            ("Compose의 LinearProgressIndicator는 두 진행 바를 동시에 지원하므로 secondaryProgress를 그대로 쓴다.", False, "Compose의 LinearProgressIndicator는 두 진행 바를 동시에 지원하지 않아, Box()로 두 바를 겹쳐 구현한다."),
            ("Compose에서 progress 매개변수를 넣지 않은 LinearProgressIndicator()는 무한 반복 애니메이션이 된다.", True, "Compose의 LinearProgressIndicator는 progress를 주지 않으면 불확정 모드, 즉 무한 반복 애니메이션이 된다.")],
      a="ⓐ ⓒ ⓓ ⓕ",
      why="<p>Compose에서 확정/불확정은 <b>progress를 주느냐 마느냐</b>로 갈린다. 진행 값을 모르면 안 준다 → 무한 애니메이션.</p>")],
fig=slide("ppa5", 28, 80),
quote=quote("ProgressBar 클래스에서 주로 출력용으로 사용되며, 추상 클래스인 AbsSeekBar 에서 파생된 RatingBar 와 SeekBar 클래스는 주로 입력용으로 사용됩니다.", s(28, 29, 30))))

# 11
rb_q, rb_a = fill(["RatingBar XML 속성", "뜻", "Compose"], [
    ["numStars", "화면에 표시할 별의 총 개수", ("?", "Row 안에 반복문으로 별 Icon을 원하는 개수만큼 가로 정렬")],
    ["rating", "기본 평점(채워질 별 개수)", ("?", "반복할 때마다 현재 별 위치와 평점을 비교해 채워진 별을 그릴지 결정")],
    ["stepSize", "별점이 변경되는 최소 단위", ("?", "Slider의 steps 파라미터")],
    ["isIndicator", "터치·드래그로 수정 가능 여부(true = 읽기 전용)", ("?", "Icon의 Modifier.clickable 활성화 여부")]])
P(dict(kind=["table", "diag"], title="RatingBar를 Compose로",
parts=[
 dict(q="Material 라이브러리에 RatingBar 컴포저블이 있나? RatingBar의 XML 속성에 대응하는 Compose 방법을 채우시오." + rb_q,
      a="Material 라이브러리에 RatingBar 컴포저블은 없다 → Row + 반복문 + 별 Icon으로 그린다." + rb_a),
 dict(q="RatingBar의 isIndicator = true인 별점에서 별을 누르면? false면? 이를 한 줄의 Modifier로 쓰면?",
      a="isIndicator = true면 읽기 전용이라 별을 눌러도 아무 반응이 없다. false면 별을 누를 때마다 onRatingChanged 콜백이 실행되어 별점이 바뀐다. <code>Modifier.clickable(enabled = !isIndicator)</code>",
      why="<p>isIndicator(표시 전용인가?)와 enabled(누를 수 있나?)는 <b>뜻이 반대</b>라 !로 뒤집는다. 문제 8의 <code>isError = !isValidInput</code>과 같은 패턴이고, 4장 문제 7의 enabled(보이지만 조작 불가)와도 연결된다.</p>")],
quote=quote("isindicator 가 true 이면 반대값인 enabled = false 가 되어, 별을 눌러도 아무 반응이 없고, 값이 false 이면, 별을 누를 때 마다 onRatingChanged 콜백 함수가 실행되어 별점이 새로 바뀝니다.", s(30, 31))))

# 12
sb_q, sb_a = fill(["SeekBar 메서드", "호출 시점", "Compose Slider 대응"], [
    ["onStartTrackingTouch(seekBar)", ("?", "터치로 thumb을 끌기 시작할 때"), ("?", "별도 파라미터 없음(onValueChangeFinished가 호출되기 전, 사용자가 처음 드래그하는 시점)")],
    ["onProgressChanged(seekBar, progress, fromUser)", ("?", "thumb 위치가 바뀔 때, 현 위치 = progress"), ("?", "onValueChange(조절할 때마다 변경된 값)")],
    ["onStopTrackingTouch(seekBar)", ("?", "손을 떼어 끌기를 멈출 때"), ("?", "onValueChangeFinished")]])
P(dict(kind=["table", "order"], title="SeekBar의 콜백과 Compose Slider",
parts=[
 dict(q="SeekBar는 무엇의 일종이며, 무엇과 모양·동작이 비슷한가? SeekBar의 thumb을 조작하면 발생하는 이벤트를 처리하는 인터페이스는?",
      a="SeekBar는 프로그레스 바의 일종으로, 사용자가 thumb으로 진행값을 조작한다. 윈도우 운영체제의 Scroll 바와 비슷하다. 이벤트 처리 인터페이스는 <b>SeekBar.OnSeekBarChangeListener</b>."),
 dict(q="SeekBar.OnSeekBarChangeListener의 세 추상 메서드의 호출 시점과 Compose Slider 대응을 채우시오." + sb_q, a=sb_a,
      why="<p>Compose Slider는 \"시작\" 전용 콜백 없이 <b>값이 바뀔 때(onValueChange)</b>와 <b>끝날 때(onValueChangeFinished)</b> 두 개로 줄였다.</p>"),
 dict(q="SeekBar의 onProgressChanged에서 fromUser가 false인 경우는? 사용자가 thumb을 잡고 끌다가 놓을 때 세 메서드가 불리는 순서는?",
      a="fromUser가 false인 경우는 사용자가 아니라 (java) 코드로 SeekBar 위치값을 바꾼 경우다. 순서: onStartTrackingTouch → onProgressChanged(여러 번) → onStopTrackingTouch",
      why="<p>SeekBar 메서드 이름이 순서를 말한다: Start → (Changed 반복) → Stop.</p>")],
quote=quote("onProgressChanged: onValueChange 파라미터에 대응됩니다. 사용자가 조절할 때마다 변경된 값이 들어옵니다. onStopTrackingTouch: onValueChangeFinished 파라미터에 대응됩니다.", s(32, 33))))

# 13
pf_q, pf_a = fill(["입력", "progressFraction", "빨간 수은주 높이(애니메이션 후, 바깥 500dp)"], [
    ["섭씨 37", ("?", "0.37"), ("?", "500 × 0.37 = 185dp")], ["섭씨 −10", ("?", "−0.1 → coerceIn으로 0"), ("?", "0dp")],
    ["섭씨 150", ("?", "1.5 → coerceIn으로 1.0"), ("?", "500dp(가득)")], ["화씨 212", ("?", "섭씨 100 → 1.0"), ("?", "500dp")],
    ["빈 입력", ("?", "celsiusValue가 null → 0f"), ("?", "0dp")]])
P(dict(kind=["calc", "diag"], title="온도계 막대(ThermometerBar)",
intro="ViewModel: <code>val progressFraction: Float get() { val c = celsiusValue ?: return 0f; val range = BOILING_C - FREEZING_C; return ((c - FREEZING_C) / range).coerceIn(0.0, 1.0).toFloat() }</code><br>ThermometerBar: 바깥 Box(폭 100dp, 높이 500dp, LightGray, RoundedCornerShape(20.dp)) 안에 안쪽 Box(align(BottomCenter), fillMaxWidth(), <b>fillMaxHeight(fraction = animatedProgress)</b>, Red, 같은 모서리). animatedProgress = animateFloatAsState(targetValue = progress, tween 500ms).",
parts=[
 dict(q="온도계 막대의 progressFraction과 수은주 높이를 구하시오." + pf_q, a=pf_a,
      why="<p>fraction = (현재 − 최저) / (최고 − 최저): 0°C를 0, 100°C를 1로 놓는 <b>비율</b>이다. 화씨로 입력해도 celsiusValue(섭씨 통일)를 쓰므로 같은 막대가 된다(문제 6).</p>"),
 dict(q="progressFraction의 coerceIn(0.0, 1.0)과 toFloat()는 각각 왜 필요한가? progressFraction의 타입이 Float인 이유는?",
      a="coerceIn(0.0, 1.0)은 범위 밖 값을 0.0~1.0으로 잘라(clamp) 수은주 막대가 넘치거나 음수가 되지 않게 한다. toFloat()는 Double로 계산된 결과를 Float로 바꾼다. 수은주의 <code>fillMaxHeight(fraction)</code>이 Float 값을 요구하므로 progressFraction도 Float다.",
      why="<p>2장 문제 17의 coerceAtLeast/AtMost가 한쪽 경계라면, coerceIn은 <b>양쪽 경계</b>를 한 번에 자른다.</p>"),
 dict(q="수은주 Box의 fillMaxHeight()에 인자가 없으면? align(Alignment.BottomCenter)가 없으면 수은주는 어디서부터 차오르나? animateFloatAsState는 2장의 무엇을 Float에 맞춘 것이며, 하는 일은?",
      a="fillMaxHeight()에 인자가 없으면 최대 100%를 채운다. align(BottomCenter)가 없으면 Box 기본 정렬(TopStart)이라 수은주가 위에서부터 채워져, 아래에서 차오르는 온도계 모양이 되지 않는다(보충 추론: 2장 문제 16 Box 기본 정렬). animateFloatAsState는 animateDpAsState를 Float에 맞춘 것으로, progress 값이 갑자기 바뀌어도 500ms 동안 부드럽게 거쳐 가며 변하게 한다."),
 dict(q="온도계 모서리를 RoundedCornerShape(20.dp)에서 50dp로 올리면 모양이 어떻게 되나? 온도계와 결과 글자를 화면 가로 중앙에 두려고 Column에 준 파라미터는? 그 파라미터가 없으면?",
      a="모서리 50dp는 온도계 전체 폭(100dp)의 반이라 반지름이 되어 캡슐 모양에 가까워진다. Column에 <code>horizontalAlignment = Alignment.CenterHorizontally</code>를 줬고, 없으면 기본값 Alignment.Start(왼쪽 정렬)가 된다.")],
fig=slide("ppa5", 35, 80),
quote=quote("range 는 전체 구간의 폭을 의미하고, .coerceIn(0.0, 1.0)은 값이 0.0보다 작거나 1.0보다 크다면, 0.0과 1.0에서 clamp 하는 기능을 합니다.", s(34, 35, 36, 37, 38, 39, 40))
 + "<p><span class='fix'>원본 s37 \"TurtleApp 에서 animatedDpAsState\" → TurtleScreen의 animateDpAsState / s40 \"아래쪽에서 padding\"이라 했지만 코드는 padding(end = 16.dp)(오른쪽 끝)</span></p>"))

# 14
sl_q, sl_a = fill(["상황", "입력창 글자", "결과 글자 / 손잡이 위치"], [
    ["섭씨 선택, 슬라이더를 44.9로", ("?", "\"44.9\""), ("?", "결과 112.8°F(44.9 × 1.8 + 32 = 112.82)")],
    ["화씨 선택, 슬라이더를 100으로", ("?", "\"212.0\"(슬라이더 값은 섭씨 100 → 화씨로 표시)"), ("?", "결과는 반대 단위 100.0°C")],
    ["섭씨 선택, 입력창에 200", "\"200\"", ("?", "손잡이: celsiusValue 200 → coerceIn으로 120(오른쪽 끝)")],
    ["입력창에 \"abc\"", "\"abc\"", ("?", "손잡이: celsiusValue null → 0f")]])
P(dict(kind=["calc", "order", "diag"], title="Slider로 온도 입력하기",
intro="<code>companion object { …; const val SLIDER_MIN_C = -20f; const val SLIDER_MAX_C = 120f }</code><br><code>val sliderValue: Float get() = celsiusValue?.toFloat()?.coerceIn(SLIDER_MIN_C, SLIDER_MAX_C) ?: 0f</code><br><code>fun onSliderChanged(newCelsiusValue: Float) { val displayValue = when (selectedUnit) { CELSIUS -&gt; newCelsiusValue; FAHRENHEIT -&gt; newCelsiusValue * 9f / 5f + 32f }; temperatureInput = \"%.1f\".format(displayValue); isValidInput = true }</code><br>UI: <code>Slider(value = viewModel.sliderValue, onValueChange = viewModel::onSliderChanged, valueRange = -20f..120f, modifier = Modifier.fillMaxWidth())</code>",
parts=[
 dict(q="슬라이더 상수 SLIDER_MIN_C·SLIDER_MAX_C에 private을 붙이지 않은 이유는? FREEZING_C·BOILING_C와 비교하면?",
      a="슬라이더 최솟값·최댓값은 Composable(Slider의 valueRange)에서도 쓰므로, 두 곳을 동시에 수정해야 하는 것을 잊는 실수를 줄이려고 private을 해제했다. FREEZING_C·BOILING_C는 ViewModel 안에서만 쓰므로 private이다."),
 dict(q="온도 변환기 Slider를 조작하거나 입력창에 쓸 때 결과를 채우시오." + sl_q, a=sl_a,
      why="<p>슬라이더 범위(−20~120)와 온도계 범위(0~100)가 다르다는 점이 숫자 함정이다.</p>"),
 dict(q="onSliderChanged가 isValidInput을 true로 두는 이유는? 슬라이더 값의 단위는 항상 무엇인가?",
      a="Slider에서 나온 값은 항상 유효한 숫자이므로 isValidInput을 true로 둔다. 슬라이더 값의 단위는 선택 단위와 관계없이 항상 <b>섭씨</b>이고, 화면 표시만 선택 단위로 바꾼다."),
 dict(q="사용자가 온도 변환기의 Slider를 끌었을 때의 경로를 순서대로 쓰시오(6단계, 방향 포함).",
      a="① Slider: 사용자가 drag해서 얻은 값으로 onValueChange 호출(Slider → ViewModel) ② ViewModel: onSliderChanged 실행, temperatureInput 상태 변경 ③ Compose runtime: temperatureInput을 읽고 있던 UI들에게 다시 그리라는 신호 ④ Slider 함수가 재구성되며 value를 sliderValue에서 다시 읽음 ⑤ sliderValue는 celsiusValue에서 파생되므로 방금 바뀐 temperatureInput을 반영한 새 값 반환 ⑥ Slider가 새 값으로 손잡이를 새 위치에 그림(ViewModel → Slider)",
      why="<p>Slider는 <b>값을 직접 들고 있지 않는다</b>: 손잡이 위치(value)도 ViewModel의 temperatureInput에서 파생(sliderValue)된다. 그래서 입력창에 숫자를 쳐도 손잡이가 따라 움직이고, 손잡이를 끌어도 입력창 글자가 바뀐다 — <b>진실은 temperatureInput 한 곳</b>(4장 문제 4 SSOT). 6단계가 원 모양으로 돌아오는 것이 그 증거.</p>")],
fig=slide("ppa5", 41, 80),
quote=quote("Compose runtime: temperatureInput 을 읽고 있던 UI 들에게 화면에 그리라는 신호를 합니다. Slider 함수가 호출되어 재구성되면서, 이 때 value 를 SliderValue 에서 받아 다시 읽게 됩니다.", s(41, 42, 43, 44, 45))))

KEYWORDS = [
 ("위젯 (Widget)", "버튼, 체크박스, 스크롤 바, 입력 창처럼 화면을 구성하는 작은 시각적 부품. GUI의 하위 개념", s(2)),
 ("TextView", "텍스트를 표시하는 기본 위젯. 자식 위젯에 공통 기능 제공", s(2)),
 ("CompoundButton", "Button에 선택(체크)/비선택(언체크) 두 상태를 추가한 추상 클래스", s(3)),
 ("lineHeight", "XML의 lineSpacingExtra/Multiplier를 Compose에서 통합 대체하는 Text 파라미터", s(4)),
 ("TextOverflow.Ellipsis", "넘치는 텍스트를 말줄임표로(XML ellipsize의 Compose 대응, maxLines와 함께)", s(5)),
 ("CheckedTextView", "TextView에 체크 표시를 더한 위젯. android:checked 기본값 false, 체크 이미지는 android:checkMark", s(6)),
 ("EditText", "텍스트를 편집할 수 있도록 TextView의 기본 속성을 변경한 위젯", s(7)),
 ("placeholder", "XML hint(비었을 때 대신 표시)의 Compose 대응(TextField·OutlinedTextField)", s(7)),
 ("PasswordVisualTransformation()", "Compose 입력창에서 비밀번호 글자를 숨겨 주는 visualTransformation 값", s(9)),
 ("isChecked() / setChecked() / toggle()", "체크 계열 위젯의 체크 상태 확인 / 설정 / 뒤집기 메서드", s(10)),
 ("RadioButton", "여러 옵션 중 하나만 선택할 때 쓰는 위젯. 라디오 그룹으로 묶음", s(11)),
 ("ToggleButton", "on/off 두 상태에 따라 다른 텍스트와 지시자(indicator)를 보여 주는 위젯", s(11)),
 ("enum class", "가능한 값의 종류가 미리 정해진 유한 집합. 지정된 값 외에는 가질 수 없도록 타입 차원에서 강제", s(13)),
 ("const val", "컴파일 시점에 이미 값이 확정되어야 하는 상수(val보다 강한 제약)", s(13)),
 ("celsiusValue", "입력을 섭씨로 통일한 내부 판정 기준(private). 배경색·온도계·슬라이더가 사용", s(16)),
 ("convertedValue", "화면에 실제로 보여 줄 반대 단위 값", s(16)),
 ("Spacer", "지정된 크기만큼 빈 공간을 차지하는 컴포저블", s(19)),
 ("함수 참조 (::)", "함수를 호출하지 않고 나중에 호출할 수 있는 참조만 만들어 넘기는 연산자", s(21)),
 ("focusedContainerColor", "입력창이 포커스를 받아 커서가 깜빡이는 상태의 배경색(unfocused는 포커스 해제 상태)", s(22)),
 ("ImageView", "이미지 출력에 필요한 공통 속성·기능을 모은 클래스. 리소스·로컬 파일·Bitmap·Drawable 출력", s(25)),
 ("ImageButton", "ImageView에 버튼처럼 누르고 떼는 효과를 추가한 클래스. 추가 속성 없음", s(25)),
 ("Bitmap", "파일이 아닌 메모리에 존재하는 비트맵", s(25)),
 ("Drawable", "안드로이드에서 화면에 그릴 수 있는 것을 대표하는 클래스", s(25)),
 ("contentScale", "XML scaleType(이미지를 뷰 크기에 맞추는 방식)의 Compose Image 대응", s(26)),
 ("ProgressBar", "작업의 진행 상태를 회전 바퀴나 수평 막대로 표시하는 출력용 위젯", s(28)),
 ("AbsSeekBar", "사용자가 끌어 놓는 방식을 추가한 ProgressBar 추상 클래스. RatingBar·SeekBar의 부모", s(28)),
 ("indeterminate (불확정 모드)", "진행 상황을 알 수 없을 때 바가 계속 움직이는 애니메이션. Compose는 progress를 안 주면 이 모드", s(29)),
 ("secondaryProgress", "주 진행 바 뒤에 표시되는 보조 진행 값", s(29)),
 ("RatingBar", "별 개수로 점수를 표시하거나 입력하는 위젯. Compose에는 컴포저블이 없어 Row + 별 Icon으로 구현", s(30)),
 ("isIndicator", "RatingBar를 터치·드래그로 수정할 수 없는 읽기 전용으로(Compose: clickable(enabled = !isIndicator))", s(31)),
 ("SeekBar", "thumb을 좌우로 끌어 값을 선택하는 입력용 프로그레스 바(윈도우의 Scroll 바와 유사)", s(32)),
 ("SeekBar.OnSeekBarChangeListener", "SeekBar의 thumb 조작 이벤트를 처리하는 인터페이스(onStartTrackingTouch, onProgressChanged, onStopTrackingTouch)", s(32)),
 ("onValueChangeFinished", "Compose Slider에서 사용자가 손을 떼어 조작을 마칠 때의 콜백(onStopTrackingTouch 대응)", s(33)),
 ("coerceIn(min, max)", "값이 범위보다 작거나 크면 min·max에서 clamp", s(36)),
 ("animateFloatAsState", "Float 값이 바뀔 때 지정한 시간 동안 부드럽게 변하게 하는 애니메이션 함수", s(37)),
 ("sliderValue", "celsiusValue에서 파생되어 −20f~120f로 clamp된 Slider 손잡이 위치(null이면 0f)", s(43)),
]

OUTRO = """
<h3>5장 범위 대조표 — 슬라이드 → 문제</h3>
""" + table(["슬라이드", "내용", "문제"], [["s2~3, 10", "위젯·TextView 계층", "1"], ["s3~5", "TextView 속성 대응", "2"], ["s6, 10~11", "체크 계열 위젯", "3"], ["s7~9", "EditText 대응", "4"],
 ["s12~14", "VM 문법·상태", "5"], ["s15~17, 23~24", "celsius/converted·결과", "6"], ["s18~21", "라디오 줄·Column", "7"], ["s21~22", "::·입력창 색", "8"], ["s25~27", "ImageView", "9"],
 ["s28~30", "ProgressBar 계열", "10"], ["s30~31", "RatingBar", "11"], ["s32~33", "SeekBar·Slider", "12"], ["s34~40", "온도계 막대", "13"], ["s41~45", "Slider 온도 입력", "14"]]) + """
<div class="note"><b>뺀 슬라이드</b>: s1 표지, s46 이후 빈 쪽. 캡처 화면의 숫자(50.0/212.0/−12.2, 167.0, 176.0, 112.8)는 문제 6·13·14 계산에 포함.</div>
<div class="note"><b>원본 오탈자</b>: s4 "letterSapcing", "킹크" / s8 "selectOnAllFocus" <span class="fix">→ selectAllOnFocus</span> / s11 "instructor" <span class="fix">→ indicator</span> / s16 convertedValue를 private이라 함(코드는 공개) / s17 "celsivusValue" / s26 "ViewModel 에서" <span class="fix">→ View</span> / s37 "TurtleApp…animatedDpAsState" / s40 padding 방향 / s41 "Space()" <span class="fix">→ Spacer()</span>.</div>
"""
