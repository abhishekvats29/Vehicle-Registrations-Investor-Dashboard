# app.py
import streamlit as st
import pandas as pd
import os

import data_fetch
import data_clean
import charts

# -------------------------------------------------
# 1. Load raw data (CSV from repo or generate sample)
# -------------------------------------------------
RAW_PATH = "data/raw/vehicle_data_raw.csv"

if not os.path.exists(RAW_PATH):
    st.warning("No CSV found, generating sample dataset...")
    data_fetch.generate_sample_raw(RAW_PATH)

df_raw = pd.read_csv(RAW_PATH)

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
    st.plotly_chart(charts.plot_trend(filtered_df), use_container_width=True)

with tab2:
    st.plotly_chart(charts.plot_top_manufacturers(filtered_df), use_container_width=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Data Source: Vahan / Sample Data")
