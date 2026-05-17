# Errors

Command failures and integration errors.

---
## [ERR-20260510-001] brave_search_conflicting_time_filters

**Logged**: 2026-05-10T22:00:00+07:00
**Priority**: low
**Status**: resolved
**Area**: integration

### Summary
Gọi Brave search với cả `freshness` và `date_after` cùng lúc làm request bị từ chối.

### Error
```
conflicting_time_filters: freshness and date_after/date_before cannot be used together
```

### Context
- Operation: tìm link bài web để tổng hợp báo cáo cuối ngày
- Tool: web_search
- Cause: truyền đồng thời bộ lọc tương đối (`freshness`) và khoảng ngày (`date_after`)

### Suggested Fix
Chỉ dùng một kiểu lọc thời gian cho mỗi request: hoặc `freshness`, hoặc `date_after/date_before`.

### Metadata
- Reproducible: yes
- Tags: brave, web_search, filters

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

## [ERR-20260420-001] wordpress-cli-app-password

**Logged**: 2026-04-20T12:45:00+07:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Example command in skill used relative scripts/wp_triage.sh from workspace root, but actual script path is under skills/wordpress-cli-app-password/scripts/wp_triage.sh.

### Error
```
bash: scripts/wp_triage.sh: No such file or directory
```

### Context
- Command attempted from workspace root using example path from skill guidance
- Correct path discovered via find under skill directory

### Suggested Fix
Document the absolute or skill-relative path explicitly in the workflow examples for OpenClaw workspace usage.

### Metadata
- Reproducible: yes
- Related Files: skills/wordpress-cli-app-password/SKILL.md

---

## [ERR-20260421-001] web_search

**Logged**: 2026-04-21T20:31:00+07:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
Brave web_search rejects combined freshness and explicit date range filters.

### Error
```
conflicting_time_filters: freshness and date_after/date_before cannot be used together
```

### Context
- Operation attempted: external research for daily web content ideation
- Input used both `freshness=month` and `date_after/date_before`
- Result: request failed before returning search results

### Suggested Fix
Use either freshness or explicit date range, not both, for Brave search calls.

### Metadata
- Reproducible: yes
- Related Files: none

---
## [ERR-20260422-001] brave_web_search_ui_lang_and_rate_limit

**Logged**: 2026-04-22T20:30:00+07:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Brave web_search rejected ui_lang=vi-VN and then hit free-plan 429 on a second immediate query.

### Error
```
422 validation: ui_lang must be one of supported enums; vi-VN not accepted.
429 rate limit exceeded for plan.
```

### Context
- Attempted Vietnamese-market research with web_search.
- First request failed on unsupported ui_lang value.
- Second request succeeded with en-US UI locale.
- Third immediate request hit plan rate limit.

### Suggested Fix
Use supported ui_lang values only (e.g. en-US) and serialize Brave queries more conservatively.

### Metadata
- Reproducible: yes
- Related Files: n/a

---
## ERR-20260424-001
- status: resolved
- context: web cron chuẩn bị bài WordPress
- issue: web_search dùng ui_lang=vi-VN không hợp lệ với Brave; web_fetch gặp 403 anti-bot ở site nguồn.
- fix: đổi sang ui_lang=en-US khi cần Brave; dùng web_search snippets làm tín hiệu ý tưởng thay vì phụ thuộc fetch toàn trang.
- See Also: wordpress web cron



## ERR-20260425-001
- status: resolved
- context: Dò tên ảnh thư viện trong HTML bài WordPress gần nhất.
- issue: Lệnh bash `grep -oE` bị vỡ quoting do trộn nhiều dấu nháy trong one-liner.
- fix: Với pattern chứa quote phức tạp, ưu tiên tách sang Python hoặc dùng here-doc để tránh lỗi escape shell.

- ERR-20260426-001 | status: resolved | context: web_search Brave API rejected ui_lang=vi-VN with 422 validation error during daily web-idea research. fix: use supported ui_lang (en-US) or web_fetch/direct source fallback.

---
## [ERR-20260429-001] web_search

**Logged**: 2026-04-29T08:00:00+07:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
web_search trả lỗi khi truyền đồng thời freshness và date_after/date_before trong lúc nghiên cứu ý tưởng bài Facebook.

### Error
```
conflicting_time_filters: freshness and date_after/date_before cannot be used together
```

### Context
- Operation: web_search
- Query intent: tìm ý tưởng về thang máy gia đình khi mất điện / ARD
- Cause: truyền cả freshness=year và date_after/date_before

### Suggested Fix
Chỉ dùng một kiểu lọc thời gian trong mỗi lần gọi web_search.

### Metadata
- Reproducible: yes
- Related Files: none
- See Also: ERR-20260418-001
## ERR-20260501-001
- Date: 2026-05-01
- Status: open
- Context: Dùng tool image_generate mặc định để tạo ảnh mẫu marketing.
- Issue: Provider trả HTTP 400: tool choice image_generation không tồn tại trong tools parameter.
- Impact: Không tạo ảnh được qua image_generate trong phiên này.
- Workaround: Dùng skill codex-imagen qua script local node bridge thay cho image_generate.
- Next step: Với tác vụ tạo ảnh, ưu tiên codex-imagen skill khi provider mặc định lỗi kiểu này.


