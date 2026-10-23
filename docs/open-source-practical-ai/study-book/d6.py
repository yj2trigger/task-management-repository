"""상세본 4장 (6주) — 히스토리 재작성과 복구. 핵심본 문제 5(rebase 예측·golden rule), 6(reset/revert), 7(상황→명령)은 다시 묻지 않는다."""
from osai import R, fig, cmd, run, quote, table, fill

INTRO = """
<div class="note"><b>상세본</b> — 6주차(Rewriting and Recovering History). rebase 결과 예측·golden rule은 핵심본 문제 5, reset 세 모드·reset vs revert는 문제 6, 상황별 명령은 문제 7에 있다. 여기서는 rebase 절차·팀의 선택, 실습 Mission 2의 실제 출력, reflog 세부, .gitignore를 다룬다.</div>
<h2>상세 4장. 6주 — 히스토리 재작성과 복구</h2>
"""

ITEMS = []
P = ITEMS.append

# 1 ------------------------------------------------------------
tm_q, tm_a = fill(["비교", "Team Merge", "Team Rebase"], [
    ["히스토리란", ("?", "실제로 일어난 일의 기록"), ("?", "프로젝트가 어떻게 만들어졌는지의 이야기")],
    ["주장", ("?", "역사 문서다. 손대지 마라"), ("?", "책의 초고를 그대로 출판하지는 않는다")],
    ["얻는 것", ("?", "진실하지만 병합 커밋으로 어수선함"), ("?", "읽기 좋지만 일부는 지어낸 것")],
    ["비용", ("?", "바쁜 프로젝트에서 git log가 시끄러움"), ("?", "다시 쓴 커밋이 원본을 가진 사람을 깨뜨림")]])
P(dict(kind=["order", "table"], title="rebase 하는 절차 · 팀은 merge와 rebase 중 무엇을 고르나",
parts=[
 dict(q="experiment 브랜치를 master 위로 rebase해 직선 히스토리로 합치는 네 단계를 명령으로 쓰시오. 4단계에서 --no-ff를 붙이지 않는 이유는?",
      a=cmd("""git checkout experiment    # 1. 옮길 브랜치로 이동
git rebase master          # 2. 올라탈 브랜치 위로 rebase
git checkout master        # 3. 그 브랜치로 돌아옴
git merge experiment       # 4. 병합 -> 이미 직선이라 fast-forward""") + "rebase의 목적이 <b>직선 히스토리</b>이므로, 4단계에서 --no-ff를 붙여 병합 커밋을 만들면 목적에 어긋난다. " + R("6주 p15"),
      why="<p>끝에 남는 파일은 merge와 바이트 단위까지 똑같고, 다른 것은 히스토리뿐이다. merge는 \"두 사람이 동시에 일하다 여기서 합쳤다\"를 남기고, rebase는 그 갈라짐을 없애 일이 차례로 일어난 것처럼 읽히게 한다. \"rebase는 더 깨끗한 히스토리를, 동시에 일어나지 않은 히스토리를 만든다.\" " + R("6주 p16") + "</p>"),
 dict(q="Team Merge와 Team Rebase의 입장을 비교한 표를 채우시오. 무엇이 정답인가?" + tm_q,
      a=tm_a + "<b>정답은 없다.</b> 팀마다 하나를 골라 적어 두며, 중요한 것은 무엇을 치기 전에 팀이 무엇을 골랐는지 아는 것이다. " + R("6주 p17"))],
fig=fig("6주", 15, 55),
quote=quote("Rebasing makes a cleaner history. It also makes a history that did not happen.", "원본 6주 p16")))

# 2 ------------------------------------------------------------
P(dict(kind=["order", "diag"], title="golden rule을 어기면 생기는 일 (세 장면)",
parts=[
 dict(q="다음 세 장면을 순서대로 쓰고, 마지막에 어떤 일이 생기는지 쓰시오. ⓐ 내가 C3 위로 rebase하고 force push한다 ⓑ 내가 C4를 push하고 팀원이 pull한다 ⓒ 아직 C4를 가진 팀원이 pull한다",
      a="<b>ⓑ → ⓐ → ⓒ</b>. ⓐ에서 원격의 C4는 사라지고 C4′만 남는다. ⓒ에서 팀원의 C4와 원격의 C4′가 병합되어(M) <b>같은 변경이 두 번</b> 히스토리에 생기고, 어느 것이 진짜인지 아무도 알 수 없다. " + R("6주 p18"),
      why="<p>실제로는 rebase 뒤 내 push가 거절되고, --force를 쓰고 싶어진다. 강제로 밀면 팀원의 다음 pull이 내가 지운 커밋을 되살린다. 이 수업의 안전한 규칙: <b>한 번도 push하지 않은 브랜치만 rebase한다</b>. " + R("6주 p18") + "</p>")],
fig=fig("6주", 18, 60),
quote=quote("Safe rule for this course: rebase only branches you have never pushed.", "원본 6주 p18")))

