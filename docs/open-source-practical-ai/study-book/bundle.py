"""장별 PDF를 합본으로 묶는다: 북마크를 달고, 오른쪽 아래에 합본 전체 기준 쪽 번호(N / 전체)를 찍는다.

사용: python bundle.py <출력.pdf> <장1.pdf> <장2.pdf> …   (북마크 이름은 파일 이름에서 '_초안…'을 뗀 것)
"""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).parent))
import osai  # noqa: F401  (qbook2 경로 준비)
import qbook2

out_pdf, parts = sys.argv[1], sys.argv[2:]
out, toc = pymupdf.open(), []
for p in parts:
    toc.append([1, Path(p).stem.split("_초안")[0].replace("_", " "), out.page_count + 1])
    out.insert_pdf(pymupdf.open(p))
out.set_toc(toc)
out.save(out_pdf)
qbook2.number_pages(out_pdf, fmt="{n} / {total}", align=2)
for _, title, start in toc:
    print(f"{start:>3}쪽~  {title}")
print("합본", out.page_count, "쪽 ->", out_pdf)
