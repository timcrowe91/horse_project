import streamlit as st
import requests
import json
import datetime
import urllib
import urllib.request
import urllib.error
import requests
import pandas as pd
from time import time, sleep
from data import get_model

st.markdown("""# Horse Arbitrator
## 🐴🐴🐴 Calculates the future odds of each horse perfectly 🐴🐴🐴
### Here is a list of current horses
""")


def BestHorseForm():
    
    Rating = float(0)
    Index = float(0)
    FormRatingAvg = float(100)
    FormRatingList = []
    horsename = []
    selectionID=[]
    
    eventTypeID = '["7"]' #ID for Horse Racing
    countryCode= '["GB","IE"]' #Country Codes. Betfair use Alpha-2 Codes under ISO 3166-1
    marketTypeCode='["WIN"]' #Market Type
    MarketStartTime= datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ') #Event Start and End times
    MarketEndTime = (datetime.datetime.now() + datetime.timedelta(hours=24))
    MarketEndTime = MarketEndTime.strftime('%Y-%m-%dT%H:%M:%SZ')
    maxResults = str(1000)
    sortType = 'FIRST_TO_START' #Sorts the Output
    Metadata = 'RUNNER_METADATA' #Provides metadata
    inplay = 'false' #still to run
    priceProjection = '["EX_BEST_OFFERS"]'#Best odds
    
    #Create an empty dataframe
    d = {'Horse Name': [], 'Form':[], 'Race': [], 'Back_Odds':[], 'Lay_Odds':[]}
    Results = pd.DataFrame(data=d)
    
    my_username = "elabentrepreneurs@gmail.com"
    my_password = "DanielTimLuis1!"
    my_app_key = "vdkWr93gI1x7WEQ3"

    payload = 'username=' + my_username + '&password=' + my_password
    headers = {'X-Application': my_app_key, 'Content-Type': 'application/x-www-form-urlencoded'}
    bet_url="https://api.betfair.com/exchange/betting/json-rpc/v1"
    resp = requests.post('https://identitysso-cert.betfair.com/api/certlogin',data=payload,cert=('test.crt','client-2048.pem'),headers=headers)
    resp_json=resp.json()
    SSOID = resp_json['sessionToken']
    
    headers = {'X-Application': my_app_key, 'X-Authentication': SSOID, 'content-type': 'application/json'}
    
    user_req='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue",\
           "params": {"filter":{"eventTypeIds":'+eventTypeID+',"marketTypeCodes":'+marketTypeCode+',\
           "inPlayOnly":'+inplay+', "marketCountries":'+countryCode+',\
           "marketStartTime":{"from":"'+MarketStartTime+'", "to":"'+MarketEndTime+'"}},\
           "sort":"'+sortType+'", "maxResults":"'+maxResults+'", "marketProjection":["'+Metadata+'"]}, "id": 1}'

    req = urllib.request.Request(bet_url, data=user_req.encode('utf-8'), headers=headers)
    response= urllib.request.urlopen(req)
    jsonResponse = response.read()
    pkg = jsonResponse.decode('utf-8')
    result = json.loads(pkg) 
    marketCatelogue = result['result']
    a=[]
    sel = []
    market_id = marketCatelogue[0]['marketId']
    for i in range(len(marketCatelogue[0]['runners'])):
        a.append(marketCatelogue[0]['runners'][i]["runnerName"])
        sel.append(marketCatelogue[0]['runners'][i]["selectionId"])

    back_odds_1 = []
    back_avail_1 = []
    back_odds_2 = []
    back_avail_2 = []
    back_odds_3 = []
    back_avail_3 = []
    lay_odds_1=[]
    lay_avail_1=[]
    lay_odds_2=[]
    lay_avail_2 =[]
    lay_odds_3=[]
    lay_avail_3 =[]
    total_matched=[]
    last_price =[]
    for i in range(len(sel)):  
        price_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listRunnerBook",\
            "params": {"locale":"en", \
                "marketId":"'+str(market_id)+'",\
                        "selectionId":"'+str(sel[i])+'",\
                        "priceProjection":{"priceData":'+priceProjection+'},"orderProjection":"ALL"},"id":1}'
       
        req = urllib.request.Request(bet_url, data=price_req.encode('utf-8'), headers=headers)
        price_response= urllib.request.urlopen(req)
        price_jsonResponse = price_response.read()
        price_pkg = price_jsonResponse.decode('utf-8')
        price_result = json.loads(price_pkg) 
        if price_result['result'][0]['runners'][0]['status'] == 'REMOVED':
            back_odds_1.append('removed')
            back_avail_1.append('removed')
            back_odds_2.append('removed')
            back_avail_2.append('removed')
            back_odds_3.append('removed')
            back_avail_3.append('removed')
            lay_odds_1.append('removed')
            lay_avail_1.append('removed')
            lay_odds_2.append('removed')
            lay_avail_2.append('removed')
            lay_odds_3.append('removed')
            lay_avail_3.append('removed')
            last_price.append('removed')
            total_matched.append('removed')
        else:
            back_odds_1.append(price_result['result'][0]['runners'][0]['ex']['availableToBack'][0]['price'])
            back_avail_1.append(price_result['result'][0]['runners'][0]['ex']['availableToBack'][0]['size'])
            back_odds_2.append(price_result['result'][0]['runners'][0]['ex']["availableToBack"][1]['price'])
            back_avail_2.append(price_result['result'][0]['runners'][0]['ex']["availableToBack"][1]['size'])
            back_odds_3.append(price_result['result'][0]['runners'][0]['ex']["availableToBack"][2]['price'])
            back_avail_3.append(price_result['result'][0]['runners'][0]['ex']["availableToBack"][2]['size'])
            if len(price_result['result'][0]['runners'][0]['ex']['availableToLay']) == 0:
                lay_odds_1.append(0)
                lay_avail_1.append(0)
                lay_odds_2.append(0)
                lay_avail_2.append(0)
                lay_odds_3.append(0)
                lay_avail_3.append(0)
            if len(price_result['result'][0]['runners'][0]['ex']['availableToLay']) == 1:
                lay_odds_1.append(price_result['result'][0]['runners'][0]['ex']['availableToLay'][0]['price'])
                lay_avail_1.append(price_result['result'][0]['runners'][0]['ex']['availableToLay'][0]['size'])
                lay_odds_2.append(0)
                lay_avail_2.append(0)
                lay_odds_3.append(0)
                lay_avail_3.append(0)
            if len(price_result['result'][0]['runners'][0]['ex']['availableToLay']) == 2:
                lay_odds_1.append(price_result['result'][0]['runners'][0]['ex']['availableToLay'][0]['price'])
                lay_avail_1.append(price_result['result'][0]['runners'][0]['ex']['availableToLay'][0]['size'])
                lay_odds_2.append(price_result['result'][0]['runners'][0]['ex']["availableToLay"][1]['price'])
                lay_avail_2.append(price_result['result'][0]['runners'][0]['ex']["availableToLay"][1]['size'])
                lay_odds_3.append(0)
                lay_avail_3.append(0)
            if len(price_result['result'][0]['runners'][0]['ex']['availableToLay']) == 3:
                lay_odds_1.append(price_result['result'][0]['runners'][0]['ex']['availableToLay'][0]['price'])
                lay_avail_1.append(price_result['result'][0]['runners'][0]['ex']['availableToLay'][0]['size'])
                lay_odds_2.append(price_result['result'][0]['runners'][0]['ex']["availableToLay"][1]['price'])
                lay_avail_2.append(price_result['result'][0]['runners'][0]['ex']["availableToLay"][1]['size'])
                lay_odds_3.append(price_result['result'][0]['runners'][0]['ex']["availableToLay"][2]['price'])
                lay_avail_3.append(price_result['result'][0]['runners'][0]['ex']["availableToLay"][2]['size'])
            total_matched.append(price_result['result'][0]['runners'][0]['totalMatched'])
            last_price.append(price_result['result'][0]['runners'][0]["lastPriceTraded"])


    df = pd.DataFrame()
    df['horse_name']=a
    df['back_odds_3']= back_odds_3
    df['back_avail_3']= back_avail_3
    df['back_odds_2']= back_odds_2
    df['back_avail_2']= back_avail_2
    df['back_odds_1']= back_odds_1
    df['back_avail_1'] = back_avail_1
    df['lay_odds_1']= lay_odds_1
    df['lay_avail_1'] = lay_avail_1
    df['lay_odds_2']= lay_odds_2
    df['lay_avail_2'] = lay_avail_2
    df['lay_odds_3']= lay_odds_3
    df['lay_avail_3'] = lay_avail_3
    df['last_price'] = last_price
    df['TotalMatched'] = total_matched

    return df, market_id

X,y,model = get_model()
prediction=model.predict(X[0])
prediction
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