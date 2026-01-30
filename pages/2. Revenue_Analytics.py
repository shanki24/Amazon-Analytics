import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Revenue Analytics | Amazon India",
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
st.title("Revenue Analytics Dashboard")
st.markdown(
    """
    **Detailed analysis of revenue performance, growth patterns, 
    geographic contribution, and pricing effectiveness (2015–2025).**
    """
)

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("Revenue Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["order_year"].unique()),
    default=sorted(df["order_year"].unique())
)

category_filter = st.sidebar.multiselect(
    "Select Subcategory",
    sorted(df["subcategory"].dropna().unique()),
    default=sorted(df["subcategory"].dropna().unique())
)

filtered_df = df[
    (df["order_year"].isin(year_filter)) &
    (df["subcategory"].isin(category_filter))
]

# --------------------------------------------------
# Q6 – REVENUE TREND ANALYSIS
# --------------------------------------------------
st.subheader("Revenue Trend Analysis")

col1, col2 = st.columns(2)

with col1:
    yearly_rev = filtered_df.groupby("order_year")["final_amount_inr"].sum().reset_index()
    fig = px.line(
        yearly_rev,
        x="order_year",
        y="final_amount_inr",
        markers=True,
        title="Yearly Revenue Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    quarterly_rev = filtered_df.groupby(
        ["order_year", "order_quarter"]
    )["final_amount_inr"].sum().reset_index()

    fig = px.bar(
        quarterly_rev,
        x="order_quarter",
        y="final_amount_inr",
        color="order_year",
        barmode="group",
        title="Quarterly Revenue Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Revenue trends reveal long-term growth and quarterly seasonality.")

st.divider()

# --------------------------------------------------
# Q6 – MONTHLY SEASONALITY
# --------------------------------------------------
st.subheader("Monthly Seasonality Analysis")

monthly_rev = filtered_df.groupby("order_month")["final_amount_inr"].sum().reset_index()

fig = px.bar(
    monthly_rev,
    x="order_month",
    y="final_amount_inr",
    title="Monthly Revenue Distribution"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Peak months indicate seasonal demand and promotional effectiveness.")

st.divider()

# --------------------------------------------------
# Q7 – CATEGORY PERFORMANCE
# --------------------------------------------------
st.subheader("Category Revenue Performance")

cat_rev = filtered_df.groupby("subcategory")["final_amount_inr"].sum().reset_index()

fig = px.treemap(
    cat_rev,
    path=["subcategory"],
    values="final_amount_inr",
    title="Revenue Contribution by Category"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Category-level insights highlight core revenue drivers.")

st.divider()

# --------------------------------------------------
# Q8 – GEOGRAPHIC REVENUE ANALYSIS
# --------------------------------------------------
st.subheader("Geographic Revenue Analysis")

col1, col2 = st.columns(2)

with col1:
    state_rev = filtered_df.groupby("customer_state")["final_amount_inr"].sum().reset_index()
    state_rev = state_rev.sort_values("final_amount_inr", ascending=False).head(10)

    fig = px.bar(
        state_rev,
        x="final_amount_inr",
        y="customer_state",
        orientation="h",
        title="Top 10 States by Revenue"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    city_rev = filtered_df.groupby("customer_city")["final_amount_inr"].sum().reset_index()
    city_rev = city_rev.sort_values("final_amount_inr", ascending=False).head(10)

    fig = px.bar(
        city_rev,
        x="final_amount_inr",
        y="customer_city",
        orientation="h",
        title="Top 10 Cities by Revenue"
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Metro and Tier-1 cities contribute a significant share of revenue.")

st.divider()

# --------------------------------------------------
# Q9 – FESTIVAL SALES ANALYTICS
# --------------------------------------------------
st.subheader("Festival Sales Impact")

festival_rev = filtered_df.groupby("is_festival_sale")["final_amount_inr"].sum().reset_index()

fig = px.bar(
    festival_rev,
    x="is_festival_sale",
    y="final_amount_inr",
    title="Festival vs Non-Festival Revenue"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Festival campaigns drive significant revenue spikes.")

st.divider()

# --------------------------------------------------
# Q10 – PRICE OPTIMIZATION ANALYSIS
# --------------------------------------------------
st.subheader("Price & Discount Impact")

if "discount_percent" in filtered_df.columns:
    fig = px.scatter(
        filtered_df,
        x="discount_percent",
        y="final_amount_inr",
        opacity=0.4,
        title="Discount Percentage vs Revenue"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Optimal discount ranges improve revenue without eroding margins.")
else:
    st.info("Discount data not available.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    ---
    **Dashboard:** Revenue Analytics  
    **Focus:** Growth, Seasonality, Geography & Pricing  
    **Audience:** Finance, Strategy & Revenue Teams
    """
)
