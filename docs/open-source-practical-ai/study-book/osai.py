"""오픈소스실전인공지능 학습본 공용 도우미. 조판은 시스템설계방법론의 qbook2를 그대로 쓴다.

- R(): 근거 쪽수 표시  - fig(): 원본 슬라이드(한 쪽에 1장)를 통째로 잘라 그림으로  - run(): runs/의 실제 git 실행 출력
- runs/*.txt 는 임시 연습 저장소에서 실제 git으로 실행해 저장한 출력이다(손으로 옮기지 않는다).
"""
import html, os, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "system-design-methodology" / "study-book"))
import qbook2
from qbook2 import quote, table, fill  # noqa: F401  (장 모듈이 여기서 가져다 쓴다)

SRC = Path(os.environ["USERPROFILE"]) / "Downloads" / "오픈소스실전인공지능"
WEEK = {"2주": "week02", "3주": "week03", "4주": "week04", "6주": "week06", "7주": "week07"}

qbook2.CSS += """
pre.out { font-family: Consolas, 'Malgun Gothic', monospace; font-size: 8pt; line-height: 1.25; border: 0.6pt solid #888; padding: 3pt 5pt; margin: 3pt 0; white-space: pre; break-inside: avoid; }
.cap { display:block; font-size: 7.4pt; color:#666; margin-top: 1pt; }
"""


def pdf(week):
    return next(SRC.glob(WEEK[week] + "*.pdf"))


def R(where):
    return f'<span class="kwa">(원본 {where})</span>'


def fig(week, page, width=70):
    import pymupdf
    out = qbook2.BUILD / f"osai_{WEEK[week]}_p{page}.png"
    if not out.exists():
        pg = pymupdf.open(pdf(week))[page - 1]
        r = pg.rect
        pg.get_pixmap(dpi=120, clip=pymupdf.Rect(0, r.height * 0.03, r.width, r.height * 0.95)).save(out)
    return f'<div class="fig"><img src="{out.as_uri()}" style="width:{width}%"><span class="src">원본 {week} p{page} 원본 그림</span></div>'


def cmd(text):
    """정답으로 쓰는 명령 묶음."""
    return f'<pre class="out">{html.escape(text.strip())}</pre>'


def run(name, label="실제 실행 출력"):
    text = (HERE / "runs" / name).read_text(encoding="utf-8").rstrip()
    return f'<pre class="out">{html.escape(text)}</pre><span class="cap">{label} (runs/{name}, 해시는 실행마다 다름)</span>'
