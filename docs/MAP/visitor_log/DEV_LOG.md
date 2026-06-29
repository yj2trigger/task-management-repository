# visitor_log spike 개발 로그

> 작성일: 2026-06-28 00:00
> 대상: `visitor_log` spike (카메라→3D 파이프라인 검증)

---

## 1. visitor_log 프로젝트 생성

**상황:** VPS·AR 앵커 기능 스펙 작성 중, 앵커 작성 시점의 주변 환경을 3D로 저장하고 나중에 AR로 덧씌우는 "과거 씬 오버레이" 기능이 필요함을 확인.

**판단:** 이 기능은 `map-service-hub`(FastAPI)와 별개로 독립적인 씬 저장·서빙 서비스가 필요. 모바일이 포인트 클라우드를 업로드하면 압축·저장하고, 렌더링 시 제공하는 역할.

**결론:** `visitor_log` Python 프로젝트 신설. spike 단계에서 파이프라인 구조를 먼저 검증한 뒤 서비스 통합 여부 결정하기로 함.

---

## 2. Python 버전 호환성 문제

**상황:** `pip install open3d` 실행 시 설치 실패. 시스템 Python이 3.14.

**판단:** open3d는 Python 3.12까지만 지원(공식 wheel). 3.14는 너무 새로워서 바이너리 미제공.

**결론:** `py -3.12 -m venv .venv`로 Python 3.12 가상환경 생성. 이후 모든 spike는 `.venv` 활성화 상태에서 실행.

---

## 3. 카메라→3D 파이프라인 설계

**상황:** ARKit/ARCore 없이 파이프라인 구조를 검증해야 함. S24(Android)는 있지만 Flutter 앱 빌드 전에 노트북에서 먼저 테스트하고 싶음.

**판단:**
- 노트북 웹캠 + Depth-Anything v2(단안 깊이 추정 모델)로 ARCore depth를 시뮬레이션
- 모델 출력(0~1 상대값) × DEPTH_SCALE(30.0) = 미터 근사 (부정확하지만 구조 검증용)
- 역투영: `X = (u-cx)/fx*d`, `Y = -(v-cy)/fy*d`, `Z = d`
- 결과: `(N, 6)` float32 배열 `[x,y,z,r,g,b]`

**결론:** `spike/realtime.py` 작성. 웹캠 실시간 → depth 추정 → 역투영 → Open3D 뷰어 파이프라인 구성. ARCore 전환 시 DEPTH_SCALE 제거, estimate_depth를 ARCore Depth API로 교체.

---

## 4. 실행 오류 연쇄

**상황:** 여러 단계에서 오류 발생.

| 오류 | 원인 | 해결 |
|------|------|------|
| `No module named 'cv2'` | 가상환경 미활성화 | `.venv\Scripts\activate` 후 재실행 |
| `cannot import name 'downsample_voxel'` | `pointcloud.py`가 자연어 주석만 있고 실제 코드 없음 | 코드로 변환 |
| `o3d.visualization.KeyAction` 없음 | Open3D 버전에 따라 KeyAction enum 경로 다름 | action 정수값(1=press, 0=release) 직접 비교로 교체 |
| `frame_to_rgb` NameError | 파일 전체 재작성 시 함수 누락 | 함수 재삽입 |

---

## 5. WASD 키 미작동

**상황:** Open3D 창에서 WASD 입력 시 작동 안 함.

**원인 분석:**
1. `register_key_action_callback` 콜백 시그니처가 `(vis, key, action)` 3개인데 `(vis, action)` 2개로 잘못 작성 → TypeError
2. 수정 후에도 Open3D 창과 OpenCV 창 간 포커스 이벤트 충돌로 키 입력이 전달되지 않음

**판단:** Open3D 이벤트 시스템과 OpenCV 이벤트 루프가 같은 스레드에서 경합. 창 포커스 무관하게 키 상태를 폴링하는 방식이 필요.

**결론:** `keyboard` 모듈 도입. `keyboard.is_pressed('w')` 등으로 매 루프마다 키 상태 직접 확인. 창 포커스 무관하게 작동.

---

## 6. 카메라 창 깜빡임

**상황:** depth 결과 없을 때는 `frame`(너비 640), 결과 있을 때는 `frame+depth`(너비 1280)를 같은 창에 표시 → 창 크기가 매 프레임 바뀌며 깜빡임.

**판단:** OpenCV `imshow`는 같은 창 이름에 다른 크기 이미지를 넣으면 창이 리사이즈됨. 항상 동일한 크기를 유지해야 함.

