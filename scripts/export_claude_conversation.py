#!/usr/bin/env python3
"""프로젝트의 Claude Code 세션(들)을 대화 형태로 추출 (읽기 전용).

사용자+어시스턴트 텍스트는 그대로, 툴 호출은 한 줄 요약("[도구: Bash] git status")만 남긴다.
tool_result, system-reminder, thinking 블록은 노이즈라 제외.

사용법:
    python scripts/export_claude_conversation.py <프로젝트폴더명> [session-id] [-o 출력파일]
    (프로젝트폴더명은 scripts/list_claude_sessions.py 출력의 [대괄호] 안 이름)
"""
import argparse
import json
import re
import sys
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
SYSTEM_REMINDER_RE = re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL)
OTHER_TAG_RE = re.compile(r"</?(ide_selection|pasted_content)[^>]*>", re.DOTALL)


def clean_text(text: str) -> str:
    text = SYSTEM_REMINDER_RE.sub("", text)
    text = OTHER_TAG_RE.sub("", text)
    return text.strip()


def tool_summary(block: dict) -> str:
    name = block.get("name", "?")
    inp = block.get("input", {})
    hint = inp.get("command") or inp.get("file_path") or inp.get("pattern") or inp.get("description") or ""
    hint = str(hint).replace("\n", " ")[:80]
    return f"[도구: {name}] {hint}".rstrip()


def render_entry(entry: dict) -> str:
    role = entry.get("message", {}).get("role")
    content = entry.get("message", {}).get("content")
    if content is None:
        return ""

    parts = []
    if isinstance(content, str):
        t = clean_text(content)
        if t:
            parts.append(t)
    elif isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")
            if btype == "text":
                t = clean_text(block.get("text", ""))
                if t:
                    parts.append(t)
            elif btype == "tool_use":
                parts.append(tool_summary(block))
            elif btype == "image":
                parts.append("[이미지 첨부]")
            # tool_result, thinking 등은 제외

    if not parts:
        return ""

    label = "사용자" if role == "user" else "어시스턴트"
    ts = entry.get("timestamp", "")
    body = "\n".join(parts)
    return f"### [{ts}] {label}\n\n{body}\n"


def export_session(jsonl_path: Path) -> str:
    out = [f"# 세션 {jsonl_path.stem}\n"]
    with jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") not in ("user", "assistant"):
                continue
            rendered = render_entry(entry)
            if rendered:
                out.append(rendered)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", help="프로젝트 폴더명 (list_claude_sessions.py 출력 기준)")
    ap.add_argument("session_id", nargs="?", help="특정 세션만. 없으면 해당 프로젝트 전체")
    ap.add_argument("-o", "--out", help="출력 파일 경로. 없으면 표준출력")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    project_dir = PROJECTS_DIR / args.project
    if not project_dir.is_dir():
        print(f"프로젝트 폴더 없음: {project_dir}", file=sys.stderr)
        sys.exit(1)

    jsonl_files = sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    if args.session_id:
        jsonl_files = [p for p in jsonl_files if p.stem == args.session_id]
        if not jsonl_files:
            print(f"session-id 못 찾음: {args.session_id}", file=sys.stderr)
            sys.exit(1)

    output = "\n\n---\n\n".join(export_session(p) for p in jsonl_files)

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"저장됨: {args.out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
