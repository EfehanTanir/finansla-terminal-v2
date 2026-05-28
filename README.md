# 📊 FINANSAL TERMINAL v2.0

> A Bloomberg Terminal-style financial dashboard — stocks, ETFs, ships, cargo planes, and macro data.

![Dark Bloomberg-style UI](https://img.shields.io/badge/UI-Bloomberg%20Dark-ff6600?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-ff4b4b?style=flat-square)

---

## 🗂 PAGES

| Page | Description | Data Source |
|------|-------------|-------------|
| 🏠 Dashboard | Live indices, movers, news ticker | yFinance |
| 🇹🇷 BIST Stocks | 30 Istanbul stocks, charts, fundamentals | yFinance |
| 🇺🇸 US Stocks | NYSE/NASDAQ, screener, candlesticks | yFinance |
| 🇪🇺 EU Stocks | Euronext, Xetra, BME, Borsa Italiana | yFinance |
| 📈 ETF Tracker | 25 ETFs, YTD performance, AUM, ranking | yFinance |
| 🌍 Macro & FX | Forex, commodities, crypto, bonds | yFinance |
| 📰 News Feed | Financial headlines, stock-specific news | yFinance News |
| 🚢 Ship Tracker | AIS vessel positions, interactive map | AISHub (free) |
| ✈️ Cargo Planes | Live ADS-B flight tracking | OpenSky Network (free) |
| 🔥 Heatmap | Treemap or grid market performance | yFinance |
| 🔍 Stock Analyzer | RSI, MACD, Bollinger Bands, SMA signals | yFinance |

---

## 🚀 DEPLOY TO RAILWAY (Recommended)

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "FINANSAL TERMINAL v2.0"
git remote add origin https://github.com/YOUR_USERNAME/finansal-terminal.git
git push -u origin main
```

### Step 2 — Create Railway Project

1. Go to **[railway.app](https://railway.app)** → New Project
2. Select **Deploy from GitHub repo**
3. Choose your `finansal-terminal` repo
4. Railway auto-detects the `Dockerfile` ✓

### Step 3 — Configure Environment Variables

In Railway dashboard → Variables, add:

```
API_PORT=8000
STREAMLIT_PORT=8501
API_URL=http://localhost:8000
```

> **Important:** Railway exposes one port per service. The app runs both backend + frontend internally. Set the **exposed port** to `8501` in Railway settings so the Streamlit UI is what users see.

### Step 4 — Set Exposed Port

Railway → Settings → Networking → **Public Port: 8501**

### Step 5 — Deploy!

Railway builds the Docker image and deploys. Your terminal will be live at:
```
https://your-project.up.railway.app
```

---

## 💻 LOCAL DEVELOPMENT

### Prerequisites
- Python 3.11+
- pip

### Install & Run

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/finansal-terminal.git
cd finansal-terminal

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env

# Run (starts both backend + frontend)
chmod +x start.sh
./start.sh
```

Then open:
- **Terminal UI** → http://localhost:8501
- **API Docs** → http://localhost:8000/docs

### Run Separately (for development)

```bash
# Terminal 1 — Backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Frontend
API_URL=http://localhost:8000 streamlit run frontend/app.py
```

---

## 🔌 FREE APIs USED

| API | Purpose | Key Required? |
|-----|---------|---------------|
| **yFinance** | All stock/ETF/FX/crypto data | ❌ No |
| **AISHub** | Ship AIS positions | ❌ Anonymous tier free |
| **OpenSky Network** | Cargo plane ADS-B data | ❌ No |
| **yFinance News** | Financial news headlines | ❌ No |

### Improve AIS Ship Data (Optional)

Register free at [aishub.net](https://www.aishub.net) and add to `.env`:
```
AISHUB_USERNAME=your_username
```

---

## 📁 PROJECT STRUCTURE

```
finansal-terminal/
├── backend/
│   └── main.py              # FastAPI app — all API endpoints
├── frontend/
│   ├── app.py               # Streamlit entry point + navigation
│   ├── components/
│   │   └── shared.py        # Reusable UI components, chart helpers
│   └── pages/
│       ├── dashboard.py     # Main overview page
│       ├── bist.py          # BIST market page
│       ├── us_stocks.py     # US market page
│       ├── eu_stocks.py     # EU market page
│       ├── etfs.py          # ETF tracker page
│       ├── macro.py         # Macro & FX page
│       ├── news.py          # News feed page
│       ├── ships.py         # Ship tracker page
│       ├── planes.py        # Cargo plane tracker page
│       ├── heatmap.py       # Market heatmap page
│       └── analyzer.py      # Technical analysis page
├── .streamlit/
│   └── config.toml          # Streamlit theme config
├── Dockerfile               # Docker build file
├── railway.toml             # Railway deployment config
├── requirements.txt         # Python dependencies
├── start.sh                 # Startup script (backend + frontend)
├── .env.example             # Environment template
└── .gitignore
```

---

## 🔧 API ENDPOINTS

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/indices` | All global indices |
| GET | `/api/stock/{symbol}?period=1y` | Stock OHLCV + info |
| GET | `/api/market/{market}` | Market board (BIST/US/EU) |
| GET | `/api/etfs` | All ETF data |
| GET | `/api/etf/{symbol}` | ETF detail |
| GET | `/api/news?query=...` | News headlines |
| GET | `/api/news/stock/{symbol}` | Stock-specific news |
| GET | `/api/macro` | FX, commodities, crypto |
| GET | `/api/ships?lat=&lon=&radius=` | AIS vessel positions |
| GET | `/api/planes?lat=&lon=&radius=` | OpenSky flight data |
| GET | `/api/heatmap/{market}` | Market heatmap data |
| GET | `/api/search?q=` | Symbol search |

Full interactive docs at: `http://localhost:8000/docs`

---

## 🎨 TECH STACK

- **Backend:** FastAPI + uvicorn (async, fast)
- **Frontend:** Streamlit (Bloomberg dark theme)
- **Charts:** Plotly (candlestick, treemap, maps)
- **Data:** yFinance, AISHub, OpenSky Network
- **Deploy:** Railway + Docker
- **Font:** IBM Plex Mono (terminal aesthetic)

---

## 📈 TRACKED ASSETS

- **BIST:** 30 stocks (THYAO, GARAN, AKBNK, EREGL, ASELS...)
- **US:** 28 stocks (AAPL, MSFT, NVDA, GOOGL, TSLA...)
- **EU:** 18 stocks (ASML, SAP, LVMH, Siemens, Airbus...)
- **ETFs:** 25 funds (SPY, QQQ, GLD, TLT, ARKK...)
- **Indices:** 16 (BIST100, SPX, DAX, CAC40, FTSE, NIKKEI...)
- **FX:** 6 pairs (EUR/USD, USD/TRY, GBP/USD...)
- **Commodities:** Gold, Silver, WTI, Brent, NatGas, Copper
- **Crypto:** BTC, ETH

---

*Built with ❤️ — FINANSAL TERMINAL v2.0*
