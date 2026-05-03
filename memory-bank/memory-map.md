# Memory Map (HOT / WARM / COLD)

Mục tiêu: thống nhất cách skill memory-tiering ghi nhớ vào Memory Bank để giữ ngữ cảnh gọn, đúng, dùng lại được.

## 1) HOT (ngắn hạn, vài lượt tới)
Ghi vào:
- `memory-bank/activeContext.md`

Nội dung phù hợp:
- Việc đang làm ngay
- Quyết định vừa chốt
- Follow-up cần xử lý sớm
- Rủi ro/blocked cần theo dõi tức thời

Nguyên tắc:
- Ngắn, dạng bullet
- Chỉ giữ thứ cần cho phiên hiện tại và phiên kế tiếp gần nhất
- Xong việc thì chuyển xuống WARM/COLD hoặc xóa khỏi HOT

## 2) WARM (ổn định, dùng lặp)
Ghi vào:
- `memory-bank/systemPatterns.md`
- `memory-bank/techContext.md`
- `memory-bank/productContext.md` (phần ổn định)

Nội dung phù hợp:
- Quy trình lặp lại nhiều lần
- Chuẩn vận hành/kỹ thuật đã ổn định
- Preference làm việc có giá trị dài hơn 1 phiên
- Bối cảnh sản phẩm/thương hiệu ít thay đổi

Nguyên tắc:
- Chỉ lưu điều đã kiểm chứng là hữu ích lặp lại
- Tránh nhồi log chi tiết theo ngày

## 3) COLD (dài hạn, lưu dấu mốc)
Ghi vào:
- `memory-bank/progress.md`
- `memory/session_summaries/`

Nội dung phù hợp:
- Mốc hoàn thành
- Bài học rút ra
- Quyết định lớn đã chốt
- Tóm tắt phiên để tra cứu sau

Nguyên tắc:
- Ưu tiên tóm tắt hơn dữ liệu thô
- Ghi theo mốc, không ghi vụn vặt

## 4) Quy trình cập nhật đề xuất
1. Bắt đầu phiên: đọc `activeContext.md` trước.
2. Trong phiên: nếu phát sinh pattern ổn định -> cập nhật WARM.
3. Kết phiên/mốc lớn: cập nhật `progress.md` + tóm tắt phiên nếu cần.
4. Dọn HOT định kỳ: bỏ mục đã hết giá trị.

## 5) Quy tắc an toàn dữ liệu
- Không lưu raw secrets/tokens vào Memory Bank.
- Nếu cần tham chiếu nhạy cảm, chỉ ghi nguồn hoặc đường dẫn nội bộ phù hợp.
- Không ghi dữ liệu thừa không phục vụ công việc.

## 6) Áp dụng cho FujiTH
- HOT: job đang chạy, bài đang duyệt, lịch đăng trong ngày.
- WARM: quy trình Viết -> Duyệt -> Đăng, chuẩn SEO/Yoast, chuẩn Facebook.
- COLD: các mốc chiến dịch đã xong, tổng kết tuần/tháng, lỗi lặp đã có hướng xử lý.
