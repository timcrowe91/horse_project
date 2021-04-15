import streamlit as st
from time import time, sleep
import pandas as pd
from data_model.data import BestHorseForm , get_classification, get_linear
from data_model.preprocessing_rex import filter_data, filter_new_data, final_results
import numpy as np


st.markdown(
    """
    <style>
    .reportview-container {
        background-image: url("https://i.ibb.co/XWYJQJX/horse-race.png");
        background-size: cover;
    }
   .sidebar .sidebar-content {
        background: url("https://i.ibb.co/XWYJQJX/horse-race.png")
    }
    </style>
    """,
    unsafe_allow_html=True
    )


st.markdown("""# Horse Arbitrator
## 🐎🐎🐎 Calculates the future odds of each horse perfectly 🐴🐴🐴
### Here is a list of current horses
""")

# X,y,model = get_model()
# prediction=model.predict(X[0])
# prediction


# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)


# filename = file_selector()
# st.write('You selected `%s`' % filename)

# uploaded_file = st.file_uploader("Upload csv file", type=["csv","npy"])
# uploaded_file_y = st.file_uploader("Upload y_0 file", type=["csv","npy"])
# uploaded_file_yy = st.file_uploader("Upload y_5 file", type=["csv","npy"])
# if uploaded_file is not None:
#     if uploaded_file_y is not None:
#         if uploaded_file_yy is not None:
#     # scaled_X, scaled_y = filter_new_data(uploaded_file)
#            

uploaded_file = st.file_uploader("Upload csv file", type=["csv"])
if uploaded_file is not None:
    # X, y_20s, y_0s = filter_data(uploaded_file)
    X, y_20, y_0 = filter_new_data(uploaded_file)
    class_model = get_classification()
    linear_model = get_linear()
    class_prediction = class_model.predict(X)

    lin_prediction = linear_model.predict(X)
    pred_df, real_pnl, mm_pnl, perc_correct, numbets = final_results(y_0, lin_prediction, y_20, class_prediction)
    st.markdown(f'Total PnL: {real_pnl}')
    st.markdown(f'Theoretical Mid-Market PnL: {mm_pnl}')
    st.markdown(f'% Correctly Predicted Price Movement: {perc_correct}')
    st.markdown(f'Number of Bets: {numbets}')

    st.write(pred_df)

    



df = pd.DataFrame(columns=['horse_name','back_odds_3','back_avail_3','back_odds_2',\
                            'back_avail_2','back_odds_1','back_avail_1','lay_odds_1',\
                            'lay_avail_1','lay_odds_2','lay_avail_2','lay_odds_3','lay_avail_3',\
                            'last_price','TotalMatched'])


placeholder = st.empty()

with placeholder.beta_container():
    a,b = BestHorseForm()
    st.markdown(f"### Predictions for event number {b}")
    st.write(a)
sleep(5)



while True:
    placeholder.empty()
    with placeholder.beta_container():
        a,b = BestHorseForm()
        st.markdown(f"### Predictions for event number {b}")
        st.write(a)
        df = df.append(a)
    sleep(5)



# price, b = BestHorseForm()
# st.markdown(f"### Predictions for event number {b}")
# st.write(price)



#    price_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params":\
#     {"marketIds":["1.181564117"],"priceProjection":{"priceData":["EX_BEST_OFFERS","EX_TRADED"],"virtualise": "true"}}, "id": 1}]' 
#     req = urllib.request.Request(bet_url, data=price_req.encode('utf-8'), headers=headers)
#     price_response= urllib.request.urlopen(req)
#     price_jsonResponse = price_response.read()
#     price_pkg = price_jsonResponse.decode('utf-8')
#     price_response = json.loads(price_pkg) 



#     for x in range(len(marketCatelogue)):
#         for w in range(len(marketCatelogue[x]['runners'])):
#             runnerform = marketCatelogue[x]['runners'][w]['metadata']['FORM']
#             if runnerform is None:
#                 runnerform = 'e'
            
#             runnerformList = list(runnerform)
            
#             for Entry in runnerformList:
#                 if Entry == 'R':#refusal to jump hurdle
#                     Rating = float(Rating) + float(5)
#                     Index = Index + 1
#                 elif Entry == 'e':#First Race
#                     Rating = float(Rating) + float(10)
#                     Index = Index + 1
#                 elif Entry == '0':#finished higher than 9th
#                     Rating = float(Rating) + float(10)
#                     Index = Index + 1
#                 elif Entry == 'F':#fell
#                     Rating = float(Rating) + float(5)
#                     Index = Index + 1
#                 elif Entry == 'U':#unseated rider
#                     Rating = float(Rating) + float(3)
#                     Index = Index + 1
#                 elif Entry == 'x':#horse has not started in a race for 3 months or more
#                     Rating = float(Rating) + float(3)
#                     Index = Index + 1
#                 elif Entry == 'C':#horse has won before at this same race distance and at this same track.
#                     Rating = float(Rating) + float(.5)
#                     Index = Index + 1
#                 elif Entry == 'B':#horse started favorite at it's last start, but it did not win
#                     Rating = float(Rating) + float(3.5)
#                     Index = Index + 1
#                 elif Entry == '/':#represents two seasons ago
#                     Rating = float(Rating) + float(8)
#                     Index = Index + 1
#                 elif Entry == '-':#represents one season ago
#                     Rating = float(Rating) + float(4)
#                     Index = Index + 1
#                 elif Entry == 'P':#pulled up by jockey
#                     Rating = float(Rating) + float(4)
#                     Index = Index + 1
#                 else:
#                     Rating = float(Rating) + float(Entry)
#                     Index = Index + 1
                                                                
