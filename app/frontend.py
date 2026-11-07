import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# 1. CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Nassau Candy | Distribution Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"

NAVY = "#17324D"
TEAL = "#138A83"
BLUE = "#3977B8"
PURPLE = "#8064C8"
ORANGE = "#D99142"
GREY = "#66768A"
COLORS = [TEAL, BLUE, PURPLE, ORANGE, "#D16B82", "#718096"]


# =========================================================
# 2. PROFESSIONAL STYLING
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F4F6F9;
        color: #24364B;
    }

    .block-container {
        max-width: 1550px;
        padding: 2rem 2.5rem 3rem 2.5rem;
    }

    [data-testid="stSidebar"] {
        background-color: #17324D;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E3E9F0;
        border-radius: 12px;
        padding: 19px;
        box-shadow: 0 2px 8px rgba(23,50,77,0.04);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color: #718096 !important;
        font-size: 13px !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #17324D !important;
        font-weight: 700 !important;
    }

    h1, h2, h3 {
        color: #17324D !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E3E9F0;
        border-radius: 10px;
    }

    .stDownloadButton button {
        background: #138A83;
        color: white;
        border: none;
        border-radius: 7px;
        font-weight: 600;
    }

    .stDownloadButton button:hover {
        background: #0E716C;
        color: white;
    }

    hr {
        border-color: #E3E9F0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. DATA LOADING
# =========================================================

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    required_columns = [
        "Row ID", "Order ID", "Sales", "Cost", "Gross Profit",
        "Units", "Region", "Ship Mode", "Country/Region",
        "Division", "City", "State/Province"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

    data["Profit Margin (%)"] = (
        data["Gross Profit"] / data["Sales"].replace(0, pd.NA)
    ) * 100

    data["Profit Per Unit"] = (
        data["Gross Profit"] / data["Units"].replace(0, pd.NA)
    )

    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Dataset could not be loaded: {error}")
    st.info(
        "Check that the CSV exists at: "
        "data/Nassau Candy Distributor.csv"
    )
    st.stop()


# =========================================================
# 4. REUSABLE HELPERS
# =========================================================

def format_chart(fig, height=380):
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(family="Arial", size=12, color="#34465A"),
        title_font=dict(size=17, color=NAVY),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=25, r=25, t=65, b=35),
        hoverlabel=dict(bgcolor=NAVY, font_color="white"),
        legend=dict(
            orientation="h",
            y=1.12,
            x=1,
            xanchor="right",
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor="#E5EAF0")
    fig.update_yaxes(gridcolor="#EDF1F5", zeroline=False)
    return fig


def insight_panel(title, findings, implication=None):

    with st.container(border=True):

        st.subheader(title)

        for heading, description in findings:

            st.markdown(f"**{heading}**")
            st.write(description)

        if implication:
            st.info(
                f"**Business Implication:** {implication}"
            )


def section_heading(title, description):
    st.markdown(
        f"<h3 style='margin-bottom:3px;color:{NAVY};'>"
        f"{html.escape(str(title))}</h3>",
        unsafe_allow_html=True,
    )
    st.caption(description)


def currency(value):
    return f"${value:,.2f}"


def show_chart(fig, height=380):
    st.plotly_chart(
        format_chart(fig, height),
        use_container_width=True,
    )


# =========================================================
# 5. SIDEBAR AND NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding:15px 0 20px 0;">
            <div style="font-size:20px;font-weight:750;">
                NASSAU CANDY
            </div>
            <div style="
                font-size:10px;
                color:#B7C9D9;
                letter-spacing:1.5px;
            ">
                DISTRIBUTION ANALYTICS
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### NAVIGATION")

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Geographic Analysis",
            "Shipping Analysis",
            "Financial Analysis",
            "Data Explorer",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### ANALYSIS FILTERS")

    regions = sorted(df["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Region", regions, default=regions
    )

    modes = sorted(df["Ship Mode"].dropna().unique().tolist())
    selected_modes = st.multiselect(
        "Shipping Mode", modes, default=modes
    )

    countries = sorted(
        df["Country/Region"].dropna().unique().tolist()
    )
    selected_countries = st.multiselect(
        "Country", countries, default=countries
    )

    divisions = sorted(df["Division"].dropna().unique().tolist())
    selected_divisions = st.multiselect(
        "Division", divisions, default=divisions
    )

    st.divider()
    st.caption("DATASET INFORMATION")
    st.write(f"Total records: {len(df):,}")
    st.write(f"Total fields: {len(df.columns)}")


# =========================================================
# 6. FILTERED DATA
# =========================================================

data = df[
    df["Region"].isin(selected_regions)
    & df["Ship Mode"].isin(selected_modes)
    & df["Country/Region"].isin(selected_countries)
    & df["Division"].isin(selected_divisions)
].copy()

if data.empty:
    st.warning("No records found for the selected filters.")
    st.stop()


# =========================================================
# 7. BUSINESS CALCULATIONS
# =========================================================

total_sales = data["Sales"].sum()
total_profit = data["Gross Profit"].sum()
total_cost = data["Cost"].sum()
total_units = data["Units"].sum()
total_orders = data["Order ID"].nunique()
total_records = len(data)

profit_margin = (
    total_profit / total_sales * 100 if total_sales else 0
)


# =========================================================
# 8. APPLICATION HEADER
# =========================================================

st.markdown(
    """
    <div style="
        background:white;
        border:1px solid #E2E8EF;
        border-radius:11px;
        padding:22px 25px;
        margin-bottom:23px;
    ">
        <div style="
            font-size:11px;
            color:#138A83;
            font-weight:700;
            letter-spacing:1.5px;
        ">
            BUSINESS INTELLIGENCE PLATFORM
        </div>
        <h1 style="
            color:#17324D;
            font-size:29px;
            margin:7px 0;
        ">
            Nassau Candy Distribution Analytics
        </h1>
        <div style="color:#718096;font-size:14px;">
            Operational distribution, geographical performance
            and financial intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 9. KPI SECTION
# =========================================================

section_heading(
    "Business Performance Summary",
    "Consolidated performance indicators for the selected records.",
)

a, b, c, d = st.columns(4)
a.metric("TOTAL SALES", currency(total_sales))
b.metric("GROSS PROFIT", currency(total_profit))
c.metric("TOTAL COST", currency(total_cost))
d.metric("PROFIT MARGIN", f"{profit_margin:.2f}%")

a, b, c, d = st.columns(4)
a.metric("UNITS SOLD", f"{total_units:,.0f}")
b.metric("UNIQUE ORDERS", f"{total_orders:,}")
c.metric("RECORDS ANALYSED", f"{total_records:,}")
d.metric("AVERAGE SALES / RECORD", currency(data["Sales"].mean()))

st.divider()


# =========================================================
# 10. EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    section_heading(
        "Regional Business Performance",
        "Comparison of sales and profitability across operating regions.",
    )

    region = data.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
    ).reset_index().sort_values("Sales", ascending=False)

    left, right = st.columns([1.65, 1])

    with left:
        fig = px.bar(
            region,
            x="Region",
            y="Sales",
            color="Region",
            text_auto=".2s",
            title="Total Revenue by Region",
            color_discrete_sequence=COLORS,
        )
        show_chart(fig)

    with right:
        leader = region.iloc[0]
        runner_up = region.iloc[1] if len(region) > 1 else None
        share = leader["Sales"] / total_sales * 100 if total_sales else 0

        findings = [
            (
                "Highest-performing region",
                f"{leader['Region']} generated {currency(leader['Sales'])} "
                f"in revenue, contributing {share:.2f}% of selected sales.",
            )
        ]

        if runner_up is not None:
            findings.append(
                (
                    "Second-highest region",
                    f"{runner_up['Region']} generated "
                    f"{currency(runner_up['Sales'])}.",
                )
            )
            findings.append(
                (
                    "Regional comparison",
                    f"The difference between the leading two regions is "
                    f"{currency(leader['Sales'] - runner_up['Sales'])}.",
                )
            )

        insight_panel(
            "Regional Revenue Insights",
            findings,
            "Regional sales concentration can help management prioritise "
            "market development and distribution planning.",
        )

    st.divider()

    section_heading(
        "Shipping Mode Distribution",
        "Distribution of dataset records across the four shipping categories.",
    )

    modes_data = data.groupby("Ship Mode").agg(
        Records=("Row ID", "count"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
    ).reset_index()

    leading_mode = modes_data.loc[modes_data["Records"].idxmax()]
    left, right = st.columns([1.65, 1])

    with left:
        fig = px.pie(
            modes_data,
            names="Ship Mode",
            values="Records",
            hole=0.5,
            title="Shipping Mode Share",
            color_discrete_sequence=COLORS,
        )
        show_chart(fig)

    with right:
        insight_panel(
            "Shipping Distribution Insights",
            [
                (
                    "Most frequently recorded mode",
                    f"{leading_mode['Ship Mode']} accounts for "
                    f"{leading_mode['Records']:,} records.",
                ),
                (
                    "Share of records",
                    f"{leading_mode['Records'] / total_records * 100:.2f}% "
                    "of the filtered dataset.",
                ),
                (
                    "Other shipping categories",
                    "The remaining records are distributed across "
                    "the other shipping categories.",
                ),
            ],
            "Standard Class dominates the observed shipping-mode "
            "distribution. This describes usage, not delivery speed.",
        )

    st.divider()

    section_heading(
        "Leading Customer Destinations",
        "Cities ranked according to their contribution to total sales.",
    )

    cities = data.groupby(
        ["Country/Region", "State/Province", "City"]
    ).agg(
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Orders=("Order ID", "nunique"),
    ).reset_index().nlargest(10, "Sales")

    cities["Destination"] = (
        cities["City"] + ", " + cities["State/Province"]
    )

    leader_city = cities.iloc[0]
    left, right = st.columns([1.65, 1])

    with left:
        fig = px.bar(
            cities.sort_values("Sales"),
            x="Sales",
            y="Destination",
            orientation="h",
            color="Sales",
            title="Top 10 Destinations by Revenue",
            color_continuous_scale="Teal",
        )
        show_chart(fig, 430)

    with right:
        insight_panel(
            "Destination Insights",
            [
                (
                    "Leading destination",
                    f"{leader_city['Destination']} generated "
                    f"{currency(leader_city['Sales'])}.",
                ),
                (
                    "Unique orders",
                    f"{leader_city['Orders']:,} distinct orders "
                    "are associated with this destination.",
                ),
                (
                    "Destination ranking",
                    "The chart ranks the ten highest-selling "
                    "destinations in the selected data.",
                ),
            ],
            "High-sales destinations may deserve closer attention "
            "when evaluating distribution capacity.",
        )


# =========================================================
# 11. GEOGRAPHIC ANALYSIS
# =========================================================

elif page == "Geographic Analysis":

    section_heading(
        "Geographic Performance",
        "Examine revenue distribution and destination-level concentration.",
    )

    region = data.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Records=("Row ID", "count"),
        Orders=("Order ID", "nunique"),
    ).reset_index()

    region["Sales Share (%)"] = (
        region["Sales"] / total_sales * 100
    )

    left, right = st.columns([1.65, 1])

    with left:
        fig = px.bar(
            region.sort_values("Sales", ascending=False),
            x="Region",
            y="Sales",
            color="Region",
            title="Revenue by Region",
            color_discrete_sequence=COLORS,
        )
        show_chart(fig)

    with right:
        best = region.loc[region["Sales"].idxmax()]
        insight_panel(
            "Geographic Findings",
            [
                (
                    "Leading region",
                    f"{best['Region']} contributes "
                    f"{best['Sales Share (%)']:.2f}% of sales.",
                ),
                (
                    "Total regions",
                    f"{region['Region'].nunique()} operating regions "
                    "are represented.",
                ),
                (
                    "Order concentration",
                    f"{best['Orders']:,} unique orders are recorded "
                    f"for {best['Region']}.",
                ),
            ],
            "Regional concentration can support decisions about "
            "market coverage and inventory allocation.",
        )

    st.divider()

    section_heading(
        "State and Province Analysis",
        "Rank destinations by sales contribution.",
    )

    states = data.groupby(
        ["Country/Region", "State/Province"]
    ).agg(
        Records=("Row ID", "count"),
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
    ).reset_index().sort_values("Sales", ascending=False)

    st.dataframe(states, use_container_width=True, hide_index=True)

    st.divider()

    section_heading(
        "City-Level Analysis",
        "Detailed comparison of customer destinations.",
    )

    city = data.groupby(
        ["Country/Region", "State/Province", "City"]
    ).agg(
        Records=("Row ID", "count"),
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Units=("Units", "sum"),
    ).reset_index().sort_values("Sales", ascending=False)

    st.dataframe(
        city.head(30),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 12. SHIPPING ANALYSIS
# =========================================================

elif page == "Shipping Analysis":

    section_heading(
        "Shipping Operations Analysis",
        "Understand shipping-mode usage and its relationship with geography.",
    )

    modes_data = data.groupby("Ship Mode").agg(
        Records=("Row ID", "count"),
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
    ).reset_index()

    modes_data["Profit Margin (%)"] = (
        modes_data["Profit"] / modes_data["Sales"] * 100
    )

    leading = modes_data.loc[modes_data["Records"].idxmax()]
    left, right = st.columns([1.65, 1])

    with left:
        fig = px.bar(
            modes_data,
            x="Ship Mode",
            y="Records",
            color="Ship Mode",
            title="Records by Shipping Mode",
            color_discrete_sequence=COLORS,
        )
        show_chart(fig)

    with right:
        insight_panel(
            "Shipping Mode Findings",
            [
                (
                    "Most frequently used mode",
                    f"{leading['Ship Mode']} has "
                    f"{leading['Records']:,} records.",
                ),
                (
                    "Unique orders",
                    f"{leading['Orders']:,} distinct orders "
                    "are associated with this category.",
                ),
                (
                    "Financial contribution",
                    f"Gross profit for this mode is "
                    f"{currency(leading['Profit'])}.",
                ),
            ],
            "Mode usage and financial contribution can be compared, "
            "but neither proves transport efficiency.",
        )

    st.divider()

    section_heading(
        "Regional Shipping Distribution",
        "Number of records associated with each mode in every region.",
    )

    heatmap = pd.crosstab(data["Region"], data["Ship Mode"])
    left, right = st.columns([1.65, 1])

    with left:
        fig = px.imshow(
            heatmap,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Teal",
            title="Region vs Shipping Mode",
        )
        show_chart(fig)

    with right:
        region_mode_share = pd.crosstab(
            data["Region"],
            data["Ship Mode"],
            normalize="index",
        ) * 100

        standard_share = (
            region_mode_share["Standard Class"].mean()
            if "Standard Class" in region_mode_share.columns
            else 0
        )

        insight_panel(
            "Regional Shipping Insights",
            [
                (
                    "Regional comparison",
                    "The heatmap compares the record count of each "
                    "shipping mode across operating regions.",
                ),
                (
                    "Standard Class",
                    f"Average regional share: {standard_share:.2f}%.",
                ),
                (
                    "Interpretation",
                    "Compare the proportions to understand how "
                    "shipping-mode usage differs geographically.",
                ),
            ],
            "These patterns can guide further investigation of "
            "regional shipping requirements.",
        )

    st.divider()

    section_heading(
        "Shipping Financial Comparison",
        "Compare sales, gross profit and profitability by shipping mode.",
    )

    st.dataframe(
        modes_data.round(2),
        use_container_width=True,
        hide_index=True,
    )

    st.warning(
        "Source-date quality warning: calculated shipping durations "
        "range from 904 to 1,642 days. These values are not treated "
        "as actual delivery times."
    )


# =========================================================
# 13. FINANCIAL ANALYSIS
# =========================================================

elif page == "Financial Analysis":

    section_heading(
        "Financial Performance",
        "Evaluate revenue, cost, gross profit and profit margins.",
    )

    finance = data.groupby("Ship Mode").agg(
        Sales=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Profit=("Gross Profit", "sum"),
    ).reset_index()

    finance["Profit Margin (%)"] = (
        finance["Profit"] / finance["Sales"] * 100
    )

    left, right = st.columns([1.65, 1])

    with left:
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=finance["Ship Mode"],
                y=finance["Sales"],
                name="Sales",
                marker_color=BLUE,
            )
        )
        fig.add_trace(
            go.Bar(
                x=finance["Ship Mode"],
                y=finance["Cost"],
                name="Cost",
                marker_color=ORANGE,
            )
        )
        fig.update_layout(
            barmode="group",
            title="Sales vs Cost by Shipping Mode",
        )
        show_chart(fig)

    with right:
        insight_panel(
            "Financial Comparison",
            [
                ("Total revenue", f"Filtered revenue: {currency(total_sales)}."),
                (
                    "Total gross profit",
                    f"Filtered gross profit: {currency(total_profit)}.",
                ),
                (
                    "Overall margin",
                    f"Weighted gross profit margin: {profit_margin:.2f}%.",
                ),
            ],
            "Financial comparisons help identify where revenue "
            "and gross profit are concentrated.",
        )

    st.divider()

    section_heading(
        "Product Division Performance",
        "Comparison of sales and profitability across product divisions.",
    )

    division = data.groupby("Division").agg(
        Sales=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Profit=("Gross Profit", "sum"),
        Units=("Units", "sum"),
    ).reset_index()

    division["Profit Margin (%)"] = (
        division["Profit"] / division["Sales"] * 100
    )

    left, right = st.columns([1.65, 1])

    with left:
        fig = px.bar(
            division,
            x="Division",
            y="Profit",
            color="Division",
            title="Gross Profit by Division",
            color_discrete_sequence=COLORS,
        )
        show_chart(fig)

    with right:
        best_division = division.loc[division["Profit"].idxmax()]
        insight_panel(
            "Division Insights",
            [
                (
                    "Leading division",
                    f"{best_division['Division']} contributes "
                    f"{currency(best_division['Profit'])} in gross profit.",
                ),
                (
                    "Units sold",
                    f"{best_division['Units']:,.0f} units are associated "
                    "with this division.",
                ),
                (
                    "Profit margin",
                    f"{best_division['Profit Margin (%)']:.2f}%.",
                ),
            ],
            "Division-level profitability can help prioritise "
            "product portfolio analysis.",
        )

    st.dataframe(
        division.round(2),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 14. DATA EXPLORER
# =========================================================

elif page == "Data Explorer":

    section_heading(
        "Dataset Explorer",
        "Search, inspect and export records from the filtered dataset.",
    )

    search = st.text_input(
        "Search dataset",
        placeholder="Enter order ID, product, city or customer ID...",
    )

    result = data.copy()

    if search:
        matched = result.astype(str).apply(
            lambda column: column.str.contains(
                search,
                case=False,
                na=False,
                regex=False,
            )
        ).any(axis=1)

        result = result[matched]

    st.write(f"Matching records: {len(result):,}")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download filtered dataset",
        data=result.to_csv(index=False).encode("utf-8"),
        file_name="nassau_candy_filtered.csv",
        mime="text/csv",
    )


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()

st.caption(
    "Nassau Candy Distribution Analytics | "
    "Python • Pandas • Streamlit • Plotly"
)

st.caption(
    "All insights are calculated from the selected dataset records. "
    "Shipping-date anomalies are disclosed and excluded from "
    "delivery-efficiency conclusions."
)
