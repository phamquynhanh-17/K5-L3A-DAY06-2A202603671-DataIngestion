# Manual Audit Template

## 1. Chunk Coherence (10 fixed source pages, scale 0-2)

| Page (PDF) | Strategy A (first chunk preview) | Score A | Strategy B/C (first chunk preview) | Score B/C | Reason |
|---:|---|---:|---|---:|---|
| 1 | `35 PaineWebber đã dự đoán rằng chứng khoán của Qualcomm sẽ đạt 1.000 đô la một cổ phần trong 12 tháng sau đó. Chứng khoá...` | | `PaineWebber đã dự đoán rằng chứng khoán của Qualcomm sẽ đạt 1.000 đô la một cổ phần trong 12 tháng sau đó. Chứng khoán đ...` | | |
| 2 | `34 thuộc cung Kim Ngưu, tức là con bò tót, nên tôi phản ứng với màu đỏ. Nếu tôi thấy màu đỏ; tôi bán các cổ phiếu của mì...` | | `thuộc cung Kim Ngưu, tức là con bò tót, nên tôi phản ứng với màu đỏ. Nếu tôi thấy màu đỏ; tôi bán các cổ phiếu của mình ...` | | |
| 3 | `33 máy tính cầm tay Palm, một điều rất hợp với khẩu hiệu mới của công ty là "Mỗi giây đều quan trọng". HÌNH 1-1 Các cổ p...` | | `máy tính cầm tay Palm, một điều rất hợp với khẩu hiệu mới của công ty là "Mỗi giây đều quan trọng".  HÌNH 1-1 Các cổ phi...` | | |
| 4 | `32 mô lớn. Có vẻ như gằn như tất cả mọi người đã mất kiên nhẫn cùng một lúc, và Mỹ trở thành Đất nước Đầu cơ, trong đó g...` | | `mô lớn. Có vẻ như gằn như tất cả mọi người đã mất kiên nhẫn cùng một lúc, và Mỹ trở thành Đất nước Đầu cơ, trong đó gồm ...` | | |
| 5 | `31 BÌNH LUẬN VÊ CHƯƠNG 1 Tất cả sự bất hạnh của nhân loại đèu do một thứ mà ra: không biết cách giữ được sự thư thái tro...` | | `BÌNH LUẬN VÊ CHƯƠNG 1 Tất cả sự bất hạnh của nhân loại đèu do một thứ mà ra: không biết cách giữ được sự thư thái trong ...` | | |
| 6 | `30 lớn nào lại muốn bán những gì họ sở hữu với cái giá thấp đến ngớ ngẩn như vậy. Thế mà lạ thay, các trường hợp lạ thườ...` | | `lớn nào lại muốn bán những gì họ sở hữu với cái giá thấp đến ngớ ngẩn như vậy. Thế mà lạ thay, các trường hợp lạ thường ...` | | |
| 7 | `29 sự ngốc nghếch của người khác. Có vẻ vậy, nhưng chuyện lại không đơn giản như vậy. Mua một cổ phiếu phát hành bị quên...` | | `sự ngốc nghếch của người khác. Có vẻ vậy, nhưng chuyện lại không đơn giản như vậy. Mua một cổ phiếu phát hành bị quên lã...` | | |
| 8 | `28 chúng thường đang phát triển các quy trình hoặc sản phẩm mới được coi là đặc biệt hứa hẹn). Chúng tôi đã thể hiện qua...` | | `chúng thường đang phát triển các quy trình hoặc sản phẩm mới được coi là đặc biệt hứa hẹn).  Chúng tôi đã thể hiện quan ...` | | |
| 9 | `27 quản lý một cách chuyên nghiệp kế hoạch đắu tư của mình theo những lề lối tiêu chuần. Thứ ba là phương pháp "bình quâ...` | | `quản lý một cách chuyên nghiệp kế hoạch đắu tư của mình theo những lề lối tiêu chuần. Thứ ba là phương pháp "bình quân c...` | | |
| 10 | `26 Trong khi thảo luận về danh mục đău tư cổ phiếu thường của nhà đău tư phòng vệ, chúng tôi mới chỉ nói về các cổ phiếu...` | | `Trong khi thảo luận về danh mục đău tư cổ phiếu thường của nhà đău tư phòng vệ, chúng tôi mới chỉ nói về các cổ phiếu ph...` | | |

