
# ============================================================
# NASSAU CANDY DISTRIBUTION ANALYTICS DASHBOARD
# STEP 7: STREAMLIT DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="📦",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"

# ------------------------------------------------------------
# 2. CUSTOM STYLING
# ------------------------------------------------------------

st.markdown("""
<style>

/* Main dashboard */
.main {
    background-color: #f7f8fc;
}

/* KPI cards */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* KPI labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #475569 !important;
}

/* KPI values */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #172554 !important;
    font-weight: 700 !important;
}

/* KPI delta */
[data-testid="stMetricDelta"] {
    color: #15803d !important;
}

h1 {
    color: #172554;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 3. LOAD DATASET
# ------------------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    data["Profit Margin (%)"] = (
        data["Gross Profit"] / data["Sales"]
    ) * 100

    data["Profit Per Unit"] = (
        data["Gross Profit"] / data["Units"]
    )

    return data


df = load_data()

# ------------------------------------------------------------
# 4. DASHBOARD HEADER
# ------------------------------------------------------------

st.title("📦 Nassau Candy Distribution Analytics")

st.markdown(
    "### Factory-to-Customer Shipping & Business Performance Analysis"
)

st.caption(
    "Interactive analysis of sales, profitability, "
    "shipping modes and customer destinations."
)

st.divider()

# ------------------------------------------------------------
# 5. SIDEBAR FILTERS
# ------------------------------------------------------------

st.sidebar.title("Dashboard Filters")

regions = sorted(df["Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

ship_modes = sorted(df["Ship Mode"].dropna().unique())

selected_modes = st.sidebar.multiselect(
    "Select Shipping Mode",
    ship_modes,
    default=ship_modes
)

countries = sorted(df["Country/Region"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=countries
)

divisions = sorted(df["Division"].dropna().unique())

selected_divisions = st.sidebar.multiselect(
    "Select Division",
    divisions,
    default=divisions
)

# ------------------------------------------------------------
# 6. FILTER DATA
# ------------------------------------------------------------

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Ship Mode"].isin(selected_modes)) &
    (df["Country/Region"].isin(selected_countries)) &
    (df["Division"].isin(selected_divisions))
].copy()

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# ------------------------------------------------------------
# 7. KPI CARDS
# ------------------------------------------------------------

st.subheader("Business Performance Overview")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
total_cost = filtered_df["Cost"].sum()
total_units = filtered_df["Units"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales else 0
)

unique_orders = filtered_df["Order ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Gross Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Total Cost",
    f"${total_cost:,.2f}"
)

col4.metric(
    "Total Units",
    f"{total_units:,}"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

col6.metric(
    "Unique Orders",
    f"{unique_orders:,}"
)

col7.metric(
    "Dataset Records",
    f"{len(filtered_df):,}"
)

col8.metric(
    "Average Sales / Record",
    f"${filtered_df['Sales'].mean():,.2f}"
)

st.divider()

# ------------------------------------------------------------
# 8. REGIONAL SALES AND PROFIT
# ------------------------------------------------------------

st.subheader("Regional Performance")

region_data = filtered_df.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Gross_Profit=("Gross Profit", "sum")
).reset_index()

fig_region = px.bar(
    region_data,
    x="Region",
    y=["Sales", "Gross_Profit"],
    barmode="group",
    title="Regional Sales vs Gross Profit",
    template="plotly_white"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# ------------------------------------------------------------
# 9. SHIPPING MODE DISTRIBUTION
# ------------------------------------------------------------

st.subheader("Shipping Mode Analysis")

mode_data = filtered_df.groupby("Ship Mode").agg(
    Records=("Row ID", "count"),
    Sales=("Sales", "sum"),
    Profit=("Gross Profit", "sum")
).reset_index()

col1, col2 = st.columns(2)

with col1:

    fig_mode = px.pie(
        mode_data,
        names="Ship Mode",
        values="Records",
        hole=0.45,
        title="Shipping Mode Distribution",
        template="plotly_white"
    )

    st.plotly_chart(
        fig_mode,
        use_container_width=True
    )

with col2:

    fig_mode_profit = px.bar(
        mode_data,
        x="Ship Mode",
        y="Profit",
        title="Gross Profit by Shipping Mode",
        template="plotly_white"
    )

    st.plotly_chart(
        fig_mode_profit,
        use_container_width=True
    )

# ------------------------------------------------------------
# 10. DESTINATION CITY ANALYSIS
# ------------------------------------------------------------

st.subheader("Top Customer Destinations")

city_data = filtered_df.groupby(
    ["Country/Region", "State/Province", "City"]
).agg(
    Records=("Row ID", "count"),
    Sales=("Sales", "sum"),
    Profit=("Gross Profit", "sum")
).reset_index()

top_cities = city_data.sort_values(
    "Sales",
    ascending=False
).head(15)

top_cities["Destination"] = (
    top_cities["City"] + ", " +
    top_cities["State/Province"] + ", " +
    top_cities["Country/Region"]
)

fig_cities = px.bar(
    top_cities,
    x="Sales",
    y="Destination",
    orientation="h",
    title="Top 15 Destinations by Sales",
    template="plotly_white"
)

fig_cities.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig_cities,
    use_container_width=True
)

# ------------------------------------------------------------
# 11. REGIONAL SHIPPING DISTRIBUTION
# ------------------------------------------------------------

st.subheader("Regional Shipping Mode Distribution")

region_mode = pd.crosstab(
    filtered_df["Region"],
    filtered_df["Ship Mode"]
)

fig_heatmap = px.imshow(
    region_mode,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    title="Shipping Mode Usage Across Regions"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# ------------------------------------------------------------
# 12. FINANCIAL SUMMARY TABLE
# ------------------------------------------------------------

st.subheader("Regional Financial Summary")

st.dataframe(
    region_data,
    use_container_width=True,
    hide_index=True
)

# ------------------------------------------------------------
# 13. DOWNLOAD FILTERED DATA
# ------------------------------------------------------------

st.subheader("Download Filtered Dataset")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv_data,
    file_name="nassau_filtered_analysis.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "Nassau Candy Distribution Analytics | "
    "Academic Data Analytics Project"
)

st.caption(
    "Note: Shipping-date differences are excluded from "
    "performance conclusions because the source dates require verification."
)
