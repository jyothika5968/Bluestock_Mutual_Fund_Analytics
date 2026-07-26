import os
import requests
import pandas as pd

API_BASE_URL = "https://api.mfapi.in/mf"

SCHEMES = {
    "SBI Bluechip": 119551,
    "ICICI Bluechip": 120503,
    "Nippon Large Cap": 118632,
    "Axis Bluechip": 119092,
    "Kotak Bluechip": 120841,
}

output_folder = "data/raw"
os.makedirs(output_folder, exist_ok=True)

all_nav_records = []

for scheme_name, amfi_code in SCHEMES.items():
    url = f"{API_BASE_URL}/{amfi_code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        result = response.json()

        scheme_meta = result.get("meta", {})
        nav_data = result.get("data", [])

        if not nav_data:
            print(f"No NAV data found for {scheme_name} ({amfi_code})")
            continue

        for record in nav_data:
            all_nav_records.append(
                {
                    "amfi_code": amfi_code,
                    "scheme_name": scheme_meta.get("scheme_name", scheme_name),
                    "fund_house": scheme_meta.get("fund_house"),
                    "scheme_category": scheme_meta.get("scheme_category"),
                    "scheme_type": scheme_meta.get("scheme_type"),
                    "date": record.get("date"),
                    "nav": record.get("nav"),
                }
            )

        print(
            f"Fetched {len(nav_data)} NAV records for "
            f"{scheme_name} ({amfi_code})"
        )

    except requests.exceptions.RequestException as error:
        print(f"API request failed for {scheme_name}: {error}")

    except ValueError:
        print(f"Invalid JSON response received for {scheme_name}")

if all_nav_records:
    nav_df = pd.DataFrame(all_nav_records)

    nav_df["date"] = pd.to_datetime(
        nav_df["date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    nav_df["nav"] = pd.to_numeric(
        nav_df["nav"],
        errors="coerce"
    )

    nav_df = nav_df.sort_values(
        by=["amfi_code", "date"],
        ascending=[True, False]
    )

    output_file = os.path.join(
        output_folder,
        "live_nav_5_schemes.csv"
    )

    nav_df.to_csv(output_file, index=False)

    print("\nLive NAV data saved successfully.")
    print(f"Output file: {output_file}")
    print(f"Shape: {nav_df.shape}")
    print("\nFirst 5 rows:")
    print(nav_df.head())

else:
    print("No NAV records were fetched.")