import plotly.express as px
import plotly.graph_objects as go

_BLUE = '#003DA5'
_LIGHT_BLUE = '#0073CF'
_ACCENT = '#E8F4FD'
_WHITE = '#FFFFFF'
_RED = '#E31837'
_MID_BLUE = '#5BA4CF'
_DARK_BLUE = '#1A3A6B'

_LAYOUT = dict(
    paper_bgcolor=_WHITE,
    plot_bgcolor=_WHITE,
    font=dict(size=13),
    margin=dict(l=40, r=40, t=60, b=40),
    showlegend=True,
)


def pie_delivery_class(df):
    counts = df['Delivery_Class'].value_counts().reset_index()
    counts.columns = ['Delivery_Class', 'Count']
    fig = px.pie(
        counts,
        names='Delivery_Class',
        values='Count',
        color_discrete_sequence=[_BLUE, _LIGHT_BLUE, _ACCENT],
        hole=0.4,
        title='Delivery Class Breakdown',
    )
    fig.update_traces(
        textinfo='label+percent',
        pull=[0.05 if v == 'Delayed' else 0 for v in counts['Delivery_Class']],
        textfont_size=13,
    )
    fig.update_layout(**_LAYOUT)
    return fig


def bar_mode_delay(df):
    grouped = df.groupby('Shipping Mode', as_index=False)['Delay_Gap'].mean()
    grouped = grouped.sort_values('Delay_Gap')
    fig = px.bar(
        grouped,
        x='Delay_Gap',
        y='Shipping Mode',
        orientation='h',
        color='Delay_Gap',
        color_continuous_scale=[_ACCENT, _BLUE],
        text_auto='.2f',
        title='Shipping Mode vs Avg Delay Gap',
        labels={'Delay_Gap': 'Avg Delay (days)', 'Shipping Mode': 'Shipping Mode'},
    )
    fig.update_layout(**_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def bar_region_delay(df):
    data = df.groupby('Order Region')['Delay_Gap'].mean().reset_index()
    data.columns = ['Region', 'Avg_Delay']
    data = data.sort_values('Avg_Delay', ascending=False)
    fig = px.bar(data, x='Region', y='Avg_Delay', color='Avg_Delay',
                 color_continuous_scale=['#AED6F1', '#2471A3', '#003DA5', '#1A1A6E'],
                 text_auto='.2f', title='Avg Delay Gap by Order Region')
    fig.update_layout(**_LAYOUT)
    fig.update_xaxes(tickangle=45, showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def histogram_delay_gap(df):
    fig = px.histogram(
        df,
        x='Delay_Gap',
        color_discrete_sequence=[_BLUE],
        nbins=15,
        title='Delivery Delay Gap Distribution',
        labels={'Delay_Gap': 'Delay Gap (days)', 'count': 'Number of Orders'},
    )
    fig.add_vline(
        x=0,
        line_dash='dash',
        line_color=_RED,
        annotation_text='On-Time Boundary',
        annotation_position='top right',
    )
    fig.update_layout(**_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, gridcolor='#F0F0F0')
    return fig


def bar_segment_delay(df):
    data = df.groupby('Customer Segment')['Delay_Gap'].mean().reset_index()
    data.columns = ['Segment', 'Avg_Delay']
    fig = px.bar(data, x='Segment', y='Avg_Delay', color='Segment',
                 color_discrete_sequence=['#003DA5', '#E31837', '#27AE60'],
                 text_auto='.2f', title='Avg Delay Gap by Customer Segment')
    fig.update_layout(**_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def bar_market_delay(df):
    data = df.groupby('Market')['Delay_Gap'].mean().reset_index()
    data.columns = ['Market', 'Avg_Delay']
    fig = px.bar(data, x='Market', y='Avg_Delay', color='Market',
                 color_discrete_sequence=['#003DA5', '#E31837', '#27AE60', '#F39C12', '#8E44AD'],
                 text_auto='.2f', title='Avg Delay Gap by Market')
    fig.update_layout(**_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def choropleth_country_delay(df):
    data = df.groupby('Order Country')['Delay_Gap'].mean().reset_index()
    data.columns = ['Country', 'Avg_Delay']
    fig = px.choropleth(data, locations='Country', locationmode='country names',
                        color='Avg_Delay',
                        color_continuous_scale=['#D6EAF8', '#2471A3', '#003DA5', '#1A1A6E'],
                        title='Avg Delivery Delay by Country',
                        labels={'Avg_Delay': 'Avg Delay (days)'})
    fig.update_layout(**_LAYOUT, geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'))
    return fig


def bar_delivery_status(df):
    counts = df['Delivery Status'].value_counts().reset_index()
    counts.columns = ['Status', 'Count']
    color_map = {'Late delivery': '#E31837', 'Advance shipping': '#003DA5', 'Shipping on time': '#27AE60', 'Shipping canceled': '#F39C12'}
    fig = px.bar(counts, x='Status', y='Count', color='Status',
                 color_discrete_map=color_map, text='Count',
                 title='Orders by Delivery Status')
    fig.update_traces(texttemplate='%{text:.3s}', textposition='outside')
    fig.update_layout(**_LAYOUT)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig
