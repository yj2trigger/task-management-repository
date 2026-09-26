# VSCode 터미널에서 gcc 인식 안 됨 — MinGW 재설치 후 PATH 캐시 문제

> 출처: 세션 `57a5314a-ff8a-4066-8557-7fe37d0fc241`(JARAM C_Study_LinkedList 폴더, 2026-05-27T22:55~23:01 UTC).

## 증상

`cmd.exe`에서는 `gcc main.c linkedList.c -o main.exe`가 정상 작동하는데, VSCode 통합 터미널에서는 `gcc`를 못 찾음.

## 진단 과정

1. 1차 가설(터미널 프로필이 PowerShell이라 PATH가 다를 수 있음, 작업 디렉터리가 다를 수 있음)로 시작했으나 `where gcc`/`pwd` 자체가 cmd 프로필에서도 실패.
2. VSCode 재시작 권장 → 재시작·리로드해도 안 됨.
3. `echo %PATH%`로 확인하니 MinGW 경로(`C:\env_coding\env_ver1\...\mingw64\bin`)가 **PATH에 이미 포함**돼 있음 — 그런데도 `where gcc`는 실패. 새 터미널을 열어도 동일.
4. **근본 원인 특정**: `dir`로 그 PATH 경로 자체를 확인하니 `지정된 경로를 찾을 수 없습니다` — PATH에 등록된 경로가 실제로는 존재하지 않는 **유령 경로**였음. 일반 cmd에서 `where gcc`로 실제 위치를 찾으니 전혀 다른 경로(`winlibs-x86_64-posix-seh-gcc-16.1.0-...`)에 설치돼 있었음.
5. 결론: 사용자가 MinGW를 재설치하면서 시스템 PATH는 새 경로로 갱신됐지만, **VSCode가 그보다 먼저 실행되어 있던 프로세스라 옛 PATH를 그대로 상속**하고 있었음. `Reload Window`는 설정 파일만 다시 읽을 뿐 프로세스 자체의 환경변수는 갱신하지 않음 — 그래서 리로드로도 해결이 안 됐음.

## 해결책 (3가지 중 택1로 제시, 세션 종료 시점엔 미확정)

- **A. VSCode 완전 종료 후 재시작**(가장 간단하지만 안 될 수도 있음 — 상위 프로세스인 탐색기/터미널 앱까지 옛 환경을 물고 있을 경우)
- **B. `settings.json`에 `terminal.integrated.env.windows`로 새 경로를 직접 박아넣기** (가장 확실, PATH 상속 문제를 우회)
- **C. 재부팅** (모든 프로세스가 새 PATH를 상속하도록 강제)

## 교훈

- Windows에서 "환경변수를 바꿨는데 이미 켜져 있던 프로그램에서 안 먹힌다"는 문제는 재시작이 아니라 **그 프로그램이 실행된 시점** 문제 — 재부팅 전에는 `Reload Window`만으로 해결 안 되는 경우가 있음.
- `where <cmd>`가 실패하는데 `echo %PATH%`엔 경로가 있다면, "PATH에 있다"와 "그 경로가 실제로 존재한다"를 구분해서 진단해야 함(`dir <path>`로 직접 확인).
