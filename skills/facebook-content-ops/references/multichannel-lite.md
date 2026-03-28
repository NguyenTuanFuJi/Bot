# Multi-channel Lite (giảm context)

## Nguyên tắc
- Không gộp nhiều nền tảng trong cùng một lượt xử lý dài.
- Tách thành 3 pha độc lập: Viết -> Duyệt -> Đăng.
- Mỗi lượt chỉ xử lý 1 việc chính.

## Pha 1: Viết
Đầu ra bắt buộc:
- Bản dài (website nếu cần)
- Bản ngắn (Facebook)
- CTA rõ

## Pha 2: Duyệt
- Chỉ nhận 1 trong 3 kết quả: duyệt / sửa / viết lại.
- Không được đăng khi chưa có tín hiệu duyệt.

## Pha 3: Đăng
- Facebook: dùng path ảnh trực tiếp, không base64 trong context.
- WordPress: dùng REST + media upload riêng, rồi mới tạo post.
- Sau đăng phải báo trạng thái + link.

## Chống phình context
- Không paste payload dài lặp lại nhiều lần.
- Chỉ giữ các biến bắt buộc: mục tiêu, nội dung đã chốt, giờ đăng, ảnh.
- Nếu nhiều bài: chạy theo batch nhỏ (1 bài/lượt).
