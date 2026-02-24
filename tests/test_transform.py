import pandas as pd
from flight_pipeline.transform import clean

def test_clean_normalizes_strings_and_cancelled():
    df = pd.DataFrame(
        {
            "airline": [" af "],
            "origin": [" cdg "],
            "dest": [" nce "],
            "flight_number": [123],
            "cancelled": ["1"],
            "actual_dep": [""],
            "actual_arr": [""],
        }
    )
    out = clean(df)

    assert out.loc[0, "airline"] == "AF"
    assert out.loc[0, "origin"] == "CDG"
    assert out.loc[0, "dest"] == "NCE"
    assert out.loc[0, "cancelled"] == 1
    assert pd.isna(out.loc[0, "actual_dep"])