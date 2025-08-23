# src/main.py
import os
import subprocess
import sys

from data_fetch import generate_sample_raw, fetch_from_url, RAW_PATH
from data_clean import run as clean_run, CLEANED_PATH

# ---------------------------
# Google Drive CSV link
# ---------------------------
# Convert your Google Sheets link to direct CSV download
sheet_id = "1q4Qn32MBJ8IfKWUlHy5907cjRD-uiKu_"
DRIVE_CSV_URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

def run_pipeline(download_url: str = None):
    # Use the provided URL or default to Google Drive CSV
    url_to_fetch = download_url if download_url else DRIVE_CSV_URL

    print(f"Fetching dataset from: {url_to_fetch}")
    try:
        fetch_from_url(url_to_fetch, RAW_PATH)
    except Exception as e:
        print("Failed to fetch from URL:", e)
        print("Falling back to generated sample raw dataset.")
        generate_sample_raw(RAW_PATH)

    print("Running cleaning step...")
    clean_run(RAW_PATH, CLEANED_PATH)

    print("\nPipeline finished. Launching Streamlit dashboard...")

    # Launch Streamlit dashboard directly
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/ui.py"])

if __name__ == "__main__":
    # Optionally accept a CSV URL as the first argument
    url = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(download_url=url)
