"""Phát hiện chồng chéo, xung đột tham số định lượng giữa các văn bản.

Với mỗi chủ đề tham số (parameters/topics.yaml), gom mọi tham số từ mọi danh mục rồi phân loại:

* ``khac-thoi-han``: cùng chủ đề nhưng thời hạn khác nhau giữa các văn bản.
* ``khac-noi-nhan``: cùng chủ đề, cùng thời hạn nhưng gửi tới nơi nhận khác nhau
  (một sự kiện có thể phát sinh nhiều nghĩa vụ song song).
* ``chua-doi-chieu``: có tham số chưa đối chiếu được toàn văn.

Mức chặt nhất (strictest) = thời hạn ngắn nhất sau khi quy đổi sang giờ; đây là gợi ý cho SLA nội bộ
khi một sự kiện thuộc phạm vi nhiều văn bản. Ngày làm việc được quy đổi như ngày lịch (cận dưới),
nên khi so sánh với đơn vị ngày lịch kết quả chỉ mang tính gần đúng.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .repository import ParamRef, Repository

FLAG_LABELS = {
    "khac-thoi-han": "Thời hạn khác nhau giữa các văn bản",
    "khac-noi-nhan": "Cùng thời hạn nhưng khác nơi nhận - phát sinh nghĩa vụ song song",
    "chua-doi-chieu": "Có tham số chưa đối chiếu toàn văn",
}


@dataclass
class TopicFinding:
    topic_id: str
    title: str
    refs: list[ParamRef]
    flags: list[str] = field(default_factory=list)
    strictest: ParamRef | None = None

    @property
    def catalogs(self) -> list[str]:
        return sorted({r.catalog.id for r in self.refs})

    @property
    def is_conflict(self) -> bool:
        return len(self.catalogs) > 1 and any(f in self.flags for f in ("khac-thoi-han", "khac-noi-nhan"))


def analyze(repo: Repository) -> list[TopicFinding]:
    findings: list[TopicFinding] = []
    for topic_id, topic in repo.topics.items():
        refs = repo.params(topic_id)
        if not refs:
            continue
        f = TopicFinding(topic_id, topic.title, refs)
        timed = [r for r in refs if r.param.hours is not None]
        if timed:
            f.strictest = min(timed, key=lambda r: (r.param.hours, r.catalog.id))
        if len({r.catalog.id for r in refs}) > 1:
            values = {(r.param.value, r.param.unit) for r in refs}
            if len(values) > 1:
                f.flags.append("khac-thoi-han")
            recipients = {r.param.recipient for r in refs if r.param.recipient}
            if len(recipients) > 1:
                f.flags.append("khac-noi-nhan")
        if any(not r.param.verified for r in refs):
            f.flags.append("chua-doi-chieu")
        findings.append(f)
    findings.sort(key=lambda x: (not x.is_conflict, x.topic_id))
    return findings


def _src(ref: ParamRef) -> str:
    doc = ref.catalog.document_number or ref.catalog.id
    return f"{doc} {ref.param.source or ref.control.id}"


def conflicts_markdown(repo: Repository) -> str:
    findings = analyze(repo)
    conflicts = [f for f in findings if f.is_conflict]
    lines = [
        "# Chồng chéo tham số định lượng giữa các văn bản",
        "",
        f"- Văn bản có tham số: {', '.join(sorted({r.catalog.id for f in findings for r in f.refs}))}",
        f"- Chủ đề có tham số: {len(findings)}; chủ đề có chồng chéo giữa văn bản: {len(conflicts)}",
        "- Quy tắc: so sánh tham số cùng chủ đề; mức chặt nhất là thời hạn ngắn nhất sau quy đổi ra giờ "
        "(ngày làm việc tính như ngày lịch, gần đúng).",
        "",
    ]
    if conflicts:
        lines += ["## I. Chồng chéo cần xử lý", ""]
        for f in conflicts:
            lines += _topic_block(f)
    others = [f for f in findings if not f.is_conflict]
    if others:
        lines += ["## II. Các chủ đề còn lại", ""]
        for f in others:
            lines += _topic_block(f)
    lines += [
        "---",
        "*Diễn giải chuyên môn từ dữ liệu của dự án, không phải ý kiến pháp lý. Kiểm tra văn bản gốc "
        "trước khi áp dụng.*",
        "",
    ]
    return "\n".join(lines)


def _topic_block(f: TopicFinding) -> list[str]:
    out = [f"### {f.title} (`{f.topic_id}`)", ""]
    for flag in f.flags:
        out.append(f"> **{FLAG_LABELS[flag]}**")
    if f.flags:
        out.append("")
    out += [
        "| Văn bản, điều khoản | Thời hạn | Mốc tính | Nơi nhận | Phạm vi | Đã đối chiếu |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(
        f.refs, key=lambda x: (x.param.hours if x.param.hours is not None else 10**9, x.catalog.id)
    ):
        p = r.param
        out.append(
            f"| {_src(r)} | {p.label()} | {p.trigger or '-'} | {p.recipient or '-'} | {p.scope or '-'} "
            f"| {'Có' if p.verified else 'Chưa'} |"
        )
    if f.strictest and len(f.catalogs) > 1:
        s = f.strictest
        out += [
            "",
            f"**Gợi ý SLA nội bộ:** khi một sự kiện thuộc phạm vi nhiều văn bản, lấy mức chặt nhất "
            f"**{s.param.label()}** ({_src(s)}) làm mốc chung, đồng thời gửi đủ các nơi nhận nêu trên.",
        ]
    out.append("")
    return out
