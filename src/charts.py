# src/charts.py
import pandas as pd
import plotly.express as px

def calculate_metrics(df):
    """Calculate total registrations, YoY growth, and QoQ growth."""
    if df.empty:
        return 0, 0.0, 0.0

    total = df['Registrations'].sum()

    # Ensure 'Date' column is datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # YoY Calculation
    df['Year'] = df['Date'].dt.year
    yearly = df.groupby('Year')['Registrations'].sum().sort_index()
    yoy = 0.0
    if len(yearly) > 1:
        yoy = ((yearly.iloc[-1] - yearly.iloc[-2]) / yearly.iloc[-2]) * 100

    # QoQ Calculation
    df['Quarter'] = df['Date'].dt.to_period('Q')
    quarterly = df.groupby('Quarter')['Registrations'].sum().sort_index()
    qoq = 0.0
    if len(quarterly) > 1:
        qoq = ((quarterly.iloc[-1] - quarterly.iloc[-2]) / quarterly.iloc[-2]) * 100

    return total, yoy, qoq

def plot_trend(df):
    """Create a line chart for registration trends over time."""
    if df.empty:
        return px.line(title="No data available for selected filters")

    trend_df = df.groupby('Date')['Registrations'].sum().reset_index()
    fig = px.line(
        trend_df,
        x='Date',
        y='Registrations',
        title="Vehicle Registrations Over Time",
        markers=True,
        line_shape='spline'
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        title_font=dict(size=18, color='#2c3e50'),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_top_manufacturers(df):
    """Create a bar chart for top manufacturers."""
    if df.empty:
        return px.bar(title="No data available for selected filters")

    manu_df = df.groupby('Manufacturer')['Registrations'].sum().reset_index()
    manu_df = manu_df.sort_values(by='Registrations', ascending=False).head(10)

    fig = px.bar(
        manu_df,
        x='Manufacturer',
        y='Registrations',
        title="Top Manufacturers by Registrations",
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
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig
