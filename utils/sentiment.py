"""
Sentiment analysis utilities
"""

import streamlit as st
from config import COLOR_GREEN, COLOR_RED, COLOR_NEUTRAL


def analyze_sentiment(text):
    """
    Simple sentiment analysis for news headlines
    Returns: 'positive', 'negative', or 'neutral'
    """
    positive_keywords = [
        'gain', 'rally', 'surge', 'jump', 'bull', 'profit', 'beat', 'soar',
        'strong', 'recovery', 'growth', 'boom', 'upgrade', 'outperform',
        'rise', 'climb', 'advance', 'peak', 'record', 'surge', 'bounce'
    ]
    
    negative_keywords = [
        'loss', 'fall', 'crash', 'plunge', 'bear', 'decline', 'miss', 'slump',
        'weak', 'correction', 'drop', 'downgrade', 'underperform', 'tumble',
        'sink', 'slide', 'cut', 'risk', 'fear', 'concern', 'sell-off'
    ]
    
    text_lower = text.lower()
    
    positive_score = sum(1 for word in positive_keywords if word in text_lower)
    negative_score = sum(1 for word in negative_keywords if word in text_lower)
    
    if positive_score > negative_score:
        return "positive", COLOR_GREEN
    elif negative_score > positive_score:
        return "negative", COLOR_RED
    else:
        return "neutral", COLOR_NEUTRAL


def get_sentiment_emoji(sentiment):
    """
    Get emoji for sentiment
    """
    if sentiment == "positive":
        return "🟢"
    elif sentiment == "negative":
        return "🔴"
    else:
        return "⚪"


def get_sentiment_color(sentiment):
    """
    Get color for sentiment
    """
    if sentiment == "positive":
        return COLOR_GREEN
    elif sentiment == "negative":
        return COLOR_RED
    else:
        return COLOR_NEUTRAL
