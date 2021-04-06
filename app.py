import streamlit as st
import requests
import json
import datetime
import urllib
import urllib.request
import urllib.error
import requests
import pandas as pd


st.markdown("""# Horse Arbitrator
## 🐴🐴🐴 Calculates the future odds of each horse perfectly 🐴🐴🐴
""")






# payload = 'username=' + my_username + '&password=' + my_password
# headers = {'X-Application': my_app_key, 'Content-Type': 'application/x-www-form-urlencoded'}
# resp = requests.post('https://identitysso-cert.betfair.com/api/certlogin',data=payload,cert=('test.crt','client-2048.pem'),headers=headers)
# json_resp=resp.json()
# SSOID = json_resp['sessionToken']

# eventTypeID = '["7"]' #ID for Horse Racing
# countryCode= '["GB","IE"]' #Country Codes. Betfair use Alpha-2 Codes under ISO 3166-1
# marketTypeCode='["WIN"]' #Market Type
# MarketStartTime= datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ') #Event Start and End times
# MarketEndTime = (datetime.datetime.now() + datetime.timedelta(hours=24))
# MarketEndTime = MarketEndTime.strftime('%Y-%m-%dT%H:%M:%SZ')
# maxResults = str(1000)
# sortType = 'FIRST_TO_START' #Sorts the Output
# Metadata = 'RUNNER_METADATA' #Provides metadata
# inplay = 'false' #still to run
# bet_url="https://api.betfair.com/exchange/betting/json-rpc/v1"
# user_req='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue",\
#            "params": {"filter":{"eventTypeIds":'+eventTypeID+',"marketTypeCodes":'+marketTypeCode+',\
#            "inPlayOnly":'+inplay+', "marketCountries":'+countryCode+',  \
#            "marketStartTime":{"from":"'+MarketStartTime+'", "to":"'+MarketEndTime+'"}},\
#            "sort":"'+sortType+'", "maxResults":"'+maxResults+'", "marketProjection":["'+Metadata+'"]}, "id": 1}'

# req = urllib.request.Request(bet_url, data=user_req.encode('utf-8'), headers=headers)
# response= urllib.request.urlopen(req)
# jsonResponse = response.read()
# pkg = jsonResponse.decode('utf-8')
# print(pkg)
# result = json.loads(pkg) 
# marketCatelogue = result

# print(marketCatelogue)

# bet_url="https://api.betfair.com/exchange/betting/json-rpc/v1"
# event_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
# headers = {'X-Application': my_app_key, 'X-Authentication': SSOID, 'content-type': 'application/json'}
# req = requests.post(bet_url, data=event_req.encode('utf-8'), headers=headers) 
# eventTypes = req.json()
# print(eventTypes)


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
    d = {'Horse Name': [], 'Form':[], 'Race': [], 'Odds':[]}
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
    

    for x in range(len(marketCatelogue)):
        for w in range(len(marketCatelogue[x]['runners'])):
            runnerform = marketCatelogue[x]['runners'][w]['metadata']['FORM']
            if runnerform is None:
                runnerform = 'e'
            
            runnerformList = list(runnerform)
            
            for Entry in runnerformList:
                if Entry == 'R':#refusal to jump hurdle
                    Rating = float(Rating) + float(5)
                    Index = Index + 1
                elif Entry == 'e':#First Race
                    Rating = float(Rating) + float(10)
                    Index = Index + 1
                elif Entry == '0':#finished higher than 9th
                    Rating = float(Rating) + float(10)
                    Index = Index + 1
                elif Entry == 'F':#fell
                    Rating = float(Rating) + float(5)
                    Index = Index + 1
                elif Entry == 'U':#unseated rider
                    Rating = float(Rating) + float(3)
                    Index = Index + 1
                elif Entry == 'x':#horse has not started in a race for 3 months or more
                    Rating = float(Rating) + float(3)
                    Index = Index + 1
                elif Entry == 'C':#horse has won before at this same race distance and at this same track.
                    Rating = float(Rating) + float(.5)
                    Index = Index + 1
                elif Entry == 'B':#horse started favorite at it's last start, but it did not win
                    Rating = float(Rating) + float(3.5)
                    Index = Index + 1
                elif Entry == '/':#represents two seasons ago
                    Rating = float(Rating) + float(8)
                    Index = Index + 1
                elif Entry == '-':#represents one season ago
                    Rating = float(Rating) + float(4)
                    Index = Index + 1
                elif Entry == 'P':#pulled up by jockey
                    Rating = float(Rating) + float(4)
                    Index = Index + 1
                else:
                    Rating = float(Rating) + float(Entry)
                    Index = Index + 1
                                                                
            rating = float(Rating)/float(Index)
            FormRatingList.append(rating)
                
        for t in range(len(FormRatingList)):
            if FormRatingList[t] < FormRatingAvg:
                FormRatingAvg = FormRatingList[t]
                horsename.append(marketCatelogue[x]['runners'][t]['runnerName'])
                selectionID.append(marketCatelogue[x]['runners'][t]['selectionId'])

        price_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listRunnerBook", "params": {"locale":"en", \
                    "marketId":"'+str(marketCatelogue[x]['marketId'])+'",\
                    "selectionId":"'+str(selectionID[-1])+'",\
                    "priceProjection":{"priceData":'+priceProjection+'},"orderProjection":"ALL"},"id":1}'
       
        req = urllib.request.Request(bet_url, data=price_req.encode('utf-8'), headers=headers)
        price_response= urllib.request.urlopen(req)
        price_jsonResponse = price_response.read()
        price_pkg = price_jsonResponse.decode('utf-8')
        price_result = json.loads(price_pkg) 
        

        Results = Results.append({'Horse Name':str(horsename[-1]), 'Form':str(int(FormRatingAvg)), 'Race':str(marketCatelogue[x]['marketName']), 'Odds':str(price_result['result'][0]['runners'][0]['ex']['availableToBack'][0]['price'])}, ignore_index=True)
        
        Rating = float(0)
        Index = float(0)
        FormRatingAvg = float(100)
        FormRatingList.clear()
        horsename.clear()
        selectionID.clear
                 
    return Results

a = BestHorseForm()
a
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
 
 
# def getMarketId(marketCatalougeResult):
#     if( marketCatalougeResult is not None):
#         for market in marketCatalougeResult:
#             return market['marketId']
 
 
# def getSelectionId(marketCatalougeResult):
#     if(marketCatalougeResult is not None):
#         for market in marketCatalougeResult:
#             return market['runners'][0]['selectionId']
 
# marketCatalougeResult = getMarketCatalogueForNextGBWin(7)
# marketid = getMarketId(marketCatalougeResult)
# runnerId = getSelectionId(marketCatalougeResult)

# marketCatalougeResult
# marketid
# runnerId