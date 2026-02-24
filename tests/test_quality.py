import pandas as pd
from flight_pipeline.quality import compute_quality_report

def test_quality_report_basic_metrics():
    df = pd.DataFrame(
        {
            "airline": ["AF", "AF", "FR"],
            "origin": ["CDG", "NCE", "BOD"],
            "dest": ["NCE", "CDG", "PMI"],
            "cancelled": [0, 1, 0],
            "actual_dep": ["08:00", None, "10:00"],
            "actual_arr": ["09:00", None, "12:00"],
        }
    )

    r = compute_quality_report(df, top_n=10)

    assert r.rows == 3
    assert abs(r.cancelled_rate - (1/3)) < 1e-9
    assert r.missing_rates["actual_dep"] > 0
    assert r.top_airlines[0][0] == "AF"