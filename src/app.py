# app.py
import streamlit as st
import pandas as pd
import os

import data_fetch
import data_clean
import charts

# -------------------------------------------------
# 1. Define paths and ensure they work on Streamlit Cloud
# -------------------------------------------------
BASE_DIR = os.path.dirname(__file__)  # folder where app.py lives
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "vehicle_data_raw.csv")

# Create directories if missing
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

# Generate sample data if CSV not found
if not os.path.exists(RAW_PATH):
    st.warning("CSV not found, generating sample dataset...")
    data_fetch.generate_sample_raw(RAW_PATH)

# Load data
try:
    df_raw = pd.read_csv(RAW_PATH)
except Exception as e:
    st.error(f"Failed to load CSV: {e}")
    st.stop()

# -------------------------------------------------
# 2. Clean data
# -------------------------------------------------
df = data_clean.clean_data(df_raw)

# -------------------------------------------------
# 3. Sidebar filters
# -------------------------------------------------
st.sidebar.title("Filters")

vehicle_types = st.sidebar.multiselect(
    "Select Vehicle Types",
    options=df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique(),
)

manufacturers = st.sidebar.multiselect(
    "Select Manufacturers",
    options=df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique(),
)

filtered_df = df[
    (df["Vehicle_Type"].isin(vehicle_types)) &
    (df["Manufacturer"].isin(manufacturers))
]

# -------------------------------------------------
# 4. Metrics
# -------------------------------------------------
total, yoy, qoq = charts.calculate_metrics(filtered_df)

st.title("🚗 Vehicle Registration Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Registrations", f"{total:,}")
col2.metric("YoY Growth", f"{yoy:.2f}%")
col3.metric("QoQ Growth", f"{qoq:.2f}%")

st.markdown("---")

# -------------------------------------------------
# 5. Charts
# -------------------------------------------------
tab1, tab2 = st.tabs(["📈 Trend", "🏭 Top Manufacturers"])

with tab1:
    fig_trend = charts.plot_trend(filtered_df)
    if fig_trend:
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No trend data available for selected filters.")

with tab2:
    fig_top = charts.plot_top_manufacturers(filtered_df)
    if fig_top:
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("No manufacturer data available for selected filters.")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Data Source: Vahan / Sample Data | Dashboard deployed via Streamlit Cloud")
