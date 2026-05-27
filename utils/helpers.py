"""
Helper functions and utilities
"""

from config import COLOR_GREEN, COLOR_RED


def format_currency(value):
    """
    Format value as currency
    """
    if value is None:
        return "N/A"
    return f"${value:,.2f}"


def format_percent(value):
    """
    Format value as percentage
    """
    if value is None:
        return "N/A"
    
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def get_change_color(value):
    """
    Get color based on change value (positive/negative)
    """
    if value is None:
        return COLOR_RED
    return COLOR_GREEN if value >= 0 else COLOR_RED


def calculate_change(current, previous):
    """
    Calculate price change and percentage
    """
    if previous == 0:
        return None, None
    
    change = current - previous
    change_pct = (change / previous) * 100
    
    return change, change_pct


def format_large_number(value):
    """
    Format large numbers (millions, billions)
    """
    if value is None:
        return "N/A"
    
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.0f}"


def is_market_open(market="US"):
    """
    Check if market is currently open
    """
    from datetime import datetime
    import pytz
    
    if market == "US":
        tz = pytz.timezone('America/New_York')
    elif market == "TURKEY":
        tz = pytz.timezone('Europe/Istanbul')
    elif market == "EUROPE":
        tz = pytz.timezone('Europe/Berlin')
    else:
        return None
    
    now = datetime.now(tz)
    day_of_week = now.weekday()  # 0=Monday, 6=Sunday
    
    if day_of_week >= 5:  # Saturday or Sunday
        return False
    
    return True
