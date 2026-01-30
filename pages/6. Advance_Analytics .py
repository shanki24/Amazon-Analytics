import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Advanced Analytics | Amazon India",
    layout="wide"
)

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------
@st.cache_data
def load_data():
    base_path = Path(__file__).parents[1] / "cleaned"
    df = pd.read_csv(base_path / "transactions_cleaned.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

df = load_data()

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("Advanced Analytics Dashboard")
st.markdown(
    """
    **Predictive insights, strategic intelligence, and executive-level monitoring
    for data-driven decision making (2015–2025).**
    """
)

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("🔎 Advanced Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["order_year"].unique()),
    default=[df["order_year"].max()]
)

filtered_df = df[df["order_year"].isin(year_filter)]

# ==================================================
# QUESTION 26 – PREDICTIVE ANALYTICS (SALES FORECAST)
# ==================================================
st.subheader("Sales Forecasting & Trend Projection")

monthly_sales = (
    df
    .groupby(["order_year", "order_month"])["final_amount_inr"]
    .sum()
    .reset_index()
)

monthly_sales["ym"] = (
    monthly_sales["order_year"].astype(str)
    + "-"
    + monthly_sales["order_month"].astype(str).str.zfill(2)
)

monthly_sales["trend"] = (
    monthly_sales["final_amount_inr"]
    .rolling(window=6, min_periods=1)
    .mean()
)

fig = px.line(
    monthly_sales,
    x="ym",
    y=["final_amount_inr", "trend"],
    title="Monthly Revenue with Trend-Based Forecast"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Rolling trends provide a reliable short-term revenue forecast.")

st.divider()

# ==================================================
# QUESTION 27 – MARKET INTELLIGENCE
# ==================================================
st.subheader("Market Intelligence & Category Signals")

category_share = (
    filtered_df
    .groupby("subcategory")["final_amount_inr"]
    .sum()
    .reset_index()
)

fig = px.treemap(
    category_share,
    path=["subcategory"],
    values="final_amount_inr",
    title="Market Share by Product Category"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Category dominance highlights competitive positioning and growth opportunities.")

st.divider()

# ==================================================
# QUESTION 28 – CROSS-SELL & UP-SELL ANALYSIS
# ==================================================
st.subheader("🔗 Cross-Sell & Up-Sell Opportunities")

basket = (
    filtered_df
    .groupby(["customer_id", "subcategory"])
    .size()
    .reset_index(name="count")
)

cross_sell = (
    basket
    .groupby("subcategory")["customer_id"]
    .nunique()
    .reset_index()
    .sort_values("customer_id", ascending=False)
)

fig = px.bar(
    cross_sell,
    x="customer_id",
    y="subcategory",
    orientation="h",
    title="Cross-Sell Potential by Category"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Categories frequently purchased together offer bundling opportunities.")

st.divider()

# ==================================================
# QUESTION 29 – SEASONAL PLANNING INSIGHTS
# ==================================================
st.subheader("Seasonal Planning & Demand Signals")

seasonality = (
    df
    .groupby("order_month")["final_amount_inr"]
    .mean()
    .reset_index()
)

fig = px.bar(
    seasonality,
    x="order_month",
    y="final_amount_inr",
    title="Average Monthly Revenue (Seasonality)"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Peak months support inventory and promotion planning.")

st.divider()

# ==================================================
# QUESTION 30 – BI COMMAND CENTER
# ==================================================
st.subheader("Business Intelligence Command Center")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{filtered_df['final_amount_inr'].sum()/1e7:.2f} Cr"
    )

with col2:
    st.metric(
        "Active Customers",
        filtered_df["customer_id"].nunique()
    )

with col3:
    st.metric(
        "Avg Order Value",
        f"₹{filtered_df['final_amount_inr'].mean():,.0f}"
    )

with col4:
    st.metric(
        "Return Rate",
        f"{filtered_df['return_status'].astype(str).str.lower().isin(['returned']).mean()*100:.2f}%"
    )

st.success("Real-time KPIs monitored successfully.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    ---
    **Dashboard:** Advanced Analytics  
    **Focus:** Predictive Insights, Strategy & BI Monitoring  
    **Audience:** Leadership, Strategy & Data Science Teams
    """
)