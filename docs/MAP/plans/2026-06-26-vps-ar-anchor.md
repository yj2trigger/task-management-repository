# VPS·AR 앵커 기능 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> 작성일: 2026-06-26 21:30
> 원본 스펙: [VPS_AR_SPEC.md](../VPS_AR_SPEC.md)

**Goal:** 여행지에서 AR 앵커(공중 글씨)를 VPS 기반으로 장소에 고정·공유하는 기능을 `map-service-client`(Flutter)에 추가하고, 백엔드는 `map-service-hub`(FastAPI)에 확장한다.

**Architecture:** Immersal Cloud REST API로 맵을 관리하고, `map-service-hub`에 좌표계·앵커 도메인을 추가한다. Flutter 클라이언트는 `lib/features/ar/` 피처로 AR 세션·손 추적·앵커 렌더링을 담당하며, 기존 네이버맵·geolocator·http 패키지를 재사용한다.

**Tech Stack:**
- 백엔드: `map-service-hub` — FastAPI 0.136, SQLAlchemy 2 async, psycopg3, GeoAlchemy2+PostGIS, Alembic, httpx
- 모바일: `map-service-client` — Flutter 3.11.4 / Dart 3.x, `ar_flutter_plugin`, `google_mlkit_hand_landmark_detection`, 기존 `http`·`geolocator`·`flutter_naver_map` 재사용
- VPS: Immersal Cloud REST API v2 (Flutter SDK 없음 — REST 직접 호출)
- 인증: `map-service-user`가 발급한 RS256 JWT → hub에서 공개키로 검증

---

## 스펙 비판 — 수정된 결정사항

| 모순 | 채택 해결책 |
|------|----------|
| "사전작업 불필요" ↔ 첫 사용자 전체 스캔 필수 | 인기 여행지 seed 맵은 운영팀 제공. 미등록 장소는 "개척 모드" UX로 프레이밍. |
| 1회 여행객 ↔ crowd-source 동기 부재 | "내 앵커를 다음 여행객이 본다" 소셜 프레이밍. 앵커에 작성자 닉네임 표시. |
| 조명 의존성 미해결 | 스캔 시 조도 체크(50lux 미만 경고). LiDAR 보조(ARKit 자동). 매칭 실패 fallback 안내. |
| 실내 GPS 한계 | GPS 반경 500m 내 좌표계 목록 + 썸네일 선택. 없으면 전체 지도 탐색. |
| Immersal Flutter SDK 없음 | Immersal REST API v2를 httpx(hub) + http(client)로 직접 호출. |
| ~~손가락 획 → 텍스트 변환~~ | **인접 객체 기준 상대 6DOF 폴리라인 저장** — 위치·방향 모두 탐지된 인접 객체의 로컬 프레임 기준으로 기록. `ref`(객체 포즈 in Immersal) + `rel`(앵커의 객체 기준 상대 포즈) + `strokes`(2D 획). 렌더링 시 객체 재탐지 → 상대 트랜스폼 적용. VPS drift가 글씨 방향에 영향 없음. |

---

## Global Constraints

- `map-service-hub`: Python 3.12, FastAPI 0.136.x, SQLAlchemy 2 async — 기존 버전 고정
- `map-service-client`: Flutter 3.11.4, Dart ^3.x
- SQLAlchemy 2 async 패턴: `async with get_hub_db().session() as s:` (hub_db.py 기존 패턴 준수)
- DB 스키마 변경은 Alembic 마이그레이션 직접 작성 (`--autogenerate` 금지)
- JWT: `map-service-user` RS256 공개키를 `HUB_JWT_PUBLIC_KEY` 환경변수로 hub에 주입
- 앵커 데이터는 **인접 객체 기준 상대 6DOF 폴리라인** — `stroke_data JSONB`
- `stroke_data` 스키마: `{ref:{pos:[x,y,z], rot:[qx,qy,qz,qw]}, rel:{pos:[dx,dy,dz], rot:[qx,qy,qz,qw]}, strokes:[[[u,v]...]], stroke_width:float}`
- `ref`: 탐지된 인접 객체 포즈 (Immersal 절대 공간). `rel`: 앵커의 해당 객체 로컬 프레임 기준 상대 포즈
- 지리 쿼리: PostGIS `ST_DWithin(geography)` 사용 (geoalchemy2 이미 설치됨)
- Flutter 기존 패키지(`http`, `geolocator`, `flutter_naver_map`) 재사용 — 불필요한 추가 금지

---

## 서브시스템 분리

| 계획 | 범위 | 선행 조건 |
|------|------|---------|
| **Plan A (이 문서)** | Hub 백엔드 API + Flutter 데이터 레이어 | 없음 |
| Plan B | Flutter AR 스캔·로컬라이제이션 (ar_flutter_plugin + Immersal) | Plan A |
| Plan C | Flutter 3D 손가락 글씨 (MediaPipe Hand Landmark) | Plan B — POC 필수. 정확도 70% 미달 시 UX 재설계 |
| Plan D | Flutter 앵커 렌더링 + 미니맵 (네이버맵 2D 오버레이) | Plan C |

---

## Plan A: Hub 백엔드 API + Flutter 데이터 레이어

### 파일 구조

```
# map-service-hub (추가/수정)
app/
  clients/immersal_client.py      ← Immersal REST API v2 래퍼 (httpx)
  db/ar_repo.py                   ← coordinate_systems·anchors 비동기 쿼리
  routers/ar_routers.py           ← FastAPI AR 엔드포인트
  schemas/ar_schemas.py           ← Pydantic 요청/응답 모델
  utils/auth.py                   ← RS256 JWT 검증 FastAPI Depends
  config.py                       ← IMMERSAL_TOKEN, HUB_JWT_PUBLIC_KEY 추가 (수정)
  main.py                         ← ar_routers 등록 (수정)
migrations/versions/XXXX_ar_tables.py

# map-service-client (추가/수정)
lib/
  data/
    models/ar_model.dart
    repositories/ar_repository.dart
  features/ar/
    screens/
      ar_map_screen.dart          ← 좌표계 선택 지도 화면
      ar_scanner_screen.dart      ← 스캔·매칭 화면 (Plan B)
      ar_write_screen.dart        ← 3D 글씨 화면 (Plan C)
      ar_anchor_view_screen.dart  ← 앵커 확인 화면 (Plan D)
    widgets/
      coordinate_system_card.dart
pubspec.yaml                      ← ar_flutter_plugin, google_mlkit_hand_landmark_detection 추가
```

---

### Task 1: Hub — Alembic 마이그레이션

**Files:**
- Create: `migrations/versions/XXXX_ar_tables.py`

- [ ] **Step 1: 마이그레이션 파일 생성**

  ```bash
  cd map-service-hub
  alembic revision -m "ar_tables"
  ```

