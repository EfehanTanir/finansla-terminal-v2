# Finansla Terminal V2 - Bloomberg Terminal Replica

📊 Professional financial dashboard with multi-source stock data, real-time updates, and global market insights.

## Features

### 📈 Stock Market Coverage
- **US Markets** (NASDAQ, NYSE) - Apple, Microsoft, Google, Tesla, NVDA, etc.
- **Turkish Markets** (Borsa Istanbul/BIST) - Turkish blue-chips and indices
- **European Markets** (Euronext, LSE, Xetra, SIX) - Major European exchanges

### 🔄 Flexible Data Sources
- **YFinance** - Free, no API key, great for testing
- **Finnhub** - Real-time data, Turkish market support, news & sentiment
- **Alpha Vantage** - Advanced technicals, FX, crypto support

### 📰 News & Sentiment
- Real-time financial news aggregation
- AI-powered sentiment analysis (Green/Red color coding)
- Stock-specific news feeds
- Trade and import/export news

### 🚢 Global Trade & Shipping
- Country-level import/export statistics
- International trade partners analysis
- Live ship tracking (vessel positions, cargo info)
- Trade data from UN Comtrade, World Bank, OECD

### 📊 Advanced Analytics
- Technical indicators and charting
- ETF analysis and holdings breakdown
- Price comparisons and historical data
- Market sentiment indicators

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/EfehanTanir/finansla-terminal-v2.git
cd finansla-terminal-v2
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys (optional for YFinance)
```

5. **Run the application**
```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

## Configuration

### API Keys (Optional)

YFinance requires no API key. For other providers:

**Finnhub** (Recommended for real-time + Turkish markets)
- Get key: https://finnhub.io/dashboard/api-token
- Add to `.env`: `FINNHUB_API_KEY=your_key`

**Alpha Vantage** (For advanced technicals)
- Get key: https://www.alphavantage.co/api/
- Add to `.env`: `ALPHA_VANTAGE_API_KEY=your_key`

### Data Provider Selection

The main page includes an interactive **Data Source** selector in the sidebar:
1. Choose your preferred provider (YFinance, Finnhub, or Alpha Vantage)
2. View provider information and capabilities
3. Use the "Quick Test" feature to verify it works
4. All pages will automatically use the selected provider

## Usage

### Pages

1. **🏠 Home** - Overview, data provider selection, provider comparison
2. **🇺🇸 US Stocks** - NASDAQ, NYSE, S&P 500 companies
3. **🇹🇷 Turkish Stocks** - Borsa Istanbul, BIST 100, local companies
4. **🇪🇺 European Stocks** - Euronext, LSE, DAX, CAC 40, etc.
5. **📈 ETFs** - ETF performance, holdings, allocations
6. **🚢 Shipping Tracker** - Live vessel tracking, cargo information
7. **✈️ Cargo Planes** - Cargo flight tracking (if APIs available)
8. **💹 Trade Data** - International imports/exports, trade partners
9. **📰 News & Sentiment** - News feeds with sentiment analysis
10. **⭐ Watchlist** - Personal portfolio tracking

### Search Functionality

Each market page includes:
- Stock search by ticker or company name
- Real-time price quotes (using selected provider)
- Technical charts and indicators
- Company fundamentals
- Historical data

### Sentiment Analysis

News items are color-coded:
- 🟢 **Green** - Positive sentiment
- 🔴 **Red** - Negative sentiment
- ⚪ **Neutral** - No clear sentiment

## Deployment

### Railway Deployment

1. **Create Railway account** - https://railway.app

2. **Connect GitHub repository**
   - Connect your GitHub account to Railway
   - Select this repository

3. **Set Environment Variables**
   - In Railway dashboard, add environment variables:
   ```
   FINNHUB_API_KEY=your_key
   ALPHA_VANTAGE_API_KEY=your_key
   ```

4. **Deploy**
   - Railway auto-deploys on push to main
   - App runs on: `https://your-railway-app.up.railway.app`

### Local Docker Deployment

```bash
# Build image
docker build -t finansla-terminal .

# Run container
docker run -p 8501:8501 -e FINNHUB_API_KEY=your_key finansla-terminal
```

## Project Structure

