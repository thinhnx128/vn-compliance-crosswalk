"""Giao diện dòng lệnh `vncc`."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from . import __version__
from .models import MODELS, Assessment
from .reports import assessment_template, coverage_markdown, gap_markdown, write_soa
from .repository import DataError, Repository, load_file

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Đối chiếu ISO/IEC 27001 với quy định Việt Nam; sinh SoA và báo cáo khoảng cách.",
)

DataDirs = typer.Option(
    None, "--data-dir", "-d", help="Thư mục dữ liệu bổ sung (có catalogs/, mappings/). Lặp được."
)
Related = typer.Option(None, "--related", "-r", help="Chỉ hiển thị đối chiếu tới danh mục này. Lặp được.")
Level = typer.Option(
    None, "--level", "-l", min=1, max=5, help="Cấp độ HTTT (1–5): chỉ lấy yêu cầu áp dụng cho cấp độ này."
)


def _repo(dirs: list[Path] | None) -> Repository:
    try:
        return Repository.load(*(dirs or []))
    except DataError as exc:
        typer.secho(str(exc), fg="red", err=True)
        raise typer.Exit(2) from exc


def _assessment(path: Path) -> Assessment:
    try:
        obj = load_file(path)
    except DataError as exc:
        typer.secho(str(exc), fg="red", err=True)
        raise typer.Exit(2) from exc
    if not isinstance(obj, Assessment):
        typer.secho(f"{path}: không phải hồ sơ đánh giá (kind: assessment)", fg="red", err=True)
        raise typer.Exit(2)
    return obj


@app.command("list")
def list_(data_dir: list[Path] | None = DataDirs) -> None:
    """Liệt kê danh mục và bảng đối chiếu đang có."""
    repo = _repo(data_dir)
    typer.echo("Danh mục:")
    for c in repo.catalogs.values():
        n = sum(1 for _ in c.controls())
        typer.echo(f"  {c.id:<20} {c.status:<9} {n:>4} mục  {c.title}")
    typer.echo("Bảng đối chiếu:")
    for m in repo.mappings.values():
        typer.echo(f"  {m.id:<36} {m.status:<9} {len(m.entries):>4} dòng")


@app.command()
def show(
    catalog: str,
    control: str,
    data_dir: list[Path] | None = DataDirs,
    related: list[str] | None = Related,
) -> None:
    """Xem một control và các yêu cầu liên quan ở danh mục khác."""
    repo = _repo(data_dir)
    try:
        ctl = repo.catalog(catalog).index()[control]
    except (DataError, KeyError) as exc:
        typer.secho(f"Không tìm thấy {catalog}:{control}", fg="red", err=True)
        raise typer.Exit(1) from exc
    typer.echo(f"{catalog}:{ctl.id}  {ctl.title}" + (f"  ({ctl.title_en})" if ctl.title_en else ""))
    items = repo.related(catalog, control, set(related) if related else None)
    if not items:
        typer.echo("  (chưa có đối chiếu)")
    for r in items:
        typer.echo(f"  -> {r.catalog}:{r.control or '-'}  [{r.relationship}, {r.confidence}]")
        typer.echo(f"     {r.rationale}")


@app.command()
def validate(
    files: list[Path] = typer.Argument(None, help="Hồ sơ đánh giá cần kiểm tra (tùy chọn)."),
    data_dir: list[Path] | None = DataDirs,
) -> None:
    """Kiểm tra cấu trúc và tham chiếu chéo của toàn bộ dữ liệu (dùng trong CI)."""
    repo = _repo(data_dir)
    errors = repo.validate()
    for f in files or []:
        e, w = repo.validate_assessment(_assessment(f))
        errors += [f"{f}: {x}" for x in e]
        for x in w:
            typer.secho(f"{f}: cảnh báo: {x}", fg="yellow")
    for e in errors:
        typer.secho(e, fg="red", err=True)
    if errors:
        raise typer.Exit(1)
    typer.echo(f"Hợp lệ: {len(repo.catalogs)} danh mục, {len(repo.mappings)} bảng đối chiếu.")


@app.command()
def init(
    catalog: str,
    out: Path = typer.Option(..., "--out", "-o"),
    organization: str = typer.Option("Công ty CP ABC", help="Tên tổ chức"),
    scope: str = typer.Option("Toàn bộ hệ thống thông tin dùng chung", help="Phạm vi"),
    level: int | None = Level,
    data_dir: list[Path] | None = DataDirs,
) -> None:
    """Tạo hồ sơ đánh giá trống đủ mọi control của một danh mục (lọc theo cấp độ nếu có)."""
    repo = _repo(data_dir)
    out.write_text(assessment_template(repo.catalog(catalog), organization, scope, level), "utf-8")
    typer.echo(f"Đã tạo: {out}")


@app.command()
def soa(
    assessment: Path = typer.Argument(..., exists=True, dir_okay=False),
    out: Path = typer.Option(Path("soa.xlsx"), "--out", "-o"),
    data_dir: list[Path] | None = DataDirs,
    related: list[str] | None = Related,
    level: int | None = Level,
) -> None:
    """Sinh Tuyên bố áp dụng (SoA) dạng Excel, có trang tổng hợp dùng công thức."""
    repo = _repo(data_dir)
    a = _assessment(assessment)
    errors, warnings = repo.validate_assessment(a)
    for w in warnings:
        typer.secho(f"Cảnh báo: {w}", fg="yellow")
    if errors:
        for e in errors:
            typer.secho(e, fg="red", err=True)
        raise typer.Exit(1)
    write_soa(repo, a, out, set(related) if related else None, level)
    typer.echo(f"Đã ghi: {out}")


@app.command()
def gap(
    assessment: Path = typer.Argument(..., exists=True, dir_okay=False),
    out: Path | None = typer.Option(None, "--out", "-o", help="Bỏ trống để in ra màn hình."),
    data_dir: list[Path] | None = DataDirs,
    related: list[str] | None = Related,
    level: int | None = Level,
) -> None:
    """Sinh báo cáo khoảng cách dạng Markdown."""
    repo = _repo(data_dir)
    text = gap_markdown(repo, _assessment(assessment), set(related) if related else None, level)
    if out:
        out.write_text(text, encoding="utf-8")
        typer.echo(f"Đã ghi: {out}")
    else:
        typer.echo(text)


@app.command()
def coverage(
    mapping: str = typer.Argument(..., help="Mã bảng đối chiếu, ví dụ iso27001-2022__nd331-2026"),
    out: Path | None = typer.Option(None, "--out", "-o", help="Bỏ trống để in ra màn hình."),
    data_dir: list[Path] | None = DataDirs,
) -> None:
    """Độ phủ của bảng đối chiếu: yêu cầu chưa có biện pháp tương ứng ở mỗi phía."""
    repo = _repo(data_dir)
    try:
        text = coverage_markdown(repo.coverage(mapping))
    except DataError as exc:
        typer.secho(str(exc), fg="red", err=True)
        raise typer.Exit(1) from exc
    if out:
        out.write_text(text, encoding="utf-8")
        typer.echo(f"Đã ghi: {out}")
    else:
        typer.echo(text)


@app.command()
def schema(out_dir: Path = typer.Option(Path("schemas"), "--out", "-o")) -> None:
    """Xuất JSON Schema cho catalog/mapping/assessment (dùng cho trình soạn YAML)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, model in MODELS.items():
        path = out_dir / f"{name}.schema.json"
        data = model.model_json_schema()
        data["$id"] = f"https://github.com/thinhnx128/vn-compliance-crosswalk/schemas/{name}.schema.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        typer.echo(f"Đã ghi: {path}")


@app.command()
def version() -> None:
    """In phiên bản."""
    typer.echo(__version__)


if __name__ == "__main__":  # pragma: no cover
    app()
