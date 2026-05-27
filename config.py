""""
Configuration and constants for Finansla Terminal V2
""""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")

# Data Provider Options
DATA_PROVIDERS = {
    "yfinance": "Yahoo Finance (Free, No API Key)",
    "finnhub": "Finnhub (Requires API Key)",
    "alpha_vantage": "Alpha Vantage (Requires API Key)"
}

# Market Configurations
US_MARKET_TICKERS = {
    "Indices": ["^GSPC", "^IXIC", "^DJI"],  # S&P 500, NASDAQ, Dow Jones
    "Tech Giants": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"],
    "Finance": ["JPM", "BAC", "WFC", "GS", "MS"],
    "Healthcare": ["JNJ", "UNH", "PFE", "MRNA", "ASML"],
    "Energy": ["XOM", "CVX", "COP"],
    "Consumer": ["MCD", "SBUX", "NKE", "AMZN", "COST"]
}

TURKISH_MARKET_TICKERS = {
    "Indices": ["XU100.IS", "XU030.IS"],  # BIST 100, BIST 30
    "Banks": ["AKBNK.IS", "SISE.IS", "GARAN.IS", "VAKBN.IS", "HALKB.IS"],
    "Energy": ["THYAO.IS", "ARCLK.IS"],
    "Retail": ["CARSI.IS", "MIGROS.IS"],
    "Tech/Telecom": ["ASELS.IS", "TURK.IS"],
    "Manufacturing": ["ASELS.IS", "TATGD.IS", "BIMAS.IS"]
}

EUROPEAN_MARKET_TICKERS = {
    "Indices": ["^STOXX50E", "^N100", "^FTSE", "^GDAXI"],  # STOXX 50, Eurostoxx, FTSE, DAX
    "France (CAC 40)": ["MC.PA", "BN.PA", "ENGI.PA", "AI.PA"],  # Lvmh, Danone, Engie, Air Liquide
    "Germany (DAX)": ["SAP.DE", "SIE.DE", "MRK.DE", "ALV.DE"],  # SAP, Siemens, Merck, Allianz
    "UK (FTSE 100)": ["SHEL.L", "ULVR.L", "HSBA.L", "AZN.L"],  # Shell, Unilever, HSBC, AstraZeneca
    "Netherlands": ["ASML.AS", "PHIA.AS"],  # ASML, Philips
    "Switzerland": ["NOVN.SW", "RHHBY.SW"]  # Novartis, Roche
}

ETF_LIST = {
    "US Large Cap": ["SPY", "IVV", "VOO"],  # S&P 500 ETFs
    "Tech Heavy": ["QQQ", "XLK", "IGV"],  # NASDAQ-100, Tech Sector, Cloud
    "Emerging Markets": ["EEM", "SCHE", "EUSA"],  # Emerging Markets
    "European": ["EZU", "EUSA", "VGK"],  # European equity ETFs
    "Global Dividend": ["VYM", "SCHD", "DGRO"],  # Dividend focus
    "Bonds": ["BND", "AGG", "LQD"],  # Bond ETFs
}

# UI Theme Colors
COLOR_GREEN = "#00D084"  # Green for positive
COLOR_RED = "#FF6B6B"   # Red for negative
COLOR_NEUTRAL = "#95A5A6" # Gray for neutral
BACKGROUND_DARK = "#0f1419"
TEXT_PRIMARY = "#E0E0E0"
TEXT_SECONDARY = "#A0A0A0"

# Cache Settings
CACHE_TTL = 300  # 5 minutes for stock data
NEWS_CACHE_TTL = 3600  # 1 hour for news

# Market Hours (UTC)
US_MARKET_OPEN = "14:30"  # 9:30 AM EST
US_MARKET_CLOSE = "21:00"  # 4:00 PM EST
TURKISH_MARKET_OPEN = "07:00"  # 10:00 AM Istanbul
TURKISH_MARKET_CLOSE = "15:00"  # 6:00 PM Istanbul
EUROPEAN_MARKET_OPEN = "07:00"  # 8:00 AM CET
EUROPEAN_MARKET_CLOSE = "16:30"  # 5:30 PM CET