**결론:** `depth_placeholder = np.zeros((orig_h, orig_w, 3))` 초기화. 항상 `np.hstack([frame, depth_placeholder])` 고정 크기로 표시. depth 결과 도착 시 placeholder 내용만 갱신.

---

## 7. FPS 개선 (스레딩)

**상황:** depth 추정이 매 N프레임마다 메인 루프를 블로킹 → 카메라 화면이 3~4초마다 끊김.

**판단:** depth 추정(CPU 집약)을 별도 스레드로 분리하면 카메라 화면은 30fps 유지 가능. 또한 모델 입력을 320×240으로 축소하면 추론 속도 2~3배 향상.

**결론:**
- `depth_worker` 백그라운드 스레드로 분리
- `threading.Lock`으로 결과 공유 보호
- 모델 입력 320×240 축소 (intrinsics도 이 크기 기준으로 변경)
- optical flow는 원본 해상도 유지 (특징점 추적 정확도)

---

## 8. 포인트 클라우드 누적 시도 → 실패

**상황:** 카메라를 돌리면 이전 방향의 3D 점이 사라짐. 누적 구현 요청.

**시도:** Visual Odometry 도입.
- `goodFeaturesToTrack` → `calcOpticalFlowPyrLK` → `findEssentialMat` → `recoverPose`
- 이동 행렬(R, t)으로 프레임 간 포즈 추정
- 각 프레임 점을 누적 world 좌표계로 변환

**실패 원인:**
1. `recoverPose`의 t는 단위벡터(크기 없음) → `t × DEPTH_SCALE × 0.1` 임의 스케일 적용
2. 단안 깊이 추정 오차 + 스케일 오차가 프레임마다 곱해져 지수적 발산
3. 결과: 3D 포인트 클라우드가 부채꼴로 폭발

**판단:** spike 환경(단안 카메라, 임의 깊이 스케일)에서는 누적에 필요한 정확한 pose를 얻을 수 없음. ARCore는 IMU(자이로+가속도계) + 카메라 융합으로 절대 pose 제공 → 누적 가능. 노트북에서는 ARCore 사용 불가.

**결론:** Visual Odometry 제거. 단순 프레임 교체 방식 복귀. 누적은 S24 ARCore 전환 후 구현.

---

## 9. 카메라 주기적 멈춤 원인 분석

**상황:** 백그라운드 스레딩 적용 후에도 카메라 화면이 2~4초 간격으로 주기적으로 멈춤.

**원인 분석:**
depth_worker 완료 주기와 freeze 주기가 일치 → result 도착 시 메인 루프 블로킹이 원인.

```
result 도착 시 메인 스레드 순차 실행:
  downsample_voxel(points, 0.02)    ← numpy, 100~500ms
  make_o3d_pointcloud(points)
  vis.remove_geometry(current_pcd)  ← O3D 씬 재할당
  vis.add_geometry(pcd)             ← O3D 씬 재구성
  vis.update_renderer()             ← GPU 렌더 완료까지 대기
```

이 5단계가 메인 루프를 통째로 블로킹. 포인트 수가 많을수록 누적 악화.

**판단:** `downsample_voxel`을 worker 스레드로 이동하고 최대 포인트 수 제한 필요. 단, ARCore 전환이 depth 품질 및 정확도 면에서 더 근본적 해결책이므로 노트북 spike에서의 최적화 우선순위는 낮음.

**결론:** 미수정 유지. ARCore + WebSocket 방식으로 전환 시 재설계.

---

## 10. 핸드폰 카메라 → 노트북 처리 방식 분석

**상황:** 노트북 단안 웹캠 + Depth-Anything v2는 물체 근처 왜곡 심함. S24 듀얼 카메라로 정확한 depth 획득하면서 처리는 노트북/서버에서 하고 싶음.

**원인(왜곡):** 단안 깊이 추정은 학습 기반 추론이므로 전경 물체(사람 등)가 크게 차지하면 배경과의 깊이 경계 오차 심함. 스테레오/LiDAR 방식은 이 문제 없음.

**분석한 옵션:**

| 방식 | depth 정확도 | 구현 난이도 | 비고 |
|------|------------|-----------|------|
| IP Webcam 앱 (WiFi 스트리밍) | 낮음 (Depth-Anything 그대로) | 매우 쉬움 | 카메라 품질만 개선 |
| ARCore depth + WebSocket | 높음 (실제 미터, ARCore) | 중간 | 왜곡 근본 해결 |
| CameraX 듀얼 스테레오 직접 구현 | 중간 | 어려움 | 별도 스테레오 매칭 필요 |

