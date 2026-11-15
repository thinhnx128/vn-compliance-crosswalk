"""Bộ máy rà soát: chọn đoạn ứng viên, gọi bộ chấm, kiểm trích dẫn, tính nhãn theo quy tắc.

Nguyên tắc an toàn:
- Trích dẫn phải khớp nguyên văn một đoạn NẰM TRONG danh sách ứng viên của chính yếu tố đang chấm, và đủ dài.
- Mọi kết luận của bộ chấm không tin cậy (AI), có hoặc không, chưa được bộ luật xác nhận (với "có" thì ở cùng đoạn)
  không bao giờ tự thành nhãn kết luận: yêu cầu đó nhận nhãn "Cần rà soát thủ công".
- Bộ chấm lỗi thì cả lần rà dừng (JudgeError), không biến thành "không có bằng chứng".
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .catalog import TYPE_WEIGHT, Catalog, Element, Requirement
from .judges import MIN_QUOTE_CHARS, MIN_QUOTE_WORDS, Judge, Verdict
from .loader import Segment, normalize

DAP_UNG = "Đủ bằng chứng trong văn bản"
CAN_XAC_NHAN = "Cần rà soát thủ công"
MOT_PHAN = "Có bằng chứng một phần"
CHUA = "Chưa tìm thấy bằng chứng"
KHONG_DU = "Văn bản không đề cập"
KHONG_AP_DUNG = "Không áp dụng (người dùng khai báo)"

BATCH = 25  # số đoạn mỗi lô gửi bộ chấm AI


@dataclass
class ElementResult:
    element: Element
    found: bool
    quote: str
    ref: str
    reason: str
    confirmed: bool = False  # có bộ chấm tin cậy (bộ luật) xác nhận
    second: Verdict | None = None  # kết quả bộ chấm thứ hai (nếu có)

    @property
    def disagree(self) -> bool:
        return self.second is not None and self.second.found != self.found


@dataclass
class RequirementResult:
    req: Requirement
    status: str
    elements: list[ElementResult] = field(default_factory=list)
    topic_hits: int = 0
    note: str = ""

    @property
    def missing(self) -> list[ElementResult]:
        return [e for e in self.elements if not e.found]

    @property
    def priority(self) -> int:
        """Điểm ưu tiên tạm (cao = sửa trước) khi chưa có danh mục mức phạt NĐ 330/2026."""
        if self.status in (DAP_UNG, KHONG_AP_DUNG):
            return 0
        if self.status == CAN_XAC_NHAN and not self.missing:
            return 1
        return TYPE_WEIGHT.get(self.req.type, 1) * 10 + len(self.missing)


def verify_quote(v: Verdict, allowed: dict[str, Segment]) -> Verdict:
    """Trích dẫn phải là chuỗi con nguyên văn (sau chuẩn hóa khoảng trắng) của một đoạn trong `allowed`, đủ dài."""
    if not v.found:
        return v
    seg = allowed.get(v.ref)
    q = normalize(v.quote)
    if seg is None:
        return Verdict(False, reason="trích dẫn từ đoạn ngoài danh sách ứng viên")
    if len(q) < MIN_QUOTE_CHARS or len(q.split()) < MIN_QUOTE_WORDS:
        return Verdict(False, reason="trích dẫn quá ngắn, quá chung chung")
    if q not in normalize(seg.text):
        return Verdict(False, reason="trích dẫn không khớp tài liệu gốc")
    return v


def _keywords(req: Requirement, el: Element) -> list:
    pats = list(req.topic)
    for alt in el.patterns:
        pats.extend(alt)
    return pats


def candidates_for(req: Requirement, el: Element, segments: list[Segment]) -> list[Segment]:
    """Mọi đoạn có liên quan (khớp ít nhất một từ khóa chủ đề hoặc mẫu), xếp liên quan nhất trước. Không cắt bớt."""
    pats = _keywords(req, el)
    scored = []
    for s in segments:
        score = sum(1 for p in pats if p.search(s.text))
        if score:
            scored.append((score, s))
    scored.sort(key=lambda x: (-x[0], x[1].doc, x[1].index))
    return [s for _, s in scored]


def run_judge(judge: Judge, req: Requirement, el: Element, cands: list[Segment]) -> Verdict:
    """Bộ luật quét một lần toàn bộ; bộ chấm AI chấm theo lô, dừng khi có bằng chứng hợp lệ."""
    if not cands:
        return Verdict(False, reason="không có đoạn liên quan")
    if getattr(judge, "scans_all", False):
        return verify_quote(judge.judge(req, el, cands), {s.ref: s for s in cands})
    last = Verdict(False)
    for i in range(0, len(cands), BATCH):
        batch = cands[i : i + BATCH]
        last = verify_quote(judge.judge(req, el, batch), {s.ref: s for s in batch})
        if last.found:
            return last
    return last


def label(results: list, topic_hits: int) -> str:
    n = sum(1 for e in results if e.found)
    if n == len(results):
        return DAP_UNG
    if n > 0:
        return MOT_PHAN
    return CHUA if topic_hits else KHONG_DU


def assess(
    catalog: Catalog,
    segments: list[Segment],
    judge: Judge,
    second: Judge | None = None,
    not_applicable: dict[str, str] | None = None,
) -> list[RequirementResult]:
    not_applicable = not_applicable or {}
    out: list[RequirementResult] = []
    for req in catalog.requirements:
        if req.id in not_applicable:
            out.append(
                RequirementResult(req, KHONG_AP_DUNG, note=f"Người dùng khai báo: {not_applicable[req.id]}")
            )
            continue
        topic_hits = sum(1 for s in segments if any(p.search(s.text) for p in req.topic))
        results = []
        for el in req.elements:
            cands = candidates_for(req, el, segments)
            v = run_judge(judge, req, el, cands)
            v2 = run_judge(second, req, el, cands) if second is not None else None
            # Một kết quả (có hoặc không) được coi là đã xác nhận khi: bộ chấm chính được tin cậy (bộ luật); hoặc bộ luật
            # chấm song song cho CÙNG kết luận, và với kết luận "có" thì ở CÙNG đoạn. Không có ngoại lệ cho trường hợp bộ
            # lọc từ khóa không tìm ra đoạn nào: bộ lọc đó có thể bỏ sót, nên ở chế độ chỉ dùng AI kết luận "không" vẫn là gợi ý.
            trusted2 = v2 is not None and getattr(second, "trusted", False)
            confirmed = getattr(judge, "trusted", False) or (
                trusted2 and v2.found == v.found and (not v.found or v2.ref == v.ref)
            )
            results.append(ElementResult(el, v.found, v.quote, v.ref, v.reason, confirmed, v2))
        status = label(results, topic_hits)
        notes = []
        unconf_yes = [e.element.id for e in results if e.found and not e.confirmed]
        unconf_no = [e.element.id for e in results if not e.found and not e.confirmed]
        if unconf_yes or unconf_no:
            # Mọi kết quả AI chưa được bộ luật xác nhận là gợi ý: yêu cầu cần người xác nhận, kể cả kết luận âm tính
            status = CAN_XAC_NHAN
            parts = []
            if unconf_yes:
                parts.append("AI báo có bằng chứng, chưa xác nhận: " + ", ".join(unconf_yes))
            if unconf_no:
                parts.append("AI báo không có bằng chứng, chưa xác nhận: " + ", ".join(unconf_no))
            notes.append("cần người xác nhận; " + "; ".join(parts))
        if any(e.disagree for e in results):
            notes.append("hai bộ chấm lệch nhau ở " + ", ".join(e.element.id for e in results if e.disagree))
        out.append(RequirementResult(req, status, results, topic_hits, "; ".join(notes)))
    return out
