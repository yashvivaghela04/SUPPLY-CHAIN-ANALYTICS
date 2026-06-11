import pandas as pd


def generate_report_text(df: pd.DataFrame) -> dict:
    if df is None or len(df) == 0:
        return {
            'summary': 'No data available for selected filters.',
            'eda_insights': ['No data available.'],
            'recommendations': ['No data available.'],
        }

    total_orders = len(df)
    on_time_rate = round(float((df['Delivery_Class'].isin(['On-Time', 'Early'])).sum() / total_orders * 100), 2) if total_orders > 0 else 0
    avg_delay = round(float(df['Delay_Gap'].mean()), 2) if not df['Delay_Gap'].empty else 0
    late_risk = round(float(df['Late_delivery_risk'].mean() * 100), 2) if not df['Late_delivery_risk'].empty else 0
    delayed_pct = round(float((df['Delivery_Class'] == 'Delayed').sum() / total_orders * 100), 2) if total_orders > 0 else 0
    early_pct = round(float((df['Delivery_Class'] == 'Early').sum() / total_orders * 100), 2) if total_orders > 0 else 0

    try:
        region_grp = df.groupby('Order Region')['Delay_Gap'].mean()
        top_region = region_grp.idxmax() if not region_grp.empty else 'N/A'
    except Exception:
        top_region = 'N/A'

    try:
        mode_grp = df.groupby('Shipping Mode')['Delay_Gap'].mean()
        top_mode = mode_grp.idxmax() if not mode_grp.empty else 'N/A'
        best_mode = mode_grp.idxmin() if not mode_grp.empty else 'N/A'
    except Exception:
        top_mode = 'N/A'
        best_mode = 'N/A'

    try:
        seg_grp = df.groupby('Customer Segment')['Late_delivery_risk'].mean()
        top_segment = seg_grp.idxmax() if not seg_grp.empty else 'N/A'
    except Exception:
        top_segment = 'N/A'

    try:
        market_grp = df.groupby('Market')['Delay_Gap'].mean()
        top_market = market_grp.idxmax() if not market_grp.empty else 'N/A'
    except Exception:
        top_market = 'N/A'

    summary = (
        f"APL Logistics processed {total_orders:,} shipments in this analysis period. "
        f"The overall on-time delivery rate stands at {on_time_rate}%, with an average delay gap of {avg_delay} days. "
        f"Late delivery risk affects {late_risk}% of all shipments, posing significant SLA compliance challenges. "
        f"The region with the highest average delay is {top_region}, while {top_mode} shows the worst shipping mode performance. "
        f"Immediate corrective action is recommended to improve delivery reliability across high-risk segments."
    )

    eda_insights = [
        f"Total orders analyzed: {total_orders:,}",
        f"On-time + early delivery rate: {on_time_rate}%",
        f"Delayed shipments: {delayed_pct}% | Early shipments: {early_pct}%",
        f"Average delivery delay gap: {avg_delay} days",
        f"Late delivery risk ratio: {late_risk}%",
        f"Highest delay region: {top_region}",
        f"Worst performing shipping mode: {top_mode}",
        f"Most at-risk customer segment: {top_segment}",
    ]

    recommendations = [
        f"Prioritize SLA review for {top_mode} shipping mode — highest average delay recorded.",
        f"Deploy additional logistics resources in {top_region} to reduce regional delay concentration.",
        f"Implement real-time delay alert systems for {top_segment} customer segment.",
        f"Negotiate revised delivery schedules with carriers operating in {top_market} market.",
        "Establish monthly delivery performance reviews with automated KPI dashboards for proactive management.",
    ]

    return {'summary': summary, 'eda_insights': eda_insights, 'recommendations': recommendations}


def download_report(df: pd.DataFrame) -> str:
    report = generate_report_text(df)

    lines = [
        "=" * 70,
        "APL LOGISTICS – SUPPLY CHAIN PERFORMANCE REPORT",
        "=" * 70,
        "",
        "EXECUTIVE SUMMARY",
        "-" * 70,
        report['summary'],
        "",
        "EDA INSIGHTS",
        "-" * 70,
    ]

    for insight in report['eda_insights']:
        lines.append(f"  • {insight}")

    lines += [
        "",
        "RECOMMENDATIONS",
        "-" * 70,
    ]

    for i, rec in enumerate(report['recommendations'], 1):
        lines.append(f"  {i}. {rec}")

    lines += ["", "=" * 70]

    return "\n".join(lines)
