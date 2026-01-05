from utils import utils
import streamlit as st
import yfinance as yf
import pandas as pd
import io
import contextlib
import urllib.parse
st.set_page_config(
    page_title="Stock Performance",
    page_icon="📈",
    layout="wide")

st.title('Compare Stock performance')

# Support preselecting tickers via query param: ?tickers=RELIANCE,INFY
params = st.experimental_get_query_params()
passed = []
if 'tickers' in params:
    raw = params.get('tickers')[0]
    raw = urllib.parse.unquote(raw)
    passed = [p for p in raw.split(',') if p]

indices = utils.index_list()
# try to pick an index that contains the most passed tickers
best_idx_pos = 0
if passed:
    best_count = 0
    for i, idx in enumerate(indices):
        symbols = utils.get_stock_list(idx)
        count = sum(1 for p in passed for sym in symbols if sym == p or sym.endswith(p) or sym.replace('.NS', '') == p)
        if count > best_count:
            best_count = count
            best_idx_pos = i

index_option = st.selectbox('How would you like to be contacted?', indices, index=best_idx_pos)
options = utils.get_stock_list(index_option)

# determine defaults based on passed tickers
defaults = []
if passed:
    for p in passed:
        for sym in options:
            if sym == p or sym.endswith(p) or sym.replace('.NS', '') == p:
                if sym not in defaults:
                    defaults.append(sym)

dropdown = st.multiselect("Pick your assets", options, default=defaults)
year_slider=st.slider("Choose Year", min_value=2022,max_value=utils.cur_year(), step=1)
if len(dropdown) > 0:
    # prepare tickers: support multiselect (list) or single selection (str)
    if isinstance(dropdown, (list, tuple)):
        tickers = [d if d.endswith('.NS') else d + '.NS' for d in dropdown]
    else:
        tickers = dropdown if dropdown.endswith('.NS') else dropdown + '.NS'

    # Silence yfinance download messages
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        data = yf.download(tickers, start=str(year_slider) + '-01-01', end=str(utils.cur_year()) + '-12-31')

    # Normalize data to a DataFrame of close prices per ticker
    adj = None
    # MultiIndex columns (e.g., ('Adj Close', 'TICKER'))
    if isinstance(data.columns, pd.MultiIndex):
        top_level = list(data.columns.get_level_values(0))
        if 'Adj Close' in top_level:
            adj = data['Adj Close']
        elif 'Close' in top_level:
            adj = data['Close']
        else:
            # fallback: try to pivot to ticker columns by taking first sublevel
            try:
                adj = data.xs('Close', axis=1, level=0, drop_level=True)
            except Exception:
                adj = data
    else:
        if 'Adj Close' in data.columns:
            adj = data['Adj Close']
        elif 'Close' in data.columns:
            adj = data['Close']
        else:
            adj = data

    df = utils.relative_return(adj)
    st.line_chart(df)