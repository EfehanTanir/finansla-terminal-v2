"""CARGO PLANES PAGE - OpenSky Network (free, no key)"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from frontend.components.shared import *
import plotly.graph_objects as go

MAJOR_AIRPORTS = {
    "Istanbul (IST/SAW)": (41.0, 29.0),
    "Frankfurt (FRA)": (50.0, 8.6),
    "Dubai (DXB)": (25.2, 55.4),
    "London (LHR)": (51.5, -0.1),
    "New York (JFK/EWR)": (40.7, -73.9),
    "Singapore (SIN)": (1.3, 103.9),
    "Hong Kong (HKG)": (22.3, 114.2),
    "Memphis (MEM) - FedEx Hub": (35.0, -90.0),
    "Louisville (SDF) - UPS Hub": (38.2, -85.7),
    "Anchorage (ANC) - Cargo Hub": (61.2, -150.0),
    "Amsterdam (AMS)": (52.3, 4.8),
    "Paris (CDG)": (49.0, 2.5),
}

CARGO_AIRLINES = {
    "FDX": "FedEx", "UPS": "UPS", "DHL": "DHL",
    "GTI": "Atlas Air", "CLX": "Cargolux", "ABX": "ABX Air",
    "FTP": "ASL Airlines", "NPT": "National Air Cargo",
    "TGO": "Turkish Cargo", "MPH": "Martinair",
    "SWG": "Silkway Airlines", "ICE": "Icelandair Cargo",
}

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">✈️ CARGO PLANES</span>
        <span style="color:#555; font-size:10px;">OPENSKY NETWORK · FREE · LIVE ADS-B DATA</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #00cc66; 
                padding:8px 12px; margin-bottom:16px; font-size:10px; color:#888;">
        ✓ Powered by <span style="color:#00cc66;">OpenSky Network</span> — completely free, no API key required.
        Live ADS-B flight data with ~15 second refresh. 
        <a href="https://opensky-network.org" target="_blank" style="color:#ff6600;">opensky-network.org</a>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🗺  LIVE FLIGHT MAP", "📋  FLIGHT TABLE"])
    
    with tab1:
        col_airport, col_radius = st.columns([2, 1])
        with col_airport:
            airport = st.selectbox("Region / Airport", list(MAJOR_AIRPORTS.keys()), key="plane_airport")
        with col_radius:
            radius = st.slider("Radius (°)", 1.0, 10.0, 3.0, 0.5, key="plane_radius")
        
        lat, lon = MAJOR_AIRPORTS[airport]
        
        col_lat, col_lon = st.columns(2)
        with col_lat:
            custom_lat = st.number_input("Lat", value=lat, format="%.4f", key="plane_lat")
        with col_lon:
            custom_lon = st.number_input("Lon", value=lon, format="%.4f", key="plane_lon")
        
        cargo_only = st.checkbox("Show known cargo airlines only", value=False, key="plane_cargo_only")
        
        if st.button("🔍 SEARCH FLIGHTS", key="plane_search"):
            with st.spinner(f"Fetching flights near {airport}..."):
                data = api_get(f"{api_url}/api/planes?lat={custom_lat}&lon={custom_lon}&radius={radius}", timeout=20)
            
            if data:
                planes = data.get("planes", [])
                
                if cargo_only:
                    planes = [p for p in planes if any(
                        p.get("callsign","").startswith(code) for code in CARGO_AIRLINES.keys()
                    )]
                
                # Filter airborne only
                airborne = [p for p in planes if not p.get("on_ground", True) and p.get("lat") and p.get("lon")]
                grounded = [p for p in planes if p.get("on_ground", False) and p.get("lat") and p.get("lon")]
                
                st.markdown(f"<div style='color:#00cc66; font-size:11px; margin-bottom:8px;'>✓ {len(airborne)} airborne · {len(grounded)} on ground</div>", unsafe_allow_html=True)
                
                if airborne or grounded:
                    fig = go.Figure()
                    
                    # Airborne planes
                    if airborne:
                        lats = [p["lat"] for p in airborne]
                        lons = [p["lon"] for p in airborne]
                        texts = [
                            f"<b>{p.get('callsign','?')}</b><br>"
                            f"Country: {p.get('origin_country','?')}<br>"
                            f"Alt: {p.get('altitude',0):.0f}m<br>"
                            f"Speed: {p.get('velocity',0):.0f} m/s<br>"
                            f"Heading: {p.get('heading',0):.0f}°"
                            for p in airborne
                        ]
                        
                        # Color by altitude
                        altitudes = [p.get("altitude", 0) or 0 for p in airborne]
                        max_alt = max(altitudes) if altitudes else 12000
                        
                        fig.add_trace(go.Scattermap(
                            lat=lats, lon=lons,
                            mode="markers",
                            marker=dict(
                                size=8,
                                color=altitudes,
                                colorscale=[[0,"#0099ff"],[0.5,"#ff6600"],[1,"#ffffff"]],
                                cmin=0, cmax=max_alt,
                                opacity=0.85,
                                colorbar=dict(
                                    title="Alt (m)",
                                    thickness=10,
                                    len=0.5,
                                    tickfont=dict(color="#555", size=9),
                                    titlefont=dict(color="#555", size=9),
                                ),
                            ),
                            text=texts,
                            hoverinfo="text",
                            name="Airborne",
                        ))
                    
                    # Grounded planes
                    if grounded:
                        fig.add_trace(go.Scattermap(
                            lat=[p["lat"] for p in grounded],
                            lon=[p["lon"] for p in grounded],
                            mode="markers",
                            marker=dict(size=5, color="#333", opacity=0.6),
                            text=[p.get("callsign","?") for p in grounded],
                            hoverinfo="text",
                            name="On Ground",
                        ))
                    
                    # Airport marker
                    fig.add_trace(go.Scattermap(
                        lat=[custom_lat], lon=[custom_lon],
                        mode="markers+text",
                        marker=dict(size=15, color="#ff6600", symbol="airport"),
                        text=[airport.split("(")[0]],
                        textposition="top right",
                        textfont=dict(color="#ff6600", size=11),
                        name="Airport",
                    ))
                    
                    fig.update_layout(
                        map=dict(
                            style="dark",
                            center=dict(lat=custom_lat, lon=custom_lon),
                            zoom=6,
                        ),
                        paper_bgcolor="#0a0a0a",
                        height=500,
                        margin=dict(l=0, r=0, t=0, b=0),
                        legend=dict(bgcolor="rgba(0,0,0,0.5)", font=dict(color="#888", size=10)),
                        font=dict(family="IBM Plex Mono", color="#888"),
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""
                    <div style="display:flex; gap:16px; font-size:10px; color:#555; margin-top:4px;">
                        <span style="color:#0099ff;">🔵 Low altitude</span>
                        <span style="color:#ff6600;">🟠 Mid altitude</span>
                        <span>⚪ High altitude</span>
                        <span style="color:#ff6600;">✈ Airport</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No flights found in this area. Try increasing the radius or choosing a busier region.")
            else:
                st.warning("Could not connect to OpenSky API. It may be temporarily unavailable.")
    
    with tab2:
        section_header("FLIGHT TABLE", "detailed flight information")
        
        airport2 = st.selectbox("Region", list(MAJOR_AIRPORTS.keys()), key="plane_airport2")
        lat2, lon2 = MAJOR_AIRPORTS[airport2]
        
        if st.button("LOAD FLIGHTS", key="plane_table_load"):
            with st.spinner("Loading flight data..."):
                data = api_get(f"{api_url}/api/planes?lat={lat2}&lon={lon2}&radius=4", timeout=20)
            
            if data and data.get("planes"):
                planes = data["planes"]
                airborne = [p for p in planes if not p.get("on_ground")]
                
                st.markdown(f"<div style='color:#555; font-size:10px; margin-bottom:8px;'>{len(airborne)} airborne flights</div>", unsafe_allow_html=True)
                
                html = """
                <div style="background:#0d0d0d; border:1px solid #2a2a2a; border-radius:2px; max-height:500px; overflow-y:auto;">
                <div style="display:grid; grid-template-columns:100px 100px 80px 80px 80px 80px; gap:4px;
                            padding:5px 8px; background:#1a1a1a; font-size:9px; color:#555; letter-spacing:0.1em; position:sticky; top:0;">
                    <span>CALLSIGN</span><span>COUNTRY</span><span>ALT (m)</span>
                    <span>SPEED m/s</span><span>HEADING</span><span>SQUAWK</span>
                </div>
                """
                
                for p in sorted(airborne, key=lambda x: x.get("altitude",0), reverse=True)[:100]:
                    cs = p.get("callsign","—").strip()
                    country = p.get("origin_country","—")[:12]
                    alt = p.get("altitude", 0) or 0
                    speed = p.get("velocity", 0) or 0
                    hdg = p.get("heading", 0) or 0
                    squawk = p.get("squawk","—")
                    
                    is_cargo = any(cs.startswith(code) for code in CARGO_AIRLINES.keys())
                    cs_color = "#ff6600" if is_cargo else "#e8e8e8"
                    cargo_label = f" ({CARGO_AIRLINES.get(cs[:3],'Cargo')})" if is_cargo else ""
                    
                    html += f"""
                    <div style="display:grid; grid-template-columns:100px 100px 80px 80px 80px 80px; gap:4px;
                                padding:5px 8px; border-bottom:1px solid #1a1a1a; font-size:10px;"
                         onmouseover="this.style.background='#1a1a1a'" onmouseout="this.style.background='transparent'">
                        <span style="color:{cs_color}; font-weight:{'700' if is_cargo else '400'};">{cs or '—'}{cargo_label}</span>
                        <span style="color:#888; font-size:9px;">{country}</span>
                        <span style="color:#0099ff;">{alt:.0f}</span>
                        <span style="color:#888;">{speed:.0f}</span>
                        <span style="color:#555;">{hdg:.0f}°</span>
                        <span style="color:#444; font-size:9px;">{squawk}</span>
                    </div>
                    """
                
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
                
                # Known cargo airline summary
                cargo_flights = [p for p in airborne if any(
                    (p.get("callsign","") or "").startswith(code) for code in CARGO_AIRLINES.keys()
                )]
                if cargo_flights:
                    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                    section_header("IDENTIFIED CARGO FLIGHTS", f"{len(cargo_flights)} found")
                    for p in cargo_flights:
                        cs = p.get("callsign","").strip()
                        airline = next((name for code, name in CARGO_AIRLINES.items() if cs.startswith(code)), "Cargo")
                        st.markdown(f"<span style='color:#ff6600;'>{cs}</span> <span style='color:#888;'>{airline}</span> — Alt: {p.get('altitude',0):.0f}m · Speed: {p.get('velocity',0):.0f} m/s", unsafe_allow_html=True)
            else:
                st.warning("No flight data available.")