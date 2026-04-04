# WP + SQL Security Lite (ưu tiên vận hành)

## Mục tiêu
Bổ sung lớp kiểm tra bảo mật thực dụng cho website WordPress có liên quan SQL/PHP trước khi deploy hoặc sau khi sửa code.

## Phạm vi kiểm tra nhanh
- SQL Injection: truy vấn raw SQL không sanitize/prepare.
- XSS: output không escape đúng ngữ cảnh.
- CSRF: form/action không có nonce verify.
- Access control: thiếu kiểm tra quyền khi thao tác admin/AJAX/REST.
- File upload: thiếu whitelist MIME/extension, thiếu validate.

## Quy trình 3 bước
1. Quick scan trước release:
   - rà vùng thay đổi mới (diff hoặc module vừa sửa)
2. Spot fix:
   - sửa các điểm high/critical trước
3. Re-check:
   - chạy lại quick scan + test đường dẫn chính

## SQL rule tối thiểu
- Không nối chuỗi trực tiếp để tạo câu SQL có input người dùng.
- Với query có input: luôn sanitize + prepare.
- Không log dữ liệu nhạy cảm từ truy vấn.

## Kết quả cần báo
- Số lỗi theo mức độ: critical/high/medium
- Danh sách lỗi high/critical đã xử lý
- Mục còn tồn tại + khuyến nghị bước tiếp
