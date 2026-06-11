from datetime import date
from data_loader import load_data


def build_summary(df):
    today = date.today().strftime("%B %d, %Y")
    total = len(df)

    # KPIs
    on_time_pct = round((df['Delivery_Class'].isin(['On-Time', 'Early'])).sum() / total * 100, 2)
    delayed_pct = round((df['Delivery_Class'] == 'Delayed').sum() / total * 100, 2)
    avg_delay = round(df['Delay_Gap'].mean(), 2)
    late_risk_pct = round(df['Late_delivery_risk'].mean() * 100, 2)
    canceled_pct = round((df['Delivery Status'] == 'Shipping canceled').sum() / total * 100, 2)

    # Aggregations
    mode_avg = df.groupby('Shipping Mode')['Delay_Gap'].mean().round(2).sort_values(ascending=False)
    region_avg = df.groupby('Order Region')['Delay_Gap'].mean().round(2).sort_values(ascending=False)
    market_avg = df.groupby('Market')['Delay_Gap'].mean().round(2).sort_values(ascending=False)
    segment_avg = df.groupby('Customer Segment')['Delay_Gap'].mean().round(2).sort_values(ascending=False)

    top3_regions = region_avg.head(3)
    top2_modes = mode_avg.head(2)
    worst_market = market_avg.index[0]
    worst_market_val = market_avg.iloc[0]
    worst_segment = segment_avg.index[0]
    worst_segment_val = segment_avg.iloc[0]
    best_mode = mode_avg.index[-1]
    best_mode_val = mode_avg.iloc[-1]

    lines = []

    def divider(char="=", n=70):
        lines.append(char * n)

    def h2(text):
        lines.append("")
        lines.append(text)
        lines.append("-" * 70)

    def bullet(items):
        for item in items:
            lines.append(f"  • {item}")

    def numbered(items):
        for i, item in enumerate(items, 1):
            lines.append(f"  {i}. {item}")

    # Title block
    divider()
    lines.append("EXECUTIVE SUMMARY")
    lines.append("APL LOGISTICS — SUPPLY CHAIN DELIVERY PERFORMANCE")
    divider()
    lines.append(f"Author : Yashvi Chunilal Vaghela | Data Analytics Project | Unified Mentor")
    lines.append(f"Date   : {today}")

    # Section 1 – Business Context
    h2("SECTION 1 — BUSINESS CONTEXT")
    lines.append("")
    lines.append(
        f"APL Logistics manages a global shipment portfolio of {total:,} orders spanning "
        f"multiple shipping modes, markets, and customer segments, where consistent on-time "
        f"delivery is directly tied to SLA compliance and customer retention."
    )
    lines.append("")
    lines.append(
        f"A significant proportion of shipments — {delayed_pct}% — are currently delayed "
        f"beyond scheduled delivery windows, creating downstream cost exposure through "
        f"penalty clauses, expediting charges, and erosion of customer trust."
    )
    lines.append("")
    lines.append(
        "This summary identifies the highest-risk operational areas and prescribes targeted "
        "interventions to improve delivery reliability and reduce systemic delay concentration."
    )

    # Section 2 – Key Metrics
    h2("SECTION 2 — KEY METRICS AT A GLANCE")
    lines.append("")
    lines.append(f"  {'KPI':<38} {'VALUE':>10}")
    lines.append(f"  {'-'*38} {'-'*10}")
    lines.append(f"  {'Total Shipments Analysed':<38} {total:>10,}")
    lines.append(f"  {'On-Time / Early Delivery Rate':<38} {on_time_pct:>9.2f}%")
    lines.append(f"  {'Delayed Shipment Rate':<38} {delayed_pct:>9.2f}%")
    lines.append(f"  {'Average Delay Gap':<38} {str(avg_delay) + ' days':>10}")
    lines.append(f"  {'Late Delivery Risk Ratio':<38} {late_risk_pct:>9.2f}%")
    lines.append(f"  {'Cancelled Shipment Rate':<38} {canceled_pct:>9.2f}%")

    # Section 3 – Critical Findings
    h2("SECTION 3 — CRITICAL FINDINGS")
    lines.append("")
    bullet([
        f"{delayed_pct}% of all shipments ({int(delayed_pct/100*total):,} orders) were "
        f"delivered late, with a mean delay of {avg_delay} days — indicating a systemic "
        f"delivery performance deficit.",

        f"Late delivery risk is elevated at {late_risk_pct}% of the portfolio, with the "
        f"{worst_segment} segment recording the highest average delay of "
        f"{worst_segment_val:.2f} days.",

        f"Shipping mode performance varies significantly: {top2_modes.index[0]} is the "
        f"worst mode at {top2_modes.iloc[0]:.2f} days avg delay vs {best_mode} at "
        f"{best_mode_val:.2f} days — a gap of "
        f"{abs(round(top2_modes.iloc[0] - best_mode_val, 2)):.2f} days.",

        f"Regional delay is concentrated in {list(top3_regions.index)[0]} "
        f"({top3_regions.iloc[0]:.2f} days), {list(top3_regions.index)[1]} "
        f"({top3_regions.iloc[1]:.2f} days), and {list(top3_regions.index)[2]} "
        f"({top3_regions.iloc[2]:.2f} days).",

        f"The {worst_market} market records the highest market-level avg delay of "
        f"{worst_market_val:.2f} days, suggesting carrier contract gaps or infrastructure "
        f"constraints in that geography.",
    ])

    # Section 4 – High Risk Areas
    h2("SECTION 4 — HIGH RISK AREAS")
    lines.append("")
    lines.append("  Top 3 High-Delay Regions:")
    for rank, (region, val) in enumerate(top3_regions.items(), 1):
        lines.append(f"    {rank}. {region:<35} {val:.2f} days avg delay")
    lines.append("")
    lines.append("  Top 2 High-Delay Shipping Modes:")
    for rank, (mode, val) in enumerate(top2_modes.items(), 1):
        lines.append(f"    {rank}. {mode:<25} {val:.2f} days avg delay")

    # Section 5 – Immediate Action Items
    h2("SECTION 5 — IMMEDIATE ACTION ITEMS")
    lines.append("")
    numbered([
        f"Suspend or reprioritise {top2_modes.index[0]} mode orders for high-value accounts "
        f"until carrier SLA compliance is confirmed and corrective measures are in place.",

        f"Activate delay escalation protocols for all orders destined to "
        f"{list(top3_regions.index)[0]} and {list(top3_regions.index)[1]}, including "
        f"real-time tracking alerts and proactive customer communication.",

        f"Flag {worst_segment} segment orders for expedited review at dispatch; assign "
        f"dedicated account managers to handle delay resolution for this segment.",
    ])

    # Section 6 – Strategic Recommendations
    h2("SECTION 6 — STRATEGIC RECOMMENDATIONS")
    lines.append("")
    numbered([
        f"Carrier Contract Renegotiation ({top2_modes.index[0]} Mode): Conduct a full "
        f"performance audit of carriers operating under the {top2_modes.index[0]} mode. "
        f"Introduce penalty clauses for delays exceeding {avg_delay:.0f} days and incentive "
        f"structures rewarding consistent on-time delivery above the current {on_time_pct}% "
        f"baseline. Set a target on-time rate of 85%+ within two quarters.",

        f"Regional Logistics Investment ({list(top3_regions.index)[0]} & "
        f"{list(top3_regions.index)[1]}): Establish dedicated regional logistics hubs or "
        f"partner with local 3PL providers in the highest-delay regions to absorb last-mile "
        f"delivery pressure. Deploy demand forecasting models to pre-position inventory "
        f"and reduce shipment lead times by an estimated 15-20%.",

        f"Predictive Delay Monitoring Platform: Invest in a real-time delay risk scoring "
        f"system that flags high-risk orders at placement stage based on mode, region, "
        f"and segment profiles. Integrate with the order management system to trigger "
        f"automatic re-routing for orders exceeding a configurable delay risk threshold, "
        f"targeting a reduction in the {late_risk_pct}% late delivery risk ratio to below 30%.",
    ])

    # Section 7 – Expected Impact
    h2("SECTION 7 — EXPECTED IMPACT")
    lines.append("")
    lines.append(
        f"Implementing the above recommendations is projected to improve the overall on-time "
        f"delivery rate from the current {on_time_pct}% toward an 85%+ target within two "
        f"to three operational quarters, reducing the delayed shipment rate from {delayed_pct}% "
        f"to below 15%."
    )
    lines.append("")
    lines.append(
        f"Targeted intervention in the top three delayed regions and the {top2_modes.index[0]} "
        f"shipping mode alone covers the majority of the delay exposure; resolving these "
        f"two vectors is expected to deliver a measurable reduction in SLA penalty costs "
        f"and a corresponding improvement in customer satisfaction scores."
    )
    lines.append("")
    lines.append(
        "Deployment of predictive delay monitoring will shift the operational posture from "
        "reactive problem resolution to proactive risk management, enabling logistics teams "
        "to intervene before delays occur rather than responding after the fact."
    )

    lines.append("")
    divider()
    lines.append("END OF EXECUTIVE SUMMARY")
    divider()

    return "\n".join(lines)


if __name__ == "__main__":
    df = load_data()
    summary = build_summary(df)
    output_path = "APL_Logistics_Executive_Summary.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print("Executive summary saved successfully!")
