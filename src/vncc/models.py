"""Mô hình dữ liệu: danh mục (catalog), bảng đối chiếu (mapping), hồ sơ đánh giá (assessment)."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SLUG = r"^[a-z0-9][a-z0-9_.-]*$"


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


# --------------------------------------------------------------------------- catalog
class Control(_Base):
    id: str = Field(min_length=1, description="Mã yêu cầu/biện pháp, duy nhất trong danh mục")
    title: str = Field(min_length=1, description="Nhãn ngắn tiếng Việt, tự diễn đạt")
    title_en: str | None = None
    summary: str | None = Field(None, description="Tóm tắt tự viết, không chép nguyên văn")
    tags: list[str] = Field(default_factory=list, description="Ví dụ: cap-do-3, dlcn-nhay-cam")


LEVEL_TAG = "cap-do-"


def applies_to_level(control: Control, level: int) -> bool:
    """Control không gắn thẻ cap-do-N áp dụng cho mọi cấp độ; có thẻ thì chỉ áp dụng cấp độ đã gắn."""
    levels = [t for t in control.tags if t.startswith(LEVEL_TAG)]
    return not levels or f"{LEVEL_TAG}{level}" in levels


class Group(_Base):
    id: str
    title: str
    controls: list[Control] = Field(default_factory=list)


class Catalog(_Base):
    kind: Literal["catalog"] = "catalog"
    id: str = Field(pattern=SLUG)
    title: str
    version: str
    publisher: str
    document_number: str | None = None
    issued_on: date | None = None
    effective_date: date | None = None
    source_url: str | None = None
    status: Literal["skeleton", "draft", "reviewed"]
    notice: str | None = None
    groups: list[Group] = Field(default_factory=list)

    def controls(self) -> Iterator[tuple[Group, Control]]:
        for group in self.groups:
            for control in group.controls:
                yield group, control

    def index(self) -> dict[str, Control]:
        return {c.id: c for _, c in self.controls()}

    def for_level(self, level: int | None) -> Catalog:
        """Bản sao chỉ gồm control áp dụng cho một cấp độ HTTT (xem applies_to_level)."""
        if level is None:
            return self
        groups = [
            g.model_copy(update={"controls": [c for c in g.controls if applies_to_level(c, level)]})
            for g in self.groups
        ]
        return self.model_copy(update={"groups": [g for g in groups if g.controls]})

    @model_validator(mode="after")
    def _unique_ids(self) -> Catalog:
        seen: set[str] = set()
        for _, c in self.controls():
            if c.id in seen:
                raise ValueError(f"Mã control bị trùng: {c.id}")
            seen.add(c.id)
        return self


# --------------------------------------------------------------------------- mapping
class Relationship(str, Enum):
    equivalent = "equivalent"
    subset_of = "subset_of"
    superset_of = "superset_of"
    intersects = "intersects"
    no_relationship = "no_relationship"

    def inverse(self) -> Relationship:
        if self is Relationship.subset_of:
            return Relationship.superset_of
        if self is Relationship.superset_of:
            return Relationship.subset_of
        return self


class MappingEntry(_Base):
    source: str
    target: str | None = None
    relationship: Relationship
    rationale: str = Field(min_length=10, description="Lý do đối chiếu, bắt buộc để phản biện được")
    confidence: Literal["high", "medium", "low"]
    reviewed_by: str | None = None
    reviewed_on: date | None = None

    @model_validator(mode="after")
    def _target_rule(self) -> MappingEntry:
        if self.relationship == Relationship.no_relationship.value:
            if self.target is not None:
                raise ValueError("Quan hệ no_relationship thì không ghi target")
        elif not self.target:
            raise ValueError(f"Thiếu target cho {self.source}")
        return self


class Mapping(_Base):
    kind: Literal["mapping"] = "mapping"
    id: str = Field(pattern=SLUG)
    source_catalog: str
    target_catalog: str
    version: str
    status: Literal["skeleton", "draft", "reviewed"]
    author: str | None = None
    notice: str | None = None
    entries: list[MappingEntry] = Field(default_factory=list)


# --------------------------------------------------------------------------- assessment
class ImplementationStatus(str, Enum):
    implemented = "implemented"
    partial = "partial"
    planned = "planned"
    not_implemented = "not_implemented"


STATUS_LABELS = {
    "implemented": "Đã triển khai",
    "partial": "Triển khai một phần",
    "planned": "Đã lập kế hoạch",
    "not_implemented": "Chưa triển khai",
    None: "Chưa đánh giá",
}


class ControlState(_Base):
    applicable: bool = True
    justification: str | None = Field(None, description="Lý do áp dụng / không áp dụng")
    status: ImplementationStatus | None = None
    evidence: list[str] = Field(default_factory=list)
    owner: str | None = None
    due: date | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def _justify_exclusion(self) -> ControlState:
        if not self.applicable and not self.justification:
            raise ValueError("Control không áp dụng phải có justification")
        return self


class Assessment(_Base):
    kind: Literal["assessment"] = "assessment"
    organization: str
    scope: str
    catalog: str
    as_of: date
    level: int | None = Field(
        None, ge=1, le=5, description="Cấp độ HTTT được đánh giá; lọc control theo thẻ cap-do-N"
    )
    controls: dict[str, ControlState] = Field(default_factory=dict)


MODELS: dict[str, type[_Base]] = {
    "catalog": Catalog,
    "mapping": Mapping,
    "assessment": Assessment,
}