**판단:** ARCore depth + WebSocket 스트리밍이 최적.

```
[S24 Flutter 앱]
    ARFrame.acquireDepthImage() → Float32 depth (실제 미터)
    ARFrame.acquireImage()      → RGB
    WebSocket으로 노트북에 전송

[노트북 Python]
    WebSocket 수신
    기존 unproject() 그대로 사용 (DEPTH_SCALE 제거)
    Open3D 시각화
```

**장점:**
- depth 정확도 ARCore 수준 (cm 단위)
- 노트북 코드 변경 최소 (수신부 + DEPTH_SCALE 제거만)
- visitor_log 서버 업로드까지 자연스럽게 연결
- 왜곡 문제 근본 해결

**결론:** 다음 단계로 Flutter ARCore 앱 + WebSocket 스트리밍 구현. 노트북 spike는 구조 검증 완료로 종료.

---

## 11. 렌더링 병목 개선 적용

**상황:** 카메라 화면이 2~4초마다 주기적으로 멈추는 문제가 result 처리 시 메인 루프 블로킹임을 확인(§9). 즉시 적용 가능한 두 가지 개선을 적용.

**변경 1: `update_geometry` 교체**

**판단:** `remove_geometry + add_geometry`는 매 프레임 GPU 버퍼를 해제·재할당해 50~200ms 소요. 기존 버퍼에 데이터만 덮어쓰는 `update_geometry`를 쓰면 재할당 없이 5~20ms로 단축.

**결론:**
```
최초 1회: add_geometry(current_pcd)          ← GPU 버퍼 할당
이후 매 프레임: current_pcd.points = new_pcd.points
               current_pcd.colors = new_pcd.colors
               update_geometry(current_pcd)  ← 덮어씀만
```

**변경 2: `voxel_down_sample()` 교체**

**판단:** 자체 구현 `downsample_voxel`은 `np.unique(axis=0)` 기반 O(N logN), 10~100ms. Open3D 내장 `voxel_down_sample()`은 C++ 해시맵 기반 O(N), 1~5ms.

**결론:** `make_o3d_pointcloud(points).voxel_down_sample(VOXEL_SIZE)` 한 줄로 교체. numpy downsample 임포트 제거.

---

## 12. 구조 전문 분석 및 시퀀스·클래스 다이어그램 작성

**상황:** spike가 어느 정도 작동하게 되어 실제 서비스 전환을 위한 구조를 설계할 필요가 생김.

**판단:** 구현 전에 시퀀스 다이어그램으로 데이터 흐름을 검증하고 클래스 다이어그램으로 컴포넌트 책임을 명확히 해야 한다. 설계 단계에서 발견한 문제:
- 30fps 전송 시 WiFi 대역폭 초과 → 5fps throttle 결정
- depth(160×120)와 RGB(640×480) 해상도 불일치 → 전송 전 RGB를 depth 해상도로 리사이즈
- pose와 frame 분리 전송 시 불일치 가능 → 원자적 번들링 결정
- 처리 중 수신 프레임 누적 시 메모리 폭발 → 처리 중 신규 프레임 드롭

**결론:** `yj2trigger/visitor_log` README에 Mermaid 시퀀스·클래스 다이어그램과 설계 결정 근거 추가.

---

## 13. 병목 심층 분석 및 최적화 우선순위 결정

**상황:** 렌더링 병목 개선(§11) 후에도 카메라가 1.5~2초 주기로 멈추고, 3D 변환 시점마다 카메라가 정지함.

**분석:**

```
estimate_depth (CPU):     1.5~2s   ← 진짜 병목 (백그라운드 스레드에 있음)
unproject (numpy CPU):    50~100ms ← 메인 스레드 블로킹
voxel_down_sample (O3D):  1~5ms    ← 이미 개선됨
update_geometry:          5~20ms   ← 이미 개선됨
```

주기가 일정한 이유: depth_worker 완료 주기 = estimate_depth 소요 시간 = 1.5~2s. 완료될 때마다 메인 스레드에서 unproject가 추가로 블로킹.

**GPU 가속 검토:**
- Intel Iris Xe: DirectML 지원. ONNX + DirectML으로 400~700ms 예상
- Google Colab T4: 100~300ms 가능하나 웹캠이 로컬이라 RGB 프레임을 네트워크로 전송해야 함 → 왕복 지연 + Colab 세션 만료 문제
- 두 방법 모두 depth 추론 자체가 여전히 병목

