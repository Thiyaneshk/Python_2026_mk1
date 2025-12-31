import pandas as pd
import datetime
import Utils.utils
from Utils import api_utils
import streamlit as st
import matplotlib.pyplot as plt

st.markdown('''**Nifty Dashboard **''')
# st.header(datetime.datetime.now().strftime("%Y-%b-%d, %A %I:%M:%S"))
# Custom function for rounding values
def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value, 2))
    else:
        a = float(round(input_value, 8))
    return a

def f_pcr(l_df):
    put_oi  =sum(l_df['peQt.opInt'].astype(float).astype(int))
    call_oi =sum(l_df['ceQt.opInt'].astype(float).astype(int))
    pcr = round(put_oi / call_oi, 3)
    return put_oi,call_oi,pcr

## Main starts here
sel1, sel2,sel3  = st.columns(3)

with sel1:
    nse_data=api_utils.edelweiss_nse_index_data()
    l_time=nse_data['JsonData']['NSEltt']
    l_nifty=nse_data['JsonData']['NSE']
    l_niftyChg=nse_data['JsonData']['NSEchg']
    l_niftyChgPct=nse_data['JsonData']['NSEchgp']
    l_BN=nse_data['JsonData']['BSE']
    l_BNChg=nse_data['JsonData']['BSEchg']
    l_BNChgPct=nse_data['JsonData']['BSEchgp']

    st.metric("Nifty", l_nifty, f'{float(l_niftyChgPct)}%')
    st.metric("Bank Nifty", l_BN, f'{float(l_BNChgPct)}%')

with sel2:
    expiry_dt_selected = Utils.utils.get_exp_date()
    st.warning( 'Data : ' + l_time)

with sel3:
    nifty_range, nifty_Option_df = api_utils.edelweiss_OptionChain_Df_v1(expiry_dt_selected, "NIFTY")
    BN_range, BN_Option_df = api_utils.edelweiss_OptionChain_Df_v1(expiry_dt_selected, "BANKNIFTY")

    nifty_start_stike, nifty_end_stike = st.select_slider(
        'Select Nifty Range',
        options=nifty_range,
        value=(min(nifty_range),max(nifty_range)))

    BN_start_stike, BN_end_stike = st.select_slider(
        'Select BN Range',
        options=BN_range,
        value=(min(BN_range),max(BN_range)))

tab1, tab2, tab3 = st.tabs(["Nifty Option Chain", "BN Option Chain", "PCR / OI Chg"])

with tab1:
    st.header("Nifty Option Chain")
    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    st.table(nifty_Option_df)

