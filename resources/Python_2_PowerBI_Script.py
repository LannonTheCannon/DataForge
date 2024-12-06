import pandas as pd
from pathlib import Path

def load_file(path):
    with open(path, 'rb') as f:
        return pd.read_pickle(f)

folder = r"C:\Users\16269\DataspellProjects\DataForge\data_pkl"
all_datasets = [load_file(file) for file in Path(folder).iterdir()]
df = pd.concat(all_datasets)

print(df.shape)
print(df.dtypes)