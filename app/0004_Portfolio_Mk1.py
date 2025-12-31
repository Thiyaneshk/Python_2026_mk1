import streamlit as st
import json
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import io
import contextlib

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
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
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
    
    df = pd.DataFrame(portfolio_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["ticker"],
        y=df["gain_loss_pct"],
        marker_color=df["gain_loss_pct"].apply(lambda x: "green" if x >= 0 else "red"),
        text=df["gain_loss_pct"].round(2).astype(str) + "%",
        textposition="auto",
        name="Gain/Loss %"
    ))
    
    fig.update_layout(
        title="Portfolio Performance by Ticker",
        xaxis_title="Ticker",
        yaxis_title="Gain/Loss %",
        height=400,
        hovermode="x unified"
    )
    
    return fig

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Current Holdings")

with col2:
    if st.button("➕ Add Ticker", width='stretch'):
        st.session_state.show_add_form = True

portfolio = load_portfolio()
holdings = portfolio.get("portfolio", [])

if holdings:
    portfolio_data = []
    for holding in holdings:
        metrics = calculate_metrics(holding["ticker"], holding["shares"], holding["buy_price"])
        if metrics:
            portfolio_data.append(metrics)
    
    if portfolio_data:
        df_display = pd.DataFrame(portfolio_data)
        df_display = df_display[["ticker", "shares", "buy_price", "current_price", "current_value", "gain_loss", "gain_loss_pct"]]
        df_display.columns = ["Ticker", "Shares", "Buy Price", "Current Price", "Current Value", "Gain/Loss $", "Gain/Loss %"]
        
        df_display["Gain/Loss %"] = df_display["Gain/Loss %"].round(2)
        df_display["Gain/Loss $"] = df_display["Gain/Loss $"].round(2)
        df_display["Current Value"] = df_display["Current Value"].round(2)
        
        st.dataframe(df_display, width='stretch')
        
        fig = plot_portfolio_performance(portfolio_data)
        if fig:
            st.plotly_chart(fig, width='stretch')
else:
    st.info("No holdings yet. Add your first ticker to get started!")

st.divider()

st.subheader("Watchlist")
watchlist = portfolio.get("watchlist", [])

if watchlist:
    for item in watchlist:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{item['ticker']}** - {item.get('reason', 'N/A')}")
        with col2:
            if st.button("✅ Add to Portfolio", key=f"add_{item['ticker']}"):
                st.info(f"Configure {item['ticker']} in Add Ticker form")
        with col3:
            if st.button("❌ Remove", key=f"remove_{item['ticker']}"):
                portfolio["watchlist"] = [w for w in watchlist if w["ticker"] != item["ticker"]]
                save_portfolio(portfolio)
                st.rerun()
else:
    st.info("No watchlist items yet.")

if st.session_state.get("show_add_form", False):
    st.divider()
    st.subheader("Add New Ticker")
    
    with st.form("add_ticker_form"):
        ticker = st.text_input("Ticker Symbol (e.g., AAPL)").upper()
        shares = st.number_input("Number of Shares", min_value=1, step=1)
        buy_price = st.number_input("Buy Price per Share", min_value=0.01, step=0.01)
        buy_date = st.date_input("Buy Date")
        notes = st.text_area("Notes (optional)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("Add to Portfolio"):
                if ticker:
                    new_holding = {
                        "ticker": ticker,
                        "shares": int(shares),
                        "buy_price": buy_price,
                        "buy_date": buy_date.isoformat(),
                        "notes": notes
                    }
                    portfolio["portfolio"].append(new_holding)
                    save_portfolio(portfolio)
                    st.success(f"✅ Added {ticker} to portfolio!")
                    st.session_state.show_add_form = False
                    st.rerun()
        
        with col2:
            if st.form_submit_button("Add to Watchlist"):
                if ticker:
                    new_watchlist = {
                        "ticker": ticker,
                        "added_date": datetime.now().isoformat(),
                        "reason": notes
                    }
                    portfolio["watchlist"].append(new_watchlist)
                    save_portfolio(portfolio)
                    st.success(f"✅ Added {ticker} to watchlist!")
                    st.session_state.show_add_form = False
                    st.rerun()
