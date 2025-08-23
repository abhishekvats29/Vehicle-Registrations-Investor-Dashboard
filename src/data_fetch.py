import os
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from io import BytesIO

BASE_DIR = os.path.dirname(__file__)
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "vehicle_data_raw.csv")

def fetch_from_url(csv_url: str = None, raw_path: str = RAW_PATH):
    """
    Try to download CSV from csv_url and save to raw_path.
    If csv_url is None, fallback to sample data generation.
    Returns DataFrame and path.
    """
    if csv_url:
        try:
            print(f">> Attempting to download data from: {csv_url}")
            resp = requests.get(csv_url, timeout=30)
            resp.raise_for_status()
            df = pd.read_csv(BytesIO(resp.content))
            os.makedirs(os.path.dirname(raw_path), exist_ok=True)
            df.to_csv(raw_path, index=False)
            print(f">> Downloaded and saved raw data to: {raw_path}")
            return df, raw_path
        except Exception as e:
            print(f">> Failed to fetch CSV: {e}")
            print(">> Falling back to sample dataset.")
            return generate_sample_raw(raw_path)
    else:
        return generate_sample_raw(raw_path)

def generate_sample_raw(raw_path: str = RAW_PATH, n_months: int = 48, seed: int = 42):
    """
    Generate realistic sample vehicle registration data.
    """
    print(">> Generating sample raw dataset...")
    np.random.seed(seed)

    makes = {
        "2W": ["Hero", "Honda", "TVS", "Bajaj", "Yamaha"],
        "3W": ["Bajaj", "Piaggio", "Mahindra", "Atul"],
        "4W": ["Maruti", "Hyundai", "Tata", "Mahindra", "Kia"]
    }

    end = datetime.today().replace(day=1)
    dates = pd.date_range(end=end, periods=n_months, freq='MS')

    rows = []
    for dt in dates:
        for vt, makers in makes.items():
            base = 20000 if vt == "2W" else (3000 if vt == "3W" else 12000)
            month_factor = 1.0 + 0.1 * np.sin(2 * np.pi * (dt.month / 12))
            for m in makers:
                share = np.random.uniform(0.6, 1.4) / len(makers)
                count = max(0, int(base * share * month_factor * np.random.uniform(0.6, 1.4)))
                rows.append({
                    "Date": dt.strftime("%Y-%m-%d"),
                    "Vehicle_Type": vt,
                    "Manufacturer": m,
                    "Registrations": count
                })

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    df.to_csv(raw_path, index=False)
    print(f">> Sample raw data saved to: {raw_path} (rows: {len(df)})")
    return df, raw_path

if __name__ == "__main__":
    # Default: use Google Drive CSV link
    DRIVE_SHEET_ID = "1q4Qn32MBJ8IfKWUlHy5907cjRD-uiKu_"
    DRIVE_CSV_URL = f"https://docs.google.com/spreadsheets/d/{DRIVE_SHEET_ID}/export?format=csv"
    fetch_from_url(DRIVE_CSV_URL)
