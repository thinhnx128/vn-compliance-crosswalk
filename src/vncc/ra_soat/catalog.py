"""Nạp danh mục yêu cầu (nội dung, căn cứ) và yếu tố kiểm được (mẫu chấm, chủ đề).

Dữ liệu nằm ở ``catalogs/ra-soat/`` khi chạy từ mã nguồn, hoặc ``vncc/data/catalogs/ra-soat/`` khi đã cài
(tìm theo cùng cách với ``vncc.repository.bundled_data_dir``).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from ..repository import bundled_data_dir

TYPE_WEIGHT = {"LD": 3, "LD+TT": 2, "TT": 1}  # dùng xếp ưu tiên khi chưa có danh mục mức phạt (NĐ 330/2026)


def data_dir() -> Path:
    return bundled_data_dir() / "catalogs" / "ra-soat"


DEFAULT_REQUIREMENTS = data_dir() / "vn-pdp-2025.requirements.json"
DEFAULT_ELEMENTS = data_dir() / "vn-pdp-2025.elements.json"
DEFAULT_MAU = data_dir() / "vn-pdp-2025.mau.json"  # ánh xạ yêu cầu -> mục trong bộ mẫu DP-01..07


@dataclass
class Element:
    id: str
    text: str
    patterns: list[list[re.Pattern]]


@dataclass
class Requirement:
    id: str
    section: str
    type: str
    title: str
    statement: str
    legal: str
    applicability: str
    iso: list[str]
    topic: list[re.Pattern]
    elements: list[Element] = field(default_factory=list)
    mau: list[str] = field(default_factory=list)  # mục mẫu tham khảo để lấp khoảng trống, ví dụ 'DP-01, mục "5. ..."'


@dataclass
class Catalog:
    framework_id: str
    framework_title: str
    version: str
    elements_version: str
    verified_on: str
    disclaimer: str
    requirements: list[Requirement]


def _rx(s: str) -> re.Pattern:
    return re.compile(s, re.IGNORECASE)


def load_mau(path: Path, ids: set[str]) -> dict[str, list[str]]:
    """Đọc ánh xạ yêu cầu -> mục mẫu. Không có tệp thì trả rỗng (báo cáo bỏ dòng gợi ý mẫu)."""
    path = Path(path)
    if not path.is_file():
        return {}
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Tệp ánh xạ mẫu {path.name} không phải JSON hợp lệ: {exc}") from exc
    files, reqs = (d.get("mau"), d.get("requirements")) if isinstance(d, dict) else (None, None)
    if not isinstance(files, dict) or not isinstance(reqs, dict):
        raise ValueError(f"Tệp ánh xạ mẫu {path.name} thiếu 'mau' hoặc 'requirements' dạng đối tượng")
    extra = sorted(set(reqs) - ids)
    if extra:
        raise ValueError(f"Ánh xạ mẫu có mã yêu cầu không tồn tại: {extra}")
    out: dict[str, list[str]] = {}
    for rid, items in reqs.items():
        if not isinstance(items, list) or not items:
            raise ValueError(f"{rid}: ánh xạ mẫu phải là danh sách không rỗng")
        for x in items:
            if not (isinstance(x, dict) and isinstance(x.get("mau"), str) and isinstance(x.get("muc"), str) and x["muc"]):
                raise ValueError(f"{rid}: mỗi mục ánh xạ cần 'mau' và 'muc' dạng chuỗi")
            if x["mau"] not in files:
                raise ValueError(f"{rid}: mẫu {x['mau']} không có trong danh sách tệp mẫu")
        out[rid] = [f'{x["mau"]}, mục "{x["muc"]}"' for x in items]
    return out


def load(
    requirements_path: Path = DEFAULT_REQUIREMENTS,
    elements_path: Path = DEFAULT_ELEMENTS,
    mau_path: Path = DEFAULT_MAU,
) -> Catalog:
    req = json.loads(Path(requirements_path).read_text(encoding="utf-8"))
    ele = json.loads(Path(elements_path).read_text(encoding="utf-8"))
    emap = ele["requirements"]
    f = req["framework"]
    out: list[Requirement] = []
    missing = [r["id"] for r in req["requirements"] if r["id"] not in emap]
    extra = sorted(set(emap) - {r["id"] for r in req["requirements"]})
    if missing or extra:
        raise ValueError(f"Danh mục yếu tố lệch danh mục yêu cầu. Thiếu: {missing}; thừa: {extra}")
    mau = load_mau(mau_path, {r["id"] for r in req["requirements"]})
    for r in req["requirements"]:
        e = emap[r["id"]]
        if not e.get("elements"):
            raise ValueError(f"{r['id']}: chưa có yếu tố")
        elements = []
        seen = set()
        for x in e["elements"]:
            if x["id"] in seen:
                raise ValueError(f"{r['id']}: trùng yếu tố {x['id']}")
            seen.add(x["id"])
            if not x.get("patterns") or not all(x["patterns"]):
                raise ValueError(f"{r['id']}.{x['id']}: thiếu mẫu chấm")
            elements.append(Element(x["id"], x["text"], [[_rx(p) for p in alt] for alt in x["patterns"]]))
        out.append(
            Requirement(
                id=r["id"],
                section=r["section"],
                type=r["type"],
                title=r["title"]["vi"],
                statement=r["statement"]["vi"],
                legal=r["legal"]["vi"],
                applicability=(r.get("applicability") or {}).get("vi", ""),
                iso=r["iso27001_2022"],
                topic=[_rx(t) for t in e["topic"]],
                elements=elements,
                mau=mau.get(r["id"], []),
            )
        )
    return Catalog(
        f["id"],
        f["title"]["vi"],
        f["version"],
        ele["catalog_version"],
        f["verified_on"],
        f["disclaimer"]["vi"],
        out,
    )
