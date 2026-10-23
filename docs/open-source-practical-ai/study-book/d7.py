"""상세본 5장 (7주) — GitHub 협업. 핵심본 문제 10(GitHub Flow·Issue/PR 함정)과 11(main 보호·병합 버튼·협업 모델)은 다시 묻지 않는다."""
from osai import R, fig, cmd, run, quote, table, fill

INTRO = """
<div class="note"><b>상세본</b> — 7주차(GitHub Collaboration Workflow). GitHub Flow 6단계, issue·PR 번호와 닫기 키워드, main 보호 규칙, 병합 버튼, shared/fork는 핵심본 문제 10·11에 있다. 여기서는 그 밖의 협업 개념과 실습(계산기) 흐름을 다룬다.</div>
<h2>상세 5장. 7주 — GitHub 협업 워크플로</h2>
"""

ITEMS = []
P = ITEMS.append

# 1 ------------------------------------------------------------
tw_q, tw_a = fill(["상황", "벌어지는 일", "왜 아픈가"], [
    ["둘 다 main에 각자 커밋하고 push", ("?", "두 번째 push가 거절됨(fast forward가 아님)"), ("?", "진 사람이 혼자 pull·병합·충돌 해결. 다른 사람은 그 과정을 못 봄")],
    ["진 사람이 git push --force", ("?", "main에서 다른 사람의 커밋이 사라질 수 있음"), ("?", "보호가 없으면 Git이 허락할 수 있음")],
    ["둘 다 조심해서 충돌 없음", ("?", "아무도 읽지 않은 코드가 main에 들어감"), ("?", "한 달 뒤 왜 그렇게 썼는지 아무도 모름")]])
P(dict(kind=["table", "diag"], title="두 사람, 저장소 하나: 무엇이 잘못되나",
parts=[
 dict(q="두 사람이 저장소 하나에서 보호 없이 일할 때 생기는 일을 채우시오. 빠진 것은 명령인가?" + tw_q,
      a=tw_a + "빠진 것은 명령이 아니라 <b>합의</b>(누가 어디에 쓰고, 언제 병합하며, 병합 전에 누가 보는가)다. GitHub는 이 합의를 구조로 만든다: <b>브랜치 = 어디에(where), PR = 언제·누가(when and who), Issue = 무엇을(what)</b>. " + R("7주 p15")),
 dict(q="Git과 GitHub는 무엇이 다른가? 대화(Issue, PR, 리뷰)는 어디에 저장되나?",
      a="<b>Git은 도구</b>(내 컴퓨터의 프로그램: 스냅샷·브랜치·병합·히스토리, 로컬 작업에 네트워크 불필요)이고, <b>GitHub는 장소</b>(Git 저장소를 호스팅하는 웹 서비스: 누가 읽고 쓸지 사람을 관리하고, Issue·PR·리뷰 같은 대화를 저장소에 붙임)다. 대화는 <b>.git에 없고 GitHub의 데이터베이스</b>에 있다. " + R("7주 p14"))],
quote=quote("The missing piece is not a command. It is an agreement", "원본 7주 p15")))

# 2 ------------------------------------------------------------
is_q, is_a = fill(["", "Bug report", "Feature request"], [
    ["제목", ("?", "무엇이 잘못됐는지 한 줄 (예: README link returns 404)"), ("?", "원하는 것 한 줄 (예: Add a CONTRIBUTING guide)")],
    ["본문에 꼭 있어야 할 것", ("?", "Expected behavior, Actual behavior, Steps to reproduce, Environment(OS, version)"), ("?", "먼저 부딪힌 문제, 제안하는 변경, 검토한 대안")],
    ["가장 중요한 줄", ("?", "Steps to reproduce (\"안 돼요\"는 고칠 수 없음)"), ("?", "해결책이 아니라 문제 (다른 사람이 더 나은 해결을 알 수 있음)")]])
