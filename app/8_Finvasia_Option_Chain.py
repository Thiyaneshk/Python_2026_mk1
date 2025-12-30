import streamlit as st
import pandas as pd
import datetime
from Utils.api_helper import ShoonyaApiPy
import yaml

socket_opened = False
def get_exp_date():
    today = datetime.date.today()
    expiry_dt = today + datetime.timedelta((3 - today.weekday()) % 7)
    input_dte = st.date_input("Enter Expiry date :", expiry_dt)
    return str.upper(input_dte.strftime('%d%b%y'))

api = ShoonyaApiPy()

with open(r'Utils/cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)

ret = api.login(userid=cred['user'], password=cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

## Exec the code only if Login in successful
if ret != None:
    # st.write('Login successful')
    expiry_dt_selected = get_exp_date()
    st.write(expiry_dt_selected)

    exch = 'NFO'
    # tsym = 'NIFTY25AUG22F'
    tsym='NIFTY'+expiry_dt_selected+'F'
    # print(tsym)
    count_slider = st.slider("Choose Strikes count : ", min_value=1, max_value=20, step=1)
    chain = api.get_option_chain(exchange=exch, tradingsymbol=tsym, strikeprice=17600, count=count_slider)
    # st.write(chain)
    chainscrips = []
    for scrip in chain['values']:
        scripdata = api.get_quotes(exchange=scrip['exch'], token=scrip['token'])
        chainscrips.append(scripdata)
    df = pd.json_normalize(chainscrips)
    # st.write(df)

    mini_df=df[['tsym','cname','oi','strprc','optt','lp']]
    pe_df   =  mini_df[ mini_df['optt'] == 'PE' ]
    ce_df   =  mini_df[ mini_df['optt'] == 'CE' ]

    pe_df_sort=pe_df.sort_values(by=['strprc'],ascending=False)
    ce_df_sort=ce_df.sort_values(by=['strprc'],ascending=False)

    merge_df = pd.merge(pe_df_sort, ce_df_sort, on='strprc', how='outer')
    st.table(merge_df)