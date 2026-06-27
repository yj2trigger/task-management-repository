# visitor_log 처리 모듈 자연어 스펙

> 작성일: 2026-06-27 00:00
> 구현 위치: `c:\onedrive\_대학교\MAP\git\visitor_log\app\processing\`
> 역할: 이 문서가 설계 의도 SSOT. 코드는 여기서 파생.

---

## pointcloud.py

### 상수

```
POINT_FLOATS = 점 하나당 float 값 개수(x, y, z, r, g, b) = 6
POINT_BYTES  = POINT_FLOATS × float32 바이트 크기(4) = 24
```

### validate_and_parse(raw_bytes, expected_count) → (N,6) float32 배열

```
expected_bytes = expected_count × POINT_BYTES
raw_bytes 길이가 expected_bytes와 다르면 ValueError 발생
raw_bytes를 float32 dtype으로 해석하고 (expected_count, 6) 형태로 reshape해서 arr에 저장
arr 전체에 isfinite 검사 후 하나라도 False이면 ValueError 발생
arr 반환
```

### compress(arr) → bytes

```
arr을 float32 dtype으로 변환 후 raw 바이트열로 직렬화
level=3 설정으로 ZstdCompressor 생성
raw를 zstd 압축해서 반환
```

### decompress(compressed, point_count) → (N,6) float32 배열

```
max_size = point_count × POINT_BYTES
ZstdDecompressor 생성
compressed를 max_size 한도로 압축 해제해서 raw 획득
raw를 float32 dtype으로 해석하고 (point_count, 6) 형태로 reshape해서 반환
```

### downsample_voxel(arr, voxel_size=0.02) → (M,6) float32 배열

```
arr이 비어있으면 arr 그대로 반환
arr의 첫 세 열(xyz)을 voxel_size로 나누고 floor 취한 뒤 int32로 변환해서 voxel_indices에 저장
voxel_indices에서 np.unique(axis=0, return_index=True)로 유일한 복셀별 첫 등장 인덱스를 unique_idx로 추출
unique_idx를 오름차순 정렬
arr에서 정렬된 unique_idx에 해당하는 행만 선택해서 반환
```

---

## blend_zones.py

### smooth_step(edge0, edge1, x) → float

```
t = x를 edge0~edge1 범위로 clamp한 뒤 (x - edge0) / (edge1 - edge0)으로 정규화
결과 = t² × (3 - 2t) 계산해서 반환
```

GLSL smoothstep(edge0, edge1, x)와 동일.

### past_scene_alpha(frag_world_pos, anchor_world_positions, inner_radius=0.3, outer_radius=1.2) → float

```
anchor_world_positions가 비어있으면 0.0 반환
max_alpha = 0.0으로 초기화
anchor_world_positions의 각 anchor_pos에 대해:
    dist = frag_world_pos와 anchor_pos 사이의 유클리드 거리 계산
    alpha = 1.0에서 smooth_step(inner_radius, outer_radius, dist)를 빼서 계산
    max_alpha = max_alpha와 alpha 중 더 큰 값으로 갱신
