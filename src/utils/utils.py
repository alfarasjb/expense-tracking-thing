from typing import Dict, List, Any

import pandas as pd

from src.definitions.constants import DATE


def response_as_dataframe(response: List[Dict[str, Any]]):
    df = pd.DataFrame(response)
    df.columns = [c.upper() for c in df.columns]
    df[DATE] = pd.to_datetime(df[DATE], unit='ms')

    return df
