"""핵심본 — 출제 가능성이 높은 것만: 그래프↔명령, reset/revert, 상황→명령, 세 상태, 충돌, GitHub 협업, 2주차 요약.

근거: 교수의 출제 예시(6주 p2, 7주 p2), 여러 주에 recap된 슬라이드, 교수의 요약표.
그래프 정답은 runs/의 실제 git 실행 출력이다.
"""
from osai import R, fig, cmd, run, quote, table, fill

INTRO = """
<div class="note"><b>시험</b> 10/26(월) 13:00~14:00, 제1학술관 302호, <b>2~7주차</b>. 교수가 든 출제 예시: ① 어떤 명령과 <b>옵션</b>을 써야 하는지 ② <b>커밋 그래프를 주고 만드는 명령 쓰기(또는 반대)</b> ③ <b>reset인가 revert인가, 왜</b>. """ + R("6주 p2, 7주 p2") + """<br>
명령 요약표에는 "외울 필요는 없고, 어떤 명령을 꺼내 쓸지 알면 된다"고 적혀 있다 """ + R("4주 p41") + """. 하지만 시험은 명령을 <b>직접 쓰게</b> 하므로, 아래 문제의 명령은 손으로 써 보며 익힌다.<br>
<b>이 핵심본</b>은 출제 예시·여러 주에 반복된 슬라이드·교수의 요약표만 골랐다. 그래프 정답은 임시 연습 저장소에서 <b>실제 git으로 실행</b>한 <code>git log --oneline --graph --all</code> 출력이다(맨 위가 최신 커밋, <code>*</code>가 커밋, <code>|\\</code>가 갈라짐·합쳐짐).</div>
<h2>핵심본 — 오픈소스실전인공지능 중간고사</h2>
"""

ITEMS = []
P = ITEMS.append

# 1 ------------------------------------------------------------
P(dict(kind=["name", "mc"], title="브랜치는 포인터, HEAD는 내가 선 브랜치",
parts=[
 dict(q="Git에서 브랜치는 무엇이고, HEAD는 무엇을 가리키는가?",
      a="Git의 브랜치는 <b>커밋 ID 하나를 담은 41바이트 파일</b>, 즉 커밋을 가리키는 포인터다. " + R("4주 p15") + " HEAD는 <b>지금 서 있는 브랜치</b>를 가리킨다. 커밋이 아니라 브랜치를 가리킨다. " + R("4주 p17"),
      why="<p>그래서 브랜치를 만들거나 지워도 파일은 복사되지 않고 작은 파일 하나만 생기거나 없어진다. 실습에서 계속 물을 세 질문: \"나는 어느 브랜치에 있나? 그 브랜치는 어느 커밋을 가리키나? HEAD는 어디를 가리키나?\" " + R("4주 p15, p17") + "</p>"),
 dict(q="Git의 브랜치·HEAD·커밋에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("git branch testing 은 testing 브랜치를 만들고 그 브랜치로 이동한다.", False, "git branch testing 은 현재 커밋을 가리키는 포인터 testing을 만들기만 하고 이동하지 않는다. HEAD는 원래 브랜치에 그대로 있다. 만들고 이동까지 하려면 git switch -c testing 을 쓴다. " + R("4주 p16, p17, p22")),
            ("커밋하면 HEAD가 가리키는 브랜치만 새 커밋으로 움직이고, 다른 브랜치는 그대로다.", True, "브랜치는 그 브랜치에 서서 커밋할 때만 움직인다. testing에서 커밋하면 testing만 앞으로 가고 master는 제자리다. " + R("4주 p19")),
            ("git switch 로 브랜치를 바꾸면 HEAD가 옮겨지고, 작업 디렉터리의 파일도 그 브랜치의 내용으로 바뀐다.", True, "브랜치를 바꾸면 HEAD가 움직이고 디스크의 파일이 그 브랜치의 스냅샷으로 다시 쓰인다. 그래서 바꾸기 전에 커밋해 두라고 한다. " + R("4주 p18, p20")),
            ("브랜치를 하나 만들면 프로젝트 파일 전체가 새로 복사된다.", False, "브랜치를 만들면 커밋을 가리키는 작은 파일 하나만 생기고, 파일은 아무것도 복사되지 않는다. 그래서 브랜치는 거의 공짜다. " + R("4주 p10, p15")),
            ("병합 커밋(merge commit)은 부모가 둘인 커밋이다.", True, "각 커밋은 바로 앞 커밋(부모)을 가리키고, 병합 커밋은 부모가 둘인 커밋일 뿐이다. " + R("4주 p12, p33"))],
      a="ⓑ ⓒ ⓔ")],
fig=fig("4주", 17, 62),
quote=quote("HEAD points to the branch you are currently on", "원본 4주 p17")))

# 2 ------------------------------------------------------------
ff_q, ff_a = fill(["비교", "Fast-forward", "Three-way merge"], [
    ["언제", ("?", "내가 서 있는 브랜치가 갈라진 뒤 움직이지 않았을 때"), ("?", "두 브랜치 모두 새 커밋이 있을 때")],
    ["Git이 하는 일", ("?", "포인터를 앞으로 민다"), ("?", "세 스냅샷(공통 조상 + 두 끝)으로 새 커밋을 만든다")],
    ["새 커밋?", ("?", "없음"), ("?", "있음, 병합 커밋")],
    ["히스토리 모양", ("?", "직선 그대로"), ("?", "갈라졌다 합쳐지는 모양")],
    ["충돌 가능?", ("?", "없음"), ("?", "있음")]])
