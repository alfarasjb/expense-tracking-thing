from typing import Dict, List, Any

import pandas as pd

from src.definitions.constants import DATE


def response_as_dataframe(response: List[Dict[str, Any]]):
    df = pd.DataFrame(response)
    print(df.empty)
    if len(df) == 0:
        return df
    df.columns = [c.upper() for c in df.columns]
    df[DATE] = pd.to_datetime(df[DATE])
    df = df.sort_values(by=DATE, ascending=True)
    df = df.drop(columns=['USER'])
    return df


def validate_float_input(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False
