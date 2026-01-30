import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Executive Dashboard | Amazon India",
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
st.title("Executive Summary Dashboard")
st.markdown(
    """
    **Strategic overview of Amazon India’s business performance (2015–2025)**  
    Designed for leadership-level decision making.
    """
)

st.divider()

# --------------------------------------------------
# EXECUTIVE KPIs (QUESTION 1)
# --------------------------------------------------
st.subheader("Key Business Metrics")

total_revenue = df["final_amount_inr"].sum()
total_orders = df["transaction_id"].nunique()
active_customers = df["customer_id"].nunique()
avg_order_value = df["final_amount_inr"].mean()

yearly_revenue = df.groupby("order_year")["final_amount_inr"].sum().reset_index()
yoy_growth = yearly_revenue["final_amount_inr"].pct_change().iloc[-1] * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Active Customers", f"{active_customers:,}")
col4.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")
col5.metric("YoY Growth", f"{yoy_growth:.2f}%")

st.caption("KPIs provide a high-level snapshot of business performance.")

st.divider()

# --------------------------------------------------
# REVENUE TREND ANALYSIS (QUESTION 1)
# --------------------------------------------------
st.subheader("Revenue Growth Trend (2015–2025)")

fig = px.line(
    yearly_revenue,
    x="order_year",
    y="final_amount_inr",
    markers=True,
    title="Yearly Revenue Trend"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("📌 Consistent long-term growth highlights strong market expansion.")

st.divider()

# --------------------------------------------------
# TOP PERFORMING CATEGORIES (QUESTION 1 & 4)
# --------------------------------------------------
st.subheader("Top Performing Categories")

category_rev = df.groupby("subcategory")["final_amount_inr"].sum().reset_index()
category_rev = category_rev.sort_values("final_amount_inr", ascending=False).head(10)

fig = px.bar(
    category_rev,
    x="final_amount_inr",
    y="subcategory",
    orientation="h",
    title="Top 10 Categories by Revenue"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Revenue concentration shows which categories drive maximum business value.")

st.divider()

# --------------------------------------------------
# MARKET & STRATEGIC OVERVIEW (QUESTION 3)
# --------------------------------------------------
st.subheader("Strategic Business Overview")

col1, col2 = st.columns(2)

with col1:
    city_rev = df.groupby("customer_city")["final_amount_inr"].sum().reset_index()
    city_rev = city_rev.sort_values("final_amount_inr", ascending=False).head(10)

    fig = px.bar(
        city_rev,
        x="final_amount_inr",
        y="customer_city",
        orientation="h",
        title="Top Revenue-Contributing Cities"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    payment_share = df["payment_method"].value_counts().reset_index()
    payment_share.columns = ["payment_method", "count"]

    fig = px.pie(
        payment_share,
        names="payment_method",
        values="count",
        title="Payment Method Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("📌 Urban markets and digital payments dominate overall business performance.")

st.divider()

# --------------------------------------------------
# FINANCIAL PERFORMANCE SNAPSHOT (QUESTION 4)
# --------------------------------------------------
st.subheader("Financial Performance Snapshot")

monthly_rev = df.groupby(["order_year", "order_month"])["final_amount_inr"].sum().reset_index()
monthly_rev["year_month"] = monthly_rev["order_year"].astype(str) + "-" + monthly_rev["order_month"].astype(str)

fig = px.line(
    monthly_rev,
    x="year_month",
    y="final_amount_inr",
    title="Monthly Revenue Trend"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Monthly revenue patterns reveal seasonality and campaign-driven spikes.")

st.divider()

# --------------------------------------------------
# GROWTH ANALYTICS (QUESTION 5)
# --------------------------------------------------
st.subheader("Growth Analytics")

customer_growth = df.groupby("order_year")["customer_id"].nunique().reset_index()

fig = px.line(
    customer_growth,
    x="order_year",
    y="customer_id",
    markers=True,
    title="Active Customer Growth Over Time"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Growing customer base indicates successful acquisition and retention strategies.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    ---
    **Dashboard:** Executive Summary  
    **Focus:** Strategic KPIs, Growth, Financial & Market Health  
    **Audience:** CXOs, Business Heads, Strategy Teams
    """
)
