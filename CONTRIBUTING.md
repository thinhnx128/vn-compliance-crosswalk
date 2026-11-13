# Hướng dẫn đóng góp

Cảm ơn anh/chị quan tâm đóng góp cho dự án.

## Nguyên tắc bắt buộc

1. **Không đưa dữ liệu thật của bất kỳ cơ quan, tổ chức nào** vào issue, pull request, ví dụ
   hay dữ liệu kiểm thử: không tên hệ thống nội bộ, địa chỉ IP, sơ đồ mạng, danh mục tài sản,
   hồ sơ đánh giá, tài khoản, khóa API. Mọi ví dụ dùng tổ chức hư cấu "Công ty CP ABC".
2. **Không chép nguyên văn nội dung tiêu chuẩn có bản quyền** (ISO/IEC...). Chỉ ghi mã điều
   khoản và nhãn ngắn tự diễn đạt.
3. Mọi thay đổi phải kèm kiểm thử và qua CI (ruff + pytest).

## Quy trình

```bash
git clone https://github.com/thinhnx128/vn-compliance-crosswalk
cd vn-compliance-crosswalk
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install          # bật gitleaks + ruff trước mỗi commit
pytest && ruff check .
```

Đặt tên nhánh theo dạng `feat/...`, `fix/...`, `docs/...`, `data/...`.

## Quy ước viết commit, pull request và ghi chú phát hành

- **Commit:** dòng đầu theo dạng `loại: mô tả` (`feat`, `fix`, `docs`, `data`, `chore`, `test`), không quá 72 ký
  tự, không chấm câu ở cuối, nói thay đổi làm gì chứ không kể lại quá trình. Phần thân (nếu có) giải thích lý do.
  Viết tiếng Việt hoặc tiếng Anh đều được.
- **Pull request:** mô tả gồm bốn phần ngắn: *Vấn đề*, *Thay đổi*, *Đã kiểm tra* (lệnh đã chạy và kết quả),
  *Chưa kiểm tra hoặc giới hạn*. Thay đổi liên quan căn cứ pháp lý phải ghi điều, khoản và ngày đối chiếu.
- **CHANGELOG và ghi chú phát hành:** theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/), viết cho
  người dùng (họ nhận được gì, cần làm gì), tiếng Việt trước, tóm tắt tiếng Anh ngay bên dưới dưới tiêu đề
  `### English`. Thay đổi chưa phát hành ghi ở mục `[Unreleased]`. Lỗi của bản trước được ghi thẳng, không nói
  giảm. Bản đã phát hành là bất biến: không sửa ghi chú cũ, chỉ đính chính ở bản sau.
- **Giọng văn:** trung tính, cụ thể, không tính từ quảng cáo; nhận định ghi rõ là nhận định; không khẳng định
  công cụ bảo đảm tuân thủ.

## Contributing (English)

Never include real organisational data or verbatim copyrighted standard text. Use the fictional
"ABC Corp" for examples. Every change needs tests and must pass `ruff check .` and `pytest`.

Writing conventions:

- **Commits:** `type: summary` (`feat`, `fix`, `docs`, `data`, `chore`, `test`), at most 72 characters, no
  trailing period; say what the change does, not how you got there. The body, if any, explains why.
  Vietnamese or English.
- **Pull requests:** four short parts: *Problem*, *Change*, *Verified* (commands run and results), *Not verified
  or limitations*. Changes touching legal references must cite the article and clause and the date checked.
- **Changelog and release notes:** Keep a Changelog format, written for users, Vietnamese first with an English
  summary under `### English`. Unreleased changes go under `[Unreleased]`. Defects in earlier releases are stated
  plainly. Published releases are immutable: corrections go in the next release.
- **Tone:** neutral and specific; no promotional language; never claim the tools guarantee compliance.
