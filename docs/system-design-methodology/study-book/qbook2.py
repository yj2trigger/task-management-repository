"""문제 중심 학습본 생성기.

장 모듈(chN.py)의 ITEMS(문제)·KEYWORDS(키워드)를 HTML로 만들고 Edge로 PDF 인쇄한다.
문제 = 소문제(parts)의 목록. 소문제마다 바로 뒤에 답·해설이 붙는다.
HTML과 원본 슬라이드 그림은 임시 폴더에만 만든다(저장소에는 소스만 둔다).

사용: python qbook2.py ch1 <출력.pdf> "<제목>" "<부제>"
"""
import importlib, math, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
DL = Path(os.environ["USERPROFILE"]) / "Downloads"
ORIG = {  # 원본 강의자료(한 쪽에 슬라이드 2장)
    "ppa1": DL / "ppa1_261020_235755.pdf", "ppa2": DL / "ppa2_261020_235757.pdf",
    "ppa3": DL / "ppa3_261020_235757.pdf", "ppa4": DL / "ppa4_261020_235758.pdf",
    "ppa5": DL / "ppa5_updated_261020_235758.pdf", "ppa6": DL / "ppa6_261020_235759.pdf",
}
BUILD = Path(tempfile.gettempdir()) / "pm_studybook"
BUILD.mkdir(exist_ok=True)

CSS = """
@page { size: A4 landscape; margin: 11mm 10mm 12mm 10mm; }
* { box-sizing: border-box; }
body { font-family: 'Malgun Gothic', sans-serif; font-size: 9.2pt; line-height: 1.5; color:#1d1d1d; margin:0; }
.cols { column-count: 2; column-gap: 9mm; column-rule: 0.6pt solid #bbb; }
h1 { font-size: 19pt; color:#1f6f43; margin: 0 0 2pt; }
h2 { font-size: 12.5pt; color:#1f6f43; border-bottom: 1.5pt solid #1f6f43; padding-bottom:2pt; margin: 10pt 0 6pt; break-after: avoid; }
h3 { font-size: 10.5pt; margin: 8pt 0 4pt; break-after: avoid; }
.sub { color:#555; font-size: 8.6pt; }
code { font-family: Consolas, 'Malgun Gothic', monospace; font-size: 8.6pt; }
.q { margin: 0 0 10pt; }
.qh { font-weight: bold; break-after: avoid; margin-bottom: 2pt; }
.kind { display:inline-block; font-size:7.6pt; color:#444; border:0.6pt solid #888; border-radius:2pt; padding:0 3pt; margin-right:3pt; vertical-align: 1pt; }
.intro { margin: 2pt 0; }
.qbody { background:#fcf8ee; border-left: 3pt double #555; padding: 3pt 7pt; margin: 4pt 0 2pt; break-after: avoid; }
.opts { margin: 2pt 0 0; padding: 0; list-style: none; }
.opts li { margin: 1pt 0; }
.ans { border-left: 1.2pt solid #888; padding: 2pt 7pt 2pt 7pt; margin: 2pt 0 6pt 0; }
.ans .lab { font-weight:bold; font-size: 8.4pt; color:#333; margin-right: 3pt; }
.ans ul.ox { margin: 2pt 0; padding:0; list-style:none; }
.ans ul.ox li { margin: 1pt 0; }
.ok { font-weight:bold; } .no { font-weight:bold; }
.why { border: 0.8pt dashed #888; padding: 3pt 6pt; margin: 3pt 0; }
.why ol { margin: 1pt 0 1pt 14pt; padding:0; } .why p { margin: 2pt 0; }
.trap { font-weight:bold; }
.quote { border-left: 3.5pt solid #333; padding: 2pt 6pt; margin: 4pt 0 2pt; font-size: 8.6pt; }
.src { display:block; text-align:right; color:#666; font-size: 7.6pt; }
.fig { margin: 4pt 0; text-align:center; break-inside: avoid; }
.fig img { max-width: 100%; border: 0.6pt solid #aaa; }
.note { border: 0.8pt dashed #888; padding: 4pt 6pt; margin: 4pt 0; }
.fix { color:#b00020; font-weight:bold; }
table { border-collapse: collapse; width: 100%; margin: 3pt 0; font-size: 8.6pt; }
th, td { border: 0.6pt solid #aaa; padding: 2pt 4pt; vertical-align: top; text-align: left; }
th { font-weight: bold; border-bottom: 1.2pt solid #333; }
td.filled { font-weight: bold; text-decoration: underline; text-underline-offset: 2pt; }
.blank { display:inline-block; min-width: 18mm; border-bottom: 0.8pt solid #333; }
.space { height: 5mm; }
ol.kwq { margin: 0 0 0 16pt; padding: 0; } ol.kwq li { margin: 2pt 0; break-inside: avoid; }
.kwa { color:#333; font-size: 8.4pt; }
"""