P(dict(kind=["graph", "table"], title="iss53과 hotfix: fast-forward와 three-way merge",
intro="상황: master에 커밋 C0, C1, C2가 있다. 기능 작업(iss53)을 하던 중 급한 버그가 들어와 hotfix를 먼저 처리한 뒤, 기능을 마저 끝내고 합친다. " + R("4주 p24~p33"),
parts=[
 dict(q="다음 순서가 되도록 명령을 쓰시오. ⓐ iss53 브랜치를 만들어 이동하고 C3을 커밋 ⓑ master로 돌아가 hotfix 브랜치를 만들어 이동하고 C4를 커밋 ⓒ master로 가서 hotfix를 병합하고 hotfix 브랜치를 지움 (파일 수정 후 커밋은 git commit -am \"메시지\" 한 줄로 써도 된다)",
      a=cmd("""git switch -c iss53          # (= git checkout -b iss53)
git commit -am "C3"
git switch master
git switch -c hotfix
git commit -am "C4"
git switch master
git merge hotfix             # Fast-forward
git branch -d hotfix""") + run("s2_ff_msg.txt", "git merge hotfix 실제 출력") + run("s2_after_ff.txt", "병합 후 그래프"),
      why="<p>master는 hotfix가 갈라진 뒤 자기 커밋이 없었으므로(바로 뒤에 있었으므로) Git은 새 커밋을 만들지 않고 <b>포인터만 C4로 민다</b>. 이것이 fast-forward이고 병합 커밋이 생기지 않는다(출력에 \"Fast-forward\"). " + R("4주 p30") + "</p>"),
 dict(q="이어서 iss53으로 돌아가 C5를 커밋한 뒤, master로 가서 iss53을 병합했다. 이번 병합은 어떤 병합이고 새 커밋이 생기는가? Git은 어떤 세 스냅샷을 비교하는가?",
      a=cmd("""git switch iss53
git commit -am "C5"
git switch master
git merge iss53              # three-way merge -> 병합 커밋 C6""") + run("s2_after_3way.txt", "병합 후 그래프") + "<b>three-way merge</b>이고 새 병합 커밋 C6이 생긴다. Git은 <b>공통 조상 C2</b>와 두 끝 <b>C4(master), C5(iss53)</b> 세 스냅샷을 비교해, C2→C4 변경과 C2→C5 변경을 모두 담은 C6을 만든다. C6은 부모가 둘이다. " + R("4주 p32, p33"),
      why="<p>판정 질문은 하나: \"내가 서 있는 브랜치(master)가 갈라진 뒤 움직였나?\" 안 움직였으면 fast-forward, 움직였으면(C4) three-way다. Git이 히스토리 모양을 보고 고르며, 사람이 고르는 것이 아니다(--no-ff로 바꿀 수는 있음). " + R("4주 p34") + "</p>"),
 dict(q="Fast-forward와 three-way merge를 비교하는 표를 채우시오." + ff_q, a=ff_a + R("4주 p34"))],
fig=fig("4주", 33, 62),
quote=quote("This is a fast-forward. No merge commit is created.", "원본 4주 p30")))

# 3 ------------------------------------------------------------
P(dict(kind=["graph"], title="그래프 → 명령: 실습 그래프 C1~C7 (oss3)",
intro="저장소 oss3, 파일 하나 oss/a.md, 브랜치 넷(master, dev, feat1, feat2), 커밋 일곱 개. 노란 C4, C6, C7은 병합 커밋(부모 둘)이다. 각 커밋은 a.md에 한 줄을 더한다(C2 university, C3 erica, C5 department of AI). " + R("4주 p43~p52") + fig("4주", 43, 62),
parts=[
 dict(q="위 그래프(원본 그림)를 만드는 명령을 처음부터 쓰시오. (git init -b master 부터)",
      a=cmd("""git init -b master
# oss/a.md 에 "hanyang" 작성
git add .
git commit -m "C1"
git branch dev
git branch feat1                 # 만들기만, 이동은 아직
git switch feat1
git commit -am "C2"              # university 추가
git commit -am "C3"              # erica 추가
git switch dev
git merge --no-ff -m "C4" feat1  # dev는 C1에 그대로 -> --no-ff 필수
git switch -c feat2              # C4에서 feat2 생성·이동
git commit -am "C5"              # department of AI 추가
git switch dev
git merge --no-ff -m "C6" feat2
git switch master
git merge --no-ff -m "C7" dev
git log --oneline --graph --all""") + run("s1_oss3.txt", "위 명령의 실제 그래프"),
      why="<p>병합 셋(C4, C6, C7) 모두 <b>받는 쪽 브랜치가 갈라진 뒤 움직이지 않았다</b>(dev는 C1, 다시 C4, master는 C1). 그래서 그냥 git merge를 쓰면 fast-forward가 되어 병합 커밋이 생기지 않는다. 그래프에 병합 커밋을 남기려면 세 번 모두 <b>git merge --no-ff</b>를 써야 한다. 이것이 이 실습의 \"유일한 어려움\"이다. " + R("4주 p43, p49") + "</p>"),
 dict(q="3단계에서 --no-ff 없이 git switch dev 후 git merge feat1 을 쓰면 그래프는 어떻게 되는가?",
      a=run("s1b_merge_msg.txt", "git merge feat1 실제 출력") + run("s1b_ff.txt", "그 뒤 그래프") + "dev가 C1에서 C3으로 <b>fast-forward</b>되어 병합 커밋 C4가 생기지 않고, 히스토리가 <b>직선</b>이 된다. 브랜치가 있었다는 흔적이 그래프에 남지 않는다. " + R("4주 p36, p49"),
      why="<p>\"직선이 나오면 이 단계를 다시 하라\"는 실습 지시가 이 함정을 가리킨다. 많은 팀이 기능마다 그래프에 보이게 하려고 --no-ff를 요구한다. " + R("4주 p35, p49") + "</p>")],
quote=quote("git merge --no-ff &lt;branch&gt;  tells Git to build a merge commit anyway", "원본 4주 p35")))

