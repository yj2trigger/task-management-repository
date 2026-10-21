"""아카데믹 글쓰기 학습본 빌드. 조판은 시스템설계방법론 학습본의 생성기(qbook2)를 그대로 쓴다.

사용: python build.py w1 <출력.pdf> "<제목>" "<부제>"
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / "system-design-methodology" / "study-book")]
import qbook2

qbook2.KIND["essay"] = "서술·수정형"  # 이 과목의 주관식은 수정형과 서술형이다

if __name__ == "__main__":
    qbook2.build(sys.argv[1].split(","), sys.argv[2], sys.argv[3], sys.argv[4])
