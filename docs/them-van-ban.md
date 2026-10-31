# Hướng dẫn thêm hoặc hoàn thiện một văn bản

## 1. Chuẩn bị nguồn

- Lấy văn bản gốc từ nguồn chính thức (Công báo, Cơ sở dữ liệu quốc gia về văn bản pháp luật,
  cổng thông tin của cơ quan ban hành).
- Ghi lại: số hiệu, ngày ban hành, ngày hiệu lực, đường dẫn nguồn. Thiếu thông tin nào thì để
  trống, **không phỏng đoán**.

## 2. Viết danh mục (`catalogs/<ma>.yaml`)

```yaml
kind: catalog
id: nd331-2026
title: ...
version: "2026"
publisher: Chính phủ nước CHXHCN Việt Nam
document_number: 331/2026/NĐ-CP
issued_on: 2026-MM-DD        # chỉ điền khi đã xác nhận
effective_date: 2026-MM-DD   # chỉ điền khi đã xác nhận
source_url: https://...
status: draft
groups:
  - id: C2
    title: Chương II - ...
    controls:
      - id: D12.K2.a
        title: Tóm tắt ngắn yêu cầu, tự viết
        tags: [cap-do-3, cap-do-4, cap-do-5]
```

Quy ước mã: `D<điều>.K<khoản>.<điểm>`. Mỗi control là **một yêu cầu kiểm chứng được**. Điều khoản
chứa nhiều nghĩa vụ thì tách thành nhiều control.

## 3. Viết bảng đối chiếu (`mappings/<nguon>__<dich>.yaml`)

Mỗi dòng bắt buộc có `relationship`, `rationale` (tối thiểu một câu giải thích) và `confidence`.
Dòng do người thứ hai rà soát thì điền `reviewed_by`, `reviewed_on`.

| Mức tin cậy | Khi nào dùng |
|---|---|
| `high` | Văn bản quy định rõ, hai người rà soát cùng kết luận |
| `medium` | Cần diễn giải, có thể có cách hiểu khác |
| `low` | Suy luận, cần ý kiến chuyên gia pháp lý hoặc hướng dẫn của cơ quan quản lý |

## 4. Kiểm tra

```bash
vncc validate
pytest
```

## 5. Chuyển trạng thái

`skeleton` → `draft` khi đã có nội dung; `draft` → `reviewed` khi toàn bộ dòng đã được người thứ
hai rà soát. Mỗi lần văn bản gốc được sửa đổi, tăng `version` và ghi vào CHANGELOG.