# 4 ------------------------------------------------------------
P(dict(kind=["graph"], title="명령 → 그래프: 명령을 보고 그래프 그리기",
parts=[
 dict(q="다음 명령을 차례로 실행한 뒤의 그래프를 그리고, 각 브랜치와 HEAD가 가리키는 커밋을 쓰시오. 마지막 커밋 C5의 부모는 몇 개인가?" + cmd("""git init -b main
git add a.txt               # a.txt 새로 만든 뒤
git commit -m "C1"
git branch feat
git switch feat
git add b.txt               # b.txt 새로 만든 뒤
git commit -m "C2"
git commit -am "C3"
git switch main
git commit -am "C4"
git merge --no-ff -m "C5" feat"""),
      a=run("s6_graph.txt", "실제 그래프") + "main과 HEAD는 <b>C5</b>, feat는 <b>C3</b>을 가리킨다. C5는 C4(main)와 C3(feat)을 부모로 갖는 <b>병합 커밋(부모 2개)</b>이다. 실제로 C5의 부모 해시를 출력하면 두 개가 나온다: " + run("s6_parents.txt", "git log -1 --format=%p 출력"),
      why="<p>그리는 순서: ① C1에서 feat가 갈라짐 ② feat에 C2, C3 ③ main에 C4 → 두 갈래 ④ main이 C4로 움직였으므로 병합은 three-way, 새 커밋 C5가 두 갈래를 잇는다. 이후 <code>git branch -d feat</code>은 병합된 브랜치라 지워진다(\"Deleted branch feat\"). " + R("4주 p21, p32, p33") + "</p>")],
quote=quote("It is special in exactly one way: it has two parents", "원본 4주 p33")))

# 5 ------------------------------------------------------------
mr_q, mr_a = fill(["비교", "merge", "rebase"], [
    ["하는 일", ("?", "세 스냅샷으로 새 병합 커밋을 만든다"), ("?", "내 커밋의 변경을 다른 브랜치 위에 다시 적용(복사)한다")],
    ["히스토리", ("?", "갈라짐이 영원히 남는다(실제로 일어난 기록)"), ("?", "직선이 된다(일어나지 않은 순서로 읽힘)")],
    ["원래 커밋", ("?", "그대로"), ("?", "새 해시의 복사본(C′)이 생기고 원본은 버려짐")],
    ["끝의 파일 내용", ("?", "같다(바이트 단위로 동일)"), ("?", "같다")]])
P(dict(kind=["graph", "table"], title="rebase: 결과 그래프 예측 (oss6)",
intro="oss6: C1에서 feat1, feat2가 갈라졌다. feat1은 a.md에 C2, C3, feat2는 새 파일 b.md에 C4, C5를 커밋했다. " + R("6주 p35~p41") + run("s3_before.txt", "rebase 전 그래프"),
parts=[
 dict(q="git switch feat1 후 git rebase feat2 를 실행하면 그래프는 어떻게 되는가? 커밋은 몇 개가 보이고, 갈라짐이 남는가? C2, C3은 어떻게 되는가?",
      a=run("s3_after_rebase.txt", "git rebase feat2 후 실제 그래프") + "C2, C3의 변경이 C5 위에 <b>다시 적용되어 C2′, C3′</b>이 되고 히스토리는 <b>한 줄</b>이 된다. 보이는 커밋은 다섯 개(C1, C4, C5, C2′, C3′)이고 갈라짐이 없다. C2′, C3′은 부모가 바뀌었으므로 <b>새 해시</b>를 갖는다(위 출력의 C2, C3 해시가 rebase 전과 다름). 원래 C2, C3은 지워지지 않고 <b>아무 브랜치도 가리키지 않게</b> 되며, <code>git reflog</code>로 볼 수 있다. " + R("6주 p14, p40"),
      why="<p>rebase는 커밋을 옮기지 않는다. <b>복사본을 만들고 원본을 버린다</b>. 그래서 C′ 표시가 붙는다. 이어서 git switch feat2, git merge feat1 을 하면 feat2가 feat1 바로 뒤에 있으므로 fast-forward가 되고, master도 같은 방법으로 따라오면 세 브랜치가 모두 C3′에서 끝난다. rebase의 목적이 직선이므로 이때는 --no-ff를 쓰지 않는다. " + R("6주 p15, p41") + "</p>" + run("s3_final.txt", "feat2·master까지 fast-forward한 최종 그래프")),
 dict(q="rebase의 golden rule은 무엇이며, 왜 지켜야 하는가?",
      a="<b>저장소 밖에 이미 존재하는(push한) 커밋은 rebase하지 않는다.</b> rebase는 새 해시의 복사본을 만들고 원본을 버리므로, 이미 push해서 팀원이 원본을 가지고 있으면 두 사람의 히스토리가 달라진다. 내 push는 거절되고, --force로 밀면 팀원이 다시 pull할 때 지운 커밋이 되살아나 <b>같은 변경이 두 번</b>(C4와 C4′) 히스토리에 생긴다. 판단 질문: \"이 커밋을 다른 사람이 본 적이 있나?\" 있으면 merge를 쓴다. " + R("6주 p18")),
 dict(q="merge와 rebase를 비교하는 표를 채우시오." + mr_q, a=mr_a + R("6주 p13, p14, p16"))],
fig=fig("6주", 14, 62),
quote=quote("Never rebase commits you have already pushed.", "원본 6주 p14")))

# 6 ------------------------------------------------------------
rs_q, rs_a = fill(["git reset 옵션", "브랜치 포인터", "스테이징 영역", "내 파일(작업 디렉터리)", "언제 쓰나"], [
    ["--soft", ("?", "뒤로 이동"), ("?", "유지"), ("?", "유지"), ("?", "커밋을 다시 하되 모두 staged 상태로, 메시지 다시 쓰기")],
    ["--mixed (기본값)", ("?", "뒤로 이동"), ("?", "비움"), ("?", "유지"), ("?", "커밋을 다시 하되 무엇을 넣을지 다시 고르기")],
    ["--hard", ("?", "뒤로 이동"), ("?", "비움"), ("?", "덮어씀(변경 사라짐)"), ("?", "작업을 완전히 버리기")]])
