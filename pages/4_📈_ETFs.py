"""
ETF Analysis Page
"""

import streamlit as st
from utils.api_clients import StockDataClient
from utils.charts import create_price_chart, create_pie_chart
from utils.helpers import format_currency, format_percent
from config import ETF_LIST

st.set_page_config(page_title="ETFs", page_icon="📈", layout="wide")

st.title("📈 ETF Analysis")
st.caption("Exchange-Traded Funds - Performance & Holdings")

data_provider = st.session_state.get('data_provider', 'yfinance')
client = StockDataClient(data_provider)

st.info(f"📡 Using **{data_provider.upper()}** as data source")

tab1, tab2, tab3 = st.tabs(["📊 ETF Browser", "🔍 Search ETF", "📋 Comparison"])

with tab1:
    st.subheader("Popular ETFs by Category")
    
    for category, etfs in ETF_LIST.items():
        st.write(f"**{category}**")
        cols = st.columns(len(etfs))
        
        for idx, etf in enumerate(etfs):
            quote = client.get_quote(etf)
            if quote:
                with cols[idx]:
                    st.metric(
                        etf,
                        format_currency(quote['price']),
                        delta=f"{format_percent(quote['change_pct'])}",
                        delta_color="off"
                    )
        st.divider()

with tab2:
    st.subheader("Search & Analyze ETF")
    
    etf_symbol = st.text_input(
        "Enter ETF ticker:",
        value="SPY",
        placeholder="e.g., SPY, QQQ, VOO"
    ).upper()
    
    if etf_symbol:
        with st.spinner(f"Loading {etf_symbol}..."):
            quote = client.get_quote(etf_symbol)
            
            if quote:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Price", format_currency(quote['price']))
                with col2:
                    st.metric("Change", format_currency(quote['change']), delta_color="off")
                with col3:
                    st.metric("% Change", format_percent(quote['change_pct']), delta_color="off")
                with col4:
                    st.metric("Volume", f"{quote.get('volume', 0):,.0f}")
                with col5:
                    ytd_return = quote['change_pct']
                    st.metric("YTD Return", format_percent(ytd_return))
                
                st.divider()
                
                st.subheader("1-Year Performance")
                hist_data = client.get_historical(etf_symbol, period="1y")
                if hist_data is not None and not hist_data.empty:
                    fig = create_price_chart(hist_data, title=f"{etf_symbol} - 1 Year Performance")
                    st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("ETF Information")
                info = client.get_company_info(etf_symbol)
                if info:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Name:** {info.get('longName', 'N/A')}")
                        st.write(f"**Type:** {info.get('category', 'N/A')}")
                    with col2:
                        st.write(f"**Assets:** {format_currency(info.get('totalAssets', 0))}")
                        st.write(f"**Expense Ratio:** {info.get('expenseRatio', 'N/A')}")
                
                st.subheader("Related News")
                news = client.get_news(etf_symbol, limit=5)
                if news:
                    for item in news[:5]:
                        st.write(f"**{item.get('headline', 'N/A')}**")
                        st.caption(item.get('summary', 'N/A')[:150] + "...")
                        st.divider()
            else:
                st.error(f"Could not find data for {etf_symbol}")

with tab3:
    st.subheader("ETF Comparison")
    
    etf1 = st.text_input("First ETF:", value="SPY")
    etf2 = st.text_input("Second ETF:", value="IVV")
    
    if etf1 and etf2:
        col1, col2 = st.columns(2)
        
        quote1 = client.get_quote(etf1)
        quote2 = client.get_quote(etf2)
        
        if quote1 and quote2:
            with col1:
                st.subheader(etf1)
                st.metric("Price", format_currency(quote1['price']))
                st.metric("Change", format_percent(quote1['change_pct']))
            
            with col2:
                st.subheader(etf2)
                st.metric("Price", format_currency(quote2['price']))
                st.metric("Change", format_percent(quote2['change_pct']))
