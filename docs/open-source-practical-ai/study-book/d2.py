"""상세본 1장 (2주) — 오픈소스 소프트웨어와 AI. 핵심본 문제 12(4가지 권리·open weight·라이선스·Git≠GitHub)는 다시 묻지 않는다."""
from osai import R, fig, cmd, run, quote, table, fill

INTRO = """
<div class="note"><b>상세본</b> — 핵심본에서 물은 지식은 다시 묻지 않고, 나머지를 주차별로 담았다. 이 장은 2주차(Open Source Software &amp; AI)다.
핵심본 문제 12(오픈소스 4가지 권리, open weight vs open source, permissive vs copyleft, Git ≠ GitHub)를 먼저 풀고 오면 좋다.</div>
<h2>상세 1장. 2주 — 오픈소스 소프트웨어와 AI</h2>
"""

ITEMS = []
P = ITEMS.append

# 1 ------------------------------------------------------------
P(dict(kind=["name", "mc"], title="오픈소스 소프트웨어와 proprietary 소프트웨어",
parts=[
 dict(q="오픈소스 소프트웨어(OSS)를 정의하고, proprietary 소프트웨어와 무엇이 다른지 쓰시오.",
      a="OSS는 <b>소스 코드와 함께 배포</b>되고 공개적·협력적으로 개발되며, 사용자에게 사용·학습·수정·배포 권리를 주는 라이선스로 공개된 소프트웨어다. proprietary 소프트웨어는 <b>제한적인 저작권 라이선스</b> 아래 있고, 사용자가 수정할 수 있도록 <b>소스가 공개되지 않는다</b>. " + R("2주 p4")),
 dict(q="오픈소스가 널리 쓰이는 사례에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("Nginx와 Apache가 전체 웹사이트의 약 절반을 서비스한다.", True, "Nginx와 Apache가 웹사이트의 약 절반을 서비스하고, 나머지의 상당 부분은 Cloudflare가 앞단에 있다. " + R("2주 p5")),
            ("Cloudflare는 오픈소스 웹 서버다.", False, "Cloudflare는 다른 서버 앞에 있는 프록시 서비스이며 오픈소스 웹 서버가 아니다(그래프 주석). " + R("2주 p5")),
            ("Chrome, Edge, Opera, Whale은 대부분 Chromium 위에 만들어졌다.", True, "대부분의 웹 브라우저는 Chromium 기반이며 Chrome, Edge, Opera, Whale이 그 예다. " + R("2주 p5")),
            ("Android는 Linux 커널 위에 만들어졌다.", True, "Android는 Linux 커널 위에 만들어진 운영체제다. " + R("2주 p5")),
            ("TOP500 슈퍼컴퓨터 중 일부만 Linux를 쓴다.", False, "TOP500 슈퍼컴퓨터 500대 모두가 2017년부터 Linux를 쓴다. " + R("2주 p6"))],
      a="ⓐ ⓒ ⓓ",
      why="<p>슬라이드의 결론: \"여러분은 모르는 사이에 몇 년째 오픈소스를 써 왔고, 이 수업은 그 반대편(만드는 쪽)으로 건너가는 것\"이다. 지난 학기에 쓴 Python, NumPy도 모두 오픈소스다. " + R("2주 p6") + "</p>")],
quote=quote("Software that is distributed with its source code", "원본 2주 p4")))

