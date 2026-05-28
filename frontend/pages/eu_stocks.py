"""EU STOCKS PAGE"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.shared import *

EU_INFO = {
    "ASML.AS": ("ASML Holding","Semiconductors","Netherlands"),
    "SAP.DE": ("SAP SE","Software","Germany"),
    "LVMH.PA": ("LVMH","Luxury","France"),
    "TTE.PA": ("TotalEnergies","Energy","France"),
    "SIE.DE": ("Siemens","Industrial","Germany"),
    "AIR.PA": ("Airbus","Aerospace","France"),
    "MC.PA": ("LVMH Moët Hennessy","Luxury","France"),
    "OR.PA": ("L'Oréal","Consumer","France"),
    "SAN.MC": ("Banco Santander","Banking","Spain"),
    "IBE.MC": ("Iberdrola","Utilities","Spain"),
    "ENEL.MI": ("Enel","Utilities","Italy"),
    "ENI.MI": ("Eni","Energy","Italy"),
    "BAS.DE": ("BASF","Chemicals","Germany"),
    "BMW.DE": ("BMW Group","Auto","Germany"),
    "VOW3.DE": ("Volkswagen","Auto","Germany"),
    "ADS.DE": ("Adidas","Consumer","Germany"),
    "DTE.DE": ("Deutsche Telekom","Telecom","Germany"),
    "BAYN.DE": ("Bayer","Pharma","Germany"),
}

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">🇪🇺 EU MARKETS</span>
        <span style="color:#555; font-size:10px;">EURONEXT · XETRA · BME · BORSA ITALIANA</span>
    </div>
    """, unsafe_allow_html=True)
    
    indices = api_get(f"{api_url}/api/indices") or {}
    col1, col2, col3, col4 = st.columns(4)
    for name, col in [("DAX",col1),("CAC40",col2),("EUROSTOXX",col3),("FTSE100",col4)]:
        if name in indices:
            d = indices[name]
            with col:
                st.metric(name, f"{d['price']:,.2f}", f"{d['change_pct']:+.2f}%")
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊  MARKET BOARD", "📈  CHART"])
    
    with tab1:
        section_header("EU EQUITIES", "blue chips across exchanges")
        
        eu_data = api_get(f"{api_url}/api/market/EU") or []
        
        if eu_data:
            sort_col, dir_col = st.columns([2, 1])
            with sort_col:
                sort_by = st.selectbox("Sort", ["Change %", "Price", "Symbol"], key="eu_sort")
            with dir_col:
                direction = st.selectbox("Order", ["Descending", "Ascending"], key="eu_dir")
            
            key_map = {"Change %": "change_pct", "Price": "price", "Symbol": "symbol"}
            eu_data.sort(key=lambda x: x.get(key_map[sort_by], 0) or 0, reverse=(direction == "Descending"))
            
            # Group by exchange
            exchanges = {"Paris (.PA)": ".PA", "Frankfurt (.DE)": ".DE", "Amsterdam (.AS)": ".AS", "Madrid (.MC)": ".MC", "Milan (.MI)": ".MI"}
            
            for exch_name, ext in exchanges.items():
                exch_stocks = [s for s in eu_data if ext in s["symbol"]]
                if exch_stocks:
                    st.markdown(f"<div style='color:#ff6600; font-size:10px; letter-spacing:0.1em; margin:12px 0 4px;'>{exch_name}</div>", unsafe_allow_html=True)
                    html = "<div style='background:#0d0d0d; border:1px solid #2a2a2a; border-radius:2px;'>"
                    for s in exch_stocks:
                        info = EU_INFO.get(s["symbol"], ("", "", ""))
                        name_str = info[0] if info[0] else s["symbol"]
                        clean_sym = s["symbol"].replace(ext, "")
                        html += stock_row_html(clean_sym, s["price"], s["change_pct"], s.get("volume"), name_str[:20])
                    html += "</div>"
                    st.markdown(html, unsafe_allow_html=True)
        else:
            st.warning("Could not load EU data")
    
    with tab2:
        section_header("EU STOCK CHART", "price history")
        
        col_sym, col_per = st.columns([2, 1])
        with col_sym:
            sym = st.text_input("Symbol (e.g. ASML.AS, SAP.DE, LVMH.PA)", value="ASML.AS", key="eu_sym")
        with col_per:
            period = st.selectbox("Period", ["1mo","3mo","6mo","1y","2y","5y"], index=3, key="eu_per")
        
        if st.button("LOAD CHART", key="eu_load"):
            with st.spinner(f"Loading {sym.upper()}..."):
                data = api_get(f"{api_url}/api/stock/{sym.upper()}?period={period}")
            
            if data and data.get("ohlcv"):
                curr = data["current_price"]
                chg = data.get("change_pct", 0)
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("PRICE", f"{curr:,.2f} {data.get('currency','EUR')}")
                c2.metric("CHANGE", fmt_pct(chg))
                c3.metric("MKT CAP", fmt_mcap(data.get("market_cap")))
                c4.metric("P/E", f"{data.get('pe_ratio'):.1f}" if data.get("pe_ratio") else "—")
                
                fig = make_candlestick(data["ohlcv"], f"{sym.upper()} — {data.get('name','')}", 450)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                if data.get("description"):
                    with st.expander("Company Description"):
                        st.write(data["description"])
            else:
                st.error(f"No data found for {sym.upper()}")