**판단:** estimate_depth 자체가 spike 전용 임시 컴포넌트. ARCore 전환 시 하드웨어 depth를 30fps로 직접 제공 → 추론 불필요 → 병목 근본 제거. GPU 가속에 시간 투자하는 것보다 ARCore로 이행하는 게 효율적.

**결론:** S24 ARCore WebSocket 스트리밍으로 전환. 노트북 spike는 파이프라인 구조 검증 완료로 종료.

---

## 14. VSCode 정지 문제

**상황:** realtime.py 실행 중 VSCode 전체가 간헐적으로 정지.

**원인:** PyTorch CPU 추론 + Open3D 뷰어 + OpenCV 렌더링이 동시에 CPU/메모리 경쟁. VSCode Python 언어 서버도 같은 프로세스에서 경쟁.

**판단:** spike 실행을 VSCode 내부 터미널에서 하는 것 자체가 문제. VSCode는 편집기로만 쓰고 실행은 분리해야 한다.

**결론:** 이후 실행은 외부 cmd/PowerShell에서 `.venv\Scripts\activate` 후 `python spike/realtime.py`.

---

## 15. q / [ / ] 키 미작동 원인 분석 및 수정

**상황:** q로 종료, [ / ]로 저장 파일 선택이 작동하지 않음.

**원인:** `cv2.waitKey()`는 OpenCV 창에 포커스가 있어야 키를 감지. 3D Point Cloud(Open3D) 창을 보는 동안에는 항상 -1 반환. Open3D `register_key_action_callback`은 반대로 Open3D 창 포커스 필요. 두 창이 분리되어 있어 어느 쪽에 포커스를 줘도 절반의 키가 작동 안 함.

**판단:** 창 포커스와 무관하게 OS 키보드 상태를 직접 폴링하는 `keyboard` 모듈로 통합. `prev_keys` 딕셔너리로 이전 프레임 상태 추적해 키 홀드 중 반복 실행 방지(엣지 트리거).

**결론:** `cv2.waitKey()` 키 감지 제거, `register_key_action_callback` 제거. 모든 키(q, s, [, ]) `keyboard.is_pressed()` + 엣지 트리거로 통합.

---

## 16. viewer.py 신규 — 독립 뷰어

**상황:** 저장된 .ply 파일 확인 시 realtime.py를 실행해야 해서 Depth-Anything 모델 로드(~10초)와 웹캠 초기화까지 기다려야 함. 확인만 할 때 불편.

**판단:** 모델·웹캠 없이 .ply 파일만 로드하는 경량 뷰어를 별도 파일로 분리. 즉시 실행 가능.

**결론:** `spike/viewer.py` 생성. Open3D Visualizer + keyboard 폴링으로 [ / ] 파일 순환, W/X/A/D/화살표 이동.

---

## 17. 키 조작 개선 — scale 부호 방식 발견 및 회전 추가

**상황 1:** W와 X가 모두 같은 방향(뒤로)으로 이동. `vc.scale(1.1)` / `vc.scale(0.9)` 모두 양수라 동일 방향.

**원인:** Open3D `vc.scale()`은 곱셈 배율이 아닌 **부호로 방향을 결정하는 델타값**. 양수 = 앞, 음수 = 뒤.

**결론:** W → `vc.scale(-2)`, X → `vc.scale(2)` 로 수정.

**상황 2:** A/D가 이동만 되고 카메라 회전이 없어 3D 탐색이 불편.

**결론:** A/D → `vc.rotate(±10, 0)` (카메라 회전). 좌우 이동은 ←/→ 화살표로 이동.

---

## 18. server.py 신규 — ARCore WebSocket 수신 서버

**상황:** S24 ARCore 앱에서 depth + RGB + pose를 스트리밍받아 3D 시각화하는 서버 필요. realtime.py는 웹캠 전용이라 분리 필요.

**판단:** WebSocket 수신, 처리, 시각화를 독립 파일로. realtime.py와 시각화 로직 공유하되 카메라·모델 코드 없음. `asyncio + websockets`로 수신, 별도 스레드에서 unproject + voxel_down_sample.

**결론:** `spike/server.py` 생성. binary 프레임 포맷(header 92B + depth_bytes + rgb_bytes) 정의. ARCore 전환 시 DEPTH_SCALE 불필요(실제 미터값).

---

## 19. Flutter ARCore 앱 구현 — arcore_streamer

**상황:** S24 ARCore에서 depth + RGB + pose를 노트북으로 스트리밍하는 Flutter 앱 필요. `flutter create spike/arcore_streamer` 로 프로젝트 생성.

**구현 구조:**
- `lib/main.dart` (Dart): IP 입력 UI + EventChannel 구독 + WebSocket 전송
- `android/.../MainActivity.kt` (Kotlin): ARCore 세션 + GLSurfaceView + EventChannel 발행

