"""STOCK ANALYZER - Deep dive with technical indicators"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from frontend.components.shared import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def calc_rsi(closes: list, period: int = 14) -> list:
    if len(closes) < period + 1:
        return [None] * len(closes)
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rsis = [None] * (period + 1)
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsis.append(100 - (100 / (1 + rs)))
    return rsis

def calc_sma(values: list, period: int) -> list:
    result = [None] * (period - 1)
    for i in range(period - 1, len(values)):
        result.append(sum(values[i-period+1:i+1]) / period)
    return result

def calc_bollinger(closes: list, period: int = 20, std_mult: float = 2.0):
    sma = calc_sma(closes, period)
    upper, lower = [], []
    for i in range(len(closes)):
        if sma[i] is None:
            upper.append(None)
            lower.append(None)
        else:
            window = closes[max(0, i-period+1):i+1]
            std = np.std(window)
            upper.append(sma[i] + std_mult * std)
            lower.append(sma[i] - std_mult * std)
    return sma, upper, lower

def calc_macd(closes: list, fast=12, slow=26, signal=9):
    def ema(data, period):
        result = [None] * (period - 1)
        k = 2 / (period + 1)
        ema_val = sum(data[:period]) / period
        result.append(ema_val)
        for i in range(period, len(data)):
            ema_val = data[i] * k + ema_val * (1 - k)
            result.append(ema_val)
        return result
    
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    macd_line = [
        (f - s) if (f is not None and s is not None) else None
        for f, s in zip(ema_fast, ema_slow)
    ]
    macd_valid = [v for v in macd_line if v is not None]
    signal_line_raw = ema(macd_valid, signal)
    
    none_count = sum(1 for v in macd_line if v is None)
    signal_line = [None] * (none_count + signal - 1) + signal_line_raw
    signal_line = signal_line[:len(macd_line)]
    
    histogram = [
        (m - s) if (m is not None and s is not None) else None
        for m, s in zip(macd_line, signal_line)
    ]
    return macd_line, signal_line, histogram

def render(api_url: str):
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="color:#ff6600; font-size:18px; font-weight:700;">🔍 STOCK ANALYZER</span>
        <span style="color:#555; font-size:10px;">TECHNICAL ANALYSIS · RSI · MACD · BOLLINGER · SMA</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_sym, col_per, col_btn = st.columns([2, 1, 1])
    with col_sym:
        symbol = st.text_input("Symbol", value="AAPL", placeholder="AAPL, THYAO.IS, ASML.AS...", key="analyzer_sym")
    with col_per:
        period = st.selectbox("Period", ["1mo","3mo","6mo","1y","2y","5y"], index=3, key="analyzer_per")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        analyze = st.button("ANALYZE", key="analyzer_btn", use_container_width=True)
    
    # Indicators toggles
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    with col_i1:
        show_sma = st.checkbox("SMA 20/50/200", value=True)
    with col_i2:
        show_bb = st.checkbox("Bollinger Bands", value=True)
    with col_i3:
        show_rsi = st.checkbox("RSI (14)", value=True)
    with col_i4:
        show_macd = st.checkbox("MACD", value=True)
    
    if analyze:
        sym = symbol.upper()
        with st.spinner(f"Analyzing {sym}..."):
            data = api_get(f"{api_url}/api/stock/{sym}?period={period}")
        
        if not data or not data.get("ohlcv"):
            st.error(f"No data found for {sym}")
            return
        
        ohlcv = data["ohlcv"]
        closes = [d["close"] for d in ohlcv]
        dates = [d["date"] for d in ohlcv]
        highs = [d.get("high", d["close"]) for d in ohlcv]
        lows = [d.get("low", d["close"]) for d in ohlcv]
        opens = [d.get("open", d["close"]) for d in ohlcv]
        volumes = [d.get("volume", 0) for d in ohlcv]
        
        curr = closes[-1]
        prev = closes[-2] if len(closes) > 1 else curr
        chg = ((curr - prev) / prev) * 100
        
        # Header metrics
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("PRICE", f"{curr:,.2f}")
        c2.metric("CHANGE", fmt_pct(chg))
        c3.metric("52W HIGH", fmt_price(data.get("52w_high")))
        c4.metric("52W LOW", fmt_price(data.get("52w_low")))
        c5.metric("MKT CAP", fmt_mcap(data.get("market_cap")))
        c6.metric("P/E", f"{data.get('pe_ratio'):.1f}" if data.get("pe_ratio") else "—")
        
        # Compute indicators
        sma20 = calc_sma(closes, 20)
        sma50 = calc_sma(closes, 50)
        sma200 = calc_sma(closes, 200)
        bb_mid, bb_upper, bb_lower = calc_bollinger(closes)
        rsi = calc_rsi(closes)
        macd_line, signal_line, histogram = calc_macd(closes)
        
        # Build subplots
        rows = 1 + (1 if show_rsi else 0) + (1 if show_macd else 0)
        row_heights = [0.55] + [0.225] * (rows - 1) if rows > 1 else [1.0]
        
        subplot_titles = [f"{sym} — {data.get('name','')}"]
        if show_rsi:
            subplot_titles.append("RSI (14)")
        if show_macd:
            subplot_titles.append("MACD")
        
        fig = make_subplots(
            rows=rows, cols=1,
            shared_xaxes=True,
            row_heights=row_heights,
            subplot_titles=subplot_titles,
            vertical_spacing=0.04,
        )
        
        # Candlesticks
        fig.add_trace(go.Candlestick(
            x=dates, open=opens, high=highs, low=lows, close=closes,
            name="OHLC",
            increasing_line_color="#00cc66",
            decreasing_line_color="#ff3333",
            increasing_fillcolor="#00cc6633",
            decreasing_fillcolor="#ff333333",
        ), row=1, col=1)
        
        # Volume
        vol_colors = ["#00cc6633" if c >= o else "#ff333333" for o, c in zip(opens, closes)]
        fig.add_trace(go.Bar(x=dates, y=volumes, marker_color=vol_colors, name="Volume", showlegend=False, yaxis="y3"), row=1, col=1)
        
        if show_sma:
            for sma, color, name in [(sma20,"#ffcc00","SMA20"),(sma50,"#0099ff","SMA50"),(sma200,"#ff6600","SMA200")]:
                valid_dates = [d for d, v in zip(dates, sma) if v is not None]
                valid_sma = [v for v in sma if v is not None]
                fig.add_trace(go.Scatter(x=valid_dates, y=valid_sma, mode="lines", 
                                          line=dict(color=color, width=1, dash="dot"), name=name), row=1, col=1)
        
        if show_bb:
            valid_dates_bb = [d for d, v in zip(dates, bb_upper) if v is not None]
            fig.add_trace(go.Scatter(x=valid_dates_bb, y=[v for v in bb_upper if v is not None],
                                      mode="lines", line=dict(color="#9933ff", width=1, dash="dot"),
                                      name="BB Upper", showlegend=True), row=1, col=1)
            fig.add_trace(go.Scatter(x=valid_dates_bb, y=[v for v in bb_lower if v is not None],
                                      mode="lines", line=dict(color="#9933ff", width=1, dash="dot"),
                                      name="BB Lower", fill="tonexty", fillcolor="#9933ff11",
                                      showlegend=False), row=1, col=1)
        
        current_row = 2
        
        if show_rsi:
            valid_dates_rsi = [d for d, v in zip(dates, rsi) if v is not None]
            valid_rsi = [v for v in rsi if v is not None]
            fig.add_trace(go.Scatter(x=valid_dates_rsi, y=valid_rsi, mode="lines",
                                      line=dict(color="#ff6600", width=1.5), name="RSI"), row=current_row, col=1)
            fig.add_hline(y=70, line=dict(color="#ff3333", width=1, dash="dot"), row=current_row, col=1)
            fig.add_hline(y=30, line=dict(color="#00cc66", width=1, dash="dot"), row=current_row, col=1)
            fig.update_yaxes(range=[0,100], row=current_row, col=1)
            current_row += 1
        
        if show_macd:
            valid_dates_macd = [d for d, v in zip(dates, macd_line) if v is not None]
            valid_macd = [v for v in macd_line if v is not None]
            valid_signal = [v for d, v in zip(dates, signal_line) if macd_line[dates.index(d)] is not None and v is not None][:len(valid_macd)]
            valid_hist = [v for v in histogram if v is not None][:len(valid_dates_macd)]
            
            hist_colors = ["#00cc6666" if h >= 0 else "#ff333366" for h in valid_hist]
            
            fig.add_trace(go.Bar(x=valid_dates_macd[:len(valid_hist)], y=valid_hist,
                                  marker_color=hist_colors, name="MACD Hist", showlegend=False), row=current_row, col=1)
            fig.add_trace(go.Scatter(x=valid_dates_macd, y=valid_macd, mode="lines",
                                      line=dict(color="#0099ff", width=1.5), name="MACD"), row=current_row, col=1)
            fig.add_trace(go.Scatter(x=valid_dates_macd[:len(valid_signal)], y=valid_signal, mode="lines",
                                      line=dict(color="#ff6600", width=1.5), name="Signal"), row=current_row, col=1)
        
        fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            height=200 + rows * 200,
            xaxis_rangeslider_visible=False,
            showlegend=True,
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Technical signals summary
        section_header("TECHNICAL SIGNALS", "computed from price data")
        
        # Current RSI signal
        curr_rsi = next((v for v in reversed(rsi) if v is not None), None)
        curr_macd = next((v for v in reversed(macd_line) if v is not None), None)
        curr_signal = next((v for v in reversed(signal_line) if v is not None), None)
        curr_sma20 = next((v for v in reversed(sma20) if v is not None), None)
        curr_sma50 = next((v for v in reversed(sma50) if v is not None), None)
        
        signals = []
        
        if curr_rsi is not None:
            if curr_rsi > 70:
                signals.append(("RSI", f"{curr_rsi:.1f}", "OVERBOUGHT", "#ff3333"))
            elif curr_rsi < 30:
                signals.append(("RSI", f"{curr_rsi:.1f}", "OVERSOLD", "#00cc66"))
            else:
                signals.append(("RSI", f"{curr_rsi:.1f}", "NEUTRAL", "#888"))
        
        if curr_macd is not None and curr_signal is not None:
            if curr_macd > curr_signal:
                signals.append(("MACD", f"{curr_macd:.3f}", "BULLISH CROSS", "#00cc66"))
            else:
                signals.append(("MACD", f"{curr_macd:.3f}", "BEARISH CROSS", "#ff3333"))
        
        if curr_sma20 and curr_sma50:
            if closes[-1] > curr_sma20 and closes[-1] > curr_sma50:
                signals.append(("TREND", f"Price above SMA20/50", "BULLISH", "#00cc66"))
            elif closes[-1] < curr_sma20 and closes[-1] < curr_sma50:
                signals.append(("TREND", f"Price below SMA20/50", "BEARISH", "#ff3333"))
            else:
                signals.append(("TREND", f"Mixed", "NEUTRAL", "#888"))
        
        # 52-week position
        high52 = data.get("52w_high")
        low52 = data.get("52w_low")
        if high52 and low52:
            pos = (curr - low52) / (high52 - low52) * 100
            signals.append(("52W POSITION", f"{pos:.0f}% of range", 
                            "HIGH" if pos > 75 else "LOW" if pos < 25 else "MID", 
                            "#ff6600" if pos > 75 else "#0099ff" if pos < 25 else "#888"))
        
        cols_sig = st.columns(len(signals)) if signals else []
        for i, (indicator, value, label, color) in enumerate(signals):
            with cols_sig[i]:
                st.markdown(f"""
                <div style="background:#111; border:1px solid #2a2a2a; border-top:3px solid {color};
                            padding:10px; text-align:center; border-radius:2px;">
                    <div style="color:#555; font-size:9px; letter-spacing:0.1em;">{indicator}</div>
                    <div style="color:#e8e8e8; font-size:13px; font-weight:600; margin:4px 0;">{value}</div>
                    <div style="color:{color}; font-size:10px; font-weight:700; letter-spacing:0.05em;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # News
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        section_header(f"{sym} NEWS", "latest headlines")
        news = api_get(f"{api_url}/api/news/stock/{sym}") or []
        for item in news[:5]:
            title = item.get("title","")
            if title:
                st.markdown(f"""
                <div style="padding:6px 0; border-bottom:1px solid #1a1a1a; font-size:11px;">
                    <a href="{item.get('link','#')}" target="_blank" style="color:#e8e8e8; text-decoration:none;">
                        {title[:120]}
                    </a>
                    <div style="color:#555; font-size:9px;">{item.get('publisher','')} · {item.get('published','')}</div>
                </div>
                """, unsafe_allow_html=True)