"""Đo độ chính xác của bộ chấm trên một bộ văn bản có nhãn theo từng yếu tố.

python -m vncc.ra_soat.danh_gia <thư mục văn bản> <tệp nhãn .json> [--bo-cham luat|ai]

Chỉ số quan trọng nhất: số "có bằng chứng" sai (dương tính giả), vì nó dẫn tới báo "Đáp ứng" sai.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

from . import catalog as cat
from .engine import assess, label
from .judges import AnthropicJudge, JudgeError, RuleJudge
from .loader import read_folder


def evaluate(folder: Path, labels_path: Path, judge) -> dict:
    labels = json.loads(Path(labels_path).read_text(encoding="utf-8"))
    nhan, mo_ho = labels["nhan"], set(labels.get("mo_ho", []))
    results = assess(cat.load(), read_folder(Path(folder)), judge)
    tp = fp = fn = tn = 0
    errors, req_match, req_total = [], 0, 0
    for r in results:
        exp = nhan.get(r.req.id)
        if exp is None:
            continue
        for e in r.elements:
            want = exp[e.element.id]
            got = e.found
            key = f"{r.req.id}.{e.element.id}"
            if got and want:
                tp += 1
            elif got and not want:
                fp += 1
                errors.append(("DƯƠNG TÍNH GIẢ", key, e.ref, e.quote[:120], key in mo_ho))
            elif not got and want:
                fn += 1
                errors.append(("ÂM TÍNH GIẢ", key, "", e.element.text, key in mo_ho))
            else:
                tn += 1
        # nhãn yêu cầu kỳ vọng tính theo cùng quy tắc, với nhãn yếu tố của người
        exp_label = label([SimpleNamespace(found=exp[e.element.id]) for e in r.elements], r.topic_hits)
        req_total += 1
        req_match += exp_label == r.status
    n = tp + fp + fn + tn
    return {
        "yeu_to": n,
        "dung": tp + tn,
        "do_chinh_xac": round((tp + tn) / n, 3) if n else 0,
        "duong_tinh_gia": fp,
        "am_tinh_gia": fn,
        "do_chinh_xac_khi_bao_co": round(tp / (tp + fp), 3) if tp + fp else None,
        "do_phu": round(tp / (tp + fn), 3) if tp + fn else None,
        "nhan_yeu_cau_khop": f"{req_match}/{req_total}",
        "loi": errors,
    }


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    folder, labels = Path(args[0]), Path(args[1])
    use_ai = (
        "--bo-cham" in args
        and args.index("--bo-cham") + 1 < len(args)
        and args[args.index("--bo-cham") + 1] == "ai"
    )
    try:
        judge = AnthropicJudge() if use_ai else RuleJudge()
        res = evaluate(folder, labels, judge)
    except JudgeError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    for k, v in res.items():
        if k != "loi":
            print(f"{k}: {v}")
    print("Lỗi:")
    for kind, key, ref, txt, amb in res["loi"]:
        print(f"  {kind} {key}{' (mơ hồ)' if amb else ''} {ref} {txt}")
    if hasattr(judge, "calls"):
        print(
            f"Model: {judge.model}, effort {judge.effort}; lượt gọi: {judge.calls}; "
            f"token vào: {judge.input_tokens}; token ra: {judge.output_tokens}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
