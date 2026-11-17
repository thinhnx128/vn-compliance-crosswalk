"""Gói zip tải về phải khớp mẫu nguồn trong kho, và phải mở được.

Gói `toolkits/dlcn/phat-hanh/bo-cong-cu-bao-ve-du-lieu-ca-nhan.zip` được dựng từ các tệp Markdown
trong `toolkits/dlcn/mau/` bằng trình đóng gói nằm ở kho riêng. Vì bước dựng không chạy trong CI,
kho ghi lại mã băm của từng mẫu nguồn tại thời điểm dựng (`phat-hanh/NGUON.txt`). Nếu ai sửa một
mẫu mà quên dựng lại gói, các kiểm tra dưới đây sẽ báo lỗi.
"""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DLCN = ROOT / "toolkits" / "dlcn"
PHAT_HANH = DLCN / "phat-hanh"
ZIP = PHAT_HANH / "bo-cong-cu-bao-ve-du-lieu-ca-nhan.zip"
SUMS = PHAT_HANH / "SHA256SUMS"
NGUON = PHAT_HANH / "NGUON.txt"

TEP_TRONG_GOI = {
    "CHK-DP_Bo_tu_kiem_tra_DLCN.xlsx",
    "DP-00_bao_cao_chan_doan.docx",
    "DP-01_chinh_sach_bao_ve_dlcn.docx",
    "DP-02_thong_bao_xu_ly_dlcn.docx",
    "DP-03_danh_gia_tac_dong.docx",
    "DP-04_quyen_chu_the_du_lieu.docx",
    "DP-05_xu_ly_vi_pham_dlcn.docx",
    "DP-06_thoa_thuan_xu_ly_dlcn.docx",
    "DP-07_mau_dong_y.docx",
    "REG-DP_So_bao_ve_DLCN.xlsx",
    "SP-01_huong_dan_su_dung.docx",
    "SP-02_dieu_khoan_su_dung.docx",
}


def _sha256(duong_dan: Path) -> str:
    return hashlib.sha256(duong_dan.read_bytes()).hexdigest()


def _sha256_van_ban(duong_dan: Path) -> str:
    """Mã băm của tệp văn bản, **không phụ thuộc kiểu xuống dòng**.

    Kho đặt `core.autocrlf=true` nên cùng một tệp có thể nằm trên đĩa dưới dạng CRLF ở máy Windows
    và LF trong CI chạy Linux. Băm thẳng byte trên đĩa sẽ cho hai kết quả khác nhau, nên phải bỏ
    dấu thứ tự byte và đưa mọi xuống dòng về LF trước khi băm.
    """
    du_lieu = duong_dan.read_bytes()
    if du_lieu.startswith(b"\xef\xbb\xbf"):
        du_lieu = du_lieu[3:]
    du_lieu = du_lieu.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(du_lieu).hexdigest()


def _doc_nguon() -> dict[str, str]:
    """Đọc NGUON.txt thành {đường dẫn tương đối: mã băm}."""
    ket_qua: dict[str, str] = {}
    for dong in NGUON.read_text(encoding="utf-8").splitlines():
        dong = dong.strip()
        if not dong or dong.startswith("#"):
            continue
        ma_bam, _, ten = dong.partition("  ")
        ket_qua[ten.strip()] = ma_bam.strip()
    return ket_qua


def test_ma_bam_goi_khop_sha256sums() -> None:
    """SHA256SUMS phải khớp gói zip đang nằm trong kho."""
    ghi_nhan = SUMS.read_text(encoding="utf-8").split()[0]
    assert ghi_nhan == _sha256(ZIP), "SHA256SUMS không khớp gói zip — dựng lại gói hoặc cập nhật SHA256SUMS"


def test_goi_dung_12_tep() -> None:
    """Gói phải gồm đúng 12 tệp, nằm ở gốc gói, không có thư mục con."""
    with zipfile.ZipFile(ZIP) as z:
        ten = [t.filename for t in z.infolist() if not t.is_dir()]
    assert set(ten) == TEP_TRONG_GOI
    assert all("/" not in t for t in ten), "tệp trong gói phải nằm ở gốc"