rv_q, rv_a = fill(["비교", "reset", "revert"], [
    ["하는 일", ("?", "브랜치 포인터를 뒤로 옮긴다"), ("?", "옛 커밋을 되돌리는 새 커밋을 추가한다")],
    ["히스토리", ("?", "다시 쓰임 — 커밋이 사라짐"), ("?", "보존 — 히스토리가 늘어남")],
    ["push한 뒤에도 안전?", ("?", "아니오"), ("?", "예")],
    ["쓰는 곳", ("?", "아직 push하지 않은 내 로컬의 실수"), ("?", "다른 사람이 이미 pull한 것")]])
P(dict(kind=["table", "essay"], title="reset인가 revert인가, 왜 (출제 예시)",
intro="main에 C1, C2, C3(각각 a.txt에 한 줄)이 있고, 마지막 커밋 C3을 되돌리려 한다.",
parts=[
 dict(q="git reset 의 세 옵션이 무엇을 바꾸는지 표를 채우시오. (아래 실제 실행 결과로 확인)" + rs_q,
      a=rs_a + R("6주 p22") + run("s4_reset_soft.txt", "--soft: C3 커밋은 사라지고 변경은 staged(M 왼쪽 칸)") + run("s4_reset_mixed.txt", "--mixed: 변경은 남고 unstaged(M 오른쪽 칸)") + run("s4_reset_hard.txt", "--hard: 변경까지 사라짐(a.txt에 C3 줄 없음, status 깨끗)"),
      why="<p>세 옵션 모두 브랜치 포인터를 뒤로 옮기는 것은 같다. <b>--hard만 커밋하지 않은 작업을 묻지도 않고 지운다</b>. 다른 둘은 포인터만 옮기고 변경은 모두 남긴다. 옵션 없이 쓴 git reset HEAD~1 은 --mixed다. " + R("6주 p22, p23") + "</p>"),
 dict(q="reset과 revert를 비교하는 표를 채우시오." + rv_q,
      a=rv_a + R("6주 p24") + run("s4_revert.txt", "git revert HEAD 실제 결과: C3은 남고 그것을 되돌리는 새 커밋이 위에 생김")),
 dict(q="[서술형] 팀원이 이미 pull한 커밋 C3에 버그가 있다. reset과 revert 중 무엇을 쓰고, 왜 그런지 쓰시오. 반대로 아직 push하지 않은 내 커밋이라면? (두괄식)",
      a="<b>모범 답안</b> 이미 팀원이 pull한 C3은 <b>git revert C3</b>으로 되돌려야 한다. revert는 C3을 지우지 않고 C3의 변경을 거꾸로 적용하는 새 커밋을 더하므로 히스토리가 다시 쓰이지 않고, 팀원의 Git과 내 Git이 같은 히스토리를 유지한다. 반면 reset은 브랜치 포인터를 뒤로 옮겨 C3을 히스토리에서 없애므로, 이미 C3을 가진 팀원과 히스토리가 어긋나 push가 거절되고 강제로 밀면 팀원의 작업을 망가뜨린다. 아직 push하지 않은 내 로컬 커밋이라면 아무도 C3을 본 적이 없으므로 <b>git reset HEAD~1</b>(변경 유지) 또는 git reset --hard HEAD~1(변경 버림)로 깔끔하게 지워도 된다. 결국 선택 기준은 \"이 커밋을 다른 사람이 본 적이 있는가?\" 하나다. " + R("6주 p24, 7주 p7") + "<br><b>채점 체크</b> □ 결론(revert) 먼저 □ revert는 새 커밋을 더함·히스토리 보존 □ reset은 히스토리를 다시 씀 □ 기준 질문 □ 반대 경우(reset)",
      why="<p>교수는 \"어느 쪽이 더 좋으냐가 아니라, 다른 사람이 이 커밋을 봤느냐가 명령을 고른다\"고 정리했다. 서술형에는 이 기준 문장을 그대로 넣는다. " + R("6주 p24") + "</p>")],
fig=fig("6주", 24, 62),
quote=quote("Only --hard destroys uncommitted work, and it destroys it without asking.", "원본 6주 p22")))

# 7 ------------------------------------------------------------
sc_q, sc_a = fill(["상황", "꺼낼 명령"], [
    ["커밋 메시지를 잘못 썼다(아직 push 안 함)", ("?", "git commit --amend -m \"새 메시지\"")],
    ["마지막 커밋에 파일 하나를 빠뜨렸다(push 안 함)", ("?", "git add &lt;파일&gt; 후 git commit --amend")],
    ["엉뚱한 파일을 staged에 올렸다", ("?", "git restore --staged &lt;파일&gt; (예전: git reset HEAD &lt;파일&gt;)")],
    ["마지막 커밋을 취소하되 수정 내용은 남기고 싶다", ("?", "git reset HEAD~1")],
    ["마지막 커밋 이후 변경을 모두 버리고 싶다", ("?", "git reset --hard (확인 창 없음)")],
    ["다른 사람이 이미 pull한 커밋을 되돌려야 한다", ("?", "git revert &lt;커밋&gt;")],
    ["미완성 작업을 둔 채 급히 다른 브랜치로 가야 한다", ("?", "git stash (돌아와서 git stash pop)")],
    ["reset·amend·rebase로 잃어버린 커밋을 찾고 싶다", ("?", "git reflog (해시를 찾아 git branch rescue &lt;해시&gt;)")],
    ["파일은 디스크에 두고 Git 추적만 그만두고 싶다", ("?", "git rm --cached &lt;파일&gt;")],
    ["staged 전 변경 / staged된 변경을 보고 싶다", ("?", "git diff / git diff --staged")],
    ["브랜치를 만들고 바로 이동하고 싶다", ("?", "git switch -c &lt;이름&gt; (= git checkout -b &lt;이름&gt;)")],
    ["병합하다 충돌이 나서 병합 전으로 돌아가고 싶다", ("?", "git merge --abort")],
    ["병합 커밋을 반드시 남기고 싶다", ("?", "git merge --no-ff &lt;브랜치&gt;")],
    ["새 브랜치를 GitHub에 처음 올린다", ("?", "git push -u origin &lt;브랜치&gt;")],
    ["병합이 끝난 브랜치를 지운다", ("?", "git branch -d &lt;이름&gt;")],
    ["모든 브랜치의 히스토리를 그림으로 본다", ("?", "git log --oneline --graph --all")]])
