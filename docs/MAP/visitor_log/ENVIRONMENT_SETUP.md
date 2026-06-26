# visitor_log 환경 설정

> 작성일: 2026-06-27 00:00
> 로컬 경로: `c:\onedrive\_대학교\MAP\git\visitor_log`
> 상태: spike 단계

---

## Python 버전

**Python 3.12 필수.** open3d가 3.13 이상 미지원.

Python 3.14(시스템 기본)로 실행하면 open3d 설치 실패.

설치 확인:
```bash
py --list
# -V:3.12 항목 있어야 함
```

없으면:
```bash
winget install Python.Python.3.12
```

---

## 가상환경 설정

```bash
cd c:\onedrive\_대학교\MAP\git\visitor_log
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install opencv-python open3d transformers torch torchvision pillow matplotlib zstandard numpy
```

매번 작업 시작 전 활성화:
```bash
.venv\Scripts\activate
```

---

## spike 실행

```bash
# 가상환경 활성화 상태에서
python spike/realtime.py
```

조작:

| 키 | 동작 |
|----|------|
| W/S/A/D | 앞/뒤/좌/우 이동 |
| ↑/↓ | 위/아래 이동 |
| 마우스 드래그 | 시점 회전 |
| 스크롤 | 줌 |
| s | 현재 씬 .ply 저장 + 블렌딩 시각화 |
| q | 종료 |

출력 파일: `spike/output/scene.ply`, `spike/output/blend_alpha.png`

---

## 주의

- `.venv/`는 `.gitignore`에 추가 필요 (용량 큼)
- `spike/` 전체는 Python 3.12 가상환경에서만 실행
- 서비스 코드(`app/`)는 Python 버전 무관 (자연어 파일만 있음)
