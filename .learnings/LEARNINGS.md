# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260403-001] best_practice

**Logged**: 2026-04-03T08:07:00+07:00
**Priority**: high
**Status**: active
**Area**: workflow

### Summary
Main agent áp dụng nguyên tắc: cách xử lý file theo skill, nội dung theo đúng yêu cầu sử dụng của sếp.

### Details
Giảm sai lệch khi xử lý tác vụ Word/Excel/Vision và giảm việc tự suy diễn ngoài phạm vi yêu cầu.

### Suggested Action
Mọi tác vụ văn phòng phải kiểm theo checklist: đúng file, đúng field, đúng định dạng đầu ra.

### Metadata
- Source: user_feedback
- Tags: office-work, skill-driven, main-agent

---

## [LRN-20260420-001] correction

**Logged**: 2026-04-20T14:24:13+07:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Workspace preference file had outdated address style and conflicted with current user preference.

### Details
The preferences file said to address the user as 'bệ hạ' and self as 'thần', but current workspace/user instructions prefer 'sếp' and 'em'. User also clarified no Chinese should appear in chat, evidence paths should not be shown, and blockers should only be mentioned when real blockers exist.

### Suggested Action
Keep USER.md and memory/preferences.md aligned with the latest conversation-level preference. Prefer Vietnamese-only chat, 'sếp/em' address style, no routine evidence lines, and only mention blockers when they exist.

### Metadata
- Source: user_feedback
- Related Files: USER.md, memory/preferences.md
- Tags: preferences, language, tone, correction

---
