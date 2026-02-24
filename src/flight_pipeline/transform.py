from __future__ import annotations

import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Normalize strings
    out["airline"] = out["airline"].astype(str).str.strip().str.upper()
    out["origin"] = out["origin"].astype(str).str.strip().str.upper()
    out["dest"] = out["dest"].astype(str).str.strip().str.upper()

    # flight_number as string (keep leading zeros if any)
    out["flight_number"] = out["flight_number"].astype(str).str.strip()

    # cancelled as int
    out["cancelled"] = pd.to_numeric(out["cancelled"], errors="coerce").fillna(0).astype(int)

    # Empty strings -> NA for actual times
    for c in ["actual_dep", "actual_arr"]:
        if c in out.columns:
            out[c] = out[c].replace("", pd.NA)

    return out