# app.py
import streamlit as st
import pandas as pd
import os

import data_fetch
import data_clean
import charts

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Vehicle Registration Investor Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #f8f9fa; }
        div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 600; }
        h1, h2, h3 { color: #2c3e50; }
        [data-testid="stSidebar"] { background-color: #ffffff; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .stTabs [role="tablist"] { margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("📊 Vehicle Registration Investor Dashboard")
st.markdown("#### Track growth trends, market share, and performance by manufacturer.")

# --- DATA PATH ---
BASE_DIR = os.path.dirname(__file__)
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "vehicle_data_raw.csv")
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

# --- LOAD DATA ---
if not os.path.exists(RAW_PATH):
    st.warning("CSV not found, generating sample dataset...")
    data_fetch.generate_sample_raw(RAW_PATH)

try:
    df_raw = pd.read_csv(RAW_PATH)
except Exception as e:
    st.error(f"Failed to load CSV: {e}")
    st.stop()

# --- CLEAN DATA ---
df = data_clean.clean_data(df_raw)

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")

vehicle_types = st.sidebar.multiselect(
    "Select Vehicle Categories",
    options=df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique()
)

manufacturers = st.sidebar.multiselect(
    "Select Manufacturers",
    options=df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique()
)

filtered_df = df[
    (df["Vehicle_Type"].isin(vehicle_types)) &
    (df["Manufacturer"].isin(manufacturers))
]

# --- METRICS ---
st.markdown("### 📈 Key Metrics")
total, yoy, qoq = charts.calculate_metrics(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Registrations", f"{total:,}")
col2.metric("YoY Growth", f"{yoy:.2f}%")
col3.metric("QoQ Growth", f"{qoq:.2f}%")

st.markdown("---")

# --- CHARTS ---
tab1, tab2 = st.tabs(["📅 Registration Trends", "🏆 Top Manufacturers"])

with tab1:
    st.markdown("### Vehicle Registrations Over Time")
    fig_trend = charts.plot_trend(filtered_df)
    if fig_trend:
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No trend data available for selected filters.")

with tab2:
    st.markdown("### Top Manufacturers by Registrations")
    fig_top = charts.plot_top_manufacturers(filtered_df)
    if fig_top:
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("No manufacturer data available for selected filters.")

# --- FOOTER ---
st.caption("Data Source: Vahan / Sample Data | Dashboard deployed via Streamlit Cloud")