# 3 ------------------------------------------------------------
P(dict(kind=["diag", "cmd"], title="Mission 2 실제 출력 읽기: amend · reset · stash · stash pop",
intro="practice 브랜치에서 c.md(apple), d.md(red)를 만들고 실습 지시대로 실행한 실제 출력이다. " + R("6주 p42~p46") + run("s8_mission2.txt"),
parts=[
 dict(q="Try 1(amend): \"asdf\"로 c.md만 커밋한 뒤 git add oss/d.md; git commit --amend -m \"C6\" 을 했다. 커밋 수는 어떻게 되었고, C6에는 어떤 파일이 들어 있는가? asdf 커밋의 해시와 C6의 해시는 같은가?",
      a="커밋 수는 asdf 직후와 <b>같다</b>(C1 위에 하나). C6에는 <b>c.md와 d.md 둘 다</b> 들어 있다(git show --stat 출력). 해시는 <b>다르다</b>(asdf와 C6의 해시가 다름) — amend는 마지막 커밋을 고치는 것이 아니라 새 커밋으로 교체하기 때문이다. " + R("6주 p20, p43")),
 dict(q="Try 2(reset): banana를 \"oops\"로 커밋한 뒤 git reset HEAD~1 을 했다. git log와 git status는 어떻게 되었는가? 이 reset은 어느 모드인가?",
      a="git log는 다시 <b>C6에서 끝나고</b>(oops 사라짐), git status -s 는 <code>␣M oss/c.md</code> — banana가 c.md에 <b>수정 상태로 남아 있다</b>. 옵션 없는 reset은 <b>--mixed</b>(포인터 뒤로, staging 비움, 파일 유지)다. " + R("6주 p22, p43")),
 dict(q="Try 3·4(stash): ⓐ stash 뒤 git status는? ⓑ master로 가서 oss 폴더에는 무엇이 있나? ⓒ practice로 돌아와 stash pop 뒤 stash list는? ⓓ reflog에서 amend와 reset은 어떻게 기록됐나?",
      a="ⓐ <b>깨끗</b>(출력 없음) — 변경이 서랍에 들어가 브랜치를 바꿀 수 있다 ⓑ <b>a.md뿐</b>(c.md, d.md는 practice의 커밋에만 있음) ⓒ <b>비었다</b> — pop은 꺼내면서 서랍에서 지운다 ⓓ <code>commit (amend): C6</code>, <code>reset: moving to HEAD~1</code>. 버려진 asdf와 oops 커밋도 reflog에 해시가 남아 있다. " + R("6주 p44, p46"),
      why="<p>stash에는 -m \"메모\"를 붙이라고 했다. 이틀 뒤면 stash가 넷인데 무엇인지 모르게 된다. reflog의 <code>reset: moving to HEAD</code> 한 줄은 git stash가 내부적으로 작업 디렉터리를 되돌리며 남긴 것이다(보충: 실제 출력에서 확인). " + R("6주 p25") + "</p>")],
quote=quote("Add -m \"a note\" when you stash, or in two days you will have four stashes and no idea what they are.", "원본 6주 p25")))

# 4 ------------------------------------------------------------
P(dict(kind=["mc", "cmd"], title="restore --staged · reflog의 한계 · rebase -i",
parts=[
 dict(q="reflog와 되돌리기 명령에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("git restore --staged &lt;file&gt;(옛 형태 git reset HEAD &lt;file&gt;)는 staging 영역만 바꾸고 파일은 건드리지 않으므로 작업을 잃을 수 없다.", True, "파일 하나를 staging 영역에서 빼는 이 용도가, reset이 staging 영역만 건드리는 유일한 경우이며 작업을 잃을 수 없다. " + R("6주 p21")),
            ("reflog는 원격 저장소에도 저장되므로 새로 clone해도 볼 수 있다.", False, "reflog는 내 컴퓨터에만 있는 로컬 기록이라 새로 clone한 저장소에는 없다. " + R("6주 p26")),
            ("reflog는 약 90일 뒤 만료되고, 지운 저장소는 구할 수 없다.", True, "reflog는 약 90일 뒤 만료되며 삭제한 저장소는 되살릴 수 없다. " + R("6주 p26")),
            ("reflog로 커밋을 되찾는 두 단계는 해시를 찾고, 그 해시를 다시 무언가(브랜치나 reset)가 가리키게 하는 것이다.", True, "복구는 ① reflog에서 해시 찾기 ② git branch rescue &lt;해시&gt;처럼 브랜치를 만들거나 그 해시로 reset하기 두 단계다. " + R("6주 p26")),
            ("reset으로 사라진 커밋은 즉시 삭제된다.", False, "reset·amend·rebase로 떨어져 나간 커밋은 지워지지 않고, 어떤 브랜치도 가리키지 않아 도달할 수 없을 뿐이다. " + R("6주 p26"))],
      a="ⓐ ⓒ ⓓ"),
 dict(q="명령 참조표의 git rebase -i HEAD~n 과 git rebase --abort 는 각각 무엇을 하는가? -i에서 고를 수 있는 동작 네 가지는?",
      a="<code>git rebase -i HEAD~n</code>은 <b>마지막 n개 커밋을 편집</b>한다 — pick / reword / squash / drop. <code>git rebase --abort</code>는 잘못된 rebase를 <b>취소</b>한다. " + R("6주 p47"),
      why="<p>squash는 여러 커밋을 하나로 접는 것으로, GitHub의 \"Squash and merge\" 버튼과 같은 개념이다. " + R("7주 p26") + "</p>")],
quote=quote("The reflog is local to your machine and expires after about 90 days.", "원본 6주 p26")))

