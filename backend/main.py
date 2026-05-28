"""
FINANSAL TERMINAL - FastAPI Backend
Bloomberg-style financial terminal backend
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yfinance as yf
import pandas as pd
import numpy as np
import httpx
import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional, List
import os
from functools import lru_cache
import time

app = FastAPI(title="Finansal Terminal API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Simple in-memory cache ───────────────────────────────────────────────────
_cache: dict = {}
CACHE_TTL = 60  # seconds

def cache_get(key: str):
    if key in _cache:
        val, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return val
    return None

def cache_set(key: str, val):
    _cache[key] = (val, time.time())

# ─── STOCK INDICES ─────────────────────────────────────────────────────────────
INDICES = {
    "BIST100": "XU100.IS",
    "BIST30": "XU030.IS",
    "SPX": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW": "^DJI",
    "DAX": "^GDAXI",
    "CAC40": "^FCHI",
    "FTSE100": "^FTSE",
    "EUROSTOXX": "^STOXX50E",
    "NIKKEI": "^N225",
    "VIX": "^VIX",
    "GOLD": "GC=F",
    "OIL": "CL=F",
    "EUR/USD": "EURUSD=X",
    "USD/TRY": "USDTRY=X",
    "BTC": "BTC-USD",
}

BIST_STOCKS = [
    "THYAO.IS","GARAN.IS","AKBNK.IS","EREGL.IS","SASA.IS",
    "KCHOL.IS","BIMAS.IS","ASELS.IS","FROTO.IS","TOASO.IS",
    "TUPRS.IS","YKBNK.IS","SAHOL.IS","SISE.IS","HALKB.IS",
    "VAKBN.IS","PGSUS.IS","TCELL.IS","VESTL.IS","ARCLK.IS",
    "KOZAL.IS","KRDMD.IS","EKGYO.IS","OYAKC.IS","TAVHL.IS",
    "MGROS.IS","LOGO.IS","NETAS.IS","GUBRF.IS","PETKM.IS",
]

US_STOCKS = [
    "AAPL","MSFT","NVDA","GOOGL","AMZN","META","TSLA","BRK-B",
    "JPM","JNJ","V","UNH","XOM","WMT","MA","HD","CVX","MRK",
    "ABBV","LLY","PFE","KO","PEP","AVGO","COST","AMD","NFLX","DIS",
]

EU_STOCKS = [
    "ASML.AS","SAP.DE","LVMH.PA","TTE.PA","SIE.DE","AIR.PA",
    "MC.PA","OR.PA","SAN.MC","IBE.MC","ENEL.MI","ENI.MI",
    "BAS.DE","BMW.DE","VOW3.DE","ADS.DE","DTE.DE","BAYN.DE",
]

TOP_ETFS = [
    "SPY","QQQ","IWM","VTI","VOO","EEM","GLD","SLV","USO",
    "TLT","HYG","LQD","XLK","XLF","XLE","XLV","ARKK","SQQQ",
    "BITO","VNQ","IAU","IEMG","EFA","AGG","BND",
]

# ─── ENDPOINTS ────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "FINANSAL TERMINAL API v2.0 ONLINE", "time": datetime.utcnow().isoformat()}

@app.get("/api/indices")
async def get_indices():
    cached = cache_get("indices")
    if cached:
        return cached
    
    result = {}
    tickers = list(INDICES.values())
    try:
        data = yf.download(tickers, period="2d", interval="1d", progress=False, group_by="ticker")
        for name, symbol in INDICES.items():
            try:
                if len(tickers) > 1:
                    hist = data[symbol] if symbol in data.columns.get_level_values(0) else None
                else:
                    hist = data
                if hist is not None and not hist.empty:
                    close_vals = hist["Close"].dropna()
                    if len(close_vals) >= 2:
                        prev = float(close_vals.iloc[-2])
                        curr = float(close_vals.iloc[-1])
                        change_pct = ((curr - prev) / prev) * 100
                        result[name] = {
                            "symbol": symbol,
                            "price": round(curr, 4),
                            "change_pct": round(change_pct, 2),
                            "prev": round(prev, 4),
                        }
            except Exception:
                pass
    except Exception as e:
        pass
    
    # Fallback individual fetch if batch failed
    if not result:
        for name, symbol in list(INDICES.items())[:8]:
            try:
                t = yf.Ticker(symbol)
                hist = t.history(period="2d")
                if len(hist) >= 2:
                    prev = float(hist["Close"].iloc[-2])
                    curr = float(hist["Close"].iloc[-1])
                    result[name] = {
                        "symbol": symbol,
                        "price": round(curr, 4),
                        "change_pct": round(((curr - prev) / prev) * 100, 2),
                        "prev": round(prev, 4),
                    }
            except Exception:
                pass
    
    cache_set("indices", result)
    return result

@app.get("/api/stock/{symbol}")
async def get_stock(symbol: str, period: str = "1y"):
    symbol = symbol.upper()
    cache_key = f"stock_{symbol}_{period}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period=period)
        info = t.info
        
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"No data for {symbol}")
        
        hist.index = hist.index.tz_localize(None) if hist.index.tzinfo else hist.index
        
        ohlcv = []
        for dt, row in hist.iterrows():
            ohlcv.append({
                "date": dt.strftime("%Y-%m-%d"),
                "open": round(float(row["Open"]), 4),
                "high": round(float(row["High"]), 4),
                "low": round(float(row["Low"]), 4),
                "close": round(float(row["Close"]), 4),
                "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else 0,
            })
        
        result = {
            "symbol": symbol,
            "name": info.get("longName", info.get("shortName", symbol)),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", None),
            "eps": info.get("trailingEps", None),
            "dividend_yield": info.get("dividendYield", None),
            "52w_high": info.get("fiftyTwoWeekHigh", None),
            "52w_low": info.get("fiftyTwoWeekLow", None),
            "avg_volume": info.get("averageVolume", None),
            "beta": info.get("beta", None),
            "description": info.get("longBusinessSummary", "")[:500],
            "currency": info.get("currency", "USD"),
            "exchange": info.get("exchange", ""),
            "ohlcv": ohlcv,
            "current_price": round(float(hist["Close"].iloc[-1]), 4),
            "prev_close": round(float(hist["Close"].iloc[-2]), 4) if len(hist) > 1 else None,
        }
        
        if result["prev_close"]:
            result["change_pct"] = round(
                (result["current_price"] - result["prev_close"]) / result["prev_close"] * 100, 2
            )
        
        cache_set(cache_key, result)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market/{market}")
async def get_market_stocks(market: str):
    market = market.upper()
    cache_key = f"market_{market}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    if market == "BIST":
        symbols = BIST_STOCKS
    elif market == "US":
        symbols = US_STOCKS
    elif market == "EU":
        symbols = EU_STOCKS
    else:
        raise HTTPException(status_code=400, detail="Market must be BIST, US, or EU")
    
    result = []
    try:
        data = yf.download(symbols, period="2d", interval="1d", progress=False, group_by="ticker")
        for sym in symbols:
            try:
                if len(symbols) > 1:
                    hist = data[sym] if sym in data.columns.get_level_values(0) else None
                else:
                    hist = data
                if hist is not None and not hist.empty:
                    closes = hist["Close"].dropna()
                    volumes = hist["Volume"].dropna()
                    if len(closes) >= 2:
                        prev = float(closes.iloc[-2])
                        curr = float(closes.iloc[-1])
                        chg = ((curr - prev) / prev) * 100
                        vol = int(volumes.iloc[-1]) if len(volumes) > 0 else 0
                        result.append({
                            "symbol": sym,
                            "price": round(curr, 2),
                            "change_pct": round(chg, 2),
                            "volume": vol,
                            "prev_close": round(prev, 2),
                        })
            except Exception:
                pass
    except Exception:
        pass
    
    result.sort(key=lambda x: abs(x["change_pct"]), reverse=True)
    cache_set(cache_key, result)
    return result

@app.get("/api/etfs")
async def get_etfs():
    cache_key = "etfs_data"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    result = []
    try:
        data = yf.download(TOP_ETFS, period="1y", interval="1d", progress=False, group_by="ticker")
        for sym in TOP_ETFS:
            try:
                hist = data[sym] if sym in data.columns.get_level_values(0) else None
                if hist is not None and not hist.empty:
                    closes = hist["Close"].dropna()
                    volumes = hist["Volume"].dropna()
                    if len(closes) >= 2:
                        prev = float(closes.iloc[-2])
                        curr = float(closes.iloc[-1])
                        start = float(closes.iloc[0])
                        ytd_chg = ((curr - start) / start) * 100
                        chg = ((curr - prev) / prev) * 100
                        
                        t = yf.Ticker(sym)
                        info = t.info
                        
                        result.append({
                            "symbol": sym,
                            "name": info.get("longName", info.get("shortName", sym)),
                            "price": round(curr, 2),
                            "change_pct": round(chg, 2),
                            "ytd_pct": round(ytd_chg, 2),
                            "volume": int(volumes.iloc[-1]) if len(volumes) > 0 else 0,
                            "aum": info.get("totalAssets", 0),
                            "expense_ratio": info.get("annualReportExpenseRatio", None),
                            "category": info.get("category", "N/A"),
                        })
            except Exception:
                pass
    except Exception:
        pass
    
    cache_set(cache_key, result)
    return result

@app.get("/api/etf/{symbol}")
async def get_etf_detail(symbol: str):
    symbol = symbol.upper()
    cache_key = f"etf_{symbol}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    try:
        t = yf.Ticker(symbol)
        info = t.info
        hist = t.history(period="1y")
        hist.index = hist.index.tz_localize(None) if hist.index.tzinfo else hist.index
        
        ohlcv = []
        for dt, row in hist.iterrows():
            ohlcv.append({
                "date": dt.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else 0,
            })
        
        holdings = []
        try:
            h = t.funds_data.top_holdings if hasattr(t, "funds_data") else {}
            if hasattr(h, "to_dict"):
                holdings = h.reset_index().to_dict("records")[:10]
        except Exception:
            pass
        
        result = {
            "symbol": symbol,
            "name": info.get("longName", symbol),
            "category": info.get("category", "N/A"),
            "aum": info.get("totalAssets", 0),
            "expense_ratio": info.get("annualReportExpenseRatio", None),
            "inception_date": info.get("fundInceptionDate", None),
            "description": info.get("longBusinessSummary", "")[:600],
            "ohlcv": ohlcv,
            "holdings": holdings,
            "ytd_pct": 0,
            "1y_pct": 0,
        }
        
        if len(ohlcv) > 1:
            start_price = ohlcv[0]["close"]
            curr_price = ohlcv[-1]["close"]
            result["ytd_pct"] = round(((curr_price - start_price) / start_price) * 100, 2)
            result["1y_pct"] = result["ytd_pct"]
        
        cache_set(cache_key, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news")
async def get_news(query: str = "stock market finance", limit: int = 20):
    cache_key = f"news_{query}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    articles = []
    
    # Use yfinance news
    try:
        symbols_to_check = ["SPY", "THYAO.IS", "^GSPC"]
        for sym in symbols_to_check:
            t = yf.Ticker(sym)
            news = t.news
            if news:
                for item in news[:8]:
                    articles.append({
                        "title": item.get("title", ""),
                        "publisher": item.get("publisher", ""),
                        "link": item.get("link", ""),
                        "published": datetime.fromtimestamp(
                            item.get("providerPublishTime", 0)
                        ).strftime("%Y-%m-%d %H:%M") if item.get("providerPublishTime") else "",
                        "symbol": sym,
                    })
    except Exception:
        pass
    
    # Deduplicate by title
    seen = set()
    unique = []
    for a in articles:
        if a["title"] not in seen and a["title"]:
            seen.add(a["title"])
            unique.append(a)
    
    result = unique[:limit]
    cache_set(cache_key, result)
    return result

@app.get("/api/news/stock/{symbol}")
async def get_stock_news(symbol: str):
    symbol = symbol.upper()
    try:
        t = yf.Ticker(symbol)
        news = t.news or []
        result = []
        for item in news[:15]:
            result.append({
                "title": item.get("title", ""),
                "publisher": item.get("publisher", ""),
                "link": item.get("link", ""),
                "published": datetime.fromtimestamp(
                    item.get("providerPublishTime", 0)
                ).strftime("%Y-%m-%d %H:%M") if item.get("providerPublishTime") else "",
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ships")
async def get_ships(lat: float = 41.0, lon: float = 29.0, radius: int = 200):
    """Fetch vessel data from AISHub (free tier) or fallback to sample data"""
    cache_key = f"ships_{lat}_{lon}_{radius}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    vessels = []
    
    # Try AISHub free API
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            url = f"https://data.aishub.net/ws.php?username=AH_ANONYMOUS_USER&format=1&output=json&compress=0&lat={lat}&lon={lon}&radius={radius}"
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and len(data) > 1:
                    for vessel in data[1]:
                        vessels.append({
                            "mmsi": vessel.get("MMSI", ""),
                            "name": vessel.get("NAME", "Unknown"),
                            "lat": vessel.get("LATITUDE", 0),
                            "lon": vessel.get("LONGITUDE", 0),
                            "speed": vessel.get("SOG", 0),
                            "course": vessel.get("COG", 0),
                            "type": vessel.get("TYPE", ""),
                            "destination": vessel.get("DEST", ""),
                            "flag": vessel.get("FLAG", ""),
                            "length": vessel.get("LENGTH", 0),
                            "status": vessel.get("STATUS", ""),
                            "timestamp": vessel.get("TIME", ""),
                        })
    except Exception:
        pass
    
    # Try OpenSea Map / VesselFinder fallback
    if not vessels:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                url = f"https://maptiles.marinetraffic.com/ais/getData?minlat={lat-5}&maxlat={lat+5}&minlon={lon-10}&maxlon={lon+10}&zoom=6"
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    for v in data.get("data", [])[:50]:
                        vessels.append({
                            "mmsi": v.get("mmsi", ""),
                            "name": v.get("shipname", "Unknown"),
                            "lat": float(v.get("lat", 0)) / 600000,
                            "lon": float(v.get("lon", 0)) / 600000,
                            "speed": float(v.get("speed", 0)) / 10,
                            "course": float(v.get("course", 0)) / 10,
                            "type": v.get("shiptype", ""),
                            "destination": v.get("destination", ""),
                            "flag": "",
                            "length": 0,
                            "status": "",
                            "timestamp": "",
                        })
        except Exception:
            pass
    
    result = {"vessels": vessels[:100], "count": len(vessels), "center": {"lat": lat, "lon": lon}}
    cache_set(cache_key, result)
    return result

@app.get("/api/planes")
async def get_planes(lat: float = 41.0, lon: float = 29.0, radius: float = 3.0):
    """Fetch cargo planes from OpenSky Network (free, no key needed)"""
    cache_key = f"planes_{lat}_{lon}_{radius}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    planes = []
    try:
        lamin = lat - radius
        lamax = lat + radius
        lomin = lon - radius * 1.5
        lomax = lon + radius * 1.5
        
        async with httpx.AsyncClient(timeout=15) as client:
            url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                states = data.get("states", []) or []
                for s in states[:100]:
                    if s and len(s) >= 17:
                        planes.append({
                            "icao24": s[0] or "",
                            "callsign": (s[1] or "").strip(),
                            "origin_country": s[2] or "",
                            "lon": s[5],
                            "lat": s[6],
                            "altitude": round(s[7], 0) if s[7] else 0,
                            "on_ground": s[8],
                            "velocity": round(s[9], 0) if s[9] else 0,
                            "heading": round(s[10], 0) if s[10] else 0,
                            "vertical_rate": s[11],
                            "squawk": s[14] or "",
                        })
    except Exception as e:
        pass
    
    result = {"planes": planes, "count": len(planes), "center": {"lat": lat, "lon": lon}}
    cache_set(cache_key, result)
    return result

@app.get("/api/macro")
async def get_macro():
    """Key macroeconomic indicators via yfinance"""
    cache_key = "macro"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    macro_symbols = {
        "USD_INDEX": "DX-Y.NYB",
        "US10Y": "^TNX",
        "US2Y": "^IRX",
        "GOLD": "GC=F",
        "SILVER": "SI=F",
        "OIL_WTI": "CL=F",
        "OIL_BRENT": "BZ=F",
        "NATGAS": "NG=F",
        "COPPER": "HG=F",
        "EUR_USD": "EURUSD=X",
        "GBP_USD": "GBPUSD=X",
        "USD_JPY": "JPY=X",
        "USD_TRY": "USDTRY=X",
        "USD_CHF": "CHF=X",
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
    }
    
    result = {}
    for name, sym in macro_symbols.items():
        try:
            t = yf.Ticker(sym)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                prev = float(hist["Close"].iloc[-2])
                curr = float(hist["Close"].iloc[-1])
                result[name] = {
                    "symbol": sym,
                    "price": round(curr, 4),
                    "change_pct": round(((curr - prev) / prev) * 100, 2),
                }
        except Exception:
            pass
    
    cache_set(cache_key, result)
    return result

@app.get("/api/search")
async def search_symbol(q: str):
    try:
        t = yf.Ticker(q)
        info = t.info
        if info and info.get("symbol"):
            return {
                "symbol": info.get("symbol", q),
                "name": info.get("longName", info.get("shortName", q)),
                "exchange": info.get("exchange", ""),
                "type": info.get("quoteType", ""),
                "currency": info.get("currency", ""),
            }
        return {"symbol": q, "name": q, "exchange": "", "type": "", "currency": ""}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/heatmap/{market}")
async def get_heatmap(market: str):
    market = market.upper()
    if market == "BIST":
        symbols = BIST_STOCKS
    elif market == "US":
        symbols = US_STOCKS
    elif market == "EU":
        symbols = EU_STOCKS
    else:
        symbols = US_STOCKS
    
    cache_key = f"heatmap_{market}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    result = []
    try:
        data = yf.download(symbols, period="2d", interval="1d", progress=False, group_by="ticker")
        for sym in symbols:
            try:
                hist = data[sym] if sym in data.columns.get_level_values(0) else None
                if hist is not None and not hist.empty:
                    closes = hist["Close"].dropna()
                    if len(closes) >= 2:
                        prev = float(closes.iloc[-2])
                        curr = float(closes.iloc[-1])
                        chg = ((curr - prev) / prev) * 100
                        result.append({"symbol": sym.replace(".IS","").replace(".AS","").replace(".DE","").replace(".PA",""), "full_symbol": sym, "change_pct": round(chg, 2)})
            except Exception:
                pass
    except Exception:
        pass
    
    cache_set(cache_key, result)
    return result