P(dict(kind=["table", "mc"], title="Issue: 행동할 수 있게 쓰기 · Labels · Assignees · Milestones",
parts=[
 dict(q="Issue를 정의하고, 버그 보고와 기능 요청을 쓰는 법을 채우시오." + is_q,
      a="Issue는 <b>작업 단위</b>다: 버그 하나, 기능 하나, 질문 하나가 저장소에 붙은 것. " + is_a + R("7주 p18, p19"),
      why="<p>\"이슈 하나 = 작업 하나\". 이슈 하나가 브랜치 하나가 되고, 그것이 PR 하나가 된다. 목록에서 제목만 보고 이해할 수 있는 것이 가장 큰 품질 신호이고, \"Bug\"는 제목이 아니다. " + R("7주 p19") + "</p>"),
 dict(q="Issue와 그 부가 정보에 대한 설명으로 옳은 것을 모두 고르시오.",
      opts=[("issue·PR 본문의 #12는 같은 저장소 안을, owner/repo#12는 다른 저장소의 12번을 가리킨다.", True, "같은 저장소 안은 #12, 저장소를 넘어서는 owner/repo#12로 연결한다. " + R("7주 p18")),
            ("쓰기 권한이 없으면 issue를 열 수 없다.", False, "접근 권한이 있고 Issues가 켜져 있으면 보통 쓰기 권한 없이도 issue를 열 수 있다. " + R("7주 p18")),
            ("label \"good first issue\"는 오픈소스 프로젝트가 새로 온 사람을 초대하는 표시다.", True, "label은 issue의 종류(bug, enhancement, documentation, question)를 나타내고, good first issue는 처음 오는 기여자를 초대한다. " + R("7주 p20")),
            ("assignee가 없는 issue에는 기록된 담당자가 없다.", True, "assignee는 누가 하고 있는지를 나타내며, 지정되지 않은 issue에는 기록된 주인이 없다. 실습에서는 짝을 지정했다. " + R("7주 p20")),
            ("milestone은 issue를 v0.1.0 같은 목표로 묶고, GitHub가 진행 막대를 보여 준다.", True, "milestone은 issue가 속한 목표를 나타내며, 묶으면 GitHub가 진행률을 보여 준다. " + R("7주 p20"))],
      a="ⓐ ⓒ ⓓ ⓔ")],
quote=quote("One issue = one bug, one feature, or one question, attached to the repository", "원본 7주 p18")))

# 3 ------------------------------------------------------------
lf_q, lf_a = fill(["단계", "누가", "하는 일"], [
    ["Open", ("?", "Author"), ("?", "push, PR 작성, issue 연결, 리뷰 요청. 공개 저장소의 커밋은 push부터 보이므로 rebase하지 말고 고침 커밋을 더함")],
    ["Review", ("?", "Reviewer"), ("?", "Files changed를 읽고 줄에 댓글, 그다음 Comment / Approve / Request changes")],
    ["Revise", ("?", "Author"), ("?", "같은 브랜치에 커밋을 더 push(PR 자동 갱신), 답하고 resolve")],
    ["Approve", ("?", "Reviewer"), ("?", "승인. 필수 승인 규칙이 병합 전에 이를 강제")],
    ["Merge", ("?", "Reviewer (이 수업)"), ("?", "기본 브랜치에 병합하고 브랜치 삭제, 닫기 키워드가 issue를 닫음")]])
P(dict(kind=["table", "order"], title="Pull Request의 일생과 리뷰",
parts=[
 dict(q="PR의 일생 다섯 단계에서 누가 무엇을 하는지 채우시오." + lf_q, a=lf_a + R("7주 p25"),
      why="<p>Review와 Revise는 승인될 때까지 반복되며, 수정은 선택이다(리뷰어가 바로 승인할 수도 있다). 이 수업에서는 짝의 승인을 기다린 뒤 병합하고, <b>병합은 리뷰어</b>가 한다. 공개 저장소에서 push한 커밋은 이미 남이 볼 수 있으므로, 리뷰 반영도 rebase가 아니라 커밋을 더하는 방식으로 한다(golden rule). " + R("7주 p25, 6주 p18") + "</p>"),
 dict(q="리뷰어와 작성자가 GitHub 화면에서 하는 일을 쓰시오. 리뷰를 제출할 때 고르는 세 가지는?",
      a="<b>리뷰어</b>: 줄 옆의 + 를 눌러 댓글을 쓰고, 여러 개를 모아 한 번에 제출한다 — <b>Comment, Approve, Request changes</b> 중 하나. <b>작성자</b>: 동의하고 고치거나 왜 아닌지 설명하고, 고침을 같은 브랜치에 push한 뒤(PR 자동 갱신) 처리된 대화를 Resolve한다. " + R("7주 p24"))],
quote=quote("Review and Revise repeat until approved", "원본 7주 p25")))

