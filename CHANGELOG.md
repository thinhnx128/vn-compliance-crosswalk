# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/), phiên bản theo [SemVer](https://semver.org/).
Dữ liệu (danh mục, đối chiếu) có số phiên bản riêng trong từng tệp YAML.

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