**판단:** Flutter에서 ARCore Depth API 직접 접근 불가 → Kotlin 네이티브 코드 필수. EventChannel로 Dart에 binary 스트리밍. GLSurfaceView 1×1로 ARCore GL 컨텍스트만 확보 (화면 불필요).

---

## 20. 빌드 오류 연쇄 및 수정

| 오류 | 원인 | 해결 |
|------|------|------|
| 한글 경로 Gradle 거부 | `android.overridePathCheck` 미설정 | `gradle.properties`에 `android.overridePathCheck=true` 추가 |
| NDK 라이선스 미동의 | Platform Tools만 설치 (sdkmanager 없음) | Android Studio 설치 → SDK Manager → Command-line Tools + NDK 설치 → `flutter doctor --android-licenses` |
| `EGLConfig` import 충돌 | `android.opengl.EGLConfig` 대신 `javax.microedition.khronos.egl.EGLConfig` 필요 | import 교체 |
| `com.google.ar.core.Image` 미존재 | ARCore 1.46에서 해당 타입명 다름 | 타입 선언 제거, 로컬 변수 타입 추론으로 교체 |
| `adb install` 한글 경로 실패 | `aapt`가 한글 경로 APK 처리 불가 | `C:\temp\app-debug.apk`로 복사 후 설치 |

**판단:** 한글 경로는 Android 빌드 도구 전반에서 문제. 근본 해결은 프로젝트를 영문 경로로 이동. Spike이므로 우회책 유지.

---

## 21. `TextureNotSetException` — ARCore 텍스처 미설정

**상황:** 앱 설치 후 실행했으나 logcat에 `TextureNotSetException` 무한 반복.

**원인:** ARCore는 카메라 영상을 받을 OpenGL 텍스처 ID를 `session.setCameraTextureName(id)`로 등록해야 함. 등록 없이 `frame.update()` 하면 텍스처 바인딩 실패.

**판단:** `onSurfaceCreated`에서 `GLES20.glGenTextures()`로 텍스처 생성 후 세션 시작 전 등록해야 GL 컨텍스트가 유효한 상태에서 처리 가능.

**결론:** `onSurfaceCreated`에 텍스처 생성 + `session.setCameraTextureName(cameraTextureId)` 추가.

---

## 22. 권한 타이밍 문제 — `onRequestPermissionsResult`

**상황:** 텍스처 수정 후에도 ARCore 세션이 시작 안 됨. `setupSession()` 이 호출됐으나 session이 null.

**원인:** `setupSession()`이 `onSurfaceCreated` (GL 스레드)에서 호출되는데, 이 시점에 카메라 권한 요청 다이얼로그가 아직 안 닫혔거나 승인 전. 권한 없이 `Session(this)` 생성 시 예외로 실패.

**판단:** 권한 승인 결과는 `onRequestPermissionsResult`로 받음. 승인 시점에 세션을 재시도해야 함.

**결론:** `onRequestPermissionsResult` 추가 → 권한 허용 시 `setupSession()` 재호출.

---

## 23. 코드 품질 검토 — 4가지 개선

**상황:** 기능 구현 후 잠재적 버그 사전 검토.

| 문제 | 원인 | 개선 방향 | 효과 |
|------|------|---------|------|
| `NotYetAvailableException` 무한 발생 | TrackingState 체크 없이 depth 획득 시도 | `camera.trackingState != TRACKING`이면 return | ARCore 준비 전 불필요한 예외 제거 |
| 메모리 누수 | 예외 발생 시 `depthImg.close()` 미호출 | `finally` 블록에서 close | ARCore 이미지 버퍼 고갈 방지 |
| depth rowStride 무시 | `i * pixelStride`로 선형 접근 (행 경계 무시) | `row * rowStride + col * pixelStride`로 교체 | 해상도별 패딩 존재 시 오프셋 오류 방지 |
| `requestInstall` GL 스레드 호출 | ARCore 설치 확인은 UI 스레드 필요 | `runOnUiThread { setupSession() }` | 크래시 방지 |

---

## 24. `ResourceExhaustedException` — 이미지 버퍼 고갈

**상황:** 앱 재실행 후 `ResourceExhaustedException` 무한 반복.

**원인:** `onDrawFrame`이 60fps로 호출되는데, 이전 프레임 처리(픽셀 루프 등)가 완료되기 전에 다음 `acquireDepthImage16Bits()`가 호출됨. ARCore는 동시에 1개 이상의 이미지를 열어두는 것을 허용하지 않으므로 버퍼 고갈 발생. `Thread.sleep(33)`은 GL 스레드를 블로킹하지만 다음 `onDrawFrame` 호출을 막지 못함.

