import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt

# Load cleaned dataset with human-readable column names
df = pd.read_csv("cleaned_water_quality_for_app.csv", parse_dates=["Date"])

st.set_page_config(layout="wide")
st.title("💧 Mercer County Water Quality Dashboard")

st.markdown("""
Explore 30+ years of water quality monitoring across Mercer County, NJ.  
Use the filters to focus on specific sites, parameters, and time periods.  
Visualize results, compare sites, and download filtered data.
""")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Parameter selector
parameters = sorted(df['Parameter'].dropna().unique())
selected_param = st.sidebar.selectbox("Select Parameter", parameters)

# Location selector
locations = df[df['Parameter'] == selected_param]['Location'].dropna().unique()
selected_locations = st.sidebar.multiselect(
    "Select Locations",
    sorted(locations),
    default=sorted(locations[:3])
)

# Date range selector
min_date = df['Date'].min()
max_date = df['Date'].max()
selected_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data
filtered_df = df[
    (df['Parameter'] == selected_param) &
    (df['Location'].isin(selected_locations)) &
    (df['Date'] >= pd.to_datetime(selected_range[0])) &
    (df['Date'] <= pd.to_datetime(selected_range[1]))
].copy()

# Ensure value is numeric
filtered_df["Value"] = pd.to_numeric(filtered_df["Value"], errors="coerce")

# Layout: map and chart side by side
col1, col2 = st.columns([1.2, 1])

# Map
with col1:
    st.subheader("📍 Monitoring Locations")
    map_data = filtered_df[['Location', 'Latitude', 'Longitude']].dropna().drop_duplicates()
    if not map_data.empty:
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=map_data['Latitude'].mean(),
                longitude=map_data['Longitude'].mean(),
                zoom=10,
                pitch=0
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=map_data,
                    get_position='[Longitude, Latitude]',
                    get_radius=100,
                    get_fill_color=[0, 128, 255],
                    pickable=True
                )
            ]
        ))
    else:
        st.info("No map data available for this filter.")

# Time series chart
with col2:
    st.subheader("📈 Time Series")
    if not filtered_df.empty:
        chart = alt.Chart(filtered_df).mark_line(point=True).encode(
            x='Date:T',
            y='Value:Q',
            color='Location:N',
            tooltip=['Date', 'Location', 'Value', 'Unit']
        ).properties(height=350)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No data to display for this selection.")

# Table + download
st.markdown("### 📄 Filtered Data Table")
st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False)
st.download_button("⬇️ Download CSV", csv, file_name="filtered_water_quality.csv", mime="text/csv")