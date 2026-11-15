"""Kiểm thử bổ sung cho các nguyên tắc an toàn của `vncc ra-soat` (theo rà soát trước khi phát hành)."""

from __future__ import annotations

import json

import pytest

from vncc.ra_soat import catalog as cat
from vncc.ra_soat.engine import CAN_XAC_NHAN, assess
from vncc.ra_soat.judges import AnthropicJudge, JudgeError, Verdict
from vncc.ra_soat.loader import Segment
from vncc.ra_soat.report import to_csv

SEG = Segment("a.md", 1, "", "Mọi tài khoản quản trị bắt buộc dùng xác thực đa yếu tố khi đăng nhập từ xa.")


class AiChiThayMotYeuTo:
    """Giả lập AI chỉ thấy bằng chứng cho đúng một yếu tố (e2 của VN-PDP-16), không được tin cậy."""

    name = "gia-lap"
    trusted = False
    scans_all = False

    def judge(self, req, el, candidates):
        if req.id == "VN-PDP-16" and el.id == "e2" and candidates:
            return Verdict(True, candidates[0].text, candidates[0].ref)
        return Verdict(False)


def test_mot_phan_co_bang_chung_chi_do_ai_cung_can_nguoi_xac_nhan():
    catalog = cat.load()
    res = assess(catalog, [SEG], AiChiThayMotYeuTo())
    r16 = next(r for r in res if r.req.id == "VN-PDP-16")
    assert r16.status == CAN_XAC_NHAN
    assert "AI báo có bằng chứng, chưa xác nhận: e2" in r16.note
    # các yếu tố còn lại: AI báo "không" và không có bộ luật xác nhận, nên cũng là gợi ý; yêu cầu vẫn xếp như khoảng trống
    assert "AI báo không có bằng chứng, chưa xác nhận" in r16.note
    assert r16.missing and r16.priority > 1


def test_ket_luan_am_tinh_cua_ai_cung_la_goi_y():
    from vncc.ra_soat.judges import RuleJudge

    class AiLuonKhong:
        name = "gia-lap"
        trusted = False
        scans_all = False

        def judge(self, req, el, candidates):
            return Verdict(False, reason="không thấy")

    catalog = cat.load()
    only_ai = assess(catalog, [SEG], AiLuonKhong())
    assert all(r.status == CAN_XAC_NHAN for r in only_ai if any(e.element for e in r.elements) and r.topic_hits)
    # có bộ luật chấm song song và đồng ý "không" thì kết luận âm tính được xác nhận
    both = assess(catalog, [Segment("b.md", 1, "", "Nội dung không liên quan tới chủ đề nào của danh mục.")],
                  AiLuonKhong(), second=RuleJudge())
    assert not any(r.status == CAN_XAC_NHAN for r in both)


def test_csv_chan_ky_tu_dieu_khien_bat_ky_truoc_cong_thuc():
    catalog = cat.load()
    seg = Segment("a.md", 1, "", chr(1) + "=HYPERLINK(1) phân quyền truy cập theo vai trò")
    assert ("'" + chr(1) + "=HYPERLINK") in to_csv(assess(catalog, [seg], _RuleLike()))


class _Resp:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


@pytest.mark.parametrize("payload, msg", [
    ({"stop_reason": "end_turn"}, "sai cấu trúc"),
    ({"content": "không phải danh sách"}, "sai cấu trúc"),
    (["không phải đối tượng"], "sai cấu trúc"),
    ({"stop_reason": "max_tokens", "content": [{"type": "text", "text": '{"co": tr'}]}, "bị cắt"),
])
def test_phan_hoi_api_bat_thuong_lam_dung_lan_ra(monkeypatch, payload, msg):
    j = AnthropicJudge(api_key="khoa-gia-dung-cho-kiem-thu")
    r = cat.load().requirements[0]
    monkeypatch.setattr("urllib.request.urlopen", lambda rq, timeout: _Resp(payload))
    with pytest.raises(JudgeError, match=msg):
        j.judge(r, r.elements[0], [SEG])


def test_csv_chan_cong_thuc_sau_khoang_trang_va_ky_tu_dieu_khien():
    catalog = cat.load()
    for prefix in (" ", chr(9), chr(11) + chr(12), chr(0)):
        seg = Segment("a.md", 1, "", prefix + "=HYPERLINK(1) phân quyền truy cập theo vai trò")
        csv_text = to_csv(assess(catalog, [seg], _RuleLike()))
        kept = prefix.replace(chr(0), "")  # ký tự NUL bị bỏ (Python 3.10 không ghi được NUL vào CSV)
        assert ("'" + kept + "=HYPERLINK") in csv_text, repr(prefix)
        assert chr(0) not in csv_text


def test_tai_lieu_chua_ky_tu_nul_van_doc_va_xuat_duoc(tmp_path):
    from vncc.ra_soat.judges import RuleJudge
    from vncc.ra_soat.loader import read_folder

    (tmp_path / "a.md").write_text("Phân quyền" + chr(0) + " truy cập theo vai trò công việc." + chr(10), encoding="utf-8")
    segs = read_folder(tmp_path)
    assert segs and chr(0) not in segs[0].text
    assert chr(0) not in to_csv(assess(cat.load(), segs, RuleJudge()))


class _RuleLike:
    """Bộ chấm luôn trích nguyên văn đoạn đầu tiên và được tin cậy (để trích dẫn đi vào CSV)."""

    name = "gia-lap-luat"
    trusted = True
    scans_all = True

    def judge(self, req, el, candidates):
        return Verdict(True, candidates[0].text, candidates[0].ref) if candidates else Verdict(False)
