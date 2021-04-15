import pandas as pd
import numpy as np
import requests
import json
import datetime
import urllib
# import urllib.request
# import urllib.error
import requests
import pandas as pd
from tensorflow.keras.models import load_model
# import tflite_runtime.interpreter as tflite
# X = pd.read_csv('raw_data/test_data_X.csv')
# y_test = pd.read_csv('raw_data/test_data_y.csv')

# X = X.drop(columns='Unnamed: 0')
# X = np.array(X)
# X = X.reshape(1413,24,5)



def get_classification():
    new_model  = load_model('data_model/Final-Classification-Model.h5')
    return new_model

def get_linear():
    new_model  = load_model('data_model/Final-Linear-Model.h5')
    return new_model



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
    resp = requests.post('https://identitysso-cert.betfair.com/api/certlogin',data=payload,cert=('data_model/test.crt','data_model/client-2048.pem'),headers=headers)
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
            if "lastPriceTraded" in price_result['result'][0]['runners'][0]:
                last_price.append(price_result['result'][0]['runners'][0]["lastPriceTraded"])
            else:
                last_price.append(0)


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


# if __name__ == '__main__':
#     X,y_test,new_model= get_model()