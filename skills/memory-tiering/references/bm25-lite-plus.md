# BM25 Lite++ cho Memory (nhẹ, thực dụng)

## Mục tiêu
Tăng chất lượng truy xuất memory mà không thêm vector DB/LLM ngoài.

## 1) Ingestion pipeline (3 bước)
1. Nạp dữ liệu: memory markdown + session summary.
2. Làm sạch/chunk: tách đoạn gọn, bỏ nhiễu lặp.
3. Index BM25: rebuild FTS sau khi có thay đổi đáng kể.

## 2) Metadata-first retrieval
Mỗi ghi chú nên có metadata cơ bản:
- nguồn (memory/preferences/session_summaries)
- thời gian
- loại nội dung (preference, decision, todo, summary)
- session id (nếu có)

Khi truy xuất:
- lọc metadata trước (nếu có điều kiện)
- rồi mới rank BM25

## 3) Query normalizer (nhẹ)
Trước khi search:
- chuẩn hóa chữ hoa/thường
- bỏ khoảng trắng thừa
- map một số synonym nghiệp vụ ngắn

Ví dụ synonym:
- "đăng web" -> "wordpress publish"
- "bài fb" -> "facebook post"
- "sếp" -> "user preference"

## 4) Observability tối giản
Ghi log nhỏ cho mỗi lượt search:
- query gốc
- query sau normalize
- top-k trả về
- thời gian xử lý
- có được dùng hay bị bỏ qua

## 5) Guardrail context
- Giới hạn đoạn trả về theo nhu cầu, không đổ quá nhiều đoạn.
- Ưu tiên đoạn mới + đúng loại nội dung.

## Checklist áp dụng nhanh
- Có cập nhật memory lớn? -> rebuild FTS
- Query mơ hồ? -> normalize trước
- Có yêu cầu theo ID/session/time? -> lọc metadata trước
- Kết quả dài quá? -> cắt top-k + summary ngắn