**판단:** 이전 처리가 끝나기 전에 새 처리를 시작하지 않아야 함. `@Volatile isProcessing` 플래그로 재진입 방지.

**결론:**
```kotlin
@Volatile private var isProcessing = false

fun processFrame() {
    if (isProcessing) return
    isProcessing = true
    try { ... } finally { isProcessing = false }
}
```
처리 중 새 프레임 진입 차단 → 버퍼 고갈 방지.

---

## 25. deploy.bat — 빌드·설치 자동화

**상황:** 매번 `flutter build apk`, `copy`, `adb install` 3단계를 수동으로 입력해야 해서 불편.

**판단:** 반복 작업이고 실수 여지 있음. 배치 스크립트로 단일 명령어화.

**결론:** `spike/arcore_streamer/deploy.bat` 생성.
```cmd
deploy.bat 192.168.35.202:44861
```
한 명령어로 빌드 → 복사 → S24 설치 완료.

---

## 26. BufferOverflowException — header 크기 오류

**상황:** ARCore 세션 시작 성공 후에도 `BufferOverflowException` 무한 반복. `depth: NxN` 로그가 나타나지 않아 overflow가 depth 처리 이전임을 확인.

**원인:**
```
header 실제 크기: 4×int32(16) + 4×float32(16) + 16×float32(64) = 96 bytes
코드: ByteBuffer.allocate(92)  ← 4 bytes 부족
→ poseMatrix 마지막 원소 putFloat 시 position=92 = limit → BufferOverflowException
```
server.py의 `HEADER_FMT` 주석도 "92 bytes"로 잘못 표기됨 (코드 자체는 `struct.calcsize`로 정확히 계산하므로 런타임 무결).

**판단:** 스펙 문서에서 92로 잘못 계산한 수치를 코드에 하드코딩. `struct.calcsize` 같은 계산 함수 사용이 아닌 수동 입력이라 검증 안 됨.

**결론:** `allocate(92)` → `allocate(96)`. server.py 주석 정정.

---

## 27. acquireCameraImage 실패 시 depthImg 누수

**상황:** 코드 검토 중 발견.

**원인:**
```kotlin
val depthImg = frame.acquireDepthImage16Bits()   // 성공
val camImg = frame.acquireCameraImage()           // 실패 시 예외
// inner try-finally 미진입 → depthImg.close() 미호출 → ARCore 버퍼 누수
```

**판단:** ARCore 이미지는 반드시 close() 해야 함. close() 미호출 시 버퍼 고갈 → `ResourceExhaustedException` 재발.

**결론:** 중첩 try-finally로 구조 변경:
```
val depthImg = acquireDepthImage16Bits()
try:
    val camImg = acquireCameraImage()
    try: 처리
    finally: camImg.close()
finally: depthImg.close()   ← camImg 실패해도 반드시 닫힘
```

---

## 28. deploy.bat — 강제 종료 + 자동 재실행 추가

**상황:** 매번 빌드 후 S24에서 앱을 수동으로 강제 종료 후 재실행해야 해서 반복적이고 번거로움.

**판단:** `adb shell am force-stop` + `adb shell am start`를 deploy.bat에 포함하면 한 명령어로 전 과정 자동화.

**결론:** deploy.bat를 4단계로 확장: 빌드 → 복사 → force-stop + 설치 → 자동 실행.

---

## 29. ARCore 연동 성공 — 프레임 전송 확인

**상황:** allocate(96) 수정 + 클린 빌드 + uninstall/install 조합으로 새 APK가 실제로 실행됨. `전송: 160x90` 로그 확인.

**결론:** ARCore depth + WebSocket → server.py 수신 파이프라인 전체 동작 확인.

---

## 30. 0 points 문제 — 빈 pcd가 Open3D에 추가됨

**상황:** 서버가 데이터를 받는데 Open3D 화면 흰색. `The number of points is 0 when creating axis-aligned bounding box` 경고.

**원인:** 카메라 엎어짐/추적 실패 프레임(유효 포인트 0)이 process_worker를 통해 빈 pcd로 Open3D에 추가됨. 이후 update_geometry가 빈 GPU 버퍼에서 올바르게 동작하지 않음.

**결론:** process_worker에서 유효 포인트 없으면 continue로 드롭. 빈 pcd는 result_queue에 넣지 않음.

---

## 31. intrinsics 스케일 오류 — "선 하나" 형태

