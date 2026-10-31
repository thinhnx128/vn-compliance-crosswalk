# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/), phiên bản theo [SemVer](https://semver.org/).
Dữ liệu (danh mục, đối chiếu) có số phiên bản riêng trong từng tệp YAML.

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