- [ ] **Step 2: 마이그레이션 내용 작성**

  ```python
  # migrations/versions/XXXX_ar_tables.py
  """ar_tables — Revision ID: <alembic 생성값>"""
  from alembic import op
  import sqlalchemy as sa

  def upgrade() -> None:
      op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
      op.create_table(
          "coordinate_systems",
          sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
          sa.Column("immersal_map_id", sa.String(64), nullable=False, unique=True),
          sa.Column("name", sa.String(100), nullable=False),
          sa.Column("description", sa.String(500), nullable=True),
          sa.Column("location", sa.Text, nullable=False),  # WKT → geography 변환
          sa.Column("thumbnail_url", sa.String(500), nullable=True),
          sa.Column("created_by", sa.BigInteger, nullable=False),
          sa.Column("created_at", sa.DateTime(timezone=True),
                    server_default=sa.text("NOW()"), nullable=False),
      )
      op.execute("""
          ALTER TABLE coordinate_systems
          ALTER COLUMN location TYPE geography(Point,4326)
          USING ST_GeogFromText(location)
      """)
      op.create_index(
          "idx_cs_location", "coordinate_systems",
          [sa.text("location")], postgresql_using="gist"
      )
      op.create_table(
          "anchors",
          sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
          sa.Column("coordinate_system_id", sa.BigInteger,
                    sa.ForeignKey("coordinate_systems.id", ondelete="CASCADE"),
                    nullable=False),
          # 폴리라인 원본 저장 (텍스트 변환 없음)
          # 스키마: {anchor_point:[x,y,z], normal:[nx,ny,nz],
          #          strokes:[[[u,v],...]], stroke_width:float}
          sa.Column("stroke_data", sa.Text, nullable=False),  # JSONB 변환 (아래)
          sa.Column("created_by", sa.BigInteger, nullable=False),
          sa.Column("created_at", sa.DateTime(timezone=True),
                    server_default=sa.text("NOW()"), nullable=False),
      )
      # JSONB로 타입 변환 (SQLAlchemy Text → JSONB)
      op.execute("ALTER TABLE anchors ALTER COLUMN stroke_data TYPE JSONB USING stroke_data::jsonb")
      op.create_index("idx_anchors_cs", "anchors", ["coordinate_system_id"])

  def downgrade() -> None:
      op.drop_table("anchors")
      op.drop_table("coordinate_systems")
  ```

- [ ] **Step 3: 마이그레이션 적용 확인**

  ```bash
  alembic upgrade head
  ```
  Expected: `Running upgrade ... -> XXXX, ar_tables`

- [ ] **Step 4: Commit**

  ```bash
  git add migrations/
  git commit -m "feat(ar): coordinate_systems·anchors Alembic 마이그레이션"
  ```

---

### Task 2: Hub — ar_schemas.py

**Files:**
- Create: `app/schemas/ar_schemas.py`

- [ ] **Step 1: 테스트 먼저 작성**

  `tests/test_ar_schemas.py`:
  ```python
  import pytest
  from pydantic import ValidationError
  from app.schemas.ar_schemas import AnchorCreate, CoordinateSystemCreate

  def test_anchor_strokes_빈_배열_거부():
      with pytest.raises(ValidationError):
          AnchorCreate(
              ref={"pos": [0,0,0], "rot": [0,0,0,1]},
              rel={"pos": [0,0,0], "rot": [0,0,0,1]},
              strokes=[])

  def test_anchor_stroke_width_음수_거부():
      with pytest.raises(ValidationError):
          AnchorCreate(
              ref={"pos": [0,0,0], "rot": [0,0,0,1]},
              rel={"pos": [0,0,0], "rot": [0,0,0,1]},
              strokes=[[[0,0],[1,1]]], stroke_width=-0.001)

  def test_위도_범위_초과_거부():
      with pytest.raises(ValidationError):
          CoordinateSystemCreate(
              immersal_map_id="x", name="n", latitude=91.0, longitude=0.0)

  def test_anchor_stroke_width_기본값():
      a = AnchorCreate(
          ref={"pos": [1,2,3], "rot": [0,0,0,1]},
          rel={"pos": [0,0,0], "rot": [0,0,0,1]},
          strokes=[[[0,0],[1,1]]])
      assert a.stroke_width == 0.003
  ```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

  ```bash
  pytest tests/test_ar_schemas.py -v
  ```
  Expected: FAIL (모듈 없음)

- [ ] **Step 3: ar_schemas.py 구현**

  ```python
  # app/schemas/ar_schemas.py
  from __future__ import annotations
  from datetime import datetime
  from typing import Annotated
  from pydantic import BaseModel, Field, field_validator


  class CoordinateSystemCreate(BaseModel):
      immersal_map_id: str = Field(min_length=1, max_length=64)
      name: str = Field(min_length=1, max_length=100)
      description: str | None = Field(default=None, max_length=500)
      latitude: float = Field(ge=-90.0, le=90.0)
      longitude: float = Field(ge=-180.0, le=180.0)
      thumbnail_url: str | None = Field(default=None, max_length=500)


  class CoordinateSystemSummary(BaseModel):
      id: int
      name: str
      latitude: float
      longitude: float
      thumbnail_url: str | None
      model_config = {"from_attributes": True}


  class CoordinateSystemDetail(BaseModel):
      id: int
      immersal_map_id: str
      name: str
      description: str | None
      latitude: float
      longitude: float
      thumbnail_url: str | None
      created_by: int
      created_at: datetime
      model_config = {"from_attributes": True}


  # 단위 쿼터니언 [qx, qy, qz, qw]
  _Quat = Annotated[list[float], Field(min_length=4, max_length=4)]
  _Vec3 = Annotated[list[float], Field(min_length=3, max_length=3)]


  class ObjectPose(BaseModel):
      """인접 객체 포즈 (Immersal 절대 공간 또는 로컬 상대 공간)."""
      pos: _Vec3
      rot: _Quat


  class StrokeData(BaseModel):
      """앵커 전체 데이터.

      ref: 탐지된 인접 객체의 Immersal 공간 포즈 (위치+방향).
           렌더링 시 이 포즈 근처에서 동일 객체를 재탐지하는 기준.
      rel: 앵커의 ref 객체 로컬 프레임 기준 상대 포즈 (위치+방향).
           객체 탐지 후 이 트랜스폼을 적용해 앵커 월드 포즈 계산.
      strokes: 앵커 로컬 평면 기준 2D 획 배열 (미터 단위).
      stroke_width: 렌더링 선 굵기 (미터).
      """
      ref: ObjectPose
      rel: ObjectPose
      strokes: Annotated[list[list[list[float]]], Field(min_length=1)]
      stroke_width: float = Field(default=0.003, gt=0)

      @field_validator("strokes")
      @classmethod
      def strokes_min_two_points(cls, v: list) -> list:
          if any(len(s) < 2 for s in v):
              raise ValueError("each stroke must have at least 2 points")
          return v


  class AnchorCreate(StrokeData):
      pass


  class AnchorResponse(BaseModel):
      id: int
      coordinate_system_id: int
      stroke_data: dict   # StrokeData JSON 그대로 반환
      created_by: int
      created_at: datetime
      model_config = {"from_attributes": True}


  class MapDownloadUrlResponse(BaseModel):
      url: str
  ```

