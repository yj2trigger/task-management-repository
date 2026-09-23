# LeRobot SO-101 환경 구축

> 대상: SO-101 듀얼암 로봇(리더/팔로워) 조작 실습용 LeRobot 환경
> 기준 시각: 2026-09-19 ~ 2026-09-22 (클로드 세션 `84142651-...` 기준 재구성)
> 코드 레포 없음. 로컬 환경 설정 작업이라 이 문서가 유일한 기록.

---

## 1. 배경 · 결정

- 실습 자료(PDF 9장, 1~9장: 환경세팅 → 가상환경 → LeRobot 구조 → 로봇 설치 → 캘리브레이션 → 텔레오퍼레이션 → HF/WandB 가입 → 데이터 수집 → Colab 학습)를 9장부터 역순으로 읽고 필요한 설치만 추림.
- 실습 자료는 **Ubuntu 기준**(conda, apt, `/dev/ttyACM`)인데 이 PC는 Windows.
- **C드라이브가 227MB만 남은 상태**라 전부 D드라이브(SSD)에서 돌아가야 함.

**결정: WSL Ubuntu를 D드라이브에 직접 생성**
- `wsl --install`(스토어 설치)은 vhdx가 C에 생겨서 배제.
- 대신 Ubuntu 24.04 rootfs tar를 받아 `wsl --import Ubuntu-LeRobot D:\WSL\Ubuntu-LeRobot <rootfs.tar.gz> --version 2`로 D에 바로 생성.
- 배포판 자체가 D의 vhdx이므로 그 안 작업물(conda, pip 캐시, LeRobot 소스, 모델 가중치)은 전부 자동으로 D에 저장됨 — 별도 경로 지정 불필요.

**하지 않기로 한 것**
- Colab 학습(9장): 클라우드라 로컬 설치 불필요.
- 실습(캘리브레이션·텔레오퍼레이션·데이터수집, 5·6·8장): 로봇 실물 연결 후 진행. 지금은 명령어 실행 환경만 구축.

---

## 2. 구축 절차 (재현용)

```bash
# 1. D에 폴더 준비, rootfs 다운로드 후 import
mkdir -p /d/WSL/Ubuntu-LeRobot /d/WSL/_downloads
curl -L -o ubuntu-24.04-wsl.rootfs.tar.gz "<Ubuntu 24.04 base rootfs URL>"
wsl --import Ubuntu-LeRobot D:\WSL\Ubuntu-LeRobot D:\WSL\_downloads\ubuntu-24.04-wsl.rootfs.tar.gz --version 2

# 2. rootfs는 root 계정뿐 — 일반 사용자 생성 + 기본 사용자 지정 (wsl.conf), apt update
wsl -d Ubuntu-LeRobot -u root -- bash -c "useradd -m -s /bin/bash -G sudo rexro; ..."
wsl --terminate Ubuntu-LeRobot   # 기본 사용자 적용 위해 재시작

# 3. Miniconda 설치 (WSL 안에서, curl -O는 반드시 $HOME 등 저장소 밖에서 실행할 것 — §4.2 참고)
# 4. conda env 생성 + LeRobot 설치
conda create -n lerobot python=3.12
cd $HOME/workspace && git clone --branch v0.6.0 <lerobot repo>
conda activate lerobot
pip install -e ".[feetech,viz,dataset,training]"   # torch 포함, 수 GB, 오래 걸림 → 백그라운드 권장
```

**함정 (실제로 겪음)**
- `.bashrc`가 비대화형 쉘에서 앞부분 `return`으로 끊겨서 `conda activate`가 안 먹음
  → `source $HOME/miniconda3/etc/profile.d/conda.sh`를 직접 source
- 첫 `pip install`이 중간에 끊김(exit 127) → conda.sh 직접 source 후 재시도하면 캐시된 wheel로 빠르게 성공

**USB 패스스루 (Windows → WSL)**
```powershell
winget install --id dorssel.usbipd-win -e   # Windows 쪽
```
```bash
# WSL 쪽 usbip 클라이언트 (git-bash 거치면 경로 자동변환 문제 있음 → MSYS_NO_PATHCONV=1 로 우회)
MSYS_NO_PATHCONV=1 wsl -d Ubuntu-LeRobot -- sudo update-alternatives --install ...
```
```powershell
# 관리자 권한 PowerShell에서 (bind는 최초 1회, attach는 연결마다)
usbipd bind --busid <busid>
usbipd attach --wsl --busid <busid>
```
- `attach`는 대상 WSL distro가 **실행 중**이어야 함 (`wsl -d Ubuntu-LeRobot -- sleep 600` 등으로 켜둘 것).

---

## 3. 검증됨

- `lerobot` conda env에서 CLI 6종 확인됨: `lerobot-teleoperate`, `lerobot-record`, `lerobot-calibrate`, `lerobot-find-port`, `lerobot-find-cameras`, `lerobot-train`
- `usbipd list`로 로봇 관련 장치 인식: `CH343 USB-Enhanced-SERIAL(COM9)` — 서보 시리얼 어댑터 1개, `720p HD Camera` — cam_wrist 추정

## 4. 미해결 · 다음 단계

- **로봇 팔 USB가 1개만 잡힘.** 4장 기준 리더+팔로워 각각 별도 USB(2개) 필요. 다른 팔 케이블 확인 필요.
- `usbipd attach` 실제 성공 여부 미확인 (관리자 권한 필요해서 사용자가 직접 실행해야 함, 이 세션에서 끝까지 못 봄).
- HuggingFace(`hf auth login`), WandB(`wandb login`) 로그인 — 가입은 브라우저에서 직접, CLI 로그인은 안 함.
- 5·6·8장(캘리브레이션·텔레오퍼레이션·데이터수집)은 로봇 USB 연결 확정 후 진행.

## 5. 참고: 무관한 별도 환경과 혼동 주의

- 이 프로젝트와 별개로 **다른 수업용 Ubuntu**(C드라이브, LeRobot 아님)가 나중에 따로 설치됨. `Ubuntu-LeRobot`은 로봇용 conda 환경 포함 16.7GB짜리 D드라이브 배포판이고, SSD가 없으면 실행 안 됨. VS Code로 WSL 연결 시 기본 배포판이 `docker-desktop`이므로 반드시 "Connect to WSL using Distro..."로 대상을 명시해서 골라야 함.
