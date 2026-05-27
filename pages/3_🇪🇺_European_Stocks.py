"""
European Stock Market Page - Euronext, LSE, Xetra, SIX
"""

import streamlit as st
from utils.api_clients import StockDataClient
from utils.charts import create_price_chart
from utils.helpers import format_currency, format_percent
from config import EUROPEAN_MARKET_TICKERS

st.set_page_config(page_title="European Stocks", page_icon="🇪🇺", layout="wide")

st.title("🇪🇺 European Stock Markets")
st.caption("Euronext, LSE, Xetra, SIX - Major European exchanges")

data_provider = st.session_state.get('data_provider', 'yfinance')
client = StockDataClient(data_provider)

st.info(f"📡 Using **{data_provider.upper()}** as data source")

tab1, tab2, tab3 = st.tabs(["📊 Market Overview", "🔍 Stock Search", "🏢 Companies"])

with tab1:
    st.subheader("Major European Indices")
    
    indices = ["^STOXX50E", "^N100", "^FTSE", "^GDAXI"]
    names = ["STOXX 50", "Eurostoxx 100", "FTSE 100", "DAX"]
    
    cols = st.columns(4)
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

with tab2:
    st.subheader("Search European Stocks")
    
    search_symbol = st.text_input(
        "Enter ticker symbol:",
        value="SAP.DE",
        placeholder="e.g., SAP.DE, ASML.AS, LVMH.PA"
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
                
                hist_data = client.get_historical(search_symbol, period="1y")
                if hist_data is not None and not hist_data.empty:
                    fig = create_price_chart(hist_data, title=f"{search_symbol} - 1 Year")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Could not find data for {search_symbol}")

with tab3:
    st.subheader("European Companies by Country")
    
    for country, tickers in EUROPEAN_MARKET_TICKERS.items():
        if country != "Indices":
            st.write(f"**{country}**")
            cols = st.columns(min(4, len(tickers)))
            
            for idx, ticker in enumerate(tickers):
                quote = client.get_quote(ticker)
                if quote:
                    with cols[idx % 4]:
                        st.metric(
                            ticker,
                            format_currency(quote['price']),
                            delta=f"{format_percent(quote['change_pct'])}",
                            delta_color="off"
                        )
            st.divider()
