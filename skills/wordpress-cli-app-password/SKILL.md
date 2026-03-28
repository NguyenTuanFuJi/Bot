---
name: wordpress-cli-app-password
description: Vận hành nội dung WordPress theo 2 chế độ WP-CLI và REST API (Application Password). Dùng khi cần tạo/cập nhật/lên lịch/publish bài viết, chạy preflight an toàn, và đề xuất bước tiếp theo cho team content.
---

# WordPress Ops v2 (WP-CLI + Application Password)

Skill này giúp agent chọn đúng cách thao tác WordPress theo hạ tầng thực tế.

## Khi nào dùng
- Người dùng muốn đăng/cập nhật/lên lịch bài WordPress bằng CLI.
- Người dùng muốn vận hành content nhanh, có quy trình an toàn.
- Người dùng muốn dùng Application Password hoặc WP-CLI server.

## 2 chế độ vận hành

### Chế độ B — REST API + Application Password (mặc định ưu tiên)
Dùng làm phương pháp chính.

Ưu điểm:
- Dễ triển khai từ xa
- Phù hợp team content chỉ cần quản trị bài viết
- Ổn định với site đã chuẩn hóa `?rest_route=/...`

### Chế độ A — WP-CLI (chỉ dùng khi khả dụng)
Chỉ dùng khi đã kiểm tra `wp` khả dụng trên server WordPress.

Ưu điểm:
- Nhanh
- Ít lỗi xác thực HTTP
- Quản trị đầy đủ (core/plugin/theme/media/search-replace)

Lưu ý triển khai hiện tại:
- Skill đã chuẩn hóa endpoint REST sang dạng `?rest_route=/...` để tương thích các site không mở ổn `/wp-json/...`.

## Đường dẫn credential chuẩn (agent phải biết)
- WordPress env: `skills/wordpress-cli-app-password/.env`
- Mẫu env: `skills/wordpress-cli-app-password/references/env-template.md`

Khi thiếu app password/token, agent phải hướng người dùng cập nhật đúng file `.env` tại skill này.

## Triage + Preflight bắt buộc trước thao tác
1. Chạy triage để nhận diện dự án và công cụ:
```bash
bash scripts/wp_triage.sh <project_root>
```
2. Xác định mode: `wpcli` hay `rest`
3. Kiểm tra cấu hình env đầy đủ
4. Kiểm tra kết nối site bằng preflight
5. Chỉ sau khi pass preflight mới chạy create/update/publish

## Lệnh nhanh

### Vận hành bài viết (REST)
```bash
bash scripts/wp_posts.sh create --env .env --title "Tiêu đề" --content-file ./post.md --status draft
bash scripts/wp_posts.sh update --env .env --id 123 --status publish
bash scripts/wp_posts.sh update --env .env --id 123 --slug "slug-than-thien" --focuskw "tu-khoa-chinh" --seo-title "SEO Title" --meta-desc "Meta description"
bash scripts/wp_posts.sh list --env .env --per-page 10
```

### Vận hành bằng WP-CLI hoặc REST qua 1 entrypoint
```bash
bash scripts/wp_ops.sh preflight --env .env --mode wpcli
bash scripts/wp_ops.sh preflight --env .env --mode rest
bash scripts/wp_ops.sh create --env .env --mode wpcli --title "Tiêu đề" --content-file ./post.md --status draft
bash scripts/wp_ops.sh publish --env .env --mode wpcli --id 123
```

## Quy tắc an toàn
- Không in secret ra output.
- Không commit `.env`.
- Luôn tạo draft trước khi publish nếu chưa QA.
- Với thao tác rủi ro (search-replace), luôn chạy dry-run trước.
- Trước khi publish/schedule, bắt buộc tối ưu ảnh SEO (tên file + alt + title/caption/description + featured image).
- Với bài website có Yoast: bắt buộc theo checklist và DoD trong `references/yoast-seo-fujith-playbook.md` trước khi publish.

## Chuẩn đầu ra khi hoàn tất tác vụ
Agent nên trả về ngắn gọn:
1. Trạng thái (thành công/thất bại)
2. Kết quả chính (ID bài, URL, status)
3. Việc đề xuất tiếp theo

Mẫu:
- Trạng thái: ...
- Kết quả: ...
- Việc tiếp theo đề xuất: ...

## Tham chiếu
- `references/env-template.md`
- `references/wordpress-content-workflow.md`
- `references/wpcli-quick-ops.md`
- `references/wpcli-safe-ops.md`
- `references/wp-safe-checklist.md`
- `references/yoast-seo-fujith-playbook.md`
