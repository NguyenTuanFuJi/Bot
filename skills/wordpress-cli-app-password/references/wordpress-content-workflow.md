# Workflow nội dung WordPress (CLI + App Password)

## Luồng chuẩn
1. Soạn nội dung markdown
2. Tạo bài `draft`
3. QA nhanh:
   - Tiêu đề
   - Excerpt
   - Nội dung hiển thị
   - Link/CTA
4. Publish hoặc schedule

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
