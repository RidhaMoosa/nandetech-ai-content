import pandas as pd

def load(data):
    if isinstance(data, pd.DataFrame):
        data.to_csv('transformed_data.csv', index=False)
    else:
        with open('transformed_data.txt', 'w') as file:
            file.write(data)
