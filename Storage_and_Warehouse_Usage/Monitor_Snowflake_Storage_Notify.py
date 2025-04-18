import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
import requests
import os

# --- Page config ---
st.set_page_config(page_title="Snowflake Storage Monitor", layout="wide")
st.title("📦 Snowflake Storage Monitoring Dashboard with Cortex AI")

# --- Sidebar configs ---
with st.sidebar:
    st.header("🔧 Configuration")
    days_back = st.slider("Days to Monitor", 7, 90, 30)
    run_anomaly = st.checkbox("Run Anomaly Detection", value=True)
    run_forecast = st.checkbox("Run Forecasting", value=True)
    run_summary = st.checkbox("Generate AI Summary", value=True)

# --- Snowflake connection ---
@st.cache_resource
def get_conn():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database="SNOWFLAKE",
        schema="ACCOUNT_USAGE"
    )

conn = get_conn()

# --- Query storage usage ---
st.subheader("📊 Table Storage Usage (Last {} Days)".format(days_back))
query = f"""
SELECT
    TABLE_NAME,
    USAGE_DATE,
    SUM(BYTES)/(1024*1024*1024) AS SIZE_GB
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE USAGE_DATE >= DATEADD(day, -{days_back}, CURRENT_DATE())
GROUP BY TABLE_NAME, USAGE_DATE
ORDER BY TABLE_NAME, USAGE_DATE;
"""
df = pd.read_sql(query, conn)

# --- Top 5 growing tables chart ---
latest = df[df['USAGE_DATE'] == df['USAGE_DATE'].max()]
top_tables = latest.sort_values(by='SIZE_GB', ascending=False).head(5)['TABLE_NAME'].tolist()
df_top = df[df['TABLE_NAME'].isin(top_tables)]
fig = px.line(df_top, x='USAGE_DATE', y='SIZE_GB', color='TABLE_NAME', markers=True)
st.plotly_chart(fig, use_container_width=True)

# --- Anomaly Detection ---
if run_anomaly:
    st.subheader("⚠️ Anomaly Detection")
    anomaly_query = f"""
    SELECT * FROM TABLE(
        SNOWFLAKE.ML.ANOMALY_DETECTION(
            INPUT => (
                SELECT
                    TABLE_NAME,
                    USAGE_DATE,
                    SUM(BYTES)/(1024*1024*1024) AS SIZE_GB
                FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
                WHERE USAGE_DATE >= DATEADD(day, -{days_back}, CURRENT_DATE())
                GROUP BY TABLE_NAME, USAGE_DATE
            ),
            TIMESTAMP_COLNAME => 'USAGE_DATE',
            TARGET_COLNAME => 'SIZE_GB',
            ID_COLNAME => 'TABLE_NAME'
        )
    );
    """
    df_anomalies = pd.read_sql(anomaly_query, conn)
    st.dataframe(df_anomalies[df_anomalies['IS_ANOMALY'] == True])

# --- Forecasting ---
if run_forecast:
    st.subheader("🔮 Forecasted Growth")
    forecast_query = f"""
    SELECT * FROM TABLE(
        SNOWFLAKE.ML.FORECAST(
            INPUT => (
                SELECT
                    TABLE_NAME,
                    USAGE_DATE,
                    SUM(BYTES)/(1024*1024*1024) AS SIZE_GB
                FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
                WHERE USAGE_DATE >= DATEADD(day, -{days_back}, CURRENT_DATE())
                GROUP BY TABLE_NAME, USAGE_DATE
            ),
            TIMESTAMP_COLNAME => 'USAGE_DATE',
            TARGET_COLNAME => 'SIZE_GB',
            ID_COLNAME => 'TABLE_NAME',
            PREDICT_FOR => INTERVAL '7 day'
        )
    );
    """
    df_forecast = pd.read_sql(forecast_query, conn)
    st.dataframe(df_forecast[df_forecast['TIMESTAMP'] == df_forecast['TIMESTAMP'].max()])

# --- Cortex Summary ---
if run_summary:
    st.subheader("🧠 Cortex AI Summary")
    summary_query = """
    WITH growth AS (
        SELECT
            TABLE_NAME,
            MIN(USAGE_DATE) AS start_date,
            MAX(USAGE_DATE) AS end_date,
            MIN(BYTES)/(1024*1024*1024) AS start_gb,
            MAX(BYTES)/(1024*1024*1024) AS end_gb
        FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
        WHERE USAGE_DATE >= DATEADD(day, -7, CURRENT_DATE())
        GROUP BY TABLE_NAME
    )
    SELECT
        SNOWFLAKE.CORTEX.COMPLETE(
            'Summarize Snowflake storage growth: ' ||
            LISTAGG(
                'Table ' || TABLE_NAME || ' grew from ' || ROUND(start_gb, 2) ||
                'GB to ' || ROUND(end_gb, 2) || 'GB.', ' '
            ),
            'gpt-3.5'
        ) AS summary
    FROM growth;
    """
    df_summary = pd.read_sql(summary_query, conn)
    st.info(df_summary.iloc[0]['SUMMARY'])
