import sys
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python ingest.py <dataset_path>")
    sys.exit(1)

dataset_path = sys.argv[1]

try:
    df = pd.read_csv(dataset_path)
    print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.\n")
    print("dataset shape:\n", df.shape)
    print("Here’s the first 5 rows:\n", df.head())

    df.to_csv("data_raw.csv", index=False)
    print("\nSaved raw data as data_raw.csv")

except Exception as e:
    print(f"Error loading dataset: {e}")
    print("Usage: python ingest.py <dataset_path>")


import subprocess
subprocess.run(["python", "preprocess.py", "data_raw.csv"])