## 2. Test Set Grounding & Metadata Audit (5 test questions x top-3)

### Strategy A
- **q16** (gold page 33, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.773764, page=33, section=preface_buffett, author=buffett): `3 Lời nói đầu cho lần xuất bản thứ tư, của Warren E. Buffett Tôi đọc bản in lần đầu tiên của cuốn sá...`
  - Top-2 (score=0.713451, page=29, section=commentary_graham_intro, author=zweig): `ng nhà đầu tư nào loại bỏ được là nguy cơ bị sai lầm. Chỉ có cách theo sát cái mà Graham gọi là "số ...`
  - Top-3 (score=0.711125, page=22, section=introduction, author=graham): `ợc bởi một nhà đầu tư bình thường với nỗ lực và khả năng ít nhất; nhưng để nâng cao tiêu chuần dễ dà...`
- **q17** (gold page 29, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.838646, page=29, section=commentary_graham_intro, author=zweig): `7 phân tích, rồi một đối tác, và chẳng bao lâu sau đã tự điều hành công ty đầu tư của riêng mình. Vi...`
  - Top-2 (score=0.697744, page=29, section=commentary_graham_intro, author=zweig): `ược 110 đô la trên một cổ phần, sau đó ba năm). Dù phải chịu sự thua lỗ gần 70% trong cuộc Đại khủng...`
  - Top-3 (score=0.666301, page=29, section=commentary_graham_intro, author=zweig): `thành bậc thầy trong việc nghiên cứu cổ phiếu ở mức chi tiết tế vi. Vào năm 1925, trong khi nghiên c...`
- **q18** (gold page 1, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.737206, page=1, section=commentary_ch1, author=zweig): `những năm 1980. Các nghiên cứu này cho thấy nếu bạn chồng một loạt chứng khoán nhỏ vào nửa cuối thán...`
  - Top-2 (score=0.732803, page=1, section=commentary_ch1, author=zweig): `hi phí môi giới, tổng số tiền mua và bán những chứng khoán bé xíu như vậy có thể ăn tới 8% đầu tư củ...`
  - Top-3 (score=0.730235, page=1, section=commentary_ch1, author=zweig): `ung một vài tính chất - Thật là nhanh! Thật là dễ! Chẳng mất gì cả! - và tất cả đều vi phạm ít nhất ...`
- **q19** (gold page 4, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.770605, page=4, section=commentary_ch1, author=zweig): `là 20%, tức là một cổ đông điển hình sẽ nắm giữ một cổ phiếu trong vòng năm năm trước khi bán nó đi....`
  - Top-2 (score=0.689022, page=4, section=commentary_ch1, author=zweig): `m và thành công, tôi có "đúng" không? Bạn có nên bị lôi cuốn và làm theo, vì bạn thẩy tôi khoe rằng ...`
  - Top-3 (score=0.658055, page=17, section=commentary_intro, author=zweig): `vẻ quá cao đối với chứng khoán những năm 1990, thì 2003 là năm chúng ta đã đi tới thời điểm mà không...`
- **q20** (gold page 14, Hit@3=False, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.749531, page=20, section=commentary_intro, author=zweig): `giá trị của mình. Một khi đã bị mất 95% tiền của mình, bạn phải thu lời được 1.900% chỉ để trở lại v...`
  - Top-2 (score=0.737906, page=5, section=commentary_ch1, author=zweig): `nh của nó; trước khi bạn mua cổ phiếu công ty đó; bạn phải bảo vệ mình cẩn thận trước các tổn thất n...`
  - Top-3 (score=0.737903, page=20, section=commentary_intro, author=zweig): `n tới mức nào, giá của các đầu tư của bạn cũng sẽ đi xuống vào lúc này lúc khác. Mặc dù không ai có ...`

