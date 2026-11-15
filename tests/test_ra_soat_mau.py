"""Vòng khép kín "rà -> mẫu để lấp -> rà lại": bộ mẫu DP-01..07 của dự án phải tự đạt trên công cụ của dự án."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from vncc.ra_soat import catalog as cat
from vncc.ra_soat.engine import DAP_UNG, assess
from vncc.ra_soat.judges import RuleJudge
from vncc.ra_soat.loader import Segment, read_folder
from vncc.ra_soat.report import to_markdown

ROOT = Path(__file__).resolve().parent.parent
MAU_JSON = ROOT / "catalogs" / "ra-soat" / "vn-pdp-2025.mau.json"


def _mau() -> dict:
    return json.loads(MAU_JSON.read_text(encoding="utf-8"))


def _mau_segments() -> list[Segment]:
    d = _mau()
    folder = ROOT / d["thu_muc_mau"]
    names = set(d["mau"].values())
    return [s for s in read_folder(folder) if s.doc in names]


def test_moi_yeu_cau_deu_co_anh_xa_toi_mau():
    ids = {r.id for r in cat.load().requirements}
    assert set(_mau()["requirements"]) == ids
    assert all(r.mau for r in cat.load().requirements)


def test_tep_mau_va_tieu_de_trong_anh_xa_co_that():
    d = _mau()
    folder = ROOT / d["thu_muc_mau"]
    headings: dict[str, set[str]] = {}
    for code, name in d["mau"].items():
        path = folder / name
        assert path.is_file(), name
        headings[code] = {
            re.sub(r"^#+\s*", "", line).strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("#")
        }
    for rid, items in d["requirements"].items():
        for x in items:
            assert x["muc"] in headings[x["mau"]], f'{rid}: {x["mau"]} không có mục "{x["muc"]}"'


def test_bo_mau_cua_du_an_tu_dat_tren_cong_cu_cua_du_an():
    res = assess(cat.load(), _mau_segments(), RuleJudge())
    chua_dat = {r.req.id: [e.element.id for e in r.missing] for r in res if r.status != DAP_UNG}
    assert not chua_dat, f"Bộ mẫu chưa đạt: {chua_dat}"


def test_bao_cao_chi_thang_mau_de_lap_khoang_trong():
    catalog = cat.load()
    seg = Segment("a.md", 1, "", "Văn bản này chỉ nói về quy định nghỉ phép của người lao động trong năm.")
    md = to_markdown(catalog, assess(catalog, [seg], RuleJudge()), "a", "luat", "2026-11-15")
    assert 'Mẫu tham khảo để lấp: DP-01, mục "9.2 Dữ liệu của ứng viên và người lao động (Luật Điều 25)"' in md


def test_bo_luat_bo_qua_tieu_de_qua_ngan_va_xet_doan_tiep_theo():
    """Lỗi cũ: tiêu đề ngắn khớp mẫu trước, trích dẫn bị loại vì quá ngắn, nên đoạn văn đủ bằng chứng bên dưới bị bỏ."""
    catalog = cat.load()
    segs = [
        Segment("a.md", 1, "Diễn tập", "# Diễn tập"),
        Segment("a.md", 2, "Diễn tập", "Diễn tập quy trình xử lý vi phạm ít nhất mỗi năm một lần bằng tình huống giả định."),
    ]
    r19 = next(r for r in assess(catalog, segs, RuleJudge()) if r.req.id == "VN-PDP-19")
    e4 = next(e for e in r19.elements if e.element.id == "e4")
    assert e4.found and e4.ref == "a.md#2"


def test_anh_xa_sai_ma_bi_tu_choi(tmp_path):
    d = _mau()
    d["requirements"]["VN-PDP-99"] = [{"mau": "DP-01", "muc": "x"}]
    bad = tmp_path / "mau.json"
    bad.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="không tồn tại"):
        cat.load(mau_path=bad)
    d = _mau()
    d["requirements"]["VN-PDP-01"] = [{"mau": "DP-99", "muc": "x"}]
    bad.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="DP-99"):
        cat.load(mau_path=bad)


def test_thieu_tep_anh_xa_thi_bao_cao_van_chay(tmp_path):
    catalog = cat.load(mau_path=tmp_path / "khong-co.json")
    assert all(not r.mau for r in catalog.requirements)