- [ ] **Step 4: 테스트 통과 확인 + Commit**

  ```bash
  pytest tests/test_ar_schemas.py -v
  git add app/schemas/ar_schemas.py tests/test_ar_schemas.py
  git commit -m "feat(ar): Pydantic 스키마 (좌표계·앵커·다운로드 URL)"
  ```

---

### Task 3: Hub — ar_repo.py

**Files:**
- Create: `app/db/ar_repo.py`

**Interfaces:**
- Produces: `find_coordinate_systems_nearby(lat, lng, radius_m)`, `create_coordinate_system(data, user_id)`, `get_coordinate_system(cs_id)`, `create_anchor(cs_id, data, user_id)`, `list_anchors(cs_id)`, `delete_anchor(anchor_id, user_id) -> bool`

- [ ] **Step 1: 통합 테스트 작성 (실 PostGIS DB 필요)**

  `tests/test_ar_repo.py`:
  ```python
  import pytest
  from app.db.ar_repo import (
      create_coordinate_system, find_coordinate_systems_nearby,
      create_anchor, delete_anchor,
  )
  from app.schemas.ar_schemas import CoordinateSystemCreate, AnchorCreate

  @pytest.mark.asyncio
  async def test_좌표계_생성_반경_조회():
      cs = await create_coordinate_system(
          CoordinateSystemCreate(
              immersal_map_id="test-001", name="덕수궁 정문",
              latitude=37.5659, longitude=126.9750,
          ), user_id=1
      )
      assert cs["name"] == "덕수궁 정문"
      nearby = await find_coordinate_systems_nearby(37.5659, 126.9750, 100.0)
      assert any(r["id"] == cs["id"] for r in nearby)

  @pytest.mark.asyncio
  async def test_앵커_삭제_권한():
      cs = await create_coordinate_system(
          CoordinateSystemCreate(
              immersal_map_id="test-002", name="테스트",
              latitude=37.0, longitude=127.0,
          ), user_id=1
      )
      from app.schemas.ar_schemas import ObjectPose
      stroke = AnchorCreate(
          ref=ObjectPose(pos=[1.0, 0.5, -2.0], rot=[0, 0, 0, 1]),
          rel=ObjectPose(pos=[0.0, 0.0, 0.05], rot=[0, 0, 0, 1]),
          strokes=[[[0.0, 0.0], [0.1, 0.1], [0.2, 0.0]]],
      )
      anchor = await create_anchor(cs["id"], stroke, user_id=1)
      assert anchor["stroke_data"]["ref"]["pos"] == [1.0, 0.5, -2.0]
      assert await delete_anchor(anchor["id"], user_id=99) is False
      assert await delete_anchor(anchor["id"], user_id=1) is True
  ```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

  ```bash
  pytest tests/test_ar_repo.py -v
  ```

- [ ] **Step 3: ar_repo.py 구현**

  ```python
  # app/db/ar_repo.py
  """AR 도메인 비동기 DB 쿼리.

  PostGIS ST_DWithin(geography) 로 meter 단위 반경 조회.
  패턴: async with get_hub_db().session() as s (hub_db.py 준수).
  """
  from __future__ import annotations
  from sqlalchemy import text
  from app.db.hub_db import get_hub_db
  from app.schemas.ar_schemas import AnchorCreate, CoordinateSystemCreate


  async def find_coordinate_systems_nearby(
      lat: float, lng: float, radius_m: float = 500.0
  ) -> list[dict]:
      sql = text("""
          SELECT id, name,
                 ST_Y(location::geometry) AS latitude,
                 ST_X(location::geometry) AS longitude,
                 thumbnail_url,
                 ST_Distance(location, ST_MakePoint(:lng, :lat)::geography) AS dist_m
          FROM coordinate_systems
          WHERE ST_DWithin(location, ST_MakePoint(:lng, :lat)::geography, :radius)
          ORDER BY dist_m LIMIT 50
      """)
      async with get_hub_db().session() as s:
          rows = (await s.execute(sql, {"lat": lat, "lng": lng, "radius": radius_m})).mappings().all()
      return [dict(r) for r in rows]


  async def create_coordinate_system(data: CoordinateSystemCreate, user_id: int) -> dict:
      sql = text("""
          INSERT INTO coordinate_systems
              (immersal_map_id, name, description, location, thumbnail_url, created_by)
          VALUES (:map_id, :name, :desc,
                  ST_MakePoint(:lng, :lat)::geography, :thumb, :user_id)
          RETURNING id, immersal_map_id, name, description,
                    ST_Y(location::geometry) AS latitude,
                    ST_X(location::geometry) AS longitude,
                    thumbnail_url, created_by, created_at
      """)
      async with get_hub_db().session() as s:
          row = (await s.execute(sql, {
              "map_id": data.immersal_map_id, "name": data.name, "desc": data.description,
              "lat": data.latitude, "lng": data.longitude,
              "thumb": data.thumbnail_url, "user_id": user_id,
          })).mappings().one()
      return dict(row)


  async def get_coordinate_system(cs_id: int) -> dict | None:
      sql = text("""
          SELECT id, immersal_map_id, name, description,
                 ST_Y(location::geometry) AS latitude,
                 ST_X(location::geometry) AS longitude,
                 thumbnail_url, created_by, created_at
          FROM coordinate_systems WHERE id = :id
      """)
      async with get_hub_db().session() as s:
          row = (await s.execute(sql, {"id": cs_id})).mappings().one_or_none()
      return dict(row) if row else None


  async def create_anchor(cs_id: int, data: AnchorCreate, user_id: int) -> dict:
      import json
      sql = text("""
          INSERT INTO anchors (coordinate_system_id, stroke_data, created_by)
          VALUES (:cs_id, :stroke_data::jsonb, :user_id)
          RETURNING id, coordinate_system_id, stroke_data, created_by, created_at
      """)
      async with get_hub_db().session() as s:
          row = (await s.execute(sql, {
              "cs_id": cs_id,
              "stroke_data": json.dumps(data.model_dump()),
              "user_id": user_id,
          })).mappings().one()
      return dict(row)


  async def list_anchors(cs_id: int) -> list[dict]:
      sql = text("""
          SELECT id, coordinate_system_id, stroke_data, created_by, created_at
          FROM anchors WHERE coordinate_system_id = :cs_id ORDER BY created_at
      """)
      async with get_hub_db().session() as s:
          rows = (await s.execute(sql, {"cs_id": cs_id})).mappings().all()
      return [dict(r) for r in rows]


  async def delete_anchor(anchor_id: int, user_id: int) -> bool:
      """본인 앵커만 삭제. 타인 또는 미존재 → False."""
      sql = text("""
          DELETE FROM anchors WHERE id = :id AND created_by = :user_id RETURNING id
      """)
      async with get_hub_db().session() as s:
          row = (await s.execute(sql, {"id": anchor_id, "user_id": user_id})).one_or_none()
      return row is not None
  ```