P(dict(kind=["cmd", "table"], title="상황 → 명령·옵션 (교수의 \"Which one do I use?\" 표 + 3·4주 명령표)",
parts=[
 dict(q="상황에 맞게 꺼낼 명령(옵션 포함)을 쓰시오." + sc_q, a=sc_a + R("6주 p27, p47, 4주 p41, 3주 p34"),
      why="<p>옵션이 핵심인 명령: <b>--amend</b>(마지막 커밋 교체), <b>--staged</b>(restore·diff에서 staging 영역), <b>--cached</b>(rm에서 추적만 해제), <b>--hard</b>(파일까지), <b>-c</b>(switch에서 만들며 이동), <b>--no-ff</b>(병합 커밋 강제), <b>-u</b>(push에서 upstream 설정, 이후 git push만 쳐도 됨), <b>--abort</b>(병합·rebase 취소). " + R("3주 p32, 4주 p41, 6주 p47") + "</p>"),
 dict(q="git commit --amend 에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("마지막 커밋에 새 커밋을 덧붙이지 않고 마지막 커밋을 교체한다.", True, "--amend는 새 커밋을 추가하지 않고 마지막 커밋을 바꿔 친다. " + R("6주 p20")),
            ("원래 커밋을 그 자리에서 고치므로 해시가 그대로다.", False, "옛 커밋을 고치는 것이 아니라 새 해시를 가진 새 커밋으로 교체한다. 그래서 --amend도 히스토리 재작성이다. " + R("6주 p20")),
            ("이미 push한 커밋을 amend하면 다음 push가 거절될 수 있다.", True, "amend는 히스토리를 다시 쓰므로 golden rule이 적용되고, 이미 push한 커밋을 amend하면 다음 push가 거절된다. 그 거절은 팀원을 보호하는 장치다. " + R("6주 p20")),
            ("빠뜨린 파일을 git add 로 올린 뒤 --amend 하면 그 파일이 마지막 커밋에 들어간다.", True, "빠뜨린 파일을 staged에 올리고 --amend로 다시 커밋하면 마지막 커밋에 포함된다. 실습에서는 git add oss/d.md 후 git commit --amend -m \"C6\" 으로 메시지와 파일을 한 번에 고쳤다. " + R("6주 p20, p43"))],
      a="ⓐ ⓒ ⓓ")],
fig=fig("6주", 27, 60),
quote=quote("Those commits are not deleted. They are only unreachable — no branch points at them.", "원본 6주 p26")))

# 8 ------------------------------------------------------------
st_q, st_a = fill(["순서", "명령(동작)", "notes.txt의 상태"], [
    ["1", "새 파일 notes.txt를 만든다", ("?", "untracked")],
    ["2", "git add notes.txt", ("?", "staged (추적 시작 + 다음 커밋에 들어갈 내용으로 표시)")],
    ["3", "git commit -m \"Add notes\"", ("?", "committed (= tracked, unmodified)")],
    ["4", "notes.txt를 수정한다", ("?", "modified (아직 staged 아님)")],
    ["5", "git add notes.txt", ("?", "staged")],
    ["6", "git rm --cached notes.txt", ("?", "다시 untracked (파일은 디스크에 남고 추적만 해제, 제거가 staged됨)")]])
P(dict(kind=["table", "name"], title="세 상태와 세 영역: 명령마다 파일은 어디로 가나",
parts=[
 dict(q="Git에서 파일의 세 상태와 프로젝트의 세 영역의 이름을 쓰시오. 기본 작업 흐름 세 단계는?",
      a="<b>세 상태</b>: modified(바꿨지만 아직 커밋 안 함) / staged(바뀐 파일의 현재 버전을 다음 커밋에 넣기로 표시) / committed(로컬 데이터베이스에 안전하게 저장). <b>세 영역</b>: working directory(실제로 편집하는 파일) / staging area(다음 커밋에 들어갈 것을 담는 바구니) / .git directory(메타데이터와 객체 데이터베이스, 저장소 자체). <b>기본 흐름</b>: modify → stage → commit. " + R("3주 p11~p13"),
      why="<p>staging area가 있는 이유는 바꾼 것을 몽땅 커밋하지 않고 <b>커밋에 넣을 것을 고르기</b> 위해서다. 새 파일은 git add 하기 전까지 항상 untracked이며, git add는 \"추적 시작\"과 \"변경을 staged로\" 두 일을 한다. " + R("3주 p12, p18, p22") + "</p>"),
 dict(q="다음 순서대로 했을 때 notes.txt의 상태를 채우시오." + st_q, a=st_a + R("3주 p11, p18, p22, p25"),
      why="<p>git commit 은 <b>staged된 것만</b> 기록한다. 수정만 하고 git add 하지 않은 변경은 커밋에 들어가지 않는다. git rm 은 파일을 지우고 그 삭제를 staged로 올리고, git rm --cached 는 파일은 두고 추적만 그만둔다. " + R("3주 p23, p25") + "</p>")],
quote=quote("staged — you marked the modified file, in its current version, to go into the next commit", "원본 3주 p11")))