# 2 ------------------------------------------------------------
hs_q, hs_a = fill(["연도", "사건", "의미"], [
    ["1953", ("?", "UNIVAC A-2"), ("?", "소스 코드와 함께 무료로 공개된 컴파일러 도구. 고객에게 개선한 것을 다시 보내 달라고 함 → 1950~60년대엔 오픈소스가 기본")],
    ["1969", ("?", "ARPANET"), ("?", "패킷 교환 네트워크. 소스 코드를 물리 테이프 없이 주고받게 함(첫 메시지 1969.10.29, LOGIN의 두 글자 후 다운)")],
    ["1969", ("?", "IBM 반독점 소송"), ("?", "IBM이 하드웨어와 소프트웨어를 따로 팔기 시작 → 소프트웨어 상업화(OSS의 일시적 쇠퇴)")],
    ["1969", ("?", "UNIX (Bell Labs)"), ("?", "Ken Thompson·Dennis Ritchie, 1973년 C로 재작성. 대학에 소스와 함께 배포됐다가 1984 AT&amp;T 분할 후 닫힘")],
    ["1983", ("?", "GNU (GNU's Not Unix)"), ("?", "Richard Stallman. UNIX 호환의 완전 자유 소프트웨어, 커널만 빠짐")],
    ["1991", ("?", "Linux 커널"), ("?", "Linus Torvalds, 1992년부터 GPL. GNU 도구 + Linux 커널 = 완전한 자유 OS")],
    ["1994~96", ("?", "LAMP 스택"), ("?", "Linux·Apache·MySQL·PHP. 라이선스를 하나도 사지 않고 웹사이트를 만들 수 있게 됨(닷컴 시대의 토대)")],
    ["2005 → 2008", ("?", "Git → GitHub"), ("?", "Linus Torvalds가 Linux 커널 관리를 위해 Git을 만들고, GitHub가 기여를 이메일이 아닌 버튼으로 바꿈")]])
P(dict(kind=["table", "order"], title="오픈소스의 짧은 역사",
parts=[
 dict(q="오픈소스 역사의 사건과 의미를 채우시오." + hs_q, a=hs_a + R("2주 p8~p15"),
      why="<p>흐름은 <b>원래 공개(1950~60s) → 상업화로 쇠퇴(1960~80s) → GNU·Linux로 부활 → LAMP로 확산 → Git·GitHub로 참여 장벽이 크게 낮아짐</b>이다. 1974~1980년 CONTU가 이 문제를 연구했고 미국 법이 소프트웨어를 보호하게 되면서 회사들이 저작권·상표를 지키고 사용료를 받았다. " + R("2주 p10, p15") + "</p>"),
 dict(q="UNIX가 대학을 통해 퍼진 이유와, 지금도 UNIX의 흔적이 남아 있는 예를 쓰시오.",
      a="1956년 반독점 동의 판결로 AT&amp;T가 컴퓨터 사업에 들어갈 수 없었기 때문에, UNIX는 <b>원가 수준의 값으로 소스 코드와 함께</b> 대학에 갔고 한 세대가 그 코드를 읽으며 OS를 배웠다. 지금도 macOS는 인증받은 UNIX이고, Linux는 UNIX 계열이며, ls, cd, grep 같은 명령이 UNIX에서 왔다. " + R("2주 p11"))],
quote=quote("GNU tools + Linux kernel = a complete free operating system", "원본 2주 p13")))

# 3 ------------------------------------------------------------
P(dict(kind=["mc"], title="왜 OSS를 쓰고 기여하는가, 그리고 단점",
parts=[
 dict(q="회사와 학생이 OSS를 쓰거나 기여하는 이유, OSS의 단점에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("한 조직이 쓰기에는 소프트웨어가 너무 많아서, 회사는 OSS 커뮤니티의 도움이 필요하다.", True, "현대 자동차처럼 한 회사가 직접 쓰는 것보다 훨씬 많은 소프트웨어가 필요하므로 OSS 커뮤니티의 도움이 필요하다. " + R("2주 p17")),
            ("문서의 오타 하나를 고치는 것도 실제 기여이며, 대부분 여기서 시작한다.", True, "자신이 쓰는 프로젝트의 문서 오타를 고치는 것은 실제 기여이고 거의 모든 사람이 여기서 시작한다. " + R("2주 p18")),
            ("OSS에는 공식 지원 창구가 있어 문제가 빨리 해결된다.", False, "OSS에는 전담 지원이 없어서 공식 지원 창구가 없고, 문제가 늦게 해결되거나 아예 해결되지 않을 수 있다. " + R("2주 p19")),
            ("어떤 라이선스는 사용하는 대가로 내 코드도 공개하도록 요구한다.", True, "OSS의 단점 중 하나가 복잡한 라이선스이며, 일부 라이선스는 내 코드도 공개하도록 요구한다(copyleft). " + R("2주 p19")),
            ("오픈소스라는 사실만으로 그 소프트웨어가 좋다는 근거가 된다.", False, "슬라이드는 \"오픈소스라는 것 자체가 좋다는 논거가 되지는 않는다\"고 경고한다. " + R("2주 p19"))],
      a="ⓐ ⓑ ⓓ",
      why="<p>학생이 기여하는 이유 다섯 가지: <b>Skill development, Portfolio building(GitHub 프로필이 실력을 보여 줌), Networking, Learning from experts, Giving back</b>. 단점 네 가지: <b>전담 지원 부족, 일관성 없는 사용자 경험, 표준화 부족과 책임 불분명(법적·상업적 보증 없음), 복잡한 라이선스</b>. " + R("2주 p18, p19") + "</p>")],
quote=quote("Being open source is not, by itself, an argument that something is good.", "원본 2주 p19")))