- ID: ERR-20260502-001
  time: 2026-05-02 20:30 Asia/Saigon
  tool: web_search
  issue: Dùng đồng thời freshness và date_after gây lỗi conflicting_time_filters.
  fix: Với Brave search chỉ dùng một kiểu lọc thời gian; retry bằng freshness hoặc date range, không kết hợp.
  status: resolved

- ID: ERR-20260502-002
  time: 2026-05-02 20:31 Asia/Saigon
  tool: web_search
  issue: ui_lang=vi-VN không được Brave hỗ trợ.
  fix: Dùng ui_lang=en-US khi tìm tiếng Việt nếu vi-VN bị từ chối.
  status: resolved

## [ERR-20260503-001] python_http_client_remote_disconnect

**Logged**: 2026-05-03T09:06:00+07:00
**Priority**: low
**Status**: pending
**Area**: integration

### Summary
Lệnh nền good-orb kết thúc code 1 với traceback Python http.client trong giai đoạn đọc response status.

### Error
```
http.client.RemoteDisconnected / _read_status during response.begin()
```

### Context
- Nguồn: exec completion event
- Dấu hiệu: traceback Python 3.12 đi qua http.client.py -> _read_status
- Hiện tại chưa có full stdout/stderr trong heartbeat nên không suy luận thêm nguyên nhân nghiệp vụ

### Suggested Fix
Khi gặp lại pattern này, kiểm tra service/endpoint phía xa có đóng kết nối sớm không và bọc retry/backoff cho request idempotent. Nếu là script dài, lưu log đầy đủ để lần sau chẩn đoán được nguyên nhân gốc.

### Metadata
- Reproducible: unknown
- Related Files: none
- Tags: python, http-client, remote-disconnect, exec-event


## ERR-20260503-001 · WP REST update returns title in POST response but title empty on later edit fetch
- Date: 2026-05-03
- Status: open
- Context: Updating WordPress draft post 2810 via REST/app-password. POST update response included title.raw/rendered correctly, but subsequent GET with context=edit returned title_raw/title_rendered empty while content and Yoast meta persisted.
- Impact: Cannot trust REST title verification on this site; publishing should pause until title is verified by alternate path.
- Safe workaround: When title matters, verify via front-end/admin or alternate API path before publish. Keep a local content backup before metadata-only updates because mixed updates can blank content/title unexpectedly.

- ERR-20260504-001 | 2026-05-04 | web_search Brave validation lỗi khi dùng freshness cùng date_after/date_before và khi đặt ui_lang=vi-VN. Cách tránh: chỉ dùng 1 kiểu lọc thời gian; ui_lang dùng giá trị hợp lệ như en-US. | resolved

## ERR-20260504-002
- status: resolved
- context: Báo giá công trình chú Luyện
- issue: Tính sai hệ số nhôm và diện tích kính; đã lấy nhôm x4 thay vì x5 tầng, và dùng 40-50m² thay vì quy ước ước tính 15m/tầng khi người dùng nhắc.
- correction: Với báo giá thang kính theo tầng, khi user nêu quy tắc theo tầng thì ưu tiên nhân theo số tầng cho nhôm và kính, không giữ số cũ nếu đã bị user sửa.

- ERR-20260506-001 | trạng thái: open | bối cảnh: tạo ảnh Facebook | lỗi: gọi sai đường dẫn script codex-imagen ở /workspace/scripts/... không tồn tại | hướng sửa: tìm đúng vị trí script trước khi chạy, hoặc ưu tiên tool image_generate nếu đủ đáp ứng.
- ERR-20260506-002 | trạng thái: open | bối cảnh: đăng album Facebook | lỗi: script cron-safe-post-album.sh lỗi curl option - unknown khi nhận message file nhiều dòng | hướng sửa: đọc script/cli hiện có và dùng đường publish phù hợp hoặc vá script sau khi xác nhận.


## ERR-20260507-001
- Date: 2026-05-07
- Status: open
- Context: Tạo 3 ảnh minh hoạ tay vịn thang máy cho bài Facebook/web.
- Issue: Tool `image_generate` trả lỗi HTTP 400: `Tool choice 'image_generation' not found in 'tools' parameter`.
- Impact: Không tạo được ảnh bằng tool ảnh mặc định trong lượt này.
- Workaround: Dùng skill `codex-imagen` qua script `codex-imagen-cliproxy-auth.mjs` khi `image_generate` lỗi backend.
- See Also: codex-imagen skill


## ERR-20260507-002
- Date: 2026-05-07
- Status: open
- Context: Sửa file hợp đồng .docx theo hàng/cột bảng đặc tính.
- Issue: Dùng chỉ số `table.cell(row, col)` sai vì bảng có merge/structure khác kỳ vọng, gây `IndexError`.
- Impact: Chỉnh sửa thất bại ở lượt đầu, dễ làm sai vị trí khi sửa hợp đồng mẫu.
- Workaround: Luôn duyệt `row.cells` thực tế theo từng hàng trước khi ghi, không giả định số cột cố định từ lần inspect trước.
- See Also: ERR-20260507-001

- ERR-20260508-001 | resolved | Python subprocess không nhận WP_* env sau khi source .env nếu chưa export; dùng `set -a; source ...; set +a` trước khi gọi Python hoặc truyền env tường minh.
