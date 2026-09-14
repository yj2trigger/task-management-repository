# 로컬 PC 도커 현황

> 대상: 이 개발 PC(Windows 11, RAM 15.7 GB, C: 220 GB)에서 MAP 레포들이 함께 쓰는 Docker Desktop
> 기준 시각: 2026-09-14 13:21
> 배경을 몰라도 이 문서만으로 현재 상태·경위·다시 켜는 법·재발 시 대응을 알 수 있게 쓴다.

---

## 1. 지금 상태 요약

| 항목 | 값 | 의미 |
|---|---|---|
| Docker Desktop | **꺼져 있음** | 2026-09-12 18:12 에 정상 종료된 뒤 켜지 않았다. 고장 아님(§4 참고) |
| WSL VM(`docker-desktop`) | Stopped | 도커 엔진이 도는 리눅스 VM. Docker Desktop 을 켜면 같이 켜진다 |
| WSL 메모리 상한 | **6 GB** (`~/.wslconfig`) | 2026-09-12 신설. 기본값(RAM 절반 ≈ 7.8 GB)보다 낮춤 |
| C: 여유 공간 | 12.92 GB | 2026-09-12 아침 0.16 GB 에서 회복 |
| 도커 가상 디스크(`docker_data.vhdx`) | 17.79 GB | 24.85 GB 에서 압축으로 줄임 |
| 페이지 파일(`pagefile.sys`) | 6.84 GB | 한때 14.44 GB 까지 커졌다가 줄어듦 |

마지막으로 켜져 있던 때(2026-09-12 13:42)의 도커 내용물:

| 종류 | 내용 |
|---|---|
| 서비스 컨테이너 7개 (모두 healthy) | `map-service-hub`, `map-service-user`, `map-service-yolo`, `map-service-proxy`(nginx), `map-service-agent`, `map-service-postgres`(PostGIS 17), `map-service-redis` — 모두 `map-service-infra/docker-compose.yml` 에서 뜬다 |
| 멈춘 컨테이너 3개 (건드리지 않음) | `map-user-postgres`, `map-user-redis`(map-service-user 레포 자체 compose, [ENVIRONMENT_SETUP.md](map-service-user/ENVIRONMENT_SETUP.md)), `hub-verify-redis` |
| 이미지 | 18개, 약 14.4 GB |
| 볼륨 | 9개, 약 0.5 GB (DB 데이터 — 지우면 안 됨) |
| 빌드 캐시 | 약 5.5 GB (정리 후) |

---

## 2. 다시 켜는 법

1. Docker Desktop 실행 (`C:\Program Files\Docker\Docker\Docker Desktop.exe`)
2. 준비 확인: `docker info --format "{{.ServerVersion}}"` 이 **버전 문자열(예: 29.4.3)을 10초 안에** 내면 준비된 것
   - 종료 코드 0 만 보고 판단하면 안 된다. 엔진이 반쯤 떠 있을 때도 0 을 내면서 버전은 비어 있는 경우를 실제로 겪었다(§3 타임라인 09:42).
3. 서비스 스택은 재시작 정책으로 **저절로 다시 뜬다.** 안 뜨면 `map-service-infra` 레포에서 `docker compose up -d`
4. 메모리 상한 확인: `docker info --format "{{.MemTotal}}"` 이 약 5.8 GB(6 GB 에서 커널 몫 제외)면 적용된 것

> 여러 Claude 세션이 이 도커를 같이 쓴다. `~/.claude/hooks/resource-lock.mjs` 가 도커 명령을 줄 세우고(10분 TTL 잠금), `docker info` 가 5초 안에 응답하지 않으면 도커 명령을 막는다. 막히면 기다린다.

---

## 3. 무슨 일이 있었나 (2026-09-12)

| 시각 | 일 |
|---|---|
| 아침 | C: 여유 0.16 GB. 도커 명령이 멈춤(`docker info` 60초 넘게 응답 없음) |
| 09:40 | 멈춘 Docker Desktop 과 WSL 종료 후 `diskpart` 로 가상 디스크 압축 → **0 GB 회수**(안에서 지운 게 없었으므로) |
| 09:42 | Docker Desktop 재시작, 엔진 잠깐 뜸 |
| 09:43:37 | **도커 VM 비정상 종료.** Hyper-V-Worker 이벤트 id 18590 "게스트 운영 체제 실패"(오류 코드 모두 0x0) |
| 09:45~ | 백엔드가 죽은 엔진을 몇 분째 기다리는 상태로 멈춤 |
| ~10:00 | C: 공간 확보(Gradle 9.5.0 캐시, 휴지통, npm·Pub 캐시) → 여유 3.95 GB. 도커 재시작 → 정상 |
| 10:0x | 도커 빌드 캐시 정리 14.01 → 5.48 GB (가상 디스크 **안에서** 8.54 GB 비움) |
| 11:40 | 가상 디스크 안에서 `fstrim` 실행(지운 공간을 "빈 칸"으로 표시) → 도커·WSL 종료 → `diskpart` 압축 → 24.85 → 17.71 GB, C: 여유 8.69 GB |
| 11:42 | 도커 재시작 직후 **2분 만에 C: 여유 8.69 → 3.09 GB.** 도커 파일은 그대로였고 `pagefile.sys` 가 14.44 GB 로 커져 있었음 |
| 13:41 | `~/.wslconfig` 에 `memory=6GB` 적용 후 재시작. VM 메모리 5.79 GB 확인, 서비스 7개 healthy |
| 13:4x | VS Code 옛 확장 버전 정리. C: 여유 11.28 GB |
| 18:12 | Docker Desktop 종료(정상 종료로 판단). 이후 페이지 파일 6.84 GB, C: 여유 12.92 GB |

