# Báo cáo cá nhân — Day 6

- **Họ và tên:** Phạm Quỳnh Anh
- **MSSV:** 2A202603671
- **Lớp:** L3A

## Dữ liệu và pipeline
- **Chủ đề, nguồn/quyền, số trang và quy tắc tính trang:**
  - Chủ đề: Tài liệu đầu tư giá trị — trích đoạn *Nhà đầu tư thông minh (The Intelligent Investor)* bản dịch tiếng Việt (Lời nói đầu & Tưởng niệm của Warren E. Buffett, Chú giải của Jason Zweig, Phần mở đầu & Chương 1 của Benjamin Graham).
  - Nguồn & quyền: File nội bộ `starter/data/sách.pdf` dùng cho học tập/thực hành cá nhân tại máy local. Do sách có bản quyền thương mại nên không commit file `.pdf` gốc lên repository công khai (đã khai báo trong `.gitignore` và mô tả tại [data/manifest.json](../../data/manifest.json)).
  - Số trang & quy tắc tính: File có `33` trang vật lý, trong đó **`32` trang nội dung hợp lệ** (mỗi trang PDF có ≥ 100 ký tự tiếng Việt chuẩn hóa NFC). Loại bỏ `1` trang (`pdf_page=31`, `book_page=5`, chỉ có 65 ký tự dòng chú thích tái bản). Lưu ý: thứ tự trang trong PDF bị đảo ngược so với số trang sách (`pdf_page` 33 → 1 tương ứng `book_page` 3 → 35).
- **Chuẩn hóa, lỗi và giới hạn:**
  - Dùng `pypdf` đọc từng trang, chuẩn hóa Unicode về `NFC`, giữ nguyên dấu ngắt dòng để phục vụ tái tạo đoạn văn.
  - Lỗi nguồn PDF: Một số ký tự tiếng Việt trong bản PDF gốc bị lỗi dấu từ quá trình OCR/xuất bản trước đó (ví dụ `"thế kỷ"` → `"thể kỷ"`, `"đầu tư"` → `"đầu tu"`, `"về"` → `"vê"`). Hiện tượng này được giữ nguyên trung thực và ghi nhận là hạn chế của nguồn dữ liệu.
- **Embedding model/provider/version/số chiều, vector store/version, metric, lệnh chạy và chi phí:**
  - Embedding: `gemini-embedding-001` qua Google Gemini API (`RETRIEVAL_DOCUMENT` cho văn bản và `RETRIEVAL_QUERY` cho câu hỏi), số chiều `3072`. *(Ghi chú: ban đầu thử OpenAI API nhưng gặp lỗi `429 - hết credit`, nên đã chuyển sang Gemini Free Tier có cơ chế tự đợi 38s khi chạm giới hạn 100 requests/phút).*
  - Vector store: `chromadb==1.5.9` (PersistentClient lưu tại `starter/results/chroma_db`), metric `cosine`. *(Máy không có Docker nên dùng Chroma local thay cho `pgvector`).*
  - Lệnh chạy (từ `starter/`): `C:\Users\Admin\.venvs\day06\Scripts\python.exe -m src.run`
  - Chi phí: `$0` (dùng Gemini Free Tier).
- **Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn:**
  - Bắt buộc: `document_id`, `source`, `page` (`pdf_page`).
  - Bổ sung: `book_page` (số trang in trên sách), `section` (`preface_buffett`, `commentary_graham_intro`, `introduction`, `commentary_intro`, `chapter_1`, `commentary_ch1`), `author_role` (`buffett`, `zweig`, `graham`).
  - Nguồn giá trị & lý do: Trích trực tiếp từ ranh giới chương/mục trong tài liệu ([data/manifest.json](../../data/manifest.json)), giúp phân biệt rõ lời khuyên gốc của Benjamin Graham với bình luận cập nhật của Jason Zweig và lời nói đầu của Warren Buffett.

