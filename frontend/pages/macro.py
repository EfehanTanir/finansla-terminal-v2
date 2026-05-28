"""MACRO & FX PAGE"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from frontend.components.shared import *
import plotly.graph_objects as go

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">🌍 MACRO & FX</span>
        <span style="color:#555; font-size:10px;">CURRENCIES · COMMODITIES · CRYPTO · BONDS</span>
    </div>
    """, unsafe_allow_html=True)
    
    macro = api_get(f"{api_url}/api/macro") or {}
    
    if macro:
        # FX Section
        section_header("FOREX", "major currency pairs")
        fx_keys = ["EUR_USD","GBP_USD","USD_JPY","USD_TRY","USD_CHF"]
        fx_data = {k: macro[k] for k in fx_keys if k in macro}
        
        cols = st.columns(len(fx_data))
        for i, (name, data) in enumerate(fx_data.items()):
            with cols[i]:
                chg = data["change_pct"]
                price = data["price"]
                st.metric(
                    name.replace("_","/"),
                    f"{price:.4f}",
                    f"{chg:+.2f}%"
                )
        
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        
        # Commodities
        section_header("COMMODITIES", "energy · metals")
        comm_keys = ["GOLD","SILVER","OIL_WTI","OIL_BRENT","NATGAS","COPPER"]
        comm_data = {k: macro[k] for k in comm_keys if k in macro}
        
        cols2 = st.columns(len(comm_data))
        for i, (name, data) in enumerate(comm_data.items()):
            with cols2[i]:
                chg = data["change_pct"]
                price = data["price"]
                st.metric(
                    name.replace("_"," "),
                    f"${price:,.2f}",
                    f"{chg:+.2f}%"
                )
        
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        
        # Crypto
        section_header("CRYPTO", "digital assets")
        crypto_keys = ["BTC","ETH"]
        crypto_data = {k: macro[k] for k in crypto_keys if k in macro}
        
        cols3 = st.columns(4)
        for i, (name, data) in enumerate(crypto_data.items()):
            with cols3[i]:
                st.metric(name, f"${data['price']:,.0f}", f"{data['change_pct']:+.2f}%")
        
        # USD + Bonds
        others = {k: macro[k] for k in ["USD_INDEX","US10Y"] if k in macro}
        for i, (name, data) in enumerate(others.items()):
            with cols3[i+2]:
                st.metric(name.replace("_"," "), f"{data['price']:.4f}", f"{data['change_pct']:+.2f}%")
    
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    
    # Chart section
    section_header("MACRO CHART", "historical price data")
    
    MACRO_SYMBOLS = {
        "EUR/USD": "EURUSD=X",
        "USD/TRY": "USDTRY=X",
        "GBP/USD": "GBPUSD=X",
        "Gold": "GC=F",
        "WTI Oil": "CL=F",
        "Bitcoin": "BTC-USD",
        "US 10Y": "^TNX",
        "USD Index": "DX-Y.NYB",
        "S&P 500": "^GSPC",
        "VIX": "^VIX",
    }
    
    col_sel, col_per = st.columns([2, 1])
    with col_sel:
        selected = st.selectbox("Select Instrument", list(MACRO_SYMBOLS.keys()), key="macro_sel")
    with col_per:
        period = st.selectbox("Period", ["1mo","3mo","6mo","1y","2y","5y"], index=3, key="macro_per")
    
    if st.button("LOAD CHART", key="macro_load"):
        sym = MACRO_SYMBOLS[selected]
        with st.spinner(f"Loading {selected}..."):
            data = api_get(f"{api_url}/api/stock/{sym}?period={period}")
        
        if data and data.get("ohlcv"):
            curr = data["current_price"]
            chg = data.get("change_pct", 0)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("CURRENT", f"{curr:,.4f}" if curr < 100 else f"{curr:,.2f}")
            c2.metric("CHANGE", fmt_pct(chg))
            c3.metric("PERIOD", period)
            
            fig = make_line_chart(data["ohlcv"], "date", "close", f"{selected} — {period}", 400, "#0099ff")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"Could not load data for {selected}")
    
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    
    # Macro matrix
    section_header("MACRO MATRIX", "all indicators at a glance")
    if macro:
        rows = []
        for name, data in macro.items():
            rows.append({
                "Indicator": name.replace("_","/"),
                "Price": f"{data['price']:,.4f}" if data['price'] < 100 else f"{data['price']:,.2f}",
                "Change %": f"{data['change_pct']:+.2f}%",
                "Signal": "🟢 UP" if data['change_pct'] > 0 else "🔴 DOWN",
            })
        
        html = """
        <div style="background:#0d0d0d; border:1px solid #2a2a2a; border-radius:2px; overflow:hidden;">
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:0;
                    padding:5px 8px; background:#1a1a1a; font-size:9px; color:#555; letter-spacing:0.1em;">
            <span>INDICATOR</span><span style="text-align:right">PRICE</span>
            <span style="text-align:right">CHANGE</span><span style="text-align:right">SIGNAL</span>
        </div>
        """
        for row in rows:
            color = "#00cc66" if "UP" in row["Signal"] else "#ff3333"
            html += f"""
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:0;
                        padding:5px 8px; border-bottom:1px solid #1a1a1a; font-size:11px;"
                 onmouseover="this.style.background='#1a1a1a'" onmouseout="this.style.background='transparent'">
                <span style="color:#e8e8e8;">{row['Indicator']}</span>
                <span style="color:#888; text-align:right;">{row['Price']}</span>
                <span style="color:{color}; text-align:right;">{row['Change %']}</span>
                <span style="color:{color}; text-align:right; font-size:10px;">{row['Signal']}</span>
            </div>
            """
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)