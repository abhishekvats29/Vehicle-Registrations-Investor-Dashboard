# src/charts.py
import pandas as pd
import plotly.express as px

# -----------------------------
# Metrics calculation
# -----------------------------
def calculate_metrics(df):
    """
    Calculate total registrations, YoY growth, and QoQ growth.
    Returns: total, yoy (%), qoq (%)
    """
    if df.empty or 'Registrations' not in df.columns:
        return 0, 0.0, 0.0

    total = df['Registrations'].sum()

    # Ensure 'Date' column is datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    if df.empty:
        return total, 0.0, 0.0

    # YoY Calculation
    df['Year'] = df['Date'].dt.year
    yearly = df.groupby('Year')['Registrations'].sum().sort_index()
    yoy = 0.0
    if len(yearly) > 1 and yearly.iloc[-2] != 0:
        yoy = ((yearly.iloc[-1] - yearly.iloc[-2]) / yearly.iloc[-2]) * 100

    # QoQ Calculation
    df['Quarter'] = df['Date'].dt.to_period('Q')
    quarterly = df.groupby('Quarter')['Registrations'].sum().sort_index()
    qoq = 0.0
    if len(quarterly) > 1 and quarterly.iloc[-2] != 0:
        qoq = ((quarterly.iloc[-1] - quarterly.iloc[-2]) / quarterly.iloc[-2]) * 100

    return total, yoy, qoq

# -----------------------------
# Trend chart
# -----------------------------
def plot_trend(df):
    """
    Line chart for vehicle registrations over time.
    """
    if df.empty or 'Date' not in df.columns or 'Registrations' not in df.columns:
        return px.line(title="No data available for selected filters")

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    if df.empty:
        return px.line(title="No data available for selected filters")

    trend_df = df.groupby('Date')['Registrations'].sum().reset_index()

    fig = px.line(
        trend_df,
        x='Date',
        y='Registrations',
        title="📈 Vehicle Registrations Over Time",
        markers=True,
        line_shape='spline'
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        title_font=dict(size=18, color='#2c3e50'),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Date",
        yaxis_title="Registrations"
    )

    return fig

# -----------------------------
# Top manufacturers chart
# -----------------------------
def plot_top_manufacturers(df):
    """
    Bar chart for top 10 manufacturers by registrations.
    """
    if df.empty or 'Manufacturer' not in df.columns or 'Registrations' not in df.columns:
        return px.bar(title="No data available for selected filters")

    manu_df = df.groupby('Manufacturer')['Registrations'].sum().reset_index()
    manu_df = manu_df.sort_values(by='Registrations', ascending=False).head(10)

    fig = px.bar(
        manu_df,
        x='Manufacturer',
        y='Registrations',
        title="🏭 Top Manufacturers by Registrations",
        text='Registrations',
        color='Registrations',
        color_continuous_scale='Blues'
    )

    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        title_font=dict(size=18, color='#2c3e50'),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Manufacturer",
        yaxis_title="Registrations"
    )

    return fig
