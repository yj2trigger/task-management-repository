"""원문 대조: 장 모듈의 quote() 인용문이 원본 자료 텍스트에 그대로 있는지 확인한다.

인용 속 "…"는 줄임 표시로 보고 조각마다 따로 찾는다. 공백·따옴표·글머리표는 무시한다.
인용의 출처 문자열("원본 2강 PPT s9")에서 자료 이름을 찾아 그 자료에서만 대조한다.
사용: python verify.py w1 w2 …
"""
import importlib, re, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / "system-design-methodology" / "study-book")]
import qbook2, sources

found = []
qbook2.quote = lambda text, src: found.append((text, src)) or ""


def norm(t, html=True):
    if html:
        t = re.sub(r"<[^>]+>", "", t).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return re.sub(r"[\s\"'“”‘’\-▪•➢-]", "", t)


cache = {}
bad = 0
for name in sys.argv[1:]:
    found.clear()
    sys.modules.pop(name, None)
    importlib.import_module(name)
    for text, src in found:
        doc = next((k for k in sources.FILES if k in src), None)
        if doc is None:
            bad += 1
            print(f"[{name}] 출처 이름 없음: {src}")
            continue
        cache.setdefault(doc, norm(sources.load(doc), html=False))
        for piece in re.split(r"…|\.\.\.", text):
            p = norm(piece)
            if len(p) >= 6 and p not in cache[doc]:
                bad += 1
                print(f"[{name}] {doc} 불일치: {piece.strip()[:70]}")
    print(f"{name}: 인용 {len(found)}개 확인")
print("불일치 합계", bad)
