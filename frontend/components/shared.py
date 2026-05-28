"""Shared UI components for FINANSAL TERMINAL"""
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="#0a0a0a",
        plot_bgcolor="#0d0d0d",
        font=dict(family="IBM Plex Mono", color="#888888", size=10),
        xaxis=dict(
            gridcolor="#1e1e1e", linecolor="#2a2a2a", tickfont=dict(color="#555"),
            showgrid=True, zeroline=False,
        ),
        yaxis=dict(
            gridcolor="#1e1e1e", linecolor="#2a2a2a", tickfont=dict(color="#555"),
            showgrid=True, zeroline=False,
        ),
        margin=dict(l=40, r=20, t=30, b=30),
        hoverlabel=dict(bgcolor="#1e1e1e", font_size=11, font_family="IBM Plex Mono"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color="#888")),
    )
)

def api_get(url: str, timeout: int = 10):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return None

def color_val(val: float, neutral_zero: bool = True) -> str:
    if val is None:
        return "#888888"
    if val > 0:
        return "#00cc66"
    elif val < 0:
        return "#ff3333"
    return "#888888"

def fmt_pct(val) -> str:
    if val is None:
        return "—"
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.2f}%"

def fmt_price(val, decimals=2) -> str:
    if val is None:
        return "—"
    return f"{val:,.{decimals}f}"

def fmt_volume(vol) -> str:
    if not vol:
        return "—"
    if vol >= 1_000_000_000:
        return f"{vol/1_000_000_000:.1f}B"
    elif vol >= 1_000_000:
        return f"{vol/1_000_000:.1f}M"
    elif vol >= 1_000:
        return f"{vol/1_000:.1f}K"
    return str(vol)

def fmt_mcap(val) -> str:
    if not val:
        return "—"
    if val >= 1_000_000_000_000:
        return f"${val/1_000_000_000_000:.2f}T"
    elif val >= 1_000_000_000:
        return f"${val/1_000_000_000:.1f}B"
    elif val >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    return f"${val:,}"

def section_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="display:flex; align-items:baseline; gap:12px; margin-bottom:12px; padding-bottom:6px; border-bottom:1px solid #2a2a2a;">
        <span style="color:#ff6600; font-size:11px; font-weight:700; letter-spacing:0.15em;">{title}</span>
        <span style="color:#555; font-size:10px;">{subtitle}</span>
    </div>
    """, unsafe_allow_html=True)

def make_candlestick(ohlcv: list, title: str = "", height: int = 400):
    if not ohlcv:
        return None
    
    dates = [d["date"] for d in ohlcv]
    opens = [d.get("open", d.get("close", 0)) for d in ohlcv]
    highs = [d.get("high", d.get("close", 0)) for d in ohlcv]
    lows = [d.get("low", d.get("close", 0)) for d in ohlcv]
    closes = [d["close"] for d in ohlcv]
    volumes = [d.get("volume", 0) for d in ohlcv]
    
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=dates, open=opens, high=highs, low=lows, close=closes,
        name="OHLC",
        increasing_line_color="#00cc66",
        decreasing_line_color="#ff3333",
        increasing_fillcolor="#00cc6633",
        decreasing_fillcolor="#ff333333",
    ))
    
    # Volume bars
    colors = ["#00cc6633" if c >= o else "#ff333333" for o, c in zip(opens, closes)]
    fig.add_trace(go.Bar(
        x=dates, y=volumes,
        name="Volume",
        marker_color=colors,
        yaxis="y2",
        showlegend=False,
    ))
    
    fig.update_layout(
        **PLOTLY_TEMPLATE["layout"],
        title=dict(text=title, font=dict(color="#ff6600", size=12)),
        height=height,
        xaxis_rangeslider_visible=False,
        yaxis2=dict(
            overlaying="y", side="right", showgrid=False,
            tickfont=dict(color="#333"), showticklabels=False,
        ),
    )
    return fig

def make_line_chart(data: list, x_key: str, y_key: str, title: str = "", height: int = 300, color: str = "#ff6600"):
    if not data:
        return None
    
    x = [d[x_key] for d in data]
    y = [d[y_key] for d in data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color=color, width=1.5),
        fill="tozeroy",
        fillcolor=f"{color}11",
        name=y_key,
    ))
    fig.update_layout(
        **PLOTLY_TEMPLATE["layout"],
        title=dict(text=title, font=dict(color="#ff6600", size=11)),
        height=height,
        showlegend=False,
    )
    return fig

def ticker_html(indices: dict) -> str:
    if not indices:
        return ""
    items = []
    for name, data in indices.items():
        chg = data.get("change_pct", 0)
        color = "#00cc66" if chg >= 0 else "#ff3333"
        sign = "▲" if chg >= 0 else "▼"
        price = data.get("price", 0)
        items.append(
            f'<span style="margin:0 20px;">'
            f'<span style="color:#ff6600;font-weight:700;">{name}</span> '
            f'<span style="color:#e8e8e8;">{price:,.2f}</span> '
            f'<span style="color:{color};">{sign}{abs(chg):.2f}%</span>'
            f'</span>'
        )
    content = "".join(items) * 3  # repeat for scroll
    return f"""
    <div style="background:#111; border-top:2px solid #ff6600; border-bottom:1px solid #2a2a2a; 
                padding:8px 0; overflow:hidden; white-space:nowrap; font-size:11px; font-family:'IBM Plex Mono', monospace;">
        <div style="display:inline-block; animation:ticker 60s linear infinite;">
            {content}
        </div>
    </div>
    <style>
    @keyframes ticker {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-33.33%); }}
    }}
    </style>
    """

def stock_row_html(sym: str, price: float, chg: float, vol=None, extra: str = "") -> str:
    color = "#00cc66" if chg >= 0 else "#ff3333"
    sign = "+" if chg >= 0 else ""
    vol_str = fmt_volume(vol) if vol else ""
    return f"""
    <div style="display:flex; justify-content:space-between; align-items:center;
                padding:5px 8px; border-bottom:1px solid #1a1a1a; font-size:11px;
                transition:background 0.1s;" 
         onmouseover="this.style.background='#1a1a1a'" 
         onmouseout="this.style.background='transparent'">
        <span style="color:#ff6600; font-weight:600; min-width:90px;">{sym}</span>
        <span style="color:#e8e8e8; font-weight:500;">{price:,.2f}</span>
        <span style="color:{color}; min-width:70px; text-align:right;">{sign}{chg:.2f}%</span>
        <span style="color:#555; font-size:10px;">{vol_str}</span>
        <span style="color:#888; font-size:10px;">{extra}</span>
    </div>
    """