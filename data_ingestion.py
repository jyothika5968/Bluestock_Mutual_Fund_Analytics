import os
import pandas as pd

folder_path = "data/raw"

csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

print(f"Total CSV Files Found: {len(csv_files)}")

for file in csv_files:
    file_path = os.path.join(folder_path, file)

    df = pd.read_csv(file_path)

    print("\n" + "="*60)
    print(f"File Name: {file}")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nData Types:")
    print(df.dtypes)
    print("\nFirst 5 Rows:")
    print(df.head())
    print("="*60)

    print("\n" + "=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)

    print(f"\nFile: {file}")
    print(f"Missing Values: {df.isnull().sum().sum()}")
    print(f"Duplicate Rows: {df.duplicated().sum()}")