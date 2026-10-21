"""원문 대조: 장 모듈의 quote() 인용문이 원본 강의자료 PDF 텍스트에 그대로 있는지 확인한다.

인용 속 "…"는 줄임 표시로 보고 조각마다 따로 찾는다. 공백·줄바꿈은 무시하고 비교한다.
사용: python verify.py ch1 ch2 …
"""
import importlib, re, sys
import pymupdf
import qbook2

found = []
qbook2.quote = lambda text, src: found.append((text, src)) or ""


def norm(t, html=True):
    if html:  # 인용문(HTML)만 태그를 지운다. 원본 텍스트에는 State<Dp> 같은 꺾쇠가 있어 지우면 안 된다.
        t = re.sub(r"<[^>]+>", "", t).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return re.sub(r"[\s\"'“”‘’-▪•➢]", "", t)  # 공백·따옴표·글머리표(사용자 정의 영역  등) 무시


texts = {d: norm("".join(p.get_text() for p in pymupdf.open(path)), html=False) for d, path in qbook2.ORIG.items()}
bad = 0
for name in sys.argv[1:]:
    found.clear()
    sys.modules.pop(name, None)
    importlib.import_module(name)
    for text, src in found:
        deck = re.search(r"ppa\d", src).group()
        for piece in re.split(r"…|\.\.\.", text):
            p = norm(piece)
            if len(p) >= 6 and p not in texts[deck]:
                bad += 1
                print(f"[{name}] {deck} 불일치: {piece.strip()[:70]}")
    print(f"{name}: 인용 {len(found)}개 확인")
print("불일치 합계", bad)
