# Vehicle Registrations — Investor Dashboard

- An interactive Streamlit dashboard to explore vehicle registration trends by vehicle category and manufacturer using public data from the Vahan Dashboard.
- Built with an investor’s perspective in mind, it provides YoY (Year-over-Year) and QoQ (Quarter-over-Quarter) growth metrics along with clean, filterable visualizations.

## Features

Date Range Selection – Focus on specific time periods.
Vehicle Type Filter – Filter data by 2W, 3W, or 4W.
Manufacturer Filter – Select one or more manufacturers.

## Key Metrics:

- Total registrations (for selected filters/date range)
- YoY % change
- QoQ % change

## Interactive Visualizations:

- Trend charts for registrations over time
- Dynamic updates based on filters
- Clean, Investor-Friendly UI – Built in Streamlit for simplicity and clarity.

## Project Structure

project_root/
│
├── data/
│   ├── raw/               # Original or downloaded data
│   ├── processed/         # Cleaned and transformed data
│
├── src/
│   ├── data_fetch.py      # Fetches/scrapes or loads sample vehicle registration data
│   ├── data_clean.py      # Cleans and processes raw data
│   ├── data_analysis.py   # Performs calculations (YoY, QoQ, totals)
│   ├── ui.py              # Streamlit UI components and layout
│   ├── main.py            # Entry point to run the dashboard
│
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Git ignore rules


## Create Virtual Environment & Install Dependencies

python -m venv .venv
source .venv/bin/activate      # On macOS/Linux
.venv\Scripts\activate         # On Windows
pip install -r requirements.txt
Prepare Data

Option 1: Use data_fetch.py to scrape/load data from Vahan Dashboard.
Option 2: Place sample data in data/raw and run:

python src/data_clean.py
Run the Dashboard
streamlit run src/main.py

## Data Source-
Vahan Dashboard: Official public data on vehicle registrations in India.

## This project focuses on:

- Vehicle Type: 2W (Two-Wheeler), 3W (Three-Wheeler), 4W (Four-Wheeler)
- Manufacturer-wise registration counts
- Data is processed into a clean monthly time series for easy analysis.

## Calculations:
- Year-over-Year (YoY) Growth:
- Measures percentage change in registrations compared to the same month in the previous year.

## Quarter-over-Quarter (QoQ) Growth:
- Measures percentage change in registrations compared to the previous quarter.
- Both metrics are calculated dynamically based on applied filters.


## Dependencies

Python 3.8+
Streamlit
Pandas
NumPy
Matplotlib / Plotly
Requests / BeautifulSoup (for scraping, if used)
Install all dependencies with:
pip install -r requirements.txt

## Technical Notes
Code Modularity:
- The project separates data fetching, cleaning, analysis, and UI into different scripts for clarity and maintainability.

SQL Support (Optional):
- If desired, data cleaning and aggregation steps can be implemented in SQL before loading into the dashboard.

Version Control:
- The project is intended to be pushed to GitHub for version tracking.

How to Use
- Select a date range in the left sidebar.
- Filter by vehicle type and manufacturer(s).

## View:

- Total registrations (matching filters)
- YoY and QoQ % changes
- Registration trends over time

## License
- This project is for educational & assessment purposes.
If you wish to extend it for production or public deployment, please ensure compliance with Vahan Dashboard data usage policies.

## Author
- Abhishek vats, Backend developer

