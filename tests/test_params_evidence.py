import pytest
from openpyxl import load_workbook
from pydantic import ValidationError
from typer.testing import CliRunner

from vncc.cli import app
from vncc.conflicts import analyze, conflicts_markdown
from vncc.export import export_xlsx
from vncc.models import Param
from vncc.reports import evidence_markdown, gap_markdown
from vncc.repository import Repository, load_file

from .test_vncc import EXAMPLE

runner = CliRunner()


@pytest.fixture(scope="module")
def repo():
    return Repository.load()


# ------------------------------------------------------------------ tham số
def test_param_validation_and_label():
    assert Param(topic="x", value=24, unit="hour").label() == "24 giờ"
    assert Param(topic="x", value="12-25", unit="date").label() == "trước ngày 25/12"
    assert Param(topic="x", value=2, unit="working_day").hours == 48
    with pytest.raises(ValidationError):
        Param(topic="x", value="25/12", unit="date")
    with pytest.raises(ValidationError):
        Param(topic="x", value="24", unit="hour")


def test_all_params_have_declared_topics(repo):
    assert repo.validate() == []
    assert len(repo.params()) >= 20


def test_incident_notification_conflict(repo):
    f = {x.topic_id: x for x in analyze(repo)}["su-co-thong-bao-co-quan"]
    assert f.is_conflict
    assert {"khac-thoi-han", "khac-noi-nhan"} <= set(f.flags)
    assert {"nd331-2026", "luat91-2025"} <= set(f.catalogs)
    assert f.strictest.catalog.id == "nd331-2026" and f.strictest.param.value == 24


def test_unverified_params_flagged(repo):
    f = {x.topic_id: x for x in analyze(repo)}["bao-cao-dinh-ky-co-quan"]
    assert "chua-doi-chieu" in f.flags and not f.is_conflict


def test_conflicts_markdown(repo):
    md = conflicts_markdown(repo)
    assert md.index("## I. Chồng chéo cần xử lý") < md.index("su-co-thong-bao-co-quan")
    assert "Gợi ý SLA nội bộ" in md and "**24 giờ**" in md


# ------------------------------------------------------------------ bằng chứng
@pytest.mark.parametrize("catalog_id", ["nd331-2026", "iso27001-2022"])
def test_evidence_covers_every_control(repo, catalog_id):
    missing = [
        c.id for _, c in repo.catalog(catalog_id).controls() if not repo.evidence_for(catalog_id, c.id)
    ]
    assert missing == []


def test_evidence_reference_errors_detected(tmp_path):
    d = tmp_path / "evidence"
    d.mkdir()
    (d / "bad.yaml").write_text(
        "kind: evidence\nid: bad\ncatalog: nd331-2026\nversion: '0'\nstatus: draft\n"
        "items:\n  D99: [{name: 'không tồn tại'}]\n",
        encoding="utf-8",
    )
    assert any("D99" in e for e in Repository.load(tmp_path).validate())


def test_evidence_markdown_level_filter(repo):
    md2 = evidence_markdown(repo, "nd331-2026", level=2)
    assert "- [ ] Quy trình quản lý sự cố có mốc thông báo 24 giờ" in md2
    assert "D30.K8" not in md2  # chỉ áp dụng cấp độ 3–4
    assert "Thời hạn: 24 giờ" in md2


def test_gap_report_lists_evidence():
    repo = Repository.load(EXAMPLE)
    md = gap_markdown(repo, load_file(EXAMPLE / "assessment-nd331-cap-do-2.yaml"))
    assert "Bằng chứng cần có" in md
    assert "Sổ theo dõi sự cố" in md


def test_excel_pack_has_evidence_and_conflicts(tmp_path, repo):
    wb = load_workbook(export_xlsx(repo, "iso27001-2022__nd331-2026", tmp_path / "p.xlsx"))
    sa = wb["Tự đánh giá"]
    head = [c.value for c in sa[16]]
    assert "Bằng chứng gợi ý" in head and "Thời hạn, tham số" in head
    tx = wb["Thời hạn & chồng chéo"]
    notes = [r[8] for r in tx.iter_rows(min_row=5, values_only=True)]
    assert any(n and n.startswith("Mức chặt nhất") for n in notes)


def test_cli_commands():
    res = runner.invoke(app, ["conflicts"])
    assert res.exit_code == 0 and "su-co-thong-bao-co-quan" in res.output
    res = runner.invoke(app, ["evidence", "iso27001-2022"])
    assert res.exit_code == 0 and "- [ ]" in res.output
    res = runner.invoke(app, ["show", "nd331-2026", "D31.K2.d"])
    assert "Thời hạn: 24 giờ" in res.output and "Bằng chứng:" in res.output
