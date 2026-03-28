---
name: facebook-content-ops
description: Vận hành nội dung Facebook theo hướng SEO + chuyển đổi. Dùng khi người dùng muốn lập kế hoạch nội dung, đề xuất việc cần làm, tối ưu bài trước khi đăng, quản lý comment sau đăng, và theo dõi KPI page.
---

# Facebook Content Ops

Skill này giúp agent **tự đề xuất công việc** và vận hành nội dung Facebook theo chu trình rõ ràng.

## Khi nào dùng
- Người dùng nói về: kế hoạch content Facebook, SEO Facebook, lịch đăng bài, tối ưu caption, kéo inbox, quản lý comment, theo dõi hiệu quả bài đăng.
- Người dùng yêu cầu: “đề xuất việc cần làm”, “lên kế hoạch tuần/tháng”, “tối ưu bài trước khi đăng”.

## Mục tiêu
1. Tăng tiếp cận tự nhiên (SEO trong Facebook Search + đề xuất)
2. Tăng tương tác chất lượng
3. Tăng chuyển đổi (inbox/lead/đơn)

## Quy trình chuẩn (rút gọn, tránh trùng lặp)

### Bước 0 (bắt buộc)
Trước mọi tác vụ nội dung, phải đọc và tuân thủ:
- `references/sop-viet-duyet-dang.md`
- `references/prepublish-gate.md`
- `references/facebook-content-standard.md`

### Bước 1: Chốt mục tiêu tuần
- Mục tiêu chính: `reach | engagement | inbox | lead | sale`
- Sản phẩm/dịch vụ ưu tiên
- Tệp khách hàng chính

### Bước 2: Đề xuất backlog theo tuần
Sinh backlog theo `references/facebook-weekly-jobpack.md` (tối đa 5 việc/lần).

### Bước 3: Viết + duyệt + đăng
- Viết theo chuẩn nội dung và random style.
- Chạy prepublish gate trước khi gửi duyệt.
- Chỉ đăng khi đã duyệt; đăng xong báo kết quả + link.

Nếu workspace có script tối ưu nội dung, ưu tiên dùng:
```bash
node skills/facebook-page-manager/scripts/fb_content_optimize.js --input <payload.json>
```

### Bước 4: Hậu kiểm + báo cáo
- Hậu kiểm 30–120 phút sau đăng.
- Cuối tuần xuất: việc đã làm, KPI, 3 ưu tiên tuần sau.

## Quy tắc đề xuất công việc
- Đề xuất ngắn, rõ, có thứ tự ưu tiên
- Mỗi việc có đầu ra cụ thể
- Không đề xuất quá 5 việc/lần để tránh quá tải

## Quy tắc tự động sau khi duyệt nội dung
Khi người dùng đã duyệt nội dung và chốt giờ đăng:
- Agent tự lên lịch đăng, không hỏi lại bước xác nhận trung gian.
- Đến giờ đăng, agent tự thực thi đăng bài.
- Sau khi đăng xong, agent tự báo kết quả (thành công/thất bại + link bài nếu có).

## Mẫu đầu ra đề xuất nhanh
- Việc 1 (Ưu tiên cao): ...
- Việc 2: ...
- Việc 3: ...
- Kết quả kỳ vọng: ...

## Tham chiếu
- `references/facebook-content-checklist.md`
- `references/facebook-weekly-plan-template.md`
- `references/facebook-weekly-jobpack.md` (bộ công việc theo tuần)
- `references/facebook-content-standard.md` (chuẩn hoá nội dung trước khi đăng)
- `references/sop-viet-duyet-dang.md` (quy trình bắt buộc viết-duyệt-đăng)
- `references/prepublish-gate.md` (cổng kiểm trước duyệt/đăng)
- `references/fuji-th-brand-profile.md` (thông tin thương hiệu dùng lâu dài)
- `references/writing-style-randomization.md` (quy tắc random writing style chống trùng)

## Quy định khi người dùng yêu cầu “làm theo tuần”
Agent phải ưu tiên đọc:
1. `references/facebook-weekly-jobpack.md`
2. `references/facebook-content-standard.md`

Sau đó xuất ra:
- Danh sách việc theo ngày trong tuần
- 3 việc ưu tiên cao nhất
- KPI cần theo dõi cuối tuần
