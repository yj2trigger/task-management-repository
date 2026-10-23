"""상세본 3장 (4주) — 브랜치와 병합. 핵심본 문제 1~4(포인터·HEAD, ff vs 3-way, 그래프↔명령)와 9(충돌)는 다시 묻지 않는다."""
from osai import R, fig, cmd, run, quote, table, fill

INTRO = """
<div class="note"><b>상세본</b> — 4주차(Branching and Merging). 브랜치·HEAD, fast-forward와 three-way, 실습 그래프 C1~C7, 충돌은 핵심본 문제 1~4, 9에 있다. 여기서는 Git 객체, 브랜치 명령의 세부, 실무 흐름, 실습의 나머지를 다룬다.</div>
<h2>상세 3장. 4주 — 브랜치와 병합</h2>
"""

ITEMS = []
P = ITEMS.append

# 1 ------------------------------------------------------------
ob_q, ob_a = fill(["Git 객체", "담는 것"], [
    ["blob", ("?", "파일 하나의 내용. 그 밖에는 아무것도, 파일 이름조차 담지 않음")],
    ["tree", ("?", "디렉터리 목록: 어떤 파일 이름이 어떤 blob에 대응하는지")],
    ["commit", ("?", "tree 하나를 가리키는 포인터 + 작성자·날짜·메시지 + 바로 앞 커밋(부모)을 가리키는 포인터")]])
P(dict(kind=["table", "calc"], title="git commit 이 실제로 저장하는 것: blob · tree · commit",
parts=[
 dict(q="Git 객체 세 가지가 담는 것을 채우시오." + ob_q, a=ob_a + R("4주 p11"),
      why="<p>각 커밋은 바로 앞 커밋을 가리키는 포인터(<b>parent</b>)를 저장하고, 부모를 거꾸로 따라가면 전체 히스토리가 된다. 병합 커밋은 부모가 둘인 커밋일 뿐이다. " + R("4주 p12") + "</p>"),
 dict(q="파일 세 개가 든 폴더를 처음 커밋하면 Git은 .git에 객체를 몇 개 쓰는가? 그 내역은? 이것이 왜 \"브랜치가 싼\" 이유가 되는가?",
      a="<b>5개</b>: 파일 내용마다 blob 3개 + 폴더 목록 tree 1개 + commit 1개. Git은 \"프로젝트의 한 버전\"을 통째로 저장하지 않고 작은 객체를 쓰며, 브랜치는 그중 커밋 하나를 가리키는 포인터일 뿐이라 브랜치를 만들 때 <b>아무것도 복사되지 않고 포인터만 더해진다</b>. " + R("4주 p10, p11"),
      why="<p>blob이 파일 이름을 담지 않는다는 점이 함정이다. 이름은 tree가 담는다. " + R("4주 p11") + "</p>")],
fig=fig("4주", 10, 60),
quote=quote("Nothing is copied. Only pointers are added.", "원본 4주 p10")))

# 2 ------------------------------------------------------------
bc_q, bc_a = fill(["명령", "하는 일"], [
    ["git branch", ("?", "브랜치 목록. * 가 지금 있는 곳")],
    ["git branch &lt;name&gt;", ("?", "여기(현재 커밋)에 브랜치를 만든다. 이동하지는 않는다")],
    ["git switch &lt;name&gt;", ("?", "있는 브랜치로 이동")],
    ["git switch -c &lt;name&gt;", ("?", "만들고 이동을 한 번에")],
    ["git checkout &lt;name&gt;", ("?", "switch의 옛 이름(어디서나 보임)")],
    ["git checkout -b &lt;name&gt;", ("?", "switch -c의 옛 이름")],
    ["git branch -d &lt;name&gt;", ("?", "병합된 브랜치 삭제")],
    ["git log --oneline --graph --all", ("?", "전체 히스토리를 그림으로")]])
P(dict(kind=["cmd", "table"], title="브랜치 명령 세부 · switch와 checkout",
parts=[
 dict(q="브랜치 명령이 하는 일을 채우시오." + bc_q, a=bc_a + R("4주 p22"),
      why="<p><b>switch와 restore는 Git 2.23에서 추가</b>되어, checkout이 하던 서로 무관한 두 일(브랜치 이동, 파일 복원)을 나눴다. 둘 다 여전히 동작한다. " + R("4주 p22") + "</p>"),
 dict(q="다음 실제 출력을 보고 답하시오. ⓐ 두 번의 git branch 출력에서 *는 무엇을 뜻하나? ⓑ testing에서 C2를 커밋한 뒤 master에서 git branch -d testing 이 거절된 이유는?" + run("s11_branch.txt"),
      a="ⓐ <b>*는 지금 서 있는 브랜치(HEAD가 가리키는 브랜치)</b>다. git switch testing 뒤에 *가 testing으로 옮겨졌다. ⓑ git branch -d 는 <b>병합된 브랜치만</b> 지운다. testing의 C2는 master에 병합되지 않았으므로, 지우면 C2를 가리키는 이름이 사라져 Git이 막는다(강제 삭제는 -D라고 안내). " + R("4주 p22") + " (-D 안내는 실제 출력, 원본 외)"),
 dict(q="브랜치를 바꾸기 전에 커밋하지 않은 변경이 있으면 어떻게 되는가?",
      a="커밋하지 않은 변경은 어느 브랜치에도 속하지 않으므로, Git은 그 변경을 <b>들고 넘어가거나</b> <b>전환을 거부</b>한다. 그래서 \"바꾸기 전에 커밋하라\"고 한다(급하면 6주의 git stash). " + R("4주 p20, 6주 p25"))],
quote=quote("switch and restore were added in Git 2.23 to split the two unrelated jobs checkout used to do.", "원본 4주 p22")))

