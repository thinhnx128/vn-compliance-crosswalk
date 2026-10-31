"""Nạp và kiểm tra tính nhất quán của dữ liệu từ một hoặc nhiều thư mục.

Thư mục dữ liệu riêng của tổ chức (ví dụ danh mục chính sách nội bộ) có thể nạp chồng lên dữ
liệu công khai bằng ``--data-dir`` mà không cần đưa lên repo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path

import yaml
from pydantic import ValidationError

from .models import MODELS, Assessment, Catalog, Mapping, Relationship


class DataError(Exception):
    pass


def load_file(path: str | Path):
    path = Path(path)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise DataError(f"{path}: YAML không hợp lệ: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("kind") not in MODELS:
        raise DataError(f"{path}: thiếu trường kind (catalog | mapping | assessment)")
    try:
        return MODELS[raw["kind"]].model_validate(raw)
    except ValidationError as exc:
        raise DataError(f"{path}: {exc}") from exc


def bundled_data_dir() -> Path:
    """Thư mục dữ liệu đóng gói kèm thư viện (catalogs/, mappings/)."""
    packaged = Path(str(resources.files("vncc") / "data"))
    if packaged.exists():
        return packaged
    return Path(__file__).resolve().parents[2]  # chạy trực tiếp từ mã nguồn repo


@dataclass
class Related:
    catalog: str
    control: str | None
    relationship: str
    confidence: str
    rationale: str


@dataclass
class Repository:
    catalogs: dict[str, Catalog] = field(default_factory=dict)
    mappings: dict[str, Mapping] = field(default_factory=dict)
    sources: dict[str, Path] = field(default_factory=dict)

    @classmethod
    def load(cls, *dirs: str | Path, include_bundled: bool = True) -> Repository:
        repo = cls()
        roots = ([bundled_data_dir()] if include_bundled else []) + [Path(d) for d in dirs]
        for root in roots:
            for sub in ("catalogs", "mappings"):
                for path in sorted((root / sub).glob("*.y*ml")):
                    repo.add(load_file(path), path)
        return repo

    def add(self, obj, path: Path | None = None) -> None:
        if isinstance(obj, Catalog):
            self.catalogs[obj.id] = obj
        elif isinstance(obj, Mapping):
            self.mappings[obj.id] = obj
        else:
            raise DataError(f"{path}: chỉ nạp catalog/mapping vào kho dữ liệu")
        if path:
            self.sources[obj.id] = path

    def catalog(self, catalog_id: str) -> Catalog:
        try:
            return self.catalogs[catalog_id]
        except KeyError:
            known = ", ".join(sorted(self.catalogs)) or "(trống)"
            raise DataError(f"Không có danh mục '{catalog_id}'. Hiện có: {known}") from None

    # ------------------------------------------------------------------ kiểm tra
    def validate(self) -> list[str]:
        """Trả về danh sách lỗi tham chiếu chéo; rỗng nghĩa là hợp lệ."""
        errors: list[str] = []
        for m in self.mappings.values():
            missing = [c for c in (m.source_catalog, m.target_catalog) if c not in self.catalogs]
            if missing:
                errors.append(f"{m.id}: tham chiếu danh mục không tồn tại: {', '.join(missing)}")
                continue
            src = self.catalogs[m.source_catalog].index()
            dst = self.catalogs[m.target_catalog].index()
            for i, e in enumerate(m.entries, 1):
                if e.source not in src:
                    errors.append(f"{m.id} dòng {i}: source '{e.source}' không có trong danh mục")
                if e.target and e.target not in dst:
                    errors.append(f"{m.id} dòng {i}: target '{e.target}' không có trong danh mục")
        return errors

    def validate_assessment(self, a: Assessment) -> tuple[list[str], list[str]]:
        """Trả về (lỗi, cảnh báo) của hồ sơ đánh giá."""
        index = self.catalog(a.catalog).index()
        errors = [f"Control '{cid}' không có trong {a.catalog}" for cid in a.controls if cid not in index]
        missing = [cid for cid in index if cid not in a.controls]
        warnings = [f"{len(missing)} control chưa có trong hồ sơ: {', '.join(missing)}"] if missing else []
        return errors, warnings

    # ------------------------------------------------------------------ tra cứu
    def related(self, catalog_id: str, control_id: str, only: set[str] | None = None) -> list[Related]:
        """Các yêu cầu ở danh mục khác liên quan tới một control, tra theo cả hai chiều."""
        out: list[Related] = []
        for m in self.mappings.values():
            for e in m.entries:
                if m.source_catalog == catalog_id and e.source == control_id:
                    other, ctl, rel = m.target_catalog, e.target, Relationship(e.relationship)
                elif m.target_catalog == catalog_id and e.target == control_id:
                    other, ctl, rel = m.source_catalog, e.source, Relationship(e.relationship).inverse()
                else:
                    continue
                if only is None or other in only:
                    out.append(Related(other, ctl, rel.value, e.confidence, e.rationale))
        return out
