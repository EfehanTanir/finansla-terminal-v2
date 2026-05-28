"""BIST STOCKS PAGE"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.shared import *
import pandas as pd

BIST_NOTABLE = [
    ("THYAO","Türk Hava Yolları","Aviation"),("GARAN","Garanti BBVA","Banking"),
    ("AKBNK","Akbank","Banking"),("EREGL","Ereğli Demir","Steel"),
    ("SASA","Sasa Polyester","Chemicals"),("KCHOL","Koç Holding","Conglomerate"),
    ("BIMAS","BİM Birleşik","Retail"),("ASELS","Aselsan","Defense"),
    ("FROTO","Ford Otosan","Auto"),("TOASO","Tofaş","Auto"),
    ("TUPRS","Tüpraş","Energy"),("YKBNK","Yapı Kredi","Banking"),
    ("TCELL","Turkcell","Telecom"),("PGSUS","Pegasus","Aviation"),
    ("KRDMD","Kardemir","Steel"),("KOZAL","Koza Altın","Mining"),
]

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">🇹🇷 BIST MARKET</span>
        <span style="color:#555; font-size:10px;">BORSA İSTANBUL · REAL-TIME</span>
    </div>
    """, unsafe_allow_html=True)
    
    # BIST100 + BIST30 header
    col1, col2, col3, col4 = st.columns(4)
    for sym, label, col in [("XU100.IS","BIST 100",col1),("XU030.IS","BIST 30",col2),("USDTRY=X","USD/TRY",col3),("EURTRY=X","EUR/TRY",col4)]:
        data = api_get(f"{api_url}/api/stock/{sym}?period=2d")
        if data and data.get("ohlcv") and len(data["ohlcv"]) >= 2:
            curr = data["ohlcv"][-1]["close"]
            prev = data["ohlcv"][-2]["close"]
            chg = ((curr - prev) / prev) * 100
            with col:
                st.metric(label, f"{curr:,.2f}", f"{chg:+.2f}%")
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊  MARKET BOARD", "📈  CHART", "ℹ  COMPANY INFO"])
    
    with tab1:
        section_header("BIST STOCKS", "all tracked equities")
        
        bist_data = api_get(f"{api_url}/api/market/BIST") or []
        
        if bist_data:
            col_sort = st.columns([2, 1])
            with col_sort[0]:
                sort_by = st.selectbox("Sort by", ["Change %", "Price", "Volume", "Symbol"], key="bist_sort")
            with col_sort[1]:
                direction = st.selectbox("Order", ["Descending", "Ascending"], key="bist_dir")
            
            key_map = {"Change %": "change_pct", "Price": "price", "Volume": "volume", "Symbol": "symbol"}
            bist_data.sort(
                key=lambda x: x.get(key_map[sort_by], 0) or 0,
                reverse=(direction == "Descending")
            )
            
            # Table header
            st.markdown("""
            <div style="display:flex; justify-content:space-between; padding:5px 8px; 
                        background:#1a1a1a; font-size:9px; color:#555; letter-spacing:0.1em;
                        border-bottom:1px solid #2a2a2a;">
                <span style="min-width:90px;">SYMBOL</span>
                <span>PRICE</span>
                <span style="min-width:70px; text-align:right;">CHANGE</span>
                <span>VOLUME</span>
                <span>PREV CLOSE</span>
            </div>
            """, unsafe_allow_html=True)
            
            html = "<div style='background:#0d0d0d; border:1px solid #2a2a2a; border-top:none; max-height:600px; overflow-y:auto;'>"
            for s in bist_data:
                sym_clean = s["symbol"].replace(".IS", "")
                html += stock_row_html(sym_clean, s["price"], s["change_pct"], s.get("volume"), 
                                        f"prev: {s.get('prev_close', 0):,.2f}")
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
            
            # Summary stats
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            gainers = sum(1 for s in bist_data if s["change_pct"] > 0)
            losers = sum(1 for s in bist_data if s["change_pct"] < 0)
            flat = len(bist_data) - gainers - losers
            
            c1, c2, c3 = st.columns(3)
            c1.metric("📈 GAINERS", gainers)
            c2.metric("📉 LOSERS", losers)
            c3.metric("➡ FLAT", flat)
        else:
            st.warning("Could not load BIST data")
    
    with tab2:
        section_header("BIST STOCK CHART", "interactive price history")
        
        col_sym, col_period = st.columns([2, 1])
        with col_sym:
            symbol_input = st.text_input("Stock Symbol (e.g. THYAO, GARAN, ASELS)", value="THYAO", key="bist_sym")
        with col_period:
            period = st.selectbox("Period", ["1mo","3mo","6mo","1y","2y","5y"], index=3, key="bist_period")
        
        symbol = symbol_input.upper().replace(".IS", "") + ".IS"
        
        if st.button("LOAD CHART", key="bist_load"):
            with st.spinner(f"Loading {symbol}..."):
                data = api_get(f"{api_url}/api/stock/{symbol}?period={period}")
            
            if data and data.get("ohlcv"):
                curr = data["current_price"]
                chg = data.get("change_pct", 0)
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("PRICE", fmt_price(curr))
                c2.metric("CHANGE", fmt_pct(chg))
                c3.metric("52W HIGH", fmt_price(data.get("52w_high")))
                c4.metric("52W LOW", fmt_price(data.get("52w_low")))
                
                fig = make_candlestick(data["ohlcv"], f"{symbol.replace('.IS','')} — {data.get('name','')}", 450)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"No data found for {symbol}")
    
    with tab3:
        section_header("COMPANY INFO", "fundamentals & description")
        
        selected = st.selectbox("Select Company", [f"{code} – {name}" for code, name, sector in BIST_NOTABLE], key="bist_info_sel")
        code = selected.split("–")[0].strip()
        full_sym = f"{code}.IS"
        
        if st.button("LOAD INFO", key="bist_info_load"):
            with st.spinner(f"Loading {full_sym}..."):
                data = api_get(f"{api_url}/api/stock/{full_sym}?period=1y")
            
            if data:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                    <div class='fin-card'>
                        <div class='fin-header'>COMPANY</div>
                        <div style="font-size:14px; color:#e8e8e8; margin-bottom:4px;">{data.get('name', code)}</div>
                        <div style="font-size:10px; color:#888;">{data.get('sector','N/A')} · {data.get('industry','N/A')}</div>
                        <div style="font-size:10px; color:#555; margin-top:4px;">{data.get('exchange','')} · {data.get('currency','TRY')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"""
                    <div class='fin-card'>
                        <div class='fin-header'>FUNDAMENTALS</div>
                        <div style="font-size:11px; line-height:2;">
                        <span style="color:#888;">Market Cap:</span> <span style="color:#e8e8e8;">{fmt_mcap(data.get('market_cap'))}</span><br>
                        <span style="color:#888;">P/E Ratio:</span> <span style="color:#e8e8e8;">{data.get('pe_ratio','N/A')}</span><br>
                        <span style="color:#888;">EPS:</span> <span style="color:#e8e8e8;">{data.get('eps','N/A')}</span><br>
                        <span style="color:#888;">Beta:</span> <span style="color:#e8e8e8;">{data.get('beta','N/A')}</span><br>
                        <span style="color:#888;">Div Yield:</span> <span style="color:#e8e8e8;">{(data.get('dividend_yield') or 0)*100:.2f}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if data.get("description"):
                    st.markdown(f"""
                    <div style="background:#111; border:1px solid #2a2a2a; padding:12px; margin-top:8px; 
                                font-size:10px; color:#888; line-height:1.6; border-radius:2px;">
                        {data['description']}
                    </div>
                    """, unsafe_allow_html=True)
                
                if data.get("ohlcv"):
                    fig = make_line_chart(data["ohlcv"], "date", "close", f"{code} — 1Y PRICE", 280)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