KIND = {"name": "설명→이름", "diag": "증상→원인", "order": "순서", "mc": "객관식",
        "essay": "주관식", "calc": "계산", "table": "표 채우기"}
MARKS = "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣ"


def s(*nums, deck="ppa1"):
    """슬라이드 번호 → '원본 ppa1 s25(p13 위)'. 한 쪽에 슬라이드 2장."""
    return f"원본 {deck} " + ", ".join(f"s{n}(p{math.ceil(n / 2)} {'위' if n % 2 else '아래'})" for n in nums)


def quote(text, src):
    return f'<div class="quote">{text}<span class="src">{src}</span></div>'


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{h}</tr>{b}</table>"


def fill(head, rows):
    """빈칸 표. 칸이 ('?', 답)이면 문제에서는 빈칸, 정답 표에서는 굵게 채운다. (문제표, 정답표)를 돌려준다."""
    def render(answer):
        h = "".join(f"<th>{c}</th>" for c in head)
        body = []
        for r in rows:
            cells = []
            for c in r:
                if isinstance(c, tuple):
                    cells.append(f'<td class="filled">{c[1]}</td>' if answer else "<td><span class='blank'></span></td>")
                else:
                    cells.append(f"<td>{c}</td>")
            body.append("<tr>" + "".join(cells) + "</tr>")
        return f"<table><tr>{h}</tr>{''.join(body)}</table>"
    return render(False), render(True)


def slide(deck, n, width=95):
    """원본 슬라이드 n을 잘라 그림으로 넣는다. 한 쪽 위(홀수)·아래(짝수) 칸을 자른다."""
    import pymupdf
    out = BUILD / f"{deck}_s{n}.png"
    if not out.exists():
        page = pymupdf.open(ORIG[deck])[math.ceil(n / 2) - 1]
        r = page.rect
        top = (0.118, 0.448) if n % 2 else (0.556, 0.886)
        clip = pymupdf.Rect(r.width * 0.095, r.height * top[0], r.width * 0.912, r.height * top[1])
        page.get_pixmap(dpi=170, clip=clip).save(out)
    return f'<div class="fig"><img src="{out.as_uri()}" style="width:{width}%"><span class="src">{s(n, deck=deck)} 원본 그림</span></div>'


ITEM = re.compile(r"\s([ⓐ-ⓩ①-⑳])\s")
GROUP = re.compile(r"(\(\d\))")


def brk(h):
    """본문 속 ⓐ… 나열: 항목의 절반 넘게 길면 항목마다 줄바꿈, 아니면 한 줄. '(2) ⓐ', 'ⓔ를' 같은 경우는 그대로."""
    out = []
    for g in GROUP.split(h):
        parts = ITEM.split(g)
        items = [re.sub(r"<[^>]+>", "", parts[i]) for i in range(2, len(parts), 2)]
        long_list = sum(len(t.strip()) > 14 for t in items) * 2 > len(items)
        seg = [parts[0]]
        for i in range(1, len(parts), 2):
            prev = seg[-1].rstrip()
            stay = not long_list or prev.endswith(("<br>", ">")) or not prev.strip()
            seg.append((" " if stay else "<br>") + parts[i] + " " + parts[i + 1])
        out.append("".join(seg))
    return "".join(out)


