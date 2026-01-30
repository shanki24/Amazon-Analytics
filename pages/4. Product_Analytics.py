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
    page_title="Product Analytics | Amazon India",
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
st.title("Product Analytics Dashboard")
st.markdown(
    """
    **Insights into product performance, brand competitiveness, 
    ratings, and product lifecycle trends (2015–2025).**
    """
)

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("Product Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["order_year"].unique()),
    default=[df["order_year"].max()]
)

category_filter = st.sidebar.multiselect(
    "Select Subcategory",
    sorted(df["subcategory"].dropna().unique()),
    default=sorted(df["subcategory"].dropna().unique())[:5]
)

filtered_df = df[
    (df["order_year"].isin(year_filter)) &
    (df["subcategory"].isin(category_filter))
]

# ==================================================
# QUESTION 16 – PRODUCT PERFORMANCE DASHBOARD
# ==================================================
st.subheader("Top Performing Products")

top_products = (
    filtered_df
    .groupby("product_name")
    .agg(
        revenue=("final_amount_inr", "sum"),
        units_sold=("quantity", "sum"),
        avg_rating=("product_rating", "mean")
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
    .head(10)
)

fig = px.bar(
    top_products,
    x="revenue",
    y="product_name",
    orientation="h",
    title="Top 10 Products by Revenue"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("A small number of products contribute a large share of total revenue.")

st.divider()

# ==================================================
# QUESTION 17 – BRAND ANALYTICS
# ==================================================
st.subheader("Brand Performance & Market Share")

brand_perf = (
    filtered_df
    .groupby("brand")["final_amount_inr"]
    .sum()
    .reset_index()
    .sort_values("final_amount_inr", ascending=False)
    .head(10)
)

fig = px.pie(
    brand_perf,
    names="brand",
    values="final_amount_inr",
    title="Top Brands by Revenue Share"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Brand dominance reflects customer trust and competitive positioning.")

st.divider()

# ==================================================
# QUESTION 18 – PRODUCT LIFECYCLE ANALYSIS
# ==================================================
st.subheader("Product Lifecycle Trends")

lifecycle = (
    filtered_df
    .groupby(["order_year", "subcategory"])["final_amount_inr"]
    .sum()
    .reset_index()
)

fig = px.line(
    lifecycle,
    x="order_year",
    y="final_amount_inr",
    color="subcategory",
    title="Category Lifecycle Over Time"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("📌 Lifecycle trends show product maturity, growth, and decline phases.")

st.divider()

# ==================================================
# QUESTION 19 – PRODUCT RATING & QUALITY ANALYSIS
# ==================================================
st.subheader("Product Ratings & Sales Impact")

rating_sales = (
    filtered_df
    .groupby("product_rating")["final_amount_inr"]
    .mean()
    .reset_index()
)

fig = px.bar(
    rating_sales,
    x="product_rating",
    y="final_amount_inr",
    title="Average Revenue by Product Rating"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Higher-rated products consistently generate higher average revenue.")

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    ---
    **Dashboard:** Product Analytics  
    **Focus:** Product Performance, Brands, Lifecycle & Quality  
    **Audience:** Product, Merchandising & Inventory Teams
    """
)