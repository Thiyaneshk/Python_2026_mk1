import pandas as pd
import datetime
import Utils.utils
from Utils import api_utils
import streamlit as st

st.markdown('''# **Nifty Dashboard**''')
# Custom function for rounding values
def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value, 2))
    else:
        a = float(round(input_value, 8))
    return a

## Main starts here
nse_data=api_utils.edelweiss_nse_index_data()

# st.write(nse_data)
l_time=nse_data['JsonData']['NSEltt']
l_nifty=nse_data['JsonData']['NSE']
l_niftyChg=nse_data['JsonData']['NSEchg']
l_niftyChgPct=nse_data['JsonData']['NSEchgp']
l_BN=nse_data['JsonData']['BSE']
l_BNChg=nse_data['JsonData']['BSEchg']
l_BNChgPct=nse_data['JsonData']['BSEchgp']

# st.warning(l_time)
expiry_dt_selected = Utils.utils.get_exp_date()
Index_selection=st.selectbox( 'Select Index :', ['NIFTY','BANKNIFTY'])
# Create 3 columns to display dashboard
col1, col2, col3 = st.columns(3)

# Select the priceChangePercent column
col1_percent = f'{float(l_niftyChgPct)}%'
col2_percent = f'{float(l_BNChgPct)}%'
# Create a metrics price box
col1.metric("Nifty", l_nifty, col1_percent)
col2.metric("Bank Nifty", l_BN, col2_percent)
col3.metric("Data of ", l_time, datetime.datetime.now().strftime("%Y-%b-%d, %A %I:%M:%S"))
col1.metric("Nifty Change", l_niftyChg, 0)
col2.metric("BN Change", l_BNChg, 0)
col3.metric("**Expiry Selected**", Index_selection, expiry_dt_selected)

# st.write("Expiry selected ", expiry_dt_selected)
# st.header('**Option chain**')
# Option_df=api_utils.edelweiss_OptionChain_Df("01Sep2022","NIFTY")
Option_df=api_utils.edelweiss_OptionChain_Df(expiry_dt_selected,Index_selection)
# pd.set_option('precision', 0)
#
pd.to_numeric(Option_df['peQt.opInt'])
pd.to_numeric(Option_df['ceQt.opInt'])

put_oi = Option_df['peQt.opInt'].sum()
call_oi = Option_df['ceQt.opInt'].sum()

pcr=round(put_oi/call_oi,3)

st.write("Puts :",put_oi, "  Calls : ", call_oi, "  PCR : ",pcr)
st.write("Puts :",put_oi, "  Calls : ", call_oi, "  PCR : ",pcr)



# st.table(Option_df)


df1 = Option_df[[
    # 'stkPrc',
             'ceQt.opInt','peQt.opInt'
             ]]
df2=Option_df[['ceQt.opIntChg','peQt.opIntChg']]
mid_rw = round(len(Option_df)/2)
st.write("Mid strike is ",mid_rw)
no_of_strike=10
OI_df=df1.iloc[mid_rw-no_of_strike:mid_rw+no_of_strike]
OI_Chg_df=df2.iloc[mid_rw-no_of_strike:mid_rw+no_of_strike]
start_stike, end_stike = st.select_slider(
     'Select a range of Strike',
     options=['14000','15000','16000','17000','17500','18000','18500','19000'],
     value=('17000', '18000') )
st.write('You selected strikes between', start_stike, 'and', end_stike)

temp_df = df1.loc[(df1.index >= float(start_stike) ) &  (df1.index <= float(end_stike)) ]
# st.table(OI_df)
# st.table(OI_Chg_df)
Consolidated_OI_Chg_df=Option_df[['ceQt.opInt','ceQt.opIntChg','peQt.opInt','peQt.opIntChg']]
# new_df.set_index('stkPrc', inplace=True)
st.write('** OP Df **')
# st.table(OI_df)
# st.table(OI_Chg_df)
# st.table(Consolidated_OI_Chg_df)

# st.bar_chart(new_df,y=new_df['stkPrc'],x=new_df['ceQt.opInt'])
oi_c1, oi_c2 =st.columns(2)

with oi_c1:
    st.header("OI Chart")
    st.bar_chart(temp_df)

    st.header("OI Change")
    st.bar_chart(OI_Chg_df)

with oi_c2:
    st.header("OI Chart - Area")
    st.area_chart(OI_df)
    # st.bar_chart(OI_Chg_df)
    st.header("OI Change - Area")
    st.area_chart(OI_Chg_df)

# with oi_c3:
# st.bar_chart(Consolidated_OI_Chg_df)
# st.bar_chart(Option_df)
# st.altair_chart(Consolidated_OI_Chg_df)

st.header('**Option chain**')
st.table(Option_df)
