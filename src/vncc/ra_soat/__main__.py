"""Dòng lệnh: python -m vncc.ra_soat danh-gia <thư mục> [--bo-cham luat|ai|ca-hai] [--ra <thư mục kết quả>].

Lệnh tương đương khi đã cài: vncc ra-soat <thư mục> ...

Mã thoát: 0 thành công; 2 lỗi đầu vào; 3 bộ chấm không chạy được (thiếu khóa, lỗi API, model từ chối, chạm trần
lượt gọi), khi đó không ghi báo cáo.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from . import catalog as cat
from .engine import assess
from .judges import AnthropicJudge, JudgeError, RuleJudge
from .loader import read_folder
from .report import to_csv, to_markdown

BO_CHAM = ("luat", "ai", "ca-hai")


def parse_not_applicable(items: list[str]) -> dict[str, str]:
    na: dict[str, str] = {}
    for item in items:
        k, _, v = item.partition("=")
        if k.strip():
            na[k.strip()] = v.strip() or "người dùng khai báo"
    return na


def run(
    thu_muc: Path, bo_cham: str = "luat", ra: Path = Path("ket-qua"), khong_ap_dung: list[str] | None = None
) -> int:
    """Chạy một lần rà; trả về mã thoát. Dùng chung cho `python -m vncc.ra_soat` và `vncc ra-soat`."""
    thu_muc, ra = Path(thu_muc), Path(ra)
    if bo_cham not in BO_CHAM:
        print(f"--bo-cham phải là một trong: {', '.join(BO_CHAM)}", file=sys.stderr)
        return 2
    if not thu_muc.exists():
        print(f"Không thấy {thu_muc}", file=sys.stderr)
        return 2
    catalog = cat.load()
    segments = read_folder(thu_muc)
    if not segments:
        print("Không đọc được đoạn văn bản nào (hỗ trợ .md, .txt, .docx).", file=sys.stderr)
        return 2
    na = parse_not_applicable(khong_ap_dung or [])
    unknown = sorted(set(na) - {r.id for r in catalog.requirements})
    if unknown:
        print(f"Mã yêu cầu không có trong danh mục: {', '.join(unknown)}", file=sys.stderr)
        return 2
    try:
        if bo_cham == "luat":
            judge, second, name = RuleJudge(), None, "bộ luật (mẫu từ khóa)"
        elif bo_cham == "ai":
            judge, second, name = AnthropicJudge(), None, "AI, thử nghiệm (khóa API của người dùng)"
        else:
            judge, second, name = AnthropicJudge(), RuleJudge(), "AI, thử nghiệm, đối chiếu với bộ luật"
        results = assess(catalog, segments, judge, second, na)
    except JudgeError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    ra.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    (ra / "bao-cao.md").write_text(to_markdown(catalog, results, thu_muc.name, name, today), encoding="utf-8")
    (ra / "ma-tran.csv").write_text(to_csv(results), encoding="utf-8")
    print(
        f"Đã rà {len(segments)} đoạn, {len(results)} yêu cầu. Kết quả: {ra / 'bao-cao.md'}, {ra / 'ma-tran.csv'}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m vncc.ra_soat", description="Rà soát khoảng trống tuân thủ (thử nghiệm)"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("danh-gia", help="rà một thư mục văn bản")
    d.add_argument("thu_muc", type=Path)
    d.add_argument("--bo-cham", choices=list(BO_CHAM), default="luat")
    d.add_argument("--ra", type=Path, default=Path("ket-qua"))
    d.add_argument(
        "--khong-ap-dung",
        action="append",
        default=[],
        metavar="MA=LY_DO",
        help="khai báo yêu cầu không áp dụng, ví dụ VN-PDP-10=DN nhỏ chọn không thực hiện (Điều 38)",
    )
    a = ap.parse_args(argv)
    return run(a.thu_muc, a.bo_cham, a.ra, a.khong_ap_dung)


if __name__ == "__main__":
    sys.exit(main())
