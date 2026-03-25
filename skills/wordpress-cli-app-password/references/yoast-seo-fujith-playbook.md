# FUJI TH · Yoast SEO Playbook (mẫu áp dụng)

Áp dụng mặc định cho bài chia sẻ kinh nghiệm và bài dự án trước khi publish.

## 1) Trường bắt buộc Yoast
- Focus keyphrase (ưu tiên <= 4 từ nội dung)
- SEO title (bắt đầu bằng keyphrase)
- Meta description (140–160 ký tự, có keyphrase)
- Slug chứa keyphrase

## 2) Checklist bắt buộc trước publish
1. Keyphrase xuất hiện ngay câu đầu đoạn mở đầu.
2. Có ít nhất 1 ảnh và alt ảnh chứa keyphrase hoặc biến thể gần nghĩa.
3. Có ít nhất 1 internal link tới bài cùng nhóm.
4. Có ít nhất 1 outbound link tới nguồn uy tín (nếu bài dạng hướng dẫn/kiến thức).
5. Keyphrase xuất hiện trong nhiều H2/H3 quan trọng và phân bổ đều toàn bài.
6. Không trùng lặp tiêu đề/slug/keyphrase với bài đã có.

## 3) Mẫu cho bài hố pit thang máy 2026
- Focus keyphrase: `hố pit thang máy 2026`
- SEO title: `Hố pit thang máy 2026: chuẩn kỹ thuật, tối ưu chi phí thi công`
- Slug: `ho-pit-thang-may-2026`
- Meta description: `Hướng dẫn xây hố pit thang máy 2026 đúng kỹ thuật, chống thấm hiệu quả, giảm phát sinh chi phí khi vật giá tăng.`

## 4) Category mặc định theo loại bài
- Chia sẻ kiến thức/hướng dẫn → ID 72 (Chia sẻ - Kinh nghiệm)
- Bài dự án/case study → ID 71 (Dự án đã làm)

## 5) Quy tắc chống trùng lặp nội dung
- Mỗi bài chỉ dùng 1 keyphrase chính.
- Không dùng lại nguyên tiêu đề cũ.
- Kiểm tra slug và tiêu đề trong danh sách bài trước khi publish.
- Nếu chủ đề tương tự, đổi góc tiếp cận và ví dụ thực tế.

## 6) Definition of Done (DoD) để được publish
- Không còn lỗi đỏ Yoast.
- Keyphrase có trong: câu đầu mở bài, SEO title, slug, meta description, tối thiểu 2 tiêu đề H2/H3.
- Mật độ keyphrase không vượt ngưỡng Yoast cảnh báo (tránh nhồi từ khóa).
- Có >= 1 ảnh + alt liên quan keyphrase.
- Có >= 2 internal links và >= 1 outbound link thường (không nofollow toàn bộ).
- Đã kiểm tra trùng lặp tiêu đề/slug/keyphrase trước khi đăng.

## 7) Lệnh thực thi chuẩn (REST route)
```bash
# 1) Preflight
bash skills/wordpress-cli-app-password/scripts/wp_ops.sh preflight --env skills/wordpress-cli-app-password/.env --mode rest

# 2) Check trùng slug/title trước publish
source skills/wordpress-cli-app-password/.env
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/?rest_route=/wp/v2/posts&per_page=100&_fields=id,slug,title" | jq

# 3) Update SEO + nội dung
bash skills/wordpress-cli-app-password/scripts/wp_ops.sh update \
  --env skills/wordpress-cli-app-password/.env \
  --mode rest \
  --id <POST_ID> \
  --title "..." \
  --slug "..." \
  --focuskw "..." \
  --seo-title "..." \
  --meta-desc "..." \
  --content-file skills/wordpress-cli-app-password/tmp/<file>.html \
  --status publish
```

## 8) Bài học vận hành quan trọng
- Tuyệt đối không gửi update rỗng (title/content rỗng) vì có thể làm bài mất dữ liệu hiển thị.
- Khi chỉ muốn sửa SEO meta, vẫn phải giữ nguyên title/content hoặc dùng payload chỉ chứa meta fields.
- Sau update, luôn re-open Yoast và bấm Re-analyze để nhận điểm mới.