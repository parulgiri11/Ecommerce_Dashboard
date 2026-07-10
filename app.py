import streamlit as st
import pandas as pd
import plotly.express as px


# Configure the page
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)


# Dashboard title
st.title("🛒 E-Commerce Sales Dashboard")
st.caption(
    "Interactive dashboard for analyzing sales performance, customer segments, and product trends."
)
st.divider()


# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("SampleSuperstore+dataset.xlsx")

df = load_data()


# Convert Order Date to datetime format
df["Order Date"] = pd.to_datetime(df["Order Date"])


# Create Month-Year column
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)


# Sidebar title
st.sidebar.title("🔍 Dashboard Filters")
st.sidebar.markdown("---")


# Region filter
region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(df["Region"].unique())
)

# Category filter
category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["Category"].unique())
)

# Segment filter
segment = st.sidebar.selectbox(
    "Select Segment",
    ["All"] + sorted(df["Segment"].unique())
)

# Filter the dataset based on the selected region
if region != "All":
    df = df[df["Region"] == region]

# Filter the dataset based on the selected category
if category != "All":
    df = df[df["Category"] == category]

# Filter the dataset based on the selected segment
if segment != "All":
    df = df[df["Segment"] == segment]


# Calculate KPIs
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_quantity = df["Quantity"].sum()


# Sales by Category
sales_by_category = df.groupby("Category")["Sales"].sum().reset_index()

# Sales by Region
sales_by_region = df.groupby("Region")["Sales"].sum().reset_index()

# Monthly Sales
monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()

# Sales by Segment
sales_by_segment = df.groupby("Segment")["Sales"].sum().reset_index()

# Top 10 Products by Sales
top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)


# Create Bar Chart
fig = px.bar(
    sales_by_category,
    x="Category",
    y="Sales",
    title="📊 Sales by Category",
    text_auto=".2s",
    color="Category",
    width=250
)

fig.update_layout(
    height=450,
    title={
        "text": "📊 Sales by Category",
        "x": 0.5,
        "xanchor": "center"
    }
)

fig.update_traces(
    marker=dict(
        line=dict(
            color="white",        # Border color
            width=1.5             # Border thickness
        )
    ),
    width=0.6                    # Width of bars
)


# Create Sales by Region Chart
fig_region = px.bar(
    sales_by_region,
    x="Region",
    y="Sales",
    title="🌍 Sales by Region",
    text_auto=".2s",
    color="Region",
    width=250
)

fig_region.update_layout(
    height=450,
    title={
        "text": "🌍 Sales by Region",
        "x": 0.5,
        "xanchor": "center"
    },
)

fig_region.update_traces(
    marker=dict(
        line=dict(
            color="white",        # Border color
            width=1.5             # Border thickness
        )
    ),
    width=0.6                    # Width of bars
)

# Create Monthly Sales Trend Chart
fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    title="📈 Monthly Sales Trend",
    markers=True
)

fig_monthly.update_layout(
    height=450,
    title={
        "text": "📈 Monthly Sales Trend",
        "x": 0.5,
        "xanchor": "center"
    }
)

# Create Sales by Segment Pie Chart
fig_segment = px.pie(
    sales_by_segment,
    names="Segment",
    values="Sales",
    title="🥧 Sales by Segment",
    hole=0.4
)

fig_segment.update_layout(
    height=450,
    title={
        "text": "🥧 Sales by Segment",
        "x": 0.5,
        "xanchor": "center"
    }
)

# Create Top 10 Products Chart
fig_top_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="🏆 Top 10 Products by Sales",
    text_auto=".2s",
    color="Sales"
)

fig_top_products.update_layout(
    height=420,
    title={
        "text": "🏆 Top 10 Products by Sales",
        "x": 0.5,
        "xanchor": "center"
    }
)


# Create four columns
col1, col2, col3, col4 = st.columns(
    [1, 1, 1, 1],
    gap="medium"
)

# Display KPI cards
with col1:
    st.markdown(f"""
    <div style="
        background-color:#4CAF50;
        padding:10px;
        border-radius:12px;
        text-align:center;
        color:white;
        box-shadow:2px 2px 8px rgba(0,0,0,0.2);
    ">
        <h5>Total Sales</h5>
        <h3>₹{total_sales:.2f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background-color:#2196F3;
        padding:10px;
        border-radius:12px;
        text-align:center;
        color:white;
        box-shadow:2px 2px 8px rgba(0,0,0,0.2);
    ">
        <h5>Total Profit</h5>
        <h3>₹{total_profit:.2f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background-color:#FF9800;
        padding:10px;
        border-radius:12px;
        text-align:center;
        color:white;
        box-shadow:2px 2px 8px rgba(0,0,0,0.2);
    ">
        <h5>Total Orders</h5>
        <h3>{total_orders:,}</h3>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
        background-color:#9C27B0;
        padding:10px;
        border-radius:12px;
        text-align:center;
        color:white;
        box-shadow:2px 2px 8px rgba(0,0,0,0.2);
    ">
        <h5>Total Quantity</h5>
        <h3>{total_quantity:,}</h3>
    </div>
    """, unsafe_allow_html=True)

# Space between KPI cards and Sales Overview
# st.write("")
# st.write("")     #This is to add some space between the KPI cards and the Sales Overview section. You can adjust the number of st.write("") calls to increase or decrease the spacing as needed.
                             #OR

st.markdown("<br><br>", unsafe_allow_html=True) #for adding space between KPI cards and Sales Overview section. You can adjust the number of <br> tags to increase or decrease the spacing as needed.

st.subheader("📊 Sales Overview")

# Create two columns for charts
chart1, chart2 = st.columns([1, 1], gap="large")
with chart1:
    st.plotly_chart(fig, use_container_width=True)
with chart2:
    st.plotly_chart(fig_region, use_container_width=True)


st.subheader("📈 Sales Trends & Customer Segments")
   
# Create two columns for second row of charts
chart3, chart4 = st.columns([1, 1], gap="large")
with chart3:
    st.plotly_chart(fig_monthly, use_container_width=True)
with chart4:
    st.plotly_chart(fig_segment, use_container_width=True)


st.subheader("🏆 Best Selling Products")

# Third row - Top 10 Products
st.plotly_chart(fig_top_products, use_container_width=True)


# Download Filtered Data Button
st.divider()
st.subheader("📥 Download Filtered Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)


# Find the number of rows and columns
# st.write("Dataset Shape:", df.shape)

# # Display all column names
# st.write("Column Names:")
# st.write(df.columns)

# # Display the dataset
# st.dataframe(df)


st.divider()

st.markdown(
    """
    <div style="text-align:center; color:gray;">
        <h5>🛒 E-Commerce Sales Dashboard</h5>
        <p>Developed by <b>Parul Giri</b></p>
        <p>Built using Python, Pandas, Plotly & Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)