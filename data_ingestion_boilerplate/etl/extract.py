import pandas as pd

def extract(filepath):
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath)
    elif filepath.endswith('.json'):
        return pd.read_json(filepath)
    elif filepath.endswith('.xml'):
        return pd.read_xml(filepath)
    elif filepath.endswith('.txt'):
        with open(filepath, 'r') as file:
            return file.read()
    else:
        raise ValueError("Unsupported file type")