**상황:** ARCore 데이터 정상 도착, Open3D에 포인트 뜨지만 "이상한 선 하나"만 표시.

**원인:** `camera.imageIntrinsics`는 카메라 이미지 해상도(예: 640×480) 기준 fx/fy/cx/cy. 하지만 depth 이미지는 160×90. 잘못된 비율로 역투영하면 XY 좌표가 극단적으로 찌그러져 선처럼 보임.

**판단:** depth 해상도 / 카메라 해상도 비율로 스케일 필요.
```kotlin
scaleX = dw / cw  // 160/640 = 0.25
fx_depth = fxCam * scaleX
cx_depth = cxCam * scaleX
```

**결론:** Kotlin `MainActivity.kt`에 intrinsics 스케일 코드 추가.

---

## 32. update_geometry 점 개수 변화 시 화면 소실

**상황:** 카메라 엎으면 포인트 클라우드가 사라지고 다시 들어도 복구 안 됨.

**원인:** `vis.update_geometry(current_pcd)` — 누적으로 점 개수가 늘어날 때 Open3D GPU 버퍼가 제대로 리사이즈되지 않음. 화면 소실 후 미복구.

**판단:** update_geometry 대신 remove_geometry + add_geometry로 매번 교체. 점 개수 변화에 안전.

**결론:**
```python
vis.remove_geometry(current_pcd, reset_bounding_box=False)
current_pcd = pcd
vis.add_geometry(current_pcd, reset_bounding_box=first)
```

---

## 33. TSDF 볼류메트릭 재구성 + ICP 포즈 정제 도입

**상황:** 단순 포인트 누적 방식은 여러 각도에서 스캔 시 부채꼴 아티팩트 발생. TSDF로 교체.

**TSDF 선택 이유:** 
- SDF 가중평균: 여러 번 관측한 표면은 SDF→0으로 수렴, 일시적 오인식은 양수로 밀려나 제거
- 사용자가 요청한 "여러 번 옳게 본 것에 맞추기"와 정확히 일치
- ICP: ARCore 포즈를 기존 TSDF에 맞게 미세 정렬, 누적 오차 보정

**미구현 / 향후 과제: Surface Completion**
스캔하지 않은 영역을 자동으로 채워 닫힌 공간을 완성하는 기능.
ARCore 스캔 데이터만으로는 실제 측정값이 없는 영역을 추론해야 하므로 연구 수준 알고리즘 필요.
Open3D 미지원. Poisson Surface Reconstruction은 부분적으로 가능하나 완전한 Room Completion은 별도 ML 모델 필요.

---

## 34. 역투영 Y·Z 부호 오류 — 쐐기 형태의 원인

**상황:** 평평한 벽을 스캔했을 때 앞/뒤에서 보면 직사각형(정상)이지만, 옆에서 보면 삼각형/쐐기 형태가 나타남.

**원인:** ARCore 공식 deprojection 수식과 코드가 다름.

| | ARCore 공식 | 기존 코드 (잘못됨) |
|--|--|--|
| Y | `(v-cy)/fy * d` | `-(v-cy)/fy * d` (부호 반전) |
| Z | `+depth` (양수) | `-depth` (음수) |

ARCore 카메라 좌표계는 X우·Y하·Z전방(OpenCV 방식) 사용. Y 부호 반전은 OpenGL 방식을 가정한 오류. Z = -depth는 OpenGL 렌더링 좌표를 가정한 오류.

**판단:** Y 부호 반전과 Z 부호가 포즈 행렬 적용 시 쐐기 왜곡을 만들었음. ARCore pose matrix가 이미 OpenCV→World 변환을 포함하므로 추가 부호 변환 불필요.

**결론:**
```python
Y = (vv - cy) / fy * depth   # 부호 반전 제거
Z = depth                     # 양수로 수정
```

---

## 35. ARCore(OpenGL) vs Open3D(OpenCV) 좌표계 불일치 — extrinsic 수정

**상황:** 평벽 스캔 시 앞/뒤 뷰가 서로 다르고, 측면에서 쐐기 형태 발생. 120°→180°+ 회전 오차.

**원인 분석:**
- ARCore 카메라 좌표계: OpenGL 방식 (Y위, Z뒤, 카메라 앞=-Z)
- Open3D TSDF가 기대하는 좌표계: OpenCV 방식 (Y아래, Z앞, 카메라 앞=+Z)
- 기존 코드: `extrinsic = inv(pose)` → OpenGL 규칙 그대로 Open3D에 전달
- Open3D가 OpenCV로 해석 → Y·Z 방향이 반전된 채 통합됨