## Cấu hình và benchmark
- **A / B / C (tham số cụ thể, khác biệt duy nhất B–C):**
  - **A**: `fixed_size(size=500, overlap=50)`, không dùng metadata filter.
  - **B**: `by_paragraph(max_size=800)`, tái tạo đoạn văn từ PDF và gom đoạn đến tối đa 800 ký tự, không dùng metadata filter *(so sánh A–B để đo riêng tác động của chunking)*.
  - **C**: `by_paragraph(max_size=800)`, **khác biệt duy nhất so với B** là áp dụng metadata filter (`section` hoặc `author_role`) khi câu hỏi có chỉ định phạm vi *(so sánh B–C để đo riêng tác động của metadata filtering)*.
- **≥20 câu: phân chia ≥15 dev / ≥5 test, câu metadata filter và cách kiểm chứng evidence:**
  - Tổng **20 câu hỏi** trong [benchmark/questions.json](../../benchmark/questions.json), tách trước khi chạy thử thành **15 câu `dev`** (`q01`–`q15`) và **5 câu `test`** (`q16`–`q20`).
  - Có **4 câu kiểm tra metadata filter** (`q04`, `q09`, `q14` ở `dev` và `q18` ở `test`).
  - Kiểm chứng: Toàn bộ 20 `evidence_quote` được kiểm tra tự động qua hàm `_verify_benchmark_quotes` để đảm bảo xuất hiện nguyên văn trên đúng `gold_page` sau chuẩn hóa trước khi đánh giá.
- **Tiêu chí chọn chiến lược đã chốt trước khi xem test:**
  - Ưu tiên `Evidence Hit@3`, tiếp theo là `Grounding quality` và `Chunk coherence`, cuối cùng mới xét số chunk và thời gian ingest.

## Kết quả
| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian (ingest) | Chi phí |
|---|---|---:|---:|---:|---:|---:|
| A | dev | 10/15 (66.7%) | 14/15 (93.3%) | 218 | 127.75s | $0 |
| A | test | 3/5 (60.0%) | 4/5 (80.0%) | 218 | 127.75s | $0 |
| B | dev | 11/15 (73.3%) | 14/15 (93.3%) | 171 | 88.01s | $0 |
| B | test | 3/5 (60.0%) | 5/5 (100.0%) | 171 | 88.01s | $0 |
| C | dev | 11/15 (73.3%) | 14/15 (93.3%) | 171 | 0.45s (reuse vectors) | $0 |
| C | test | 3/5 (60.0%) | 5/5 (100.0%) | 171 | 0.45s (reuse vectors) | $0 |

| Strategy | Coherence trung bình /2 (n) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N hoặc N/A) | Grounding 0/1/2 (số câu) và trung bình /2 |
|---|---:|---:|---:|---|
| A | 1.20 / 2.0 (n=10) | 15/15 | N/A | 0: 1, 1: 0, 2: 4 — TB: 1.60 / 2.0 |
| B | 1.50 / 2.0 (n=10) | 15/15 | N/A | 0: 0, 1: 0, 2: 5 — TB: 2.00 / 2.0 |
| C | 1.50 / 2.0 (n=10) | 15/15 | 1/1 (test), 3/3 (dev) | 0: 0, 1: 0, 2: 5 — TB: 2.00 / 2.0 |

- Đường dẫn trace, nhãn thủ công và cách chọn mẫu:
  - Trace top-3: `starter/results/traces_A.json`, `starter/results/traces_B.json`, `starter/results/traces_C.json`.
  - Tổng hợp số liệu: `starter/results/summary.json` và [artifacts/experiment_log.csv](../../artifacts/experiment_log.csv).
  - Nhãn audit thủ công: `starter/results/manual_audit_completed.md` (10 trang đầu cố định `pdf_page` 1–10 cho Coherence; 5 câu `test` `q16`–`q20` cho Metadata & Grounding).

