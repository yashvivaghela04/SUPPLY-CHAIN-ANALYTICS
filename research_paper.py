from datetime import date
from data_loader import load_data


def build_paper(df):
    today = date.today().strftime("%B %d, %Y")
    total = len(df)

    # --- Section 5 stats ---
    on_time_n = (df['Delivery_Class'].isin(['On-Time', 'Early'])).sum()
    on_time_pct = round(on_time_n / total * 100, 2)
    delayed_pct = round((df['Delivery_Class'] == 'Delayed').sum() / total * 100, 2)
    early_pct = round((df['Delivery_Class'] == 'Early').sum() / total * 100, 2)
    on_time_only_pct = round((df['Delivery_Class'] == 'On-Time').sum() / total * 100, 2)
    avg_delay = round(df['Delay_Gap'].mean(), 2)
    late_risk_pct = round(df['Late_delivery_risk'].mean() * 100, 2)

    mode_avg = df.groupby('Shipping Mode')['Delay_Gap'].mean().round(2).sort_values(ascending=False)
    region_avg = df.groupby('Order Region')['Delay_Gap'].mean().round(2).sort_values(ascending=False)
    market_avg = df.groupby('Market')['Delay_Gap'].mean().round(2).sort_values(ascending=False)
    segment_avg = df.groupby('Customer Segment')['Delay_Gap'].mean().round(2).sort_values(ascending=False)

    top3_regions = region_avg.head(3)
    worst_mode = mode_avg.index[0]
    worst_mode_val = mode_avg.iloc[0]
    best_mode = mode_avg.index[-1]
    best_mode_val = mode_avg.iloc[-1]
    worst_market = market_avg.index[0]
    worst_market_val = market_avg.iloc[0]
    worst_segment = segment_avg.index[0]
    worst_segment_val = segment_avg.iloc[0]

    # --- Build text ---
    lines = []

    def h1(text):
        lines.append("=" * 75)
        lines.append(text)
        lines.append("=" * 75)

    def h2(text):
        lines.append("")
        lines.append(text)
        lines.append("-" * 75)

    def para(*paragraphs):
        for p in paragraphs:
            lines.append("")
            lines.append(p)

    def bullet(items):
        for item in items:
            lines.append(f"  • {item}")

    def numbered(items):
        for i, item in enumerate(items, 1):
            lines.append(f"  {i}. {item}")

    # Title block
    h1("DELIVERY PERFORMANCE, DELAY RISK, AND LOGISTICS EFFICIENCY ANALYSIS")
    h1("IN GLOBAL SUPPLY CHAIN OPERATIONS")
    lines.append("")
    lines.append(f"Author : Yashvi Chunilal Vaghela | Data Analytics Project | Unified Mentor")
    lines.append(f"Date   : {today}")
    lines.append(f"Subject: Supply Chain Performance Research Report")

    # Section 1 – Abstract
    h2("SECTION 1 — ABSTRACT")
    para(
        "This study presents a comprehensive analysis of delivery performance, delay risk, and "
        "logistics efficiency across global supply chain operations using transactional shipment "
        "data from APL Logistics. The dataset encompasses {:,} shipment records spanning multiple "
        "shipping modes, geographic regions, and customer segments, enabling a statistically "
        "robust examination of operational patterns.".format(total),

        "Our analysis reveals that {:.1f}% of shipments were delivered on time or early, while "
        "{:.1f}% experienced delays, with an average delay gap of {:.2f} days across the entire "
        "portfolio. Late delivery risk affects {:.1f}% of all shipments, posing material "
        "challenges to SLA compliance and customer satisfaction.".format(
            on_time_pct, delayed_pct, avg_delay, late_risk_pct),

        "Shipping mode, order region, and market segment are identified as primary determinants "
        "of delivery variance, with {} exhibiting the highest average delay of {:.2f} days and "
        "{} performing best at {:.2f} days average delay gap.".format(
            worst_mode, worst_mode_val, best_mode, best_mode_val),

        "The findings support targeted operational interventions including carrier renegotiation, "
        "regional resource reallocation, and real-time delay monitoring systems to improve "
        "overall delivery reliability and reduce SLA breach rates across high-risk segments.",

        "Actionable recommendations derived from the data analysis are presented to guide "
        "logistics managers toward evidence-based decision-making and continuous performance "
        "improvement."
    )

    # Section 2 – Introduction
    h2("SECTION 2 — INTRODUCTION")
    para(
        "Global supply chain operations face increasing pressure to meet stringent delivery "
        "commitments in the face of rising shipment volumes, diverse geographic spread, and "
        "complex multi-modal logistics networks. Delivery delays impose direct costs through "
        "SLA penalties, customer churn, and elevated operational expenditure, while also "
        "generating indirect costs through reputational damage and lost future business. "
        "Understanding the structural drivers of delivery risk is therefore a strategic "
        "priority for logistics operators seeking to maintain competitive service levels.",

        "This study leverages a large-scale operational dataset from APL Logistics to quantify "
        "delivery performance across key dimensions including shipping mode, order region, "
        "market, and customer segment. The primary objectives are: (1) to establish baseline "
        "delivery performance metrics across the full shipment portfolio; (2) to identify the "
        "shipping modes, regions, and segments most susceptible to delay; (3) to quantify late "
        "delivery risk concentration; and (4) to derive targeted, data-driven recommendations "
        "for improving logistics efficiency and reducing delay rates. The analysis applies "
        "exploratory data analysis techniques and descriptive statistics to surface actionable "
        "insights directly from the operational record."
    )

    # Section 3 – Dataset Description
    h2("SECTION 3 — DATASET DESCRIPTION")
    para(
        "The dataset comprises {:,} shipment records exported from APL Logistics' operational "
        "transaction system, covering orders processed across multiple years of global "
        "operations. Each record contains approximately 40 data fields capturing the full "
        "lifecycle of a shipment from order placement to final delivery.".format(total),

        "Key fields used in this analysis include:"
    )
    lines.append("")
    bullet([
        "Days for shipping (real)      — Actual number of days taken to ship the order",
        "Days for shipment (scheduled) — Originally promised shipping duration",
        "Delivery Status               — Categorical label: Late delivery, Advance shipping,",
        "                                Shipping on time, Shipping canceled",
        "Late_delivery_risk            — Binary flag (0/1) indicating predicted late delivery",
        "Shipping Mode                 — Transport method: First Class, Second Class,",
        "                                Standard Class, Same Day",
        "Order Region                  — Geographic region of the destination order",
        "Order Country                 — Destination country at order level",
        "Market                        — High-level market grouping (e.g., Europe, LATAM, Pacific Asia)",
        "Customer Segment              — Commercial classification: Consumer, Corporate, Home Office",
        "Order Item Quantity           — Units ordered per line item",
        "Sales                         — Revenue value per order",
        "Order Profit Per Order        — Net profit recorded per order",
        "Delay_Gap (engineered)        — Computed: Days for shipping (real) minus Days for",
        "                                shipment (scheduled); positive = delayed",
        "Delivery_Class (engineered)   — Derived: Early (Delay_Gap < 0), On-Time (= 0),",
        "                                Delayed (> 0)",
    ])
    para(
        "Data quality processing included removal of records with entirely null customer "
        "identifiers and standardisation of the customer country field (e.g., 'EE. UU.' "
        "normalised to 'United States'). No imputation was applied to the core delay "
        "and delivery fields to preserve the integrity of performance metrics."
    )

    # Section 4 – Methodology
    h2("SECTION 4 — METHODOLOGY")
    para(
        "The analytical pipeline follows four sequential stages: data ingestion and cleaning, "
        "feature engineering, exploratory data analysis, and insight synthesis.",

        "Data Cleaning: Raw CSV data is loaded with latin-1 encoding to accommodate "
        "non-ASCII characters present in customer name fields. Records are filtered to "
        "exclude rows where both customer last name and postal code are simultaneously "
        "null, as these represent incomplete or test transactions. Customer country values "
        "are standardised to a consistent English representation.",

        "Feature Engineering: Two derived columns are constructed to support performance "
        "analysis. The Delay_Gap column is computed as the arithmetic difference between "
        "actual and scheduled shipping days:",
    )
    lines.append("")
    lines.append("    Delay_Gap = Days_for_shipping_real − Days_for_shipment_scheduled")
    lines.append("")
    para(
        "A positive Delay_Gap indicates the shipment arrived later than scheduled; zero "
        "indicates on-time delivery; negative values indicate early arrival. The "
        "Delivery_Class column encodes this as a categorical label: 'Early' (Delay_Gap < 0), "
        "'On-Time' (Delay_Gap = 0), and 'Delayed' (Delay_Gap > 0).",

        "Exploratory Data Analysis: Aggregations are performed across shipping mode, order "
        "region, market, and customer segment dimensions using grouped mean calculations "
        "on Delay_Gap and Late_delivery_risk. On-time rate is computed as the proportion "
        "of records classified as 'Early' or 'On-Time'. All percentage metrics are rounded "
        "to two decimal places. Top-N rankings are derived from sorted aggregation results.",

        "Insight Synthesis: Key findings are extracted by identifying the highest and lowest "
        "performing categories within each analytical dimension. Recommendations are formulated "
        "by mapping high-risk categories to operational levers available to logistics managers."
    )

    # Section 5 – EDA
    h2("SECTION 5 — EXPLORATORY DATA ANALYSIS")

    lines.append("")
    lines.append("5.1  Overall Delivery Performance")
    lines.append("-" * 50)
    lines.append("")
    bullet([
        f"Total shipments analysed          : {total:,}",
        f"On-time or early delivery rate    : {on_time_pct}%",
        f"On-time only (Delay_Gap = 0)      : {on_time_only_pct}%",
        f"Early deliveries (Delay_Gap < 0)  : {early_pct}%",
        f"Delayed shipments (Delay_Gap > 0) : {delayed_pct}%",
        f"Average delay gap                 : {avg_delay} days",
        f"Late delivery risk ratio          : {late_risk_pct}%",
    ])

    lines.append("")
    lines.append("5.2  Shipping Mode Analysis — Avg Delay Gap (days)")
    lines.append("-" * 50)
    lines.append("")
    for mode, val in mode_avg.items():
        lines.append(f"  {mode:<22} {val:>7.2f} days")

    lines.append("")
    lines.append("5.3  Regional Analysis — Top 3 Most Delayed Regions")
    lines.append("-" * 50)
    lines.append("")
    for rank, (region, val) in enumerate(top3_regions.items(), 1):
        lines.append(f"  {rank}. {region:<35} {val:.2f} days avg delay")
    lines.append("")
    lines.append("  Full regional breakdown:")
    for region, val in region_avg.items():
        lines.append(f"    {region:<35} {val:.2f} days")

    lines.append("")
    lines.append("5.4  Market Analysis — Avg Delay Gap by Market")
    lines.append("-" * 50)
    lines.append("")
    for market, val in market_avg.items():
        lines.append(f"  {market:<25} {val:>7.2f} days")

    lines.append("")
    lines.append("5.5  Customer Segment Analysis — Avg Delay Gap")
    lines.append("-" * 50)
    lines.append("")
    for seg, val in segment_avg.items():
        lines.append(f"  {seg:<20} {val:>7.2f} days")

    # Section 6 – Key Findings
    h2("SECTION 6 — KEY FINDINGS")
    lines.append("")
    bullet([
        f"Delivery reliability gap: Only {on_time_pct}% of shipments meet or exceed scheduled "
        f"delivery dates, while {delayed_pct}% are delayed — indicating a systemic performance "
        f"deficit requiring structural operational intervention.",

        f"Shipping mode is a primary delay driver: {worst_mode} is the worst-performing mode "
        f"with an average delay gap of {worst_mode_val:.2f} days, compared to {best_mode} "
        f"at {best_mode_val:.2f} days, a differential of "
        f"{abs(round(worst_mode_val - best_mode_val, 2)):.2f} days.",

        f"Regional concentration of delays: The top three most delayed regions — "
        f"{list(top3_regions.index)[0]}, {list(top3_regions.index)[1]}, and "
        f"{list(top3_regions.index)[2]} — account for disproportionate delay exposure and "
        f"require targeted resource allocation.",

        f"Market-level risk: {worst_market} market records the highest average delay gap of "
        f"{worst_market_val:.2f} days, suggesting carrier contract terms or regional "
        f"infrastructure constraints require re-evaluation.",

        f"Segment vulnerability: The {worst_segment} segment experiences the highest average "
        f"delay of {worst_segment_val:.2f} days and a late delivery risk concentration of "
        f"{late_risk_pct}%, warranting dedicated SLA monitoring and proactive communication "
        f"protocols.",
    ])

    # Section 7 – Recommendations
    h2("SECTION 7 — RECOMMENDATIONS")
    lines.append("")
    numbered([
        f"Carrier Performance Review for {worst_mode}: Initiate an immediate SLA audit and "
        f"renegotiation process with carriers operating under the {worst_mode} shipping mode, "
        f"which records the highest average delay of {worst_mode_val:.2f} days. Introduce "
        f"performance-based penalty clauses and milestone-linked incentives.",

        f"Regional Logistics Reinforcement in {list(top3_regions.index)[0]}: Deploy additional "
        f"warehouse capacity, last-mile delivery partners, and demand forecasting resources in "
        f"{list(top3_regions.index)[0]}, identified as the single highest-delay region. "
        f"Establish a regional delay task force with monthly KPI reviews.",

        f"Real-Time Delay Alert System for {worst_segment} Segment: Implement automated "
        f"in-transit monitoring and proactive customer notification for orders in the "
        f"{worst_segment} segment. Integrate predictive delay scoring at order placement to "
        f"enable pre-emptive re-routing.",

        f"Market Contract Renegotiation for {worst_market}: Review and restructure delivery "
        f"commitments and carrier agreements for the {worst_market} market, where average "
        f"delay stands at {worst_market_val:.2f} days. Explore alternative routing strategies "
        f"and regional hub consolidation.",

        "Executive KPI Dashboard and Governance Cadence: Establish a monthly supply chain "
        "performance governance forum with automated KPI dashboards covering on-time rate, "
        "delay gap distribution, and late delivery risk by mode, region, and segment. "
        "Set quarterly improvement targets and track variance against baseline metrics "
        "established in this report.",
    ])

    # Section 8 – Conclusion
    h2("SECTION 8 — CONCLUSION")
    para(
        "This analysis of {:,} APL Logistics shipment records reveals a delivery landscape "
        "characterised by significant but addressable performance gaps. With {:.1f}% of "
        "shipments experiencing delays and a mean delay gap of {:.2f} days, the operational "
        "data confirms that current logistics configurations expose a material share of "
        "the shipment portfolio to SLA breach risk. The concentration of delay in specific "
        "shipping modes, regions, and markets indicates that targeted, rather than blanket, "
        "interventions will yield the greatest efficiency gains.".format(
            total, delayed_pct, avg_delay),

        "The five recommendations presented in Section 7 provide a prioritised roadmap for "
        "logistics leadership to reduce delay rates, improve customer satisfaction, and "
        "strengthen contractual compliance. Successful execution requires cross-functional "
        "collaboration between operations, carrier management, technology, and customer "
        "success teams. The statistical foundations laid in this report should serve as the "
        "baseline against which future performance improvements are measured, enabling a "
        "culture of continuous, evidence-driven logistics optimisation."
    )

    # Section 9 – References
    h2("SECTION 9 — REFERENCES")
    lines.append("")
    numbered([
        "Christopher, M. (2016). Logistics & Supply Chain Management (5th ed.). "
        "Pearson Education. — Foundational framework for supply chain performance measurement "
        "and SLA design.",

        "Chopra, S., & Meindl, P. (2021). Supply Chain Management: Strategy, Planning, "
        "and Operation (7th ed.). Pearson. — Quantitative models for delay risk and "
        "transportation mode analysis.",

        "Rodrigue, J.-P. (2020). The Geography of Transport Systems (5th ed.). Routledge. "
        "— Regional logistics infrastructure analysis and global shipping mode characteristics.",

        "McKinsey & Company (2023). 'Supply Chain Resilience: From Cost Centre to "
        "Value Driver.' McKinsey Global Institute. — Industry benchmarks for on-time "
        "delivery performance and operational KPI governance.",
    ])

    lines.append("")
    lines.append("=" * 75)
    lines.append("END OF REPORT")
    lines.append("=" * 75)

    return "\n".join(lines)


if __name__ == "__main__":
    df = load_data()
    paper = build_paper(df)
    output_path = "APL_Logistics_Research_Paper.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(paper)
    print("Research paper saved successfully!")
