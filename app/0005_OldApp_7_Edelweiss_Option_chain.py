from Utils import api_utils
import time
import altair as alt
import streamlit as st
import requests,json
import pandas as pd
from datetime import datetime

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

def recordData_thiya2(expiry, scrip):
    url = "https://ewmw.edelweiss.in/api/Market/optionchainguest"
    # url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
    payload = {"exp": str(expiry), "aTyp": "OPTIDX", "uSym": scrip}
    response = requests.post(url, payload)

    jsoned_response = response.json()

    # st.write('First response')
    # st.json(jsoned_response['opChn'])

    # return jsoned_response['opChn']


    data_length = len(jsoned_response['opChn'])
    ######### Gets NIFTY and SENSEX price data
    url = "https://ewmw.edelweiss.in/api/Market/Process/GetMarketStatus/20559,26753"
    atmresponse = requests.get(url)
    jsoned_atmresponse = atmresponse.json()
    jsoned_atmresponse = json.loads(jsoned_atmresponse)

    st.write('Second response')
    st.json(jsoned_atmresponse)


    if scrip == "NIFTY":
        atm = jsoned_atmresponse['JsonData']['NSE']
        atm = round(atm / 50) * 50
    if scrip == "BANKNIFTY":
        atm = jsoned_atmresponse['JsonData']['BSE']
        atm = round(atm / 100) * 100

    # print("ATM: ", atm)

    oiData = []
    atm_premium = 0

    for i in range(data_length):
        strike = jsoned_response['opChn'][i]['stkPrc']
        strike = int(float(strike))
        ce_premium = jsoned_response['opChn'][i]['ceQt']['ltp']
        pe_premium = jsoned_response['opChn'][i]['peQt']['ltp']
        ce_oi = jsoned_response['opChn'][i]['ceQt']['opInt']
        pe_oi = jsoned_response['opChn'][i]['peQt']['opInt']
        ce_oichg = jsoned_response['opChn'][i]['ceQt']['opIntChg']
        pe_oichg = jsoned_response['opChn'][i]['peQt']['opIntChg']

        temp_dict = {}


        temp_dict['strike'] = strike
        if strike == atm:
            atm_premium = float(ce_premium) + float(pe_premium)

        temp_dict['ceOI'] = ce_oi
        temp_dict['peOI'] = pe_oi
        temp_dict['ceOIchg'] = ce_oichg
        temp_dict['peOIchg'] = pe_oichg

        oiData.append(temp_dict)

    print(atm_premium)
    time_now = datetime.now()
    time_now = time_now.strftime("%H:%M")
    data = {"time": time_now, "OI": oiData, "ATM": atm, "ATMPremium": atm_premium}
    json_data = json.dumps(data)
    # print(json_data)
    # file = open("MyOIWorld/todaysData.txt", 'a')
    # file.write(json.dumps(data))
    # file.write(json_data)
    # print(json_data)
    return jsoned_response['opChn'], json_data

def recordData_thiya(expiry, scrip):
    url = "https://ewmw.edelweiss.in/api/Market/optionchainguest"
    # url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
    payload = {"exp": str(expiry), "aTyp": "OPTIDX", "uSym": scrip}
    response = requests.post(url, payload)
    jsoned_response = response.json()
    return jsoned_response

# main

print("Start edelweiss Option chain data :")
# api_data=api_utils.edelweiss_OptionChain_thiya("01Sep2022","NIFTY")
# # st.json(api_data)
# st.write('done')



# #
# st.write('Step 1')
# df = pd.read_json(api_data)
# # st.dataframe(df.tail())
# st.write('Step 2')
# # df_1=pd.json_normalize(json.loads(df.to_json()))
# df_1=df[['OI']]
# # st.dataframe(df_1.tail())
# st.write('Step 3')
# df_2=df_1.to_json()
# # st.json(df_2)
# st.write('step 4')
# df_3 = pd.read_json(df_2)
# # st.dataframe(df_3.tail())
# st.write('step 5')
# df_4=pd.json_normalize(df_3['OI'])
# st.dataframe(df_4)


