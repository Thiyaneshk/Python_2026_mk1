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

st.title("Trailer Location Viewer")
st.markdown(
    """
    **:rainbow[Select a trailer to view its current location]**
    """
)

try:
    query = "SELECT * FROM OPENQUERY(ARMRPT, 'SELECT TRAILER_ID,CLASS,STATUS,COORDINATES,LATITUDE,LONGITUDE FROM VW_TK_TRAILER_CURR_LOCATION LIMIT 100 WITH UR ')"
    df = pd.read_sql(query, engine)
    
    # Create a selection widget
    selected_trailer = st.selectbox(
        "Select a Trailer:",
        options=df['TRAILER_ID'].unique(),
        index=0
    )
    
    # Filter dataframe for selected trailer
    selected_df = df[df['TRAILER_ID'] == selected_trailer]
    
    # Display trailer details
    st.subheader(f"Trailer Details: {selected_trailer}")
    st.dataframe(selected_df)
    
    # Show the location on map
    st.subheader("Location")
    if not selected_df.empty:
        # Create a map centered on the trailer location
        st.map(
            selected_df,
            latitude='LATITUDE',
            longitude='LONGITUDE',
            size=20,  # Fixed size for single point
            color='#FF0000'  # Red color for the point
        )
        
        # Show coordinates
        lat = selected_df['LATITUDE'].values[0]
        lon = selected_df['LONGITUDE'].values[0]
        st.write(f"**Coordinates:** {lat:.4f}, {lon:.4f}")
        
        # Google Maps link
        st.markdown(
            f"[Open in Google Maps](https://www.google.com/maps?q={lat},{lon})",
            unsafe_allow_html=True
        )
    else:
        st.warning("No location data available for selected trailer")
    
    # Show all trailers table (optional)
    with st.expander("View All Trailers"):
        st.dataframe(df)

except Exception as e:
    st.error(f"MSSQL connection failed: {e}")