# 4 ------------------------------------------------------------
rl_q, rl_a = fill(["AI에서 공개되는 것", "무엇인가", "보통 공개되나?"], [
    ["Code", "프로그램(추론 vs 학습)", ("?", "추론 코드: 예 / 학습 코드: 드묾")],
    ["Weights", "학습된 숫자, 즉 모델 자체", ("?", "자주")],
    ["Data", "모델이 무엇으로 학습했는지", ("?", "드묾")],
    ["Recipe", "학습에 쓴 설정과 절차", ("?", "드묾")]])
ml_q, ml_a = fill(["모델", "하는 일", "공개한 곳", "라이선스"], [
    ["Llama", "텍스트 생성, 채팅", ("?", "Meta"), ("?", "Llama Community License")],
    ["Qwen", "텍스트, 코드, 멀티모달", ("?", "Alibaba"), ("?", "Apache 2.0")],
    ["DeepSeek", "텍스트, 추론, 코드", ("?", "DeepSeek"), ("?", "MIT")],
    ["Gemma", "텍스트·비전, 노트북에서 돌릴 만큼 작음", ("?", "Google"), ("?", "Gemma terms, Gemma 4부터 Apache 2.0")],
    ["gpt-oss", "텍스트, 추론", ("?", "OpenAI"), ("?", "Apache 2.0")],
    ["FLUX", "이미지 생성", ("?", "Black Forest Labs"), ("?", "변형에 따라 Apache 2.0 또는 비상업")],
    ["Whisper", "음성 → 텍스트", ("?", "OpenAI"), ("?", "MIT")]])
P(dict(kind=["table", "mc"], title="AI 스택과 공개되는 것 · 오픈 AI 모델",
parts=[
 dict(q="AI 스택 중 오픈소스가 <b>아닌</b> 예외 하나는? 응용 계층 아래의 오픈소스 예를 계층별로 쓰시오.",
      a="예외는 <b>NVIDIA CUDA</b>(proprietary)다. 언어·OS: Python, Linux / 수치 계산: NumPy, SciPy, pandas / 딥러닝 프레임워크: PyTorch, JAX / 모델 라이브러리·서빙: Hugging Face Transformers, vLLM. 그래서 논문이 어떻게 구현됐는지 추측하지 않고 코드를 읽을 수 있다. " + R("2주 p21")),
 dict(q="AI 모델에서 무엇이 보통 공개되는지 표를 채우시오. 대부분의 \"오픈\" AI 모델은 무엇만 공개하는가?" + rl_q,
      a=rl_a + "대부분의 \"오픈\" AI 모델은 <b>코드와 가중치만</b> 공개한다. 그래서 실행하고 fine-tune할 수는 있지만 처음부터 다시 만들 수 없고 무엇을 학습했는지 볼 수 없다. 학습 데이터와 레시피까지 모두 공개하는 드문 예는 <b>OLMo, Pythia, SmolLM</b>이다. " + R("2주 p22")),
 dict(q="오늘날의 오픈 AI 모델과 라이선스 표를 채우시오." + ml_q, a=ml_a + R("2주 p24"),
      why="<p>누구나 내려받을 수 있지만 작은 버전은 노트북에서, 큰 버전은 GPU가 많이 필요하고 <b>라이선스가 모두 같지 않다</b>. 같은 회사(OpenAI)라도 gpt-oss는 Apache 2.0, Whisper는 MIT다. " + R("2주 p24") + "</p>")],
quote=quote("Most \"open\" AI models release only the code and the weights.", "원본 2주 p22")))

