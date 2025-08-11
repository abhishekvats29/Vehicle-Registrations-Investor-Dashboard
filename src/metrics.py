# src/metrics.py
import pandas as pd

def yearly_aggregates(df: pd.DataFrame, groupby_cols=None, value_col="Registrations"):
    """
    Aggregate by Year + groupby_cols (list or None) and compute YoY % change.
    Returns a dataframe with columns: Year, <group cols...>, Total, YoY_pct
    """
    if groupby_cols is None:
        groupby_cols = []

    gb = ['Year'] + list(groupby_cols)
    agg = df.groupby(gb, as_index=False)[value_col].sum().rename(columns={value_col: 'Total'})
    # Compute YoY percent change for each group
    agg = agg.sort_values(gb)
    # Percent change within each groupby_cols partition
    if groupby_cols:
        agg['YoY_pct'] = agg.groupby(groupby_cols)['Total'].pct_change(periods=1) * 100
    else:
        agg['YoY_pct'] = agg['Total'].pct_change(periods=1) * 100
    return agg

def quarterly_aggregates(df: pd.DataFrame, groupby_cols=None, value_col="Registrations"):
    """
    Aggregate by Quarter + groupby_cols and compute QoQ % change.
    Quarter column in df expected as string like '2023Q2' or we can compute from Date.
    Returns columns: Quarter (period), Year, Quarter_Num, <group cols...>, Total, QoQ_pct
    """
    df = df.copy()
    if groupby_cols is None:
        groupby_cols = []

    # Create a quarter period column if not present
    if 'Quarter' not in df.columns:
        df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)

    # Extract Year and quarter number
    df['Year'] = df['Date'].dt.year
    df['Quarter_Num'] = df['Date'].dt.quarter
    gb = ['Quarter', 'Year', 'Quarter_Num'] + list(groupby_cols)
    agg = df.groupby(gb, as_index=False)[value_col].sum().rename(columns={value_col: 'Total'})
    agg = agg.sort_values(['Year', 'Quarter_Num'] + list(groupby_cols))

    if groupby_cols:
        agg['QoQ_pct'] = agg.groupby(groupby_cols)['Total'].pct_change(periods=1) * 100
    else:
        agg['QoQ_pct'] = agg['Total'].pct_change(periods=1) * 100

    return agg

def top_n_manufacturers(df: pd.DataFrame, n=10, timeframe=None):
    """
    Return top-n manufacturers by total registrations in the given timeframe (tuple of start/end dates) or whole df.
    """
    df2 = df.copy()
    if timeframe is not None:
        start, end = timeframe
        df2 = df2[(df2['Date'] >= start) & (df2['Date'] <= end)]
    by_maker = df2.groupby('Manufacturer', as_index=False)['Registrations'].sum().rename(columns={'Registrations': 'Total'})
    return by_maker.sort_values('Total', ascending=False).head(n)
