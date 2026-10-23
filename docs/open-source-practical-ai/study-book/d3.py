"""상세본 2장 (3주) — Git 기초. 핵심본 문제 8(세 상태·세 영역)과 7(상황→명령)은 다시 묻지 않는다."""
from osai import R, fig, cmd, run, quote, table, fill

INTRO = """
<div class="note"><b>상세본</b> — 3주차(Git Basics). 세 상태·세 영역 추적은 핵심본 문제 8, 상황별 명령은 핵심본 문제 7에 있다. 여기서는 그 밖의 3주차 내용과 <code>git status -s</code> 출력 읽기를 다룬다. 출력은 임시 연습 저장소에서 실제로 실행한 결과다.</div>
<h2>상세 2장. 3주 — Git 기초</h2>
"""

ITEMS = []
P = ITEMS.append

# 1 ------------------------------------------------------------
P(dict(kind=["mc", "name"], title="Git의 설계 목표 · 분산 · 스냅샷 · 무결성",
parts=[
 dict(q="Git의 설계 목표 세 가지를 쓰시오.",
      a="① <b>비선형 개발</b> 지원(여러 사람이 동시에 작업) ② <b>분산 개발</b>(하나의 중앙 사본이 필요 없음) ③ 큰 프로젝트를 효율적으로 다루기. " + R("3주 p6")),
 dict(q="Git의 저장 방식과 무결성에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("모든 클론은 첫 커밋부터의 전체 히스토리를 가진 완전한 백업이다.", True, "분산 버전 관리에서 클라이언트는 전체 히스토리를 포함해 저장소를 그대로 미러링하므로, 모든 클론이 데이터 전체의 백업이다. " + R("3주 p7")),
            ("커밋, 히스토리 보기, 버전 비교에는 인터넷이 필요하다.", False, "Git의 대부분 작업(커밋, 히스토리 보기, 버전 비교)은 네트워크 없이 로컬에서 된다. 인터넷은 다른 사람과 공유할 때만 필요하다. " + R("3주 p7")),
            ("Git은 커밋할 때마다 바뀐 줄(차이)만 저장한다.", False, "Git은 차이가 아니라 스냅샷을 저장한다. 바뀌지 않은 파일은 이전 파일에 연결하고, 바뀐 파일은 전체 새 버전을 저장한다. 그래서 옛 버전으로 돌아가기가 빠르다. " + R("3주 p8")),
            ("Git은 모든 것을 SHA-1 해시(40자리 16진수)로 체크섬하며, 보통 앞 7자리만 본다.", True, "Git 데이터베이스는 파일 이름이 아니라 해시로 저장하고, 해시는 0-9, a-f로 된 40자리이며 실제로는 앞 7자리를 주로 본다. " + R("3주 p9")),
            ("Git은 거의 항상 데이터를 더하기만 하므로, 커밋한 것은 거의 언제나 되살릴 수 있다.", True, "Git의 거의 모든 동작은 데이터를 더하므로 한번 커밋한 데이터를 실수로 지우기 어렵고 대부분 되돌릴 수 있다. 그래서 \"자주 일찍 커밋하라\"고 한다. " + R("3주 p10"))],
      a="ⓐ ⓓ ⓔ")],
quote=quote("Every clone is a full backup of all the data", "원본 3주 p7")))

# 2 ------------------------------------------------------------
cf_q, cf_a = fill(["하고 싶은 것", "명령"], [
    ["커밋에 남길 이름 설정", ("?", "git config --global user.name \"Your Name\"")],
    ["커밋에 남길 이메일 설정(GitHub 계정과 같은 이메일)", ("?", "git config --global user.email \"your@email.com\"")],
    ["설정 확인", ("?", "git config --list (원본 표기는 –-list)")],
    ["기본 브랜치 이름을 main으로", ("?", "git config --global init.defaultBranch main")],
    ["지금 폴더를 Git 저장소로(첫 브랜치 main)", ("?", "git init (또는 git init -b main)")],
    ["GitHub의 기존 저장소를 히스토리째 복사", ("?", "git clone https://github.com/user/repo.git")]])
P(dict(kind=["cmd", "table"], title="Git 설정과 저장소 만들기",
parts=[
 dict(q="하고 싶은 일에 맞는 명령을 쓰시오." + cf_q, a=cf_a + R("3주 p16, p17"),
      why="<p>user.email을 GitHub 계정과 같게 하지 않으면 커밋이 내 계정과 연결되지 않는다. GitHub는 기본 브랜치로 main을 쓰고, 오래된 자료는 master라고 한다. git init은 .git 디렉터리를 만들 뿐 아직 아무것도 추적하지 않고, git clone은 최신 파일만이 아니라 전체 히스토리를 받는다. " + R("3주 p16, p17") + "</p>")],
quote=quote("Use the same email as your GitHub account, or your commits will not be linked to you", "원본 3주 p16")))