# 5 ------------------------------------------------------------
P(dict(kind=["diag", "cmd"], title="왜 버전 관리인가 · 첫 실습",
parts=[
 dict(q="report.py → report_v2.py → report_final.py → report_final_REALLY.py 처럼 파일 이름으로 버전을 관리할 때 생기는 문제 네 가지를 쓰시오.",
      a="① 두 파일 사이에 <b>무엇이</b> 바뀌었는지 알 수 없다 ② <b>왜</b>, <b>누가</b> 바꿨는지 알 수 없다 ③ 지난 화요일 버전으로 <b>돌아갈</b> 수 없다 ④ 두 사람이 서로 덮어쓰지 않고 <b>동시에</b> 작업할 수 없다. 버전 관리는 이 네 가지를 모두 해결한다. " + R("2주 p27")),
 dict(q="2주차 실습: ⓐ Git이 설치됐는지 확인하는 명령과, Windows에서 그 명령을 칠 곳 ⓑ 프로필 저장소를 만들려면 저장소 이름을 무엇으로 하나 ⓒ 그 저장소의 공개 설정·README·라이선스 선택 ⓓ 브라우저에서 README를 고쳐 저장한 것은 무엇이 되나",
      a="ⓐ <code>git --version</code>, Windows에서는 Command Prompt가 아니라 <b>Git Bash</b> ⓑ <b>자기 GitHub 사용자명과 똑같이</b> ⓒ Public, \"Add a README file\" 체크, 라이선스 <b>MIT</b> ⓓ 첫 커밋(first commit) " + R("2주 p30, p32, p33"),
      why="<p>GitHub 사용자명은 커리어 내내 따라다니므로 신중히(실명이나 깔끔한 변형) 고르라고 했다. 학생 인증은 github.com/education에서 하고 승인에 며칠 걸릴 수 있다. " + R("2주 p31") + "</p>")],
quote=quote("Version control solves all four.", "원본 2주 p27")))

KEYWORDS = [
 ("proprietary software", "제한적인 저작권 라이선스 아래 있고 소스가 공개되지 않는 소프트웨어", "원본 2주 p4"),
 ("UNIVAC A-2 (1953)", "소스 코드와 함께 무료로 공개된 컴파일러 도구", "원본 2주 p8"),
 ("ARPANET (1969)", "패킷 교환 광역 네트워크. 소스 코드 교환을 쉽게 함", "원본 2주 p9"),
 ("UNIX (1969)", "Bell Labs, Ken Thompson·Dennis Ritchie. 1973년 C로 재작성", "원본 2주 p11"),
 ("GNU (1983)", "GNU's Not Unix. Richard Stallman의 UNIX 호환 자유 소프트웨어", "원본 2주 p12"),
 ("Linux kernel (1991)", "Linus Torvalds. 1992년부터 GPL", "원본 2주 p13"),
 ("LAMP stack", "Linux, Apache, MySQL, PHP (1994~96)", "원본 2주 p14"),
 ("NVIDIA CUDA", "오픈소스 AI 스택에서 유일하게 proprietary로 남은 것", "원본 2주 p21"),
 ("OLMo · Pythia · SmolLM", "학습 데이터와 레시피까지 모두 공개하는 드문 모델", "원본 2주 p22"),
 ("profile repository", "GitHub 사용자명과 똑같은 이름의 저장소", "원본 2주 p32"),
]

OUTRO = """<div class="note"><b>뺀 것</b>: 성적 비율·출석 규정(2주 p2), 웹 서버·브라우저 점유율 수치 그래프, ARPANET 지도, 설문 링크.</div>"""
