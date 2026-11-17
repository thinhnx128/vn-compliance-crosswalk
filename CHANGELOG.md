# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/), phiên bản theo [SemVer](https://semver.org/).
Dữ liệu (danh mục, đối chiếu) có số phiên bản riêng trong từng tệp YAML.

## [Unreleased]

## [0.5.2] - 2026-11-17

### Thay đổi
- `toolkits/dlcn/README.md`: biên tập lại phần tiếng Việt và thêm bản tiếng Anh ở cuối trang. Nội dung pháp lý
  không đổi.
- `CONTRIBUTING.md`: thêm quy ước viết commit, pull request và ghi chú phát hành (song ngữ).
- Ghi chú phát hành có sẵn phần tiếng Anh ở chân (quy trình phát hành); mục 0.5.1 của tệp này được bổ sung
  bản tiếng Anh, khớp với ghi chú trên trang phát hành.

### Thêm mới
- Mẫu issue "Yêu cầu hỗ trợ" và "Báo lỗi, góp ý" (song ngữ); liên kết liên hệ khi mở issue.
- Email liên hệ me@nguyenxuanthinh.com trong README, cho nội dung không nên công khai.
- Lệnh `vncc ra-soat <thư mục>` (thử nghiệm): rà chính sách, quy trình của tổ chức (`.md`, `.txt`, `.docx`) theo 22
  yêu cầu bảo vệ dữ liệu cá nhân của Luật 91/2025/QH15 và NĐ 356/2025/NĐ-CP, xuất báo cáo khoảng trống (Markdown) và
  ma trận (CSV) kèm trích dẫn nguyên văn. Bộ chấm theo luật chạy trên máy, không cần mạng; bộ chấm AI dùng khóa API
  của người dùng, chưa được đo độ chính xác. Danh mục ở `catalogs/ra-soat/`, hướng dẫn ở `docs/ra-soat/README.md`.
  Đánh giá sơ bộ, không phải kết luận pháp lý. Đối chiếu văn bản ngày 13/11/2026.
- `vncc ra-soat`: mỗi khoảng trống trong báo cáo ghi mẫu và mục cụ thể trong bộ DP-01..07 có thể dùng để lấp
  (`catalogs/ra-soat/vn-pdp-2025.mau.json`).
- Mẫu DP-01: thêm mục 9 (dữ liệu trẻ em; ứng viên và người lao động; camera, ghi âm, sinh trắc học, vị trí, cookie;
  trí tuệ nhân tạo và môi trường kiểm thử; mã hóa trên điện toán đám mây, sao lưu; danh sách bên xử lý) và nội dung
  báo cáo lãnh đạo ở mục 12; các mục sau đánh số lại. Mẫu DP-05: thêm mục 8 về diễn tập. Phần ghi "thực tiễn tốt"
  không phải nghĩa vụ luật định.
- **Gói Word, Excel trong `toolkits/dlcn/phat-hanh/` đã dựng lại** theo mẫu hiện tại (12 tệp, mã băm mới ghi ở
  `SHA256SUMS` và trong `toolkits/dlcn/README.md`). Gói trong bản phát hành 0.5.1 thiếu các mục bổ sung nói trên;
  gói trong bản này có. Tệp đính kèm của bản phát hành 0.5.1 không đổi, bản này là bản mới.
- Mẫu SP-01 và SP-02 trong gói nay ghi email liên hệ `me@nguyenxuanthinh.com` bên cạnh trang Issues; gói 0.5.1
  chỉ ghi trang Issues.

### Thêm mới (so với 0.5.1, ngoài các mục ở trên)
- Dẫn chiếu **Nghị định 330/2026/NĐ-CP ngày 19/8/2026** (xử phạt vi phạm hành chính trong lĩnh vực an ninh mạng và
  bảo vệ dữ liệu cá nhân, hiệu lực từ 19/8/2026) trong `README.md`, `toolkits/dlcn/README.md` và các mẫu DP-00,
  SP-02. **Chỉ dẫn chiếu:** bộ công cụ không đối chiếu khoảng trống với hành vi vi phạm và chế tài trong nghị định
  đó, và không kết luận gì về khả năng bị xử phạt. Mẫu DP-00 tách tiêu chí mức rủi ro khỏi khả năng bị xử phạt.
  Rà soát văn bản mới ngày 16/11/2026 không tìm thấy văn bản nào sửa đổi Luật 91/2025 hay NĐ 356/2025, trong phạm
  vi tra cứu của tác giả.
- `toolkits/dlcn/phat-hanh/NGUON.txt` và `tests/test_goi_phat_hanh.py`: chốt chặn để gói zip không lệch mẫu nguồn.
  Kiểm tra mã băm gói, danh sách 12 tệp, mẫu không đổi kể từ lần dựng, cấu trúc OOXML của từng tệp, và câu chữ bên
  trong tệp Word phải khớp mẫu hiện tại.