- [ ] **Step 4: 테스트 통과 + Commit**

  ```bash
  pytest tests/test_ar_repo.py -v
  git add app/db/ar_repo.py tests/test_ar_repo.py
  git commit -m "feat(ar): AR DB 레포지토리 (PostGIS 반경 쿼리, 앵커 CRUD)"
  ```

---

### Task 4: Hub — immersal_client.py

**Files:**
- Create: `app/clients/immersal_client.py`
- Modify: `app/config.py` — `IMMERSAL_TOKEN`, `IMMERSAL_API_URL`
- Modify: `app/main.py` — lifespan shutdown에 `dispose_immersal_client`

- [ ] **Step 1: 테스트 작성**

  `tests/test_immersal_client.py`:
  ```python
  import pytest, httpx
  from unittest.mock import AsyncMock, patch
  from app.clients.immersal_client import get_map_download_url, submit_scan

  @pytest.mark.asyncio
  async def test_get_map_download_url():
      mock_resp = httpx.Response(200, json={"url": "https://cdn.immersal.com/abc.bytes"})
      with patch("app.clients.immersal_client.get_immersal_client") as mg:
          mg.return_value.get = AsyncMock(return_value=mock_resp)
          url = await get_map_download_url("abc123")
      assert url == "https://cdn.immersal.com/abc.bytes"

  @pytest.mark.asyncio
  async def test_submit_scan():
      mock_resp = httpx.Response(200)
      with patch("app.clients.immersal_client.get_immersal_client") as mg:
          mg.return_value.post = AsyncMock(return_value=mock_resp)
          await submit_scan("abc123", b"\x00\x01")
          mg.return_value.post.assert_called_once()
  ```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

  ```bash
  pytest tests/test_immersal_client.py -v
  ```

- [ ] **Step 3: immersal_client.py 구현**

  ```python
  # app/clients/immersal_client.py
  """Immersal Cloud REST API v2 클라이언트 (httpx AsyncClient 싱글톤).
  API 상세: https://developers.immersal.com/docs/rest-api/
  """
  from __future__ import annotations
  import httpx
  from app.config import settings

  _client: httpx.AsyncClient | None = None


  def get_immersal_client() -> httpx.AsyncClient:
      global _client
      if _client is None:
          _client = httpx.AsyncClient(
              base_url=settings.IMMERSAL_API_URL,
              headers={"Authorization": f"Bearer {settings.IMMERSAL_TOKEN}"},
              timeout=30.0,
          )
      return _client


  async def dispose_immersal_client() -> None:
      global _client
      if _client is not None:
          await _client.aclose()
          _client = None


  async def get_map_download_url(map_id: str) -> str:
      """맵 파일 서명 다운로드 URL 발급.
      Flutter 클라이언트가 직접 다운로드 — 서버 대역폭 불필요.
      """
      resp = await get_immersal_client().get(f"/v2/maps/{map_id}/download")
      resp.raise_for_status()
      return resp.json()["url"]


  async def submit_scan(map_id: str, scan_bytes: bytes) -> None:
      """스캔 데이터 업로드 (crowd-source 기여). Immersal이 비동기 병합."""
      resp = await get_immersal_client().post(
          f"/v2/maps/{map_id}/scans",
          content=scan_bytes,
          headers={"Content-Type": "application/octet-stream"},
      )
      resp.raise_for_status()
  ```

- [ ] **Step 4: config.py 수정**

  ```python
  IMMERSAL_TOKEN: str = ""
  IMMERSAL_API_URL: str = "https://api.immersal.com"
  ```

- [ ] **Step 5: main.py lifespan shutdown에 추가**

  ```python
  from app.clients.immersal_client import dispose_immersal_client
  # lifespan shutdown 단계:
  await dispose_immersal_client()
  ```

- [ ] **Step 6: 테스트 통과 + Commit**

  ```bash
  pytest tests/test_immersal_client.py -v
  git add app/clients/immersal_client.py app/config.py app/main.py tests/test_immersal_client.py
  git commit -m "feat(ar): Immersal REST API 클라이언트"
  ```

---

### Task 5: Hub — JWT 검증 Depends

**Files:**
- Create: `app/utils/auth.py`
- Modify: `app/config.py` — `HUB_JWT_PUBLIC_KEY`
- Modify: `requirements.txt` — `PyJWT[crypto]`

- [ ] **Step 1: PyJWT 추가**

  `requirements.txt`:
  ```
  # [Auth]
  PyJWT[crypto]>=2.10.1,<3.0
  ```
  ```bash
  pip install "PyJWT[crypto]>=2.10.1,<3.0"
  ```

- [ ] **Step 2: 테스트 작성**

  `tests/test_auth.py`:
  ```python
  import pytest, jwt
  from unittest.mock import patch
  from cryptography.hazmat.primitives.asymmetric import rsa
  from cryptography.hazmat.backends import default_backend
  from cryptography.hazmat.primitives import serialization
  from fastapi import HTTPException
  from fastapi.security import HTTPAuthorizationCredentials
  from app.utils.auth import get_current_user_id

  def _make_pair():
      pk = rsa.generate_private_key(65537, 2048, default_backend())
      pub = pk.public_key().public_bytes(
          serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
      ).decode()
      return pk, pub

  @pytest.mark.asyncio
  async def test_유효한_토큰():
      pk, pub = _make_pair()
      token = jwt.encode({"sub": "42"}, pk, algorithm="RS256")
      creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
      with patch("app.utils.auth._get_public_key", return_value=pub):
          assert await get_current_user_id(creds) == 42

  @pytest.mark.asyncio
  async def test_잘못된_토큰_401():
      creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="bad.tok")
      with patch("app.utils.auth._get_public_key", return_value="invalid"):
          with pytest.raises(HTTPException) as exc:
              await get_current_user_id(creds)
      assert exc.value.status_code == 401
  ```

- [ ] **Step 3: 테스트 실행 — 실패 확인**

  ```bash
  pytest tests/test_auth.py -v
  ```

- [ ] **Step 4: auth.py 구현**

  ```python
  # app/utils/auth.py
  """map-service-user RS256 JWT 검증 FastAPI Depends."""
  from __future__ import annotations
  import jwt
  from fastapi import HTTPException, Security
  from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
  from app.config import settings

  _bearer = HTTPBearer()
  _public_key: str | None = None


  def _get_public_key() -> str:
      global _public_key
      if _public_key is None:
          _public_key = settings.HUB_JWT_PUBLIC_KEY.replace("\\n", "\n")
      return _public_key


  async def get_current_user_id(
      creds: HTTPAuthorizationCredentials = Security(_bearer),
  ) -> int:
      try:
          payload = jwt.decode(creds.credentials, _get_public_key(), algorithms=["RS256"])
          return int(payload["sub"])
      except (jwt.PyJWTError, KeyError, ValueError) as e:
          raise HTTPException(status_code=401, detail="Invalid or expired token") from e
  ```

- [ ] **Step 5: config.py에 추가**

  ```python
  HUB_JWT_PUBLIC_KEY: str = ""
  ```

