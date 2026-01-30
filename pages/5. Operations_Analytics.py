import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Operations Analytics | Amazon India",
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
st.title("Operations & Logistics Analytics")
st.markdown(
    """
    **Operational performance analysis covering delivery efficiency, 
    payments, returns, and customer service insights (2015–2025).**
    """
)

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("Operations Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["order_year"].unique()),
    default=[df["order_year"].max()]
)

filtered_df = df[df["order_year"].isin(year_filter)]

# ==================================================
# QUESTION 21 – DELIVERY PERFORMANCE DASHBOARD
# ==================================================
st.subheader("Delivery Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        filtered_df,
        x="delivery_days",
        nbins=30,
        title="Delivery Time Distribution (Days)"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    delivery_city = (
        filtered_df
        .groupby("customer_city")["delivery_days"]
        .mean()
        .reset_index()
        .sort_values("delivery_days")
        .head(10)
    )

    fig = px.bar(
        delivery_city,
        x="delivery_days",
        y="customer_city",
        orientation="h",
        title="Fastest Delivery Cities"
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Faster deliveries improve customer satisfaction and repeat purchases.")

st.divider()

# ==================================================
# QUESTION 22 – PAYMENT ANALYTICS
# ==================================================
st.subheader("Payment Method Analytics")

payment_trend = (
    filtered_df
    .groupby(["order_year", "payment_method"])
    .size()
    .reset_index(name="count")
)

fig = px.area(
    payment_trend,
    x="order_year",
    y="count",
    color="payment_method",
    title="Payment Method Usage Over Time"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Digital payment methods show strong adoption over the decade.")

st.divider()

# ==================================================
# QUESTION 23 – RETURNS & CANCELLATIONS
# ==================================================
st.subheader("Returns & Cancellations Analysis")

return_df = filtered_df.copy()
return_df["return_flag"] = (
    return_df["return_status"]
    .astype(str)
    .str.lower()
    .isin(["returned", "yes", "y", "true", "1"])
    .astype(int)
)

return_rate = (
    return_df
    .groupby("subcategory")["return_flag"]
    .mean()
    .reset_index()
    .sort_values("return_flag", ascending=False)
)

fig = px.bar(
    return_rate,
    x="return_flag",
    y="subcategory",
    orientation="h",
    title="Return Rate by Category"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("High return categories indicate quality or expectation gaps.")

st.divider()

# ==================================================
# QUESTION 24 – CUSTOMER SERVICE & SATISFACTION
# ==================================================
st.subheader("Customer Satisfaction & Service Quality")

if "customer_rating" in filtered_df.columns:
    rating_dist = (
        filtered_df
        .groupby("customer_rating")
        .size()
        .reset_index(name="count")
    )

    fig = px.bar(
        rating_dist,
        x="customer_rating",
        y="count",
        title="Customer Rating Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Higher ratings correlate with faster delivery and fewer returns.")
else:
    st.info("Customer rating data not available.")

st.divider()

# ==================================================
# QUESTION 25 – SUPPLY CHAIN / OPERATIONAL HEALTH
# ==================================================
st.subheader("Supply Chain & Operational Health")

col1, col2 = st.columns(2)

with col1:
    fig = px.box(
        filtered_df,
        x="subcategory",
        y="delivery_days",
        title="Delivery Time Variability by Category"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
        filtered_df,
        x="delivery_days",
        nbins=25,
        title="Overall Delivery Performance Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Operational consistency is key to supply chain efficiency.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    ---
    **Dashboard:** Operations Analytics  
    **Focus:** Delivery, Payments, Returns & Service Quality  
    **Audience:** Operations, Logistics & CX Teams
    """
)