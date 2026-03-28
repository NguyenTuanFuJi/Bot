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

## Quy trình chuẩn

### Bước 0 (bắt buộc): Áp dụng SOP Viết → Duyệt → Đăng
Trước mọi tác vụ nội dung, agent phải đọc và tuân thủ:
- `references/sop-viet-duyet-dang.md`
- `references/prepublish-gate.md`

### Bước 1: Chốt mục tiêu tuần
Agent phải hỏi/chốt nhanh:
- Mục tiêu chính tuần này: `reach | engagement | inbox | lead | sale`
- Sản phẩm/dịch vụ ưu tiên
- Tệp khách hàng chính

### Bước 2: Tự đề xuất backlog công việc
Agent luôn đề xuất theo nhóm việc:
1. **Chiến lược**
   - Chốt 3 cụm chủ đề tuần
   - Chốt 1 ưu đãi/chào mời chính
2. **Sản xuất nội dung**
   - 2 bài giáo dục
   - 1 bài case/chứng thực
   - 1 bài chuyển đổi
3. **Tối ưu SEO Facebook**
   - Từ khóa chính/phụ cho từng bài
   - Hook + CTA + hashtag cụm
4. **Vận hành sau đăng**
   - Kịch bản phản hồi comment
   - Kịch bản kéo inbox
5. **Đo lường**
   - Reach, engagement, comment chất lượng, inbox/lead

### Bước 3: Tạo bài theo khung chuẩn
Mỗi bài phải có:
- Hook (dòng đầu)
- Nỗi đau/bối cảnh
- Giải pháp (bullet)
- Bằng chứng ngắn
- CTA duy nhất
- 3–5 hashtag

### Bước 4: Preflight trước đăng
Trước khi đăng, agent phải tự kiểm:
- Có từ khóa chính chưa
- CTA có rõ chưa
- Độ dài có dễ đọc không
- Hashtag có bị nhồi quá không

Nếu workspace có skill `facebook-page` và script tối ưu nội dung, ưu tiên dùng:
```bash
node skills/facebook-page-manager/scripts/fb_content_optimize.js --input <payload.json>
```
Chỉ đăng khi chất lượng đạt ngưỡng.

### Bước 5: Hậu kiểm sau đăng (30–120 phút)
Agent đề xuất ngay các việc:
- Trả lời comment ưu tiên cao
- Ghim comment CTA
- Tổng hợp câu hỏi lặp lại để tạo bài tiếp theo

### Bước 6: Báo cáo tuần
Agent luôn xuất 3 phần:
1. Việc đã làm
2. Kết quả theo KPI
3. Việc tuần sau (ưu tiên cao nhất)

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
