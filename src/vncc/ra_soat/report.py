"""Xuất báo cáo khoảng trống (Markdown) và ma trận (CSV)."""

from __future__ import annotations

import csv
import io
from collections import Counter

from .catalog import Catalog
from .engine import CAN_XAC_NHAN, CHUA, DAP_UNG, KHONG_AP_DUNG, KHONG_DU, MOT_PHAN, RequirementResult

ORDER = [DAP_UNG, CAN_XAC_NHAN, MOT_PHAN, CHUA, KHONG_DU, KHONG_AP_DUNG]


def _safe(s: str) -> str:
    """Chặn chèn công thức khi mở CSV bằng bảng tính."""
    # Ký tự NUL làm mô-đun csv của Python 3.10 báo lỗi và không có nghĩa trong văn bản: bỏ đi
    s = s.replace("\x00", "")
    # Kiểm tra cả sau khi bỏ khoảng trắng, ký tự điều khiển ở đầu (bảng tính có thể bỏ qua chúng)
    head = s.lstrip("".join(chr(c) for c in range(33)) + "\x7f")
    return "'" + s if s[:1] in ("=", "+", "-", "@", "\t", "\r") or head[:1] in ("=", "+", "-", "@") else s


def to_csv(results: list[RequirementResult]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(
        [
            "Mã yêu cầu",
            "Tên yêu cầu",
            "Loại",
            "Trạng thái",
            "Mã yếu tố",
            "Yếu tố",
            "Có bằng chứng",
            "Vị trí",
            "Trích dẫn",
            "Ghi chú",
        ]
    )
    def row(cells):  # mọi ô đều bỏ ký tự NUL (Python 3.10 không ghi được NUL vào CSV)
        w.writerow([str(c).replace("\x00", "") for c in cells])

    for r in results:
        if not r.elements:
            row([r.req.id, r.req.title, r.req.type, r.status, "", "", "", "", "", _safe(r.note)])
        for e in r.elements:
            row(
                [
                    r.req.id,
                    r.req.title,
                    r.req.type,
                    r.status,
                    e.element.id,
                    e.element.text,
                    "Có" if e.found else "Không",
                    _safe(e.ref),
                    _safe(e.quote),
                    _safe(r.note),
                ]
            )
    return "﻿" + buf.getvalue()


def to_markdown(
    catalog: Catalog, results: list[RequirementResult], source: str, judge_name: str, date: str
) -> str:
    c = Counter(r.status for r in results)
    lines = [
        "# Báo cáo rà soát khoảng trống tuân thủ (đánh giá sơ bộ)",
        "",
        f"Khung: {catalog.framework_title} · Danh mục {catalog.version}, yếu tố {catalog.elements_version}, "
        f"đối chiếu văn bản ngày {catalog.verified_on}",
        f"Bộ văn bản: `{source}` · Bộ chấm: {judge_name} · Ngày chạy: {date}",
        "",
        f"> **Đánh giá sơ bộ do công cụ tạo ra, không phải kết luận pháp lý hay kết luận đánh giá.** {catalog.disclaimer}",
        "> Công cụ chỉ thấy nội dung văn bản được đưa vào; việc thực hiện trên thực tế cần kiểm tra riêng.",
        "> **Cách đọc nhãn:** \"Đủ bằng chứng trong văn bản\" chỉ ghi nhận văn bản có câu chữ tương ứng, không chứng nhận"
        " tổ chức đã thực hiện hay đã tuân thủ. \"Chưa tìm thấy bằng chứng\" và \"Văn bản không đề cập\" không chứng minh"
        " văn bản thiếu nội dung: bộ chấm theo luật bỏ sót nhiều cách diễn đạt khác mẫu, cần rà thủ công trước khi kết luận."
        " \"Không áp dụng\" là do người dùng tự khai báo, công cụ không thẩm định căn cứ được miễn.",
        "",
        "## Tổng hợp",
        "",
        "| Trạng thái | Số yêu cầu |",
        "|---|---|",
    ]
    lines += [f"| {s} | {c.get(s, 0)} |" for s in ORDER]
    gaps = sorted([r for r in results if r.priority > 0], key=lambda r: (-r.priority, r.req.id))
    lines += [
        "",
        "## Khoảng trống cần xử lý (xếp theo ưu tiên)",
        "",
        "Ưu tiên tạm tính theo loại yêu cầu (luật định trước) và số yếu tố còn thiếu; "
        "chưa tính mức phạt theo NĐ 330/2026 vì công cụ chưa có danh mục mức phạt.",
        "",
    ]
    if not gaps:
        lines.append("Không phát hiện khoảng trống trong phạm vi văn bản được rà.")
    for i, r in enumerate(gaps, 1):
        lines.append(f"{i}. **{r.req.id} — {r.req.title}** ({r.status}; căn cứ: {r.req.legal})")
        for e in r.missing:
            lines.append(f"   - Thiếu: {e.element.text}")
        if r.note:
            lines.append(f"   - {r.note}")
    lines += ["", "## Chi tiết theo yêu cầu", ""]
    for r in results:
        lines.append(f"### {r.req.id} — {r.req.title}: {r.status}")
        lines.append("")
        if r.note:
            lines.append(f"_{r.note}_")
            lines.append("")
        for e in r.elements:
            mark = "Có" if e.found else "Không"
            lines.append(f"- [{mark}] {e.element.text}")
            if e.found:
                q = e.quote if len(e.quote) <= 240 else e.quote[:237] + "..."
                lines.append(f'  - `{e.ref}`: "{q}"')
        lines.append("")
    return "\n".join(lines) + "\n"
