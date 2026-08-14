# map-yoloservice 개발 로그

> 작성일: 2026-08-14
> 대상: `map-yoloservice` (카메라 실시간 인식 — YOLO 추론 + Gemini Vision 식별)
> 형식: `docs/MAP/visitor_log/DEV_LOG.md`와 동일(상황/판단/결론).
>
> **범위**: 이 문서는 `map-yoloservice`를 `map-service-infra` 오케스트레이션에 편입하고
> 실기(Galaxy S24 Ultra)에서 end-to-end 연결을 확인하기까지의 기록이다. 서비스 내부
> 로직(YOLO 추론·Gemini 호출) 자체는 이번 범위가 아니다.
>
> **선행 기록**: 여기서 다루는 문제는 `tasks/in-progress.md`의 "MAP (map-service-client)
> — 비전 화면 전면/후면 카메라 전환" 항목에 *"별개로 발견한 이슈(이번 범위 밖)"*로
> 2026-08-07에 먼저 적혀 있던 것이다. 이번에 그 (a)/(b) 두 건을 실제로 해결했다.

---

## 1. WebSocket 연결 실패 원인 재확인 (2026-08-13)

**상황:** client의 비전 화면이 `/ws/vision`으로 붙지 못하는 문제. 2026-08-07 기록상 원인은
두 가지로 추정돼 있었음 — (a) `map-yoloservice`가 인프라에 통합 안 돼서 어디에도 안 떠있음,
(b) client `.env`의 `VISION_SERVER_HOST=localhost:8001`이 실기 기준 "폰 자기 자신"을 가리킴.

**판단:** (a)를 먼저 확인해보니 추정과 달랐다. `docker-compose.yml`에는 이미 `yolo` 서비스가
`vision` 프로파일로 **정의돼 있었다**(L208~247). 즉 "통합이 안 된 것"이 아니라 "정의는
있는데 실제로 기동해본 적이 없어서 아무도 깨진 걸 몰랐던" 상태였음.

**결론:** 원인을 "미통합"이 아니라 "정의는 있으나 기동 불가"로 정정. 실제로 띄워보는 것부터
시작하기로 함 — 아래 2~4번이 그 과정에서 하나씩 드러난 실패들이다.

---

## 2. compose의 빌드 컨텍스트 경로와 실제 클론 폴더명 불일치 (2026-08-13)

**상황:** `docker compose --profile vision up`을 실행하니 빌드 자체가 시작되지 않음.
compose의 `yolo.build.context`가 `../map-service-yolo`인데, 실제 클론된 폴더명은
`map-yoloservice`였음.

**판단:** 근본 해결은 둘 중 하나 — 레포 이름을 바꾸거나, compose의 context 경로를 고치거나.
그런데 둘 다 팀 공용 자산(레포명·infra 설정)을 건드리는 일이라 혼자 판단해 바꾸면
다른 사람 환경이 깨질 수 있다. 특히 compose 쪽을 `../map-yoloservice`로 고치면, 이미
`map-service-yolo`로 클론해둔 팀원의 환경이 반대로 깨진다.

**결론:** 로컬에 심볼릭 링크만 걸어 우회 —
`MAP/git/map-service-yolo` → `MAP/git/map-yoloservice`. 커밋되는 파일은 하나도 안 건드리므로
다른 사람 영향 0. **다만 이건 임시조치이므로 팀 논의 대상으로 남긴다**(아래 "남은 팀 논의" 참고).

---

## 3. torch가 GPU/CUDA 휠로 잡혀 이미지가 수 GB로 불어남 (2026-08-13)

**상황:** 빌드가 시작되자 `pip install`이 `nvidia-cublas`, `nvidia-cudnn` 등 NVIDIA
런타임 패키지를 줄줄이 받기 시작. 이 PC에는 NVIDIA GPU가 없고 컨테이너도 CPU로만 도는데도.

**판단:** `requirements.txt`가 `ultralytics`만 명시하고 `torch`는 그 의존성으로 딸려오게
돼 있었는데, PyPI 기본 `torch` 휠은 CUDA 런타임을 통째로 포함한다. 즉 GPU 없는 환경에서도
수 GB를 받아 이미지에 그대로 얹히는 구조. 빌드가 느린 것도 문제지만, 이번 세션에서 실제로
**디스크가 0바이트까지 차서** 빌드가 반복 실패한 직접 원인이기도 했다.

**결론:** `requirements.txt`에 PyTorch 공식 CPU 전용 휠 저장소를 지정하고 `torch`를 명시적
의존성으로 끌어올림 (커밋 `8c11210`):

```
--extra-index-url https://download.pytorch.org/whl/cpu
torch>=2.0.0
```

GPU 배포가 필요해지면 이 두 줄만 빼면 원래 동작으로 돌아간다(주석에 이유 명시해둠).

---

## 4. Dockerfile 포트(8001)와 나머지 전부(8000)의 불일치 (2026-08-13)

**상황:** 빌드가 끝나고 컨테이너는 떴는데 헬스체크가 계속 실패해 `unhealthy` 상태로 남음.

