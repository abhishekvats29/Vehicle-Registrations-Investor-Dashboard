import os
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from io import BytesIO

RAW_PATH = "data/raw/vehicle_data_raw.csv"

def fetch_from_url(csv_url: str, raw_path: str = RAW_PATH):
    """
    Try to download CSV from csv_url and save as CSV to raw_path.
    If download fails, exception will be raised.
    """
    print(f">> Attempting to download data from: {csv_url}")
    resp = requests.get(csv_url, timeout=30)
    resp.raise_for_status()

    # read into dataframe
    df = pd.read_csv(BytesIO(resp.content))

    # ensure folder exists
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)

    # save as CSV (not Excel)
    df.to_csv(raw_path, index=False)
    print(f">> Downloaded and saved raw data to: {raw_path}")
    return raw_path

def generate_sample_raw(raw_path: str = RAW_PATH, n_months: int = 48):
    """
    Generate sample realistic vehicle registration data for demo/testing.
    Columns:
      - Date (monthly)
      - Vehicle_Type (2W/3W/4W)
      - Manufacturer
      - Registrations (Count)
    """
    print(">> Generating sample raw dataset...")
    np.random.seed(42)

    # Define manufacturers and shares
    makes = {
        "2W": ["Hero", "Honda", "TVS", "Bajaj", "Yamaha"],
        "3W": ["Bajaj", "Piaggio", "Mahindra", "Atul"],
        "4W": ["Maruti", "Hyundai", "Tata", "Mahindra", "Kia"]
    }

    # monthly dates
    end = datetime.today().replace(day=1)
    dates = [end - pd.DateOffset(months=i) for i in range(n_months)]
    dates = sorted(dates)

    rows = []
    for dt in dates:
        for vt, makers in makes.items():
            base = 20000 if vt == "2W" else (3000 if vt == "3W" else 12000)
            # seasonality + noise
            month_factor = 1.0 + 0.1 * np.sin(2 * np.pi * (dt.month / 12))
            for m in makers:
                # manufacturer share variation
                share = np.random.uniform(0.6, 1.4) / len(makers)
                count = max(0, int(base * share * month_factor * np.random.uniform(0.6, 1.4)))
                rows.append({
                    "Date": dt.strftime("%Y-%m-%d"),
                    "Vehicle_Type": vt,
                    "Manufacturer": m,
                    "Registrations": count
                })

    df = pd.DataFrame(rows)

    # ensure folder exists
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)

    # save as CSV (not Excel)
    df.to_csv(raw_path, index=False)
    print(f">> Sample raw data saved to: {raw_path} (rows: {len(df)})")
    return raw_path

if __name__ == "__main__":
    # Example usage:
    # csv_url = "https://example.com/vahan_export.csv"
    # fetch_from_url(csv_url)

    # Default: generate sample
    generate_sample_raw()