### Sửa lỗi
- `vncc ra-soat`: bộ chấm theo luật không còn dừng ở một tiêu đề ngắn khớp mẫu (trích dẫn quá ngắn bị loại) mà xét
  tiếp các đoạn sau, nên không bỏ sót bằng chứng nằm ngay dưới tiêu đề.

### English
- `toolkits/dlcn/README.md`: Vietnamese text edited and an English version added below it. No change to the
  legal content.
- `CONTRIBUTING.md`: writing conventions for commits, pull requests and release notes (bilingual).
- Release notes now end with an English footer (release workflow); the 0.5.1 entry in this file gains an
  English version matching the notes on the release page.
- New bilingual issue forms, "Support request" and "Error report, feedback", with contact links.
- Contact email me@nguyenxuanthinh.com in the README, for matters that should not be public.
- New `vncc ra-soat <folder>` command (experimental): checks an organisation's policies and procedures (`.md`,
  `.txt`, `.docx`) against 22 personal data protection requirements of Law No. 91/2025/QH15 and Decree No.
  356/2025/ND-CP and writes a gap report (Markdown) and a matrix (CSV) with verbatim quotes. The rule judge runs
  offline; the AI judge uses the user's own API key and its accuracy has not been measured. Catalog in
  `catalogs/ra-soat/`, guide in `docs/ra-soat/README.md`. Preliminary assessment, not legal advice. Legal texts
  checked on 13 November 2026.
- `vncc ra-soat`: each gap in the report names the DP-01..07 template section that can fill it. Template DP-01
  gains section 9 (children; job applicants and employees; cameras, recordings, biometric and location data,
  cookies; AI and test environments; cloud encryption and backups; list of processors) and management reporting in
  section 12; DP-05 gains section 8 on drills. Fix: the rule judge no longer stops at a short matching heading whose
  quote is too short.
- **The Word/Excel package under `toolkits/dlcn/phat-hanh/` has been rebuilt** from the current templates (12 files,
  new checksum in `SHA256SUMS` and in `toolkits/dlcn/README.md`). The package attached to release 0.5.1 lacks the
  additions above; this one has them. SP-01 and SP-02 now carry the contact email alongside the Issues page.
- Reference to **Decree No. 330/2026/ND-CP of 19 August 2026** on administrative penalties in the fields of
  cybersecurity and personal data protection, in force from 19 August 2026, in `README.md`,
  `toolkits/dlcn/README.md` and templates DP-00 and SP-02. **Reference only:** the toolkit does not map its findings
  to the violations or sanctions in that Decree and draws no conclusion about exposure to penalties. A review of new
  instruments on 16 November 2026 found nothing amending Law 91/2025 or Decree 356/2025, within the sources checked.
- `toolkits/dlcn/phat-hanh/NGUON.txt` and `tests/test_goi_phat_hanh.py`: guards against the zip drifting from the
  templates — package checksum, the 12 expected files, templates unchanged since the build, each file's OOXML
  structure, and the text inside each Word file matching the current template.

## [0.5.1] - 2026-11

### Sửa
- Gói Word, Excel của bộ công cụ bảo vệ dữ liệu cá nhân (2 sổ Excel, 10 tài liệu Word) chưa có trong bản
  phát hành 0.5.0 dù hướng dẫn nói là có. Gói nay nằm trong kho tại `toolkits/dlcn/phat-hanh/` và được quy
  trình phát hành đính kèm khi tạo bản phát hành. Gói không đổi: cùng mã băm SHA-256 với gói đã chuẩn bị cho
  0.5.0.
- `toolkits/dlcn/README.md` trỏ thẳng tới gói zip và ghi mã băm SHA-256; quy trình phát hành kiểm tra mã băm
  (`SHA256SUMS`) và dừng nếu CHANGELOG thiếu mục của phiên bản.

### English
- The Word and Excel package of the personal data protection toolkit (2 Excel workbooks, 10 Word documents)
  was missing from release 0.5.0, although the guide said it was included. The package is now stored in the
  repository under `toolkits/dlcn/phat-hanh/` and is attached by the release workflow when a release is
  created. The package itself is unchanged: it has the same SHA-256 checksum as the package prepared for 0.5.0.
- `toolkits/dlcn/README.md` now links directly to the zip and states its SHA-256 checksum; the release
  workflow verifies the checksum (`SHA256SUMS`) and stops if the CHANGELOG has no entry for the version.

## [0.5.0] - 2026-11

### Thêm mới
- Bộ công cụ bảo vệ dữ liệu cá nhân cho doanh nghiệp vừa và nhỏ (`toolkits/dlcn/`): 22 câu tự kiểm tra có căn
  cứ điều, khoản theo Luật 91/2025/QH15 và NĐ 356/2025/NĐ-CP; nguồn Markdown của mẫu báo cáo chẩn đoán, chính
  sách, thông báo xử lý, đánh giá tác động, quy trình giải quyết yêu cầu của chủ thể, xử lý vi phạm, thỏa thuận
  với bên xử lý, mẫu đồng ý; hướng dẫn sử dụng. Đối chiếu văn bản ngày 13/11/2026.
