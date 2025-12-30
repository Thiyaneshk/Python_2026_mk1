import streamlit as st
import pandas as pd
import pyodbc

# MSSQL connection parameters
server = st.secrets["mssql"]["server"]
database = st.secrets["mssql"]["database"]
username = st.secrets["mssql"]["username"]
password = st.secrets["mssql"]["password"]
# driver = st.secrets["mssql"]["driver"]
driver = "ODBC Driver 17 for SQL Server"

conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
)

st.title("Test DB Connection")
st.markdown(
    """
    **:rainbow[Lets's test out DB connection!! you can build!]**

    """
)

# st.write(pyodbc.drivers())

# st.write(f"Connection string: {conn_str}")

# --- MSSQL Data Fetch Example ---
try:
    conn = pyodbc.connect(conn_str)
    # query = "SELECT * FROM VW_TK_TERMINALS ORDER BY 4, 2"
    query = "SELECT * FROM OPENQUERY(ARMRPT, 'SELECT * FROM VW_TK_TERMINALS WITH UR ')";

    df = pd.read_sql(query, conn)
    st.dataframe(df)
    conn.close()
except Exception as e:
    st.error(f"MSSQL connection failed: {e}")

# if st.button("Click here!"):
#     st.balloons()