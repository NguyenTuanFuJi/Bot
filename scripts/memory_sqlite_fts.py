#!/usr/bin/env python3
"""
Lightweight Markdown + SQLite FTS5 indexer for OpenClaw memory files.
- No vector DB
- No extra LLM/API
- Vietnamese-friendly full-text search (BM25 ranking)

Usage:
  python3 scripts/memory_sqlite_fts.py rebuild
  python3 scripts/memory_sqlite_fts.py search "nội dung cần tìm" --limit 10
"""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "memory" / "memory_fts.db"
MEMORY_MD = ROOT / "MEMORY.md"
MEMORY_DIR = ROOT / "memory"


def conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA synchronous=NORMAL;")
    return c


def init_db(c: sqlite3.Connection) -> None:
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS docs (
          id INTEGER PRIMARY KEY,
          path TEXT NOT NULL UNIQUE,
          title TEXT,
          mtime INTEGER NOT NULL,
          body TEXT NOT NULL,
          indexed_at TEXT NOT NULL
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(
          title, body, path UNINDEXED, content='docs', content_rowid='id'
        );

        CREATE TRIGGER IF NOT EXISTS docs_ai AFTER INSERT ON docs BEGIN
          INSERT INTO docs_fts(rowid, title, body, path) VALUES (new.id, new.title, new.body, new.path);
        END;
        CREATE TRIGGER IF NOT EXISTS docs_ad AFTER DELETE ON docs BEGIN
          INSERT INTO docs_fts(docs_fts, rowid, title, body, path) VALUES ('delete', old.id, old.title, old.body, old.path);
        END;
        CREATE TRIGGER IF NOT EXISTS docs_au AFTER UPDATE ON docs BEGIN
          INSERT INTO docs_fts(docs_fts, rowid, title, body, path) VALUES ('delete', old.id, old.title, old.body, old.path);
          INSERT INTO docs_fts(rowid, title, body, path) VALUES (new.id, new.title, new.body, new.path);
        END;
        """
    )
    c.commit()


def all_memory_files() -> list[Path]:
    files = []
    if MEMORY_MD.exists():
        files.append(MEMORY_MD)
    if MEMORY_DIR.exists():
        # include nested summaries, journals, and any markdown memory shards
        for p in sorted(MEMORY_DIR.rglob("*.md")):
            files.append(p)
    # de-dup while preserving order
    seen = set()
    out = []
    for f in files:
        if f in seen:
            continue
        seen.add(f)
        out.append(f)
    return out


def first_heading(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()
    return "(untitled)"


def upsert_file(c: sqlite3.Connection, p: Path) -> None:
    body = p.read_text(encoding="utf-8", errors="ignore")
    title = first_heading(body)
    mtime = int(p.stat().st_mtime)
    indexed_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    c.execute(
        """
        INSERT INTO docs(path, title, mtime, body, indexed_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(path) DO UPDATE SET
          title=excluded.title,
          mtime=excluded.mtime,
          body=excluded.body,
          indexed_at=excluded.indexed_at
        """,
        (str(p.relative_to(ROOT)), title, mtime, body, indexed_at),
    )


def rebuild() -> None:
    c = conn()
    init_db(c)
    existing = {row[0] for row in c.execute("SELECT path FROM docs")}
    now = set()
    for p in all_memory_files():
        rp = str(p.relative_to(ROOT))
        now.add(rp)
        upsert_file(c, p)
    # remove stale docs
    stale = existing - now
    if stale:
        c.executemany("DELETE FROM docs WHERE path = ?", [(s,) for s in stale])
    c.commit()
    total = c.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
    print(f"Indexed {total} memory files into {DB_PATH}")


def search(query: str, limit: int) -> None:
    c = conn()
    init_db(c)
    rows = c.execute(
        """
        SELECT d.path,
               snippet(docs_fts, 1, '[', ']', ' … ', 24) AS excerpt,
               bm25(docs_fts) AS score
        FROM docs_fts
        JOIN docs d ON d.id = docs_fts.rowid
        WHERE docs_fts MATCH ?
        ORDER BY score
        LIMIT ?
        """,
        (query, limit),
    ).fetchall()
    if not rows:
        print("No results.")
        return
    for i, (path, excerpt, score) in enumerate(rows, 1):
        print(f"{i}. {path}  (bm25={score:.4f})")
        print(f"   {excerpt}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)

    sp.add_parser("rebuild")
    s = sp.add_parser("search")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=10)

    args = ap.parse_args()
    if args.cmd == "rebuild":
        rebuild()
    elif args.cmd == "search":
        search(args.query, args.limit)


if __name__ == "__main__":
    main()
