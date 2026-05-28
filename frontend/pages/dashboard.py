"""DASHBOARD - Main overview page"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.shared import *

def render(api_url: str):
    # Ticker tape
    with st.spinner(""):
        indices = api_get(f"{api_url}/api/indices") or {}
    
    if indices:
        st.markdown(ticker_html(indices), unsafe_allow_html=True)
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div>
            <span style="color:#ff6600; font-size:18px; font-weight:700; letter-spacing:0.05em;">MARKET OVERVIEW</span>
            <span style="color:#555; font-size:10px; margin-left:12px;">REAL-TIME DATA VIA YFINANCE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Index tiles
    section_header("GLOBAL INDICES", "live")
    
    if indices:
        cols = st.columns(4)
        idx_items = list(indices.items())
        for i, (name, data) in enumerate(idx_items[:8]):
            with cols[i % 4]:
                chg = data.get("change_pct", 0)
                price = data.get("price", 0)
                st.metric(
                    label=name,
                    value=f"{price:,.2f}" if price < 10000 else f"{price:,.0f}",
                    delta=f"{chg:+.2f}%",
                )
        
        st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)
        cols2 = st.columns(4)
        for i, (name, data) in enumerate(idx_items[8:16]):
            with cols2[i % 4]:
                chg = data.get("change_pct", 0)
                price = data.get("price", 0)
                st.metric(
                    label=name,
                    value=f"{price:,.4f}" if price < 100 else f"{price:,.2f}",
                    delta=f"{chg:+.2f}%",
                )
    else:
        st.warning("⚠ Could not load index data. Backend may be starting...")
    
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    
    # Market movers + News side by side
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        section_header("TOP MOVERS — BIST", "today")
        bist_data = api_get(f"{api_url}/api/market/BIST") or []
        if bist_data:
            gainers = sorted(bist_data, key=lambda x: x["change_pct"], reverse=True)[:8]
            st.markdown("<div style='background:#111; border:1px solid #2a2a2a; border-radius:2px;'>", unsafe_allow_html=True)
            html = ""
            for s in gainers:
                html += stock_row_html(s["symbol"].replace(".IS",""), s["price"], s["change_pct"], s.get("volume"))
            st.markdown(html + "</div>", unsafe_allow_html=True)
        else:
            st.info("Loading BIST data...")
        
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        section_header("TOP MOVERS — US", "today")
        us_data = api_get(f"{api_url}/api/market/US") or []
        if us_data:
            gainers = sorted(us_data, key=lambda x: x["change_pct"], reverse=True)[:8]
            html = "<div style='background:#111; border:1px solid #2a2a2a; border-radius:2px;'>"
            for s in gainers:
                html += stock_row_html(s["symbol"], s["price"], s["change_pct"], s.get("volume"))
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("Loading US data...")
    
    with col_r:
        section_header("LATEST NEWS", "financial markets")
        news = api_get(f"{api_url}/api/news") or []
        if news:
            for item in news[:12]:
                title = item.get("title", "")
                pub = item.get("publisher", "")
                published = item.get("published", "")
                link = item.get("link", "#")
                if title:
                    st.markdown(f"""
                    <div style="padding:8px; border-bottom:1px solid #1a1a1a; margin-bottom:2px;">
                        <a href="{link}" target="_blank" style="color:#e8e8e8; text-decoration:none; font-size:11px; line-height:1.4;">
                            {title[:120]}{'...' if len(title)>120 else ''}
                        </a>
                        <div style="margin-top:3px;">
                            <span style="color:#ff6600; font-size:9px;">{pub}</span>
                            <span style="color:#444; font-size:9px; margin-left:8px;">{published}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Loading news...")
    
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    
    # Macro snapshot bottom
    section_header("MACRO SNAPSHOT", "fx · commodities · crypto")
    macro = api_get(f"{api_url}/api/macro") or {}
    if macro:
        cols = st.columns(4)
        items = list(macro.items())
        for i, (name, data) in enumerate(items):
            with cols[i % 4]:
                chg = data.get("change_pct", 0)
                price = data.get("price", 0)
                decimals = 4 if price < 10 else 2
                st.metric(
                    label=name.replace("_", "/"),
                    value=f"{price:,.{decimals}f}",
                    delta=f"{chg:+.2f}%",
                )
