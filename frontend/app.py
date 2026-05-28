"""
FINANSAL TERMINAL v2.0
Bloomberg-style financial terminal
"""

import streamlit as st

st.set_page_config(
    page_title="FINANSAL TERMINAL",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get help": None, "Report a bug": None, "About": "FINANSAL TERMINAL v2.0"}
)

# Global CSS - Bloomberg dark theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #111111;
    --bg-card: #161616;
    --bg-hover: #1e1e1e;
    --accent-orange: #ff6600;
    --accent-blue: #0099ff;
    --accent-green: #00cc66;
    --accent-red: #ff3333;
    --accent-yellow: #ffcc00;
    --text-primary: #e8e8e8;
    --text-secondary: #888888;
    --text-dim: #555555;
    --border: #2a2a2a;
    --border-accent: #ff6600;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background-color: var(--bg-primary) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d0d0d !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-primary) !important;
}

/* Remove streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Metrics */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 8px 12px;
}
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-size: 10px !important; }
[data-testid="stMetricValue"] { color: var(--text-primary) !important; font-size: 16px !important; font-weight: 600 !important; }
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-secondary) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    border-radius: 2px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    border-color: var(--accent-orange) !important;
    color: var(--accent-orange) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.05em !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-orange) !important;
    border-bottom: 2px solid var(--accent-orange) !important;
}

/* DataFrames */
.stDataFrame { border: 1px solid var(--border) !important; }
[data-testid="stDataFrame"] table { font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; }

/* Inputs */
.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    border-radius: 2px !important;
}
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); }
::-webkit-scrollbar-thumb:hover { background: var(--text-dim); }

/* Custom cards */
.fin-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-orange);
    padding: 12px 16px;
    margin: 4px 0;
    border-radius: 2px;
}
.fin-header {
    color: var(--accent-orange);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
    margin-bottom: 10px;
}
.up-color { color: #00cc66 !important; }
.down-color { color: #ff3333 !important; }
.dim-color { color: #888888; }
.accent-color { color: #ff6600; }
.blue-color { color: #0099ff; }

/* Ticker tape */
.ticker-wrap {
    background: var(--bg-secondary);
    border-top: 1px solid var(--accent-orange);
    border-bottom: 1px solid var(--border);
    padding: 6px 0;
    overflow: hidden;
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

# ─── Navigation ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 8px;">
        <span style="color:#ff6600; font-size:20px; font-weight:700; letter-spacing:0.1em;">FINANSAL</span>
        <span style="color:#888; font-size:10px; display:block; letter-spacing:0.2em;">TERMINAL v2.0</span>
        <div style="border-bottom:1px solid #2a2a2a; margin:12px 0;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.selectbox(
        "NAVIGATE",
        [
            "🏠  DASHBOARD",
            "🇹🇷  BIST STOCKS", 
            "🇺🇸  US STOCKS",
            "🇪🇺  EU STOCKS",
            "📈  ETF TRACKER",
            "🌍  MACRO & FX",
            "📰  NEWS FEED",
            "🚢  SHIP TRACKER",
            "✈️  CARGO PLANES",
            "🔥  HEATMAP",
            "🔍  STOCK ANALYZER",
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='border-bottom:1px solid #2a2a2a; margin: 8px 0;'></div>", unsafe_allow_html=True)
    
    # API Status
    st.markdown("<span style='color:#888; font-size:9px; letter-spacing:0.1em;'>API STATUS</span>", unsafe_allow_html=True)
    
    import requests as req
    api_url = os.environ.get("API_URL", "http://localhost:8000")
    try:
        r = req.get(f"{api_url}/", timeout=3)
        st.markdown("<span style='color:#00cc66; font-size:10px;'>● BACKEND ONLINE</span>", unsafe_allow_html=True)
    except:
        st.markdown("<span style='color:#ff3333; font-size:10px;'>● BACKEND OFFLINE</span>", unsafe_allow_html=True)
        api_url = "http://localhost:8000"
    
    st.markdown(f"<span style='color:#555; font-size:9px;'>yFinance ● AISHub ● OpenSky</span>", unsafe_allow_html=True)
    st.markdown("<div style='border-bottom:1px solid #2a2a2a; margin: 8px 0;'></div>", unsafe_allow_html=True)
    
    from datetime import datetime
    st.markdown(f"<span style='color:#555; font-size:9px;'>{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</span>", unsafe_allow_html=True)

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Route to pages
page_name = page.split("  ")[-1]

if page_name == "DASHBOARD":
    from frontend.pages import dashboard
    dashboard.render(api_url)
elif page_name == "BIST STOCKS":
    from frontend.pages import bist
    bist.render(api_url)
elif page_name == "US STOCKS":
    from frontend.pages import us_stocks
    us_stocks.render(api_url)
elif page_name == "EU STOCKS":
    from frontend.pages import eu_stocks
    eu_stocks.render(api_url)
elif page_name == "ETF TRACKER":
    from frontend.pages import etfs
    etfs.render(api_url)
elif page_name == "MACRO & FX":
    from frontend.pages import macro
    macro.render(api_url)
elif page_name == "NEWS FEED":
    from frontend.pages import news
    news.render(api_url)
elif page_name == "SHIP TRACKER":
    from frontend.pages import ships
    ships.render(api_url)
elif page_name == "CARGO PLANES":
    from frontend.pages import planes
    planes.render(api_url)
elif page_name == "HEATMAP":
    from frontend.pages import heatmap
    heatmap.render(api_url)
elif page_name == "STOCK ANALYZER":
    from frontend.pages import analyzer
    analyzer.render(api_url)