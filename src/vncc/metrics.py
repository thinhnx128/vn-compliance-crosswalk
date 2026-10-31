"""Tính toán chỉ số tuân thủ, với quy tắc tính được nêu rõ.

Quy tắc (mặc định):

* Mẫu số = số control **áp dụng** (applicable = true), kể cả control chưa đánh giá.
* Tử số = số control ``implemented`` + 0,5 x số control ``partial``.
* Control ``planned``, ``not_implemented`` và chưa đánh giá tính 0.
* Control không áp dụng bị loại khỏi cả tử số và mẫu số.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .models import Assessment, Catalog, ControlState

PARTIAL_WEIGHT = 0.5
RULE = (
    "Tỷ lệ = (Đã triển khai + 0,5 x Triển khai một phần) / Số control áp dụng; "
    "control không áp dụng bị loại khỏi mẫu số, control chưa đánh giá tính 0."
)


@dataclass
class Tally:
    total: int = 0
    not_applicable: int = 0
    counts: Counter | None = None

    @property
    def applicable(self) -> int:
        return self.total - self.not_applicable

    @property
    def score(self) -> float | None:
        if not self.applicable:
            return None
        c = self.counts or Counter()
        return (c["implemented"] + PARTIAL_WEIGHT * c["partial"]) / self.applicable


def state_of(assessment: Assessment, control_id: str) -> ControlState:
    return assessment.controls.get(control_id, ControlState())


def tally(catalog: Catalog, assessment: Assessment) -> dict[str, Tally]:
    """Thống kê theo nhóm; khóa '*' là toàn bộ danh mục."""
    result: dict[str, Tally] = {"*": Tally(counts=Counter())}
    for group, control in catalog.controls():
        t = result.setdefault(group.id, Tally(counts=Counter()))
        state = state_of(assessment, control.id)
        for bucket in (t, result["*"]):
            bucket.total += 1
            if not state.applicable:
                bucket.not_applicable += 1
            else:
                bucket.counts[state.status or "unassessed"] += 1
    return result
