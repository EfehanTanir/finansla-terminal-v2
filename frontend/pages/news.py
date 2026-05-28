"""NEWS FEED PAGE"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.shared import *

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">📰 NEWS FEED</span>
        <span style="color:#555; font-size:10px;">REAL-TIME FINANCIAL NEWS · MULTIPLE SOURCES</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🌍  MARKET NEWS", "🔍  STOCK NEWS"])
    
    with tab1:
        section_header("LATEST MARKET NEWS", "aggregated from yfinance")
        
        col_search, col_btn = st.columns([3, 1])
        with col_search:
            query = st.text_input("Search topic", value="stock market finance", key="news_query", 
                                   placeholder="e.g. Fed rates, BIST, earnings...")
        with col_btn:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            refresh = st.button("REFRESH", key="news_refresh")
        
        with st.spinner("Loading news..."):
            news = api_get(f"{api_url}/api/news?query={query}&limit=30") or []
        
        if news:
            # Group by publisher
            publishers = list(set(item.get("publisher","") for item in news if item.get("publisher")))
            
            # All news feed
            for item in news:
                title = item.get("title","")
                pub = item.get("publisher","")
                published = item.get("published","")
                link = item.get("link","#")
                symbol = item.get("symbol","")
                
                if not title:
                    continue
                
                pub_color = "#ff6600" if "Bloomberg" in pub or "Reuters" in pub else "#0099ff"
                
                st.markdown(f"""
                <div style="background:#111; border:1px solid #1e1e1e; border-left:3px solid #2a2a2a;
                            padding:10px 14px; margin-bottom:4px; border-radius:2px;
                            transition:all 0.15s;"
                     onmouseover="this.style.borderLeftColor='#ff6600'; this.style.background='#161616'"
                     onmouseout="this.style.borderLeftColor='#2a2a2a'; this.style.background='#111'">
                    <a href="{link}" target="_blank" 
                       style="color:#e8e8e8; text-decoration:none; font-size:12px; line-height:1.5; font-weight:500;">
                        {title}
                    </a>
                    <div style="margin-top:5px; display:flex; gap:12px; align-items:center;">
                        <span style="color:{pub_color}; font-size:9px; letter-spacing:0.05em;">{pub}</span>
                        <span style="color:#444; font-size:9px;">{published}</span>
                        {'<span style="color:#ff6600; font-size:9px; background:#ff660011; padding:1px 5px; border-radius:2px;">'+symbol+'</span>' if symbol else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No news available. Try refreshing.")
    
    with tab2:
        section_header("STOCK-SPECIFIC NEWS", "headlines for any ticker")
        
        col_sym, col_btn2 = st.columns([3, 1])
        with col_sym:
            stock_sym = st.text_input("Enter symbol", value="AAPL", key="news_sym",
                                       placeholder="AAPL, THYAO.IS, ASML.AS...")
        with col_btn2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            load_news = st.button("LOAD NEWS", key="news_sym_btn")
        
        if load_news or stock_sym:
            sym = stock_sym.upper()
            with st.spinner(f"Loading news for {sym}..."):
                stock_news = api_get(f"{api_url}/api/news/stock/{sym}") or []
            
            if stock_news:
                st.markdown(f"<div style='color:#888; font-size:10px; margin-bottom:12px;'>{len(stock_news)} articles found for <span style='color:#ff6600;'>{sym}</span></div>", unsafe_allow_html=True)
                
                for item in stock_news:
                    title = item.get("title","")
                    pub = item.get("publisher","")
                    published = item.get("published","")
                    link = item.get("link","#")
                    
                    if not title:
                        continue
                    
                    st.markdown(f"""
                    <div style="background:#111; border:1px solid #1e1e1e; border-left:3px solid #ff6600;
                                padding:10px 14px; margin-bottom:4px; border-radius:2px;">
                        <a href="{link}" target="_blank" 
                           style="color:#e8e8e8; text-decoration:none; font-size:12px; line-height:1.5;">
                            {title}
                        </a>
                        <div style="margin-top:5px;">
                            <span style="color:#ff6600; font-size:9px;">{pub}</span>
                            <span style="color:#444; font-size:9px; margin-left:10px;">{published}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"No news found for {sym}. Try a different symbol.")
