# WordPress FUJI TH - Hướng dẫn vận hành

Cập nhật: 2026-06-25

## Thông tin công ty
- Tên: CÔNG TY TNHH FUJI TH
- Địa chỉ: Số 10, ngõ 117, phố Mai Phúc, phường Phúc Lợi, Hà Nội
- Điện thoại: 0989 397 282 – 0924 286 386
- MST: 0109220557
- Email: fujith557@gmail.com

## Quy tắc bắt buộc
- Luôn dùng đúng SĐT, địa chỉ, email từ thông tin công ty — KHÔNG tự ý bịa/thay đổi.
- SĐT khi ghi nội dung: viết liền 10 số, không tách khoảng trắng/chấm/gạch.
- **Chỉ làm thang cáp kéo** — KHÔNG đăng bài, tư vấn, hoặc gợi ý thang trục vít, thang thủy lực, thang không hố pit.

## Thông tin site
- URL: https://thangmayfujith.com
- User: fuji-temp (Chuyen Nguyen, ID: 2)
- Credentials: `skills/wordpress-cli-app-password/.env`
- Mode ưu tiên: REST API + Application Password

## Skill chính
- Vị trí: `skills/wordpress-cli-app-password/`
- SKILL.md: Quy trình chính (triage → preflight → thao tác)

## Scripts
- `scripts/wp_triage.sh` — Kiểm tra project
- `scripts/wp_ops.sh` — Lệnh chính: preflight/create/update/publish
- `scripts/wp_posts.sh` — Quản lý bài viết

## References (tài liệu tham khảo)
- `references/yoast-seo-fujith-playbook.md` — Quy tắc SEO/Yoast FUJI TH
- `references/wordpress-content-workflow.md` — Luồng soạn → draft → QA → publish
- `references/site-categories-fujith.md` — Category theo loại bài
- `references/wp-safe-checklist.md` — Checklist an toàn
- `references/wp-sql-security-lite.md` — Kiểm tra bảo mật SQL/PHP
- `references/wpcli-quick-ops.md` / `wpcli-safe-ops.md` — Lệnh WP-CLI

## Category FUJI TH
| ID | Tên | Slug | Dùng cho |
|---|---|---|---|
| 72 | Chia sẻ - Kinh nghiệm | chia-se-kinh-nghiem | Bài kiến thức/hướng dẫn |
| 71 | Dự án đã làm | du-an-da-lam | Case study/công trình |
| 1 | Về thang máy | ve-thang-may | Giới thiệu tổng quan |

## Quy trình chuẩn (workflow)
1. Soạn nội dung markdown
2. Tạo bài `draft`
3. QA nhanh: tiêu đề, excerpt, nội dung, link/CTA
4. Tối ưu ảnh SEO: tên file có từ khóa, alt text, featured image
5. Kiểm tra Yoast SEO (xem checklist bên dưới)
6. Publish hoặc schedule

## Checklist Yoast bắt buộc trước publish
- Focus keyphrase (≤ 4 từ)
- SEO title bắt đầu bằng keyphrase
- Meta description 140–160 ký tự
- Slug chứa keyphrase
- Keyphrase ở câu đầu mở bài
- ≥ 1 ảnh + alt chứa keyphrase
- ≥ 1 internal link + ≥ 1 outbound link
- Không trùng slug/title với bài đã có

## Lệnh thao tác chuẩn

### Preflight
```bash
cd skills/wordpress-cli-app-password
bash scripts/wp_ops.sh preflight --env .env --mode rest
```

### Check trùng slug/title
```bash
cd skills/wordpress-cli-app-password
source .env
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/?rest_route=/wp/v2/posts&per_page=100&_fields=id,slug,title" | jq
```

### Tạo draft
```bash
bash scripts/wp_posts.sh create --env .env --title "Tiêu đề" --content-file ./post.html --status draft
```

### Publish bài
```bash
bash scripts/wp_posts.sh update --env .env --id <POST_ID> --status publish
```

### Update SEO + nội dung
```bash
bash scripts/wp_ops.sh update --env .env --mode rest --id <POST_ID> \
  --title "..." --slug "..." --focuskw "..." \
  --seo-title "..." --meta-desc "..." \
  --content-file ./post.html --status publish
```

### Lên lịch (UTC)
```bash
bash scripts/wp_posts.sh update --env .env --id <POST_ID> --status future --date-gmt "2026-03-28T01:00:00"
```

### Danh sách bài gần nhất
```bash
bash scripts/wp_posts.sh list --env .env --per-page 10
```

## Bài học vận hành quan trọng
- Tuyệt đối không gửi update rỗng (title/content rỗng) vì có thể làm mất dữ liệu hiển thị
- Khi chỉ muốn sửa SEO meta, vẫn phải giữ nguyên title/content hoặc dùng payload chỉ chứa meta fields
- Sau update, luôn re-open Yoast và bấm Re-analyze để nhận điểm mới
- Luôn chạy draft trước, publish sau khi sếp duyệt
- Không in secret ra log

## Ghi chú từ session 2026-06-25
- Bài ID 2907, 2904, 2855 bị trống title.rendered (có thể do theme hoặc cấu hình hiển thị)
- Cần kiểm tra thêm nếu sếp muốn sửa

## 2026-08-04: Tự động đăng bài không chờ duyệt
- REST API bị chặn (404), chuyển sang XML-RPC API
- XML-RPC endpoint: https://thangmayfujith.com/xmlrpc.php
- Auth: user=fuji-temp, pass=Kd1a iK2j KXAm cxMO HZjf KXDC
- wp.newPost → tạo draft, wp.editPost(status=publish) → publish
- Tất cả cron job đã cập nhật: tự đăng ngay, không gửi sếp duyệt
- Báo kết quả + link qua Telegram sau khi đăng
