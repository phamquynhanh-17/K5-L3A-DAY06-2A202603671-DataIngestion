# Manual Audit Completed — Day 06

> **Lưu ý về thiên lệch (Bias):** Người chấm là tác giả bài làm (Phạm Quỳnh Anh). Để giảm thiên lệch, 10 trang chấm Coherence (PDF pages 1–10) được cố định trước khi xem điểm retrieval, và các nhãn Grounding được đối chiếu trực tiếp với `evidence_quote` và trang nguồn trong `traces_{A,B,C}.json`.

## 1. Chunk Coherence (10 vị trí nguồn cố định: PDF pages 1–10, thang 0–2)

Quy ước thang điểm: `0` = bị cắt giữa ý/thiếu chủ thể làm không hiểu; `1` = hiểu một phần, thiếu ngữ cảnh đầu hoặc cuối; `2` = tự hiểu được và giữ trọn ý.

| Page (PDF) | Score A | Score B/C | Lý do chấm |
|---:|---:|---:|---|
| 1 | 1 | 2 | A cắt ngang giữa từ/ý ở cuối cửa sổ 500 ký tự (`Chứng khoá...`). B/C giữ trọn đoạn về dự báo Qualcomm của PaineWebber. |
| 2 | 1 | 1 | Cả A và B/C đều bắt đầu giữa câu từ trang trước (`thuộc cung Kim Ngưu...`), nhưng B/C kết thúc trọn đoạn văn. |
| 3 | 1 | 2 | A cắt ngang đoạn về Palm và hình 1-1; B/C giữ trọn đoạn ví dụ về NASDAQ và Puma Technology. |
| 4 | 1 | 1 | Đầu trang nối tiếp từ trang 3 (`mô lớn...`), A cắt giữa chừng phần phân tích kỹ thuật đầu tư, B/C giữ trọn đoạn. |
| 5 | 2 | 2 | Đầu chương *BÌNH LUẬN VỀ CHƯƠNG 1*, cả A và B/C đều chứa trọn trích dẫn Blaise Pascal và lập luận mở đầu. |
| 6 | 1 | 1 | Bắt đầu giữa câu từ trang trước (`lớn nào lại muốn bán...`), A bị cắt cụt ở ký tự 500 còn B/C giữ hết đoạn 1957. |
| 7 | 1 | 1 | Bắt đầu giữa cụm từ (`sự ngốc nghếch của người khác...`); A cắt ngang phần bán khống, B/C giữ trọn đoạn. |
| 8 | 1 | 1 | Bắt đầu giữa câu (`chúng thường đang phát triển...`), B/C gom đủ đoạn kết luận tiếp theo. |
| 9 | 1 | 2 | A cắt ngang giữa phần giải thích phương pháp bình quân chi phí đô la; B/C giữ trọn ý phương pháp thứ ba. |
| 10 | 2 | 2 | Cả A và B/C đều bắt đầu từ đầu câu hoàn chỉnh (`Trong khi thảo luận về danh mục...`) và giữ rõ ngữ cảnh. |

- **Trung bình Coherence Strategy A**: `12 / 10 = 1.20 / 2.0`
- **Trung bình Coherence Strategy B & C**: `15 / 10 = 1.50 / 2.0`

## 2. Metadata Usefulness (5 câu test × top-3 = 15 bản ghi / chiến lược)

- Kiểm tra đối chiếu `source`, `page`, `section`, `author_role` trong `traces_{A,B,C}.json` với `data/manifest.json`:
  - **Strategy A**: `15/15` bản ghi có metadata đầy đủ và chính xác; Filter compliance: `N/A` (không dùng filter).
  - **Strategy B**: `15/15` bản ghi có metadata đầy đủ và chính xác; Filter compliance: `N/A` (không dùng filter).
  - **Strategy C**: `15/15` bản ghi có metadata đầy đủ và chính xác; Filter compliance: `1/1` trên tập test (`q18` với `section=commentary_ch1`), và `3/3` trên tập dev (`q04`, `q09`, `q14`).

## 3. Grounding Quality (5 câu test: `q16`–`q20`, thang 0–2)

Quy ước: `0` = không có bằng chứng; `1` = có nhưng thiếu điều kiện/ngữ cảnh; `2` = đủ để trả lời và truy nguồn.

| Question | Strategy A | Strategy B | Strategy C | Nhận xét |
|---|---:|---:|---:|---|
| `q16` (page 33) | 2 | 2 | 2 | Top-1 cả 3 chiến lược đều trả về đúng đoạn lời nói đầu của Warren Buffett (IQ vs khuôn khổ trí tuệ). |
| `q17` (page 29) | 2 | 2 | 2 | Top-1 cả 3 chiến lược đều chứa đầy đủ sự kiện Savold Tire (lãi 250% tháng 4/1919, lừa đảo tháng 10). |
| `q18` (page 1) | 2 | 2 | 2 | A có ở Top-2; B & C có ở Top-1/Top-2 kèm đầy đủ giải thích chi phí môi giới 8% của Plexus Group. C lọc đúng `section=commentary_ch1`. |
| `q19` (page 4) | 2 | 2 | 2 | Top-1 cả 3 chiến lược đều có đủ số liệu mức luân chuyển NYSE năm 1973 (20%) và 2002 (105%). |
| `q20` (page 14) | 0 | 2 | 2 | **A thất bại (0 điểm)**: top-3 trả về trang 20, 5, 20, không có bằng chứng quản lý quỹ đầu cơ. **B & C đạt 2 điểm**: Top-2 trả về đúng đoạn trên trang 14. |

- **Grounding Strategy A**: `0: 1 câu, 1: 0 câu, 2: 4 câu` → Trung bình `1.60 / 2.0`
- **Grounding Strategy B**: `0: 0 câu, 1: 0 câu, 2: 5 câu` → Trung bình `2.00 / 2.0`
- **Grounding Strategy C**: `0: 0 câu, 1: 0 câu, 2: 5 câu` → Trung bình `2.00 / 2.0`

