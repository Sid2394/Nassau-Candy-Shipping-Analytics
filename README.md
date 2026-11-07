# 🍬 Nassau Candy Shipping Analytics

### Factory-to-Customer Shipping Route Efficiency Analysis

A data analytics project focused on analyzing shipping patterns, geographical distribution, sales performance, and profitability for Nassau Candy Distributor using Python and Streamlit.

## 📌 Project Overview

This project analyzes the sales and shipping dataset of Nassau Candy Distributor to understand order distribution, shipping preferences, regional performance, and financial outcomes.

The objective is to transform raw business data into meaningful insights through data cleaning, exploratory data analysis (EDA), visualization, and an interactive dashboard.

## 🎯 Project Objectives

- Analyze shipping mode distribution and usage patterns.
- Compare sales and profitability across different regions.
- Identify top-performing cities and states.
- Examine shipping patterns across regions and countries.
- Evaluate revenue, costs, gross profit, and profit margins.
- Build an interactive dashboard for business insights.
- Identify data quality issues that may affect shipping analysis.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and processing |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive charts |
| Streamlit | Interactive dashboard |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
Nassau_Candy_Shipping_Analytics/
│
├── app/
│   ├── dashboard.py
│   └── frontend.py
│
├── data/
│   ├── Nassau Candy Distributor.csv
│   └── processed/
│
├── notebooks/
│   ├── 01_dataset_inspection.py
│   ├── 02_data_validation.py
│   ├── 03_shipping_date_investigation.py
│   ├── 04_shipping_pattern_analysis.py
│   ├── 05_geographic_financial_analysis.py
│   ├── 06_shipping_distribution_analysis.py
│   └── 07_create_visualizations.py
│
├── outputs/
│   └── charts/
│
├── .gitignore
└── README.md
```

## 📊 Dataset Information

The dataset contains **10,194 records and 18 original columns**, covering order details, customer information, geographical locations, product information, sales, units, costs, and gross profit.

Key dataset attributes include:

- Order ID and Order Date
- Ship Date and Ship Mode
- Country, City, State, and Region
- Product Name and Division
- Sales, Units, Cost, and Gross Profit

## 🔍 Analysis Performed

### 1. Data Inspection and Validation
- Dataset structure and data types.
- Missing values and duplicate records.
- Date validation.
- Financial consistency checks.
- Shipping date anomaly investigation.

### 2. Geographic Analysis
- Regional sales and profit comparison.
- State-wise sales performance.
- Top-performing destination cities.
- Country-wise business distribution.

### 3. Shipping Analysis
- Shipping mode distribution.
- Regional shipping preferences.
- Shipping mode contribution to sales and profit.
- Investigation of recorded shipping durations.

### 4. Financial Analysis
- Total revenue and cost.
- Gross profit.
- Overall profit margin.
- Regional and shipping-mode profitability.

## 📈 Key Findings

| Metric | Result |
|---|---:|
| Total Records | 10,194 |
| Unique Orders | 8,549 |
| Total Sales | $141,783.63 |
| Total Cost | $48,340.83 |
| Gross Profit | $93,442.80 |
| Overall Profit Margin | 65.91% |
| Total Units Sold | 38,654 |

### Important Business Insights

- Pacific contributes the highest regional sales at approximately 32.66%.
- Standard Class is the most frequently used shipping mode, accounting for approximately 60.04% of records.
- California is the highest-selling state.
- New York City is the highest-selling destination city.
- Standard Class contributes approximately 60.30% of total sales.

**Data quality note:** The recorded Order Date and Ship Date values produce unusually long shipping durations of 904–1,642 days. These values require source-data verification. Therefore, they are treated as a data quality concern rather than confirmed actual delivery times or shipping delays.

## 📊 Interactive Dashboard

The Streamlit dashboard provides five main sections:

1. Executive Overview
2. Geographic Analysis
3. Shipping Analysis
4. Financial Analysis
5. Data Explorer

It includes interactive filters, charts, key performance indicators, business insights, and data exploration features.

## 🚀 How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/Sid2394/Nassau-Candy-Shipping-Analytics.git
```

### Step 2: Navigate to the project directory

```bash
cd Nassau-Candy-Shipping-Analytics
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit folium openpyxl
```

### Step 6: Run the dashboard

```bash
streamlit run app/frontend.py
```

The dashboard will open in your browser, usually at:

`http://localhost:8501`

## 🔮 Future Scope

- Integration of real-time shipment tracking data.
- Route optimization using geographical and distance information.
- Predictive analytics for delivery time estimation.
- Identification of shipping cost optimization opportunities.
- Advanced business intelligence reporting.
- Deployment of the dashboard for public access.

## 👩‍💻 Author

**Siddhant Uniyal**

GitHub: [@Sid2394](https://github.com/Sid2394)

## 📄 License

This project is developed for educational and analytical purposes.