### Strategy B
- **q16** (gold page 33, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.769676, page=33, section=preface_buffett, author=buffett): `Lời nói đầu cho lần xuất bản thứ tư, của Warren E. Buffett Tôi đọc bản in lần đầu tiên của cuốn sách...`
  - Top-2 (score=0.717709, page=20, section=commentary_intro, author=zweig): `Nhưng cho dù bạn cần thận tới mức nào, giá của các đầu tư của bạn cũng sẽ đi xuống vào lúc này lúc k...`
  - Top-3 (score=0.710947, page=19, section=commentary_intro, author=zweig): `Khi đó bạn sẽ học được bài học của ông rằng nhà đẳu tư thông minh thì có phẩm chất của "tính cách" h...`
- **q17** (gold page 29, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.853471, page=29, section=commentary_graham_intro, author=zweig): `phân tích, rồi một đối tác, và chẳng bao lâu sau đã tự điều hành công ty đầu tư của riêng mình.  Việ...`
  - Top-2 (score=0.682698, page=29, section=commentary_graham_intro, author=zweig): `Dù phải chịu sự thua lỗ gần 70% trong cuộc Đại khủng hoảng 1929-1932, Graham đã vượt qua và còn phát...`
  - Top-3 (score=0.676243, page=29, section=commentary_graham_intro, author=zweig): `Graham trở thành bậc thầy trong việc nghiên cứu cổ phiếu ở mức chi tiết tế vi. Vào năm 1925, trong k...`
- **q18** (gold page 1, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.743686, page=1, section=commentary_ch1, author=zweig): `Điêu gì đã gây ra cú hích vào tháng Giêng? Đầu tiên, nhiều nhà đầu tư bán những chứng khoán tệ nhất ...`
  - Top-2 (score=0.727387, page=1, section=commentary_ch1, author=zweig): `Với ngày càng nhiều người biết đến hiệu ứng tháng Giêng, nhiều nhà kinh doanh đã mua chứng khoán vào...`
  - Top-3 (score=0.726415, page=1, section=commentary_ch1, author=zweig): `Từ CÔNG THỨC ĐẾN THÀM HỌA Nhưng kinh doanh như bị ma đuổi không phải là cách đầu cơ duy nhất. Trong ...`
- **q19** (gold page 4, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.796505, page=4, section=commentary_ch1, author=zweig): `Vào năm 1973, khi Graham sửa lại lần cuối cùng cuốn Nhà đầu tư thông minh, mức luân chuyển hằng năm ...`
  - Top-2 (score=0.678172, page=17, section=commentary_intro, author=zweig): `Vào năm 2002, các nhà đắu tư thu được 27 tỉ đô la từ các quỹ đầu tư tương hỗ chứng khoán, và một bài...`
  - Top-3 (score=0.658563, page=3, section=commentary_ch1, author=zweig): `Năm 1999, cổ phần của Puma Technology, chẳng hạn, đã sang tay trung bình cứ sau mỗi 5,7 ngày. Mặc ch...`
- **q20** (gold page 14, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.746865, page=33, section=preface_buffett, author=buffett): `Nếu làm theo những nguyên tắc ứng xử và kinh doanh mà Graham truyền bá - và nếu đặc biệt chú ý tới n...`
  - Top-2 (score=0.734362, page=14, section=chapter_1, author=graham): `Theo quan điểm thận trọng của chúng tôi, tất cả những nhà đầu tư không chuyên nghiệp nào đang kinh d...`
  - Top-3 (score=0.731546, page=29, section=commentary_graham_intro, author=zweig): `Cho dù bạn có cẩn thận tới đâu, một nguy cơ không nhà đầu tư nào loại bỏ được là nguy cơ bị sai lầm....`

