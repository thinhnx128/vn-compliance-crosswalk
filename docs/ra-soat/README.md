# Rà soát khoảng trống bảo vệ dữ liệu cá nhân (thử nghiệm)

*[English below](#english)*

> **Đánh giá sơ bộ, không phải kết luận pháp lý hay kết luận đánh giá. Mẫu tham khảo, không phải tư vấn pháp lý.**
> **Ngày đối chiếu văn bản pháp luật: 13/11/2026.** Nguồn: Công báo số 971+972 ngày 24/7/2025 (Luật 91/2025/QH15,
> hiệu lực 01/01/2026) và Công báo số 18 ngày 18/01/2026 (Nghị định 356/2025/NĐ-CP). Nhãn của công cụ nói về
> **bằng chứng trong văn bản**, không phải kết luận tuân thủ pháp luật.

## Công cụ làm gì

Lệnh `vncc ra-soat` đọc một thư mục chính sách, quy trình của tổ chức (`.md`, `.txt`, `.docx`) và đối chiếu với
22 yêu cầu bảo vệ dữ liệu cá nhân theo Luật 91/2025/QH15 và NĐ 356/2025/NĐ-CP (cùng 22 yêu cầu của bộ tự kiểm tra
trong [`toolkits/dlcn`](../../toolkits/dlcn/README.md)). Kết quả là hai tệp:

- `bao-cao.md`: tổng hợp theo trạng thái, danh sách khoảng trống xếp theo ưu tiên, chi tiết từng yêu cầu kèm
  **trích dẫn nguyên văn** và vị trí (`tên-tệp#số-đoạn`) của đoạn làm bằng chứng;
- `ma-tran.csv`: ma trận yêu cầu, yếu tố, có bằng chứng hay không, vị trí, trích dẫn (mở được bằng Excel).

Công cụ chỉ thấy nội dung văn bản được đưa vào. Văn bản có ghi không có nghĩa là tổ chức đã thực hiện; việc thực hiện
trên thực tế cần kiểm tra riêng.

## Cài đặt và chạy

```bash
pip install "git+https://github.com/thinhnx128/vn-compliance-crosswalk"

vncc ra-soat thu-muc-chinh-sach/ --ra ket-qua
vncc ra-soat thu-muc-chinh-sach/ --khong-ap-dung "VN-PDP-10=DN nhỏ chọn không thực hiện (Điều 38)"
vncc ra-soat thu-muc-chinh-sach/ --bo-cham ai       # thử nghiệm, cần ANTHROPIC_API_KEY của chính bạn
vncc ra-soat thu-muc-chinh-sach/ --bo-cham ca-hai   # AI, đối chiếu với bộ luật
```

Chạy từ mã nguồn: `python -m vncc.ra_soat danh-gia <thư mục> [--bo-cham luat|ai|ca-hai] [--ra <thư mục>]`.

Trên Windows, đặt `PYTHONUTF8=1` trước khi chạy để tiếng Việt hiển thị và ghi tệp đúng (PowerShell bên dưới; với
CMD dùng `set PYTHONUTF8=1`):

```powershell
$env:PYTHONUTF8 = "1"
vncc ra-soat .\chinh-sach --ra .\ket-qua
```

| Tham số | Ý nghĩa |
|---|---|
| `--bo-cham luat` | Mặc định. Bộ chấm theo luật (mẫu từ khóa), chạy trên máy, không cần mạng |
| `--bo-cham ai` | Bộ chấm AI (thử nghiệm). Văn bản được gửi tới Anthropic bằng khóa API của chính bạn |
| `--bo-cham ca-hai` | Bộ chấm AI, có bộ luật chấm song song để xác nhận chéo |
| `--ra` | Thư mục ghi kết quả (mặc định `ket-qua`) |
| `--khong-ap-dung MA=LY_DO` | Khai báo yêu cầu không áp dụng cho tổ chức, kèm lý do. Lặp được |

Biến môi trường của bộ chấm AI: `ANTHROPIC_API_KEY` (bắt buộc), `RA_SOAT_MODEL` (mặc định `claude-opus-5-5`),
`RA_SOAT_EFFORT` (mặc định `low`), `RA_SOAT_MAX_CALLS` (trần số lượt gọi, mặc định 300).

Mã thoát: `0` thành công; `2` lỗi đầu vào (không thấy thư mục, không đọc được đoạn nào, mã yêu cầu sai);
`3` bộ chấm không chạy được, khi đó **không ghi báo cáo**.

**Trước khi dùng bộ chấm AI với văn bản thật:** văn bản sẽ rời khỏi máy của bạn tới nhà cung cấp AI. Chỉ làm vậy
khi tổ chức đã cho phép và điều khoản dịch vụ của nhà cung cấp phù hợp với quy định nội bộ.

## Cách chấm

1. **Tách văn bản thành đoạn.** Mỗi dòng có nội dung (đoạn văn, mục danh sách, dòng bảng, tiêu đề) là một đoạn,
   có tên tệp, số thứ tự và tiêu đề gần nhất. Văn bản được chuẩn hóa Unicode (NFC) và bỏ ký tự NUL; trích dẫn được
   so khớp trên văn bản đã chuẩn hóa này.
2. **Tách yêu cầu thành yếu tố.** Mỗi yêu cầu có 2 đến 4 yếu tố kiểm được (ví dụ VN-PDP-16: phân quyền, xác thực đa
   yếu tố, nhật ký truy cập). Danh mục ở [`catalogs/ra-soat/`](../../catalogs/ra-soat/).
3. **Chấm từng yếu tố.** Bộ chấm nhận các đoạn liên quan và trả lời có bằng chứng hay không, kèm trích dẫn.
4. **Gán nhãn yêu cầu theo quy tắc**, không do bộ chấm quyết định:

| Nhãn | Quy tắc |
|---|---|
| Đủ bằng chứng trong văn bản | Mọi yếu tố có bằng chứng, và mọi bằng chứng đã được bộ luật xác nhận |
| Cần rà soát thủ công | Có ít nhất một kết luận của AI (có hoặc không có bằng chứng) mà bộ luật chưa xác nhận; báo cáo ghi rõ từng yếu tố. Chạy `--bo-cham ai` một mình thì hầu hết yêu cầu sẽ ở nhãn này |
| Có bằng chứng một phần | Có bằng chứng cho một số yếu tố |
| Chưa tìm thấy bằng chứng | Văn bản có nói tới chủ đề nhưng công cụ không tìm thấy bằng chứng cho yếu tố nào (không chứng minh văn bản thiếu nội dung đó) |
| Văn bản không đề cập | Công cụ không thấy văn bản nói tới chủ đề |
| Không áp dụng (người dùng khai báo) | Người dùng khai báo bằng `--khong-ap-dung`; công cụ không thẩm định việc được miễn |

Ưu tiên khoảng trống tạm tính theo loại yêu cầu (luật định trước thực tiễn tốt) và số yếu tố còn thiếu.

## Nguyên tắc an toàn

- Trích dẫn phải **khớp nguyên văn** (sau khi gộp khoảng trắng) một đoạn nằm trong danh sách đoạn ứng viên của chính
  yếu tố đang chấm, dài tối thiểu 20 ký tự và 4 từ. Trích dẫn bịa, sai vị trí hoặc quá chung chung bị loại.
- **Mọi kết quả của bộ chấm AI là gợi ý.** Kết luận của AI chỉ được tính khi bộ luật chấm song song cho cùng kết luận
  (với "có" thì ở **cùng đoạn**). Ngược lại, yêu cầu nhận nhãn "Cần rà soát thủ công"; báo cáo ghi rõ từng yếu tố chưa xác
  nhận.
- Bộ chấm chỉ được hỏi trên các **đoạn ứng viên** do bộ lọc từ khóa chọn. Ở chế độ `ca-hai`, nếu bộ lọc không chọn
  được đoạn nào thì cả hai bộ chấm đều không xem nội dung, và kết luận âm tính khi đó chỉ ngang chế độ bộ luật; nó
  không có nghĩa là hai bộ chấm đã cùng xem xét văn bản. Ở chế độ chỉ dùng AI, trường hợp này là "Cần rà soát thủ công".
- Thiếu khóa, lỗi gọi API, phản hồi sai cấu trúc hoặc bị cắt, model từ chối trả lời, chạm trần số lượt gọi: lần rà
  **dừng** (mã thoát 3), không ghi báo cáo, không biến lỗi thành "không có bằng chứng".
- Văn bản đầu vào được đặt trong ranh giới dữ liệu `<tai_lieu>`; văn bản không tự đóng, mở được ranh giới này. Câu
  chèn lệnh trong văn bản không đổi được kết quả của bộ luật (có kiểm thử). Với bộ chấm AI thật, việc chống chèn lệnh
  **chưa được thử**.
- Tệp CSV chặn chèn công thức: ô bắt đầu bằng `=`, `+`, `-`, `@` (kể cả sau khoảng trắng, ký tự điều khiển ở đầu)
  được thêm dấu `'`.
- Lớp gọi API: phiên bản `2026-10-21`, không gửi `temperature`, `output_config.effort` mặc định `low`, có
  `fallbacks: "default"` với header beta `server-side-fallback-2026-07-01`.

## Kết quả đo bộ chấm theo luật

Đo ngày 15/11/2026 trên dữ liệu trong kho (`python -m vncc.ra_soat.danh_gia tests/data/ra_soat/cong-ty-abc
tests/data/ra_soat/cong-ty-abc.nhan.json`):

| Bộ văn bản | Kết quả |
|---|---|
| Bộ mẫu DP-01..07 trong `toolkits/dlcn/mau/` | 14 đủ bằng chứng, 7 có bằng chứng một phần, 1 chưa tìm thấy bằng chứng |
| Bộ văn bản hư cấu "Công ty CP ABC" (`tests/data/ra_soat/`, 3 tệp, 65 yếu tố, viết bằng lời khác bộ mẫu, có bẫy) | Đúng 46/65 yếu tố (0,708); **0 dương tính giả**; 19 âm tính giả; độ phủ 0,296; nhãn yêu cầu khớp 12/22 |

Bộ mẫu DP-01..07 là bộ đã dùng để viết mẫu chấm, nên kết quả trên bộ mẫu không nói lên độ chính xác. Bộ văn bản hư
cấu không dùng để chỉnh mẫu chấm. Nhãn của bộ này do một người gán, chưa được nhiều người đối chiếu.

Nhận định: bộ luật đáng tin khi nói "có" nhưng bỏ sót phần lớn bằng chứng viết bằng lời khác mẫu. Vai trò của nó là
lưới an toàn và bộ chấm thứ hai. Nhãn "Chưa tìm thấy bằng chứng" hay "Văn bản không đề cập" của bộ luật không chứng
minh văn bản thiếu nội dung đó.

## Giới hạn

- **Bộ chấm AI là thử nghiệm: chưa chạy với API thật, chưa đo độ chính xác.**
- `.docx`: chỉ đọc thân văn bản, bỏ qua đầu trang, chân trang, chú thích. Chưa hỗ trợ PDF.
- Ưu tiên khoảng trống chưa tính mức phạt (NĐ 330/2026).
- Bộ văn bản đo nhỏ (65 yếu tố); nhãn chưa phải bộ nhãn chuẩn.
- Mẫu chấm hiện chỉ nhận tiếng Việt.

---

## English

**Personal data protection gap review (experimental).** *Preliminary assessment, not a legal opinion or an audit
conclusion. Reference template, not legal advice. Legal texts checked on 13 November 2026 against the Official
Gazette (No. 971+972 of 24 July 2025 for Law No. 91/2025/QH15; No. 18 of 18 January 2026 for Decree No.
356/2025/ND-CP). Labels describe evidence in the documents, not legal compliance.*

`vncc ra-soat` reads a folder of an organisation's policies and procedures (`.md`, `.txt`, `.docx`) and checks it
against the 22 personal data protection requirements used by the [`toolkits/dlcn`](../../toolkits/dlcn/README.md)
self-assessment. It writes `bao-cao.md` (summary, prioritised gaps, per-requirement detail with **verbatim quotes** and
their location) and `ma-tran.csv` (requirement/element matrix). The tool only sees the text it is given; written policy
is not proof of practice.

```bash
pip install "git+https://github.com/thinhnx128/vn-compliance-crosswalk"
vncc ra-soat policies/ --ra results
vncc ra-soat policies/ --khong-ap-dung "VN-PDP-10=reason"   # declare a requirement not applicable
vncc ra-soat policies/ --bo-cham ai       # experimental, uses your own ANTHROPIC_API_KEY
vncc ra-soat policies/ --bo-cham ca-hai   # AI judge cross-checked by the rule judge
python -m vncc.ra_soat danh-gia policies/  # same, from source
```

On Windows set `PYTHONUTF8=1` first (PowerShell: `$env:PYTHONUTF8 = "1"`; CMD: `set PYTHONUTF8=1`). Exit codes: `0` success, `2` input error, `3` judge failure (no report is written).
The AI judge sends your documents to Anthropic; only do this with your organisation's permission.

**How scoring works.** Documents are split into segments (one per non-empty line), normalised to Unicode NFC with NUL
characters removed; quotes are matched against this normalised text. Each requirement is split into 2–4
checkable elements (`catalogs/ra-soat/`). A judge decides per element whether evidence exists and quotes it. Requirement
labels follow fixed rules: Sufficient evidence in the documents (all elements evidenced and confirmed by the rule
judge), Needs manual review (any
AI conclusion, positive or negative, not confirmed by the rule judge; with `--bo-cham ai` alone most requirements land
here), Partial evidence, No evidence found (topic mentioned, no element evidenced;
this does not prove the content is absent), Not addressed in the documents, Not applicable (declared by the user, not
verified).

**Safeguards.** Quotes must match, verbatim, a segment from that element's own candidate list, with at least 20
characters and 4 words. Every AI result is a suggestion: an AI conclusion counts only when the rule judge reaches the
same conclusion (for "yes", on the same segment); otherwise the requirement is "Needs manual review". Missing key, API errors, malformed or truncated responses, refusals or
reaching the call limit stop the run with exit code 3. Judges only see the **candidate segments** picked by a keyword
filter; in `ca-hai` mode, when the filter picks nothing, neither judge reads the text and the negative result is only as
strong as the rule-only mode (in AI-only mode it becomes "Needs manual review"). Input text is fenced inside
`<tai_lieu>` tags it cannot close; injected instructions do not change rule-judge results (tested), but prompt-injection
resistance of the real AI judge is untested. CSV cells are protected against formula injection.

**Measured results (rule judge, 15 Nov 2026).** Templates DP-01..07 in `toolkits/dlcn/mau/`: 14 sufficient evidence, 7 partial
evidence, 1 no evidence found (these templates were used to write the patterns, so this is not an accuracy figure). Independent fictional set
"Công ty CP ABC" (`tests/data/ra_soat/`, 65 elements, with traps): 46/65 correct (0.708), **0 false positives**, 19
false negatives, recall 0.296, requirement labels matching 12/22. Labels were assigned by one person. The rule judge is
reliable when it says "yes" but misses most evidence phrased differently.

**Limitations.** The AI judge is experimental: never run against the real API and its accuracy is unmeasured. `.docx`
support reads the document body only; PDF is not supported. Gap priority does not yet consider penalty levels (Decree
330/2026). Patterns only recognise Vietnamese text.