- [ ] **Step 6: 테스트 통과 + Commit**

  ```bash
  pytest tests/test_auth.py -v
  git add app/utils/auth.py app/config.py requirements.txt tests/test_auth.py
  git commit -m "feat(ar): RS256 JWT 검증 FastAPI 의존성"
  ```

---

### Task 6: Hub — ar_routers.py

**Files:**
- Create: `app/routers/ar_routers.py`
- Modify: `app/main.py`

**Endpoints (7개):**
- `GET  /v1/ar/coordinate-systems?lat=&lng=&radius=500` → 인증 불필요
- `POST /v1/ar/coordinate-systems` → 인증 필요
- `GET  /v1/ar/coordinate-systems/{cs_id}` → 인증 불필요
- `GET  /v1/ar/coordinate-systems/{cs_id}/map-download-url` → 인증 필요
- `POST /v1/ar/coordinate-systems/{cs_id}/anchors` → 인증 필요
- `GET  /v1/ar/coordinate-systems/{cs_id}/anchors` → 인증 필요
- `DELETE /v1/ar/coordinate-systems/{cs_id}/anchors/{anchor_id}` → 인증 필요 + 본인만

- [ ] **Step 1: 라우터 테스트 작성**

  `tests/test_ar_routers.py`:
  ```python
  import pytest
  from httpx import AsyncClient, ASGITransport
  from unittest.mock import AsyncMock, patch
  from app.main import app

  @pytest.mark.asyncio
  async def test_목록_인증_불필요():
      with patch("app.routers.ar_routers.find_coordinate_systems_nearby",
                 new_callable=AsyncMock, return_value=[]):
          async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
              resp = await c.get("/v1/ar/coordinate-systems?lat=37.5&lng=127.0")
      assert resp.status_code == 200

  @pytest.mark.asyncio
  async def test_앵커_생성_토큰_없으면_403():
      async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
          resp = await c.post(
              "/v1/ar/coordinate-systems/1/anchors",
              json={"content": "테스트", "pos_x": 0, "pos_y": 1, "pos_z": 0},
          )
      assert resp.status_code == 403

  @pytest.mark.asyncio
  async def test_앵커_삭제_타인_403():
      with patch("app.utils.auth.get_current_user_id", return_value=99):
          with patch("app.routers.ar_routers.delete_anchor",
                     new_callable=AsyncMock, return_value=False):
              async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
                  resp = await c.delete(
                      "/v1/ar/coordinate-systems/1/anchors/1",
                      headers={"Authorization": "Bearer fake"},
                  )
      assert resp.status_code == 403
  ```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

  ```bash
  pytest tests/test_ar_routers.py -v
  ```

- [ ] **Step 3: ar_routers.py 구현**

  ```python
  # app/routers/ar_routers.py
  from __future__ import annotations
  from fastapi import APIRouter, Depends, HTTPException, Response
  from app.clients.immersal_client import get_map_download_url
  from app.db.ar_repo import (
      create_anchor, create_coordinate_system, delete_anchor,
      find_coordinate_systems_nearby, get_coordinate_system, list_anchors,
  )
  from app.schemas.ar_schemas import (
      AnchorCreate, AnchorResponse, CoordinateSystemCreate,
      CoordinateSystemDetail, CoordinateSystemSummary, MapDownloadUrlResponse,
  )
  from app.utils.auth import get_current_user_id

  router = APIRouter(prefix="/v1/ar")


  @router.get("/coordinate-systems", response_model=list[CoordinateSystemSummary])
  async def nearby_coordinate_systems(lat: float, lng: float, radius: float = 500.0):
      return await find_coordinate_systems_nearby(lat, lng, radius)


  @router.post("/coordinate-systems", response_model=CoordinateSystemDetail, status_code=201)
  async def create_cs(body: CoordinateSystemCreate,
                      user_id: int = Depends(get_current_user_id)):
      return await create_coordinate_system(body, user_id)


  @router.get("/coordinate-systems/{cs_id}", response_model=CoordinateSystemDetail)
  async def get_cs(cs_id: int):
      cs = await get_coordinate_system(cs_id)
      if cs is None:
          raise HTTPException(404, "coordinate system not found")
      return cs


  @router.get("/coordinate-systems/{cs_id}/map-download-url",
              response_model=MapDownloadUrlResponse)
  async def map_download_url(cs_id: int, user_id: int = Depends(get_current_user_id)):
      cs = await get_coordinate_system(cs_id)
      if cs is None:
          raise HTTPException(404, "coordinate system not found")
      return {"url": await get_map_download_url(cs["immersal_map_id"])}


  @router.post("/coordinate-systems/{cs_id}/anchors",
               response_model=AnchorResponse, status_code=201)
  async def add_anchor(cs_id: int, body: AnchorCreate,
                       user_id: int = Depends(get_current_user_id)):
      if await get_coordinate_system(cs_id) is None:
          raise HTTPException(404, "coordinate system not found")
      return await create_anchor(cs_id, body, user_id)


  @router.get("/coordinate-systems/{cs_id}/anchors",
              response_model=list[AnchorResponse])
  async def get_anchors(cs_id: int, user_id: int = Depends(get_current_user_id)):
      if await get_coordinate_system(cs_id) is None:
          raise HTTPException(404, "coordinate system not found")
      return await list_anchors(cs_id)


  @router.delete("/coordinate-systems/{cs_id}/anchors/{anchor_id}", status_code=204)
  async def remove_anchor(cs_id: int, anchor_id: int,
                          user_id: int = Depends(get_current_user_id)):
      if not await delete_anchor(anchor_id, user_id):
          raise HTTPException(403, "not your anchor or not found")
      return Response(status_code=204)
  ```

- [ ] **Step 4: main.py에 router 등록**

  ```python
  from app.routers.ar_routers import router as ar_router
  app.include_router(ar_router)
  ```

- [ ] **Step 5: 테스트 통과 + Commit**

  ```bash
  pytest tests/test_ar_routers.py -v
  git add app/routers/ar_routers.py app/main.py tests/test_ar_routers.py
  git commit -m "feat(ar): AR FastAPI 라우터 (좌표계·앵커 7개 엔드포인트)"
  ```

---

### Task 7: Flutter — pubspec 패키지 추가

**Files:**
- Modify: `pubspec.yaml`, `ios/Podfile`, `ios/Runner/Info.plist`, `android/app/src/main/AndroidManifest.xml`

- [ ] **Step 1: pubspec.yaml에 추가**

  ```yaml
  ar_flutter_plugin: ^0.7.3
  google_mlkit_hand_landmark_detection: ^0.1.0
  ```

- [ ] **Step 2: iOS 최소 버전**

  `ios/Podfile`: `platform :ios, '12.0'` → `'14.0'`

- [ ] **Step 3: 카메라 권한**

  `ios/Runner/Info.plist`:
  ```xml
  <key>NSCameraUsageDescription</key>
  <string>AR 기능과 손 추적을 위해 카메라를 사용합니다</string>
  ```
  `android/app/src/main/AndroidManifest.xml`:
  ```xml
  <uses-permission android:name="android.permission.CAMERA" />
  <uses-feature android:name="android.hardware.camera.ar" android:required="true" />
  ```

