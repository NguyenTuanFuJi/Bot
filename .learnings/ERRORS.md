# Errors

Command failures and integration errors.

---

## [ERR-20260403-001] clawhub_install_rate_limit

**Logged**: 2026-04-03T08:07:00+07:00
**Priority**: medium
**Status**: monitored
**Area**: integration

### Summary
Cài skill từ ClawHub bị 429 rate limit ở lượt đầu.

### Error
```
ClawHub /api/v1/download failed (429): Rate limit exceeded
```

### Context
- Hành động: cài skill self-improving-agent
- Kết quả: retry thành công sau chờ ngắn

### Suggested Fix
Áp dụng backoff khi gặp 429 và hạn chế burst call.

### Metadata
- Reproducible: unknown
- Tags: clawhub, install, retry

---
