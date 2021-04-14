import streamlit as st
from time import time, sleep
import pandas as pd
from data_model.data import BestHorseForm, get_classification, get_linear
from data_model.preprocessing import filter_new_data 
import numpy as np

# import requests as re
# import json


page_bg_img = '''
<style>
body {
background-image: url("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMSEhUSEhMVFRUXFRcXFRUVGBcXFxcVFxcXFxUVFRUYHSggGBolHRcXITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OFxAQFysdHR8tLSstKy0tLSstLS0rLSstLSstLS0rLS0tLSstLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAMEBBgMBIgACEQEDEQH/xAAbAAACAgMBAAAAAAAAAAAAAAAAAQIEAwUGB//EAEEQAAIBAgQDBQUEBwYHAAAAAAABAgMRBBIhMQVBUQYTImFxMoGRobEUQsHRUmJygpLh8BYjM0NTsiREY4OzwtP/xAAZAQEBAQEBAQAAAAAAAAAAAAAAAQIDBAX/xAAkEQEAAwABBQEAAQUAAAAAAAAAAQIRAxITITFRQQQiI1Jhcf/aAAwDAQACEQMRAD8AEA0Kx6XjAgAIAsNBYAsIYAArACAdgALgABcGwBIGi3Tw0UlKpNJPZKWr9FYq8R7TYSiskaMKkrbrX4tt3ZytzVic9uteK0xpGvwfFFUqzpKLWRzjJt84ysklbmtfIpYbtNGcpOtCnSh91U4zc29dLJ5bebsaTE8USxMsRQU4Xyu0nFtyWjfhVrNciTy/G68P13F+gGv4Zxt4mU094pO9kvDs9t7O3xNidK26o1xtXpnDCwXFc0ydgFcdwAAAAAAAAAAAABADALgRSQrghMqABpCYBcdyNgAlcQAAAAAADABITkopzkm0tkub5Il6b8kaftRjXCCox3ftPp+r6nLltkeHTir1S0vFuJSqTcpN3fLoui6IoEfNiUzzxGPYnKNwjRVidFOXJszxgTRQwvEZ0KinD093NHf4DFKrTjUjony6PnF+n0sef4ig0/Iu8H4m6D6xftRvZX5PyZ2pbHLkp1Q7sDR0O01HMo1M1Jv2XJZoSXJqcfxSN0n7+jW3uZ3iYn08sxMe0gACoB3EADALiAYAgAAAABjE2hkWEURGhFQ0JhcAAAGAgAp8Tx8KEHOb9Fzb6IKtylb8yvQx1KcssKkJSW6TTf8AM884xxmpiJeJ2jygnovXqyhTm004uzWqa3XoznPI6xw+PL1wIQbdlqcNw7tdXuozjCpfS7tTfq5LS3qj0CjOMaTqvNFZb+LwtrnkUrScf1rK5L8sVhI4bTKvxHELDxzOScndeHlbf8rnH42hOpmrSfPSPRdPU6GniqSeeUVObUW1KKlBN6pWenh0Rg4niqk76K2rvZbeR5uqbTsvTFYrGQ5CbFBXHWleT9SVLROT2Sv/ACNK2lHH/Z4eCMXN/fl93plXU0a4rOLb0nd3ea+/uKk6zer5mMsQNpT4jGeklkfxj/IrYzR6MpNE4jBnWKeRwlqlrG/3Xzt5M2fZvj7oNU5tuk3/AAN815dUaZ+hBI1E4zasTGS9bi77a328zHh8TCom4SzJScW1e11o7N7+qOG4bx6uqawtJRbk8lOcr5oJ8lbTQ7TheAVClGjF3UVa/V7t/E7Vtry2p0rSGJErG2CAdhWAEMRKICESkKwUpIBSAkiIAwuAwSFcnChOWyEzhiJCc7FuMacfDPxS55ZWa+Tv8COIpYV+1GTstb1NPekjjbnrDrXhtKpQm6k+6ppyna7Wyins5yekVo997aEq3Y/Dzl3mOrznLZU6LVOnH9VSknKb87R9DS8Q42qV6OEj3VJPNK126k2rXlJ6tcjPwKauq9ZupUfsRfsxtzt7zlfktZ2pxxVs6nYLh9X/AA6eJpq3tuusvwnBtlLGdgMDD/msT5pKk7+Sbireupdx/Gsu8vEc7juOSlsc46vrpjZ/8Ng43w1GMZLarP8AvKt+ueXs/upGhxfFp1ZOU5N33vzS5FKvWlLdmGS0NxAt0ca73ZchxaycXrTfLo+duhpKQmXIQbyduo8a7U7dZK/ok3+QUVZ3DF6w/eT/AAA1zQmTZE0IEwyjsB0PAuyzrRVSpUyQl7KilKTW13dpRXxOfxFO0pK90pNX22bW3uPTuDRUaFJLlTh/tR53xjCunXqQa+/JrzUndNfE1MZDlS2zMKcG0007STun0a2PT+E4xVqUKiXtR1XRrSS+J5lTpOUoxW8mkve7Hq9GjGEVCKtGKyxXktEap7Z5vR2HYlYVjq86PvFqTsFgIakojBBTAQrgOwwuAGLKyUabbta/lubTDQT0s/W0mvkmLiDlC8abadldrSWv3Ytq8fU8c/ys9Q9Ff48z+sMaEKX+K0n+jmV/fFar32KeM49hoxcYwqZv1ZW+ZQr8NlunHM37Orsurk92ZsJw+NPVaz/S6fsrkc4m3JPmXSYrxw0teU5XUabpxe+7m+ilL8EkLEV+7ioqzyatO+re1/yOijR5vZXd/q2cbxbGd7Pwq0U9PPzfmb6cWttU61RybcndvdljDYpxWm+y8inNGTDVLlaTqScndu5FxMs4kchNGKZhlLWxZlAwVY9CwMahzCTuZ8mnr9TFGFmVEFuGKfg9WrfUyW+89kV4XrVIU46Zmoxv582FVGhHWf2Gq/61L4T/ACNHxzhE8NPJOzurxktn+RdhFFFvhvD5V6ipx5+0/wBGH3pP3fMpRO87B4e9CctLyq7+UYrS/S9x4/UtM54b2EUkkttl6LRGk7WcKdampwX95TTdv0obuPqt17zo+4fVDVDzNzyUz289aXidx4/Sq5ZQmvuyjL4NM9ZhNPWLunqn1T1R51iOzmK7yUFQn7TSlbwWbdpZ9rW1PR8LgVThCmn7MVH4KxmvJWPcunJSbeoIDL3XmHdLr8jffp9cezf4xBYy915h3XmO/T6dq/xiEZXR8w7rzRe9T6dq/wAYxGTufT5h3Xn9S92n+UHbv8Y7AT7tgXuU+wnRb5LLmZLvXa1/kvqYZyYlVPlPopWCyFGRK41cartJWcaDSbWaUY+7Vv6HISOg7V4rWFL9HxS9XpFfDX3mjw2FnWnkpxu/kl1k+SPRTxVzlUlTnNxhBXnOSjFdW/w8yhxPC1KFadKT1g7Xi3Zpq6lHysz0bg/Bo4fxN5qrVnPlFPeNNPZPm92UO2PB1Wh30V46cfFZLxUlq7+cdX6XLHLG4TXw43DcSktJLMuu0v5myoYynLaVn0ldfyNOqBcweHcpKEVeUnZLq/61NzEJDaSh6GKVA6/hXCIUqahKMZyes20n4ukb8kWHw2j/AKUPh+Bw7mN9LjIYKThKUYtqKu30/roa6cz0yMEllSSjtlSsrdLHn3HsD3NWUPuvxRfWLN8d+pLRjXV53jL3fUvdi8E6mJjO3hhq/XkarEPw+87jsNRSw+ZfebubvOVSPMulKPGuFxxNJwlv92XNMuApHkicdMeRcQwsqM5U57xfx6NeR6V2ToZMLTXVZn79Tju3U4yxHhd2o2lbqdzwT/ApfsL6I9HJO0hivtfuFxXA8zSSEJzS3YnWj1CnYLGOWJiuZieOiUWUgZV+3eRCWNfJIYLgFF4mXX5CWIl1GC+Fih38uod/LqXBsEI1/fy6gMFuRjkgchZiCcAr11BOT5cuvREVMqY1X8ywjnPss69V/pS1k3tFdfRHVYDBwowyQ/ek95Pq/wAiGEoKnHTd6t+ZmdQ1NtTGXOjDjcSqdKc29oS+LVkviQnI5TtBxDvH3aleEXdtPRy5ethWuyTLRQWiR2XZHh+WPfyXikmoabR5y9Xt6Gr4VwVO1Ssnk3Ub2cujfSJucVxtw0hFWVkvRcjred8QkQ3iGaPA8WqVXayt5XN2nojhMY3EmaPtfge8o517VN39YvRr6M3lzm+1PEczWGp+KTazW+UdOfUtN1LOYwPDHXcoR9pRcork7bp9DZ9lOIvDy7mp7LdvOLv9B4CnLCYyEajVpxSb6Kat8mWO0fAJPNVg7vd02tX1af4HotMT4n9YdhJms49xRYek52bltFcr9Wch/afERpxp5knHTO0nNx5RbfTruUcVxHEYlqEqkpJuyjol62SVznHF58r1MeBwVTF1bLVt3nLkk/62PUMLRUIRitkkilwTh0MPSUIbvWcnvKXVmxRnkvvhawlYEiIHJpJxI2Q7iuBCWGi+RjlgomdMdy6Kf2PoxfZpFxgxo10qMujIM2YMujWxGXnTXQhLDp9RopSkBYeD8wLoSmEjDG/MVSbMiE62pkoTKjhrdtDlUtsaGwcivOdio8VYarp8xiDF1lKE4Xabi0muvI4+hFSms/sp3a6pfd+iO1nQTVzmMbgfHLL1OtJZlnxHFXOV72XJLYo1sVd7mCvRcdys5HSIhnXadmFalKb5vT3Ftdo8PnyOTT21i7J9L8jF2cTWDS1Tedp+rdmc9huzmJnOWdKCcm3OTUr6vVRi7v32OWRMzrXn8bjjvaXLenh2m2rOouXlBc35mXs3wpUl3tTWpLXXVpP15lnB8Bw8MryZpLXNJt3fXLeyNnOmmZm0RGQuT+uS7ZvNOFt4x197ujZYLjiqUouWtS2VrrJaX961LHE+HwVKpONFTqKOl80pN3S0u9bbnG4FqFWMK9OSg3aSlGcHrs09Hubrlq/8SfEtpLA1o1syoqqrq+WKqxt1cVex0tLg1FVO+UWpNei/hsisuzlBNuDqw6ZKj29Xd2M8OEzj7GKxCXRuE/8AfFmZtE/qxDaJDsa77LiFtir/ALdCD+ORxJ0vtK9qWHn+7Vpv5OSOef7VdCxWhUq38VOn+7Ub+sEWCKTYXY2K/kAXDMJvyEn5EErhcLBlKHcLisAU2FhJgEAwAK1leXQ19eo1uzZ/Y292NcNjzLEwjn3VfK7JZp22Z0C4fBbIn9jXkXqgxzKxD5mSjLodEsHDojIsPDlFfAvUY52dea0sV8Ts3zOq7iIOjHp8hF0x51iG3uY6E4R0nRVTW988o6dNNLHoEuGUXvSpv91fkQlwTDP/ACKfwa+jOkcsM9LSU+2CWjw9ktlCadl6NItQ7X0OdOsvdTfzzF59ncK/8lL0lNfSRil2Wwv6E16VJ/i2Z2k/i5Zjp9rMM91Vj6wi/wDbJlulx3DSV++jHykpRfwaKj7J4f8A6n8f8jF/ZGj/AKlVfwP/ANSf2z+puqXEKMtqtJ+k4fmZ4yT2aa8mmvkaKl2Twy9rvJvq5KPyiiS7L4dez3sfONRp/JEyv1fLd6DTNbS4W4q0cTiUvN05/wDkgyzDDSSt39R+bhQ/+ZnI+qtJ+Y7vqamrwus5LLjayjzTUL+7Kor5FmngZpa4nES9ZQX0gMj6Ltw9xgjhlzqVn/3JL6WJwpJc5P8AanKX1Iqdl0GAECuJpDs+iGAkl/TCwrDSAB3E4goroAnBdPqOMUh2QJIBSpRfIB5XyYFEGBFVESuQACzIYBYQwALAojTABAMAECAaYAIYAKwxMYDVhMAALBYLjALBYbEAJA0CYwENBYAE7gSFYBJDsFgAWRdB2C4rgMBWACpfr8CNr+g0gciom2kQdZvYhuPL5gSVV7LV/JE1OXVfAilYTl0Ayqr1JKoYE+g8wFjOgzFZjTQFoLFVMmpMDOFjDnY+9IrKMxqoPOBMTQJjsAhjygAAAWABiABiGACABgIGwCwAKxITYCYAAFFDJITiVDsLMIFqA2JgyLAaHcggKJXBISJMgAENIBkokUSYVJyQ0yCiTRBPOPOQC4E3UBTMaGBkzkoyMRKIGQLkMwnK4DlMXe+oKkSyrqBHvfUaqeRLKiSQAoseVhd9foJgPKxNCcmK7AMyAjlACkNABpAxrYAAERkMApIJAAQ4gwAgY0ABSiZIgARIixgFNAAEAAABKJOIAAuZJbDACrV5hh9/eAAW0AwAGRYwATBjAAQAAH//2Q==");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)



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

uploaded_file = st.file_uploader("Upload a file", type=["csv","npy"])
if uploaded_file is not None:
    # scaled_X, scaled_y = filter_new_data(uploaded_file)
    X = np.load(uploaded_file)
    class_model = get_classification()
    linear_model = get_linear()
    class_prediction = class_model.predict(X[0:3])
    a = pd.DataFrame(class_prediction, columns=['down','same','up'])
    a=a.idxmax(axis=1, skipna=True)
    b = pd.DataFrame()
    b['direction'] = a
    lin_prediction = linear_model.predict(X[0:3])
    b['pred_prob'] = lin_prediction
    st.write(b)



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