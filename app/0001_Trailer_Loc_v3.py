import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
import plotly.express as px  # Add this import

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
    **:rainbow[Select one or more trailers to view their locations]**
    """
)

try:
    query = "SELECT * FROM OPENQUERY(ARMRPT, 'SELECT TRAILER_ID,CLASS,STATUS,COORDINATES,LATITUDE,LONGITUDE,GOOGLE_MAPS_URL FROM VW_TK_TRAILER_CURR_LOCATION LIMIT 100 WITH UR ')"
    df = pd.read_sql(query, engine)

    # Layout: Pie chart on the side of trailer selection
    col1, col2 = st.columns([1, 2])

    with col1:
        # Multi-select widget for trailers, default is blank
        selected_trailers = st.multiselect(
            "Select Trailers:",
            options=df['TRAILER_ID'].unique(),
            default=[]
        )
        # Pie chart of trailer counts by STATUS
        status_counts = df['STATUS'].value_counts().reset_index()
        status_counts.columns = ['STATUS', 'COUNT']
        fig_status = px.pie(status_counts, names='STATUS', values='COUNT', title="Trailer Distribution by Status")
        fig_status.update_traces(textinfo='percent+label')
        fig_status.update_layout(showlegend=True)
        st.plotly_chart(fig_status, use_container_width=True)

        # Pie chart of trailer counts by CLASS
        class_counts = df['CLASS'].value_counts().reset_index()
        class_counts.columns = ['CLASS', 'COUNT']
        fig_class = px.pie(class_counts, names='CLASS', values='COUNT', title="Trailer Distribution by Class")
        fig_class.update_traces(textposition='inside', textinfo='percent+label')
        fig_class.update_layout(showlegend=True)
        st.plotly_chart(fig_class, use_container_width=True)


    with col2:
        # Filter dataframe for selected trailers
        selected_df = df[df['TRAILER_ID'].isin(selected_trailers)]

        # Show the location(s) on map
        if not selected_df.empty:
            map_df = selected_df
        else:
            map_df = df

        mean_lat = map_df['LATITUDE'].mean()
        mean_lon = map_df['LONGITUDE'].mean()
        m = folium.Map(location=[mean_lat, mean_lon], zoom_start=8)

        # Add markers for each selected trailer
        if not selected_df.empty:
            for _, row in selected_df.iterrows():
                folium.Marker(
                    location=[row['LATITUDE'], row['LONGITUDE']],
                    popup=f"Trailer: {row['TRAILER_ID']}",
                    # icon=folium.Icon(color='red')
                    icon=folium.Icon(color='red', icon='truck', prefix='fa')  # Truck icon
                ).add_to(m)

        # Always show heatmap for current map_df
        heat_data = map_df[['LATITUDE', 'LONGITUDE']].values.tolist()
        HeatMap(heat_data, radius=15).add_to(m)

        st_folium(m, width="100%", height=1000)

    # Show all trailers table (optional)
    # with st.expander("View All Trailers"):
    #     st.dataframe(df)
    with st.expander("View All Trailers"):
        df_display = df.copy()
        # Make the GOOGLE_MAPS_URL a clickable link
        df_display['GOOGLE_MAPS_URL'] = df_display['GOOGLE_MAPS_URL'].apply(
            lambda url: f'<a href="{url}" target="_blank">Open in Google Maps</a>' if pd.notnull(url) else ""
        )
        # Show as HTML table with links
        st.markdown(
            df_display.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
except Exception as e:
    st.error(f"MSSQL connection failed: {e}")