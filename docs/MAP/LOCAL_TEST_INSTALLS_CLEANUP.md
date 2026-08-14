# 로컬 테스트용 설치 목록 (이미지 챗봇 실제 앱 테스트)

> 작성일: 2026-07-29
> 갱신일: 2026-08-14 — 아래 "2026-08-14 갱신 요약" 참고. **이 날짜 이전 내용은 상당수 낡았음.**
> 목적: `map-yoloservice` 이미지 입력 AI 챗봇을 실제 Flutter 앱(`map-service-client`)으로
> 테스트하기 위해 로컬에 설치한 항목. 나중에 삭제할 때 이 목록만 보고 지우면 됨.

---

## 2026-08-14 갱신 요약

작성 시점(2026-07-29)에는 yolo 서비스를 **로컬 venv + uvicorn(:8001)** 으로 직접 띄우고,
Flutter는 **별도 SDK 폴더(worktree)** 로 우회하는 구조였다. 그 뒤 둘 다 바뀌었다.

| 바뀐 것 | 이전(2026-07-29) | 지금(2026-08-14) |
|---|---|---|
| yolo 기동 방식 | 로컬 venv + `uvicorn :8001` | **Docker 컨테이너**(`map-service-infra`, `--profile vision`) |
| client가 보는 vision 주소 | `VISION_SERVER_HOST=localhost:8001` | **안 씀** — `API_BASE_URL`을 proxy(8090)로 지정하면 `/ws/vision`이 자동으로 풀림 |
| Flutter 버전 고정 방식 | `C:\FlutterSDKs\3.41.9` (git worktree) | **fvm** (`C:\Users\rexro\fvm\versions\3.41.9`, 프로젝트의 `.fvm/flutter_sdk` 심볼릭 링크가 가리킴) |

경위는 `docs/MAP/map-yoloservice/DEV_LOG.md` 참고.

---

## 삭제하면 끝나는 것 (폴더 통째로 지우기만 하면 됨)

| 항목 | 경로 | 비고 |
|---|---|---|
| map-yoloservice 클론 (repo+venv+.env+모델) | `C:\onedrive\_대학교\MAP\git\map-yoloservice\` | `.env`에 **GEMINI_API_KEY 평문 포함** — 폴더째 삭제 전 키 재사용 여부 확인. Docker로 기동하는 지금도 이 클론은 **빌드 소스로 필요**하므로 함부로 지우면 안 됨 |
| ~~Flutter 3.41.9 별도 SDK (worktree)~~ | ~~`C:\FlutterSDKs\3.41.9\`~~ | **2026-08-14 삭제 완료** — fvm으로 대체됨(아래 "주의" 참고) |

## 명령으로 되돌려야 하는 것

| 항목 | 되돌리는 법 |
|---|---|
| `map-service-yolo` 심볼릭 링크 | `MAP/git/map-service-yolo` → `map-yoloservice`. compose의 빌드 컨텍스트 경로(`../map-service-yolo`)와 실제 클론 폴더명이 달라서 건 우회책. 지우려면 링크만 삭제하면 되지만, **지우면 vision 프로파일 빌드가 다시 깨진다** |
| ~~Flutter 3.41.9 worktree 등록~~ | **불필요** — `C:\Program Files\flutter`(부모 저장소)와 worktree 둘 다 2026-08-14에 삭제돼 좀비 메타데이터가 남을 곳 자체가 없음 |
| wscat 전역 설치 (npm) | `npm uninstall -g wscat` |
| map-service-client 로컬 브랜치 `feat/#43` | 원격 추적만 하는 로컬 브랜치, 볼일 끝나면 `git checkout main && git branch -D "feat/#43"` |
| map-service-client `.env` | `C:\dev\map-service-client\.env` — gitignore 대상이라 커밋 위험 없음, 삭제만 하면 됨. **경로 주의**: 한글 경로 문제로 프로젝트가 `C:\dev\`로 이동됨(원래 `MAP\git\` 아님) |
| `adb reverse tcp:8090 tcp:8090` | 실기 테스트용 포트 포워딩. `adb reverse --remove tcp:8090` 또는 USB 분리 시 자동 해제 |

## 자동으로 사라지는 것 (신경 안 써도 됨)

- ~~yolo-vision-agent 서버 (uvicorn, `localhost:8001`)~~ — **더는 이렇게 안 띄움**. 지금은
  Docker 컨테이너(`map-service-yolo`)라 `docker compose down`으로 내림
- Flutter 앱 실행(`flutter run`) — 터미널/세션 끝나면 종료
- `map-service-client\.dart_tool/`, `build/`, `pubspec.lock` — 전부 gitignore 대상, 커밋 안 됨.
  지우고 싶으면 `flutter clean`. **용량이 큼**(gradle 캐시 포함 수 GB) — 디스크 부족할 때 1순위 정리 대상
- `C:\Users\rexro\AppData\Roaming\Ultralytics\settings.json` — ultralytics 최초 실행 시 자동
  생성된 설정 파일, 용량 미미, 안 지워도 무해

## 주의

- **Flutter SDK는 이제 fvm이 관리한다.** 프로젝트의 `.fvm/flutter_sdk`는
  `C:\Users\rexro\fvm\versions\3.41.9`를 가리키는 심볼릭 링크다. 이 경로를 지우면 빌드가
  깨지므로, 디스크 정리 시 **fvm 폴더는 건드리지 말 것**.
  (2026-08-14에 지운 건 이와 무관한 중복 설치본 `C:\Program Files\flutter`와
  `C:\FlutterSDKs\3.41.9`였다.)
- 버전을 3.41.9로 고정하는 이유는 그대로다: `map-service-client`의 `phosphor_flutter` 패키지가
  Flutter 3.44+의 `IconData` `final class` 변경과 충돌해 빌드 실패 → 변경 이전 버전으로 우회.
  근본 해결(= `phosphoricons_flutter`로 교체)은 여전히 팀 작업으로 남아있음
  (`tasks/in-progress.md` 참고).
- **Docker 빌드는 디스크를 많이 먹는다.** vision 프로파일 이미지에 torch가 들어가고,
  캐시 없이 빌드하면 수 GB가 나간다. 2026-08-14에 이것 때문에 C드라이브가 0바이트까지 차서
  빌드가 반복 실패하고, 그 여파로 `sfc /scannow`가 시스템 파일 손상을 발견·복구한 사고가 있었다.
  빌드 전 여유 공간을 확인할 것.
