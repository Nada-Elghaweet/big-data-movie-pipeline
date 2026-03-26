import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Usage: python ingest.py <dataset_path>")
    sys.exit(1)

dataset_path = sys.argv[1]

try:
    df = pd.read_csv(dataset_path)
    print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    sys.exit(1)

df.to_csv("data_raw.csv", index=False)
print("Saved raw data as data_raw.csv")