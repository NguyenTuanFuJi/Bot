---
name: memory-tiering
description: Organize memory into short-term, medium-term, and long-term layers during memory cleanup or compaction work. Use when reviewing what should stay active, what should become a stable preference or system fact, and what should be archived into durable summaries.
---

# Memory Tiering

Use three layers:

## HOT
Keep only what is needed in the next few turns:
- active task context
- immediate follow-ups
- temporary notes
- short-lived reminders

## WARM
Store stable but still practical context:
- user preferences
- recurring workflows
- important system setup details
- ongoing projects that still matter

## COLD
Archive durable summaries:
- finished project summaries
- long-term decisions
- lessons learned
- stable historical notes

## Workflow

1. Review recent memory and current task context
2. Mark completed or stale details
3. Move urgent items to HOT
4. Move stable reusable facts to WARM
5. Summarize finished items into COLD
6. Remove dead context that no longer helps

## BM25 Lite++ integration (áp dụng mặc định)
Khi làm retrieval trên memory hiện có:
1. Dùng pipeline nạp -> làm sạch/chunk -> index BM25
2. Lọc theo metadata trước khi rank BM25 (nếu có điều kiện thời gian/loại/session)
3. Normalize query ngắn gọn trước khi search
4. Giới hạn top-k để tránh phình context
5. Ghi log nhẹ để cải thiện dần chất lượng truy xuất

Tham chiếu chi tiết:
- `references/bm25-lite-plus.md`

## Rules
- Keep HOT small
- Prefer summaries over raw detail in long-term memory
- Do not store raw secrets when a file path or system source is enough
- Preserve user preferences and recurring operating rules carefully
- When unsure, summarize instead of deleting

## Typical trigger phrases
- run memory tiering
- organize memory
- prune memory
- archive old context
- compact memory notes

Use this skill as a cleanup workflow, not as a replacement for normal memory recall.
