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
    query = "SELECT * FROM OPENQUERY(ARMRPT, 'SELECT TRAILER_ID,CLASS,STATUS,COORDINATES,LATITUDE,LONGITUDE FROM VW_TK_TRAILER_CURR_LOCATION LIMIT 100 WITH UR ')"
    # zsp_a1002_bringg_efficiency_metrics_Details
    df = pd.read_sql(query, engine)
    st.dataframe(df)
    st.map(df)
    # Round latitude and longitude to 2 decimal places
    # df['LATITUDE'] = df['LATITUDE'].round(2)
    # df['LONGITUDE'] = df['LONGITUDE'].round(2)
    # st.map(df, latitude="LATITUDE", longitude="LONGITUDE", size="CLASS") #, color="STATUS")
except Exception as e:
    st.error(f"MSSQL connection failed: {e}")