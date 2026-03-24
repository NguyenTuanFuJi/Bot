#!/usr/bin/env python3
"""
Trí Khố Việt - Session summarizer (rule-based, no external LLM)
Input : plain transcript text file
Output: markdown bullet summary with keywords + purpose
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path
from datetime import datetime

STOPWORDS = {
    "là", "và", "của", "cho", "với", "trong", "được", "không", "các", "một",
    "này", "đó", "khi", "đang", "đã", "sẽ", "thì", "như", "để", "từ", "về",
    "the", "and", "for", "with", "from", "that", "this", "you", "your",
}

KEY_PATTERNS = {
    "decision": [r"\b(chốt|quyết định|đồng ý|ok|chuẩn)\b"],
    "todo": [r"\b(cần|hãy|tiếp tục|todo|việc cần làm|sẽ làm)\b"],
    "constraint": [r"\b(không được|phải|bắt buộc|ưu tiên|giới hạn)\b"],
    "purpose": [r"\b(mục tiêu|mục đích|để|nhằm)\b"],
}


def sent_split(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts = re.split(r"(?<=[\.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def extract_keywords(text: str, k: int = 12) -> list[str]:
    toks = re.findall(r"[\wÀ-ỹ]+", text.lower())
    toks = [t for t in toks if len(t) >= 3 and t not in STOPWORDS and not t.isdigit()]
    cnt = Counter(toks)
    return [w for w, _ in cnt.most_common(k)]


def pick_lines(lines: list[str], patterns: list[str], n: int = 5) -> list[str]:
    out = []
    for ln in lines:
        low = ln.lower()
        if any(re.search(p, low) for p in patterns):
            out.append(ln)
        if len(out) >= n:
            break
    return out


def summarize(text: str, session_id: str) -> str:
    lines = sent_split(text)

    decisions = pick_lines(lines, KEY_PATTERNS["decision"], n=6)
    todos = pick_lines(lines, KEY_PATTERNS["todo"], n=6)
    constraints = pick_lines(lines, KEY_PATTERNS["constraint"], n=5)
    purposes = pick_lines(lines, KEY_PATTERNS["purpose"], n=3)

    purpose = purposes[0] if purposes else (lines[0] if lines else "(chưa xác định)")
    kw = extract_keywords(text, k=12)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    def bullets(items: list[str]) -> str:
        if not items:
            return "  - (không có)"
        return "\n".join([f"  - {x}" for x in items])

    md = []
    md.append(f"## Session: {session_id} | {now}")
    md.append(f"- Mục tiêu: {purpose}")
    md.append("- Quyết định:")
    md.append(bullets(decisions))
    md.append("- Việc dang dở:")
    md.append(bullets(todos))
    md.append("- Ràng buộc:")
    md.append(bullets(constraints))
    md.append(f"- Từ khoá: [{', '.join(kw)}]")
    return "\n".join(md) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Transcript text path")
    ap.add_argument("--session-id", required=True)
    ap.add_argument("--out", required=True, help="Output markdown path")
    args = ap.parse_args()

    text = Path(args.input).read_text(encoding="utf-8", errors="ignore")
    out = summarize(text, args.session_id)
    p = Path(args.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding="utf-8")
    print(f"Wrote summary: {p}")


if __name__ == "__main__":
    main()
