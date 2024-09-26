import pandas as pd

def transform(data):
    if isinstance(data, str):
        return data.lower()
    elif isinstance(data, pd.DataFrame):
        return data.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    return data
