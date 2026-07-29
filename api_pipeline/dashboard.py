import streamlit as st
import psycopg2
import pandas as pd

# 1. Configure the visual web layout styling
st.set_page_config(page_title="KWASU Analytics Hub", page_icon="📊", layout="wide")

st.title("📊 KWASU Live Exchange Rate Analytics Dashboard")
st.markdown("This dashboard reads real-time currency metrics directly from your local PostgreSQL Database Engine.")

try:
    # 2. Establish connection to your database server
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Fridaous@123"
    )
    
    # 3. Pull the live data using pandas into a clean data frame matrix
    query = "SELECT currency_code, rate_to_usd, last_synchronized_at FROM global_exchange_rates;"
    df = pd.read_sql_query(query, connection)
    connection.close()

    # 4. Display the raw database grid visually
    st.subheader("📋 Live Database Table State")
    st.dataframe(df, use_container_width=True)

    # 5. Build an interactive visual bar chart automatically
    st.subheader("📈 Currency Value vs USD Visual Matrix")
    st.bar_chart(data=df, x="currency_code", y="rate_to_usd")

except Exception as e:
    st.error(f"Could not connect to database charts. Error details: {e}")