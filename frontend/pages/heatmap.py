"""HEATMAP PAGE"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from frontend.components.shared import *
import plotly.graph_objects as go
import math

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">🔥 MARKET HEATMAP</span>
        <span style="color:#555; font-size:10px;">VISUAL PERFORMANCE GRID · DAY CHANGE</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_mkt, col_mode = st.columns([2, 1])
    with col_mkt:
        market = st.selectbox("Market", ["US", "BIST", "EU"], key="heatmap_market")
    with col_mode:
        view_mode = st.selectbox("View", ["Treemap", "Grid"], key="heatmap_mode")
    
    if st.button("GENERATE HEATMAP", key="heatmap_gen"):
        with st.spinner(f"Loading {market} heatmap..."):
            data = api_get(f"{api_url}/api/heatmap/{market}") or []
        
        if data:
            # Color scale: deep red → neutral gray → deep green
            def pct_to_color(pct: float) -> str:
                pct = max(-10, min(10, pct))
                if pct > 0:
                    intensity = min(pct / 5, 1.0)
                    g = int(180 * intensity + 50)
                    r = int(30 * (1 - intensity))
                    return f"rgb({r},{g},50)"
                elif pct < 0:
                    intensity = min(abs(pct) / 5, 1.0)
                    r = int(200 * intensity + 50)
                    g = int(30 * (1 - intensity))
                    return f"rgb({r},{g},30)"
                return "rgb(80,80,80)"
            
            if view_mode == "Treemap":
                symbols = [d["symbol"] for d in data]
                pcts = [d["change_pct"] for d in data]
                parents = [""] * len(symbols)
                values = [max(abs(p) * 10 + 5, 5) for p in pcts]
                colors = [pct_to_color(p) for p in pcts]
                labels = [f"{s}<br>{'+' if p>=0 else ''}{p:.2f}%" for s, p in zip(symbols, pcts)]
                
                fig = go.Figure(go.Treemap(
                    labels=symbols,
                    parents=parents,
                    values=values,
                    text=labels,
                    textinfo="text",
                    marker=dict(
                        colors=colors,
                        line=dict(color="#0a0a0a", width=2),
                    ),
                    hovertemplate="<b>%{label}</b><br>Change: %{text}<extra></extra>",
                    textfont=dict(family="IBM Plex Mono", size=12, color="white"),
                ))
                
                fig.update_layout(
                    paper_bgcolor="#0a0a0a",
                    height=550,
                    margin=dict(l=0, r=0, t=0, b=0),
                    font=dict(family="IBM Plex Mono", color="#888"),
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            else:  # Grid view
                data_sorted = sorted(data, key=lambda x: x["change_pct"], reverse=True)
                
                cols_per_row = 5
                rows = math.ceil(len(data_sorted) / cols_per_row)
                
                for row_i in range(rows):
                    cols = st.columns(cols_per_row)
                    for col_i in range(cols_per_row):
                        idx = row_i * cols_per_row + col_i
                        if idx < len(data_sorted):
                            item = data_sorted[idx]
                            pct = item["change_pct"]
                            sym = item["symbol"]
                            
                            if pct > 3:
                                bg, text_c = "#003d1f", "#00cc66"
                            elif pct > 1:
                                bg, text_c = "#002a15", "#00aa55"
                            elif pct > 0:
                                bg, text_c = "#001a0d", "#007733"
                            elif pct < -3:
                                bg, text_c = "#3d0000", "#ff3333"
                            elif pct < -1:
                                bg, text_c = "#2a0000", "#cc2222"
                            elif pct < 0:
                                bg, text_c = "#1a0000", "#993333"
                            else:
                                bg, text_c = "#1a1a1a", "#888888"
                            
                            with cols[col_i]:
                                st.markdown(f"""
                                <div style="background:{bg}; border:1px solid #2a2a2a; border-radius:2px;
                                            padding:10px 8px; text-align:center; margin-bottom:4px;">
                                    <div style="color:#e8e8e8; font-size:11px; font-weight:700;">{sym}</div>
                                    <div style="color:{text_c}; font-size:13px; font-weight:700; margin-top:2px;">
                                        {'+' if pct>=0 else ''}{pct:.2f}%
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
            
            # Stats bar
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            gainers = [d for d in data if d["change_pct"] > 0]
            losers = [d for d in data if d["change_pct"] < 0]
            
            col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
            col_s1.metric("📈 GAINERS", len(gainers))
            col_s2.metric("📉 LOSERS", len(losers))
            col_s3.metric("TOTAL", len(data))
            if gainers:
                best = max(gainers, key=lambda x: x["change_pct"])
                col_s4.metric("BEST", f"{best['symbol']} +{best['change_pct']:.2f}%")
            if losers:
                worst = min(losers, key=lambda x: x["change_pct"])
                col_s5.metric("WORST", f"{worst['symbol']} {worst['change_pct']:.2f}%")
        else:
            st.warning(f"Could not load {market} heatmap data")
    else:
        st.markdown("""
        <div style="text-align:center; padding:80px 0; color:#333; font-size:13px;">
            <div style="font-size:32px; margin-bottom:16px;">🔥</div>
            Select a market and click GENERATE HEATMAP
        </div>
        """, unsafe_allow_html=True)