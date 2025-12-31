from utils import utils
import streamlit as st
import yfinance as yf
import pandas as pd
st.set_page_config(
    page_title="Stock Performance",
    page_icon="📈",
    layout="wide")

st.title('Compare Stock performance')
index_option = st.selectbox( 'How would you like to be contacted?', utils.index_list())
dropdown=st.multiselect("Pick your assets", utils.get_stock_list(index_option))
year_slider=st.slider("Choose Year", min_value=2022,max_value=utils.cur_year(), step=1)
if len(dropdown) > 0:
    # prepare tickers: support multiselect (list) or single selection (str)
    if isinstance(dropdown, (list, tuple)):
        tickers = [d if d.endswith('.NS') else d + '.NS' for d in dropdown]
    else:
        tickers = dropdown if dropdown.endswith('.NS') else dropdown + '.NS'

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