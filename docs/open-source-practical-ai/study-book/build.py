"""오픈소스실전인공지능 학습본 빌드.

사용: python build.py core <출력.pdf> "<제목>" "<부제>"
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import osai  # noqa: F401  (qbook2 경로와 CSS를 준비한다)
import qbook2

qbook2.KIND.update({"graph": "그래프↔명령", "cmd": "상황→명령"})

if __name__ == "__main__":
    qbook2.build(sys.argv[1].split(","), sys.argv[2], sys.argv[3], sys.argv[4])