---

## 4. 원인

C: 공간을 잡아먹은 것은 두 가지다.

1. **도커 가상 디스크가 커지기만 한다.** `%LOCALAPPDATA%\Docker\wsl\disk\docker_data.vhdx` 는 쓰는 만큼 늘고, 안에서 이미지·캐시를 지워도 파일 크기는 줄지 않는다. 빌드를 반복하면 빌드 캐시가 쌓여 계속 커진다(당시 빌드 캐시만 14 GB).
2. **WSL 메모리가 페이지 파일을 키운다.** RAM 이 15.7 GB 인데 WSL 기본값은 RAM 의 절반까지 쓴다. 도커가 뜨면 Windows 전체 커밋 사용량이 한도(당시 23.8 / 25.6 GB)에 닿고, Windows 가 자동 관리 페이지 파일을 키워 한도를 늘린다. 그 크기만큼 C: 가 준다. 즉 **이 PC 에서는 WSL 메모리 상한이 디스크 공간에도 영향을 준다.**

VM 이 09:43 에 죽은 직접 원인은 **확인되지 않았다**(오류 코드 0x0). 당시 C: 여유가 0.2~1 GB 였으므로 디스크 부족이 가장 유력하다.

18:12 종료는 고장이 아닌 정상 종료로 판단했다: 도커·VM 프로세스가 모두 사라졌고(VM 만 죽으면 Docker Desktop 창 프로세스는 남는다), 이후 게스트 실패 이벤트도 없고, 백엔드 로그에 오류·메모리 부족 기록이 없다. 다만 로그에서 종료 문구 자체를 찾지는 못했다.

---

## 5. 한 조치

| 조치 | 효과 | 되돌리는 법 |
|---|---|---|
| `~/.wslconfig` 신설: `[wsl2] memory=6GB` | 도커 VM 메모리 5.79 GB 로 제한, 페이지 파일 14.44 → 6.84 GB | 파일 삭제 또는 값 변경 후 `wsl --shutdown` |
| 도커 빌드 캐시 정리(`docker builder prune -f`) | 가상 디스크 안에서 8.54 GB 비움 | 다음 빌드가 느려질 뿐, 되돌릴 필요 없음 |
| `fstrim` + `diskpart compact vdisk` | 가상 디스크 파일 24.85 → 17.71 GB | — |
| Gradle 9.5.0 캐시·배포판 삭제 | 0.98 GB | 필요하면 Gradle 이 다시 받음 |
| 휴지통 비움 | 1.39 GB | 복구 불가 |
| npm 캐시, Pub 패키지 캐시(`hosted`, `git`) 삭제 | 0.24 / 0.37 GB | `npm install`, `flutter pub get` 때 다시 받음 |
| VS Code 옛 확장 버전 정리 | 약 1.2 GB | — |

건드리지 않은 것: 이름 붙은 이미지, 볼륨(DB 데이터), 멈춘 컨테이너, Gradle 8.12.1(백엔드 레포들이 사용)·8.14(Flutter 안드로이드 빌드가 사용), `hiberfil.sys`(최대 절전 유지).

---

## 6. 재발하면

C: 공간이 급히 줄거나 도커가 멈추면 이 순서로 본다.

1. **페이지 파일부터**: `C:\pagefile.sys` 크기와 커밋 사용량(작업 관리자 → 성능 → 메모리 → "커밋됨"). 커밋이 한도에 붙어 있으면 `.wslconfig` 상한을 더 낮추거나 다른 프로그램을 줄인다. 페이지 파일을 고정 크기로 줄이는 것은 권하지 않는다(커밋 한도가 내려가 메모리 부족 크래시가 늘어난다).
2. **도커 사용량**: `docker system df`. 빌드 캐시가 크면 `docker builder prune -f`.
3. **가상 디스크 압축**(파일 크기를 실제로 줄이려면 아래 순서를 모두 지켜야 한다):
   1. 도커 안에서 정리(prune)
   2. `fstrim` — **빠뜨리면 압축해도 0 GB 회수**(실측):
      `docker run --rm --privileged --pid=host --entrypoint nsenter redis:7-alpine -t 1 -m -- fstrim -av`
      특권 컨테이너 명령이라 Claude 자동 모드에서는 거부된다. 사람이 직접 실행한다.
   3. Docker Desktop 종료 → `wsl --shutdown`
   4. 관리자 `diskpart`:
      ```
      select vdisk file="%LOCALAPPDATA%\Docker\wsl\disk\docker_data.vhdx"
      attach vdisk readonly
      compact vdisk
      detach vdisk
      ```
      (24.85 GB 기준 약 2분)
   5. Docker Desktop 재시작 → §2 로 준비 확인
4. 컨테이너가 메모리 부족으로 죽으면 `.wslconfig` 의 6 GB 를 올린다.

---

## 7. 아직 확인하지 못한 것

- 09:43 VM 비정상 종료의 직접 원인(디스크 부족 추정)
- 6 GB 상한에서 YOLO 추론과 빌드가 겹치는 무거운 부하를 버티는지 — 부하 시험 안 함
- 09-12 10시~11시 40분 사이 C: 여유가 3.90 → 1.55 GB 로 줄어든 원인 — 도커 가상 디스크는 그대로였고, 오늘 바뀐 100 MB 이상 파일 중에도 없었다. 페이지 파일 확장이었을 가능성이 높지만 당시 크기는 재지 않았다
