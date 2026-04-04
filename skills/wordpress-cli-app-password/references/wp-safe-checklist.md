# Checklist an toàn (bắt buộc)

## Trước thao tác
- Xác nhận đúng môi trường (dev/staging/prod)
- Xác nhận đúng mode (wpcli/rest)
- Chạy preflight thành công
- Nếu thao tác rủi ro: backup trước
- Nếu có thay đổi code liên quan SQL/PHP: đọc `references/wp-sql-security-lite.md`

## Trong thao tác
- Không in secret ra log
- Giới hạn phạm vi thay đổi
- Với search-replace: luôn dry-run trước
- Không nối chuỗi SQL trực tiếp với dữ liệu input

## Sau thao tác
- Kiểm tra trạng thái lệnh
- Kiểm tra URL/bài viết hiển thị đúng
- Nếu có thay đổi code: chạy quick security check trước khi chốt
- Ghi nhận kết quả + đề xuất bước tiếp
