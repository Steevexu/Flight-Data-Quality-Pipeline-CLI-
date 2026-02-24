import pandas as pd
import pytest
from flight_pipeline.schema import flight_schema

def test_schema_accepts_valid_row():
    df = pd.DataFrame(
        {
            "flight_date": ["2026-02-01"],
            "airline": ["AF"],
            "flight_number": ["1234"],
            "origin": ["CDG"],
            "dest": ["NCE"],
            "scheduled_dep": ["08:10"],
            "actual_dep": ["08:25"],
            "scheduled_arr": ["09:45"],
            "actual_arr": ["10:02"],
            "cancelled": [0],
        }
    )
    validated = flight_schema().validate(df, lazy=True)
    assert len(validated) == 1

def test_schema_rejects_origin_equals_dest():
    df = pd.DataFrame(
        {
            "flight_date": ["2026-02-01"],
            "airline": ["AF"],
            "flight_number": ["1234"],
            "origin": ["CDG"],
            "dest": ["CDG"],
            "scheduled_dep": ["08:10"],
            "actual_dep": ["08:25"],
            "scheduled_arr": ["09:45"],
            "actual_arr": ["10:02"],
            "cancelled": [0],
        }
    )
    with pytest.raises(Exception):
        flight_schema().validate(df, lazy=True)