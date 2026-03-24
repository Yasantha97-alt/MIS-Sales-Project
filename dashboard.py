import streamlit as st
import sqlite3
import pandas as pd

st.title("📊 Sales Dashboard")

try:
    conn = sqlite3.connect('data.db')
    df = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()

    if not df.empty:
        st.subheader("Raw Data")
        st.dataframe(df)

        st.subheader("Sales by Outlet")
        summary = df.groupby("outlet")["sales"].sum()
        st.bar_chart(summary)
    else:
        st.warning("The database is empty. Add some data using your Flask form first!")

except Exception as e:
    st.error("Could not find the database. Make sure you have run the Flask app at least once to create 'data.db'.")