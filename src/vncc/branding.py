"""Thông tin tác giả và watermark dùng cho trang web và gói Excel."""

from __future__ import annotations

from urllib.parse import quote

AUTHOR = "Nguyễn Xuân Thịnh"
HANDLE = "thinhnx128"
GITHUB_URL = f"https://github.com/{HANDLE}"
LINKEDIN_URL = f"https://www.linkedin.com/in/{HANDLE}"
REPO_URL = f"{GITHUB_URL}/vn-compliance-crosswalk"
CREDIT = f"© {AUTHOR} · github.com/{HANDLE}"


def watermark_svg() -> str:
    """Ô watermark lặp: tên tác giả và tài khoản GitHub, xoay chéo, màu xám trung tính hợp cả nền sáng và tối."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="440" height="260">'
        '<g transform="rotate(-24 220 130)" fill="#7a8594" font-family="Segoe UI,Arial,sans-serif" '
        'text-anchor="middle">'
        f'<text x="220" y="124" font-size="18" font-weight="600">{AUTHOR}</text>'
        f'<text x="220" y="148" font-size="13">github.com/{HANDLE}</text>'
        "</g></svg>"
    )


def watermark_data_uri() -> str:
    return "data:image/svg+xml," + quote(watermark_svg(), safe="")