# 9 ------------------------------------------------------------
P(dict(kind=["diag", "order"], title="충돌(conflict) 읽고 끝내기",
intro="master와 fix-b가 a.md의 <b>같은 줄</b>을 서로 다르게 바꾼 상태에서 master에 fix-b를 병합했다. " + R("4주 p53~p56") + run("s5_conflict.txt", "git merge fix-b 실제 출력과 파일 내용"),
parts=[
 dict(q="Git은 언제 자동 병합을 멈추는가? 위 파일에서 <code>=======</code> 위와 아래는 각각 어느 쪽 내용인가?",
      a="두 쪽이 <b>같은 파일의 같은 줄</b>을 바꿨을 때만 멈춘다(다른 곳을 고쳤으면 자동 병합). 이것은 오류가 아니라 어느 쪽을 원하는지 Git이 추측하지 않는 것이다. <code>=======</code> <b>위(&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD ~)는 지금 서 있는 브랜치(master)</b>, <b>아래(~ &gt;&gt;&gt;&gt;&gt;&gt;&gt; fix-b)는 병합해 들어오는 브랜치</b>의 내용이다. " + R("4주 p38, p39")),
 dict(q="충돌을 해결하고 병합을 끝내는 순서를 쓰시오. 병합을 아예 취소하려면?",
      a=cmd("""# 1. 파일을 원하는 내용으로 고치고 <<<<<<< ======= >>>>>>> 줄을 모두 지운다
git add oss/a.md      # 2. 해결한 파일을 stage
git commit            # 3. -m 없이: Git이 써 둔 병합 메시지가 열림
# 병합 자체를 취소: git merge --abort""") + "한쪽만 고르거나 둘 다 남겨도 되지만 <b>표시 줄을 남겨서는 안 된다</b>(그대로 커밋되어 코드가 깨진다). 아직 해결 안 된 파일은 git status 가 알려 준다(위 출력의 <code>UU</code>). " + R("4주 p39, p40"),
      why="<p>fast-forward는 충돌할 수 없고 three-way merge만 충돌할 수 있다. 충돌 중 git merge --abort 는 저장소를 병합 시작 전 상태로 정확히 되돌린다. " + R("4주 p34, p40") + "</p>")],
quote=quote("It stops only when both sides changed the same lines of the same file", "원본 4주 p38")))

# 10 -----------------------------------------------------------
P(dict(kind=["mc", "order"], title="GitHub Flow · Issue · Pull Request",
parts=[
 dict(q="이 수업이 쓰는 GitHub Flow의 규칙 하나와 6단계를 순서대로 쓰시오.",
      a="규칙: <b>main은 언제나 배포 가능하고, pull request를 거치지 않고는 아무것도 main에 들어가지 않는다.</b> 6단계: <b>Branch → Commit → Open PR → Discuss → Approve → Merge</b>(main에서 작업 하나당 브랜치 하나 → push 전까지 로컬 → \"이것을 main에 넣자\" 제안 → 리뷰 댓글과 추가 커밋 → 리뷰어 승인 → main에 병합하고 브랜치 삭제). " + R("7주 p16")),
 dict(q="GitHub의 Issue와 Pull Request에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("Issue #1, #2를 연 뒤 처음 여는 Pull Request의 번호는 #3이다.", True, "Issue와 PR은 하나의 번호 순서를 함께 쓰므로 #1, #2 다음 PR은 #3이다. 번호는 다시 쓰이지 않는다. " + R("7주 p18, p22")),
            ("저장소를 clone하면 issue와 pull request도 함께 내려받는다.", False, "Issue와 PR은 GitHub의 데이터베이스에 있고 .git에 없으므로, clone하면 커밋과 브랜치만 받고 issue는 받지 못한다. " + R("7주 p14, p18")),
            ("PR 본문에 \"Closes #1,#4\"라고 쓰면 #1과 #4가 모두 닫힌다.", False, "\"Closes #1,#4\"는 #1만 닫는다. 둘 다 닫으려면 \"Closes #1, closes #4\"처럼 번호마다 키워드를 붙인다. " + R("7주 p23")),
            ("PR의 base는 받는 브랜치(보통 main), compare는 주는 브랜치(내 작업)다.", True, "PR은 compare 브랜치를 base 브랜치에 병합해 달라는 요청이고, 화살표는 compare에서 base로 향한다. " + R("7주 p22")),
            ("자기 PR을 스스로 승인(Approve)할 수 없다.", True, "GitHub은 자기 PR 승인을 막는다. 그래서 실습은 두 사람이 서로의 PR을 리뷰했다. " + R("7주 p24")),
            ("PR을 연 뒤 같은 브랜치에 커밋을 더 push하면 PR이 자동으로 갱신된다.", True, "PR은 커밋이 아니라 브랜치를 따라가므로, 같은 브랜치에 push하면 PR이 스스로 갱신된다. 리뷰 반영은 이렇게 한다. " + R("7주 p22, p25"))],
      a="ⓐ ⓓ ⓔ ⓕ",
      why="<p>닫기 키워드는 close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved이고 대소문자는 상관없다. 기본 브랜치(main)에 병합될 때만 issue가 자동으로 닫히며, 기본 브랜치가 아닌 곳으로의 병합은 자동으로 닫지 않는다. " + R("7주 p23") + "</p>")],
quote=quote("You cannot approve your own pull request", "원본 7주 p24")))

# 11 -----------------------------------------------------------
pm_q, pm_a = fill(["main 보호 규칙(Settings → Branches)", "막는 것"], [
    ["Require a pull request before merging", ("?", "git push origin main 이 거절된다. 모든 변경은 PR을 거친다")],
    ["Require approvals (1~2)", ("?", "다른 사람이 승인하기 전까지 Merge 버튼이 꺼져 있다(자기 승인 불가)")],
    ["Require status checks to pass", ("?", "테스트가 실패한 PR은 병합할 수 없다")],
    ["Block force pushes", ("?", "main에 대한 force push를 거절한다")],
    ["Do not allow bypassing", ("?", "관리자에게도 규칙을 적용한다(기본은 꺼짐)")]])
