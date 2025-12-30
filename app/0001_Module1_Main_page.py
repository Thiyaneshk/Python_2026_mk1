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

try:
    query = "SELECT * FROM OPENQUERY(ARMRPT, 'SELECT * FROM VW_TK_TERMINALS WITH UR ')"
    # zsp_a1002_bringg_efficiency_metrics_Details
    df = pd.read_sql(query, engine)
    st.dataframe(df)
except Exception as e:
    st.error(f"MSSQL connection failed: {e}")