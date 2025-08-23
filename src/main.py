# src/main.py
import subprocess
import sys

if __name__ == "__main__":
    # Launch the Streamlit UI
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/ui.py"])
