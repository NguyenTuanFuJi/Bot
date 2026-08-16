# Checklist Kiểm Tra Trùng Lặp Nội Dụng (Dedup Gate)

**Áp dụng:** Bắt buộc trước khi viết BẤT KỲ bài mới nào (Facebook + Website)

---

## Bước 1: Tra cứu nội dung đã có

Đọc `memory/content-log.md` — lấy toàn bộ bài đã đăng/đang draft trong 30 ngày gần nhất.

Nếu cần kiểm tra sâu hơn:
- Website: chạy `wp_posts.sh list` hoặc curl API lấy danh sách post gần nhất
- Facebook: kiểm tra draft_fb_*.md trong workspace

---

## Bước 2: So sánh 3 tiêu chí

### A. Chủ đề chính (Topic Cluster)
Gom bài viết thành các nhóm chủ đề:
- Lắp đặt / quy trình
- Chi phí / báo giá
- Bảo dưỡng / sửa chữa
- Tiết kiệm điện
- An toàn / cứu hộ
- Vật liệu / cabin / thiết kế
- Công nghệ / động cơ
- MRL / không phòng máy
- So sánh loại thang
- Phong thủy / vị trí
- Sử dụng hàng ngày
- Uy tín / chọn nhà cung cấp

→ Nếu bài mới thuộc **cùng cluster** với bài đã có: chuyển sang so sánh tiêu chí B và C.

### B. Từ khóa Focus (Focus Keyphrase)
- So sánh focus keyphrase mới với keyphrase đã dùng trong 30 ngày
- **Trùng 100%** = ❌ KHÔNG được viết lại
- **Trùng ≥ 50% từ** = ⚠️ Cần khác góc ≥ 45°

### C. Góc tiếp cận (Content Angle)
Các góc viết phổ biến:
- **Hướng dẫn** (how-to): làm thế nào, bước nào
- **So sánh** (comparison): A vs B, ưu nhược điểm
- **Giải pháp** (solution): giải quyết vấn đề cụ thể
- **Cảnh báo** (warning): sai lầm, rủi ro, lưu ý
- **Tổng quan** (overview): giới thiệu, khái niệm
- **Case study** (proof): dự án thực tế, con số
- **Danh sách** (listicle): 5 lý do, 7 bước, 10 mẹo

→ Nếu cùng cluster + cùng góc: ❌ KHÔNG được viết

---

## Bước 3: Quyết định

| Kết quả | Hành động |
|---|---|
| ✅ Khác cluster → Proceed bình thường | Viết bài mới |
| ⚠️ Cùng cluster, khác góc ≥ 45° → Proceed có ghi chú | Viết bài, ghi rõ góc mới vào content-log |
| ⚠️ Cùng cluster + góc tương tự → Báo sếp | Nêu rõ: "Chủ đề X đã đăng ngày Y góc Z, đề xuất góc thay thế: W" |
| ❌ Trùng keyphrase + góc → Báo sếp | Không viết, đề xuất chủ đề khác hoàn toàn |

---

## Bước 4: Ghi nhận vào content-log

Sau khi bài được tạo (dù là draft), **PHẢI** cập nhật `memory/content-log.md` ngay:
- Ngày tạo
- Tiêu đề bài
- Focus keyphrase
- Topic cluster
- Content angle (góc viết)
- Trạng thái (draft / published)
- Post ID (nếu có)

---

## Bảng góc tiếp cận đã dùng (cập nhật theo thời gian)

