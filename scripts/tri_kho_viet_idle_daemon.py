#!/usr/bin/env python3
"""
Trí Khố Việt - Idle-triggered session summarizer daemon

Behavior:
- Observe session activity by latest mtime of *.jsonl under OpenClaw sessions dir
- If activity stops for `idle_minutes`, run one rollup pass + FTS rebuild
- Trigger once per idle period (no periodic forced summary)
"""
from __future__ import annotations

import argparse
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSIONS_DIR = Path("/home/tuan/.openclaw/agents/main/sessions")


def latest_mtime(sessions_dir: Path) -> float:
    mt = 0.0
    if not sessions_dir.exists():
        return mt
    for p in sessions_dir.glob("*.jsonl"):
        try:
            st = p.stat()
            if st.st_mtime > mt:
                mt = st.st_mtime
        except FileNotFoundError:
            continue
    return mt


def run_rollup(idle_minutes: int) -> None:
    subprocess.run(
        [
            "python3",
            str(ROOT / "scripts" / "tri_kho_viet_auto_rollup.py"),
            "--idle-minutes",
            str(idle_minutes),
        ],
        cwd=str(ROOT),
        check=False,
    )
    subprocess.run(
        ["python3", str(ROOT / "scripts" / "memory_sqlite_fts.py"), "rebuild"],
        cwd=str(ROOT),
        check=False,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--idle-minutes", type=int, default=30)
    ap.add_argument("--poll-seconds", type=int, default=20)
    args = ap.parse_args()

    idle_seconds = args.idle_minutes * 60

    last_seen_mtime = latest_mtime(SESSIONS_DIR)
    last_change_at = time.time()
    rolled_for_current_idle = False

    while True:
        now = time.time()
        mt = latest_mtime(SESSIONS_DIR)

        if mt > last_seen_mtime:
            last_seen_mtime = mt
            last_change_at = now
            rolled_for_current_idle = False

        idle_for = now - last_change_at

        if idle_for >= idle_seconds and not rolled_for_current_idle:
            run_rollup(args.idle_minutes)
            rolled_for_current_idle = True

        time.sleep(max(5, args.poll_seconds))


if __name__ == "__main__":
    main()
