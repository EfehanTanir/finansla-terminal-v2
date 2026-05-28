"""
Turkish Stock Market Page - Borsa Istanbul (BIST)
"""

import streamlit as st
from utils.api_clients import StockDataClient
from utils.charts import create_price_chart
from utils.helpers import format_currency, format_percent
from config import TURKISH_MARKET_TICKERS, FINNHUB_API_KEY

st.set_page_config(page_title="Turkish Stocks", page_icon="🇹🇷", layout="wide")

# ==========================================
# 🧠 MEMORY INITIALIZATION (CRITICAL FOR MULTIPAGE)
# ==========================================
if 'data_provider' not in st.session_state:
    st.session_state.data_provider = "finnhub"

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
# ==========================================

st.title("🇹🇷 Turkish Stock Market (Borsa Istanbul)")
st.caption("BIST 100, BIST 30 - Turkish exchanges")

data_provider = st.session_state.get('data_provider', 'finnhub')
client = StockDataClient(data_provider)

# Warning for Turkish market support
if data_provider == "yfinance":
    st.warning(
        "⚠️ **Note:** YFinance has limited Turkish market data. For best results, use **Finnhub** "
        "(change in sidebar) which has full BIST coverage. Turkish tickers use `.IS` suffix (e.g., AKBNK.IS)"
    )
elif data_provider == "finnhub" and not FINNHUB_API_KEY:
    st.warning("⚠️ Finnhub API Key not configured. Set FINNHUB_API_KEY in .env file or cloud variables.")

st.info(f"📡 Using **{data_provider.upper()}** as data source")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Market Overview", "🔍 Stock Search", "📱 Companies"])

with tab1:
    st.subheader("Major Indices")
    
    # BIST indices
    indices = ["XU100.IS", "XU030.IS"]
    names = ["BIST 100", "BIST 30"]
    
    cols = st.columns(2)
    for idx, (symbol, name) in enumerate(zip(indices, names)):
        quote = client.get_quote(symbol)
        if quote:
            with cols[idx]:
                st.metric(
                    name,
                    format_currency(quote['price']),
                    delta=f"{format_percent(quote['change_pct'])}",
                    delta_color="off"
                )
        else:
            with cols[idx]:
                st.warning(f"Data unavailable for {name}")

with tab2:
    st.subheader("Search Turkish Stocks")
    
    search_symbol = st.text_input(
        "Enter ticker (with .IS suffix):",
        value="AKBNK.IS",
        placeholder="e.g., AKBNK.IS, GARAN.IS"
    ).upper()
    
    if search_symbol:
        with st.spinner(f"Loading {search_symbol}..."):
            quote = client.get_quote(search_symbol)
            
            if quote:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Price", format_currency(quote['price']))
                with col2:
                    st.metric("Change", format_currency(quote['change']), delta_color="off")
                with col3:
                    st.metric("% Change", format_percent(quote['change_pct']), delta_color="off")
                with col4:
                    st.metric("Volume", f"{quote.get('volume', 0):,.0f}")
                
                st.divider()
                
                # Chart
                hist_data = client.get_historical(search_symbol, period="1y")
                if hist_data is not None and not hist_data.empty:
                    fig = create_price_chart(hist_data, title=f"{search_symbol} - 1 Year")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Historical data not available for this ticker")
            else:
                st.error(f"Could not find data for {search_symbol}")
                st.info("💡 Tip: Make sure to use the correct format (e.g., AKBNK.IS) and that your provider supports Turkish stocks.")

with tab3:
    st.subheader("Turkish Companies by Sector")
    
    for sector, tickers in TURKISH_MARKET_TICKERS.items():
        if sector != "Indices":
            st.write(f"**{sector}**")
            cols = st.columns(min(3, len(tickers)))
            
            for idx, ticker in enumerate(tickers[:3]):
                quote = client.get_quote(ticker)
                if quote:
                    with cols[idx % 3]:
                        st.metric(
                            ticker,
                            format_currency(quote['price']),
                            delta=f"{format_percent(quote['change_pct'])}",
                            delta_color="off"
                        )
                else:
                    with cols[idx % 3]:
                        st.caption(f"{ticker}: N/A")
            
            st.divider()