- [ ] **Step 4: 빌드 오류 없음 확인**

  ```bash
  flutter pub get
  flutter build ios --no-codesign 2>&1 | grep -iE "^.*error" | head -10
  ```
  Expected: 오류 없음

- [ ] **Step 5: Commit**

  ```bash
  git add pubspec.yaml pubspec.lock ios/ android/
  git commit -m "feat(ar): AR·손추적 Flutter 패키지 추가"
  ```

---

### Task 8: Flutter — ar_model.dart

**Files:**
- Create: `lib/data/models/ar_model.dart`

- [ ] **Step 1: 테스트 먼저 작성**

  `test/data/models/ar_model_test.dart`:
  ```dart
  import 'package:flutter_test/flutter_test.dart';
  import 'package:map_service_client/data/models/ar_model.dart';

  void main() {
    final anchorJson = {
      'id': 1,
      'coordinate_system_id': 1,
      'stroke_data': {
        'ref': {'pos': [1.0, 0.5, -2.0], 'rot': [0.0, 0.0, 0.0, 1.0]},
        'rel': {'pos': [0.0, 0.0, 0.05], 'rot': [0.0, 0.0, 0.0, 1.0]},
        'strokes': [[[0.0, 0.0], [0.1, 0.1], [0.2, 0.0]]],
        'stroke_width': 0.003,
      },
      'created_by': 42,
      'created_at': '2026-06-26T12:00:00Z',
    };

    test('CoordinateSystem.fromJson', () {
      final cs = CoordinateSystem.fromJson(
          {'id': 1, 'name': '덕수궁', 'latitude': 37.5, 'longitude': 126.9});
      expect(cs.name, '덕수궁');
      expect(cs.latitude, closeTo(37.5, 0.001));
    });

    test('Anchor.fromJson - ref.pos 파싱', () {
      final a = Anchor.fromJson(anchorJson);
      expect(a.strokeData.ref.pos, [1.0, 0.5, -2.0]);
      expect(a.strokeData.rel.rot, [0.0, 0.0, 0.0, 1.0]);
      expect(a.strokeData.strokes.first.length, 3);
    });

    test('toCreateJson에 id 미포함', () {
      expect(Anchor.fromJson(anchorJson).toCreateJson().containsKey('id'), isFalse);
    });
  }
  ```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

  ```bash
  flutter test test/data/models/ar_model_test.dart
  ```

- [ ] **Step 3: ar_model.dart 구현**

  ```dart
  // lib/data/models/ar_model.dart
  class CoordinateSystem {
    final int id;
    final String? immersalMapId;
    final String name;
    final String? description;
    final double latitude;
    final double longitude;
    final String? thumbnailUrl;

    const CoordinateSystem({
      required this.id, this.immersalMapId, required this.name,
      this.description, required this.latitude, required this.longitude,
      this.thumbnailUrl,
    });

    factory CoordinateSystem.fromJson(Map<String, dynamic> json) => CoordinateSystem(
          id: json['id'] as int,
          immersalMapId: json['immersal_map_id'] as String?,
          name: json['name'] as String,
          description: json['description'] as String?,
          latitude: (json['latitude'] as num).toDouble(),
          longitude: (json['longitude'] as num).toDouble(),
          thumbnailUrl: json['thumbnail_url'] as String?,
        );
  }

  // 위치 [x,y,z] + 방향 [qx,qy,qz,qw]
  class ObjectPose {
    final List<double> pos;
    final List<double> rot;
    const ObjectPose({required this.pos, required this.rot});

    factory ObjectPose.fromJson(Map<String, dynamic> json) => ObjectPose(
          pos: List<double>.from((json['pos'] as List).map((e) => (e as num).toDouble())),
          rot: List<double>.from((json['rot'] as List).map((e) => (e as num).toDouble())),
        );

    Map<String, dynamic> toJson() => {'pos': pos, 'rot': rot};
  }

  class StrokeData {
    /// ref: 탐지된 인접 객체의 Immersal 공간 포즈.
    ///   렌더링 시 이 포즈 근처에서 동일 객체를 재탐지하는 기준점.
    final ObjectPose ref;

    /// rel: 앵커의 ref 객체 로컬 프레임 기준 상대 포즈.
    ///   객체 재탐지 후 이 트랜스폼을 합성해 앵커 월드 포즈 결정.
    final ObjectPose rel;

    final List<List<List<double>>> strokes; // 획 → 점 → [u, v] (미터)
    final double strokeWidth;

    const StrokeData({
      required this.ref, required this.rel,
      required this.strokes, this.strokeWidth = 0.003,
    });

    factory StrokeData.fromJson(Map<String, dynamic> json) => StrokeData(
          ref: ObjectPose.fromJson(json['ref'] as Map<String, dynamic>),
          rel: ObjectPose.fromJson(json['rel'] as Map<String, dynamic>),
          strokes: (json['strokes'] as List)
              .map((s) => (s as List)
                  .map((p) => (p as List).map((v) => (v as num).toDouble()).toList())
                  .toList())
              .toList(),
          strokeWidth: (json['stroke_width'] as num? ?? 0.003).toDouble(),
        );

    Map<String, dynamic> toJson() => {
          'ref': ref.toJson(),
          'rel': rel.toJson(),
          'strokes': strokes,
          'stroke_width': strokeWidth,
        };
  }

  class Anchor {
    final int id;
    final int coordinateSystemId;
    final StrokeData strokeData;
    final int createdBy;
    final DateTime createdAt;

    const Anchor({
      required this.id, required this.coordinateSystemId,
      required this.strokeData, required this.createdBy, required this.createdAt,
    });

    factory Anchor.fromJson(Map<String, dynamic> json) => Anchor(
          id: json['id'] as int,
          coordinateSystemId: json['coordinate_system_id'] as int,
          strokeData: StrokeData.fromJson(json['stroke_data'] as Map<String, dynamic>),
          createdBy: json['created_by'] as int,
          createdAt: DateTime.parse(json['created_at'] as String),
        );

    Map<String, dynamic> toCreateJson() => strokeData.toJson();
  }
  ```

- [ ] **Step 4: 테스트 통과 + Commit**

  ```bash
  flutter test test/data/models/ar_model_test.dart
  git add lib/data/models/ar_model.dart test/data/models/
  git commit -m "feat(ar): AR 데이터 모델 (CoordinateSystem, Anchor)"
  ```

---

### Task 9: Flutter — ar_repository.dart

**Files:**
- Create: `lib/data/repositories/ar_repository.dart`

> **착수 전:** `lib/core/api/` 기존 HTTP 클라이언트 패턴 확인 필수. 기존 방식과 통일.

- [ ] **Step 1: lib/core/api/ 기존 패턴 확인**

  ```bash
  ls lib/core/api/
  cat lib/core/api/*.dart
  ```