with tab2:
    st.header("BN Option Chain")
    st.table(BN_Option_df)

    with tab3:
        st.header("PCR")
        nifty_put_oi, nifty_call_oi, nifty_pcr = f_pcr(nifty_Option_df)
        BN_put_oi, BN_call_oi, BN_pcr = f_pcr(BN_Option_df)

        NiftyPCR, BNPCR = st.columns(2)
        with NiftyPCR:
            st.subheader("Nifty PCR : "+str(nifty_pcr))
            labels = 'Nifty Puts ' +str(nifty_put_oi), 'Nifty Calls' +str(nifty_call_oi)
            OI = [nifty_put_oi, nifty_call_oi]
            explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
            fig1, ax1 = plt.subplots()
            ax1.pie(OI, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

        ## Bank nifty Pie chart
        with BNPCR:
            st.subheader("Bank Nifty PCR : "+str(BN_pcr))
            labels = 'Nifty Puts ' +str(BN_put_oi), 'Nifty Calls' +str(BN_call_oi)
            labels = 'BN Puts', 'BN Calls'
            OI = [BN_put_oi, BN_call_oi]
            explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
            fig1, ax1 = plt.subplots()
            ax1.pie(OI, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)


# nifty_range, nifty_Option_df=api_utils.edelweiss_OptionChain_Df_v1(expiry_dt_selected,"NIFTY")
# BN_range, BN_Option_df=api_utils.edelweiss_OptionChain_Df_v1(expiry_dt_selected,"BANKNIFTY")
#
# st.write(nifty_range)
#
# st.write(BN_range)



##############
#
# # Create 3 columns to display dashboard
# col1, col2, col3 = st.columns(3)
#
# # Select the priceChangePercent column
# col1_percent = f'{float(l_niftyChgPct)}%'
# col2_percent = f'{float(l_BNChgPct)}%'
# # Create a metrics price box
# col1.metric("Nifty", l_nifty, col1_percent)
# col2.metric("Bank Nifty", l_BN, col2_percent)
# col3.metric("Data of ", l_time, datetime.datetime.now().strftime("%Y-%b-%d, %A %I:%M:%S"))
# col1.metric("Nifty Change", l_niftyChg, 0)
# col2.metric("BN Change", l_BNChg, 0)
# col3.metric("**Expiry Selected**", Index_selection, expiry_dt_selected)
#
# # st.write("Expiry selected ", expiry_dt_selected)
# # st.header('**Option chain**')
# # Option_df=api_utils.edelweiss_OptionChain_Df("01Sep2022","NIFTY")
#
# ## Get the data from API
# # Option_df=api_utils.edelweiss_OptionChain_Df(expiry_dt_selected,Index_selection)
#
# # pd.set_option('precision', 0)
# #
# pd.to_numeric(Option_df['peQt.opInt'])
# pd.to_numeric(Option_df['ceQt.opInt'])
#
# put_oi = Option_df['peQt.opInt'].sum()
# call_oi = Option_df['ceQt.opInt'].sum()
#
# pcr=round(put_oi/call_oi,3)
#
# st.write("Puts :",put_oi, "  Calls : ", call_oi, "  PCR : ",pcr)
#
#
#
# # st.table(Option_df)
#
#
# df1 = Option_df[[
#     # 'stkPrc',
#              'ceQt.opInt','peQt.opInt'
#              ]]
# df2=Option_df[['ceQt.opIntChg','peQt.opIntChg']]
# mid_rw = round(len(Option_df)/2)
# st.write("Mid strike is ",mid_rw)
# no_of_strike=10
# OI_df=df1.iloc[mid_rw-no_of_strike:mid_rw+no_of_strike]
# OI_Chg_df=df2.iloc[mid_rw-no_of_strike:mid_rw+no_of_strike]
# # start_stike, end_stike = st.select_slider(
# #      'Select a range of Strike',
# #      options=['14000','15000','16000','17000','17500','18000','18500','19000'],
# #      value=('17000', '18000') )
# # st.write('You selected strikes between', start_stike, 'and', end_stike)
#
# temp_df = df1.loc[(df1.index >= float(start_stike) ) &  (df1.index <= float(end_stike)) ]
# # st.table(OI_df)
# # st.table(OI_Chg_df)
# Consolidated_OI_Chg_df=Option_df[['ceQt.opInt','ceQt.opIntChg','peQt.opInt','peQt.opIntChg']]
# # new_df.set_index('stkPrc', inplace=True)
# st.write('** OP Df **')
# # st.table(OI_df)
# # st.table(OI_Chg_df)
# # st.table(Consolidated_OI_Chg_df)
#
# # st.bar_chart(new_df,y=new_df['stkPrc'],x=new_df['ceQt.opInt'])
# oi_c1, oi_c2 =st.columns(2)
#
# with oi_c1:
#     st.header("OI Chart")
#     st.bar_chart(temp_df)
#
#     st.header("OI Change")
#     st.bar_chart(OI_Chg_df)
#
# with oi_c2:
#     st.header("OI Chart - Area")
#     st.area_chart(OI_df)
#     # st.bar_chart(OI_Chg_df)
#     st.header("OI Change - Area")
#     st.area_chart(OI_Chg_df)
#
# # with oi_c3:
# # st.bar_chart(Consolidated_OI_Chg_df)
# # st.bar_chart(Option_df)
# # st.altair_chart(Consolidated_OI_Chg_df)
#
# st.header('**Option chain**')
# st.table(Option_df)
#
#
# ###################