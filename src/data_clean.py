import os
import pandas as pd
import numpy as np

RAW_PATH = "data/raw/vehicle_data_raw.xlsx"
CLEANED_PATH = "data/processed/vehicle_data_cleaned.xlsx"

def safe_read_raw(raw_path: str = RAW_PATH, sheet_name: str = 0):
    print(f">> Reading raw file: {raw_path}")
    df = pd.read_excel(raw_path, sheet_name=sheet_name)
    print(f">> Raw columns: {list(df.columns)}")
    return df

def normalize_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names and types to an expected schema:
    Expected columns in cleaned data:
      - Date (datetime)
      - Year (int)
      - Quarter (str, format 'YYYYQx' or 'YYYY-Q{1..4}')
      - Vehicle_Type (2W/3W/4W)
      - Manufacturer
      - Registrations (int)
    """
    print(">> Cleaning data...")
    df = df.copy()

    # Lower/strip column names
    df.columns = [str(c).strip() for c in df.columns]

    # Try to find common column name variants
    col_map = {}
    for c in df.columns:
        lc = c.lower()
        if "date" in lc:
            col_map[c] = "Date"
        elif "vehicle" in lc and "type" in lc:
            col_map[c] = "Vehicle_Type"
        elif lc in ("type", "v_type"):
            col_map[c] = "Vehicle_Type"
        elif "manufacturer" in lc or "make" in lc:
            col_map[c] = "Manufacturer"
        elif "regist" in lc or "count" in lc or "registration" in lc:
            col_map[c] = "Registrations"

    df = df.rename(columns=col_map)
    # Fill missing expected columns if absent
    if "Registrations" not in df.columns:
        df["Registrations"] = 1
    if "Manufacturer" not in df.columns:
        df["Manufacturer"] = "Unknown"
    if "Vehicle_Type" not in df.columns:
        df["Vehicle_Type"] = "Unknown"

    # Parse dates
    if "Date" in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    else:
        if "Year" in df.columns and "Month" in df.columns:
            df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
        else:
            df['Date'] = pd.Timestamp.today().normalize()

    before = len(df)
    df = df[~df['Date'].isna()].copy()
    df['Registrations'] = pd.to_numeric(df['Registrations'], errors='coerce').fillna(0).astype(int)
    after = len(df)
    print(f">> Dropped {before - after} rows with invalid dates")

    # Add Year and Quarter
    df['Year'] = df['Date'].dt.year
    q = df['Date'].dt.quarter
    df['Quarter'] = df['Year'].astype(str) + "Q" + q.astype(str)

    # Standardize Vehicle_Type
    vt_map = {
        '2w': '2W', '2-w': '2W', 'two wheeler': '2W', 'two-wheeler': '2W',
        '3w': '3W', '3-w': '3W', 'three wheeler': '3W',
        '4w': '4W', '4-w': '4W', 'four wheeler': '4W', 'car': '4W'
    }
    df['Vehicle_Type'] = df['Vehicle_Type'].astype(str).str.strip().str.lower().map(vt_map).fillna(
        df['Vehicle_Type'].astype(str).str.strip().str.upper()
    )

    # Remove empty rows
    drop_mask = (df['Registrations'] == 0) & (df['Manufacturer'].str.lower() == 'unknown') & (df['Vehicle_Type'].str.lower() == 'unknown')
    dropped = drop_mask.sum()
    if dropped > 0:
        print(f">> Dropping {dropped} empty/irrelevant rows")
    df = df[~drop_mask].copy()

    # Aggregate duplicates
    agg = df.groupby(['Date', 'Year', 'Quarter', 'Vehicle_Type', 'Manufacturer'], as_index=False)['Registrations'].sum()

    return agg

def save_clean(df: pd.DataFrame, cleaned_path: str = CLEANED_PATH):
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    df.to_excel(cleaned_path, index=False)
    print(f">> Cleaned data saved to: {cleaned_path}")

def run(cleaned_path: str = CLEANED_PATH, raw_path: str = RAW_PATH):
    df_raw = safe_read_raw(raw_path)
    df_clean = normalize_and_clean(df_raw)
    save_clean(df_clean, cleaned_path)
    return cleaned_path

# ✅ Alias for backward compatibility
clean_data = normalize_and_clean

if __name__ == "__main__":
    if not os.path.exists(RAW_PATH):
        print("Raw file not found - generate sample raw data first (use data_fetch.py).")
    else:
        run()