#############################

# st.write('Altair chart')
# alt_df=df_4[['strike','ceOI','ceOIchg']]
# c = alt.Chart(alt_df).mark_circle().encode(
#      x='strike', y='ceOI', size='ceOIchg', color='c', tooltip=['strike', 'ceOI', 'ceOIchg'])
#
# st.altair_chart(c, width='stretch')

# st.write('Line chart')
# st.line_chart(df_4,  x='ceOI',y='strike')
# st.bar_chart(df_4,  x='ceOI',y='strike')
# st.bar_chart(df_4,  y='ceOI',x='strike')
# st.line_chart(df_4,  x='peOI',y='strike')
# st.write('Bar chart')
# st.bar_chart(df_4, x=['ceOI','peOI'],y='strike')
# st.bar_chart(df_4, x='ceOI',y='strike')
# st.bar_chart(df_4, x='ceOIchg',y='strike')
# # st.bar_chart(df_4, y='ceOI',x='strike')
# st.line_chart(df_4)
# st.area_chart(df_4)
# st.area_chart(df_4)

#########################################
# st.area_chart(df_4)

# st.write('eeeeeeeeee')
# df = pd.json_normalize(api_data,record_path=['OI'])
# st.dataframe(df.tail())
#
# st.write('222222')
# # df_nested_list = pd.json_normalize(df, record_path =['OI'])
# # st.table(df_nested_list)
# df_OI=df['OI']
# st.dataframe(df_OI.tail())
#
# st.write('3333')
# OI_df_normalized=pd.read_json(df_OI)
# st.dataframe(OI_df_normalized.tail())


#### main for testing


st.header("**Start edelweiss Option chain data :**")
# api_data1, api_data2=recordData_thiya2("01Sep2022","NIFTY")
api_data1=api_utils.edelweiss_OptionChain_thiya("01Sep2022","NIFTY")
st.json(api_data1)
# # st.write('done')
# print("API fetch completed... lets display")
# st.json(api_data1['opChn'])
# print("DF generated")
df=pd.json_normalize(api_data1['opChn'])
st.dataframe(df)
# new_df=df[['stkPrc','atm','ceQt.ltp','ceQt.trdSym']]

new_df=df[['stkPrc','atm',
           'ceQt.trdSym','ceQt.ltp','ceQt.chg','ceQt.chgP',
           'ceQt.bidPr','ceQt.askPr','ceQt.vol',
           'ceQt.opInt','ceQt.opIntChg',
           'ceQt.ltpivfut','ceQt.ltpivspt',
           'peQt.trdSym', 'peQt.ltp', 'peQt.chg', 'peQt.chgP',
           'peQt.bidPr', 'peQt.askPr', 'peQt.vol',
           'peQt.opInt', 'peQt.opIntChg',
          'peQt.ltpivfut', 'peQt.ltpivspt',
           ]]
st.write("New DF generated")
st.dataframe(new_df)

## just to get df column names
# for col in df.columns:
#     st.write(col)

# peQT.OpInt, peQt.chg, chgP, vol, bidPr, askPr, ltp, trdSym, ltpivspt

# st.table()
# st.dataframe(pd.json_normalize(api_data1))

# ############## Below is successful in getting Nifty_spot & BN Spot
#
# json_data=api_utils.edelweiss_nse_index_data()
# st.json(json_data)
# st.write('Now get the Nifty/BN data')
# l_time=json_data['JsonData']['NSEltt']
# l_nifty=json_data['JsonData']['NSE']
# l_niftyChg=json_data['JsonData']['NSEchg']
# l_niftyChgPct=json_data['JsonData']['NSEchgp']
# l_BN=json_data['JsonData']['BSE']
# l_BNChg=json_data['JsonData']['BSEchg']
# l_BNChgPct=json_data['JsonData']['BSEchgp']
#
##################################################