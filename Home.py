import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Amazon India Analytics | Home",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# DATA LOADING (Lightweight KPIs only)
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned/transactions_cleaned.csv")

try:
    df = load_data()

    if df.empty:
        st.error("Dataset loaded but is empty.")
        st.stop()

except Exception as e:
    st.error("❌ Error loading dataset:")
    st.exception(e)
    st.stop()

# --------------------------------------------------
# TITLE & INTRO
# --------------------------------------------------
st.title("Amazon India – A Decade of Sales Analytics")
st.markdown(
    """
    ### Business Intelligence & Analytics Platform (2015–2025)

    This interactive analytics platform provides **executive-level insights, 
    revenue intelligence, customer analytics, product performance tracking, 
    and advanced business analytics** for Amazon India over a decade.

    Use the dashboards from the **left navigation panel** to explore 
    strategic, tactical, and operational insights.
    """
)

st.divider()

# --------------------------------------------------
# KPI SNAPSHOT (EXECUTIVE OVERVIEW)
# --------------------------------------------------
st.subheader("Key Business Snapshot")

try:
    total_revenue = df["final_amount_inr"].sum()
    active_customers = df["customer_id"].nunique()
    total_orders = df["transaction_id"].nunique()
    avg_order_value = df["final_amount_inr"].mean()

except KeyError as e:
    st.error("❌ Column missing in dataset:")
    st.exception(e)
    st.write("Available columns:", list(df.columns))
    st.stop()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Active Customers", f"{active_customers:,}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")

st.caption("Snapshot KPIs for quick executive decision-making.")

st.divider()

# --------------------------------------------------
# DASHBOARD OVERVIEW
# --------------------------------------------------
st.subheader("Available Dashboards")

st.markdown(
    """
    Navigate through the dashboards using the **sidebar**:

    **Executive Dashboard**  
    → High-level KPIs, growth trends, market positioning, and strategic insights.

    **Revenue Analytics**  
    → Revenue trends, category performance, geographic analysis, festivals, and pricing insights.

    **Customer Analytics**  
    → RFM segmentation, customer lifetime value, Prime vs Non-Prime behavior, and demographics.

    **Product Analytics**  
    → Product & brand performance, ratings, lifecycle analysis, and inventory insights.

    **Operations Analytics**  
    → Delivery performance, payment methods, returns, and operational efficiency.

    **Advanced Analytics**  
    → Predictive analytics, forecasting, market intelligence, and BI command center insights.
    """
)

st.divider()

# --------------------------------------------------
# DATA & TECHNOLOGY STACK
# --------------------------------------------------
st.subheader("Data & Technology Stack")

st.markdown(
    """
    **Data Sources**
    - Transaction data (Orders, Revenue, Discounts, Returns)
    - Customer demographics & behavior
    - Product catalog & pricing
    - Time dimension for trend analysis

    **Technology Stack**
    - Python
    - Streamlit (Multi-page BI Application)
    - Pandas & NumPy
    - Plotly (Interactive Visualizations)
    - MySQL (Data Source)
    """
)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    ---
    **Project:** Amazon India – A Decade of Sales Analytics  
    **Purpose:** Business Intelligence, Analytics & Decision Support  
    **Built with:** Streamlit & Python
    """
)
