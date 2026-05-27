"""
Watchlist & Portfolio Tracking Page
"""

import streamlit as st
import pandas as pd
from utils.api_clients import StockDataClient
from utils.helpers import format_currency, format_percent

st.set_page_config(page_title="Watchlist", page_icon="⭐", layout="wide")

st.title("⭐ My Watchlist")
st.caption("Track your favorite stocks and manage your portfolio")

data_provider = st.session_state.get('data_provider', 'yfinance')
client = StockDataClient(data_provider)

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}

tab1, tab2, tab3 = st.tabs(["📌 My Stocks", "💼 Portfolio", "📊 Performance"])

with tab1:
    st.subheader("Watchlist Stocks")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        new_stock = st.text_input("Add ticker to watchlist:")
    with col2:
        if st.button("Add", use_container_width=True):
            if new_stock and new_stock.upper() not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_stock.upper())
                st.success(f"Added {new_stock.upper()} to watchlist!")
                st.rerun()
            elif new_stock.upper() in st.session_state.watchlist:
                st.warning("Already in watchlist!")
    
    st.divider()
    
    if st.session_state.watchlist:
        watchlist_data = []
        for symbol in st.session_state.watchlist:
            quote = client.get_quote(symbol)
            if quote:
                watchlist_data.append({
                    "Ticker": symbol,
                    "Price": format_currency(quote['price']),
                    "Change": format_currency(quote['change']),
                    "Change %": format_percent(quote['change_pct']),
                    "High": format_currency(quote.get('high', 0)),
                    "Low": format_currency(quote.get('low', 0))
                })
        
        if watchlist_data:
            df = pd.DataFrame(watchlist_data)
            st.dataframe(df, use_container_width=True)
            
            st.divider()
            
            st.subheader("Manage Watchlist")
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                remove_stock = st.selectbox("Remove stock:", st.session_state.watchlist)
            with col2:
                if st.button("Remove", use_container_width=True):
                    st.session_state.watchlist.remove(remove_stock)
                    st.success(f"Removed {remove_stock}")
                    st.rerun()
    else:
        st.info("📌 Your watchlist is empty. Add stocks using the input above!")

with tab2:
    st.subheader("Portfolio Holdings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        add_ticker = st.text_input("Ticker:")
    with col2:
        quantity = st.number_input("Quantity:", min_value=1, value=1)
    with col3:
        if st.button("Add to Portfolio"):
            if add_ticker:
                st.session_state.portfolio[add_ticker.upper()] = quantity
                st.success(f"Added {quantity} shares of {add_ticker.upper()}")
                st.rerun()
    
    st.divider()
    
    if st.session_state.portfolio:
        portfolio_data = []
        total_value = 0
        
        for ticker, qty in st.session_state.portfolio.items():
            quote = client.get_quote(ticker)
            if quote:
                value = quote['price'] * qty
                total_value += value
                portfolio_data.append({
                    "Ticker": ticker,
                    "Quantity": qty,
                    "Price": format_currency(quote['price']),
                    "Value": format_currency(value),
                    "Change %": format_percent(quote['change_pct'])
                })
        
        if portfolio_data:
            df = pd.DataFrame(portfolio_data)
            st.dataframe(df, use_container_width=True)
            
            st.divider()
            st.metric("Portfolio Value", format_currency(total_value))
    else:
        st.info("💼 Your portfolio is empty. Add holdings above!")

with tab3:
    st.subheader("Performance Analytics")
    
    if st.session_state.watchlist or st.session_state.portfolio:
        stocks_to_analyze = list(set(st.session_state.watchlist + list(st.session_state.portfolio.keys())))
        
        performance_data = []
        for ticker in stocks_to_analyze[:10]:
            quote = client.get_quote(ticker)
            if quote:
                performance_data.append({
                    "Ticker": ticker,
                    "Price": quote['price'],
                    "Change %": quote['change_pct']
                })
        
        if performance_data:
            df = pd.DataFrame(performance_data)
            df_sorted = df.sort_values("Change %", ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top Gainers**")
                gainers = df_sorted[df_sorted["Change %"] > 0].head(5)
                for _, row in gainers.iterrows():
                    st.metric(row["Ticker"], format_percent(row["Change %"]), delta=None)
            
            with col2:
                st.markdown("**Top Losers**")
                losers = df_sorted[df_sorted["Change %"] < 0].tail(5)
                for _, row in losers.iterrows():
                    st.metric(row["Ticker"], format_percent(row["Change %"]), delta=None)
    else:
        st.info("Add stocks to your watchlist or portfolio to see performance analytics.")
