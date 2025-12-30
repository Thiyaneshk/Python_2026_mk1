import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# MSSQL connection parameters
server = st.secrets["mssql"]["server"]
database = st.secrets["mssql"]["database"]
username = st.secrets["mssql"]["username"]
password = st.secrets["mssql"]["password"]
driver = st.secrets["mssql"]["driver"]

# Create SQLAlchemy engine
engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver.replace(' ', '+')}&TrustServerCertificate=yes"
)

st.title("Test DB Connection")
st.markdown(
    """
    **:rainbow[Lets's test out DB connection!! you can build!]**
    """
)

# try:
    # query = "SELECT * FROM OPENQUERY(ARMRPT, 'CALL TMWIN.ZSP_A1002_BRINGG_EFFICIENCY_METRICS_DETAILS(''4/6/2025'',''4/19/2025'',''ARNSKENT'',''AC'')')"
    
# Example parameters
vStart = '2024-04-01'
vEnd = '2024-04-30'
vLoc = 'ARNSKENT'
vType = 'AC'

try:
    query = (
        "SELECT * FROM OPENQUERY(ARMRPT, "
        f"'SELECT * FROM TABLE(ZSP_A1002_BRINGG_EFFICIENCY_METRICS_DETAILS(''{vStart}'',''{vEnd}'',''{vLoc}'',''{vType}''))')"
    )
    df = pd.read_sql(query, engine)
    st.dataframe(df)
except Exception as e:
    st.error(f"MSSQL connection failed: {e}")