**판단:** `Dockerfile`의 `EXPOSE`/`HEALTHCHECK`/`ENTRYPOINT`가 전부 **8001**을 쓰고 있었는데,
이 서비스를 둘러싼 나머지는 전부 **8000**을 기대하고 있었다 —
compose의 포트 매핑(`127.0.0.1:8004:8000`), compose 자체 헬스체크(`localhost:8000/health`),
nginx의 `proxy_pass`. 즉 서비스 혼자 다른 포트를 듣고 있었던 것.

이 불일치가 여태 안 드러난 이유: 원래 이 서비스는 로컬에서 `uvicorn ... --port 8001`로
직접 띄워 쓰던 1회성 구현이었고(2026-07-29 `LOCAL_TEST_INSTALLS_CLEANUP.md` 참고),
컨테이너로 기동해본 적이 없어서 Dockerfile 쪽 값은 아무도 검증한 적이 없었다.

**결론:** Dockerfile 3곳을 전부 8000으로 통일(커밋 `8c11210`). compose·nginx 쪽(팀 공용)이
아니라 서비스 쪽을 고친 이유는, 8000이 이미 다수 규약이고 나머지를 다 바꾸는 것보다
영향 범위가 작기 때문.

---

## 5. client의 vision 주소 지정 방식을 proxy 단일 경로로 통일 (2026-08-13)

**상황:** 2026-08-07 기록의 (b) — client `.env`가 `VISION_SERVER_HOST=localhost:8001`로
vision 서버를 **따로** 가리키고 있었음. 실기에서 `localhost`는 폰 자신이라 근본적으로 틀린 값.

**판단:** 에뮬레이터라면 `10.0.2.2`로 우회 가능하지만, 실기에서는 그 별칭이 없다. 게다가
"vision만 별도 호스트를 갖는" 구조 자체가 문제 — 서비스가 하나 늘 때마다 client `.env`에
주소가 하나씩 늘어난다. client 코드(`vision_ws_service.dart`)를 확인해보니 `API_BASE_URL`이
있으면 거기서 `/ws/vision`을 자동으로 풀도록 이미 돼 있었다.

**결론:** `VISION_SERVER_HOST`를 쓰지 않고 `API_BASE_URL`을 infra proxy(8090) 하나로 지정.
proxy가 `/ws/vision`을 yolo로 넘겨주므로 client는 주소를 하나만 알면 된다.
실기 연결은 `adb reverse tcp:8090 tcp:8090`으로 폰의 8090을 PC로 되돌려 해결
(무선 디버깅 환경이라 폰에서 PC IP를 직접 치는 것보다 안정적).

---

## 6. 실기 end-to-end 검증 (2026-08-14)

**상황:** 위 수정들을 반영해 전체 스택을 띄우고 실제 폰에서 확인.

**판단:** "컨테이너가 healthy" 만으로는 client가 실제로 붙었다는 증거가 안 된다 —
서버 쪽 로그에 **연결 수립 기록**이 찍히는 걸 봐야 한다고 보고 그것을 검증 기준으로 삼음.

**결론:** 전부 확인됨.

- 7개 컨테이너 전부 `healthy`: `postgres` / `redis` / `user` / `agent` / `hub` / `proxy` / `yolo`
- yolo 컨테이너 로그에 실제 연결 수립 확인:
  ```
  172.20.0.7:48958 - "WebSocket /ws/vision" [accepted]
  connection open
  ```
  (172.20.0.7 = proxy 컨테이너 IP — client → proxy → yolo 경로가 실제로 뚫렸다는 뜻)
- 음성 인식(STT)도 실동작 확인 — 마이크 버튼을 누르니 주변 대화가 한글로 정확히 전사됨.

**미검증으로 남은 것:** 카메라 프레임을 실제로 보내 **Gemini 식별 응답까지 돌아오는 전체
왕복**은 확인하지 못했다. adb로는 마이크/카메라에 실제 입력을 주입할 방법이 없고, 화면의
"채팅" 탭도 텍스트 입력이 아니라 음성 전용이었기 때문. 연결·전사까지는 증명됐으므로
남은 건 사람이 직접 폰을 들고 한 번 말해보면 끝나는 수준이다.

---

## 남은 팀 논의 / 후속 작업

| 항목 | 내용 |
|---|---|
| 레포명 vs compose 경로 불일치 | 2번의 심볼릭 링크는 **내 로컬 임시조치**. 근본 해결은 레포명을 `map-service-yolo`로 바꾸거나 compose context를 `../map-yoloservice`로 고치는 것 — 어느 쪽이든 팀 합의 필요(한쪽을 고르면 반대쪽으로 클론해둔 사람 환경이 깨짐). |
| `.env`의 `VISION_SERVER_HOST` | 이제 안 쓰는 키. client `.env`(gitignore 대상)에는 임시 주석과 함께 남겨뒀으나, 팀 공용 `.env.example`에도 있다면 제거 대상인지 확인 필요. |
| Gemini 왕복 미검증 | 6번 참고. 실기에서 사람이 직접 1회 확인하면 종료. |
| GPU 배포 시 | 3번의 CPU 휠 지정 2줄을 빼야 함. requirements.txt 주석에 명시해둠. |