def test_mau_nguon_khong_doi_ke_tu_lan_dung_goi() -> None:
    """Mẫu trong `mau/` phải đúng bản đã dùng để dựng gói.

    Đây là chốt chặn chính: sửa mẫu mà quên dựng lại gói thì người tải về nhận tài liệu cũ.
    """
    ghi_nhan = _doc_nguon()
    hien_tai = {
        f"mau/{p.name}": _sha256_van_ban(p) for p in sorted((DLCN / "mau").glob("*.md"))
    }
    assert set(ghi_nhan) == set(hien_tai), (
        "danh sách mẫu đổi so với NGUON.txt — dựng lại gói rồi cập nhật NGUON.txt"
    )
    lech = sorted(t for t in hien_tai if hien_tai[t] != ghi_nhan[t])
    assert not lech, (
        f"mẫu đã sửa nhưng gói chưa dựng lại: {', '.join(lech)}. "
        "Dựng lại gói, rồi cập nhật NGUON.txt và SHA256SUMS."
    )


MAU_UNG_VOI_TEP = {
    "mau/DP-00_bao_cao_chan_doan.md": "DP-00_bao_cao_chan_doan.docx",
    "mau/DP-01_chinh_sach_bao_ve_dlcn.md": "DP-01_chinh_sach_bao_ve_dlcn.docx",
    "mau/DP-02_thong_bao_xu_ly_dlcn.md": "DP-02_thong_bao_xu_ly_dlcn.docx",
    "mau/DP-03_danh_gia_tac_dong.md": "DP-03_danh_gia_tac_dong.docx",
    "mau/DP-04_quyen_chu_the_du_lieu.md": "DP-04_quyen_chu_the_du_lieu.docx",
    "mau/DP-05_xu_ly_vi_pham_dlcn.md": "DP-05_xu_ly_vi_pham_dlcn.docx",
    "mau/DP-06_thoa_thuan_xu_ly_dlcn.md": "DP-06_thoa_thuan_xu_ly_dlcn.docx",
    "mau/DP-07_mau_dong_y.md": "DP-07_mau_dong_y.docx",
    "mau/SP-01_huong_dan_su_dung.md": "SP-01_huong_dan_su_dung.docx",
    "mau/SP-02_dieu_khoan_su_dung.md": "SP-02_dieu_khoan_su_dung.docx",
}


def _chuan_hoa(van_ban: str) -> str:
    """Bỏ cách đánh dấu của Markdown và gộp khoảng trắng, để so câu chữ với bản Word."""
    import re

    van_ban = van_ban.replace("**", "").replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", van_ban).strip()


def _cau_dac_trung(duong_dan: Path, so_cau: int = 3) -> list[str]:
    """Vài câu văn xuôi đủ dài trong mẫu, dùng để nhận ra bản Word có đúng mẫu này không.

    Bỏ qua dòng hướng dẫn nội bộ, dòng bảng, tiêu đề, và dòng có ô thay thế `{{...}}` hoặc `[●`,
    vì trình đóng gói biến đổi những dòng đó.
    """
    ra: list[str] = []
    cac_dong = duong_dan.read_text(encoding="utf-8").splitlines()

    # Bỏ khối front-matter YAML ở đầu tệp: trình đóng gói dựng nó thành bảng thông tin tài liệu,
    # không giữ nguyên câu chữ, nên không dùng để đối chiếu được.
    if cac_dong and cac_dong[0].strip() == "---":
        for vi_tri, dong in enumerate(cac_dong[1:], start=1):
            if dong.strip() == "---":
                cac_dong = cac_dong[vi_tri + 1 :]
                break

    import re as _re

    for dong in cac_dong:
        dong = dong.strip()
        if not dong or dong.startswith(("#", "|", ">", "---")) or "{{" in dong or "[●" in dong:
            continue
        # Dòng danh sách vẫn dùng được: bỏ dấu đầu dòng, giữ lại câu chữ.
        dong = _re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", dong)
        cau = _chuan_hoa(dong)
        if len(cau) >= 60:
            ra.append(cau)
        if len(ra) >= so_cau:
            break
    return ra


