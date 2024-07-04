from typing import Dict, List, Any

import pandas as pd


def response_as_dataframe(response: List[Dict[str, Any]]):
    df = pd.DataFrame(response)
    df.columns = [c.upper() for c in df.columns]
    return df