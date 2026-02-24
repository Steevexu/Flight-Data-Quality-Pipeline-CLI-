from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .io import read_csv, write_parquet, read_parquet
from .schema import flight_schema
from .transform import clean
from .quality import compute_quality_report, render_markdown

app = typer.Typer(add_completion=False, help="Flight data quality pipeline (Pandera + Parquet + report)")
console = Console()


@app.command()
def run(
    input: Path = typer.Option(..., "--input", "-i", exists=True, readable=True, help="Input CSV file"),
    out: Path = typer.Option(Path("data/processed/flights.parquet"), "--out", "-o", help="Output Parquet file"),
):
    """Run the pipeline: read CSV -> clean -> validate -> write Parquet."""
    df = read_csv(input)
    console.print(f"Loaded rows: [bold]{len(df)}[/bold]")

    df = clean(df)

    schema = flight_schema()
    try:
        validated = schema.validate(df, lazy=True)
    except Exception as e:
        console.print("[red]Validation failed[/red]")
        console.print(str(e))
        raise typer.Exit(code=1)

    write_parquet(validated, out)
    console.print(Panel(f"✅ Exported Parquet: {out}", title="Success"))


@app.command()
def report(
    input: Path = typer.Option(..., "--input", "-i", exists=True, readable=True, help="Input Parquet file"),
    out: Path = typer.Option(Path("reports/quality_report.md"), "--out", "-o", help="Output Markdown report"),
    top: int = typer.Option(10, "--top", help="Top N airlines/routes"),
    fail_if_cancelled_rate: float | None = typer.Option(
        None, "--fail-if-cancelled-rate", help="Fail if cancelled rate is greater than this threshold (0..1)"
    ),
    fail_if_missing_actual_dep: float | None = typer.Option(
        None,
        "--fail-if-missing-actual-dep",
        help="Fail if missing rate of actual_dep is greater than this threshold (0..1)",
    ),
):
    """Generate a data quality report (console + Markdown)."""
    df = read_parquet(input)
    r = compute_quality_report(df, top_n=top)

    # Console output (Rich)
    console.print(f"[bold]Rows:[/bold] {r.rows}")
    console.print(f"[bold]Cancelled rate:[/bold] {r.cancelled_rate:.2%}")

    table = Table(title="Missing values")
    table.add_column("Column")
    table.add_column("Missing rate")
    for col, rate in r.missing_rates.items():
        table.add_row(col, f"{rate:.2%}")
    console.print(table)

    table2 = Table(title=f"Top airlines (top {top})")
    table2.add_column("Airline")
    table2.add_column("Count", justify="right")
    for a, c in r.top_airlines:
        table2.add_row(a, str(c))
    console.print(table2)

    table3 = Table(title=f"Top routes (top {top})")
    table3.add_column("Route")
    table3.add_column("Count", justify="right")
    for route, c in r.top_routes:
        table3.add_row(route, str(c))
    console.print(table3)

    # Markdown report (always generated)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(r), encoding="utf-8")
    console.print(Panel(f"✅ Report generated: {out}", title="Success"))

    # -----------------------------
    # Quality Gate
    # -----------------------------
    gate_failures: list[str] = []

    if fail_if_cancelled_rate is not None and r.cancelled_rate > fail_if_cancelled_rate:
        gate_failures.append(
            f"Cancelled rate {r.cancelled_rate:.2%} > threshold {fail_if_cancelled_rate:.2%}"
        )

    missing_actual_dep = r.missing_rates.get("actual_dep")
    if fail_if_missing_actual_dep is not None and missing_actual_dep is not None:
        if missing_actual_dep > fail_if_missing_actual_dep:
            gate_failures.append(
                f"Missing actual_dep {missing_actual_dep:.2%} > threshold {fail_if_missing_actual_dep:.2%}"
            )

    if gate_failures:
        console.print("[red][bold]QUALITY GATE FAILED[/bold][/red]")
        for msg in gate_failures:
            console.print(f"[red]- {msg}[/red]")
        raise typer.Exit(code=2)
    else:
        console.print("[green][bold]QUALITY GATE PASSED[/bold][/green]")

if __name__ == "__main__":
    app()