- [ ] **Step 2: 테스트 작성**

  `test/data/repositories/ar_repository_test.dart`:
  ```dart
  import 'dart:convert';
  import 'package:flutter_test/flutter_test.dart';
  import 'package:http/http.dart' as http;
  import 'package:http/testing.dart';
  import 'package:map_service_client/data/models/ar_model.dart';
  import 'package:map_service_client/data/repositories/ar_repository.dart';

  final _aJson = {
    'id': 1,
    'coordinate_system_id': 1,
    'stroke_data': {
      'ref': {'pos': [1.0, 0.0, -2.0], 'rot': [0.0, 0.0, 0.0, 1.0]},
      'rel': {'pos': [0.0, 0.0, 0.05], 'rot': [0.0, 0.0, 0.0, 1.0]},
      'strokes': [[[0.0, 0.0], [0.05, 0.05]]],
      'stroke_width': 0.003,
    },
    'created_by': 1,
    'created_at': '2026-06-26T00:00:00Z',
  };

  ArRepository _repo(MockClient m) => ArRepository(
        baseUrl: 'http://test', getToken: () => 'tok', client: m);

  void main() {
    test('fetchNearby 파싱', () async {
      final m = MockClient((_) async => http.Response(
            jsonEncode([{'id': 1, 'name': '덕수궁', 'latitude': 37.5, 'longitude': 126.9}]), 200));
      expect((await _repo(m).fetchNearbyCoordinateSystems(37.5, 126.9)).first.name, '덕수궁');
    });

    test('createAnchor 201', () async {
      final m = MockClient((_) async => http.Response(jsonEncode(_aJson), 201));
      expect((await _repo(m).createAnchor(1, Anchor.fromJson(_aJson))).id, 1);
    });

    test('deleteAnchor 403 예외', () async {
      final m = MockClient((_) async => http.Response('', 403));
      expect(() => _repo(m).deleteAnchor(1, 1), throwsException);
    });
  }
  ```

- [ ] **Step 3: 테스트 실행 — 실패 확인**

  ```bash
  flutter test test/data/repositories/ar_repository_test.dart
  ```

- [ ] **Step 4: ar_repository.dart 구현**

  ```dart
  // lib/data/repositories/ar_repository.dart
  import 'dart:convert';
  import 'package:http/http.dart' as http;
  import 'package:map_service_client/data/models/ar_model.dart';

  class ArRepository {
    final String _baseUrl;
    final String Function() _getToken;
    final http.Client _client;

    ArRepository({
      required String baseUrl,
      required String Function() getToken,
      http.Client? client,
    })  : _baseUrl = baseUrl,
          _getToken = getToken,
          _client = client ?? http.Client();

    Map<String, String> get _auth => {
          'Authorization': 'Bearer ${_getToken()}',
          'Content-Type': 'application/json',
        };

    Future<List<CoordinateSystem>> fetchNearbyCoordinateSystems(
        double lat, double lng, {double radius = 500}) async {
      final resp = await _client.get(
          Uri.parse('$_baseUrl/v1/ar/coordinate-systems?lat=$lat&lng=$lng&radius=$radius'));
      if (resp.statusCode != 200) throw Exception('fetchNearby ${resp.statusCode}');
      return (jsonDecode(resp.body) as List)
          .map((e) => CoordinateSystem.fromJson(e as Map<String, dynamic>))
          .toList();
    }

    Future<CoordinateSystem> fetchCoordinateSystem(int id) async {
      final resp = await _client.get(
          Uri.parse('$_baseUrl/v1/ar/coordinate-systems/$id'));
      if (resp.statusCode == 404) throw Exception('not found');
      if (resp.statusCode != 200) throw Exception('fetchCS ${resp.statusCode}');
      return CoordinateSystem.fromJson(jsonDecode(resp.body) as Map<String, dynamic>);
    }

    Future<String> fetchMapDownloadUrl(int csId) async {
      final resp = await _client.get(
          Uri.parse('$_baseUrl/v1/ar/coordinate-systems/$csId/map-download-url'),
          headers: _auth);
      if (resp.statusCode != 200) throw Exception('fetchUrl ${resp.statusCode}');
      return (jsonDecode(resp.body) as Map<String, dynamic>)['url'] as String;
    }

    Future<CoordinateSystem> createCoordinateSystem({
      required String immersalMapId, required String name,
      String? description, required double latitude, required double longitude,
      String? thumbnailUrl,
    }) async {
      final resp = await _client.post(
        Uri.parse('$_baseUrl/v1/ar/coordinate-systems'),
        headers: _auth,
        body: jsonEncode({
          'immersal_map_id': immersalMapId, 'name': name,
          if (description != null) 'description': description,
          'latitude': latitude, 'longitude': longitude,
          if (thumbnailUrl != null) 'thumbnail_url': thumbnailUrl,
        }),
      );
      if (resp.statusCode != 201) throw Exception('createCS ${resp.statusCode}');
      return CoordinateSystem.fromJson(jsonDecode(resp.body) as Map<String, dynamic>);
    }

    Future<List<Anchor>> fetchAnchors(int csId) async {
      final resp = await _client.get(
          Uri.parse('$_baseUrl/v1/ar/coordinate-systems/$csId/anchors'),
          headers: _auth);
      if (resp.statusCode != 200) throw Exception('fetchAnchors ${resp.statusCode}');
      return (jsonDecode(resp.body) as List)
          .map((e) => Anchor.fromJson(e as Map<String, dynamic>))
          .toList();
    }

    Future<Anchor> createAnchor(int csId, Anchor anchor) async {
      final resp = await _client.post(
        Uri.parse('$_baseUrl/v1/ar/coordinate-systems/$csId/anchors'),
        headers: _auth, body: jsonEncode(anchor.toCreateJson()),
      );
      if (resp.statusCode != 201) throw Exception('createAnchor ${resp.statusCode}');
      return Anchor.fromJson(jsonDecode(resp.body) as Map<String, dynamic>);
    }

    Future<void> deleteAnchor(int csId, int anchorId) async {
      final resp = await _client.delete(
          Uri.parse('$_baseUrl/v1/ar/coordinate-systems/$csId/anchors/$anchorId'),
          headers: _auth);
      if (resp.statusCode == 403) throw Exception('not authorized');
      if (resp.statusCode != 204) throw Exception('deleteAnchor ${resp.statusCode}');
    }
  }
  ```

- [ ] **Step 5: 테스트 통과 + Commit**

  ```bash
  flutter test test/data/repositories/ar_repository_test.dart
  git add lib/data/repositories/ar_repository.dart test/data/repositories/
  git commit -m "feat(ar): AR HTTP 레포지토리"
  ```

---

### Task 10: Flutter — ArMapScreen (좌표계 선택 화면)

**Files:**
- Create: `lib/features/ar/screens/ar_map_screen.dart`
- Create: `lib/features/ar/widgets/coordinate_system_card.dart`
- Modify: `lib/core/router/` — `/ar` 라우트 등록

