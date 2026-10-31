# vn-compliance-crosswalk

[![CI](https://github.com/thinhnx128/vn-compliance-crosswalk/actions/workflows/ci.yml/badge.svg)](https://github.com/thinhnx128/vn-compliance-crosswalk/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)

**Đối chiếu ISO/IEC 27001:2022 với quy định Việt Nam dưới dạng dữ liệu máy đọc được ("Compliance-as-Code"),
và tự sinh Tuyên bố áp dụng (SoA), báo cáo khoảng cách.**

*[English below](#english)*

## Vì sao có dự án này

Doanh nghiệp Việt Nam vận hành ISMS theo ISO/IEC 27001 đồng thời phải tuân thủ quy định trong nước
như Nghị định 331/2026/NĐ-CP về bảo vệ an ninh mạng đối với hệ thống thông tin và Luật Bảo vệ dữ
liệu cá nhân 91/2025/QH15. Việc đối chiếu hiện nay thường nằm rải rác trong các tệp Excel, khó
kiểm chứng, khó cập nhật khi văn bản thay đổi và không tái sử dụng được giữa các tổ chức.

Dự án đưa mỗi yêu cầu thành một bản ghi dữ liệu, mỗi dòng đối chiếu kèm **loại quan hệ, lý do và
mức tin cậy**, nên ai cũng có thể phản biện qua pull request.

## Trạng thái dữ liệu

| Danh mục | Mã | Trạng thái |
|---|---|---|
| ISO/IEC 27001:2022 Phụ lục A (93 biện pháp) | `iso27001-2022` | Đầy đủ mã và nhãn |
| Nghị định 331/2026/NĐ-CP ngày 19/8/2026 (64 yêu cầu, 9 nhóm, gắn thẻ cấp độ) | `nd331-2026` | Bản nháp, cần rà soát chéo |
| Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 | `luat91-2025` | Khung, dự kiến v0.3 |

| Bảng đối chiếu | Dòng | Trạng thái |
|---|---:|---|
| `iso27001-2022__nd331-2026` | 68 | Bản nháp, chưa rà soát chéo |

Danh mục `skeleton` **không được dùng để đánh giá tuân thủ**. Trong danh mục NĐ 331, các mục gắn
thẻ `can-doi-chieu` (Điều 33–37) chưa đối chiếu được toàn văn, phải kiểm tra văn bản gốc.

### Phát hiện chính từ bảng đối chiếu NĐ 331

Chạy `vncc coverage iso27001-2022__nd331-2026` cho thấy chỉ khoảng **6/10 yêu cầu của NĐ 331 có biện
pháp tương ứng trong Phụ lục A** của ISO/IEC 27001. Phần còn lại chủ yếu là nghĩa vụ hành chính, pháp
lý đặc thù của Việt Nam mà một ISMS đạt chứng nhận vẫn chưa có sẵn:

- xác định HTTT, nguyên tắc một chủ quản, cấm chia tách hình thức để hạ cấp độ;
- lập hồ sơ đề xuất cấp độ, thẩm định độc lập, phê duyệt theo thẩm quyền;
- ban hành Quy chế bảo đảm an ninh mạng **trước** khi phê duyệt cấp độ;
- báo cáo sự cố 24 giờ, 72 giờ cho cơ quan chuyên trách và báo cáo định kỳ hằng năm;
- các mốc chuyển tiếp: 6 tháng phê duyệt cấp độ, 12 tháng đáp ứng đầy đủ điều kiện.

Một phần nguyên nhân là danh mục ISO ở đây mới gồm Phụ lục A; các điều khoản chính (ví dụ 6.1 đánh
giá rủi ro, 9.2 đánh giá nội bộ) sẽ được bổ sung ở phiên bản sau. Tiêu chí xác định cấp độ tóm tắt
tại [docs/nd331-cap-do.md](docs/nd331-cap-do.md).

## Cài đặt

```bash
pip install "git+https://github.com/thinhnx128/vn-compliance-crosswalk"
```

## Sử dụng nhanh

```bash
# Xem dữ liệu đang có
vncc list

# Tạo hồ sơ đánh giá trống (93 biện pháp) rồi điền trạng thái
vncc init iso27001-2022 -o hoso.yaml --organization "Công ty CP ABC"

# Kiểm tra hồ sơ, sinh SoA Excel và báo cáo khoảng cách
vncc validate hoso.yaml
vncc soa hoso.yaml -o soa.xlsx
vncc gap hoso.yaml -o gap.md

# Tra cứu một biện pháp và các yêu cầu liên quan
vncc show iso27001-2022 5.24
vncc show nd331-2026 D31.K2.d

# Tự đánh giá tuân thủ NĐ 331 cho một HTTT cấp độ 2 (chỉ sinh yêu cầu áp dụng cho cấp độ 2)
vncc init nd331-2026 --level 2 -o hoso-nd331.yaml
vncc gap hoso-nd331.yaml -o gap-nd331.md

# Độ phủ bảng đối chiếu: yêu cầu NĐ chưa có biện pháp ISO tương ứng
vncc coverage iso27001-2022__nd331-2026
```

Chạy thử với ví dụ hư cấu "Công ty CP ABC" (có danh mục chính sách nội bộ riêng):

```bash
vncc soa examples/abc-corp/assessment.yaml -d examples/abc-corp -o soa.xlsx
vncc gap examples/abc-corp/assessment.yaml -d examples/abc-corp
vncc gap examples/abc-corp/assessment-nd331-cap-do-2.yaml
```

### SoA sinh ra gồm

- **Thông tin:** tổ chức, phạm vi, ngày chốt số liệu, phiên bản danh mục, quy tắc tính.
- **SoA:** mã, nhóm, biện pháp, áp dụng, lý do, trạng thái, bằng chứng, người phụ trách, hạn,
  yêu cầu liên quan theo bảng đối chiếu; có lọc, cố định tiêu đề và danh sách chọn.
- **Tổng hợp:** thống kê theo nhóm bằng **công thức Excel sống**, sửa SoA là số liệu tự cập nhật.

**Quy tắc tính tỷ lệ tuân thủ:** (Đã triển khai + 0,5 × Triển khai một phần) / Số biện pháp áp
dụng. Biện pháp không áp dụng bị loại khỏi mẫu số; biện pháp chưa đánh giá tính 0.

## Dữ liệu riêng của tổ chức

Tham số `-d/--data-dir` nạp chồng thư mục dữ liệu riêng (danh mục chính sách nội bộ, bảng đối
chiếu nội bộ) lên dữ liệu công khai **mà không cần đưa lên GitHub**. Cấu trúc thư mục:

```
du-lieu-noi-bo/
├── catalogs/   # danh mục chính sách, quy định nội bộ
└── mappings/   # đối chiếu ISO <-> chính sách nội bộ
```

Hồ sơ đánh giá thật, danh mục tài sản, bằng chứng của tổ chức **tuyệt đối không commit** lên repo
công khai.

## Mô hình dữ liệu

Ba loại tệp YAML, phân biệt bằng trường `kind`. JSON Schema nằm trong `schemas/` (sinh bằng
`vncc schema`), dùng được với trình soạn thảo để gợi ý và kiểm tra khi gõ.

| kind | Nội dung |
|---|---|
| `catalog` | Danh mục yêu cầu: nhóm, mã, nhãn ngắn tự diễn đạt, thẻ (`cap-do-N`, chủ thể thực hiện, `can-doi-chieu`) |
| `mapping` | Đối chiếu giữa hai danh mục: quan hệ, lý do, mức tin cậy, người rà soát |
| `assessment` | Hồ sơ đánh giá của một tổ chức: cấp độ HTTT (tùy chọn), áp dụng, trạng thái, bằng chứng, người phụ trách |

**Lọc theo cấp độ:** yêu cầu không gắn thẻ `cap-do-N` áp dụng cho mọi cấp độ; yêu cầu có thẻ chỉ áp
dụng cho các cấp độ đã gắn. Đặt `level` trong hồ sơ hoặc dùng `--level` ở `init`, `soa`, `gap`.

Loại quan hệ theo cách tiếp cận tập hợp của NIST OLIR: `equivalent`, `subset_of`, `superset_of`,
`intersects`, `no_relationship`. Tra cứu hai chiều tự động đảo `subset_of` ↔ `superset_of`.

## Lộ trình

- **v0.1:** danh mục ISO 27001:2022, mô hình dữ liệu, SoA, báo cáo khoảng cách, ví dụ hư cấu.
- **v0.2 (hiện tại):** danh mục và đối chiếu NĐ 331/2026, lọc theo cấp độ, báo cáo độ phủ.
- **v0.3:** đối chiếu toàn văn Điều 33–37 NĐ 331; điều khoản chính ISO/IEC 27001 (4–10); Luật 91/2025 và NĐ 356/2025.
- **v0.4:** xuất định dạng NIST OSCAL; trang tra cứu tĩnh trên GitHub Pages.

## Bản quyền và miễn trừ

- Mã nguồn: MIT. Dữ liệu đối chiếu: CC BY 4.0 ([LICENSE-DATA](LICENSE-DATA)).
- Dự án **không chứa nội dung tiêu chuẩn ISO**; chỉ có mã điều khoản và nhãn ngắn tự diễn đạt.
- Văn bản quy phạm pháp luật Việt Nam được tóm tắt, dẫn nguồn và ngày hiệu lực; người dùng phải
  đối chiếu văn bản gốc.
- Đối chiếu là **diễn giải chuyên môn của tác giả**, không phải ý kiến pháp lý và không thay thế
  hướng dẫn của cơ quan có thẩm quyền.

## Đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md) và [docs/them-van-ban.md](docs/them-van-ban.md). Đề xuất
sửa một dòng đối chiếu: dùng mẫu issue **"Đề xuất sửa đối chiếu"**.

---

## English

**Machine-readable crosswalks between ISO/IEC 27001:2022 and Vietnamese regulations (Decree
331/2026 on cybersecurity of information systems, Personal Data Protection Law 91/2025), with SoA,
gap-report and coverage generators.** Version 0.2 ships a 64-requirement catalog of Decree 331/2026
tagged by security level (1–5) and a 68-entry draft mapping to ISO/IEC 27001 Annex A; the coverage
report shows that more than a third of the Decree's obligations (level determination dossiers, independent
appraisal, 24/72-hour incident reporting, annual reporting) have no Annex A counterpart. Each mapping entry records a set-theoretic relationship (NIST OLIR
style), a rationale and a confidence level, so mappings can be reviewed like code.

```bash
pip install "git+https://github.com/thinhnx128/vn-compliance-crosswalk"
vncc init iso27001-2022 -o assessment.yaml
vncc soa assessment.yaml -o soa.xlsx
vncc gap assessment.yaml -o gap.md
```

Private organisational catalogs and mappings can be overlaid with `--data-dir` without publishing
them. The project contains no ISO standard text. Mappings are the author's professional
interpretation, not legal advice.

Author: [Nguyen Xuan Thinh](https://github.com/thinhnx128).
