"""
Shipping Tracker Page
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Shipping Tracker", page_icon="🚢", layout="wide")

st.title("🚢 Shipping & Maritime Tracker")
st.caption("Live vessel positions, cargo tracking, port data")

st.warning(
    "⚠️ Real-time AIS data from MarineTraffic, VesselFinder requires API keys.\n"
    "This page shows sample data. To enable live tracking, configure shipping APIs in .env"
)

tab1, tab2, tab3 = st.tabs(["🗺️ Live Vessels", "📦 Cargo Tracking", "⚓ Port Analytics"])

with tab1:
    st.subheader("Live Vessel Tracking")
    
    vessels = pd.DataFrame({
        "Vessel Name": ["MSC GULSUN", "EVER GIVEN", "OOCL Hong KONG", "MAERSK SEALAND", "CMA CGM ANTOINE"],
        "Type": ["Container", "Container", "Container", "Container", "Container"],
        "Flag": ["Switzerland", "Panama", "Hong Kong", "Denmark", "France"],
        "Current Position": ["Singapore Strait", "Suez Canal", "Port of Shanghai", "Port of Rotterdam", "Port of Antwerp"],
        "Last Update": ["15 min ago", "8 min ago", "45 min ago", "2 hours ago", "1 hour ago"],
        "Cargo": ["Electronics, Textiles", "Machinery, Auto Parts", "Semiconductors", "Industrial Equipment", "Chemical Products"]
    })
    
    st.dataframe(vessels, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Vessel Search")
        search_vessel = st.text_input("Search by vessel name or IMO:")
        if search_vessel:
            st.info(f"🔍 Would search live AIS data for: {search_vessel}")
    
    with col2:
        st.markdown("### Route Visualization")
        st.info("Interactive map would show vessel routes and positions")

with tab2:
    st.subheader("Cargo Tracking & Shipments")
    
    shipments = pd.DataFrame({
        "Shipment ID": ["SHP-2024-001", "SHP-2024-002", "SHP-2024-003", "SHP-2024-004"],
        "Origin": ["Shanghai, China", "Singapore", "Rotterdam, Netherlands", "Dubai, UAE"],
        "Destination": ["Los Angeles, USA", "Hamburg, Germany", "New York, USA", "Singapore"],
        "Cargo Type": ["Electronics", "Textiles", "Machinery", "Oil & Gas Equipment"],
        "Weight (Tons)": [450, 320, 780, 1200],
        "Status": ["In Transit", "In Port", "Loading", "Delivered"],
        "ETD": ["2024-06-15", "2024-06-10", "2024-06-20", "2024-06-05"]
    })
    
    st.dataframe(shipments, use_container_width=True)
    
    st.divider()
    
    st.markdown("### Cargo Search")
    cargo_search = st.text_input("Search by cargo type or commodity:")
    if cargo_search:
        st.info(f"📦 Searching for cargo: {cargo_search}")
    
    st.subheader("Global Cargo Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Shipments", "2,847", "+12%")
    with col2:
        st.metric("Containers in Transit", "1.2M", "-3%")
    with col3:
        st.metric("Avg Transit Time", "28 days", "+2 days")
    with col4:
        st.metric("Shipping Cost Index", "847", "-5%")

with tab3:
    st.subheader("Major Port Analytics")
    
    ports = pd.DataFrame({
        "Port": ["Singapore", "Shanghai", "Rotterdam", "Dubai", "Los Angeles", "Busan"],
        "Country": ["Singapore", "China", "Netherlands", "UAE", "USA", "South Korea"],
        "Containers (TEU)": [37.1, 43.3, 13.7, 15.6, 9.2, 22.2],
        "Ships Today": [127, 243, 58, 94, 31, 156],
        "Congestion Level": ["Low", "High", "Medium", "Medium", "Low", "High"],
        "Wait Time (hours)": [2, 18, 6, 8, 1, 16]
    })
    
    st.dataframe(ports, use_container_width=True)
    
    st.divider()
    
    st.subheader("Port Congestion Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**High Congestion** 🔴")
        st.write("Shanghai: 18h wait")
        st.write("Busan: 16h wait")
    
    with col2:
        st.markdown("**Medium Congestion** 🟡")
        st.write("Rotterdam: 6h wait")
        st.write("Dubai: 8h wait")
    
    with col3:
        st.markdown("**Low Congestion** 🟢")
        st.write("Singapore: 2h wait")
        st.write("LA: 1h wait")
