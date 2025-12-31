from utils import utils
from plotly.subplots import make_subplots
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import io
import contextlib
import urllib.parse

st.set_page_config(
    page_title="Market Profile Chart",
    page_icon="💹",
    layout="wide") 

# Support preselecting via ?ticker=RELIANCE
params = st.experimental_get_query_params()
passed_ticker = None
if 'ticker' in params:
    passed_ticker = urllib.parse.unquote(params.get('ticker')[0])

indices = utils.index_list()
best_idx = 0
if passed_ticker:
    for i, idx in enumerate(indices):
        symbols = utils.get_stock_list(idx)
        if any(sym == passed_ticker or sym.endswith(passed_ticker) or sym.replace('.NS', '') == passed_ticker for sym in symbols):
            best_idx = i
            break

index_option = st.sidebar.selectbox( 'Choose a Index :', indices, index=best_idx)
options = utils.get_stock_list(index_option)

# default ticker
default_ticker = None
if passed_ticker:
    for sym in options:
        if sym == passed_ticker or sym.endswith(passed_ticker) or sym.replace('.NS', '') == passed_ticker:
            default_ticker = sym
            break

ticker = st.sidebar.selectbox( 'Choose a Stock', options, index=options.index(default_ticker) if default_ticker in options else 0)

i = st.sidebar.selectbox(
    "Interval in minutes",
    ("1m", "5m", "15m", "30m")
)

p = st.sidebar.number_input("How many days (1-30)", min_value=1, max_value=30, step=1)

stock = yf.Ticker(ticker)
# Silence yfinance console messages for missing/delisted symbols
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    history_data = stock.history(interval=i, period=str(p) + "d")

# Handle missing or empty history data (e.g., delisted or unavailable symbols)
if history_data is None or history_data.empty or history_data['Close'].isna().all():
    st.warning(f"No price data found for {ticker}; symbol may be delisted or unavailable.")
    st.stop()

prices = history_data['Close']
volumes = history_data['Volume']

lower = prices.min()
upper = prices.max()

prices_ax = np.linspace(lower, upper, num=20)
vol_ax = np.zeros(20)

for idx in range(0, len(volumes)):
    p = prices.iloc[idx]
    v = volumes.iloc[idx]
    if (p >= prices_ax[0] and p < prices_ax[1]):
        vol_ax[0] += v

    elif (p >= prices_ax[1] and p < prices_ax[2]):
        vol_ax[1] += v

    elif (p >= prices_ax[2] and p < prices_ax[3]):
        vol_ax[2] += v

    elif (p >= prices_ax[3] and p < prices_ax[4]):
        vol_ax[3] += v

    elif (p >= prices_ax[4] and p < prices_ax[5]):
        vol_ax[4] += v

    elif (p >= prices_ax[5] and p < prices_ax[6]):
        vol_ax[5] += v

    elif (p >= prices_ax[6] and p < prices_ax[7]):
        vol_ax[6] += v

    elif (p >= prices_ax[7] and p < prices_ax[8]):
        vol_ax[7] += v

    elif (p >= prices_ax[8] and p < prices_ax[9]):
        vol_ax[8] += v

    elif (p >= prices_ax[9] and p < prices_ax[10]):
        vol_ax[9] += v

    elif (p >= prices_ax[10] and p < prices_ax[11]):
        vol_ax[10] += v

    elif (p >= prices_ax[11] and p < prices_ax[12]):
        vol_ax[11] += v

    elif (p >= prices_ax[12] and p < prices_ax[13]):
        vol_ax[12] += v

    elif (p >= prices_ax[13] and p < prices_ax[14]):
        vol_ax[13] += v

    elif (p >= prices_ax[14] and p < prices_ax[15]):
        vol_ax[14] += v

    elif (p >= prices_ax[15] and p < prices_ax[16]):
        vol_ax[15] += v

    elif (p >= prices_ax[16] and p < prices_ax[17]):
        vol_ax[16] += v

    elif (p >= prices_ax[17] and p < prices_ax[18]):
        vol_ax[17] += v

    elif (p >= prices_ax[18] and p < prices_ax[19]):
        vol_ax[18] += v

    else:
        vol_ax[19] += v

fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.2, 0.8],
    specs=[[{}, {}]],
    horizontal_spacing=0.01
)

fig.add_trace(
    go.Bar(
        x=vol_ax,
        y=prices_ax,
        text=np.around(prices_ax, 2),
        textposition='auto',
        orientation='h'
    ),
    row=1, col=1
)

dateStr = pd.to_datetime(history_data.index).strftime("%d-%m-%Y %H:%M:%S")

fig.add_trace(
    go.Candlestick(x=dateStr,
                   open=history_data['Open'],
                   high=history_data['High'],
                   low=history_data['Low'],
                   close=history_data['Close'],
                   yaxis="y2"
                   ),
    row=1, col=2
)

fig.update_layout(
    title_text='Market Profile Chart',  # title of plot
    bargap=0.01,  # gap between bars of adjacent location coordinates,
    showlegend=False,
    xaxis=dict(
        showticklabels=False
    ),
    yaxis=dict(
        showticklabels=False
    ),
    yaxis2=dict(
        title="Price (INR)",
        side="right"

    )

)

fig.update_yaxes(nticks=20)
fig.update_yaxes(side="right")
fig.update_layout(height=800)

config = {
    'modeBarButtonsToAdd': ['drawline']
}

st.plotly_chart(fig, width='stretch', config=config)