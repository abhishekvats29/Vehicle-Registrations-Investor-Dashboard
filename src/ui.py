# src/ui.py
import streamlit as st
import pandas as pd
from datetime import datetime
from charts import calculate_metrics, plot_trend, plot_top_manufacturers

# -------------------
# PAGE CONFIGURATION
# -------------------
st.set_page_config(
    page_title="Vehicle Registration Investor Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------
# CUSTOM PAGE STYLES
# -------------------
st.markdown("""
    <style>
        .stApp {
            background-color: #f8f9fa;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.5rem;
            font-weight: 600;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------
# PAGE TITLE
# -------------------
st.title("📊 Vehicle Registration Investor Dashboard")
st.markdown(
    "#### Track growth trends, market share, and performance by manufacturer."
)

# -------------------
# LOAD DATA
# -------------------
@st.cache_data
def load_data():
    """Load cleaned vehicle registration data."""
    df = pd.read_excel("data/processed/vehicle_data_cleaned.xlsx")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -------------------
# SIDEBAR FILTERS
# -------------------
st.sidebar.header("🔍 Filters")

# Date filter
min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Vehicle type filter
vehicle_types = st.sidebar.multiselect(
    "Select Vehicle Categories",
    options=df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique()
)

# Manufacturer filter
manufacturers = st.sidebar.multiselect(
    "Select Manufacturers",
    options=df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique()
)

# -------------------
# FILTER DATA
# -------------------
filtered_df = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["Vehicle_Type"].isin(vehicle_types)) &
    (df["Manufacturer"].isin(manufacturers))
]

# -------------------
# METRICS SECTION
# -------------------
st.markdown("### 📈 Key Metrics")
total, yoy, qoq = calculate_metrics(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Registrations", f"{total:,}")
col2.metric("YoY Growth", f"{yoy:.2f}%")
col3.metric("QoQ Growth", f"{qoq:.2f}%")

# -------------------
# TREND CHART
# -------------------
st.markdown("### 📅 Registration Trends Over Time")
st.plotly_chart(plot_trend(filtered_df), use_container_width=True)

# -------------------
# TOP MANUFACTURERS CHART
# -------------------
st.markdown("### 🏆 Top Manufacturers")
st.plotly_chart(plot_top_manufacturers(filtered_df), use_container_width=True)

# -------------------
# DATA TABLE
# -------------------
st.markdown("### 📋 Detailed Data")
st.dataframe(filtered_df.style.format({"Registrations": "{:,}"}))

# -------------------
# FOOTER
# -------------------
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit & Plotly | Data Source: Vahan Dashboard",
    unsafe_allow_html=True
)
