import requests,io
import pandas as pd
import streamlit as st
from datetime import date
import datetime
import calendar


## Emoji - https://emojifinder.com/

# @st.cache
def get_exp_date():
    today = datetime.date.today()
    expiry_dt = today + datetime.timedelta((3 - today.weekday()) % 7)
    input_dte = st.date_input("Enter Expiry date :", expiry_dt)
    return str.upper(input_dte.strftime('%d%b%Y'))

@st.cache
def Expiry_dates():
    list_exp_dates = list()
    expiry_day = "Thursday"
    start_date = datetime.date.today().strftime("%d/%m/%Y")
    end_date = datetime.date(datetime.date.today().year, 12, 31).strftime("%d/%m/%Y")

    # start_date = datetime.datetime.strptime(start, '%d/%m/%Y')
    # end_date = datetime.datetime.strptime(end, '%d/%m/%Y')

    for i in range((end_date - start_date).days):
        if calendar.day_name[(start_date + datetime.timedelta(days=i + 1)).weekday()] == expiry_day:
            # print((start_date + datetime.timedelta(days=i + 1)).strftime("%d%b%Y"))
            list_exp_dates.append((start_date + datetime.timedelta(days=i + 1)).strftime("%d%b%Y"))
    print("Printing list :", list_exp_dates)
    return list_exp_dates

@st.cache
def index_list():
    return ['Nifty', 'Bank-Nifty', 'Nifty-500','Nifty-IT','NASDAQ']

@st.cache
def get_stock_list(index_name):
    if str.upper(index_name) == 'NIFTY-50':
        url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
    elif str.upper(index_name) == 'NIFTY-500':
        url = 'https://www1.nseindia.com/content/indices/ind_nifty500list.csv'
    elif str.upper(index_name) == 'BANK-NIFTY':
        url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
    else:
        url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
    s = requests.get(url).content
    script_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    index_list={'Symbol':['^NSEI','^NSEBANK','^GSPC','^DJI','^IXIC']}
    index_df=pd.DataFrame(index_list)
    # return index_df
    script_df['Symbol'] = script_df['Symbol']+'.NS'
    script_df = pd.concat([index_df, script_df[:]]).reset_index(drop=True)
    Scripts_dropdown = script_df.Symbol.unique().tolist()
    return Scripts_dropdown

@st.cache
def get_nifty50_list():
    url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
    # url = 'https://www1.nseindia.com/content/indices/ind_nifty500list.csv'
    s = requests.get(url).content
    script_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    index_list={'Symbol':['^NSEI','^NSEBANK']}
    index_df=pd.DataFrame(index_list)
    # return index_df
    script_df['Symbol'] = script_df['Symbol']+'.NS'
    script_df = pd.concat([index_df, script_df[:]]).reset_index(drop=True)
    Scripts_dropdown = script_df.Symbol.unique().tolist()
    return Scripts_dropdown

@st.cache
def get_nifty500_list():
    # url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
    url = 'https://www1.nseindia.com/content/indices/ind_nifty500list.csv'
    s = requests.get(url).content
    script_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    index_list={'Symbol':['^NSEI','^NSEBANK']}
    index_df=pd.DataFrame(index_list)
    # return index_df
    script_df['Symbol'] = script_df['Symbol']+'.NS'
    script_df = pd.concat([index_df, script_df[:]]).reset_index(drop=True)
    Scripts_dropdown = script_df.Symbol.unique().tolist()
    return Scripts_dropdown

def relative_return(df):
    rel=df.pct_change()
    cumret=(1+rel).cumprod() - 1
    cumret=cumret.fillna(0)
    return cumret

@st.cache
def cur_year():
    return date.today().year

@st.cache
def cur_year_YYYY_MON_DD():
    return str(date.today().year) + '-12-31'