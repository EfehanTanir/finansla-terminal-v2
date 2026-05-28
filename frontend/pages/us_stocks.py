"""US STOCKS PAGE"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.shared import *

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">🇺🇸 US MARKETS</span>
        <span style="color:#555; font-size:10px;">NYSE · NASDAQ · REAL-TIME DATA</span>
    </div>
    """, unsafe_allow_html=True)
    
    # US index header
    indices = api_get(f"{api_url}/api/indices") or {}
    col1, col2, col3, col4 = st.columns(4)
    for name, sym, col in [("S&P 500","SPX",col1),("NASDAQ","NASDAQ",col2),("DOW","DOW",col3),("VIX","VIX",col4)]:
        if name in indices:
            d = indices[name]
            with col:
                st.metric(name, f"{d['price']:,.2f}", f"{d['change_pct']:+.2f}%")
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊  MARKET BOARD", "📈  CHART & ANALYSIS", "🔍  SCREENER"])
    
    with tab1:
        section_header("US EQUITIES", "top 30 by market cap")
        
        us_data = api_get(f"{api_url}/api/market/US") or []
        
        if us_data:
            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                sort_by = st.selectbox("Sort by", ["Change %", "Price", "Volume", "Symbol"], key="us_sort")
            with col_f2:
                direction = st.selectbox("Order", ["Descending", "Ascending"], key="us_dir")
            
            key_map = {"Change %": "change_pct", "Price": "price", "Volume": "volume", "Symbol": "symbol"}
            us_data.sort(key=lambda x: x.get(key_map[sort_by], 0) or 0, reverse=(direction == "Descending"))
            
            col_l, col_r = st.columns(2)
            mid = len(us_data) // 2
            
            for col, items in [(col_l, us_data[:mid]), (col_r, us_data[mid:])]:
                with col:
                    html = "<div style='background:#0d0d0d; border:1px solid #2a2a2a; border-radius:2px;'>"
                    for s in items:
                        html += stock_row_html(s["symbol"], s["price"], s["change_pct"], s.get("volume"))
                    html += "</div>"
                    st.markdown(html, unsafe_allow_html=True)
            
            gainers = sum(1 for s in us_data if s["change_pct"] > 0)
            losers = sum(1 for s in us_data if s["change_pct"] < 0)
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("📈 GAINERS", gainers)
            c2.metric("📉 LOSERS", losers)
            c3.metric("TOTAL", len(us_data))
    
    with tab2:
        section_header("US STOCK CHART", "candlestick & volume")
        
        col_sym, col_per = st.columns([2, 1])
        with col_sym:
            sym = st.text_input("Symbol (e.g. AAPL, NVDA, TSLA)", value="AAPL", key="us_sym")
        with col_per:
            period = st.selectbox("Period", ["1mo","3mo","6mo","1y","2y","5y"], index=3, key="us_per")
        
        if st.button("LOAD CHART", key="us_load"):
            with st.spinner(f"Loading {sym.upper()}..."):
                data = api_get(f"{api_url}/api/stock/{sym.upper()}?period={period}")
            
            if data and data.get("ohlcv"):
                curr = data["current_price"]
                chg = data.get("change_pct", 0)
                mcap = data.get("market_cap", 0)
                pe = data.get("pe_ratio")
                
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("PRICE", f"${curr:,.2f}")
                c2.metric("CHANGE", fmt_pct(chg))
                c3.metric("MKT CAP", fmt_mcap(mcap))
                c4.metric("P/E", f"{pe:.1f}" if pe else "—")
                c5.metric("BETA", f"{data.get('beta', 0):.2f}" if data.get("beta") else "—")
                
                fig = make_candlestick(data["ohlcv"], f"{sym.upper()} — {data.get('name','')}", 450)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # News for this stock
                news = api_get(f"{api_url}/api/news/stock/{sym.upper()}") or []
                if news:
                    section_header(f"{sym.upper()} NEWS", "latest headlines")
                    for item in news[:6]:
                        st.markdown(f"""
                        <div style="padding:6px 0; border-bottom:1px solid #1a1a1a; font-size:11px;">
                            <a href="{item.get('link','#')}" target="_blank" style="color:#e8e8e8; text-decoration:none;">
                                {item.get('title','')[:110]}
                            </a>
                            <div style="color:#555; font-size:9px; margin-top:2px;">
                                {item.get('publisher','')} · {item.get('published','')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error(f"No data for {sym.upper()}")
    
    with tab3:
        section_header("QUICK SCREENER", "filter US stocks")
        
        us_data_screen = api_get(f"{api_url}/api/market/US") or []
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            min_chg = st.slider("Min Change %", -20.0, 0.0, -20.0, 0.5, key="us_min_chg")
        with col_f2:
            max_chg = st.slider("Max Change %", 0.0, 20.0, 20.0, 0.5, key="us_max_chg")
        
        filtered = [s for s in us_data_screen if min_chg <= s["change_pct"] <= max_chg]
        
        if filtered:
            html = "<div style='background:#0d0d0d; border:1px solid #2a2a2a; border-radius:2px;'>"
            for s in sorted(filtered, key=lambda x: x["change_pct"], reverse=True):
                html += stock_row_html(s["symbol"], s["price"], s["change_pct"], s.get("volume"))
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
            st.caption(f"{len(filtered)} stocks match filter")
        else:
            st.info("No stocks match the filter criteria")