## Phân tích và kết luận
- **So sánh A–B và B–C; 2 ví dụ sai có ID câu và nguồn:**
  - **A vs B (Chunking)**: Chiến lược B giảm 21.6% số lượng chunk (171 so với 218), cải thiện `Dev Hit@1` (11/15 so với 10/15), `Test Hit@3` (5/5 so với 4/5), `Coherence` (1.50 so với 1.20) và `Grounding` (2.00 so với 1.60).
    - *Ví dụ sai 1 (`q20`, tập `test`, `gold_page=14`)*: Ở **A**, câu hỏi về nguyên tắc quản lý tiền vốn khi đầu cơ bị miss (`Hit@3=False`, top-3 trả về `pdf_page` 20, 5, 20) do cửa sổ 500 ký tự cắt ngang đoạn văn, làm mất ngữ cảnh nối giữa *"thử vận may"* và *"dành một khoản càng nhỏ càng tốt trong quỹ riêng"*. Ở **B**, đoạn văn được giữ trọn nên truy xuất đúng ở Top-2.
    - *Ví dụ sai 2 (`q02`, tập `dev`, `gold_page=33`)*: Ở **B/C**, câu hỏi về *"chương 8 và chương 20"* bị miss `Hit@3` (`top-3` trả về `pdf_page` 33 đoạn đầu, 20, 27) vì đoạn chứa đáp án nằm ở nửa sau trang 33 bị tách thành chunk riêng không lọt top-3, trong khi **A** nhờ overlap 50 ký tự giữ được cụm từ khóa lọt Top-3.
  - **B vs C (Metadata Filter)**: Trên tập 20 câu hiện tại, chỉ số Hit@1 và Hit@3 giữa B và C bằng nhau do model `gemini-embedding-001` đã phân biệt ngữ nghĩa tốt giữa lời văn của Graham và Zweig. Tuy nhiên **C** đạt **100% tuân thủ filter (4/4 câu)**, đảm bảo loại bỏ hoàn toàn rủi ro trả nhầm tác giả/phần sách khi người dùng chỉ định rõ phạm vi.
- **Chiến lược chọn, đánh đổi, điều kiện áp dụng:**
  - Chọn **Chiến lược C** (`by_paragraph` + metadata filter khi có yêu cầu).
  - Đánh đổi: Cần công sức chuẩn hóa và gán nhãn `section`/`author_role` khi ingest (phụ thuộc cấu trúc tài liệu), nhưng đổi lại giảm 21.6% chi phí lưu trữ/embedding so với fixed-size và tăng độ tin cậy truy xuất theo phạm vi.
- **Hạn chế của dữ liệu, nhãn, test nhỏ, đo thời gian/chi phí:**
  - Tập `test` chỉ có 5 câu (và 1 câu filter) nên sự khác biệt 1 câu tạo chênh lệch 20%, chưa đủ lớn để kết luận tổng quát cho toàn bộ cuốn sách 515 trang.
  - Nhãn audit thủ công do chính tác giả chấm nên tồn tại nguy cơ thiên lệch chủ quan.
  - Thời gian ingest của A và B bao gồm cả thời gian ngủ chờ rate limit 38s/lần của Gemini Free Tier, không phản ánh thuần túy tốc độ tính toán.
  - Dữ liệu bị lỗi dấu tiếng Việt rải rác từ bản PDF gốc và thứ tự trang PDF bị đảo ngược.
- **Nếu làm lại hoặc mở rộng, cải tiến gì?**
  - Ghép đoạn văn xuyên ranh giới trang (`cross-page paragraph merging`) để khắc phục việc đầu mỗi trang PDF bị cắt giữa câu.
  - Mở rộng benchmark lên 50+ câu trên toàn bộ các chương sách và thêm tìm kiếm hybrid (BM25 + dense vector) cho các câu hỏi chứa tên riêng hoặc số hiệu chương (như `q02`).

