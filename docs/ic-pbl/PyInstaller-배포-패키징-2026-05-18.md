# ic-pbl 키오스크 — PyInstaller로 Windows/Mac 배포 패키징

> 출처: 세션 `fc92d894-2735-407e-b398-ccfa98339e42`(`c:\onedrive\_대학교\프로그래밍기초\icpbl\ic-pbl 프로그램` 폴더, 2026-05-18T08:50~09:03 UTC). `pmg-EDK에서-아이스크림-전환-2026-05-26.md`가 다루는 세션(같은 `build_mac.sh` 파일이 등장)보다 8일 앞선 초기 배포 준비 작업 — 이 시점엔 아직 EDK/아이스크림 전환 전, 로컬 폴더명도 `icpbl\ic-pbl 프로그램`으로 이후의 `pmg-ic-pbl`과 다름(같은 프로젝트가 폴더를 옮기며 이어진 것으로 보임).

## 요청과 구현

"PyInstaller를 이용해서 mac과 window에서 이용 가능하도록 하세요" → PyQt6 기반 키오스크 앱을 실행파일로 배포하기 위한 4개 파일 작업:

| 파일 | 역할 |
|---|---|
| `main.py`(수정) | 빌드된 실행 파일에서는 `sys.executable` 옆의 `data/` 폴더를 쓰도록 경로 처리 + 기본 실행 모드를 GUI로 고정 |
| `kiosk.spec`(신규) | PyInstaller 설정. PyQt6는 `collect_all`로 플랫폼별 바이너리 자동 포함, 지연 import 누락 방지 위해 모든 GUI 화면 모듈을 `hiddenimports`에 명시 |
| `build_windows.ps1`(신규) | Windows 빌드 스크립트 |
| `build_mac.sh`(신규) | Mac 빌드 스크립트 |

**핵심 설계 포인트**: PyInstaller는 **빌드하는 OS의 실행 파일만 만들 수 있음** — Windows에서 `.exe`, Mac에서 `.app`을 각각 그 OS에서 따로 빌드해야 함(크로스 컴파일 불가). 데이터 저장 위치는 실행 파일과 같은 폴더의 `data/`로 고정, 실행 파일만 옮기면 데이터가 초기화된다는 점을 배포 안내에 명시.

## 실제 빌드 시도 중 겪은 3단계 실행 오류 — 전형적인 Windows 초보자 PowerShell 삽질

1. **`.ps1` 더블클릭하면 메모장이 열림**: Windows가 `.ps1`을 스크립트가 아니라 텍스트로 취급하는 기본 연결 때문. 해결: PowerShell 터미널 **안에서** 입력해야 함.
2. **`이 시스템에서 스크립트를 실행할 수 없으므로...` (PSSecurityException)**: 기본 실행 정책(`Restricted`)이 로컬 스크립트 실행을 막음. `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`로 그 세션에서만 우회하거나, 스크립트 없이 명령어 2줄(`pip install` + `pyinstaller kiosk.spec`)을 직접 치는 방법으로 우회.
3. **`'pyinstaller' 용어가 인식되지 않습니다`**: `pip install`은 성공했지만 스크립트가 PATH에 안 걸림(흔한 pip 콘솔스크립트 PATH 문제) → `python -m PyInstaller`로 모듈 실행 방식으로 우회.

세 오류 모두 "설치 자체는 됐는데 실행 경로/정책이 막혀서 안 됨"이라는 같은 패턴 — 이 컴퓨터에서 반복되는 유형의 문제(다른 세션들의 gcc PATH 문제와 같은 계열)임.

## 이 문서가 메우는 공백

기존 ic-pbl 문서에는 배포/패키징 관련 내용이 없었음 — 이 세션이 배포 파이프라인(PyInstaller)을 처음 도입한 지점.
