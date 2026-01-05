from Utils import utils
import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
import io
import contextlib

# App title
st.markdown('''
# Stock Price App
Shown are the stock price data for query companies!

**Credits**
- App built by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor))
- Built in `Python` using `streamlit`,`yfinance`, `cufflinks`, `pandas` and `datetime`
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2022, 12, 31))

# Retrieving tickers data
# ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
# ticker_list = pd.read_csv(r"C:\Users\thiya\OneDrive\Desktop\Nifty50_list.txt")

index_option = st.sidebar.selectbox( 'Choose Index', utils.index_list())
# dropdown=st.multiselect("Pick your assets", utils.get_stock_list(index_option))

tickerSymbol = st.sidebar.selectbox('Stock ticker', utils.get_stock_list(index_option)) # Select ticker symbol
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
# Silence yfinance console messages
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

if tickerDf is None or tickerDf.empty:
    st.warning(f"No historical price data found for {tickerSymbol}; symbol may be delisted or unavailable.")
    st.stop()

# Ticker information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)

# Ticker data
# st.header('**Ticker data**')
# st.write(tickerDf.tail())

# Bollinger bands
st.header('**Candle stick chart**')
qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')

#
# def add_ema(self, periods=20, column=None, str=None,
#             name='', **kwargs):
# qf.add_bollinger_bands()
qf.add_ema(periods=200)
qf.add_ema(periods=13)
qf.add_ema(periods=34)
qf.add_rsi( periods=20, rsi_upper=70, rsi_lower=30, showbands=True, column=None)
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

####
#st.write('---')
#st.write(tickerData.info)