def render_part(label, part):
    q = brk(part["q"])
    opts = part.get("opts")
    if opts:
        q += '<ul class="opts">' + "".join(f"<li>{MARKS[i]} {o[0]}</li>" for i, o in enumerate(opts)) + "</ul>"
    out = [f'<div class="qbody">{label}{q}</div>', '<div class="space"></div>' * part.get("space", 1), '<div class="ans">']
    if part.get("a"):
        out.append(f'<span class="lab">정답</span>{brk(part["a"])}')
    if opts:
        out.append('<ul class="ox">' + "".join(
            f'<li>{MARKS[i]} <span class="{"ok" if o[1] else "no"}">{"○ 옳음" if o[1] else "✕ 틀림"}</span> — {o[2]}</li>'
            for i, o in enumerate(opts)) + "</ul>")
    if part.get("why"):
        out.append(f'<div class="why">{part["why"]}</div>')
    out.append("</div>")
    return "".join(out)


def render_problem(no, p):
    kinds = "".join(f'<span class="kind">{KIND[k]}</span>' for k in p["kind"])
    out = [f'<div class="q"><div class="qh">{kinds}문제 {no}. {p["title"]}</div>']
    if p.get("intro"):
        out.append(f'<div class="intro">{p["intro"]}</div>')
    parts = p["parts"]
    for i, part in enumerate(parts):
        out.append(render_part(f"<b>({i + 1})</b> " if len(parts) > 1 else "", part))
    out.append(p.get("fig", "") + p.get("quote", ""))
    out.append("</div>")
    return "".join(out)


def render_keywords(kws):
    if not kws:
        return ""
    dic = table(["키워드 (원문 표기)", "슬라이드 설명", "원본"], [[f"<b>{k}</b>", d, src] for k, d, src in kws])
    quiz = "".join(f"<li>{d} → <span class='blank'></span> <span class='kwa'>정답: <b>{k}</b></span></li>" for k, d, _ in kws)
    return (f"<h3>키워드 사전 — 원문 표기 그대로 외울 것</h3>{dic}"
            f"<h3>키워드 빈칸 — 설명을 보고 용어 쓰기 ({len(kws)}문항)</h3><div class='note'>정답을 종이로 가리고 푸세요. 영문 병기까지 정확히.</div><ol class='kwq'>{quiz}</ol>")


def build(mod_names, out_pdf, title, subtitle):
    parts = [f"<h1>{title}</h1><div class='sub'>{subtitle}</div>"]
    no = 0
    for name in mod_names:
        m = importlib.import_module(name)
        parts.append(getattr(m, "INTRO", ""))
        for item in m.ITEMS:
            if isinstance(item, str):
                parts.append(item)
            else:
                no += 1
                parts.append(render_problem(no, item))
        parts.append(render_keywords(getattr(m, "KEYWORDS", [])))
        parts.append(getattr(m, "OUTRO", ""))
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='cols'>{''.join(parts)}</div></body></html>"
    html_path = BUILD / (Path(out_pdf).stem + ".html")
    html_path.write_text(doc, encoding="utf-8")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={out_pdf}", html_path.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    number_pages(out_pdf)
    print("problems:", no, "->", out_pdf)


def number_pages(pdf_path, fmt="- {n} -", align=1):
    """쪽 하단에 쪽 번호를 찍는다(align 1 = 가운데, 2 = 오른쪽). 합본은 오른쪽에 전체 기준 번호를 따로 찍는다."""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    total = doc.page_count
    for i, page in enumerate(doc):
        r = page.rect
        box = pymupdf.Rect(28, r.height - 24, r.width - 28, r.height - 10)
        page.insert_textbox(box, fmt.format(n=i + 1, total=total), fontsize=8, color=(0.35, 0.35, 0.35), align=align)
    doc.saveIncr()


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    build(sys.argv[1].split(","), sys.argv[2], sys.argv[3], sys.argv[4])
