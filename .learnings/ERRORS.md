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
## [ERR-20260417-001] facebook cron-safe-post-album.sh

**Logged**: 2026-04-17T01:04:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Wrapper đăng album Facebook lỗi khi caption có số điện thoại ở đầu bằng dấu gạch nối.

### Error
```
curl: option -: is unknown
```

### Context
- Operation: đăng album Facebook qua scripts/cron-safe-post-album.sh
- Input: caption chứa dòng `📞 0924286386 - 0989397282`
- Likely cause: script build curl command không quote an toàn với message nhiều dòng/ký tự đặc biệt

### Suggested Fix
Sửa wrapper để truyền message từ file bằng cơ chế an toàn hoặc dùng `--form-string` / mảng argv không eval.

### Metadata
- Reproducible: yes
- Related Files: skills/facebook-page-manager/scripts/cron-safe-post-album.sh

---
## [ERR-20260417-002] gateway_update_run_timeout

**Logged**: 2026-04-17T17:28:00+07:00
**Priority**: medium
**Status**: pending
**Area**: integration

### Summary
Gọi gateway.update.run để cập nhật OpenClaw bị timeout sau 120 giây.

### Error
```
gateway timeout after 120000ms
Gateway target: ws://127.0.0.1:18789
```

### Context
- Operation: cập nhật OpenClaw theo yêu cầu người dùng
- Tool: gateway(action=update.run)
- Sau lỗi đã kiểm tra `openclaw status`: gateway vẫn chạy bình thường, trạng thái cập nhật báo up to date.

### Suggested Fix
Thử lại update.run với timeout dài hơn (ví dụ 300-600s) và theo dõi logs nếu vẫn timeout.

### Metadata
- Reproducible: unknown
- Related Files: .learnings/ERRORS.md
- Tags: gateway, update, timeout

---
## [ERR-20260418-001] web_search

**Logged**: 2026-04-18T20:31:00+07:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
web_search trả lỗi do dùng đồng thời freshness và date_after

### Error
```
conflicting_time_filters: freshness and date_after/date_before cannot be used together
```

### Context
- Operation: web_search
- Query: xu hướng cải tạo nhà phố lắp thang máy gia đình tiết kiệm diện tích 2026 Việt Nam
- Cause: truyền cả freshness=month và date_after

### Suggested Fix
Chỉ dùng một kiểu lọc thời gian trong mỗi lần gọi web_search

### Metadata
- Reproducible: yes
- Related Files: none

---
