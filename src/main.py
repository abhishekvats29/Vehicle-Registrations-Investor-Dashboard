# src/main.py
import os
import subprocess
import sys

from data_fetch import generate_sample_raw, fetch_from_url, RAW_PATH
from data_clean import run as clean_run, CLEANED_PATH

def run_pipeline(download_url: str = None):
    if download_url:
        print("Fetching from URL...")
        try:
            fetch_from_url(download_url)
        except Exception as e:
            print("Failed to fetch from URL:", e)
            print("Falling back to generated sample raw dataset.")
            generate_sample_raw()
    else:
        print("No URL provided — generating sample raw dataset.")
        generate_sample_raw()

    print("Running cleaning step...")
    clean_run()

    print("\nPipeline finished. Launching Streamlit dashboard...")

    # Launch Streamlit dashboard directly
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/ui.py"])

if __name__ == "__main__":
    # Optionally accept a CSV URL as the first argument
    url = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(download_url=url)
