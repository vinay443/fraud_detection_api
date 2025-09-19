import pandas as pd
from pathlib import Path

csv = Path("data/creditcard.csv")
assert csv.exists(), f"CSV not found at {csv.resolve()}"

df = pd.read_csv(csv, nrows=5)
print("COLUMNS:", df.columns.tolist())
print("\nHEAD:")
print(df.head(2).to_string(index=False))
