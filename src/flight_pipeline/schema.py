from __future__ import annotations

import pandera as pa
from pandera import Column, Check


def flight_schema() -> pa.DataFrameSchema:
    return pa.DataFrameSchema(
        {
            "flight_date": Column(pa.DateTime, coerce=True, nullable=False),
            "airline": Column(str, Check.str_length(2, 6), nullable=False),
            "flight_number": Column(str, Check.str_length(1, 10), nullable=False),
            "origin": Column(str, Check.str_length(3, 3), nullable=False),
            "dest": Column(str, Check.str_length(3, 3), nullable=False),
            "scheduled_dep": Column(str, nullable=False),
            "actual_dep": Column(str, nullable=True),
            "scheduled_arr": Column(str, nullable=False),
            "actual_arr": Column(str, nullable=True),
            "cancelled": Column(int, Check.isin([0, 1]), nullable=False),
        },
        checks=[
            Check(lambda df: df["origin"].str.upper().str.len().eq(3), error="origin must be 3 letters"),
            Check(lambda df: df["dest"].str.upper().str.len().eq(3), error="dest must be 3 letters"),
            Check(lambda df: df["origin"].str.upper().ne(df["dest"].str.upper()), error="origin != dest"),
        ],
        coerce=True,
        strict=True,
    )
