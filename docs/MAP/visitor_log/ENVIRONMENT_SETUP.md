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

## ARCore 서버 실행 (S24 연동)

```cmd
cd c:\onedrive\_대학교\MAP\git\visitor_log
python spike/server.py
```

서버 조작:

| 키 | 동작 |
|----|------|
| W / X | 앞/뒤 |
| A / D | 카메라 좌/우 회전 |
| ← / → | 좌/우 이동 |
| ↑ / ↓ | 위/아래 이동 |
| 마우스 드래그 | 시점 회전 |
| s | .ply 저장 |
| q | 종료 |

---

## Flutter ARCore 앱 빌드 + S24 설치

```cmd
cd c:\onedrive\_대학교\MAP\git\visitor_log\spike\arcore_streamer
flutter build apk --debug
copy /y "build\app\outputs\flutter-apk\app-debug.apk" "C:\temp\app-debug.apk"
adb -s 192.168.35.202:44861 uninstall com.wemeettrip.arcore_streamer
adb -s 192.168.35.202:44861 install --no-streaming "C:\temp\app-debug.apk"
```

**주의:**
- `adb -s` 뒤 IP:포트는 S24 무선 디버깅 화면에서 확인
- 설치 후 S24에서 ARCore Streamer 앱 탭 → IP 입력 → 연결

---

## 주의

- `.venv/`는 `.gitignore`에 추가 필요 (용량 큼)
- `spike/` 전체는 Python 3.12 가상환경에서만 실행
- 서비스 코드(`app/`)는 Python 버전 무관 (자연어 파일만 있음)
