import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Analytics | Amazon India",
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
st.title("Customer Analytics Dashboard")
st.markdown(
    """
    **Deep-dive into customer behavior, segmentation, retention, 
    and demographic patterns (2015–2025).**
    """
)

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("🔎 Customer Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["order_year"].unique()),
    default=sorted(df["order_year"].unique())
)

prime_filter = st.sidebar.selectbox(
    "Prime Membership",
    ["All", 1, 0]
)

filtered_df = df[df["order_year"].isin(year_filter)]

if prime_filter != "All":
    filtered_df = filtered_df[filtered_df["is_prime_member"] == prime_filter]

# ==================================================
# QUESTION 11 – CUSTOMER SEGMENTATION (RFM)
# ==================================================
st.subheader("Customer Segmentation (RFM Analysis)")

@st.cache_data
def compute_rfm(data):
    rfm = data.groupby("customer_id").agg({
        "order_date": lambda x: (data["order_date"].max() - x.max()).days,
        "transaction_id": "count",
        "final_amount_inr": "sum"
    }).reset_index()

    rfm.columns = ["customer_id", "recency", "frequency", "monetary"]

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])

    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm["segment"] = kmeans.fit_predict(rfm_scaled)

    return rfm

rfm = compute_rfm(filtered_df)

fig = px.scatter(
    rfm,
    x="frequency",
    y="monetary",
    color="segment",
    title="Customer Segments based on RFM"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("RFM segmentation helps identify loyal, high-value, and at-risk customers.")

st.divider()

# ==================================================
# QUESTION 12 – CUSTOMER JOURNEY & PURCHASE BEHAVIOR
# ==================================================
st.subheader("Customer Purchase Behavior")

purchase_freq = filtered_df.groupby("customer_id")["transaction_id"].count().reset_index()

fig = px.histogram(
    purchase_freq,
    x="transaction_id",
    nbins=40,
    title="Customer Purchase Frequency Distribution"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("📌 Majority customers are low-frequency buyers, while a small group drives repeat sales.")

st.divider()

# ==================================================
# QUESTION 13 – PRIME MEMBERSHIP ANALYTICS
# ==================================================
st.subheader("Prime vs Non-Prime Customer Analysis")

col1, col2 = st.columns(2)

with col1:
    prime_aov = filtered_df.groupby("is_prime_member")["final_amount_inr"].mean().reset_index()

    fig = px.bar(
        prime_aov,
        x="is_prime_member",
        y="final_amount_inr",
        title="Average Order Value: Prime vs Non-Prime"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    prime_freq = filtered_df.groupby("is_prime_member")["transaction_id"].count().reset_index()

    fig = px.bar(
        prime_freq,
        x="is_prime_member",
        y="transaction_id",
        title="Order Volume: Prime vs Non-Prime"
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Prime members exhibit higher order values and stronger engagement.")

st.divider()

# ==================================================
# QUESTION 14 – CUSTOMER RETENTION & LIFECYCLE
# ==================================================
st.subheader("Customer Retention & Lifetime Value")

clv = filtered_df.groupby("customer_id")["final_amount_inr"].sum().reset_index()

fig = px.histogram(
    clv,
    x="final_amount_inr",
    nbins=50,
    title="Customer Lifetime Value (CLV) Distribution"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("A long-tail CLV distribution indicates few high-value customers driving revenue.")

st.divider()

# ==================================================
# QUESTION 15 – DEMOGRAPHICS & BEHAVIOR
# ==================================================
st.subheader("Demographic & Behavioral Insights")

col1, col2 = st.columns(2)

with col1:
    age_spend = filtered_df.groupby("customer_age_group")["final_amount_inr"].mean().reset_index()

    fig = px.bar(
        age_spend,
        x="customer_age_group",
        y="final_amount_inr",
        title="Average Spend by Age Group"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    tier_spend = filtered_df.groupby("customer_tier")["final_amount_inr"].mean().reset_index()

    fig = px.bar(
        tier_spend,
        x="customer_tier",
        y="final_amount_inr",
        title="Average Spend by Customer Tier"
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Demographic segmentation supports targeted marketing and personalization strategies.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    ---
    **Dashboard:** Customer Analytics  
    **Focus:** Segmentation, Retention & Customer Value  
    **Audience:** Marketing, CRM & Strategy Teams
    """
)