#             rating = float(Rating)/float(Index)
#             FormRatingList.append(rating)
                
#         for t in range(len(FormRatingList)):
#             if FormRatingList[t] < FormRatingAvg:
#                 FormRatingAvg = FormRatingList[t]
#                 horsename.append(marketCatelogue[x]['runners'][t]['runnerName'])
#                 selectionID.append(marketCatelogue[x]['runners'][t]['selectionId'])

#         price_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listRunnerBook", "params": {"locale":"en", \
#                     "marketId":"'+str(marketCatelogue[x]['marketId'])+'",\
#                     "selectionId":"'+str(selectionID[-1])+'",\
#                     "priceProjection":{"priceData":'+priceProjection+'},"orderProjection":"ALL"},"id":1}'
       
#         req = urllib.request.Request(bet_url, data=price_req.encode('utf-8'), headers=headers)
#         price_response= urllib.request.urlopen(req)
#         price_jsonResponse = price_response.read()
#         price_pkg = price_jsonResponse.decode('utf-8')
#         price_result = json.loads(price_pkg) 
        

#         Results = Results.append({'Horse Name':str(horsename[-1]), 'Form':str(int(FormRatingAvg)), 'Race':str(marketCatelogue[x]['marketName']), 'Back_Odds':str(price_result['result'][0]['runners'][0]['ex']['availableToBack']),'Lay_Odds':str(price_result['result'][0]['runners'][0]['ex']['availableToLay'])}, ignore_index=True)
        
#         Rating = float(0)
#         Index = float(0)
#         FormRatingAvg = float(100)
#         FormRatingList.clear()
#         horsename.clear()
#         # selectionID.clear     
#     return Results


    
# def getMarketCatalogueForNextGBWin(eventTypeID):
#     if (eventTypeID is not None):
#         print( 'Calling listMarketCatalouge Operation to get MarketID and selectionId')
#         now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
#         market_catalogue_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventTypeIds":["' + eventTypeID + '"],"marketCountries":["GB"],"marketTypeCodes":["WIN"],'\
#                                                                                                                                                              '"marketStartTime":{"from":"' + now + '"}},"sort":"FIRST_TO_START","maxResults":"1","marketProjection":["RUNNER_METADATA"]}, "id": 1}'
#         """
#         print  market_catalogue_req
#         """
#         market_catalogue_response = callAping(market_catalogue_req)
#         """
#         print market_catalogue_response
#         """
#         market_catalouge_loads = json.loads(market_catalogue_response)
#         try:
#             market_catalouge_results = market_catalouge_loads['result']
#             return market_catalouge_results
#         except:
#             print  ('Exception from API-NG' + str(market_catalouge_results['error']))
#             exit()
 



# my_username = "elabentrepreneurs@gmail.com"
# my_password = "DanielTimLuis1!"
# appKey = "vdkWr93gI1x7WEQ3"
# payload = 'username=' + my_username + '&password=' + my_password
# headers = {'X-Application': appKey, 'Content-Type': 'application/x-www-form-urlencoded'}
# resp = requests.post('https://identitysso-cert.betfair.com/api/certlogin',data=payload,cert=('test.crt','client-2048.pem'),headers=headers)
# resp_json=resp.json()
# SSOID = resp_json['sessionToken']



# URL = url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
# jsonrpc_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
# headers = {'X-Application': appKey, 'X-Authentication': SSOID, 'content-type': 'application/json'}
 
# def callAping(jsonrpc_req):
#     req = urllib.request.Request(url, jsonrpc_req, headers)
#     response = urllib.request.urlopen(req)
#     jsonResponse = response.read()
#     return jsonResponse


# def getMarketCatalogueForNextGBWin(eventTypeID):
#     if (eventTypeID is not None):
#         print ('Calling listMarketCatalouge Operation to get MarketID and selectionId')
#         now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
#         market_catalogue_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventTypeIds":["' + eventTypeID + '"],"marketCountries":["GB","IE"],"marketTypeCodes":["WIN"],'\
#                                                                                                                                                              '"marketStartTime":{"from":"' + now + '"}},"sort":"FIRST_TO_START","maxResults":"1","marketProjection":["RUNNER_METADATA"]}, "id": 1}'
#         """
#         print  market_catalogue_req
#         """
#         market_catalogue_response = callAping(market_catalogue_req)
#         """
#         print market_catalogue_response
#         """
#         market_catalouge_loads = json.loads(market_catalogue_response)
#         try:
#             market_catalouge_results = market_catalouge_loads['result']
#             return market_catalouge_results
#         except:
#             print  ('Exception from API-NG' + str(market_catalouge_results['error']))
#             exit()

# a=getMarketCatalogueForNextGBWin('["7"]'.encode('utf-8'))
# a