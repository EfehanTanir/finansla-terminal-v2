"""ETF TRACKER PAGE"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.shared import *
import plotly.graph_objects as go

ETF_CATEGORIES = {
    "Broad Market": ["SPY","VOO","VTI","QQQ","IWM"],
    "International": ["EEM","EFA","IEMG"],
    "Fixed Income": ["TLT","HYG","LQD","AGG","BND"],
    "Commodities": ["GLD","SLV","USO","IAU"],
    "Sector": ["XLK","XLF","XLE","XLV"],
    "Thematic": ["ARKK","BITO","VNQ"],
    "Inverse/Leveraged": ["SQQQ"],
}

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">📈 ETF TRACKER</span>
        <span style="color:#555; font-size:10px;">EXCHANGE TRADED FUNDS · YTD PERFORMANCE · AUM</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊  ALL ETFs", "📈  ETF DETAIL", "🏆  PERFORMANCE RANKING"])
    
    with tab1:
        section_header("ETF MARKET BOARD", "year-to-date performance")
        
        with st.spinner("Loading ETF data..."):
            etfs = api_get(f"{api_url}/api/etfs") or []
        
        if etfs:
            col_f1, col_f2 = st.columns([2,1])
            with col_f1:
                sort_by = st.selectbox("Sort by", ["YTD %", "Change %", "AUM", "Price", "Symbol"], key="etf_sort")
            with col_f2:
                direction = st.selectbox("Order", ["Descending", "Ascending"], key="etf_dir")
            
            key_map = {"YTD %": "ytd_pct", "Change %": "change_pct", "AUM": "aum", "Price": "price", "Symbol": "symbol"}
            etfs_sorted = sorted(etfs, key=lambda x: x.get(key_map[sort_by], 0) or 0, reverse=(direction == "Descending"))
            
            # Header
            st.markdown("""
            <div style="display:grid; grid-template-columns:80px 1fr 90px 90px 100px 80px; gap:4px;
                        padding:5px 8px; background:#1a1a1a; font-size:9px; color:#555; letter-spacing:0.1em;
                        border-bottom:1px solid #2a2a2a;">
                <span>SYMBOL</span><span>NAME</span><span style="text-align:right">PRICE</span>
                <span style="text-align:right">DAY%</span><span style="text-align:right">YTD%</span>
                <span style="text-align:right">AUM</span>
            </div>
            """, unsafe_allow_html=True)
            
            html = "<div style='background:#0d0d0d; border:1px solid #2a2a2a; border-top:none; max-height:500px; overflow-y:auto;'>"
            for e in etfs_sorted:
                ytd = e.get("ytd_pct", 0)
                chg = e.get("change_pct", 0)
                ytd_col = "#00cc66" if ytd >= 0 else "#ff3333"
                chg_col = "#00cc66" if chg >= 0 else "#ff3333"
                name = (e.get("name") or e["symbol"])[:30]
                aum_str = fmt_mcap(e.get("aum"))
                html += f"""
                <div style="display:grid; grid-template-columns:80px 1fr 90px 90px 100px 80px; gap:4px;
                            padding:5px 8px; border-bottom:1px solid #1a1a1a; font-size:11px;
                            align-items:center;"
                     onmouseover="this.style.background='#1a1a1a'" onmouseout="this.style.background='transparent'">
                    <span style="color:#ff6600; font-weight:600;">{e['symbol']}</span>
                    <span style="color:#888; font-size:10px;">{name}</span>
                    <span style="color:#e8e8e8; text-align:right;">{e['price']:,.2f}</span>
                    <span style="color:{chg_col}; text-align:right;">{'+' if chg>=0 else ''}{chg:.2f}%</span>
                    <span style="color:{ytd_col}; text-align:right; font-weight:600;">{'+' if ytd>=0 else ''}{ytd:.2f}%</span>
                    <span style="color:#555; font-size:10px; text-align:right;">{aum_str}</span>
                </div>
                """
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
            
            # Category breakdown
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            section_header("BY CATEGORY", "grouped view")
            
            for cat, syms in ETF_CATEGORIES.items():
                cat_etfs = [e for e in etfs if e["symbol"] in syms]
                if cat_etfs:
                    avg_ytd = sum(e.get("ytd_pct", 0) for e in cat_etfs) / len(cat_etfs)
                    col_c = "#00cc66" if avg_ytd >= 0 else "#ff3333"
                    st.markdown(f"<span style='color:#888; font-size:10px; letter-spacing:0.1em;'>{cat} <span style='color:{col_c};'>avg YTD {avg_ytd:+.1f}%</span></span>", unsafe_allow_html=True)
                    
                    cols = st.columns(len(cat_etfs))
                    for i, e in enumerate(cat_etfs):
                        with cols[i]:
                            st.metric(e["symbol"], f"${e['price']:.2f}", f"{e.get('ytd_pct',0):+.1f}% YTD")
                    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        else:
            st.warning("Could not load ETF data")
    
    with tab2:
        section_header("ETF DETAIL", "full breakdown + chart")
        
        col_sym, col_per = st.columns([2, 1])
        with col_sym:
            etf_sym = st.text_input("ETF Symbol", value="SPY", key="etf_detail_sym")
        with col_per:
            period = st.selectbox("Period", ["1mo","3mo","6mo","1y","2y","5y"], index=3, key="etf_detail_per")
        
        if st.button("LOAD ETF", key="etf_detail_load"):
            with st.spinner(f"Loading {etf_sym.upper()}..."):
                data = api_get(f"{api_url}/api/etf/{etf_sym.upper()}")
                chart_data = api_get(f"{api_url}/api/stock/{etf_sym.upper()}?period={period}")
            
            if data:
                c1, c2, c3, c4 = st.columns(4)
                price = chart_data["current_price"] if chart_data else 0
                c1.metric("PRICE", f"${price:,.2f}")
                c2.metric("AUM", fmt_mcap(data.get("aum")))
                c3.metric("EXP RATIO", f"{(data.get('expense_ratio') or 0)*100:.2f}%" if data.get("expense_ratio") else "—")
                c4.metric("YTD", fmt_pct(data.get("ytd_pct")))
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                    <div class='fin-card'>
                        <div class='fin-header'>FUND INFO</div>
                        <div style="font-size:14px; color:#e8e8e8;">{data.get('name', etf_sym.upper())}</div>
                        <div style="font-size:10px; color:#888; margin-top:4px;">{data.get('category','N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if data.get("description"):
                    with st.expander("Fund Description"):
                        st.write(data["description"])
                
                if chart_data and chart_data.get("ohlcv"):
                    fig = make_line_chart(chart_data["ohlcv"], "date", "close", f"{etf_sym.upper()} — Price", 350)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"No data for {etf_sym.upper()}")
    
    with tab3:
        section_header("PERFORMANCE RANKING", "YTD leaders & laggards")
        
        etfs_all = api_get(f"{api_url}/api/etfs") or []
        
        if etfs_all:
            etfs_ytd = sorted(etfs_all, key=lambda x: x.get("ytd_pct", 0), reverse=True)
            
            col_best, col_worst = st.columns(2)
            
            with col_best:
                st.markdown("<div style='color:#00cc66; font-size:11px; margin-bottom:8px; letter-spacing:0.1em;'>🏆 TOP PERFORMERS</div>", unsafe_allow_html=True)
                html = "<div style='background:#0d0d0d; border:1px solid #2a2a2a; border-radius:2px;'>"
                for e in etfs_ytd[:10]:
                    ytd = e.get("ytd_pct", 0)
                    bar_w = min(int(abs(ytd) * 3), 100)
                    html += f"""
                    <div style="padding:6px 8px; border-bottom:1px solid #1a1a1a; display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#ff6600; font-weight:600; min-width:60px;">{e['symbol']}</span>
                        <div style="flex:1; margin:0 8px;">
                            <div style="background:#00cc6633; height:4px; width:{bar_w}%; border-radius:2px;"></div>
                        </div>
                        <span style="color:#00cc66; font-weight:600;">+{ytd:.2f}%</span>
                    </div>
                    """
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            
            with col_worst:
                st.markdown("<div style='color:#ff3333; font-size:11px; margin-bottom:8px; letter-spacing:0.1em;'>📉 WORST PERFORMERS</div>", unsafe_allow_html=True)
                html = "<div style='background:#0d0d0d; border:1px solid #2a2a2a; border-radius:2px;'>"
                for e in reversed(etfs_ytd[-10:]):
                    ytd = e.get("ytd_pct", 0)
                    bar_w = min(int(abs(ytd) * 3), 100)
                    html += f"""
                    <div style="padding:6px 8px; border-bottom:1px solid #1a1a1a; display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#ff6600; font-weight:600; min-width:60px;">{e['symbol']}</span>
                        <div style="flex:1; margin:0 8px;">
                            <div style="background:#ff333333; height:4px; width:{bar_w}%; border-radius:2px;"></div>
                        </div>
                        <span style="color:#ff3333; font-weight:600;">{ytd:.2f}%</span>
                    </div>
                    """
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