# 3 ------------------------------------------------------------
P(dict(kind=["diag", "table"], title="git status -s 출력 읽기 (실제 실행)",
intro="아래는 새 저장소에서 README를 만들고 add·commit·수정을 이어 가며 <code>git status -s</code>를 친 실제 출력이다. " + run("s7_states.txt"),
parts=[
 dict(q="위 출력에서 <code>??</code>, <code>A␣</code>, <code>␣M</code>, <code>MM</code>은 각각 README가 어떤 상태라는 뜻인가? (짧은 출력은 왼쪽 칸이 staging 영역, 오른쪽 칸이 작업 디렉터리)",
      a="<code>??</code> untracked(새 파일, 아직 git add 안 함) / <code>A␣</code> 새 파일이 staged됨(다음 커밋에 추가) / <code>␣M</code> 추적 중인 파일이 수정됐지만 staged 안 됨(modified) / <code>MM</code> 수정분 일부는 staged, 그 뒤에 또 수정해 staged 안 된 변경도 있음. 아무것도 안 나오면 깨끗(unmodified)하다. " + R("3주 p18~p21") + " (칸의 의미는 실제 출력으로 확인한 보충)",
      why="<p>git status -s 는 파일마다 한 줄로 보여 주는 짧은 출력이다. 슬라이드는 \"git status를 계속 쳐라, 내가 어디 있는지 아는 가장 싼 방법\"이며 출력이 다음에 칠 명령까지 알려 준다고 했다. " + R("3주 p19, p21") + "</p>"),
 dict(q="MM 상태에서 <code>git diff</code>와 <code>git diff --staged</code>는 각각 무엇을 보여 주는가? 위 출력의 + 줄로 답하시오.",
      a="<code>git diff</code>는 <b>아직 staged 안 된 변경</b>(+again), <code>git diff --staged</code>는 <b>staged되어 다음 커밋에 들어갈 변경</b>(+world)을 보여 준다. 이 두 명령이 커밋 전에 스스로 확인하는 짝이다. " + R("3주 p24")),
 dict(q="MM 상태에서 <code>git rm --cached README</code>를 쳤더니 위처럼 거절됐다. 왜인가? (보충)",
      a="staging 영역의 내용이 작업 파일과도, 마지막 커밋(HEAD)과도 다르기 때문이다. 이대로 추적을 끊으면 staged한 내용(world 추가분)이 어디에도 남지 않으므로 Git이 막고 <code>-f</code>로 강제하라고 안내한다. 정상적인 경우(아래 문제 4)에는 파일은 남고 추적만 해제된다. (보충: 원본에 없는 실제 실행 결과)")],
quote=quote("Run it constantly. It is the cheapest way to know where you are.", "원본 3주 p19")))

# 4 ------------------------------------------------------------
P(dict(kind=["mc", "diag"], title="git add · commit 메시지 · rm · add -A",
parts=[
 dict(q="git add 가 하는 두 가지 일을 쓰고, git add 를 어떻게 생각하라고 했는지 쓰시오.",
      a="① 새 파일의 <b>추적을 시작</b>한다 ② 이미 추적 중인 파일의 <b>변경을 stage</b>한다. \"이 파일을 프로젝트에 추가\"가 아니라 <b>\"이 내용을 다음 커밋에 넣어라\"</b>로 생각한다. " + R("3주 p22")),
 dict(q="커밋 메시지로 수업 기준에 맞는 것을 모두 고르시오.",
      opts=[("Add a short README", True, "한 줄, 명령형(Add)으로 무엇을 바꿨는지 썼으므로 좋은 메시지다. " + R("3주 p23")),
            ("update", False, "\"update\"는 무엇을 왜 바꿨는지 알 수 없어 나중에 비용이 되며, 이 수업 채점에서도 감점 요인이라고 했다. " + R("3주 p23")),
            ("Fix division by zero in divide()", True, "명령형(Fix)으로 무엇을 고쳤는지 분명히 썼다(보충 예시). " + R("3주 p23")),
            ("asdf", False, "의미 없는 메시지는 나중에 비용이 된다고 수업이 직접 예로 든 나쁜 메시지다. " + R("3주 p23")),
            ("I changed some code by using a for loop", False, "메시지에는 어떻게(how)가 아니라 무엇을, 왜 바꿨는지를 쓴다. 명령형도 아니다. " + R("3주 p23"))],
      a="ⓐ ⓒ"),
 dict(q="이미 추적 중인 secret.txt를 .gitignore에 적었는데도 git status에 계속 나온다. 왜이며, 어떻게 해야 하나? (실제 실행)" + run("s10_tracked_ignore.txt"),
      a=".gitignore는 <b>아직 추적하지 않는 파일만</b> 막고, 이미 추적 중인 파일에는 효과가 없다. 먼저 <code>git rm --cached secret.txt</code>로 추적을 끊어야 한다(위 출력의 <code>D␣</code>는 추적 해제가 staged된 것, 파일은 디스크에 남음). " + R("6주 p31, 3주 p25"),
      why="<p>단, 이미 push한 비밀 값은 rm --cached로도 과거 커밋에서 지워지지 않는다. 유일한 해결은 키를 폐기하고 새로 발급하는 것이다. " + R("6주 p30") + "</p>"),
 dict(q="<code>git add -A</code>는 무엇과 같은가? 왜 조심하라고 했나?",
      a="새 파일·수정·삭제를 모두 stage하며 <code>git add . ; git add -u .</code>과 같다(점을 빠뜨리지 말 것). 편하지만 건드린 것을 몽땅 stage해 지저분한 커밋이 되므로, 매번 git status를 먼저 친다. " + R("3주 p26"))],
quote=quote("Think of it as \"put this content into the next commit\", not \"add this file to the project\"", "원본 3주 p22")))

