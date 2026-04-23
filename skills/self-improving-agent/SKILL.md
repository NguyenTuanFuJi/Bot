---
name: self-improvement
description: "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects the assistant, (3) User requests a missing capability, (4) An external API/tool fails, (5) Knowledge is outdated/incorrect, (6) A better recurring approach is discovered."
metadata:
---

# Self-Improvement Skill

Mục tiêu: ghi nhận lỗi/bài học ngắn gọn để tránh lặp sai, rồi nâng cấp dần thành quy ước ổn định.

## Khi nào phải dùng
- Lệnh chạy lỗi hoặc hành vi tool/API bất thường.
- Người dùng sửa lại câu trả lời/cách làm.
- Phát hiện cách làm tốt hơn cho tác vụ lặp lại.
- Người dùng yêu cầu tính năng chưa có.

## Cấu trúc bắt buộc
Trước khi log, đảm bảo có thư mục `.learnings/` với 3 file:
- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`

Nếu thiếu thì tạo, **không ghi đè file đang có**.

## Quy tắc an toàn dữ liệu
- Không log secret/token/private key/env nhạy cảm.
- Chỉ ghi tóm tắt hoặc bản đã che thông tin nhạy cảm.

## Ghi vào file nào
- Sai lệnh/lỗi tích hợp → `ERRORS.md`
- Sửa nhận định/cách làm, kiến thức mới, best practice → `LEARNINGS.md`
- Thiếu năng lực/tính năng người dùng yêu cầu → `FEATURE_REQUESTS.md`

## Mẫu ID
- Learning: `LRN-YYYYMMDD-XXX`
- Error: `ERR-YYYYMMDD-XXX`
- Feature: `FEAT-YYYYMMDD-XXX`

## Workflow tối thiểu
1. Ghi entry ngắn, đúng loại file.
2. Nếu trùng pattern cũ, thêm liên kết `See Also`.
3. Khi đã xử lý xong, cập nhật trạng thái (`resolved`/`promoted`).
4. Nếu có tính lặp cao, promote quy tắc sang file nền (`AGENTS.md`/`SOUL.md`/`TOOLS.md`).

## Promote khi nào
Promote sang quy ước nền khi:
- Lặp lại nhiều lần (>=3 lần), hoặc
- Ảnh hưởng rộng, dễ tái diễn, hoặc
- Là nguyên tắc cần nhớ cho mọi phiên.

## Tham chiếu (đọc khi cần)
- Hướng dẫn đầy đủ: `references/full-guide.md`
- OpenClaw integration: `references/openclaw-integration.md`
- Hook setup: `references/hooks-setup.md`
- Ví dụ mẫu: `references/examples.md`
- Script hỗ trợ:
  - `scripts/activator.sh`
  - `scripts/error-detector.sh`
  - `scripts/extract-skill.sh`

## Gợi ý vận hành nhanh
- Task nhỏ: log ngắn + rõ 1 hành động sửa.
- Task lớn/nhiều lỗi: gom theo pattern, tránh spam từng dòng vụn.
- Định kỳ rà `.learnings/` để dọn pending và promote cái đáng giữ.
