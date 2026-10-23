"""원문 대조: 장 모듈의 quote() 인용문이 원본 강의 PDF 텍스트에 그대로 있는지 확인한다.

출처 문자열("원본 4주 p30")의 주차로 PDF를 고른다. 공백·따옴표·하이픈·글머리표는 무시한다.
사용: python verify.py core
"""
import importlib, re, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import osai
import qbook2
import pymupdf

found = []
qbook2.quote = lambda text, src: found.append((text, src)) or ""
osai.quote = qbook2.quote


def norm(t, html=True):
    if html:
        t = re.sub(r"<[^>]+>", "", t).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return re.sub(r"[\s\"'“”‘’\-–▪•-]", "", t)


texts = {w: norm("".join(p.get_text() for p in pymupdf.open(osai.pdf(w))), html=False) for w in osai.WEEK}
bad = 0
for name in sys.argv[1:]:
    found.clear()
    sys.modules.pop(name, None)
    importlib.import_module(name)
    for text, src in found:
        w = next((k for k in osai.WEEK if k in src), None)
        for piece in re.split(r"…", text):
            p = norm(piece)
            if w is None or (len(p) >= 6 and p not in texts[w]):
                bad += 1
                print(f"[{name}] {w} 불일치: {piece.strip()[:70]}")
    print(f"{name}: 인용 {len(found)}개 확인")
print("불일치 합계", bad)
