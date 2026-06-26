# Claude Code 플러그인/스킬 (user scope)

> 작성일: 2026-06-08 00:00
> 목적: `~/.claude`에 user-scope로 설치한 플러그인/스킬 SSOT. 모든 프로젝트 세션에서 공통 로드됨 — 프로젝트별 docs에 중복 기록하지 않음.
> 설치 확인: `claude plugin list`

## 설치 목록

| 스킬 | 마켓플레이스 | 플러그인 ID | 용도 |
|---|---|---|---|
| Karpathy Guidelines | `forrestchang/andrej-karpathy-skills` | `andrej-karpathy-skills@karpathy-skills` | LLM 코딩 실수(과설계, 비외과적 수정 등) 줄이는 행동 가이드라인 |
| claude-video | `bradautomates/claude-video` | `watch@claude-video` | 영상 다운로드·프레임 추출·전사 후 질의응답 |
| Superpowers | (공식 `claude-plugins-official`) | `superpowers@claude-plugins-official` | TDD/디버깅/협업 패턴 스킬 모음 |
| Understand-Anything | `Lum1104/Understand-Anything` | `understand-anything@understand-anything` | 코드베이스 분석·지식그래프·온보딩 가이드 |
| agentmemory | (npm, MCP 서버) | user-scope MCP `agentmemory` (`npx -y @agentmemory/agentmemory`) | AI 에이전트용 영구 메모리 |

## 사용법

### Karpathy Guidelines
명령어 없음 — `karpathy-guidelines` 스킬이 코드 작성/리뷰/리팩터링 요청 시 자동 발동. 4원칙: 가정 명시, 단순함 우선, surgical 수정, 검증가능 목표.

### claude-video
```
/watch <영상URL 또는 로컬경로> [질문]
```
`<>` `[]`는 표기 규칙(필수/선택)이며 입력하지 않음. 예: `/watch https://youtube.com/watch?v=abc123 이 영상 뭐 설명함?`
사전 요구: yt-dlp, ffmpeg (없으면 preflight 단계서 안내).

### Superpowers
명령어 암기 불필요 — `using-superpowers` 스킬이 세션 시작 시 자동 로드되어 상황에 맞는 스킬을 알아서 호출.
주요 스킬: `test-driven-development`, `systematic-debugging`, `brainstorming`, `writing-plans`, `executing-plans`, `requesting-code-review`/`receiving-code-review`, `using-git-worktrees`, `dispatching-parallel-agents`, `subagent-driven-development`, `finishing-a-development-branch`, `verification-before-completion`, `writing-skills`.

### Understand-Anything
| 명령어 | 용도 |
|---|---|
| `/understand` | 코드베이스 분석 → 지식그래프 생성 |
| `/understand-explain` | 특정 파일/함수/모듈 딥다이브 설명 |
| `/understand-chat` | 지식그래프 기반 코드베이스 Q&A |
| `/understand-dashboard` | 웹 대시보드로 그래프 시각화 |
| `/understand-diff` | git diff/PR 영향범위·리스크 분석 |
| `/understand-domain` | 비즈니스 도메인 지식 추출 + 플로우 그래프 |
| `/understand-onboard` | 신규 팀원용 온보딩 가이드 생성 |
| `/understand-knowledge` | Karpathy식 위키 지식베이스 → 지식그래프 |

### agentmemory
Claude Code 슬래시 명령 아님 — 터미널에서 직접 실행:
```
agentmemory status         # 연결상태·메모리 개수·헬스체크
agentmemory doctor         # 진단+자동수정 ([F]ix/[S]kip/[?]more/[Q]uit)
agentmemory demo           # 샘플 세션 시드 후 recall 시연
agentmemory remove         # 완전 제거 (--keep-data: 데이터 보존)
agentmemory import-jsonl   # ~/.claude/projects 기존 대화기록 가져오기
agentmemory mcp            # standalone MCP 서버 모드
```
REST API: `localhost:3111` (기본), 뷰어(웹 UI로 메모리 직접 조회/관리): `3111+1` 포트.

## 설치 정보 원본 위치
- 마켓플레이스 등록: `~/.claude/plugins/known_marketplaces.json`
- 설치 내역: `~/.claude/plugins/installed_plugins.json`
- agentmemory MCP 등록: `~/.claude.json` (user config, `claude mcp get agentmemory`로 확인)
