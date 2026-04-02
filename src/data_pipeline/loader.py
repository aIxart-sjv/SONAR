import pandas as pd
import os

def load_dataset(data_path):
    dataframes = []

    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            full_path = os.path.join(data_path, file)
            print(f"Loading {file}...")
            df = pd.read_csv(full_path, low_memory=False, encoding='latin1')

            # 🔥 FIX: remove spaces from column names
            df.columns = df.columns.str.strip()

            dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df