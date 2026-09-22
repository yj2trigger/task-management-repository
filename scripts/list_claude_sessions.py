#!/usr/bin/env python3
"""모든 프로젝트의 Claude Code 세션 목록 조회 (읽기 전용).

VSCode 확장의 세션 목록은 현재 연 폴더로 제한되지만,
`claude --resume <session-id>`는 어느 폴더에서 실행하든 동작한다.
이 스크립트는 session-id를 찾는 용도.

사용법:
    python scripts/list_claude_sessions.py [검색어]
    claude --resume <출력된 session-id>
"""
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"


def first_user_text(jsonl_path: Path) -> str:
    try:
        with jsonl_path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "user":
                    continue
                content = entry.get("message", {}).get("content")
                if isinstance(content, str):
                    text = content
                elif isinstance(content, list):
                    text = next(
                        (b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"),
                        "",
                    )
                else:
                    text = ""
                text = text.strip().replace("\n", " ")
                if text and not text.startswith("<"):
                    return text[:70]
    except OSError:
        pass
    return "(제목 없음)"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    query = sys.argv[1].lower() if len(sys.argv) > 1 else None

    rows = []
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        for jsonl_path in project_dir.glob("*.jsonl"):
            mtime = jsonl_path.stat().st_mtime
            title = first_user_text(jsonl_path)
            if query and query not in title.lower() and query not in project_dir.name.lower():
                continue
            rows.append((mtime, project_dir.name, jsonl_path.stem, title))

    rows.sort(reverse=True)

    for mtime, project, session_id, title in rows:
        date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        print(f"{date}  [{project}]")
        print(f"  {session_id}  {title}")


if __name__ == "__main__":
    main()
