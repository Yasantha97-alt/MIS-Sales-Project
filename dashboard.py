import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# --- CLOUD CONFIGURATION ---
DB_URL = "postgresql://postgres.iyzhqjmghcwykhpmlxzw:LankaSales2026@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

st.set_page_config(page_title="FLI Sales Dashboard", layout="wide")

def load_data():
    try:
        conn = psycopg2.connect(DB_URL)
        query = "SELECT date, outlet, sales FROM sales ORDER BY date DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        # Convert date column to actual datetime objects
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"Error connecting to Cloud: {e}")
        return pd.DataFrame()

# --- DASHBOARD UI ---
st.title("📊 FLI Strategic Planning - Sales Dashboard")
st.markdown("---")

df = load_data()

if not df.empty:
    # 1. Key Metrics (KPIs)
    col1, col2, col3 = st.columns(3)
    total_sales = df['sales'].sum()
    total_entries = len(df)
    avg_sales = df['sales'].mean()

    col1.metric("Total Sales (LKR)", f"{total_sales:,.2f}")
    col2.metric("Total Records", total_entries)
    col3.metric("Average Sale", f"{avg_sales:,.2f}")

    st.markdown("---")

    # 2. Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Sales by Outlet")
        fig_pie = px.pie(df, values='sales', names='outlet', hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)

    with chart_col2:
        st.subheader("Sales Trend Over Time")
        # Group by date for line chart
        trend_df = df.groupby('date')['sales'].sum().reset_index()
        fig_line = px.line(trend_df, x='date', y='sales', markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    # 3. Raw Data Table
    st.subheader("Recent Cloud Entries")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("No data found in the cloud. Please enter some data using the form first!")

# Refresh Button
if st.button('🔄 Refresh Data'):
    st.rerun()
