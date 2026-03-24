---
name: wordpress-cli-app-password
description: Quản trị nội dung WordPress bằng CLI với Application Password. Dùng khi cần đăng bài, cập nhật bài, lên lịch, đổi trạng thái draft/publish, thêm tags/categories và kiểm tra kết quả qua REST API.
---

# WordPress CLI + Application Password

Skill này giúp agent thao tác WordPress bằng CLI, không cần đăng nhập wp-admin mỗi lần.

## Khi nào dùng
- Người dùng muốn đăng/cập nhật/lên lịch bài WordPress bằng lệnh
- Người dùng muốn tự động hóa quy trình xuất bản nội dung
- Người dùng yêu cầu dùng Application Password để xác thực an toàn

## Yêu cầu
- Có `curl`, `jq`
- Có thông tin:
  - `WP_BASE_URL` (vd: `https://example.com`)
  - `WP_USER`
  - `WP_APP_PASSWORD`

## Thiết lập nhanh
1. Tạo Application Password trong WordPress user profile.
2. Tạo file `.env` nội bộ theo mẫu trong `references/env-template.md`.
3. Chạy script trong `scripts/`.

## Tác vụ chính
- Tạo bài draft/publish
- Cập nhật bài theo ID
- Lên lịch bài (status=future + date)
- Lấy danh sách bài gần nhất

## Lệnh khuyến nghị
```bash
bash scripts/wp_posts.sh create --env .env --title "Tiêu đề" --content-file ./post.md --status draft
bash scripts/wp_posts.sh update --env .env --id 123 --title "Tiêu đề mới"
bash scripts/wp_posts.sh list --env .env --per-page 10
```

## Quy tắc an toàn
- Không in Application Password ra màn hình.
- Không commit `.env` chứa secret.
- Luôn tạo draft trước khi publish nếu chưa QA nội dung.

## Quy trình chuẩn gợi ý
1. Tạo nội dung
2. Đẩy lên WordPress ở trạng thái draft
3. QA tiêu đề, slug, excerpt, category/tag
4. Publish hoặc schedule

## Tham chiếu
- `references/env-template.md`
- `references/wordpress-content-workflow.md`