# 5 ------------------------------------------------------------
gi_q, gi_a = fill(["패턴", "맞는 것", "뜻"], [
    ["*.log", ("?", "debug.log · foo.log"), ("?", "* 는 0개 이상의 문자")],
    ["build/", ("?", "어디에 있든 build 디렉터리"), ("?", "끝의 / 는 디렉터리만")],
    ["**/logs", ("?", "logs/ · src/a/logs/"), ("?", "** 는 깊이와 상관없이")],
    ["/config.json", ("?", "루트에 있는 것 하나만"), ("?", "앞의 / 는 루트에 고정")],
    ["temp?.txt", ("?", "temp1.txt · tempA.txt"), ("?", "? 는 정확히 문자 하나")],
    ["!keep.log", ("?", "keep.log는 남김(무시하지 않음)"), ("?", "! 는 앞 규칙의 예외")]])
P(dict(kind=["table", "mc"], title=".gitignore: 무엇을 빼고, 패턴은 어떻게 읽나",
parts=[
 dict(q=".gitignore 패턴이 무엇에 맞는지 채우시오." + gi_q,
      a=gi_a + R("6주 p31") + run("s9_gitignore.txt", "실제 확인: check-ignore가 어느 규칙에 걸렸는지 보여 줌"),
      why="<p>실제 출력으로 확인한 것: <code>temp12.txt</code>는 ?가 정확히 한 글자라서 <b>무시되지 않았고</b>, <code>sub/config.json</code>은 /config.json이 루트에 고정되어 <b>무시되지 않았으며</b>, <code>keep.log</code>는 !keep.log 예외로 <b>남았다</b>(status에 ??로 보임). " + R("6주 p31") + "</p>"),
 dict(q="저장소에 넣으면 안 되는 것과 .gitignore에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("__pycache__/, node_modules/ 같은 캐시와 .vscode/ 같은 편집기 설정은 버전 관리에 넣지 않는다.", True, "버전 관리에는 내가 쓴 소스만 넣는다. 캐시, 편집기·IDE 설정, OS 찌꺼기(.DS_Store), 큰 바이너리·데이터셋, 키·토큰·비밀번호가 든 파일은 넣지 않는다. " + R("6주 p29")),
            (".gitignore는 프로젝트 루트에 두고 커밋한다.", True, ".gitignore는 프로젝트의 일부이므로 루트에 두고 커밋하며, 새 찌꺼기가 생기면 고친다. " + R("6주 p31")),
            ("API 키를 커밋해 push했다면, 파일을 지우는 커밋을 하면 해결된다.", False, "옛 커밋에 키가 그대로 남아 있으므로 파일을 지워도 소용없다. 유일한 해결은 키를 폐기하고 새로 발급하는 것이다. 공개 저장소는 봇이 훑어 몇 분 만에 쓰인다. " + R("6주 p30")),
            ("이미 추적 중인 파일도 .gitignore에 적으면 바로 추적이 멈춘다.", False, ".gitignore는 이미 추적 중인 파일에 영향을 주지 않는다. 먼저 git rm --cached로 추적을 끊고 패턴을 더한다. " + R("6주 p31"))],
      a="ⓐ ⓑ")],
quote=quote("The only real fix is to revoke the key and issue a new one.", "원본 6주 p30")))

KEYWORDS = [
 ("Team Merge / Team Rebase", "히스토리는 사실의 기록 / 만들어진 과정의 이야기", "원본 6주 p17"),
 ("git rebase -i HEAD~n", "마지막 n개 커밋 편집(pick / reword / squash / drop)", "원본 6주 p47"),
 ("git rebase --abort", "잘못된 rebase 취소", "원본 6주 p47"),
 ("git stash -m \"메모\"", "메모를 붙여 서랍에 넣기", "원본 6주 p25"),
 ("git stash list", "서랍에 무엇이 있는지 보기", "원본 6주 p25"),
 ("unreachable commit", "지워지지 않았지만 어떤 브랜치도 가리키지 않는 커밋", "원본 6주 p26"),
 (".gitignore", "Git이 추적을 시작하지 않을 파일 목록(이미 추적 중인 파일엔 효과 없음)", "원본 6주 p31"),
 ("! (gitignore)", "앞 규칙의 예외", "원본 6주 p31"),
]

OUTRO = """<div class="note"><b>뺀 것</b>: Mission 1(oss6) 단계별 화면(핵심본 문제 5에 실제 그래프), 지난주 recap. <b>원본 빈틈</b>: 6주 p10 "오늘 할 것"의 cherry-pick은 설명 슬라이드가 없다.</div>"""
