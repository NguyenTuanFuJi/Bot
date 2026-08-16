# Workflow nội dung WordPress (CLI + App Password)

## Luồng chuẩn
1. **Kiểm tra trùng lặp (BẮT BUỘC)**
   - Đọc `memory/content-log.md` — lấy danh sách bài 30 ngày gần nhất
   - So sánh Topic Cluster + Focus Keyphrase + Content Angle
   - Nếu trùng keyphrase + góc → KHÔNG viết, báo sếp
   - Chi tiết: xem `skills/facebook-content-ops/references/content-dedup-checklist.md`
2. Soạn nội dung markdown
3. Tạo bài `draft`
3. QA nhanh:
   - Tiêu đề
   - Excerpt
   - Nội dung hiển thị
   - Link/CTA
4. Tối ưu ảnh SEO trước khi publish:
   - Tên file ảnh có từ khóa (không dấu, nối bằng `-`)
   - Alt text mô tả đúng nội dung ảnh
   - Title/Caption/Description ảnh đầy đủ
   - Gắn ảnh đại diện (featured image) đã tối ưu
5. Publish hoặc schedule

## Mẫu lệnh

### Tạo draft
```bash
bash scripts/wp_posts.sh create \
  --env .env \
  --title "Tiêu đề bài viết" \
  --content-file ./post.md \
  --status draft
```

### Publish bài theo ID
```bash
bash scripts/wp_posts.sh update \
  --env .env \
  --id 123 \
  --status publish
```

### Lên lịch (UTC)
```bash
bash scripts/wp_posts.sh update \
  --env .env \
  --id 123 \
  --status future \
  --date-gmt "2026-03-28T01:00:00"
```

### Danh sách bài gần nhất
```bash
bash scripts/wp_posts.sh list --env .env --per-page 10
```