**연쇄 효과:**
- 표면이 Y·Z 반전된 위치에 배치 → 쐐기/왜곡 형태
- 앞/뒤 뷰 비대칭
- 카메라 회전 시 Y·Z 반전이 회전 방향을 왜곡 → 120°가 180°+로 보임

**판단:** ARCore pose에 Y·Z 반전 행렬을 곱해 Open3D가 기대하는 좌표계로 변환 필요.

**결론:**
```python
flip_yz = np.diag([1.0, -1.0, -1.0, 1.0])
extrinsic = flip_yz @ np.linalg.inv(pose)
```

---

## 36. ARCore Anchor API — 상대 포즈 안정화 아이디어 (미적용)

**아이디어 배경:** camera.pose는 drift 발생 가능. ARCore Anchor는 지속적으로 위치 정제 → 포인트 클라우드 자동 정렬 가능.

**구현 방향 (검토용):**
```kotlin
val anchor = session.createAnchor(camera.pose)  // 첫 프레임에 생성
val relPose = anchor.pose.inverse().compose(camera.pose)  // anchor 기준 상대 포즈
relPose.toMatrix(poseMatrix, 0)
```

**적용 시 유용한 상황:** loop closure, 빠른 이동 후 재정렬, Cloud Anchor 공유.

---

## 다음 진행 순서

| 순서 | 작업 | 상태 |
|------|------|------|
| 1 | **flip_yz 효과 확인** — server.py extrinsic 수정이 쐐기 왜곡·회전 오차 해결하는지 검증 | ⏳ |
| 2 | 효과 없으면 **Anchor 기반 포즈**로 전환 — camera.pose → anchor 기준 상대 포즈 | 대기 |
| 3 | **VOXEL_SIZE 최적화** — 2cm 기준으로 정밀도·성능 균형 조정 | 대기 |
| 4 | **색상 추가** — 현재 그레이스케일, RGB로 전환 시 시각적 품질 향상 | 대기 |
| 5 | **Flutter ARCore 앱 → map-service-client 통합** | 대기 |
| 6 | **visitor_log FastAPI 서버** — 씬 저장·서빙 (Plan A) | 대기 |

---

## 현재 상태 (2026-06-29)

| 항목 | 상태 |
|------|------|
| 웹캠 실시간 3D 시각화 | ✅ 작동 |
| 카메라 창 깜빡임 | ✅ 수정 완료 |
| 백그라운드 스레딩 (FPS 개선) | ✅ 적용 |
| WASD 이동 | ✅ keyboard 모듈로 작동 |
| .ply 저장 + 블렌딩 시각화 | ✅ 작동 |
| 저장 파일 [ / ] 선택 | ✅ 작동 |
| 포인트 클라우드 누적 | ❌ ARCore 전환 후 구현 |
| 정확한 depth (미터) | ❌ ARCore 전환 후 해결 |
| 카메라 주기적 멈춤 | ⚠️ 원인 파악 완료. ARCore 전환으로 근본 해결 |
| GPU 가속 검토 | ✅ 분석 완료 — ARCore 전환이 더 효율적으로 결론 |
| VSCode 정지 | ✅ 외부 cmd 실행으로 해결 |
| 구조 설계 (시퀀스·클래스 다이어그램) | ✅ yj2trigger/visitor_log README에 추가 |
| q / [ / ] 키 미작동 | ✅ keyboard 모듈 엣지 트리거로 수정 |
| viewer.py (독립 뷰어) | ✅ 구현 완료 |
| server.py (WebSocket 수신) | ✅ 구현 완료 |
| Flutter ARCore 앱 | ✅ 구현 + 설치 완료 |
| ARCore → 서버 프레임 전송 | ✅ 확인 완료 (전송: 160x90) |
| intrinsics 스케일 오류 | ✅ depth/camera 비율로 수정 |
| update_geometry 점 개수 변화 소실 | ✅ remove+add 방식으로 교체 |
| 포인트 클라우드 누적 | ✅ process_worker accumulate 구현 |
| 부채꼴 패턴 | ⚠️ 스윕 스캔의 정상 결과 — 색상·pose 정확도 개선 필요 |

## 다음 단계

1. **Flutter ARCore 앱 구현** — `spike/arcore_streamer/` 에 ARCore depth + RGB + pose WebSocket 스트리밍
2. **포인트 클라우드 누적** — ARCore Pose × depth → 오차 없는 누적 (server.py에 추가)
3. `visitor_log` FastAPI 서버 구현 (Plan A — map-service-hub 확장)