# 5 ------------------------------------------------------------
rm_q, rm_a = fill(["하고 싶은 것", "명령"], [
    ["로컬 저장소에 GitHub 저장소를 origin이라는 이름으로 연결", ("?", "git remote add origin https://github.com/username/oss2.git")],
    ["연결된 원격 주소 확인", ("?", "git remote -v")],
    ["origin 주소 바꾸기", ("?", "git remote set-url origin NEW_ADDRESS")],
    ["현재 브랜치 이름을 main으로", ("?", "git branch -M main")],
    ["처음 push하며 upstream 설정", ("?", "git push -u origin main")],
    ["다른 사람이 올린 커밋을 받아 현재 브랜치에 합치기", ("?", "git pull (upstream 설정 전에는 git pull origin main)")]])
P(dict(kind=["cmd", "table"], title="원격 저장소: remote · push · pull",
parts=[
 dict(q="원격 저장소 작업에 맞는 명령을 쓰시오. remote의 관례 이름은?" + rm_q, a=rm_a + "관례상 주 원격의 이름은 <b>origin</b>이다. " + R("3주 p29~p33"),
      why="<p>push는 내 로컬 커밋을 원격에 올리고, pull은 다른 사람이 더한 커밋을 내려받아 현재 브랜치에 합친다. -u로 upstream을 설정하면 이후 git push, git pull만 쳐도 된다. clone한 저장소에는 origin이 이미 설정되어 있다. 들일 습관: <b>작업 시작 전 pull, 끝낼 때 push</b>. 여기까지는 모두 로컬이라 아무도 볼 수 없었고, push부터 남이 보게 된다. " + R("3주 p30, p32, p33") + "</p>"),
 dict(q="3주차 실습에서 5개 커밋을 올릴 GitHub 저장소를 만들 때 README와 라이선스를 넣지 않은 \"빈 저장소\"로 만든 까닭을 추측해 쓰시오. (보충 추론)",
      a="로컬에 이미 히스토리가 있으므로, GitHub 쪽에 README 커밋이 생기면 원격과 로컬 히스토리가 서로 다른 커밋에서 시작해 첫 push가 거절되고 병합이 필요해진다. 빈 저장소면 로컬 히스토리를 그대로 push할 수 있다. (보충 추론: 원본은 \"No readme file, No license\"만 지시) " + R("3주 p40"))],
quote=quote("The -u flag sets the upstream, so later you can just type git push", "원본 3주 p32")))

KEYWORDS = [
 ("distributed version control system", "모든 클론이 전체 히스토리를 가진 완전한 백업인 버전 관리", "원본 3주 p7"),
 ("snapshot", "커밋마다 모든 파일이 그 순간 어떻게 생겼는지 찍어 둔 것", "원본 3주 p8"),
 ("SHA-1 hash", "40자리 16진수 체크섬. 실제로는 앞 7자리를 봄", "원본 3주 p9"),
 ("tracked / untracked", "마지막 스냅샷에 있거나 새로 staged된 파일 / 그 밖의 파일", "원본 3주 p18"),
 ("git status -s", "파일마다 한 줄의 짧은 상태 출력", "원본 3주 p21"),
 ("git diff / git diff --staged", "staged 안 된 변경 / staged된 변경", "원본 3주 p24"),
 ("git rm", "추적 중인 파일을 지우고 그 삭제를 stage", "원본 3주 p25"),
 ("git add -A", "새 파일·수정·삭제를 모두 stage (= git add . ; git add -u .)", "원본 3주 p26"),
 ("origin", "주 원격 저장소의 관례 이름", "원본 3주 p29"),
 ("push / pull", "내 커밋을 원격에 올리기 / 남의 커밋을 받아 합치기", "원본 3주 p30"),
 ("git remote set-url", "origin 주소 바꾸기", "원본 3주 p31"),
]

OUTRO = """<div class="note"><b>뺀 것</b>: Git 설치·Git Bash 열기·pwd/ls(3주 p2, p15, p36), VS Code 숙제(p43). <b>원본 표기</b>: p16 "git config –-list" <span class="fix">→ --list</span>, p26 "git add –A" <span class="fix">→ -A</span>.</div>"""
