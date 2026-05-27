"""
Cargo Planes Tracker Page
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cargo Planes", page_icon="✈️", layout="wide")

st.title("✈️ Cargo Planes Tracker")
st.caption("Live cargo flight tracking, routes, and capacity")

st.warning(
    "⚠️ Real-time cargo flight data requires specialized aviation APIs.\n"
    "This page shows sample data structure. Integration available via FlightRadar24 or similar APIs."
)

tab1, tab2, tab3 = st.tabs(["📍 Live Flights", "📦 Cargo Capacity", "🌐 Routes"])

with tab1:
    st.subheader("Active Cargo Flights")
    
    flights = pd.DataFrame({
        "Flight": ["FX901", "DL8084", "AA8821", "KL7731", "AF6842"],
        "Aircraft": ["Boeing 777F", "Boeing 767F", "Airbus A330F", "Boeing 747F", "Boeing 777F"],
        "Origin": ["Shanghai (PVG)", "Memphis (MEM)", "Los Angeles (LAX)", "Amsterdam (AMS)", "Paris (CDG)"],
        "Destination": ["Los Angeles (LAX)", "Indianapolis (IND)", "Miami (MIA)", "Tokyo (NRT)", "Singapore (SIN)"],
        "Cargo Type": ["Electronics", "Pharmaceuticals", "Perishables", "Machinery", "Components"],
        "Cargo Weight (kg)": [90000, 58000, 76000, 85000, 68000],
        "Status": ["In Flight", "In Flight", "Landed", "Pre-takeoff", "In Flight"],
        "ETA": ["2024-06-01 14:30", "2024-06-01 08:45", "2024-06-01 06:15", "2024-06-02 09:30", "2024-06-02 16:00"]
    })
    
    st.dataframe(flights, use_container_width=True)
    
    st.divider()
    
    st.markdown("### Flight Search")
    col1, col2 = st.columns(2)
    
    with col1:
        flight_search = st.text_input("Search by flight number:")
        if flight_search:
            st.info(f"✈️ Searching for flight: {flight_search}")
    
    with col2:
        route_search = st.text_input("Search by route (e.g., SFO-NYC):")
        if route_search:
            st.info(f"📍 Searching for route: {route_search}")

with tab2:
    st.subheader("Global Cargo Capacity & Utilization")
    
    capacity_data = pd.DataFrame({
        "Airline": ["FedEx", "DHL Aviation", "Lufthansa Cargo", "AirBridge Cargo", "Cargolux"],
        "Aircraft Count": [655, 260, 130, 60, 40],
        "Capacity (tons/day)": [8700, 3500, 1800, 900, 550],
        "Current Utilization": ["92%", "87%", "79%", "85%", "81%"],
        "Rate Change (YoY)": ["+8%", "+12%", "-2%", "+15%", "+5%"]
    })
    
    st.dataframe(capacity_data, use_container_width=True)
    
    st.divider()
    
    st.subheader("Global Cargo Aviation Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Cargo Flights", "1,247", "+3%")
    with col2:
        st.metric("Daily Capacity", "52,000 tons", "+5%")
    with col3:
        st.metric("Avg Utilization", "87%", "+2%")
    with col4:
        st.metric("Peak Route", "Chicago-LA", "daily")
    
    st.divider()
    
    st.subheader("Cargo Type Distribution")
    
    cargo_types = pd.DataFrame({
        "Type": ["Electronics", "Pharmaceuticals", "Perishables", "Machinery", "Auto Parts", "Other"],
        "Volume %": [35, 20, 15, 12, 10, 8]
    })
    
    st.bar_chart(cargo_types.set_index("Type")["Volume %"])

with tab3:
    st.subheader("Major Cargo Routes")
    
    routes = pd.DataFrame({
        "Route": [
            "Asia to North America",
            "Europe to Asia",
            "Intra-Asia",
            "North America to Europe",
            "Middle East to Asia"
        ],
        "Daily Flights": [156, 132, 89, 67, 54],
        "Avg Cargo (tons)": [78, 65, 52, 61, 45],
        "Peak Times": [
            "Mon-Wed",
            "Tue-Thu",
            "Daily",
            "Wed-Fri",
            "Sun-Tue"
        ],
        "Demand Trend": ["+12%", "+8%", "+15%", "+3%", "+18%"]
    })
    
    st.dataframe(routes, use_container_width=True)
    
    st.divider()
    
    st.subheader("Route Analytics")
    
    selected_route = st.selectbox(
        "Select route for details:",
        routes["Route"].tolist()
    )
    
    if selected_route:
        route_data = routes[routes["Route"] == selected_route].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Daily Flights", route_data["Daily Flights"])
        with col2:
            st.metric("Avg Cargo per Flight", f"{route_data['Avg Cargo (tons)']} tons")
        with col3:
            st.metric("Demand Trend", route_data["Demand Trend"])
        
        st.markdown(f"**Peak Times:** {route_data['Peak Times']}")
