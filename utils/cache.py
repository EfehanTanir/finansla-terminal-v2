"""
Caching utilities for API requests
"""

import streamlit as st
from datetime import datetime, timedelta
import hashlib
from config import CACHE_TTL, NEWS_CACHE_TTL


def get_cache_key(provider, ticker, data_type="quote"):
    """
    Generate a unique cache key
    """
    key = f"{provider}_{ticker}_{data_type}"
    return hashlib.md5(key.encode()).hexdigest()


@st.cache_data(ttl=CACHE_TTL)
def cached_stock_data(provider, ticker, data_type="quote"):
    """
    Cache stock data with TTL
    """
    pass


@st.cache_data(ttl=NEWS_CACHE_TTL)
def cached_news_data(ticker):
    """
    Cache news data with longer TTL
    """
    pass


def clear_cache():
    """
    Clear Streamlit cache
    """
    st.cache_data.clear()
