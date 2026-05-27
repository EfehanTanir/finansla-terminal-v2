"""
Chart and visualization utilities using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import COLOR_GREEN, COLOR_RED, BACKGROUND_DARK, TEXT_PRIMARY


def create_candlestick_chart(data, title="", height=600):
    """
    Create candlestick chart from OHLC data
    """
    if data.empty:
        return None
    
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color=COLOR_GREEN,
        decreasing_line_color=COLOR_RED
    )])
    
    fig.update_layout(
        title=title,
        yaxis_title="Price (USD)",
        template="plotly_dark",
        height=height,
        hovermode='x unified',
        paper_bgcolor=BACKGROUND_DARK,
        plot_bgcolor=BACKGROUND_DARK,
        font=dict(color=TEXT_PRIMARY),
    )
    
    return fig


def create_price_chart(data, title="", height=500):
    """
    Create line price chart
    """
    if data.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color=COLOR_GREEN, width=2),
        fill='tozeroy',
        fillcolor=f'rgba(0, 208, 132, 0.1)'
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title="Price (USD)",
        xaxis_title="Date",
        template="plotly_dark",
        height=height,
        hovermode='x unified',
        paper_bgcolor=BACKGROUND_DARK,
        plot_bgcolor=BACKGROUND_DARK,
        font=dict(color=TEXT_PRIMARY),
    )
    
    return fig


def create_volume_chart(data, title="Volume", height=300):
    """
    Create volume bar chart
    """
    if data.empty or 'Volume' not in data.columns:
        return None
    
    colors = [COLOR_GREEN if data['Close'].iloc[i] >= data['Open'].iloc[i] else COLOR_RED 
              for i in range(len(data))]
    
    fig = go.Figure(data=[
        go.Bar(
            x=data.index,
            y=data['Volume'],
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>Volume: %{y:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=title,
        yaxis_title="Volume",
        template="plotly_dark",
        height=height,
        hovermode='x',
        paper_bgcolor=BACKGROUND_DARK,
        plot_bgcolor=BACKGROUND_DARK,
        font=dict(color=TEXT_PRIMARY),
        showlegend=False
    )
    
    return fig


def create_comparison_chart(tickers_data, title="Price Comparison", height=500):
    """
    Create multi-ticker comparison chart
    
    Args:
        tickers_data: Dict of {ticker: price_series}
    """
    fig = go.Figure()
    
    for ticker, data in tickers_data.items():
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data.values,
            mode='lines',
            name=ticker,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title=title,
        yaxis_title="Price",
        xaxis_title="Date",
        template="plotly_dark",
        height=height,
        hovermode='x unified',
        paper_bgcolor=BACKGROUND_DARK,
        plot_bgcolor=BACKGROUND_DARK,
        font=dict(color=TEXT_PRIMARY),
    )
    
    return fig


def create_pie_chart(labels, values, title="", height=400):
    """
    Create pie chart for allocation/composition
    """
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hovertemplate='<b>%{label}</b><br>%{value}%<extra></extra>',
            marker=dict(line=dict(color=BACKGROUND_DARK, width=2))
        )
    ])
    
    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=height,
        paper_bgcolor=BACKGROUND_DARK,
        font=dict(color=TEXT_PRIMARY),
    )
    
    return fig