- Trang "Kiểm tra nhanh" 10 câu (`docs/kiem-tra-nhanh/`), chạy trên trình duyệt.
- `LICENSE-DATA` áp dụng thêm cho `toolkits/` và các tệp mẫu biểu phát hành kèm.

## [0.4.0] - 2026-11

### Thêm mới
- Tham số định lượng trên yêu cầu (`params`: thời hạn, mốc ngày, chu kỳ, nơi nhận, phạm vi, trạng thái
  đối chiếu) và từ điển chủ đề `parameters/topics.yaml`.
- Lệnh `vncc conflicts` và trang Excel "Thời hạn & chồng chéo": phát hiện thời hạn khác nhau, nơi nhận
  khác nhau giữa các văn bản, gợi ý SLA nội bộ theo mức chặt nhất.
- Danh mục một phần `luat91-2025` (Điều 23) và `nd356-2025` (Điều 5, 8, 18, 19, 28, 29): chỉ các nghĩa
  vụ có tham số định lượng đã đối chiếu.
- Lớp bằng chứng `evidence/` cho đủ 93 biện pháp ISO/IEC 27001 và 64 yêu cầu NĐ 331; hiện trong SoA,
  báo cáo khoảng cách, gói Excel, `vncc show`; lệnh `vncc evidence` xuất danh mục kiểm tra theo cấp độ.
- JSON Schema cho `evidence` và `topics`.

## [0.3.1] - 2026-11

### Thêm mới
- Watermark tác giả trên trang xác định cấp độ (lớp chữ chìm, không chặn thao tác, hiện cả khi in và
  chụp màn hình), dòng ghi tác giả ở chân trang và thẻ meta tác giả.
- Gói Excel ghi tác giả trong thuộc tính tệp, trang Hướng dẫn và chân trang khi in.

## [0.3.0] - 2026-11

### Thêm mới
- Công cụ xác định cấp độ HTTT theo NĐ 331/2026 (Điều 9, 11–15): bộ tiêu chí dạng dữ liệu
  (`src/vncc/nd331_cap_do.json`) dùng chung cho lệnh `vncc level` (hỏi–đáp hoặc đọc tệp) và trang web
  `docs/cap-do/` (sinh bằng `vncc site`); kết quả của trang web và CLI được kiểm thử trùng khớp.
- Lệnh `vncc export-xlsx`: gói Excel tự đánh giá có ô chọn cấp độ, cột áp dụng và bảng tổng hợp dùng
  công thức sống; kèm danh mục, bảng đối chiếu, độ phủ, tiêu chí cấp độ.
- Quy trình phát hành tự động: gắn thẻ `vX.Y.Z` là tạo Release kèm gói Excel.
- Trang chủ GitHub Pages (`docs/index.md`).

## [0.2.0] - 2026-11

### Thêm mới
- Danh mục `nd331-2026`: 64 yêu cầu nghĩa vụ của Nghị định 331/2026/NĐ-CP, 9 nhóm, gắn thẻ cấp độ,
  chủ thể thực hiện và thẻ `can-doi-chieu` cho nội dung chưa đối chiếu được toàn văn (Điều 33–37).
- Bảng đối chiếu `iso27001-2022__nd331-2026`: 68 dòng, bản nháp.
- Lọc theo cấp độ HTTT: trường `level` trong hồ sơ đánh giá, tùy chọn `--level` cho `init`, `soa`, `gap`.
- Lệnh `vncc coverage`: độ phủ của bảng đối chiếu ở cả hai phía.
- Tài liệu tóm tắt tiêu chí xác định cấp độ (`docs/nd331-cap-do.md`) và ví dụ hồ sơ cấp độ 2.

### Sửa
- CI: cấp quyền đọc pull request cho gitleaks; nâng actions/checkout, actions/setup-python lên v7.

## [0.1.0] - 2026-11

### Thêm mới
- Mô hình dữ liệu catalog / mapping / assessment, kèm JSON Schema.
- Danh mục ISO/IEC 27001:2022 Phụ lục A: 93 biện pháp, mã và nhãn ngắn tự diễn đạt.
- Khung danh mục NĐ 331/2026/NĐ-CP và Luật 91/2025/QH15 (trạng thái skeleton).
- CLI `vncc`: list, show, validate, init, soa, gap, schema.
- SoA Excel có trang tổng hợp dùng công thức; báo cáo khoảng cách Markdown, nêu rõ quy tắc tính.
- Nạp chồng dữ liệu riêng của tổ chức bằng `--data-dir`.
- Ví dụ hư cấu "Công ty CP ABC".
