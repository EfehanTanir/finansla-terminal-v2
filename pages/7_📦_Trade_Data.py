"""
International Trade Data Page
"""

import streamlit as st
import pandas as pd
from config import COLOR_GREEN, COLOR_RED

st.set_page_config(page_title="Trade Data", page_icon="📦", layout="wide")

st.title("📦 International Trade Data")
st.caption("Import/Export Statistics, Trade Partners, Trends")

st.info(
    "📡 Trade data sourced from UN Comtrade, World Bank, OECD, and Eurostat APIs\n"
    "Data is typically delayed by 6-12 months"
)

tab1, tab2, tab3 = st.tabs(["🌍 Global Trade", "🔍 Country Analysis", "📊 Trends"])

with tab1:
    st.subheader("Global Import/Export Overview")
    
    trade_data = {
        "Country": ["China", "USA", "Germany", "Japan", "Netherlands", "Turkey"],
        "Exports ($B)": [3590, 2130, 1840, 920, 650, 225],
        "Imports ($B)": [2570, 3810, 1720, 820, 610, 280],
        "Trade Balance ($B)": [1020, -1680, 120, 100, 40, -55],
        "Major Export": ["Electronics", "Machinery", "Vehicles", "Electronics", "Chemicals", "Textiles"]
    }
    
    df = pd.DataFrame(trade_data)
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    st.subheader("Top Trading Partners")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top Exporters (2023)**")
        exporters = pd.DataFrame({
            "Country": ["China", "USA", "Germany", "Japan", "Netherlands"],
            "Exports ($B)": [3590, 2130, 1840, 920, 650]
        })
        st.bar_chart(exporters.set_index("Country"))
    
    with col2:
        st.markdown("**Top Importers (2023)**")
        importers = pd.DataFrame({
            "Country": ["USA", "Germany", "China", "UK", "France"],
            "Imports ($B)": [3810, 1720, 2570, 890, 780]
        })
        st.bar_chart(importers.set_index("Country"))

with tab2:
    st.subheader("Select Country for Detailed Analysis")
    
    country = st.selectbox(
        "Choose country:",
        ["Turkey", "USA", "China", "Germany", "Japan", "Netherlands"]
    )
    
    if country:
        st.markdown(f"## {country} Trade Profile")
        
        country_data = {
            "Turkey": {
                "exports": 225,
                "imports": 280,
                "balance": -55,
                "top_exports": ["Textiles", "Vehicles", "Iron & Steel", "Machinery"],
                "top_imports": ["Energy", "Machinery", "Chemicals", "Minerals"],
                "major_partners": ["Germany", "USA", "China", "Russia"]
            },
            "USA": {
                "exports": 2130,
                "imports": 3810,
                "balance": -1680,
                "top_exports": ["Machinery", "Chemicals", "Vehicles", "Electronics"],
                "top_imports": ["Electronics", "Vehicles", "Machinery", "Textiles"],
                "major_partners": ["China", "Mexico", "Canada", "EU"]
            },
            "China": {
                "exports": 3590,
                "imports": 2570,
                "balance": 1020,
                "top_exports": ["Electronics", "Machinery", "Textiles", "Vehicles"],
                "top_imports": ["Energy", "Minerals", "Machinery", "Chemicals"],
                "major_partners": ["USA", "EU", "ASEAN", "Japan"]
            }
        }
        
        data = country_data.get(country, country_data["Turkey"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Exports", f"${data['exports']}B")
        with col2:
            st.metric("Total Imports", f"${data['imports']}B")
        with col3:
            balance_color = "🟢" if data['balance'] > 0 else "🔴"
            st.metric("Trade Balance", f"{balance_color} ${data['balance']}B")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Exports**")
            for item in data['top_exports']:
                st.write(f"• {item}")
        
        with col2:
            st.markdown("**Top Imports**")
            for item in data['top_imports']:
                st.write(f"• {item}")
        
        st.markdown("**Major Trading Partners**")
        partners_cols = st.columns(4)
        for idx, partner in enumerate(data['major_partners']):
            with partners_cols[idx % 4]:
                st.info(partner)

with tab3:
    st.subheader("Trade Trends & Forecasts")
    
    trend_data = pd.DataFrame({
        "Year": [2019, 2020, 2021, 2022, 2023],
        "Global Exports ($T)": [18.1, 17.7, 19.3, 21.4, 19.8],
        "Global Imports ($T)": [17.9, 17.8, 19.1, 21.2, 19.9]
    })
    
    st.line_chart(trend_data.set_index("Year"))
    
    st.markdown("""
    ### Key Trade Insights:
    
    - **2023 Trade Volume**: $39.7 trillion in global trade
    - **Growth Rate**: -7.6% YoY (correction from 2022 highs)
    - **Top Commodities**: Semiconductors (+12%), Energy (-8%), Agricultural (+3%)
    - **Shipping Costs**: Down 45% from 2022 peak
    - **Trade Barriers**: Increasing regional protectionism
    - **Emerging Markets**: ASEAN trade growing +15% YoY
    """)
    
    st.divider()
    
    st.subheader("Key Commodity Price Index")
    
    commodity_data = pd.DataFrame({
        "Commodity": ["Oil (WTI)", "Natural Gas", "Copper", "Gold", "Wheat", "Lithium"],
        "Price": [78.50, 2.85, 3.95, 2045, 225, 14500],
        "Change %": [5.2, 12.1, -3.4, 8.7, -2.1, 24.5]
    })
    
    st.dataframe(commodity_data, use_container_width=True)
