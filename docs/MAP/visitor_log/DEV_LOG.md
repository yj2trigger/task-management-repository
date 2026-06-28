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

## 현재 상태 (2026-06-28)

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
| 카메라 주기적 멈춤 | ⚠️ 원인 파악 완료. ARCore 전환 시 재설계 |

## 다음 단계

1. **Flutter ARCore 앱 구현** — ARFrame depth + RGB를 WebSocket으로 노트북에 스트리밍
2. **노트북 수신부 구현** — WebSocket 수신 + DEPTH_SCALE 제거 + 기존 unproject 재사용
3. **포인트 클라우드 누적** — ARCore Pose × ARCore depth → 정확한 누적
4. `visitor_log` FastAPI 서버 구현 (Plan A — map-service-hub 확장)