### Strategy C
- **q16** (gold page 33, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.769676, page=33, section=preface_buffett, author=buffett): `Lời nói đầu cho lần xuất bản thứ tư, của Warren E. Buffett Tôi đọc bản in lần đầu tiên của cuốn sách...`
  - Top-2 (score=0.717709, page=20, section=commentary_intro, author=zweig): `Nhưng cho dù bạn cần thận tới mức nào, giá của các đầu tư của bạn cũng sẽ đi xuống vào lúc này lúc k...`
  - Top-3 (score=0.710947, page=19, section=commentary_intro, author=zweig): `Khi đó bạn sẽ học được bài học của ông rằng nhà đẳu tư thông minh thì có phẩm chất của "tính cách" h...`
- **q17** (gold page 29, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.853471, page=29, section=commentary_graham_intro, author=zweig): `phân tích, rồi một đối tác, và chẳng bao lâu sau đã tự điều hành công ty đầu tư của riêng mình.  Việ...`
  - Top-2 (score=0.682698, page=29, section=commentary_graham_intro, author=zweig): `Dù phải chịu sự thua lỗ gần 70% trong cuộc Đại khủng hoảng 1929-1932, Graham đã vượt qua và còn phát...`
  - Top-3 (score=0.676243, page=29, section=commentary_graham_intro, author=zweig): `Graham trở thành bậc thầy trong việc nghiên cứu cổ phiếu ở mức chi tiết tế vi. Vào năm 1925, trong k...`
- **q18** (gold page 1, Hit@3=True, Filter={'section': 'commentary_ch1'}): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.743686, page=1, section=commentary_ch1, author=zweig): `Điêu gì đã gây ra cú hích vào tháng Giêng? Đầu tiên, nhiều nhà đầu tư bán những chứng khoán tệ nhất ...`
  - Top-2 (score=0.727387, page=1, section=commentary_ch1, author=zweig): `Với ngày càng nhiều người biết đến hiệu ứng tháng Giêng, nhiều nhà kinh doanh đã mua chứng khoán vào...`
  - Top-3 (score=0.726415, page=1, section=commentary_ch1, author=zweig): `Từ CÔNG THỨC ĐẾN THÀM HỌA Nhưng kinh doanh như bị ma đuổi không phải là cách đầu cơ duy nhất. Trong ...`
- **q19** (gold page 4, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.796505, page=4, section=commentary_ch1, author=zweig): `Vào năm 1973, khi Graham sửa lại lần cuối cùng cuốn Nhà đầu tư thông minh, mức luân chuyển hằng năm ...`
  - Top-2 (score=0.678172, page=17, section=commentary_intro, author=zweig): `Vào năm 2002, các nhà đắu tư thu được 27 tỉ đô la từ các quỹ đầu tư tương hỗ chứng khoán, và một bài...`
  - Top-3 (score=0.658563, page=3, section=commentary_ch1, author=zweig): `Năm 1999, cổ phần của Puma Technology, chẳng hạn, đã sang tay trung bình cứ sau mỗi 5,7 ngày. Mặc ch...`
- **q20** (gold page 14, Hit@3=True, Filter=None): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: 
  - Top-1 (score=0.746865, page=33, section=preface_buffett, author=buffett): `Nếu làm theo những nguyên tắc ứng xử và kinh doanh mà Graham truyền bá - và nếu đặc biệt chú ý tới n...`
  - Top-2 (score=0.734362, page=14, section=chapter_1, author=graham): `Theo quan điểm thận trọng của chúng tôi, tất cả những nhà đầu tư không chuyên nghiệp nào đang kinh d...`
  - Top-3 (score=0.731546, page=29, section=commentary_graham_intro, author=zweig): `Cho dù bạn có cẩn thận tới đâu, một nguy cơ không nhà đầu tư nào loại bỏ được là nguy cơ bị sai lầm....`
