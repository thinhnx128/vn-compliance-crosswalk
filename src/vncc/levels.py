"""Xác định cấp độ HTTT sơ bộ theo tiêu chí Nghị định 331/2026/NĐ-CP (Điều 9, 11–15).

Tiêu chí được khai báo dưới dạng dữ liệu trong ``nd331_cap_do.json`` và dùng chung với trang web
``docs/cap-do/index.html``, để logic của CLI và trang web không bị lệch nhau.

Quy tắc: lấy cấp độ cao nhất trong các tiêu chí thỏa mãn (Điều 8 khoản 2). Câu hỏi không hiển thị
với loại hệ thống đã chọn (``show_if``) được đặt về giá trị mặc định trước khi đánh giá.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from importlib import resources
from typing import Any


@lru_cache(maxsize=1)
def criteria_data() -> dict[str, Any]:
    return json.loads((resources.files("vncc") / "nd331_cap_do.json").read_text(encoding="utf-8"))


def criteria_json() -> str:
    return json.dumps(criteria_data(), ensure_ascii=False, separators=(",", ":"))


@dataclass
class Match:
    id: str
    level: int
    article: str
    label: str


@dataclass
class LevelResult:
    level: int | None
    matches: list[Match] = field(default_factory=list)
    approval: str | None = None
    warnings: list[str] = field(default_factory=list)
    reminders: list[str] = field(default_factory=list)
    answers: dict[str, Any] = field(default_factory=dict)


def _test(answers: dict[str, Any], cond: list) -> bool:
    key, op, value = cond
    actual = answers.get(key)
    if op == "eq":
        return actual == value
    if op == "in":
        return actual in value
    if op == "contains":
        return value in (actual or [])
    if op == "contains_any":
        return any(v in (actual or []) for v in value)
    if op == "not_contains_any":
        return not any(v in (actual or []) for v in value)
    if op == "gte":
        return (actual or 0) >= value
    if op == "lt":
        return (actual or 0) < value
    raise ValueError(f"Toán tử không hỗ trợ: {op}")


def normalize(answers: dict[str, Any]) -> dict[str, Any]:
    """Kiểm tra kiểu, điền mặc định, và xóa câu trả lời của câu hỏi không áp dụng."""
    data = criteria_data()
    out: dict[str, Any] = {}
    known = {q["id"] for q in data["questions"]}
    unknown = set(answers) - known
    if unknown:
        raise ValueError(f"Câu hỏi không tồn tại: {', '.join(sorted(unknown))}")
    for q in data["questions"]:
        default = q.get("default", [] if q["type"] == "multi" else None)
        v = answers.get(q["id"], default)
        if q["type"] == "choice":
            allowed = [o["value"] for o in q["options"]]
            if v is None:
                raise ValueError(f"Thiếu câu trả lời: {q['id']}")
            if v not in allowed:
                raise ValueError(f"{q['id']}: '{v}' không hợp lệ, chọn một trong {allowed}")
        elif q["type"] == "multi":
            v = list(v or [])
            allowed = {o["value"] for o in q["options"]}
            bad = [x for x in v if x not in allowed]
            if bad:
                raise ValueError(f"{q['id']}: giá trị không hợp lệ {bad}")
        elif q["type"] == "bool":
            if not isinstance(v, bool):
                raise ValueError(f"{q['id']}: phải là true/false")
        elif q["type"] == "int":
            if isinstance(v, bool) or not isinstance(v, int) or v < 0:
                raise ValueError(f"{q['id']}: phải là số nguyên không âm")
        out[q["id"]] = v
    for q in data["questions"]:
        cond = q.get("show_if")
        if cond and not _test(out, cond):
            out[q["id"]] = q.get("default", [] if q["type"] == "multi" else None)
    return out


def determine(answers: dict[str, Any]) -> LevelResult:
    data = criteria_data()
    a = normalize(answers)
    matches = [
        Match(c["id"], c["level"], c["article"], c["label"])
        for c in data["criteria"]
        if all(_test(a, cond) for cond in c["all"])
    ]
    level = max((m.level for m in matches), default=None)
    warnings: list[str] = []
    if not a["info"]:
        warnings.append("Chưa chọn loại thông tin hệ thống xử lý (Điều 9 khoản 1).")
    if level is None:
        warnings.append(
            "Chưa khớp tiêu chí nào: cần đánh giá theo Khung quản lý rủi ro an ninh mạng hoặc "
            "bổ sung thông tin về hệ thống."
        )
    return LevelResult(
        level=level,
        matches=sorted(matches, key=lambda m: (-m.level, m.id)),
        approval=data["approval"].get(str(level)) if level else None,
        warnings=warnings,
        reminders=list(data["reminders"]),
        answers=a,
    )