max_alpha 반환
```

블렌딩 구역:

| 거리 | alpha | 표시 |
|------|-------|------|
| 0 ~ inner_radius (0.3m) | 1.0 | 과거 씬 100% |
| inner ~ outer (0.3~1.2m) | SmoothStep | 전환 |
| outer 이상 (1.2m~) | 0.0 | 현재 카메라만 |
| 앵커 여러 개 겹침 | max(α1, α2...) | bubble 공존 |

---

## spike/realtime.py 자연어 스펙

> 구현 위치: `c:\onedrive\_대학교\MAP\git\visitor_log\spike\realtime.py`

### 설정 상수

```
CAMERA_INDEX    = 0      기본 웹캠 인덱스
PROCESS_EVERY_N = 5      매 N프레임마다 depth 추정 (성능 조절)
VOXEL_SIZE      = 0.02   다운샘플 복셀 크기 (미터)
DEPTH_SCALE     = 5.0    spike 전용 — 모델 출력(0~1) → 미터 변환 배율. ARCore 전환 시 삭제
MAX_DEPTH       = 10.0   이 거리 초과 점 제거 (미터)
MOVE_SPEED      = 0.1    1인칭 키보드 이동 속도 (미터/키입력)
```

### load_model() → depth 추정 파이프라인

```
transformers의 depth-estimation 파이프라인을
depth-anything/Depth-Anything-V2-Small-hf 모델로 생성해 반환
```

### frame_to_rgb(frame) → (H,W,3) float32 배열

```
OpenCV BGR 프레임을 RGB 순서로 변환
255로 나눠 0~1 정규화해 반환
```

### estimate_depth(pipe, rgb_arr) → (H,W) float32 배열

```
rgb_arr을 PIL Image로 변환
pipe에 입력해 depth 이미지 획득
255로 나눠 0~1 정규화
DEPTH_SCALE 곱해 미터 단위로 변환해 반환
```

### estimate_intrinsics(w, h) → (fx, fy, cx, cy)

```
수직 FOV 60도를 라디안으로 변환
fy = h / (2 × tan(FOV/2)) 계산
fx = fy로 설정 (정사각 픽셀 가정)
cx = w/2, cy = h/2로 설정
fx, fy, cx, cy 반환
```

### unproject(rgb, depth, fx, fy, cx, cy) → (N,6) float32 배열

```
h, w = depth 형태에서 추출
meshgrid로 uu, vv 픽셀 좌표 격자 생성
mask = depth가 0 초과이고 MAX_DEPTH 이하인 픽셀
X = (uu - cx) / fx × depth
Y = (vv - cy) / fy × depth
Z = depth
mask 적용해 xyz 배열 생성
rgb에 mask 적용해 rgb_flat 추출
xyz와 rgb_flat 이어붙여 (N,6) float32 배열 반환
```

### make_o3d_pointcloud(points) → Open3D PointCloud 객체

```
Open3D PointCloud 객체 생성
points의 xyz를 PointCloud의 points로 설정
points의 rgb를 PointCloud의 colors로 설정
PointCloud 객체 반환
```

### save_ply(points, path)

```
n = len(points)
ply 헤더 문자열 생성 (포맷·요소수·x,y,z,r,g,b 선언 포함)
points의 xyz 추출
points의 rgb를 0~255 uint8로 변환
path에 파일 열기
헤더 쓰기
각 점마다 x y z r g b 한 줄씩 쓰기
```

### visualize_blend(points, anchor_positions)

```
points 앞 5000개에 대해 각각 past_scene_alpha 계산해 alphas 배열 생성
3D scatter plot 생성 (x, z, y 순, alpha값을 RdBu_r 색상으로)
컬러바 추가
spike/output/blend_alpha.png로 저장
```

### on_key(vis, key, action) — 1인칭 카메라 키 콜백

```
action이 KEY_DOWN이 아니면 False 반환
W: eye[2], lookat[2]를 MOVE_SPEED 증가
S: eye[2], lookat[2]를 MOVE_SPEED 감소
A: eye[0], lookat[0]를 MOVE_SPEED 감소
D: eye[0], lookat[0]를 MOVE_SPEED 증가
↑: eye[1], lookat[1]를 MOVE_SPEED 증가
↓: eye[1], lookat[1]를 MOVE_SPEED 감소
변경된 eye, lookat, up을 뷰어 카메라에 적용
False 반환
```

### main()

```
spike/output 디렉토리 생성
load_model()로 depth 파이프라인 생성
VideoCapture(CAMERA_INDEX)로 웹캠 열기 — 실패 시 종료
Open3D VisualizerWithKeyCallback 생성
W/S/A/D/↑/↓ 키에 on_key 콜백 등록
frame_count, current_pcd, latest_points = 0, None, None 초기화

루프 (웹캠 열린 동안):
    프레임 읽기 — 실패 시 종료
    frame_count += 1

    frame_count % PROCESS_EVERY_N == 0 일 때:
        frame_to_rgb → rgb
        estimate_depth → depth
        estimate_intrinsics → fx, fy, cx, cy
        unproject → points
        downsample_voxel → points
        latest_points = points
        make_o3d_pointcloud → pcd
        current_pcd 있으면 뷰어에서 제거
        pcd 뷰어에 추가, current_pcd = pcd
        depth를 COLORMAP_MAGMA로 변환 → depth_vis
        frame과 depth_vis 가로 이어붙여 'Camera + Depth' 창 표시

    vis.poll_events(), vis.update_renderer()

    's' 키 && latest_points 있으면:
        save_ply(latest_points, output/scene.ply)
        visualize_blend(latest_points, [[0,0,2], [0.5,0,3]])
    'q' 키이면 루프 종료

웹캠 해제, 뷰어 닫기, OpenCV 창 닫기
```
