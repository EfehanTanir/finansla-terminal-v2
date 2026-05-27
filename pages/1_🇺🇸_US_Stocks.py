"""
US Stock Market Page - NASDAQ, NYSE, S&P 500
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.api_clients import StockDataClient
from utils.charts import create_price_chart, create_candlestick_chart, create_volume_chart
from utils.helpers import format_currency, format_percent, get_change_color, is_market_open
from config import US_MARKET_TICKERS

st.set_page_config(page_title="US Stocks", page_icon="🇺🇸", layout="wide")

st.title("🇺🇸 US Stock Market")
st.caption("NASDAQ, NYSE, S&P 500 - Real-time quotes and analysis")

# Get selected data provider
data_provider = st.session_state.get('data_provider', 'yfinance')
client = StockDataClient(data_provider)

st.info(f"📡 Using **{data_provider.upper()}** as data source")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Overview", "🔍 Stock Search", "📈 Top Gainers", "⭐ Watchlist"])

with tab1:
    st.subheader("Market Indices")
    
    col1, col2, col3 = st.columns(3)
    
    indices = ["^GSPC", "^IXIC", "^DJI"]
    indices_names = ["S&P 500", "NASDAQ", "Dow Jones"]
    
    for idx, (symbol, name) in enumerate(zip(indices, indices_names)):
        quote = client.get_quote(symbol)
        if quote:
            cols = [col1, col2, col3]
            with cols[idx]:
                st.metric(
                    name,
                    format_currency(quote['price']),
                    delta=f"{format_percent(quote['change_pct'])}",
                    delta_color="off"
                )
    
    st.divider()
    
    # Stock categories
    st.subheader("Popular Sectors")
    
    for category, tickers in US_MARKET_TICKERS.items():
        if category != "Indices":
            st.write(f"**{category}**")
            cols = st.columns(len(tickers[:5]))
            
            for idx, ticker in enumerate(tickers[:5]):
                quote = client.get_quote(ticker)
                if quote:
                    with cols[idx]:
                        color = get_change_color(quote['change'])
                        st.metric(
                            ticker,
                            format_currency(quote['price']),
                            delta=f"{format_percent(quote['change_pct'])}",
                            delta_color="off"
                        )
            st.divider()

with tab2:
    st.subheader("Search Stocks")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_symbol = st.text_input(
            "Enter ticker symbol:",
            value="AAPL",
            placeholder="e.g., AAPL, MSFT, GOOGL"
        ).upper()
    
    with col2:
        period = st.selectbox("Period:", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
    
    if search_symbol:
        with st.spinner(f"Loading {search_symbol}..."):
            # Get quote
            quote = client.get_quote(search_symbol)
            
            if quote:
                # Header
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Price", format_currency(quote['price']))
                with col2:
                    st.metric(
                        "Change",
                        format_currency(quote['change']),
                        delta_color="off"
                    )
                with col3:
                    st.metric(
                        "% Change",
                        format_percent(quote['change_pct']),
                        delta_color="off"
                    )
                with col4:
                    st.metric("Volume", f"{quote.get('volume', 0):,.0f}")
                
                st.divider()
                
                # Chart
                st.subheader("Price Chart")
                hist_data = client.get_historical(search_symbol, period=period)
                
                if hist_data is not None and not hist_data.empty:
                    fig = create_price_chart(hist_data, title=f"{search_symbol} - {period}")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Volume chart
                    fig_volume = create_volume_chart(hist_data)
                    st.plotly_chart(fig_volume, use_container_width=True)
                else:
                    st.warning("Could not load historical data")
                
                # Company info
                st.subheader("Company Information")
                info = client.get_company_info(search_symbol)
                if info:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                        st.write(f"**Country:** {info.get('country', 'N/A')}")
                    with col2:
                        st.write(f"**Market Cap:** {format_currency(info.get('marketCap', 0))}")
                        st.write(f"**52W High:** {format_currency(info.get('fiftyTwoWeekHigh', 0))}")
                        st.write(f"**52W Low:** {format_currency(info.get('fiftyTwoWeekLow', 0))}")
                
                # News
                st.subheader("Latest News")
                news = client.get_news(search_symbol, limit=5)
                if news:
                    for item in news[:5]:
                        st.write(f"**{item.get('headline', 'N/A')}**")
                        st.caption(item.get('summary', 'N/A')[:200] + "...")
                        st.divider()
                else:
                    st.info("No news available")
            else:
                st.error(f"Could not find data for {search_symbol}")

with tab3:
    st.subheader("Top Gainers")
    st.info("This section will show top performers for the day")

with tab4:
    st.subheader("My Watchlist")
    
    watchlist_symbol = st.text_input("Add to watchlist:", key="watchlist_input")
    if st.button("Add"):
        if watchlist_symbol not in st.session_state.watchlist:
            st.session_state.watchlist.append(watchlist_symbol)
            st.success(f"Added {watchlist_symbol} to watchlist!")
    
    if st.session_state.watchlist:
        st.write("**Your Watchlist:**")
        for symbol in st.session_state.watchlist:
            col1, col2 = st.columns([4, 1])
            with col1:
                quote = client.get_quote(symbol)
                if quote:
                    st.write(f"{symbol}: {format_currency(quote['price'])} ({format_percent(quote['change_pct'])})")
            with col2:
                if st.button("❌", key=f"remove_{symbol}"):
                    st.session_state.watchlist.remove(symbol)
                    st.rerun()
    else:
        st.info("Your watchlist is empty. Add stocks to track them!")
