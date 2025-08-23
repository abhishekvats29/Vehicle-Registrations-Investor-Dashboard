# src/ui.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from src import data_fetch, data_clean
from charts import calculate_metrics, plot_trend, plot_top_manufacturers

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Vehicle Registration Investor Dashboard",
    page_icon="🚗",
    layout="wide",  # full-width layout
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS TO ELIMINATE CUTTING ---
st.markdown("""
    <style>
        /* Reduce top padding for the entire page */
        .block-container {
            padding-top: 0rem;  /* was 0.5rem or 1rem */
            padding-bottom: 1rem;
        }

        /* Remove extra top margin above the title */
        .css-1v3fvcr h1, .css-1v3fvcr h2, .css-1v3fvcr h3 {
            margin-top: 0rem !important;
        }

        /* Ensure metrics and charts start immediately */
        .stMetric {
            margin-top: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)
# --- HIDE STREAMLIT MENU, FOOTER, AND HEADER ---
st.markdown("""
    <style>
        /* Hide Streamlit header & menu */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- HEADER WRAPPER ---
with st.container():
    st.title("📊 Vehicle Registration Investor Dashboard")
    st.markdown("#### Track growth trends, market share, and performance by manufacturer.")




# --- DATA PATHS & GOOGLE DRIVE LINK ---
CLEANED_PATH = "src/data/processed/vehicle_data_cleaned.xlsx"
DRIVE_SHEET_ID = "1q4Qn32MBJ8IfKWUlHy5907cjRD-uiKu_"
DRIVE_CSV_URL = f"https://docs.google.com/spreadsheets/d/{DRIVE_SHEET_ID}/export?format=csv"

# --- LOAD DATA WITH CACHING ---
@st.cache_data
def load_data():
    if os.path.exists(CLEANED_PATH):
        df = pd.read_excel(CLEANED_PATH)
    else:
        df_raw, _ = data_fetch.fetch_from_url(DRIVE_CSV_URL)
        df = data_clean.clean_data(df_raw)
        os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
        df.to_excel(CLEANED_PATH, index=False)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

with st.spinner("Loading dataset, please wait..."):
    df = load_data()


# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")
min_date, max_date = df['Date'].min(), df['Date'].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)
vehicle_types = st.sidebar.multiselect(
    "Select Vehicle Categories",
    options=df['Vehicle_Type'].unique(),
    default=df['Vehicle_Type'].unique()
)
manufacturers = st.sidebar.multiselect(
    "Select Manufacturers",
    options=df['Manufacturer'].unique(),
    default=df['Manufacturer'].unique()
)

# --- DATA FILTERING ---
filtered_df = df[
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1])) &
    (df['Vehicle_Type'].isin(vehicle_types)) &
    (df['Manufacturer'].isin(manufacturers))
]

# --- METRICS ---
with st.expander("📈 Key Metrics", expanded=True):
    total, yoy, qoq = calculate_metrics(filtered_df)
    col1, col2, col3 = st.columns([1,1,1])
    col1.metric("Total Registrations", f"{total:,}")
    col2.metric("YoY Growth", f"{yoy:.2f}%")
    col3.metric("QoQ Growth", f"{qoq:.2f}%")

# --- TREND CHART ---
with st.expander("📅 Registration Trends Over Time", expanded=True):
    trend_fig = plot_trend(filtered_df)
    st.plotly_chart(trend_fig, use_container_width=True)

# --- TOP MANUFACTURERS ---
with st.expander("🏆 Top Manufacturers", expanded=True):
    top_manu_fig = plot_top_manufacturers(filtered_df)
    st.plotly_chart(top_manu_fig, use_container_width=True)

# --- DATA TABLE ---
with st.expander("📋 Detailed Data", expanded=False):
    st.dataframe(filtered_df.style.format({"Registrations": "{:,}"}), height=400)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit & Plotly | Data Source: Vahan / Google Drive CSV",
    unsafe_allow_html=True
)
