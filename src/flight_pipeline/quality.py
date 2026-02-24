from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
import pandas as pd


@dataclass(frozen=True)
class QualityReport:
    rows: int
    cancelled_rate: float
    missing_rates: dict[str, float]
    top_airlines: list[tuple[str, int]]
    top_routes: list[tuple[str, int]]


def compute_quality_report(df: pd.DataFrame, top_n: int = 10) -> QualityReport:
    rows = len(df)
    cancelled_rate = float(df["cancelled"].mean()) if rows and "cancelled" in df.columns else 0.0

    missing_cols = [c for c in ["actual_dep", "actual_arr"] if c in df.columns]
    missing_rates = {c: float(df[c].isna().mean()) if rows else 0.0 for c in missing_cols}

    airlines = Counter(df["airline"].astype(str)) if "airline" in df.columns else Counter()
    routes = (
        Counter((df["origin"].astype(str) + "→" + df["dest"].astype(str)))
        if "origin" in df.columns and "dest" in df.columns
        else Counter()
    )

    return QualityReport(
        rows=rows,
        cancelled_rate=cancelled_rate,
        missing_rates=missing_rates,
        top_airlines=airlines.most_common(top_n),
        top_routes=routes.most_common(top_n),
    )


def render_markdown(r: QualityReport) -> str:
    lines: list[str] = []
    lines.append("# Flight Data Quality Report")
    lines.append("")
    lines.append(f"- **Rows**: {r.rows}")
    lines.append(f"- **Cancelled rate**: {r.cancelled_rate:.2%}")
    lines.append("")
    lines.append("## Missing values")
    if not r.missing_rates:
        lines.append("- (no columns found)")
    else:
        for k, v in r.missing_rates.items():
            lines.append(f"- **{k}**: {v:.2%}")
    lines.append("")
    lines.append("## Top airlines")
    if not r.top_airlines:
        lines.append("- (no data)")
    else:
        for a, c in r.top_airlines:
            lines.append(f"- {a}: {c}")
    lines.append("")
    lines.append("## Top routes")
    if not r.top_routes:
        lines.append("- (no data)")
    else:
        for route, c in r.top_routes:
            lines.append(f"- {route}: {c}")
    lines.append("")
    return "\n".join(lines)