- [ ] **Step 1: 위젯 테스트 작성**

  `test/features/ar/widgets/coordinate_system_card_test.dart`:
  ```dart
  import 'package:flutter/material.dart';
  import 'package:flutter_test/flutter_test.dart';
  import 'package:map_service_client/data/models/ar_model.dart';
  import 'package:map_service_client/features/ar/widgets/coordinate_system_card.dart';

  void main() {
    testWidgets('카드에 이름 표시', (tester) async {
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: CoordinateSystemCard(
            cs: CoordinateSystem(id: 1, name: '덕수궁', latitude: 37.5, longitude: 126.9),
            onTap: () {},
          ),
        ),
      ));
      expect(find.text('덕수궁'), findsOneWidget);
    });
  }
  ```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

  ```bash
  flutter test test/features/ar/widgets/
  ```

- [ ] **Step 3: coordinate_system_card.dart 구현**

  ```dart
  // lib/features/ar/widgets/coordinate_system_card.dart
  import 'package:flutter/material.dart';
  import 'package:map_service_client/data/models/ar_model.dart';

  class CoordinateSystemCard extends StatelessWidget {
    final CoordinateSystem cs;
    final VoidCallback onTap;
    const CoordinateSystemCard({super.key, required this.cs, required this.onTap});

    @override
    Widget build(BuildContext context) => ListTile(
          leading: cs.thumbnailUrl != null
              ? Image.network(cs.thumbnailUrl!, width: 48, height: 48, fit: BoxFit.cover)
              : const Icon(Icons.place),
          title: Text(cs.name, style: const TextStyle(fontWeight: FontWeight.w600)),
          subtitle: cs.description != null ? Text(cs.description!) : null,
          onTap: onTap,
        );
  }
  ```

- [ ] **Step 4: ar_map_screen.dart 구현**

  ```dart
  // lib/features/ar/screens/ar_map_screen.dart
  import 'package:flutter/material.dart';
  import 'package:flutter_naver_map/flutter_naver_map.dart';
  import 'package:geolocator/geolocator.dart';
  import 'package:go_router/go_router.dart';
  import 'package:map_service_client/data/models/ar_model.dart';
  import 'package:map_service_client/data/repositories/ar_repository.dart';
  import 'package:map_service_client/features/ar/widgets/coordinate_system_card.dart';

  class ArMapScreen extends StatefulWidget {
    final ArRepository repository;
    const ArMapScreen({super.key, required this.repository});
    @override State<ArMapScreen> createState() => _State();
  }

  class _State extends State<ArMapScreen> {
    List<CoordinateSystem> _systems = [];
    bool _loading = true;
    String? _error;
    Position? _pos;

    @override void initState() { super.initState(); _load(); }

    Future<void> _load() async {
      setState(() { _loading = true; _error = null; });
      try {
        final pos = await Geolocator.getCurrentPosition(
            locationSettings: const LocationSettings(accuracy: LocationAccuracy.high));
        final sys = await widget.repository
            .fetchNearbyCoordinateSystems(pos.latitude, pos.longitude);
        if (mounted) setState(() { _pos = pos; _systems = sys; _loading = false; });
      } catch (e) {
        if (mounted) setState(() { _error = e.toString(); _loading = false; });
      }
    }

    @override
    Widget build(BuildContext context) => Scaffold(
          appBar: AppBar(title: const Text('AR 장소 선택')),
          body: _loading
              ? const Center(child: CircularProgressIndicator())
              : _error != null
                  ? Center(child: Text(_error!))
                  : Stack(children: [
                      if (_pos != null)
                        NaverMap(
                          options: NaverMapViewOptions(
                            initialCameraPosition: NCameraPosition(
                              target: NLatLng(_pos!.latitude, _pos!.longitude),
                              zoom: 15,
                            ),
                          ),
                          onMapReady: (ctrl) {
                            for (final cs in _systems) {
                              ctrl.addOverlay(NMarker(
                                  id: 'cs_${cs.id}',
                                  position: NLatLng(cs.latitude, cs.longitude)));
                            }
                          },
                        ),
                      DraggableScrollableSheet(
                        initialChildSize: 0.3,
                        minChildSize: 0.15,
                        maxChildSize: 0.6,
                        builder: (_, sc) => Container(
                          decoration: BoxDecoration(
                            color: Theme.of(context).scaffoldBackgroundColor,
                            borderRadius:
                                const BorderRadius.vertical(top: Radius.circular(16)),
                          ),
                          child: _systems.isEmpty
                              ? const Center(child: Text('주변에 AR 장소가 없습니다'))
                              : ListView.builder(
                                  controller: sc,
                                  itemCount: _systems.length,
                                  itemBuilder: (_, i) => CoordinateSystemCard(
                                    cs: _systems[i],
                                    onTap: () => context.push('/ar/scan/${_systems[i].id}'),
                                  ),
                                ),
                        ),
                      ),
                    ]),
          floatingActionButton: FloatingActionButton.extended(
            onPressed: _load,
            icon: const Icon(Icons.refresh),
            label: const Text('새로고침'),
          ),
        );
  }
  ```

- [ ] **Step 5: go_router `/ar` 라우트 등록**

  `lib/core/router/` 기존 라우터에:
  ```dart
  GoRoute(
    path: '/ar',
    builder: (context, state) => ArMapScreen(
      repository: ArRepository(
        baseUrl: dotenv.env['API_BASE_URL']!,
        getToken: () => /* lib/core/state/ JWT 상태 접근 방식 확인 후 교체 */ '',
      ),
    ),
  ),
  ```

- [ ] **Step 6: 테스트 통과 + Commit**

  ```bash
  flutter test test/features/ar/
  git add lib/features/ar/ lib/core/router/ test/features/ar/
  git commit -m "feat(ar): ArMapScreen (네이버맵 + 좌표계 바텀시트)"
  ```

---

## 스펙 커버리지 (Plan A)

| 스펙 항목 | Plan A | 다음 |
|----------|--------|------|
| 좌표계 목록 (지도 점 표시) | ✅ | — |
| 맵 파일 다운로드 URL | ✅ | Plan B에서 실제 다운로드 |
| 좌표계 생성 (신규 장소) | ✅ | — |
| 앵커 저장 (3D 좌표) | ✅ | — |
| 스캔 업로드 인터페이스 | ✅ | Plan B에서 호출 플로우 완성 |
| 부분 스캔 → 로컬라이제이션 | ❌ | Plan B |
| 손가락 3D 글씨 | ❌ | Plan C |
| 앵커 렌더링 | ❌ | Plan D |
| 미니맵 UI (2D) | ❌ | Plan D |

---

## 환경변수 신규

| 서비스 | 변수명 | 내용 |
|--------|--------|------|
| `map-service-hub` | `IMMERSAL_TOKEN` | Immersal 계정 Bearer token |
| `map-service-hub` | `IMMERSAL_API_URL` | `https://api.immersal.com` (기본값) |
| `map-service-hub` | `HUB_JWT_PUBLIC_KEY` | map-service-user RS256 공개키 (PEM, `\n` 이스케이프) |
| `map-service-client` | `.env` `API_BASE_URL` | hub 백엔드 URL |