mb_q, mb_a = fill(["병합 버튼", "비슷한 git 개념", "main의 모양", "원래 해시가 남나?"], [
    ["Create a merge commit", ("?", "git merge --no-ff"), ("?", "부모가 둘인 합류점"), ("?", "예")],
    ["Squash and merge", ("?", "git rebase -i 로 squash 후 fast-forward"), ("?", "PR마다 새 커밋 하나"), ("?", "아니오(하나로 접힘)")],
    ["Rebase and merge", ("?", "git rebase 후 fast-forward"), ("?", "직선, 커밋은 모두 남음(복사본)"), ("?", "아니오")]])
P(dict(kind=["table", "mc"], title="main 보호 · 병합 버튼 3종 · 협업 모델 2가지",
parts=[
 dict(q="main 보호 규칙이 각각 무엇을 막는지 채우시오. 보호된 main에 직접 push하면 어떤 오류가 나오는가?" + pm_q,
      a=pm_a + "보호된 main에 git push origin main 을 하면 <b>GH006: Protected branch</b> 오류로 거절된다. " + R("7주 p27, p47")),
 dict(q="GitHub의 병합 버튼 세 가지를 비교하시오. (이 수업의 기본은 Create a merge commit)" + mb_q, a=mb_a + R("7주 p26")),
 dict(q="두 협업 모델에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("Shared repository에서는 소유자가 Settings → Collaborators로 팀원을 초대하고, 초대를 수락해야 push할 수 있다.", True, "공유 저장소 모델은 여러 사람이 쓰기 권한을 갖고, 초대받은 사람이 수락하지 않으면 push가 거절된다. 이 수업의 팀 프로젝트가 이 모델이다. " + R("7주 p30")),
            ("Shared repository에서는 각자 main에 직접 push하는 것이 원칙이다.", False, "공유 저장소에서도 각자 자기 브랜치를 push하고 PR을 연다. 새 규칙은 \"main에 절대 push하지 않는다\"이다. " + R("7주 p30")),
            ("Fork 모델은 쓰기 권한이 없을 때, 저장소를 내 계정으로 복사(fork)해 작업하고 원본(upstream)에 PR을 보내는 방식이다.", True, "fork를 clone해 브랜치·커밋·push를 내 fork에 하고, 내 fork에서 upstream으로 PR을 연다. upstream에는 직접 push하지 않는다. " + R("7주 p31")),
            ("fork는 원본이 바뀌면 자동으로 따라간다.", False, "fork는 복사한 시점에서 멈춘다. upstream이라는 이름의 remote를 더해 정기적으로 동기화해야 한다. " + R("7주 p31"))],
      a="ⓐ ⓒ")],
quote=quote("main is always deployable, and nothing reaches main except through a pull request.", "원본 7주 p16")))

# 12 -----------------------------------------------------------
P(dict(kind=["mc", "name"], title="2주차 한 쪽 요약: OSS · open weight · 라이선스 · Git과 GitHub",
parts=[
 dict(q="오픈소스 라이선스가 사용자에게 주는 네 가지 권리를 쓰시오. open weight 모델과 (완전한 의미의) open source 모델의 차이는?",
      a="<b>Use</b>(어떤 목적으로든 사용) · <b>Study</b>(어떻게 동작하는지 읽기) · <b>Change</b>(필요에 맞게 수정) · <b>Distribute</b>(수정했든 안 했든 공유). " + R("2주 p4") + " <b>open weight</b>는 학습된 모델(가중치)을 내려받아 실행·fine-tune할 수 있지만 무엇으로 학습했는지 볼 수 없고 처음부터 재현할 수 없다(널리 알려진 모델 대부분). <b>open source</b>는 코드, 가중치, 학습 데이터에 대한 정보까지 모두 공개되어 원칙적으로 다른 사람이 다시 만들 수 있다(훨씬 드묾). " + R("2주 p22, p23")),
 dict(q="2주차 내용에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("MIT, Apache, BSD는 거의 모든 사용을 허락하는 permissive 라이선스이고, Apache는 특허 권리도 준다.", True, "permissive 라이선스(MIT, Apache, BSD)는 거의 모든 사용을 허락하며, Apache는 특허 권리도 부여한다. " + R("2주 p25")),
            ("GPL은 파생 저작물도 같은 라이선스로 공개하도록 요구하는 copyleft 라이선스다.", True, "copyleft인 GPL은 파생 저작물에 같은 라이선스를 요구하고, AGPL은 이를 네트워크로 제공되는 소프트웨어까지 넓힌다. " + R("2주 p25")),
            ("Git과 GitHub는 같은 것이다.", False, "Git은 내 컴퓨터에 설치하는 프로그램(파일 히스토리 기록)이고, GitHub는 Git 저장소를 호스팅하는 웹사이트다. GitLab, Bitbucket도 Git 저장소를 호스팅한다. " + R("2주 p29")),
            ("Git은 분산 버전 관리 시스템이라, 내 컴퓨터에 최신 버전만 있고 히스토리는 서버에만 있다.", False, "분산(distributed)이란 모든 사본이 완전하다는 뜻이다. 내 컴퓨터가 전체 히스토리를 가지며, 대부분의 Git 작업은 인터넷 없이 로컬에서 된다. " + R("2주 p28, 3주 p7")),
            ("AI에서는 코드, 모델 가중치, 데이터셋에 각각 다른 라이선스가 붙을 수 있고 세 가지를 모두 지켜야 한다.", True, "AI에서는 코드·가중치·데이터셋 세 라이선스가 동시에 적용될 수 있고, 모두 만족해야 하며 서로 맞지 않을 때도 있다. " + R("2주 p25"))],
      a="ⓐ ⓑ ⓔ")],
quote=quote("Code, weights, and information about the training data are all released", "원본 2주 p23")))