# 4 ------------------------------------------------------------
P(dict(kind=["cmd", "order"], title="실습: 짝과 계산기 만들기 (한 사이클 전체)",
intro="저장소 calculator, 기능 넷(add.py, subtract.py, multiply.py, divide.py), 기능마다 issue 하나·브랜치 하나·PR 하나, 리뷰와 병합은 짝이 한다. Owner(사용자명이 알파벳순으로 앞선 사람)가 저장소를 만든다. " + R("7주 p33"),
parts=[
 dict(q="Owner가 issue #1, #2를, Partner가 #3, #4를 연 뒤 Partner가 처음 여는 PR의 번호는? 그 PR 본문에 무엇을 써야 병합 시 issue #1이 닫히는가?",
      a="PR 번호는 <b>#5</b>다(issue와 PR이 번호 순서를 함께 쓰므로). 본문에 <b>Closes #1</b>을 정확히 쓴다. 리뷰어를 지정하지 않으면 짝에게 알림이 가지 않는다. " + R("7주 p40")),
 dict(q="Partner가 두 번째 기능 #2(subtract)를 만드는 명령을 순서대로 쓰시오. (main을 최신으로 → 브랜치 → 커밋 메시지에 issue 번호 → push)",
      a=cmd("""git switch main && git pull           # 짝의 add.py가 이미 들어와 있음
git switch -c feat/subtract
# subtract.py 작성, python으로 확인 (prints 1 for (3, 2))
git add subtract.py
git commit -m "Add subtract.py (#2)"
git push -u origin feat/subtract       # -u는 첫 push에만
# 그다음 PR: base main, compare feat/subtract, 본문 "Closes #2", 리뷰어 지정""") + R("7주 p39, p46")),
 dict(q="리뷰어가 PR을 병합한 뒤 두 사람이 할 일과, 작성자만 할 일은? 네 기능을 모두 마쳤을 때 저장소의 모습은?",
      a="두 사람: <code>git switch main &amp;&amp; git pull</code>로 짝의 파일을 받는다. 작성자만: <code>git branch -d feat/add</code>로 로컬 브랜치를 지운다. 다 마치면 main에 README와 .py 네 개, issue 넷 모두 닫힘, PR 넷 모두 병합, 브랜치는 main뿐, git log --oneline --graph에 <b>병합 커밋 넷</b>(Create a merge commit을 썼으므로). " + R("7주 p43, p46")),
 dict(q="(선택 실습) main 보호 규칙을 켠 뒤 main에서 README를 고쳐 커밋하고 push했더니 GH006으로 거절됐다. 슬라이드는 이 로컬 커밋을 git reset --hard origin/main 으로 지웠다. 여기서 revert가 아니라 reset을 쓴 이유는?",
      a="그 커밋은 push가 거절되어 <b>원격에 올라간 적이 없고 아무도 본 적이 없으므로</b>, 히스토리를 다시 써도 다른 사람과 어긋날 일이 없다. 그래서 로컬 실수를 없애는 reset을 쓴다(슬라이드의 주석 \"nobody saw it\"). revert는 이미 다른 사람이 본 커밋에 쓴다. " + R("7주 p47, 6주 p24"))],
quote=quote("Do not merge your own pull request.", "원본 7주 p40")))

KEYWORDS = [
 ("Issue", "작업 단위(버그 하나, 기능 하나, 질문 하나). GitHub DB에 있고 .git에는 없음", "원본 7주 p18"),
 ("owner/repo#12", "다른 저장소의 issue·PR을 가리키는 표기", "원본 7주 p18"),
 ("Steps to reproduce", "버그 보고에서 가장 중요한 줄", "원본 7주 p19"),
 ("good first issue", "새 기여자를 초대하는 label", "원본 7주 p20"),
 ("Assignee / Milestone", "누가 하나 / 어느 목표(v0.1.0)에 속하나", "원본 7주 p20"),
 ("Comment / Approve / Request changes", "리뷰 제출 시 고르는 세 가지", "원본 7주 p24"),
 ("Resolve conversation", "처리된 리뷰 대화를 닫기", "원본 7주 p24"),
 ("Collaborators", "공유 저장소에 쓰기 권한으로 초대하는 Settings 메뉴", "원본 7주 p30"),
]

OUTRO = """<div class="note"><b>뺀 것</b>: 실습 화면 캡처(초대 수락, Compare &amp; pull request 버튼 등). <b>원본 빈틈</b>: 7주 p31 "sync regularly (next slide)"의 upstream 동기화 슬라이드가 없다. 보충하면 <code>git remote add upstream &lt;원본 주소&gt;</code> 후 <code>git pull upstream main</code>(또는 fetch 후 merge)으로 원본의 새 커밋을 받는다(원본 외).</div>"""
