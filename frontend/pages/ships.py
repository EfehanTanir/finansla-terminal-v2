"""SHIP TRACKER PAGE - AISHub free API"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.shared import *
import plotly.graph_objects as go

VESSEL_TYPES = {
    0: "Unknown", 1: "Reserved", 20: "WIG", 21: "WIG Hazardous A",
    30: "Fishing", 31: "Towing", 32: "Towing Large",
    36: "Sailing", 37: "Pleasure Craft",
    60: "Passenger", 61: "Passenger Hazardous A",
    70: "Cargo", 71: "Cargo Hazardous A",
    80: "Tanker", 81: "Tanker Hazardous A",
    89: "Tanker Other", 90: "Other",
}

MAJOR_PORTS = {
    "Istanbul (Bosphorus)": (41.0, 29.0),
    "Rotterdam": (51.9, 4.5),
    "Singapore": (1.3, 103.8),
    "Shanghai": (31.2, 121.5),
    "Los Angeles": (33.7, -118.2),
    "Dubai (Jebel Ali)": (24.9, 55.0),
    "Hamburg": (53.5, 10.0),
    "Antwerp": (51.2, 4.4),
    "Piraeus (Athens)": (37.9, 23.6),
    "New York": (40.7, -74.0),
    "Tokyo": (35.6, 139.8),
    "Mumbai": (18.9, 72.8),
}

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">🚢 SHIP TRACKER</span>
        <span style="color:#555; font-size:10px;">AIS VESSEL DATA · FREE API · LIVE POSITIONS</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #0099ff; 
                padding:8px 12px; margin-bottom:16px; font-size:10px; color:#888;">
        ℹ Data sourced from <span style="color:#0099ff;">AISHub</span> (free anonymous tier) and 
        <span style="color:#0099ff;">OpenSky Network</span>. Coverage may be limited in some regions.
        For full coverage, register at <a href="https://www.aishub.net" target="_blank" style="color:#ff6600;">aishub.net</a> (free).
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🗺  LIVE MAP", "📋  VESSEL TABLE"])
    
    with tab1:
        col_port, col_radius = st.columns([2, 1])
        with col_port:
            port = st.selectbox("Select Region / Port", list(MAJOR_PORTS.keys()), key="ship_port")
        with col_radius:
            radius = st.slider("Radius (nm)", 50, 500, 200, 50, key="ship_radius")
        
        lat, lon = MAJOR_PORTS[port]
        
        col_lat, col_lon = st.columns(2)
        with col_lat:
            custom_lat = st.number_input("Custom Lat", value=lat, min_value=-90.0, max_value=90.0, format="%.4f", key="ship_lat")
        with col_lon:
            custom_lon = st.number_input("Custom Lon", value=lon, min_value=-180.0, max_value=180.0, format="%.4f", key="ship_lon")
        
        if st.button("🔍 SEARCH VESSELS", key="ship_search"):
            with st.spinner(f"Fetching vessels near {port}..."):
                data = api_get(f"{api_url}/api/ships?lat={custom_lat}&lon={custom_lon}&radius={radius}", timeout=20)
            
            if data:
                vessels = data.get("vessels", [])
                count = data.get("count", 0)
                
                st.markdown(f"<div style='color:#00cc66; font-size:11px; margin-bottom:8px;'>✓ {count} vessels found</div>", unsafe_allow_html=True)
                
                if vessels:
                    # Plotly map
                    lats = [v.get("lat", 0) for v in vessels if v.get("lat")]
                    lons = [v.get("lon", 0) for v in vessels if v.get("lon")]
                    names = [v.get("name", "Unknown") for v in vessels if v.get("lat")]
                    destinations = [v.get("destination", "—") for v in vessels if v.get("lat")]
                    speeds = [v.get("speed", 0) for v in vessels if v.get("lat")]
                    flags = [v.get("flag", "") for v in vessels if v.get("lat")]
                    
                    texts = [
                        f"<b>{n}</b><br>Dest: {d}<br>Speed: {s:.1f} kn<br>Flag: {f}"
                        for n, d, s, f in zip(names, destinations, speeds, flags)
                    ]
                    
                    fig = go.Figure()
                    
                    # Vessel markers by speed
                    colors = ["#ff6600" if s > 15 else "#0099ff" if s > 5 else "#555" for s in speeds]
                    
                    fig.add_trace(go.Scattermap(
                        lat=lats, lon=lons,
                        mode="markers",
                        marker=dict(size=8, color=colors, opacity=0.8),
                        text=texts,
                        hoverinfo="text",
                        name="Vessels",
                    ))
                    
                    # Port marker
                    fig.add_trace(go.Scattermap(
                        lat=[custom_lat], lon=[custom_lon],
                        mode="markers+text",
                        marker=dict(size=14, color="#ff6600", symbol="star"),
                        text=[port],
                        textposition="top right",
                        textfont=dict(color="#ff6600", size=11),
                        name="Port",
                        hoverinfo="text",
                    ))
                    
                    fig.update_layout(
                        map=dict(
                            style="dark",
                            center=dict(lat=custom_lat, lon=custom_lon),
                            zoom=5,
                        ),
                        paper_bgcolor="#0a0a0a",
                        plot_bgcolor="#0a0a0a",
                        height=500,
                        margin=dict(l=0, r=0, t=0, b=0),
                        legend=dict(bgcolor="rgba(0,0,0,0.5)", font=dict(color="#888", size=10)),
                        font=dict(family="IBM Plex Mono", color="#888"),
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Legend
                    st.markdown("""
                    <div style="display:flex; gap:16px; font-size:10px; color:#555; margin-top:4px;">
                        <span>🔵 Slow (&lt;5kn)</span>
                        <span style="color:#0099ff;">🔵 Moving (5-15kn)</span>
                        <span style="color:#ff6600;">🟠 Fast (&gt;15kn)</span>
                        <span style="color:#ff6600;">⭐ Port</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No vessel positions returned. AISHub anonymous tier may have limited coverage. Register free at aishub.net for better data.")
            else:
                st.warning("Could not connect to AIS API. Check backend status.")
    
    with tab2:
        section_header("VESSEL DETAILS", "searchable vessel table")
        
        port2 = st.selectbox("Region", list(MAJOR_PORTS.keys()), key="ship_port2")
        lat2, lon2 = MAJOR_PORTS[port2]
        
        if st.button("LOAD VESSELS", key="ship_table_load"):
            with st.spinner("Loading vessel data..."):
                data = api_get(f"{api_url}/api/ships?lat={lat2}&lon={lon2}&radius=300", timeout=20)
            
            if data and data.get("vessels"):
                vessels = data["vessels"]
                
                # Filter controls
                col_type, col_flag = st.columns(2)
                with col_type:
                    min_speed = st.slider("Min Speed (kn)", 0.0, 30.0, 0.0, 0.5)
                
                filtered = [v for v in vessels if (v.get("speed") or 0) >= min_speed]
                
                st.markdown(f"<div style='color:#555; font-size:10px; margin-bottom:8px;'>{len(filtered)} vessels</div>", unsafe_allow_html=True)
                
                html = """
                <div style="background:#0d0d0d; border:1px solid #2a2a2a; border-radius:2px; max-height:500px; overflow-y:auto;">
                <div style="display:grid; grid-template-columns:130px 100px 80px 80px 1fr; gap:4px;
                            padding:5px 8px; background:#1a1a1a; font-size:9px; color:#555; letter-spacing:0.1em; position:sticky; top:0;">
                    <span>NAME</span><span>MMSI</span><span>SPEED</span><span>FLAG</span><span>DESTINATION</span>
                </div>
                """
                
                for v in filtered[:100]:
                    name = (v.get("name") or "Unknown")[:18]
                    mmsi = v.get("mmsi","—")
                    speed = v.get("speed", 0)
                    flag = v.get("flag","—")
                    dest = (v.get("destination") or "—")[:20]
                    spd_color = "#ff6600" if speed > 15 else "#0099ff" if speed > 5 else "#555"
                    
                    html += f"""
                    <div style="display:grid; grid-template-columns:130px 100px 80px 80px 1fr; gap:4px;
                                padding:5px 8px; border-bottom:1px solid #1a1a1a; font-size:10px;"
                         onmouseover="this.style.background='#1a1a1a'" onmouseout="this.style.background='transparent'">
                        <span style="color:#e8e8e8;">{name}</span>
                        <span style="color:#555; font-size:9px;">{mmsi}</span>
                        <span style="color:{spd_color};">{speed:.1f} kn</span>
                        <span style="color:#888;">{flag}</span>
                        <span style="color:#555; font-size:10px;">{dest}</span>
                    </div>
                    """
                
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.warning("No vessel data available for this region.")
