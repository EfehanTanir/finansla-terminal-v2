"""
Main Streamlit application - Bloomberg Terminal V2 Replica
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from config import DATA_PROVIDERS
from utils.api_clients import StockDataClient
from utils.helpers import format_currency, format_percent, get_change_color

# Page configuration
st.set_page_config(
    page_title="Finansla Terminal V2",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Bloomberg-style theme
st.markdown("""
<style>
    /* Main theme */
    :root {
        --primary-color: #00D084;
        --bg-color: #0f1419;
        --secondary-bg: #1a1f26;
        --text-color: #E0E0E0;
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #00D084 !important;
        font-weight: 700;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1f26;
    }
    
    /* Cards */
    [data-testid="stMetricValue"] {
        color: #00D084;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_provider' not in st.session_state:
    st.session_state.data_provider = "yfinance"

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []


def main():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Finansla Terminal V2")
        st.caption("Professional Financial Dashboard - Bloomberg Terminal Replica")
    
    with col2:
        st.write(f"")
        st.caption(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    st.divider()
    
    # Sidebar - Data Source Selection
    st.sidebar.title("⚙️ Configuration")
    st.sidebar.markdown("### 📡 Data Source")
    st.sidebar.caption("Select where to fetch stock prices from")
    
    selected_provider = st.sidebar.selectbox(
        "Choose Data Provider:",
        options=list(DATA_PROVIDERS.keys()),
        format_func=lambda x: DATA_PROVIDERS[x],
        key="provider_select",
        help="Different providers have different coverage and update frequencies"
    )
    
    st.session_state.data_provider = selected_provider
    
    # Provider info box
    provider_info = {
        "yfinance": {
            "icon": "🟢",
            "description": "Yahoo Finance - Free, no API key needed. Best for US and major markets.",
            "delay": "~15-20 min delay",
            "coverage": "US, Europe, Emerging Markets",
            "pros": ["No key required", "Great historical data", "Reliable"]
        },
        "finnhub": {
            "icon": "🔵",
            "description": "Finnhub - Real-time data. Requires API key. Covers US, Europe, Turkey.",
            "delay": "Real-time (~1 min)",
            "coverage": "US, Europe, Turkey, Emerging Markets",
            "pros": ["Real-time data", "Turkish market support", "Company news & sentiment"]
        },
        "alpha_vantage": {
            "icon": "🟡",
            "description": "Alpha Vantage - Premium technical analysis. Requires API key.",
            "delay": "Intraday (~5 min)",
            "coverage": "US, some Europe",
            "pros": ["Advanced technicals", "FX data", "Crypto support"]
        }
    }
    
    info = provider_info[selected_provider]
    
    with st.sidebar.expander(f"{info['icon']} {selected_provider.upper()} Info"):
        st.write(info['description'])
        st.write(f"**Update Delay:** {info['delay']}")
        st.write(f"**Market Coverage:** {info['coverage']}")
        st.markdown("**Advantages:**")
        for pro in info['pros']:
            st.write(f"✅ {pro}")
    
    # API Key check
    if selected_provider == "finnhub":
        st.sidebar.warning("⚠️ Finnhub requires an API key. Set FINNHUB_API_KEY in .env file.")
        st.sidebar.markdown("[Get Finnhub API Key →](https://finnhub.io/dashboard/api-token)")
    elif selected_provider == "alpha_vantage":
        st.sidebar.warning("⚠️ Alpha Vantage requires an API key. Set ALPHA_VANTAGE_API_KEY in .env file.")
        st.sidebar.markdown("[Get Alpha Vantage API Key →](https://www.alphavantage.co/api/)")
    
    st.sidebar.divider()
    
    # Quick test
    st.sidebar.markdown("### 🧪 Quick Test")
    test_symbol = st.sidebar.text_input(
        "Test ticker symbol:",
        value="AAPL",
        help="Enter a ticker to test the current data provider"
    )
    
    if st.sidebar.button("🔄 Fetch Data", use_container_width=True):
        with st.spinner(f"Fetching {test_symbol} from {selected_provider}..."):
            try:
                client = StockDataClient(selected_provider)
                quote = client.get_quote(test_symbol)
                
                if quote:
                    col1, col2, col3, col4 = st.sidebar.columns(4)
                    with col1:
                        st.metric("Price", format_currency(quote['price']))
                    with col2:
                        change_color = get_change_color(quote['change'])
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
                        st.caption(f"Provider: {quote['provider']}")
                    
                    st.sidebar.success(f"✅ {test_symbol} data fetched successfully!")
                else:
                    st.sidebar.error(f"❌ Could not fetch data for {test_symbol}")
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)}")
    
    st.sidebar.divider()
    st.sidebar.markdown("### 📚 Navigation")
    st.sidebar.info(
        "Use the pages menu (☰) to navigate to different sections:\n\n"
        "- 🇺🇸 US Stocks\n"
        "- 🇹🇷 Turkish Stocks\n"
        "- 🇪🇺 European Stocks\n"
        "- 📈 ETFs\n"
        "- 🚢 Shipping Tracker\n"
        "- ✈️ Cargo Planes\n"
        "- 💹 Trade Data\n"
        "- 📰 News & Sentiment\n"
        "- ⭐ Watchlist"
    )
    
    # Main content
    st.markdown("""
    # Welcome to Finansla Terminal V2 🚀
    
    Your professional financial dashboard with real-time market data, technical analysis, and global insights.
    
    ## 🎯 Key Features:
    
    - **Multi-Market Support**: US, Turkish (Borsa Istanbul), and European stock exchanges
    - **Flexible Data Sources**: Switch between YFinance, Finnhub, and Alpha Vantage
    - **Real-time Updates**: Live quotes, charts, and news feeds
    - **Sentiment Analysis**: AI-powered market sentiment with color coding
    - **Global Trade Data**: Import/export statistics, trade partners, trends
    - **Shipping Intelligence**: Live vessel tracking and cargo monitoring
    - **Advanced Analytics**: Technical indicators, ETF analysis, portfolio tracking
    
    ## 🚀 Quick Start:
    
    1. **Select a Data Provider** in the sidebar (left) - YFinance is recommended for beginners
    2. **Choose a Market Page** from the navigation menu
    3. **Search for Stocks** or browse market indices
    4. **Add to Watchlist** to track your favorite stocks
    5. **Check News & Sentiment** for latest market insights
    
    ## 💡 Pro Tips:
    
    - **YFinance** is free and requires no API key - great for testing!
    - **Finnhub** provides real-time data and covers Turkish markets
    - **Combine providers** for the best coverage (use sidebar test feature)
    - Check **Market Status** to know when exchanges are open
    
    ---
    
    ### Provider Comparison:
    """)
    
    # Provider comparison table
    comparison_data = {
        "Feature": ["API Key Required", "Real-Time Data", "US Markets", "European Markets", "Turkish Markets", "News", "Sentiment", "Historical Data"],
        "YFinance": ["❌ No", "⚠️ Delayed", "✅ Yes", "✅ Yes", "⚠️ Limited", "✅ Yes", "❌ No", "✅ Excellent"],
        "Finnhub": ["✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Good"],
        "Alpha Vantage": ["✅ Yes", "✅ Yes", "✅ Yes", "⚠️ Limited", "❌ No", "❌ No", "❌ No", "✅ Good"]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.table(comparison_df)
    
    st.markdown("""
    ---
    
    ### 🔗 Resources:
    
    - [YFinance Documentation](https://yfinance.readthedocs.io/)
    - [Finnhub API Docs](https://finnhub.io/docs/api/)
    - [Alpha Vantage API Docs](https://www.alphavantage.co/documentation/)
    - [Streamlit Documentation](https://docs.streamlit.io/)
    
    ### 📝 Environment Setup:
    
    Create a `.env` file in the root directory with your API keys:
    
    ```
    FINNHUB_API_KEY=your_key_here
    ALPHA_VANTAGE_API_KEY=your_key_here
    ```
    
    ---
    
    **Made with ❤️ using Streamlit, Python, and open-source APIs**
    """)


if __name__ == "__main__":
    main()
