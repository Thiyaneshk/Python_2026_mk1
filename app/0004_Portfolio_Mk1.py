import streamlit as st
import json
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Portfolio Tracker", layout="wide")
st.title("📈 Portfolio Tracker")

PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "portfolio.json")

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    return {"portfolio": [], "watchlist": []}

def save_portfolio(data):
    os.makedirs(os.path.dirname(PORTFOLIO_FILE), exist_ok=True)
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=2)

def fetch_stock_data(ticker, period="3mo"):
    try:
        data = yf.download(ticker, period=period, progress=False)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_metrics(ticker, shares, buy_price):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice", None)
        
        if current_price is None:
            return None
        
        current_value = shares * current_price
        buy_value = shares * buy_price
        gain_loss = current_value - buy_value
        gain_loss_pct = (gain_loss / buy_value * 100) if buy_value > 0 else 0
        
        return {
            "ticker": ticker,
            "current_price": current_price,
            "buy_price": buy_price,
            "shares": shares,
            "current_value": current_value,
            "buy_value": buy_value,
            "gain_loss": gain_loss,
            "gain_loss_pct": gain_loss_pct
        }
    except Exception as e:
        st.warning(f"Could not fetch price for {ticker}")
        return None

def plot_portfolio_performance(portfolio_data):
    if not portfolio_data:
        st.info("No portfolio data to display")
        return