def _van_ban_trong_docx(du_lieu: bytes) -> str:
    import io
    import re
    import xml.etree.ElementTree as ET

    with zipfile.ZipFile(io.BytesIO(du_lieu)) as tep:
        xml = tep.read("word/document.xml").decode("utf-8")
    goc = ET.fromstring(xml)

    # Trong một đoạn, các đoạn chữ (w:t) phải nối liền nhau vì Word hay cắt một từ thành nhiều
    # đoạn; giữa hai đoạn văn thì chèn dấu cách, nếu không câu cuối đoạn trên sẽ dính câu đầu
    # đoạn dưới.
    cac_doan = []
    for doan in goc.iter():
        if doan.tag.endswith("}p"):
            cac_doan.append("".join(n.text or "" for n in doan.iter() if n.tag.endswith("}t")))
    return re.sub(r"\s+", " ", _chuan_hoa(" ".join(cac_doan)))


@pytest.mark.parametrize("ten_mau,ten_docx", sorted(MAU_UNG_VOI_TEP.items()))
def test_noi_dung_trong_goi_dung_mau_hien_tai(ten_mau: str, ten_docx: str) -> None:
    """Nối gói với mẫu: câu chữ của mẫu phải có thật trong tệp Word tương ứng trong gói.

    `NGUON.txt` chỉ chứng minh `mau/` không đổi kể từ lần dựng; nó **không** chứng minh gói được
    dựng từ chính các mẫu đó. Nếu ai cập nhật mẫu và `NGUON.txt` nhưng quên dựng lại gói thì các
    kiểm tra kia vẫn xanh. Kiểm tra này đọc thẳng câu chữ bên trong tệp Word nên bắt được ca đó.
    """
    duong_dan_mau = DLCN / ten_mau
    cau_can_co = _cau_dac_trung(duong_dan_mau)
    assert cau_can_co, f"{ten_mau}: không lấy được câu đặc trưng nào để đối chiếu"

    with zipfile.ZipFile(ZIP) as goi:
        van_ban = _van_ban_trong_docx(goi.read(ten_docx))

    thieu = [c for c in cau_can_co if c not in van_ban]
    assert not thieu, (
        f"{ten_docx} trong gói không chứa câu chữ của {ten_mau} — gói nhiều khả năng là bản cũ. "
        f"Dựng lại gói. Câu thiếu: {thieu[0][:120]}"
    )


@pytest.mark.parametrize("ten_tep", sorted(TEP_TRONG_GOI))
def test_tep_office_mo_duoc(ten_tep: str) -> None:
    """Mỗi tệp Word, Excel trong gói phải là OOXML hợp lệ và tự đủ.

    Kiểm: mở được như zip, có `[Content_Types].xml`, có phần chính, và mọi quan hệ trong các tệp
    `.rels` đều trỏ tới một phần có thật trong gói.
    """
    import re
    import xml.etree.ElementTree as ET

    with zipfile.ZipFile(ZIP) as goi:
        du_lieu = goi.read(ten_tep)

    import io

    with zipfile.ZipFile(io.BytesIO(du_lieu)) as tep:
        hong = tep.testzip()
        assert hong is None, f"{ten_tep}: phần hỏng {hong}"
        cac_phan = set(tep.namelist())
        assert "[Content_Types].xml" in cac_phan
        phan_chinh = "word/document.xml" if ten_tep.endswith(".docx") else "xl/workbook.xml"
        assert phan_chinh in cac_phan, f"{ten_tep}: thiếu {phan_chinh}"

        for ten_phan in cac_phan:
            if ten_phan.endswith(".xml") or ten_phan.endswith(".rels"):
                ET.fromstring(tep.read(ten_phan))  # XML phải phân tích được

        for ten_rels in (p for p in cac_phan if p.endswith(".rels")):
            thu_muc = re.sub(r"_rels/[^/]+$", "", ten_rels)
            goc = ET.fromstring(tep.read(ten_rels))
            for quan_he in goc:
                dich = quan_he.get("Target", "")
                if quan_he.get("TargetMode") == "External" or dich.startswith(("http", "mailto:")):
                    continue
                duong_dan = (thu_muc + dich).replace("/./", "/")
                while "/../" in duong_dan:
                    duong_dan = re.sub(r"[^/]+/\.\./", "", duong_dan, count=1)
                duong_dan = duong_dan.lstrip("/")
                assert duong_dan in cac_phan, f"{ten_tep}: {ten_rels} trỏ tới phần không có: {dich}"
