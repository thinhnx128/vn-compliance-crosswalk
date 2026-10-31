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

Đặt tên nhánh theo dạng `feat/...`, `fix/...`, `docs/...`, `data/...`. Commit message ngắn gọn,
viết tiếng Việt hoặc tiếng Anh đều được.

## Contributing (English)

Never include real organisational data or verbatim copyrighted standard text. Use the fictional
"ABC Corp" for examples. Every change needs tests and must pass `ruff check .` and `pytest`.
