import streamlit as st
from data_loader import load_data, apply_filters
from kpi_engine import (
    get_on_time_rate,
    get_avg_delay,
    get_late_risk_ratio,
    get_mode_efficiency,
    get_country_delay,
)
from charts import (
    pie_delivery_class,
    bar_mode_delay,
    bar_region_delay,
    histogram_delay_gap,
    bar_segment_delay,
    bar_market_delay,
    choropleth_country_delay,
    bar_delivery_status,
)
from report_generator import download_report

st.set_page_config(
    page_title="APL Logistics – Supply Chain Dashboard",
    layout="wide",
    page_icon="🚚",
)

st.markdown(
    """
    <div style='background:#003DA5; padding:20px; border-radius:8px; margin-bottom:8px;'>
        <span style='color:#FFFFFF; font-size:30px; font-weight:700;'>🚚 APL Logistics</span><br>
        <span style='color:#A8C8E8; font-size:15px;'>
            Supply Chain Delivery Performance &amp; Delay Risk Analytics
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    "<hr style='border:none; border-top:2px solid #0073CF; margin:8px 0 16px 0;'>",
    unsafe_allow_html=True,
)


@st.cache_data
def get_data():
    return load_data()


df = get_data()

with st.sidebar:
    st.markdown(
        "<p style='color:#003DA5; font-size:18px; font-weight:700; margin-bottom:8px;'>APL Logistics</p>",
        unsafe_allow_html=True,
    )
    st.metric("Records", f"{len(df):,}")
    st.markdown(
        "<p style='color:#555555; font-size:12px; margin-top:8px;'>Data: 180,519 shipments</p>",
        unsafe_allow_html=True,
    )

fc1, fc2, fc3, fc4 = st.columns(4)
with fc1:
    shipping_modes = st.multiselect(
        "Shipping Mode",
        options=sorted(df["Shipping Mode"].dropna().unique()),
    )
with fc2:
    regions = st.multiselect(
        "Order Region",
        options=sorted(df["Order Region"].dropna().unique()),
    )
with fc3:
    markets = st.multiselect(
        "Market",
        options=sorted(df["Market"].dropna().unique()),
    )
with fc4:
    segments = st.multiselect(
        "Customer Segment",
        options=sorted(df["Customer Segment"].dropna().unique()),
    )
filtered_df = apply_filters(
    df,
    shipping_modes=shipping_modes or None,
    regions=regions or None,
    markets=markets or None,
    segments=segments or None,
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Delivery Overview", "⚠️ Delay Risk Analysis", "🚚 Shipping Mode Analysis", "🗺️ Regional Heatmap"]
)

with tab1:
    if len(filtered_df) == 0:
        st.warning("⚠️ No data found for selected filters. Please adjust your filter selection.")
        st.stop()

    on_time = get_on_time_rate(filtered_df)
    avg_delay = get_avg_delay(filtered_df)
    late_risk = get_late_risk_ratio(filtered_df)

    on_time_display = f"{on_time:.1f}%" if not (on_time != on_time) else "N/A"
    avg_delay_display = f"{avg_delay:.2f}" if not (avg_delay != avg_delay) else "N/A"
    late_risk_display = f"{late_risk:.1f}%" if not (late_risk != late_risk) else "N/A"

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f"""<div style='background:#FFFFFF; border-left:4px solid #003DA5; padding:15px;
                            border-radius:6px; box-shadow:0 1px 4px rgba(0,0,0,0.1); margin-bottom:8px;'>
                <p style='color:#888888; font-size:12px; margin:0 0 4px 0;'>On-Time Rate</p>
                <p style='color:#003DA5; font-size:28px; font-weight:700; margin:0;'>
                    {on_time_display}</p>
            </div>""",
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""<div style='background:#FFFFFF; border-left:4px solid #003DA5; padding:15px;
                            border-radius:6px; box-shadow:0 1px 4px rgba(0,0,0,0.1); margin-bottom:8px;'>
                <p style='color:#888888; font-size:12px; margin:0 0 4px 0;'>Avg Delay Days</p>
                <p style='color:#003DA5; font-size:28px; font-weight:700; margin:0;'>
                    {avg_delay_display}</p>
            </div>""",
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""<div style='background:#FFFFFF; border-left:4px solid #003DA5; padding:15px;
                            border-radius:6px; box-shadow:0 1px 4px rgba(0,0,0,0.1); margin-bottom:8px;'>
                <p style='color:#888888; font-size:12px; margin:0 0 4px 0;'>Late Risk Ratio</p>
                <p style='color:#003DA5; font-size:28px; font-weight:700; margin:0;'>
                    {late_risk_display}</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.plotly_chart(pie_delivery_class(filtered_df), use_container_width=True)
    with c2:
        fig_status = bar_delivery_status(filtered_df)
        st.plotly_chart(fig_status, use_container_width=True)

    st.plotly_chart(histogram_delay_gap(filtered_df), use_container_width=True)

    st.download_button(
        label="📥 Download Full Analysis Report",
        data=download_report(filtered_df),
        file_name="APL_Logistics_Report.txt",
        mime="text/plain",
    )

with tab2:
    if len(filtered_df) == 0:
        st.warning("⚠️ No data found for selected filters. Please adjust your filter selection.")
        st.stop()

    fig_region = bar_region_delay(filtered_df)

    fig_market = bar_market_delay(filtered_df)

    r1, r2 = st.columns([2, 1])
    with r1:
        st.plotly_chart(fig_region, use_container_width=True)
    with r2:
        st.plotly_chart(fig_market, use_container_width=True)

    fig_segment = bar_segment_delay(filtered_df)
    st.plotly_chart(fig_segment, use_container_width=True)

with tab3:
    if len(filtered_df) == 0:
        st.warning("⚠️ No data found for selected filters. Please adjust your filter selection.")
        st.stop()

    fig_mode = bar_mode_delay(filtered_df)
    st.plotly_chart(fig_mode, use_container_width=True)

    mode_eff = get_mode_efficiency(filtered_df)
    st.dataframe(
        mode_eff.style.format(
            {"Avg_Delay_Gap": "{:.2f}", "Late_Risk_Pct": "{:.1f}%"}
        ).set_properties(**{"background-color": "#E8F4FD", "color": "#003DA5"}),
        use_container_width=True,
    )

with tab4:
    if len(filtered_df) == 0:
        st.warning("⚠️ No data found for selected filters. Please adjust your filter selection.")
        st.stop()

    st.plotly_chart(choropleth_country_delay(filtered_df), use_container_width=True)

    country_delay = get_country_delay(filtered_df)
    top10 = country_delay.nlargest(10, "Avg_Delay_Gap")

    import plotly.express as px
    fig = px.bar(
        top10,
        x="Avg_Delay_Gap",
        y="Order Country",
        orientation="h",
        color_discrete_sequence=["#003DA5"],
    )
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(size=13),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        title="Top 10 Countries by Avg Delay",
    )
    ch1, ch2 = st.columns([1, 1])
    with ch1:
        st.plotly_chart(fig, use_container_width=True)
