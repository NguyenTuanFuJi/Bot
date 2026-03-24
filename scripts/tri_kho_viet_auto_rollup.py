#!/usr/bin/env python3
"""
Trí Khố Việt - Auto session rollup
- Periodically scans OpenClaw session jsonl files
- If a session has been idle for N minutes, generate compact bullet summary
- Stores summaries in memory/session_summaries/auto/
- Updates local state to avoid duplicate rollups
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SESSIONS_DIR = Path("/home/tuan/.openclaw/agents/main/sessions")
DEFAULT_OUT_DIR = ROOT / "memory" / "session_summaries" / "auto"
DEFAULT_STATE = ROOT / "memory" / "session_summaries" / ".rollup_state.json"


def extract_text(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    if isinstance(x, (int, float, bool)):
        return str(x)
    if isinstance(x, list):
        return " ".join(t for t in (extract_text(i) for i in x) if t)
    if isinstance(x, dict):
        # common structures
        for key in ("text", "content", "message", "value"):
            if key in x:
                t = extract_text(x[key])
                if t:
                    return t
        # fallback
        return " ".join(t for t in (extract_text(v) for v in x.values()) if t)
    return ""


def load_state(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def summarize_text(text: str, session_id: str) -> str:
    import importlib.util

    mod_path = ROOT / "scripts" / "tri_kho_viet_summarize.py"
    spec = importlib.util.spec_from_file_location("tri_kho_viet_summarize", mod_path)
    if not spec or not spec.loader:
        raise RuntimeError("Cannot load tri_kho_viet_summarize.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.summarize(text, session_id)


def session_plain_text(path: Path, max_chars: int) -> str:
    lines_out = []
    if not path.exists():
        return ""

    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue

        role = obj.get("role") or obj.get("sender") or "msg"
        txt = ""
        if "content" in obj:
            txt = extract_text(obj.get("content"))
        if not txt:
            txt = extract_text(obj)
        txt = " ".join(txt.split())
        if txt:
            lines_out.append(f"{role}: {txt}")

    text = "\n".join(lines_out)
    if len(text) > max_chars:
        text = text[-max_chars:]
    return text


def process(sessions_dir: Path, out_dir: Path, state_path: Path, idle_minutes: int, max_chars: int) -> tuple[int, int]:
    now = datetime.now(timezone.utc).timestamp()
    idle_sec = idle_minutes * 60

    state = load_state(state_path)
    done = 0
    skipped = 0

    out_dir.mkdir(parents=True, exist_ok=True)

    for p in sorted(sessions_dir.glob("*.jsonl")):
        if p.name.endswith(".lock"):
            continue
        st = p.stat()
        age = now - st.st_mtime
        if age < idle_sec:
            skipped += 1
            continue

        sig = f"{int(st.st_mtime)}:{st.st_size}"
        key = str(p)
        if state.get(key) == sig:
            skipped += 1
            continue

        text = session_plain_text(p, max_chars=max_chars)
        if not text.strip():
            state[key] = sig
            skipped += 1
            continue

        session_id = p.stem
        summary_md = summarize_text(text, session_id)
        out_path = out_dir / f"{session_id}.md"
        out_path.write_text(summary_md, encoding="utf-8")

        state[key] = sig
        done += 1

    save_state(state_path, state)
    return done, skipped


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-dir", default=str(DEFAULT_SESSIONS_DIR))
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    ap.add_argument("--state", default=str(DEFAULT_STATE))
    ap.add_argument("--idle-minutes", type=int, default=30)
    ap.add_argument("--max-chars", type=int, default=20000)
    args = ap.parse_args()

    sessions_dir = Path(args.sessions_dir)
    if not sessions_dir.exists():
        print(f"Sessions dir not found: {sessions_dir}")
        return

    done, skipped = process(
        sessions_dir=sessions_dir,
        out_dir=Path(args.out_dir),
        state_path=Path(args.state),
        idle_minutes=args.idle_minutes,
        max_chars=args.max_chars,
    )
    print(f"rollup_done={done} skipped={skipped}")


if __name__ == "__main__":
    main()