```
finansla-terminal-v2/
├── main.py                 # Streamlit entry point
├── config.py              # Configuration and constants
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── .env.example          # Environment variables template
├── .streamlit/
│   └── config.toml       # Streamlit theme config
├── utils/
│   ├── __init__.py
│   ├── api_clients.py    # StockDataClient, NewsClient
│   ├── cache.py          # Caching utilities
│   ├── charts.py         # Plotly visualizations
│   ├── sentiment.py      # Sentiment analysis
│   └── helpers.py        # Helper functions
└── pages/
    ├── 1_🇺🇸_US_Stocks.py
    ├── 2_🇹🇷_Turkish_Stocks.py
    ├── 3_🇪🇺_European_Stocks.py
    ├── 4_📈_ETFs.py
    ├── 5_🚢_Shipping_Tracker.py
    ├── 6_✈️_Cargo_Planes.py
    ├── 7_💹_Trade_Data.py
    ├── 8_📰_News_Sentiment.py
    └── 9_⭐_Watchlist.py
```

## Data Providers Comparison

| Feature | YFinance | Finnhub | Alpha Vantage |
|---------|----------|---------|---------------|
| API Key Required | ❌ No | ✅ Yes | ✅ Yes |
| Real-Time Data | ⚠️ Delayed (~20 min) | ✅ Yes | ✅ Yes |
| US Markets | ✅ Yes | ✅ Yes | ✅ Yes |
| European Markets | ✅ Yes | ✅ Yes | ⚠️ Limited |
| Turkish Markets | ⚠️ Limited | ✅ Yes | ❌ No |
| News | ✅ Yes | ✅ Yes | ❌ No |
| Sentiment | ❌ No | ✅ Yes | ❌ No |
| Historical Data | ✅ Excellent | ✅ Good | ✅ Good |
| Free Tier | ✅ Unlimited | ✅ 60 calls/min | ✅ 5 calls/min |

## Technologies Used

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Plotly Express
- **APIs**: YFinance, Finnhub, Alpha Vantage, UN Comtrade, World Bank
- **Sentiment**: TextBlob, custom NLP
- **Caching**: Streamlit cache decorators
- **Deployment**: Railway, Docker

## API Rate Limits

- **YFinance**: No official limit (practical: ~200 calls/min)
- **Finnhub**: 60 API calls per minute (free tier)
- **Alpha Vantage**: 5 calls per minute (free tier)
- **UN Comtrade**: 100 calls per hour (free tier)
- **World Bank**: No official limit

## Troubleshooting

### "API Key not configured"
Make sure to:
1. Create a `.env` file in the root directory
2. Add `FINNHUB_API_KEY=your_key` and/or `ALPHA_VANTAGE_API_KEY=your_key`
3. Restart the Streamlit app

### "Turkish stocks not showing"
Turkish stocks require Finnhub API key. Use tickers with `.IS` suffix (e.g., `AKBNK.IS`).

### "Slow data loading"
1. Check internet connection
2. Try switching to YFinance (doesn't require API calls)
3. Check API rate limits
4. Clear cache: `streamlit cache clear`

### "Data not updating"
Streamlit caches data for 5 minutes. Wait 5 minutes or restart the app for fresh data.

## Contributing

Contributions are welcome! Feel free to:
- Add new pages
- Improve existing features
- Add more data providers
- Enhance sentiment analysis
- Report bugs

## License

MIT License - Feel free to use this for personal or commercial projects.

## Support

- 📖 [Streamlit Docs](https://docs.streamlit.io/)
- 📚 [Finnhub API](https://finnhub.io/docs/api/)
- 🔍 [YFinance Docs](https://yfinance.readthedocs.io/)
- 🚀 [Railway Docs](https://docs.railway.app/)

## Roadmap

- [ ] Add WebSocket support for real-time updates
- [ ] Implement advanced portfolio optimization
- [ ] Add ML-based stock prediction
- [ ] Integrate crypto markets
- [ ] Add trading bot framework
- [ ] Implement custom alerts
- [ ] Add dark mode toggle
- [ ] Mobile app version

---

Made with ❤️ using Python, Streamlit, and open-source APIs.

**Now with multi-source data provider selection! 🚀**
