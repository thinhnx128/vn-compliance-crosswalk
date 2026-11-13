# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/), phiên bản theo [SemVer](https://semver.org/).
Dữ liệu (danh mục, đối chiếu) có số phiên bản riêng trong từng tệp YAML.

## [Unreleased]

### Thay đổi
- `toolkits/dlcn/README.md`: biên tập lại phần tiếng Việt và thêm bản tiếng Anh ở cuối trang. Nội dung pháp lý
  không đổi.
- `CONTRIBUTING.md`: thêm quy ước viết commit, pull request và ghi chú phát hành (song ngữ).
- Ghi chú phát hành có sẵn phần tiếng Anh ở chân (quy trình phát hành); mục 0.5.1 của tệp này được bổ sung
  bản tiếng Anh, khớp với ghi chú trên trang phát hành.

### Thêm mới
- Mẫu issue "Yêu cầu hỗ trợ" và "Báo lỗi, góp ý" (song ngữ); liên kết liên hệ khi mở issue.
- Email liên hệ me@nguyenxuanthinh.com trong README, cho nội dung không nên công khai.

### English
- `toolkits/dlcn/README.md`: Vietnamese text edited and an English version added below it. No change to the
  legal content.
- `CONTRIBUTING.md`: writing conventions for commits, pull requests and release notes (bilingual).
- Release notes now end with an English footer (release workflow); the 0.5.1 entry in this file gains an
  English version matching the notes on the release page.
- New bilingual issue forms, "Support request" and "Error report, feedback", with contact links.
- Contact email me@nguyenxuanthinh.com in the README, for matters that should not be public.

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