KEYWORDS = [
 ("branch", "커밋 ID 하나를 담은 41바이트 파일. 커밋을 가리키는 포인터", "원본 4주 p15"),
 ("HEAD", "지금 서 있는 브랜치를 가리킴(커밋이 아니라 브랜치)", "원본 4주 p17"),
 ("parent", "각 커밋이 가리키는 바로 앞 커밋. 병합 커밋은 부모가 둘", "원본 4주 p12"),
 ("fast-forward", "받는 브랜치가 움직이지 않았을 때 포인터만 앞으로 미는 병합. 새 커밋 없음", "원본 4주 p30"),
 ("three-way merge", "공통 조상과 두 끝, 세 스냅샷으로 새 병합 커밋을 만드는 병합", "원본 4주 p32"),
 ("--no-ff", "fast-forward가 가능해도 병합 커밋을 강제로 만드는 merge 옵션", "원본 4주 p35"),
 ("conflict", "두 쪽이 같은 파일의 같은 줄을 바꿨을 때 Git이 병합을 멈추는 것", "원본 4주 p38"),
 ("rebase", "내 커밋의 변경을 다른 브랜치 위에 다시 적용(새 해시의 복사본)", "원본 6주 p14"),
 ("golden rule of rebasing", "저장소 밖에 존재하는(push한) 커밋은 rebase하지 않는다", "원본 6주 p18"),
 ("git commit --amend", "마지막 커밋을 새 커밋으로 교체(히스토리 재작성)", "원본 6주 p20"),
 ("git restore --staged", "파일을 staging 영역에서만 빼기(예전: git reset HEAD &lt;file&gt;)", "원본 6주 p21"),
 ("git reset --soft / --mixed / --hard", "포인터만 / 포인터+staging 비움 / 포인터+staging+파일까지 덮어씀", "원본 6주 p22"),
 ("git revert", "옛 커밋을 되돌리는 새 커밋을 추가(히스토리 보존, push 후에도 안전)", "원본 6주 p24"),
 ("git stash / git stash pop", "변경을 서랍에 넣어 두기 / 다시 꺼내기", "원본 6주 p25"),
 ("git reflog", "HEAD가 있었던 모든 위치의 기록. 잃어버린 커밋을 찾는 안전망(로컬, 약 90일)", "원본 6주 p26"),
 ("git rm --cached", "파일은 두고 추적만 그만두기", "원본 3주 p25"),
 ("git push -u origin &lt;branch&gt;", "브랜치를 처음 올리며 upstream 설정(이후 git push만)", "원본 3주 p32"),
 ("modified / staged / committed", "파일의 세 상태", "원본 3주 p11"),
 ("working directory / staging area / .git directory", "Git 프로젝트의 세 영역", "원본 3주 p12"),
 ("GitHub Flow", "Branch → Commit → Open PR → Discuss → Approve → Merge", "원본 7주 p16"),
 ("base / compare", "PR에서 받는 브랜치 / 주는 브랜치", "원본 7주 p22"),
 ("Closes #1", "PR 본문의 닫기 키워드. 기본 브랜치에 병합될 때 issue를 닫음", "원본 7주 p23"),
 ("GH006: Protected branch", "보호된 main에 직접 push했을 때의 거절 오류", "원본 7주 p47"),
 ("upstream", "fork 모델에서 원본 저장소(동기화용 remote 이름)", "원본 7주 p31"),
 ("open weight", "가중치는 공개, 학습 데이터·재현은 불가", "원본 2주 p23"),
 ("permissive / copyleft", "MIT·Apache·BSD / GPL·AGPL(파생물도 같은 라이선스)", "원본 2주 p25"),
]

OUTRO = """
<h3>핵심본에 넣은 것과 근거</h3>
""" + table(["문제", "주제", "근거(출제 단서)"], [["1~4", "브랜치·HEAD, ff vs 3-way, 그래프↔명령", "출제 예시 ②, 4주 p15~p43(6주 recap)"], ["5", "rebase 결과 예측·golden rule", "6주 p12~p18, p35~p41(7주 recap)"], ["6", "reset vs revert와 이유", "출제 예시 ③, 6주 p22~p24(7주 recap)"],
 ["7", "상황→명령·옵션", "출제 예시 ①, 6주 p27·p47, 4주 p41, 3주 p34"], ["8", "세 상태·세 영역", "3주 p11~p13(4주 recap)"], ["9", "충돌", "4주 p38~p40"], ["10~11", "GitHub 협업", "7주"], ["12", "OSS·라이선스", "2주"]]) + """
<div class="note"><b>상세본으로 미룬 것</b>: OSS 역사 연표(UNIVAC·ARPANET·UNIX·GNU·Linux·LAMP), AI 모델 라이선스 표, 회사·학생이 OSS를 쓰는 이유와 단점, Git 객체(blob·tree·commit), SHA-1, git config, .gitignore 패턴, issue 작성 양식·label·milestone, 실습 단계별 절차.</div>
<div class="note"><b>원본 표기·빈틈</b>: 3주 p16 "git config –-list"의 앞 하이픈이 대시(–)로 찍힘 <span class="fix">→ git config --list</span> / 7주 p31 "sync regularly (next slide)"라고 했지만 다음 쪽이 Lab이라 upstream 동기화 방법은 원본에 없음 / 6주 p10 "오늘 할 것"의 cherry-pick은 설명 슬라이드가 없음.</div>
<div class="note"><b>확인 범위</b>: 그래프·reset·revert·충돌의 출력은 임시 연습 저장소에서 git 2.x로 실제 실행한 결과다(runs/). 실습 그림과 커밋 이름은 같고 해시는 실행마다 다르다. git commit -am 은 이미 추적 중인 파일의 수정만 담으므로, 새 파일은 먼저 git add 해야 한다.</div>
"""