| Topic Cluster | Bài đã đăng | Ngày | Focus Keyphrase | Góc đã dùng |
|---|---|---|---|---|
| MRL / không phòng máy | Thang Máy Gia Đình Không Phòng Máy (MRL): 5 Lợi Ích | 28/07 | thang máy gia đình không phòng máy | Lợi ích |
| MRL / không phòng máy | Thang Máy Không Phòng Máy (MRL): Ưu Nhược Điểm | 11/08 | thang máy không phòng máy | Ưu nhược điểm |
| Sai lầm lắp đặt | Lắp Thang Máy: 5 Sai Lầm Phổ Biến | 11/07 | lắp thang máy gia đình | Cảnh báo |
| Sai lầm lắp đặt | 5 sai lầm khi lắp thang máy gia đình (FB) | 11/08 | — | Cảnh báo |
| Tiết kiệm điện | Tiết Kiệm Điện Thang Máy: 6 Cách | 05/08 | tiết kiệm điện thang máy gia đình | Giải pháp |
| Tiết kiệm điện | Thang máy có tốn điện không? (FB) | 09/07 | — | Giải đáp |
| Tiết kiệm điện | Thang Máy Gia Đình Có Tốn Điện Không? | 10/08 | thang máy gia đình có tốn điện không | Giải đáp |
| Bảo dưỡng | 5 Dấu Hiệu Cần Bảo Dưỡng (FB) | 08/07 | — | Cảnh báo |
| Bảo dưỡng | 5 dấu hiệu cần bảo dưỡng ngay (FB) | 04/08 | — | Cảnh báo |
| Trọng tải | Cách Chọn Trọng Tải Thang Máy | 04/08 | trọng tải thang máy gia đình | Hướng dẫn |
| Động cơ | Động Cơ Thang Máy: So Sánh 4 Loại | 30/07 | động cơ thang máy gia đình | So sánh |
| Inox / vật liệu | Inox Thang Máy: So Sánh 304 Và 201 | 30/07 | inox thang máy gia đình | So sánh |
| Sử dụng hàng ngày | 6 Thói Quen Dùng Thang Máy Hàng Ngày | 29/07 | thói quen dùng thang máy gia đình | Hướng dẫn |
| Thời gian lắp đặt | Thời Gian Lắp Đặt: 4 Giai Đoạn | 28/07 | thời gian lắp đặt thang máy gia đình | Hướng dẫn |
| Quy trình lắp đặt | Quy Trình 6 Bước Tại FUJI TH | 27/07 | quy trình lắp đặt thang máy gia đình | Hướng dẫn |
| Tư vấn lần đầu | Tư Vấn Lần Đầu: 8 Câu Hỏi | 17/07 | tư vấn thang máy gia đình | Hướng dẫn |
| Báo giá | Báo Giá Thang Máy 2026 | 04/08 | báo giá thang máy gia đình | Giải pháp |
| Chi phí vận hành | Chi Phí Vận Hành: 6 Khoản Mục | 21/07 | chi phí vận hành thang máy gia đình | Giải pháp |
| Cửa thang máy | Cửa Tự Động Và Thủ Công | 25/07 | cửa thang máy gia đình | So sánh |
| Mất điện | Thang Máy Mất Điện: 5 Cơ Chế An Toàn | 25/07 | thang máy gia đình mất điện | Giải pháp |
| Nghiệm thu | Nghiệm Thu: 7 Bước Kiểm Tra | 24/07 | nghiệm thu thang máy gia đình | Hướng dẫn |
| Kích thước | Kích Thước: Bảng Quy Chuẩn | 22/07 | kích thước thang máy gia đình | Hướng dẫn |
| Phong thủy | Phong Thủy Vị Trí Đặt Thang Máy | 14/07 | phong thủy thang máy gia đình | Hướng dẫn |
| Ánh sáng cabin | Thiết Kế Ánh Sáng Cabin | 16/07 | thiết kế ánh sáng cabin thang máy | Hướng dẫn |
| Phối màu cabin | Phối Màu Nội Thất Cabin | 16/07 | phối màu cabin thang máy | Hướng dẫn |
| Chọn nhà cung cấp | Cách chọn thang máy uy tín: 7 tiêu chí | 12/07 | chọn thang máy gia đình uy tín | Hướng dẫn |
| Công nghệ FUJI TH | Công nghệ FUJI TH: 5 khác biệt | 15/07 | công nghệ thang máy FUJI TH | Giải pháp |
| 7 tiêu chí chọn | Chọn Thang Máy: 7 Tiêu Chí | 31/07 | chọn thang máy gia đình | Hướng dẫn |
| Trẻ nhỏ | Thang Máy Và Trẻ Nhỏ: 8 Tính Năng | 18/07 | thang máy gia đình trẻ nhỏ | Hướng dẫn |
| Mùa mưa | Thang Máy Mùa Mưa: 7 Lưu Ý | 18/07 | thang máy gia đình mùa mưa | Hướng dẫn |
| Tháng đầu dùng | Thang Mới Lắp Xong: 7 Điều | 10/07 | thang máy tháng đầu sử dụng | Hướng dẫn |
| Lắp đặt trọn gói | Lắp Đặt Trọn Gói: Quy Trình 6 Bước | 10/07 | lắp đặt thang máy gia đình | Hướng dẫn |
| 5 lý do chọn FUJI TH | 5 Lý Do Gia Đình Hà Nội Chọn FUJI TH | 25/07 | lắp đặt thang máy gia đình FUJI TH | Giải pháp |
| 7 cam kết | Thang Máy FUJI TH: 7 Cam Kết | 08/07 | — | Giải pháp |
| Hậu mãi | Dịch Vụ Hậu Mãi: 5 Cam Kết | 09/07 | — | Giải pháp |
| Trục vít vs cáp kéo | So Sánh Trục Vít Và Cáp Kéo | 09/07 | — | So sánh |