# 3 ------------------------------------------------------------
P(dict(kind=["order"], title="실무에서 만나는 브랜치 흐름 (hotfix)",
parts=[
 dict(q="다음을 실제 순서대로 나열하시오. ⓐ hotfix를 main 라인에 병합해 배포 ⓑ main 라인에서 앱 작업 중 ⓒ 기능 브랜치로 돌아가 이어서 작업 ⓓ 새 기능이 들어와 브랜치를 만들어 작업 ⓔ 기능이 끝나면 그것도 병합 ⓕ 급한 버그가 보고됨 ⓖ main 라인으로 돌아가 hotfix 브랜치를 땀",
      a="<b>ⓑ → ⓓ → ⓕ → ⓖ → ⓐ → ⓒ → ⓔ</b>. 아무것도 잃지 않고, 진행 중인 두 작업이 서로 부딪히지 않는다. " + R("4주 p24"),
      why="<p>hotfix를 기능 브랜치가 아니라 main에서 따는 이유: 미완성 기능이 버그 수정에 끌려 들어가지 않게 하려는 것이다. " + R("4주 p28") + " 이 흐름의 그래프와 명령은 핵심본 문제 2에 있다.</p>")],
fig=fig("4주", 24, 55),
quote=quote("Nothing is lost, and the two pieces of work never collide while in progress.", "원본 4주 p24")))

# 4 ------------------------------------------------------------
P(dict(kind=["mc", "cmd"], title="병합 마무리와 실습의 나머지",
parts=[
 dict(q="병합과 충돌 마무리에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("충돌을 해결한 뒤 git commit 을 -m 없이 치면 Git이 미리 써 둔 병합 메시지가 열린다.", True, "해결한 파일을 stage하고 -m 없이 git commit 하면 Git이 써 둔 병합 메시지가 열린다. " + R("4주 p40")),
            ("충돌 중에 git merge --abort 를 치면 병합 시작 전 상태로 정확히 돌아간다.", True, "git merge --abort 는 저장소를 병합을 시작하기 전 모습으로 정확히 되돌린다. " + R("4주 p40")),
            ("충돌 표시 줄을 남긴 채 커밋해도 Git이 자동으로 지워 준다.", False, "표시 줄을 남기면 그대로 커밋되어 코드를 깨뜨린다. <<<<<<<, =======, >>>>>>> 줄을 모두 직접 지워야 한다. " + R("4주 p39")),
            ("VS Code는 충돌 화면에서 어느 쪽을 남길지 고르게 해 주며, 실습에서는 Accept Incoming Change를 골랐다.", True, "VS Code가 충돌을 자동으로 보여 주고, 실습에서는 들어오는 쪽(Incoming)을 받아들였다. " + R("4주 p55")),
            ("실습 Stage 6에서 fix-a를 먼저 병합할 때도 충돌이 난다.", False, "fix-a를 master에 먼저 병합하면 master가 갈라진 뒤 움직이지 않았으므로 fast-forward로 성공한다. 그다음 fix-b를 병합할 때 같은 줄을 바꿨으므로 충돌이 난다. " + R("4주 p53, p54"))],
      a="ⓐ ⓑ ⓓ"),
 dict(q="실습 Stage 5에서 네 브랜치(master, dev, feat1, feat2)를 모두 GitHub에 올리려면? 브랜치 하나를 처음 올리는 명령은?",
      a="브랜치를 하나씩 <code>git push -u origin &lt;branch&gt;</code>로 올리거나(4주 명령표), 한 번에 올리려면 <code>git push -u origin --all</code>을 쓴다(보충: 원본은 \"한 번에 올리는 방법을 찾아보라\"고만 함). GitHub 브랜치 목록에 넷이 모두 보여야 한다. " + R("4주 p41, p52"))],
quote=quote("git merge --abort puts the repository back exactly as it was before you started.", "원본 4주 p40")))

KEYWORDS = [
 ("blob", "파일 하나의 내용(이름도 담지 않음)", "원본 4주 p11"),
 ("tree", "파일 이름 → blob 대응의 디렉터리 목록", "원본 4주 p11"),
 ("commit object", "tree 포인터 + 작성자·날짜·메시지 + 부모 포인터", "원본 4주 p11"),
 ("git switch / git checkout", "브랜치 이동(새 이름 / 옛 이름, Git 2.23에서 분리)", "원본 4주 p22"),
 ("git branch -d", "병합된 브랜치 삭제", "원본 4주 p22"),
 ("hotfix", "main 라인에서 따서 급한 버그만 고치는 브랜치", "원본 4주 p28"),
 ("git merge --abort", "충돌 난 병합을 시작 전 상태로 취소", "원본 4주 p40"),
]

OUTRO = """<div class="note"><b>뺀 것</b>: 실습 Stage 0~5의 단계별 화면(핵심본 문제 3에 명령 전체와 실제 그래프), 지난주 recap 슬라이드.</div>"""
