"""
News & Sentiment Analysis Page
"""

import streamlit as st
from datetime import datetime, timedelta
from utils.api_clients import StockDataClient
from utils.sentiment import analyze_sentiment, get_sentiment_emoji, get_sentiment_color

st.set_page_config(page_title="News & Sentiment", page_icon="📰", layout="wide")

st.title("📰 Financial News & Sentiment Analysis")
st.caption("Real-time news with AI-powered sentiment analysis")

data_provider = st.session_state.get('data_provider', 'yfinance')
client = StockDataClient(data_provider)

st.info(f"📡 Using **{data_provider.upper()}** as data source")

tab1, tab2, tab3 = st.tabs(["🌍 Market News", "🔍 Stock News", "📊 Sentiment Analysis"])

with tab1:
    st.subheader("Market-Wide News")
    st.info("Major financial news and market movements")
    
    news_items = [
        {
            "headline": "Tech Stocks Rally on Strong Earnings Beat",
            "summary": "NVIDIA and other chip makers surge following positive guidance",
            "source": "Reuters",
            "time": "2 hours ago",
            "related_stocks": ["NVDA", "MSFT", "GOOGL"]
        },
        {
            "headline": "Market Correction Fears Spark Selloff",
            "summary": "Major indices decline as inflation concerns resurface",
            "source": "Bloomberg",
            "time": "5 hours ago",
            "related_stocks": ["SPY", "QQQ", "IWM"]
        },
        {
            "headline": "Oil Prices Hit 6-Month High on Supply Constraints",
            "summary": "Energy sector benefits from geopolitical tensions",
            "source": "CNBC",
            "time": "8 hours ago",
            "related_stocks": ["XOM", "CVX", "COP"]
        }
    ]
    
    for news in news_items:
        sentiment, color = analyze_sentiment(news['headline'])
        emoji = get_sentiment_emoji(sentiment)
        
        st.markdown(f"### {emoji} {news['headline']}")
        st.write(news['summary'])
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.caption(f"📍 {news['source']}")
        with col2:
            st.caption(f"⏰ {news['time']}")
        with col3:
            st.caption(f"Sentiment: **{sentiment.upper()}**")
        with col4:
            related = " | ".join(news['related_stocks'])
            st.caption(f"Stocks: {related}")
        
        st.divider()

with tab2:
    st.subheader("Search Stock News")
    
    search_symbol = st.text_input(
        "Enter ticker:",
        value="AAPL",
        placeholder="e.g., AAPL, MSFT, NVDA"
    ).upper()
    
    limit = st.slider("Number of articles:", 5, 20, 10)
    
    if search_symbol:
        with st.spinner(f"Loading news for {search_symbol}..."):
            news_items = client.get_news(search_symbol, limit=limit)
            
            if news_items:
                for item in news_items:
                    headline = item.get('headline', item.get('title', 'N/A'))
                    summary = item.get('summary', '')[:200] if item.get('summary') else 'N/A'
                    
                    sentiment, color = analyze_sentiment(headline)
                    emoji = get_sentiment_emoji(sentiment)
                    
                    st.markdown(f"### {emoji} {headline}")
                    st.write(f"{summary}...")
                    st.caption(f"Sentiment: **{sentiment.upper()}** | Source: {item.get('source', 'N/A')}")
                    st.divider()
            else:
                st.info(f"No news available for {search_symbol}")

with tab3:
    st.subheader("Sentiment Analysis Dashboard")
    
    sentiment_stocks = st.multiselect(
        "Select stocks to analyze:",
        ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL"],
        default=["AAPL", "MSFT"]
    )
    
    if sentiment_stocks:
        col1, col2, col3 = st.columns(3)
        
        for idx, stock in enumerate(sentiment_stocks):
            news_items = client.get_news(stock, limit=5)
            
            if news_items:
                sentiments = []
                for item in news_items:
                    headline = item.get('headline', item.get('title', ''))
                    sentiment, _ = analyze_sentiment(headline)
                    sentiments.append(sentiment)
                
                positive_count = sentiments.count('positive')
                negative_count = sentiments.count('negative')
                neutral_count = sentiments.count('neutral')
                
                cols = [col1, col2, col3]
                with cols[idx % 3]:
                    st.metric(f"{stock} Sentiment", f"+{positive_count}/-{negative_count}")
                    
                    st.write(f"🟢 Positive: {positive_count}")
                    st.write(f"🔴 Negative: {negative_count}")
                    st.write(f"⭕ Neutral: {neutral_count}")
