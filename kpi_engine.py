import pandas as pd


def get_on_time_rate(df):
    return (df['Delivery_Class'].isin(['On-Time', 'Early'])).mean() * 100


def get_avg_delay(df):
    return df['Delay_Gap'].mean()


def get_late_risk_ratio(df):
    return (df['Late_delivery_risk'] == 1).mean() * 100


def get_mode_efficiency(df):
    grouped = df.groupby('Shipping Mode').agg(
        Avg_Delay_Gap=('Delay_Gap', 'mean'),
        Order_Count=('Delay_Gap', 'count'),
        Late_Risk_Pct=('Late_delivery_risk', lambda x: (x == 1).mean() * 100)
    ).reset_index()
    return grouped


def get_regional_delay(df):
    grouped = df.groupby('Order Region').agg(
        Avg_Delay_Gap=('Delay_Gap', 'mean'),
        Late_Risk_Pct=('Late_delivery_risk', lambda x: (x == 1).mean() * 100)
    ).reset_index()
    return grouped


def get_market_delay(df):
    grouped = df.groupby('Market').agg(
        Avg_Delay_Gap=('Delay_Gap', 'mean'),
        Late_Risk_Pct=('Late_delivery_risk', lambda x: (x == 1).mean() * 100)
    ).reset_index()
    return grouped


def get_segment_delay(df):
    grouped = df.groupby('Customer Segment').agg(
        Avg_Delay_Gap=('Delay_Gap', 'mean'),
        Late_Risk_Pct=('Late_delivery_risk', lambda x: (x == 1).mean() * 100)
    ).reset_index()
    return grouped


def get_delivery_class_dist(df):
    counts = df['Delivery_Class'].value_counts()
    return {
        'Early': int(counts.get('Early', 0)),
        'On-Time': int(counts.get('On-Time', 0)),
        'Delayed': int(counts.get('Delayed', 0))
    }


def get_country_delay(df):
    grouped = df.groupby('Order Country').agg(
        Avg_Delay_Gap=('Delay_Gap', 'mean'),
        Order_Count=('Delay_Gap', 'count')
    ).reset_index()
    return grouped
