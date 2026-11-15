"""Đọc bộ văn bản của tổ chức thành các đoạn có vị trí.

Hỗ trợ .md, .txt, .docx (đọc thẳng XML trong tệp, không cần thư viện ngoài).
Mỗi đoạn là một dòng có nội dung (đoạn văn, mục danh sách, dòng bảng, tiêu đề) kèm tên tệp, số thứ tự và tiêu đề gần nhất.
"""

from __future__ import annotations

import re
import unicodedata
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

SUPPORTED = {".md", ".txt", ".docx"}
_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


@dataclass(frozen=True)
class Segment:
    doc: str  # tên tệp tương đối
    index: int  # số thứ tự đoạn trong tệp, bắt đầu từ 1
    heading: str  # tiêu đề gần nhất phía trên
    text: str  # nội dung gốc (đã chuẩn hóa Unicode NFC)

    @property
    def ref(self) -> str:
        return f"{self.doc}#{self.index}"


def normalize(s: str) -> str:
    """Chuẩn hóa để so khớp trích dẫn: NFC, gộp khoảng trắng, bỏ khoảng trắng hai đầu."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()


def _docx_paragraphs(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    out = []
    for p in root.iter(f"{_W}p"):
        texts = [t.text or "" for t in p.iter(f"{_W}t")]
        line = "".join(texts)
        style = p.find(f"{_W}pPr/{_W}pStyle")
        if style is not None and style.get(f"{_W}val", "").lower().startswith("heading"):
            line = "# " + line
        out.append(line)
    return out


def _strip_front_matter(lines: list[str]) -> list[str]:
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[i + 1 :]
    return lines


def read_document(path: Path, root: Path) -> list[Segment]:
    ext = path.suffix.lower()
    if ext == ".docx":
        lines = _docx_paragraphs(path)
    else:
        lines = _strip_front_matter(path.read_text(encoding="utf-8-sig").splitlines())
    name = path.relative_to(root).as_posix()
    segs: list[Segment] = []
    heading = ""
    idx = 0
    for raw in lines:
        text = unicodedata.normalize("NFC", raw.replace("\x00", "")).strip()  # bỏ ký tự NUL
        if not text or re.fullmatch(r"\|?[\s:|-]+\|?", text):  # dòng trống, dòng kẻ bảng
            continue
        idx += 1
        if text.startswith("#"):
            heading = text.lstrip("#").strip()
        segs.append(Segment(name, idx, heading, text))
    return segs


def read_folder(folder: Path) -> list[Segment]:
    folder = Path(folder).resolve()
    if folder.is_file():
        return read_document(folder, folder.parent)
    segs: list[Segment] = []
    for p in sorted(folder.rglob("*")):
        if p.is_file() and p.suffix.lower() in SUPPORTED and not p.name.startswith((".", "~$")):
            segs.extend(read_document(p, folder))
    return segs
