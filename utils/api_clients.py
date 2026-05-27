"""
API Client implementations for different data providers
"""

import yfinance as yf
import finnhub
import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from config import FINNHUB_API_KEY, ALPHA_VANTAGE_API_KEY


class StockDataClient:
    """
    Unified interface for different stock data providers
    """
    
    def __init__(self, provider="yfinance"):
        """
        Initialize client with selected provider
        
        Args:
            provider: 'yfinance', 'finnhub', or 'alpha_vantage'
        """
        self.provider = provider
        
        if provider == "finnhub" and FINNHUB_API_KEY:
            self.finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        elif provider == "alpha_vantage" and ALPHA_VANTAGE_API_KEY:
            self.av_api_key = ALPHA_VANTAGE_API_KEY
    
    # ============= FINNHUB METHODS =============
    def get_finnhub_quote(self, symbol):
        """
        Get real-time quote from Finnhub
        """
        try:
            if not FINNHUB_API_KEY:
                st.warning("⚠️ Finnhub API Key not configured. Set FINNHUB_API_KEY in .env")
                return None
            
            quote = self.finnhub_client.quote(symbol)
            return {
                "symbol": symbol,
                "price": quote.get("c"),  # current price
                "change": quote.get("d"),  # change in price
                "change_pct": quote.get("dp"),  # change percent
                "high": quote.get("h"),  # high
                "low": quote.get("l"),  # low
                "open": quote.get("o"),  # open
                "previous_close": quote.get("pc"),  # previous close
                "timestamp": quote.get("t"),
                "provider": "Finnhub"
            }
        except Exception as e:
            st.error(f"Finnhub Error: {str(e)}")
            return None
    
    def get_finnhub_company_profile(self, symbol):
        """
        Get company profile from Finnhub
        """
        try:
            if not FINNHUB_API_KEY:
                return None
            
            profile = self.finnhub_client.company_profile2(symbol=symbol)
            return profile
        except Exception as e:
            st.error(f"Finnhub Profile Error: {str(e)}")
            return None
    
    def get_finnhub_news(self, symbol, limit=10):
        """
        Get news from Finnhub
        """
        try:
            if not FINNHUB_API_KEY:
                return []
            
            news = self.finnhub_client.company_news(symbol, _from=self._get_date_from_days(30), to=datetime.now().strftime("%Y-%m-%d"), limit=limit)
            return news
        except Exception as e:
            st.warning(f"Finnhub News Error: {str(e)}")
            return []
    
    def get_finnhub_sentiment(self, symbol):
        """
        Get sentiment data from Finnhub
        """
        try:
            if not FINNHUB_API_KEY:
                return None
            
            # Using news-sentiment endpoint
            sentiment = self.finnhub_client.news_sentiment(symbol)
            return sentiment
        except Exception as e:
            st.warning(f"Finnhub Sentiment Error: {str(e)}")
            return None
    
    # ============= YFINANCE METHODS =============
    def get_yfinance_quote(self, symbol):
        """
        Get real-time quote from YFinance
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            
            if data.empty:
                return None
            
            current_price = ticker.info.get("currentPrice") or data["Close"].iloc[-1]
            previous_close = ticker.info.get("previousClose") or data["Close"].iloc[0]
            
            change = current_price - previous_close
            change_pct = (change / previous_close) * 100 if previous_close else 0
            
            return {
                "symbol": symbol,
                "price": current_price,
                "change": change,
                "change_pct": change_pct,
                "high": data["High"].iloc[-1] if not data.empty else None,
                "low": data["Low"].iloc[-1] if not data.empty else None,
                "open": data["Open"].iloc[-1] if not data.empty else None,
                "previous_close": previous_close,
                "volume": data["Volume"].iloc[-1] if not data.empty else None,
                "timestamp": datetime.now().timestamp(),
                "provider": "YFinance"
            }
        except Exception as e:
            st.error(f"YFinance Error: {str(e)}")
            return None
    
    def get_yfinance_historical(self, symbol, period="1y"):
        """
        Get historical data from YFinance
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist
        except Exception as e:
            st.error(f"YFinance Historical Error: {str(e)}")
            return None
    
    def get_yfinance_company_info(self, symbol):
        """
        Get company info from YFinance
        """
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except Exception as e:
            st.error(f"YFinance Info Error: {str(e)}")
            return None
    
    def get_yfinance_news(self, symbol, limit=10):
        """
        Get news from YFinance
        """
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            return news[:limit] if news else []
        except Exception as e:
            st.warning(f"YFinance News Error: {str(e)}")
            return []
    
    # ============= ALPHA VANTAGE METHODS =============
    def get_alpha_vantage_quote(self, symbol):
        """
        Get quote from Alpha Vantage
        """
        try:
            if not ALPHA_VANTAGE_API_KEY:
                st.warning("⚠️ Alpha Vantage API Key not configured.")
                return None
            
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url)
            data = response.json()
            
            if "Global Quote" not in data:
                return None
            
            quote = data["Global Quote"]
            return {
                "symbol": symbol,
                "price": float(quote.get("05. price", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_pct": float(quote.get("10. change percent", "0").rstrip("%")),
                "high": float(quote.get("03. high", 0)),
                "low": float(quote.get("04. low", 0)),
                "open": float(quote.get("02. open", 0)),
                "previous_close": float(quote.get("08. previous close", 0)),
                "volume": int(quote.get("06. volume", 0)),
                "timestamp": datetime.now().timestamp(),
                "provider": "Alpha Vantage"
            }
        except Exception as e:
            st.error(f"Alpha Vantage Error: {str(e)}")
            return None
    
    # ============= UNIFIED INTERFACE =============
    def get_quote(self, symbol):
        """
        Get quote using configured provider
        """
        if self.provider == "finnhub":
            return self.get_finnhub_quote(symbol)
        elif self.provider == "alpha_vantage":
            return self.get_alpha_vantage_quote(symbol)
        else:  # yfinance
            return self.get_yfinance_quote(symbol)
    
    def get_historical(self, symbol, period="1y"):
        """
        Get historical data using configured provider
        """
        if self.provider == "yfinance":
            return self.get_yfinance_historical(symbol, period)
        else:
            # Fallback to yfinance for others
            return self.get_yfinance_historical(symbol, period)
    
    def get_company_info(self, symbol):
        """
        Get company info using configured provider
        """
        if self.provider == "finnhub":
            return self.get_finnhub_company_profile(symbol)
        elif self.provider == "yfinance":
            return self.get_yfinance_company_info(symbol)
        else:
            return None
    
    def get_news(self, symbol, limit=10):
        """
        Get news using configured provider
        """
        if self.provider == "finnhub":
            return self.get_finnhub_news(symbol, limit)
        elif self.provider == "yfinance":
            return self.get_yfinance_news(symbol, limit)
        else:
            return []
    
    # ============= HELPER METHODS =============
    @staticmethod
    def _get_date_from_days(days=30):
        """
        Get date string from X days ago
        """
        return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")


class NewsClient:
    """
    Financial news aggregation client
    """
    
    def __init__(self):
        pass
    
    def get_market_news(self, category="general", limit=20):
        """
        Get market-wide news
        """
        try:
            # This would integrate with news APIs
            pass
        except Exception as e:
            st.error(f"News Error: {str(e)}")
            return []
