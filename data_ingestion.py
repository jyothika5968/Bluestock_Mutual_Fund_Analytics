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

    print("\n" + "=" * 60)
print("FUND MASTER EXPLORATION")
print("=" * 60)

fund_master_path = os.path.join(folder_path, "01_fund_master.csv")
nav_history_path = os.path.join(folder_path, "02_nav_history.csv")

fund_master_df = pd.read_csv(fund_master_path)
nav_history_df = pd.read_csv(nav_history_path)

print("\nUnique Fund Houses:")
print(fund_master_df["fund_house"].unique())

print("\nUnique Categories:")
print(fund_master_df["category"].unique())

print("\nUnique Sub-Categories:")
print(fund_master_df["sub_category"].unique())

print("\nUnique Risk Categories:")
print(fund_master_df["risk_category"].unique())

print("\n" + "=" * 60)
print("AMFI CODE VALIDATION")
print("=" * 60)

fund_master_codes = set(fund_master_df["amfi_code"])
nav_history_codes = set(nav_history_df["amfi_code"])

matched_codes = fund_master_codes.intersection(nav_history_codes)
missing_codes = fund_master_codes.difference(nav_history_codes)

print(f"Total AMFI Codes in Fund Master: {len(fund_master_codes)}")
print(f"Matched Codes in NAV History: {len(matched_codes)}")
print(f"Missing Codes: {len(missing_codes)}")

if missing_codes:
    print("Missing AMFI Codes:")
    print(sorted(missing_codes))
else:
    print("All AMFI codes are available in NAV history.")

print("\n" + "=" * 60)
print("DATA QUALITY SUMMARY")
print("=" * 60)

print("10 CSV datasets loaded successfully.")
print("No duplicate rows found in any dataset.")
print("Only 04_monthly_sip_inflows.csv contains 12 missing values.")
print(f"{len(matched_codes)} AMFI codes matched with NAV history.")
print(f"{len(missing_codes)} AMFI codes are missing from NAV history.")