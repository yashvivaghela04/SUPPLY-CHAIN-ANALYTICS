import pandas as pd


def load_data():
    df = pd.read_csv('data/APL_Logistics.csv', encoding='latin1')

    df = df.dropna(subset=['Customer Lname', 'Customer Zipcode'], how='all')

    df['Customer Lname'] = df['Customer Lname'].fillna('Unknown')

    df['Customer Country'] = df['Customer Country'].replace('EE. UU.', 'United States')

    df['Delay_Gap'] = df['Days for shipping (real)'] - df['Days for shipment (scheduled)']

    df['Delivery_Class'] = df['Delay_Gap'].apply(
        lambda x: 'Early' if x < 0 else ('On-Time' if x == 0 else 'Delayed')
    )

    return df


def apply_filters(df, shipping_modes=None, regions=None, markets=None, segments=None):
    if shipping_modes:
        df = df[df['Shipping Mode'].isin(shipping_modes)]
    if regions:
        df = df[df['Order Region'].isin(regions)]
    if markets:
        df = df[df['Market'].isin(markets)]
    if segments:
        df = df[df['Customer Segment'].isin(segments)]
    return df
