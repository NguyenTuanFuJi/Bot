# Trí Khố Việt — Đặc tả mục tiêu (v1)

## Mục tiêu
Thiết kế lớp nhớ cho OpenClaw theo hướng nhẹ, ổn định, ưu tiên tiếng Việt, giảm token context khi gọi model.

## Yêu cầu bắt buộc
1. **Dùng tốt cho tiếng Việt**
   - Lưu UTF-8 đầy đủ.
   - Chuẩn hoá từ khoá tiếng Việt (giữ dấu, đồng thời tạo biến thể không dấu để tìm kiếm).

2. **Giảm context gọi API**
   - Không nạp toàn bộ lịch sử cũ.
   - Trước mỗi phiên mới, chỉ bơm vào context phần tóm tắt ngắn (bullet + keyword + mục đích).
   - Giới hạn độ dài tóm tắt theo ngân sách token (ví dụ 300–700 token).

3. **Không mất trí nhớ của agent**
   - Dữ liệu nhớ lưu local, bền vững: `MEMORY.md`, `memory/*.md`, và SQLite.
   - SQLite chạy WAL để giảm rủi ro hỏng dữ liệu.
   - Có snapshot/backup định kỳ.

4. **Tổng hợp session cũ ngắn gọn theo bullet/keyword/mục đích**
   - Mỗi session sinh ra 1 bản tóm tắt chuẩn:
     - `Mục tiêu:`
     - `Quyết định:`
     - `Việc dang dở:`
     - `Ràng buộc:`
     - `Từ khoá:`
   - Ưu tiên tóm tắt theo quy tắc (rule-based), không phụ thuộc LLM ngoài.

5. **Ghi nhớ tự động dữ liệu quan trọng**
   - Auto-capture khi có tín hiệu:
     - quyết định cuối cùng
     - deadline/thời gian
     - cấu hình/khoá logic (không lưu secret nhạy cảm dạng plaintext)
     - TODO quan trọng
   - Gắn mức độ ưu tiên: `critical/high/normal`.

6. **Truy vấn tự động và nhanh**
   - Dùng SQLite FTS5/BM25 để recall text-only, không vector.
   - Truy vấn nền < 200ms cho tập dữ liệu nhỏ/vừa (mục tiêu).

## Kiến trúc đề xuất
- **Store tầng 1 (nguồn chuẩn):** Markdown (`MEMORY.md`, `memory/*.md`)
- **Store tầng 2 (index):** SQLite + FTS5 (BM25)
- **Pipeline:**
  1) ingest session mới
  2) trích ý chính rule-based
  3) ghi summary + keywords
  4) update index
  5) phục vụ recall nhanh

## Định dạng tóm tắt chuẩn (đề xuất)
```md
## Session: <id> | <time>
- Mục tiêu: ...
- Quyết định:
  - ...
- Việc dang dở:
  - ...
- Ràng buộc:
  - ...
- Từ khoá: [k1, k2, k3]
```

## Tiêu chí nghiệm thu (MVP)
- [ ] Có script build index từ markdown sang SQLite FTS5.
- [ ] Có script `search` trả kết quả theo BM25.
- [ ] Có script `summarize-session` tạo bullet/keyword/mục đích.
- [ ] Có cơ chế auto-capture dữ liệu quan trọng.
- [ ] Có cron định kỳ tạo bản tóm tắt session cũ.
- [ ] Có giới hạn độ dài context khi inject vào phiên mới.

## Lộ trình ngắn
- P1: index + search (đã có nền)
- P2: auto summarize session -> markdown
- P3: auto capture + score ưu tiên
- P4: cron định kỳ + tối ưu recall cho phiên mới
