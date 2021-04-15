import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import RobustScaler
# import matplotlib.pyplot as plt
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import FunctionTransformer
from pickle import dump
from pickle import load



def mask_first(x):
    result = np.ones_like(x)
    result[0] = 0
    return result


# def get_X_y(df, number_of_sequences, length):
    
#     X = []
#     y_0s = []
#     y_5s = []
#     y_10s = []
#     y_15s = []
#     y_20s = []
#     y_25s = []
#     y_30s = []

#     counter = 1

#     for horse in horse_races:
#         # track progress of the loop by displaying iteration counts by 250s
#         if counter%1000 == 0:
#             print(f"Iteration: {counter}")
#         counter+=1
        
#         # convert all rows of a certain horse/race combo to a unique dataframe
#         sub_df = pd.DataFrame(df_resorted[df_resorted['Horse_Race'] == horse])
        
#         # pull a sequence of rows and columns from that dataframe
#         X_subsample = sub_df[start:start+length-1][['Implied_Prob_s', 
#                                                     'Pressure1_s', 
#                                                     'Pressure2_s', 
#                                                     'Pressure3_s', 
#                                                     'Matched_Percentage_s']]
        
#         y_subsample_0s = sub_df.iloc[start][['Implied_Prob']]
#         y_subsample_5s = sub_df.iloc[start-1][['Implied_Prob']]
#         y_subsample_10s = sub_df.iloc[start-2][['Implied_Prob']]
#         y_subsample_15s = sub_df.iloc[start-3][['Implied_Prob']]
#         y_subsample_20s = sub_df.iloc[start-4][['Implied_Prob']]
#         y_subsample_25s = sub_df.iloc[start-5][['Implied_Prob']]
#         y_subsample_30s = sub_df.iloc[start-6][['Implied_Prob']]
        
        
#         # append that sequence to a list
#         X.append(X_subsample)
#         y_0s.append(y_subsample_0s)
#         y_5s.append(y_subsample_5s)
#         y_10s.append(y_subsample_10s)
#         y_15s.append(y_subsample_15s)
#         y_20s.append(y_subsample_20s)
#         y_25s.append(y_subsample_25s)
#         y_30s.append(y_subsample_30s)
        
#     return np.array(X), np.array(y_0s), np.array(y_5s), np.array(y_10s), np.array(y_15s), np.array(y_20s), np.array(y_25s), np.array(y_30s)


# def get_start_point(df, length, start_points):
#     start = np.random.randint(0, high=df.shape[0] - length)
    
#     if start in start_points:
#         start = get_start_point(df, length, start_points)
        
#     return start




# def filter_data(csv_file):
#     start= 12
#     length = 37
#     df = pd.read_csv(csv_file)
#     df = df[~df['Horse'].str.endswith("(NR)")]
#     df = df.sort_values(["Race", "TimeToOff"], ascending=[True, False])
#     df['SecondsToOff'] = round(df['TimeToOff'] * 24 * 60 * 60)
#     df['TimeDiff'] = - df['SecondsToOff'].diff()
#     df_group = df[df['TimeDiff'] > 0].groupby("Race").agg({'TimeDiff': ['mean', 'min', 'max', 'count'], 'Book': ['min', 'max']})
#     df_races = df_group[(df_group['TimeDiff']['min'] >= 4) & (df_group['TimeDiff']['max'] <= 6) & \
#          (df_group['TimeDiff']['mean'].between(4.98, 5.02)) & (df_group['TimeDiff']['count'] >= 58) & \
#          (df_group['Book']['min'] >= 0.985) & (df_group['Book']['max'] <= 1.015)]
#     df_filtered = df[df['Race'].isin(df_races.index)].sort_values(['Race', 'Horse', 'SecondsToOff'], ascending = [True, True, False])
#     df_filtered['MatchedDiff'] = df_filtered['TotalMatched'].diff()
#     df_filtered['Horse_Race'] = df_filtered['Horse'] + df_filtered['Race']
#     horse_races = df_filtered['Horse_Race'].unique()
#     df_filtered.reset_index(inplace=True, drop=True)
#     mask = df_filtered.groupby(['Horse_Race'])['Horse_Race'].transform(mask_first).astype(bool)
#     df_matched_filtered = df_filtered[mask]
#     df_matched_filtered_grouped = df_matched_filtered.groupby("Horse_Race").agg({"MatchedDiff": ["min"]})
#     df_horses_matched_neg = df_matched_filtered_grouped[df_matched_filtered_grouped['MatchedDiff']['min'] < 0].index
#     df_filtered_preodds = df_matched_filtered[~ df_matched_filtered['Horse_Race'].isin(df_horses_matched_neg)]
#     df_odds_filter = df_filtered_preodds.groupby("Horse_Race").agg({"BackOdds1": ["max", "min"]})
#     df_horses_high_odds = df_odds_filter[(df_odds_filter['BackOdds1']['min'] >= 1.01) & (df_odds_filter['BackOdds1']['max'] < 100)].index
#     df_filtered_final = df_filtered_preodds[df_filtered_preodds['Horse_Race'].isin(df_horses_high_odds)]
#     df = df_filtered_final.copy()
#     df['Implied_Prob'] = 1 / (0.5 * (df['BackOdds1'] + df['LayOdds1']))
#     df['Pressure1'] = df['BackAvail1'] / (df['BackAvail1'] + df['LayAvail1'])
#     df['Pressure2'] = df['BackAvail2'] / (df['BackAvail2'] + df['LayAvail2'])
#     df['Pressure3'] = df['BackAvail3'] / (df['BackAvail3'] + df['LayAvail3'])
#     df['Matched_Percentage'] = df['MatchedDiff'] / df['TotalMatched']


#     r_scaler = RobustScaler() # Instanciate Robust Scaler
#     r_scaler.fit(df[['Implied_Prob', 'Pressure1', 'Pressure2', 'Pressure3', 'Matched_Percentage']])
#     dump(r_scaler, open('robust_scaler.pkl', 'wb') ) # Fit scaler to feature
#     df[['Implied_Prob_s', 'Pressure1_s', 'Pressure2_s', 'Pressure3_s', 'Matched_Percentage_s']] = \
#         r_scaler.transform(df[['Implied_Prob', 'Pressure1', 'Pressure2', 'Pressure3', 'Matched_Percentage']]) #Scale
    

#     df.reset_index(inplace=True, drop=True)
#     df_resorted = df.sort_values(by=['Horse_Race','SecondsToOff'], ascending=[True, True])
#     df_resorted.reset_index(inplace=True, drop=True)


#      y_0s = []
#      y_20s = []
#      X = []

#     counter = 1

#     for horse in horse_races:
#         # track progress of the loop by displaying iteration counts by 250s
#         if counter%1000 == 0:
#             print(f"Iteration: {counter}")
#         counter+=1
        
#         # convert all rows of a certain horse/race combo to a unique dataframe
#         sub_df = pd.DataFrame(df_resorted[df_resorted['Horse_Race'] == horse])
        
#         # pull a sequence of rows and columns from that dataframe
#         X_subsample = sub_df[start:start+length-1][['Implied_Prob_s', 
#                                                     'Pressure1_s', 
#                                                     'Pressure2_s', 
#                                                     'Pressure3_s', 
#                                                     'Matched_Percentage_s']]
        
#         y_subsample_0s = sub_df.iloc[start][['Implied_Prob']]
#         y_subsample_5s = sub_df.iloc[start-1][['Implied_Prob']]
#         y_subsample_10s = sub_df.iloc[start-2][['Implied_Prob']]
#         y_subsample_15s = sub_df.iloc[start-3][['Implied_Prob']]
#         y_subsample_20s = sub_df.iloc[start-4][['Implied_Prob']]
#         y_subsample_25s = sub_df.iloc[start-5][['Implied_Prob']]
#         y_subsample_30s = sub_df.iloc[start-6][['Implied_Prob']]

            # # append that sequence to a list
        # X.append(X_subsample)
        # y_0s.append(y_subsample_0s)
        # y_20s.append(y_subsample_20s)


        # convert lists to numpy arrays

#         y_0s = np.array(y_0s)
#         y_20s = np.array(y_20s)
#         X = np.array(X)


        
# #         # flip axis 1 of the X array
# #         '''because X has been sorted in reverse chronological order, 
# #         its time values must be flipped back before introducing them 
# #         to the model for training'''
# #         X = np.flip(X, axis=1)

#     # convert lists to numpy arrays

#     y_0s = np.array(y_0s)
#     y_20s = np.array(y_20s)
#     X = np.array(X)

        
#     # flip axis 1 of the X array
#     '''because X has been sorted in reverse chronological order, 
#     its time values must be flipped back before introducing them 
#     to the model for training'''
#     X = np.flip(X, axis=1)

#     return X, y_20s, y_0s


def filter_new_data(csv_file):
    start= 12
    length = 37
    df = pd.read_csv(csv_file)
    df = df[~df['Horse'].str.endswith("(NR)")]
    df = df.sort_values(["Race", "TimeToOff"], ascending=[True, False])
    df['SecondsToOff'] = round(df['TimeToOff'] * 24 * 60 * 60)
    df['TimeDiff'] = - df['SecondsToOff'].diff()
    df_group = df[df['TimeDiff'] > 0].groupby("Race").agg({'TimeDiff': ['mean', 'min', 'max', 'count'], 'Book': ['min', 'max']})
    df_races = df_group[(df_group['TimeDiff']['min'] >= 4) & (df_group['TimeDiff']['max'] <= 6) & \
         (df_group['TimeDiff']['mean'].between(4.98, 5.02)) & (df_group['TimeDiff']['count'] >= 58) & \
         (df_group['Book']['min'] >= 0.985) & (df_group['Book']['max'] <= 1.015)]
    df_filtered = df[df['Race'].isin(df_races.index)].sort_values(['Race', 'Horse', 'SecondsToOff'], ascending = [True, True, False])
    df_filtered['MatchedDiff'] = df_filtered['TotalMatched'].diff()
    df_filtered['Horse_Race'] = df_filtered['Horse'] + df_filtered['Race']
    horse_races = df_filtered['Horse_Race'].unique()
    df_filtered.reset_index(inplace=True, drop=True)
    mask = df_filtered.groupby(['Horse_Race'])['Horse_Race'].transform(mask_first).astype(bool)
    df_matched_filtered = df_filtered[mask]
    df_matched_filtered_grouped = df_matched_filtered.groupby("Horse_Race").agg({"MatchedDiff": ["min"]})
    df_horses_matched_neg = df_matched_filtered_grouped[df_matched_filtered_grouped['MatchedDiff']['min'] < 0].index
    df_filtered_preodds = df_matched_filtered[~ df_matched_filtered['Horse_Race'].isin(df_horses_matched_neg)]
    df_odds_filter = df_filtered_preodds.groupby("Horse_Race").agg({"BackOdds1": ["max", "min"]})
    df_horses_high_odds = df_odds_filter[(df_odds_filter['BackOdds1']['min'] >= 1.01) & (df_odds_filter['BackOdds1']['max'] < 100)].index
    df_filtered_final = df_filtered_preodds[df_filtered_preodds['Horse_Race'].isin(df_horses_high_odds)]
    df = df_filtered_final.copy()
    df['Implied_Prob'] = 1 / (0.5 * (df['BackOdds1'] + df['LayOdds1']))
    df['Pressure1'] = df['BackAvail1'] / (df['BackAvail1'] + df['LayAvail1'])
    df['Pressure2'] = df['BackAvail2'] / (df['BackAvail2'] + df['LayAvail2'])
    df['Pressure3'] = df['BackAvail3'] / (df['BackAvail3'] + df['LayAvail3'])
    df['Matched_Percentage'] = df['MatchedDiff'] / df['TotalMatched']


    r_scaler = load(open('data_model/robust_scaler.pkl','rb')) # Fit scaler to feature
    df[['Implied_Prob_s', 'Pressure1_s', 'Pressure2_s', 'Pressure3_s', 'Matched_Percentage_s']] = \
        r_scaler.transform(df[['Implied_Prob', 'Pressure1', 'Pressure2', 'Pressure3', 'Matched_Percentage']]) #Scale
    

    df.reset_index(inplace=True, drop=True)
    df_resorted = df.sort_values(by=['Horse_Race','SecondsToOff'], ascending=[True, True])
    df_resorted.reset_index(inplace=True, drop=True)


    y_0s = []
    y_20s = []
    X = []

    counter = 1

    for horse in horse_races:
        # track progress of the loop by displaying iteration counts by 250s
        if counter%1000 == 0:
            print(f"Iteration: {counter}")
        counter+=1
        
        # convert all rows of a certain horse/race combo to a unique dataframe
        sub_df = pd.DataFrame(df_resorted[df_resorted['Horse_Race'] == horse])
        
        # pull a sequence of rows and columns from that dataframe
        X_subsample = sub_df[start:start+length-1][['Implied_Prob_s', 
                                                    'Pressure1_s', 
                                                    'Pressure2_s', 
                                                    'Pressure3_s', 
                                                    'Matched_Percentage_s']]
        
        y_subsample_0s = sub_df.iloc[start][['Implied_Prob']]
        y_subsample_20s = sub_df.iloc[start-4][['Implied_Prob']]
        
        # append that sequence to a list
        X.append(X_subsample)
        y_0s.append(y_subsample_0s)
        y_20s.append(y_subsample_20s)
    

    # convert lists to numpy arrays
    X = np.array(X)
    y_0s = np.array(y_0s)
    y_20s = np.array(y_20s)
        
    # flip axis 1 of the X array
    '''because X has been sorted in reverse chronological order, its 
    time values must be flipped back to chrono order (counting down 
    to race start)before they can be introduced to the model for training'''
    X = np.flip(X, axis=1)

    return X, y_20s, y_0s


def find_ticks(array, value):
    # 1. convert implied_prob to bet odds by dividing it into 1
    bet_odds = abs(1 / value)
    # 2. find the tick closest to the bet_odds
    array = np.asarray(array)
    idx = (np.abs(array - bet_odds)).argmin()
    # 3. determine the tick below and above the bet_odds
    if  bet_odds >= 1000:
        return 1000, 0
    elif bet_odds <= 1.01:
        return 0, 1.01
    elif array[idx] < bet_odds:
        tick_below = array[idx]
        tick_above = array[idx+1]
    elif array[idx] > bet_odds:
        tick_below = array[idx-1]
        tick_above = array[idx]
    elif array[idx] == bet_odds:
        tick_below = array[idx-1]
        tick_above = array[idx+1]
    return tick_below, tick_above

def distance_between_ticks(array, value_1, value_2):
    
    '''This function takes two values from an array 
    and returns the number of values that exist between the two.'''
    array = array.tolist()
        
    # find tick_1 index in the list of ticks
    index_1 = array.index(value_1)
    
    # find tick_2 index in the list of ticks
    index_2 = array.index(value_2)
    
    # calculate the difference between the two
    distance = index_2 - index_1
    
    # return the difference
    return distance


def final_results(last_odds_test, y_pred, y_test, direction):
    min_change = 4
    stake = 10
    betfair_ticks = pd.read_csv("data_model/BetfairTicks.csv")['Price']
    results = pd.DataFrame()
    results['Last_Prob'] = last_odds_test
    results['Pred_Prob'] = y_pred
    results['True_Prob'] = y_test
    results['Last_Odds'] = 1 / results['Last_Prob']
    results['Last_Back'], results['Last_Lay'] = zip(*results['Last_Prob'].apply(lambda x: find_ticks(betfair_ticks, x)))
    results['Pred_Odds'] = 1 / results['Pred_Prob']
    results['Pred_Back'], results['Pred_Lay'] = zip(*results['Pred_Prob'].apply(lambda x: find_ticks(betfair_ticks, x)))
    results['True_Odds'] = 1 / results['True_Prob']
    results['True_Back'], results['True_Lay'] = zip(*results['True_Prob'].apply(lambda x: find_ticks(betfair_ticks, x)))
    results['Tick_Change'] = results.apply(lambda x: distance_between_ticks(betfair_ticks, x['Last_Back'], x['Pred_Back']), axis=1)
    results['direction'] = direction
    # results['Bet_Type'] = np.where((results['Pred_Lay'] < results['Last_Back']) & (results['direction'] == 'Down','Back', np.where((results['Pred_Back'] > results['Last_Lay']) & (results['direction'] == 'Up','Lay', 'No Bet'))
    # abba = 1
    bets=[]
    for i in results['direction']:
        if i == 'Down':
            bets.append('Back')
        elif i == 'Up':
            bets.append('Lay')
        else:
            bets.append('No Bet')
    results['Bet_Type']= bets

    results['Min_Tick_Change_Predicted'] = np.where(abs(results['Tick_Change']) >= min_change, 1, 0)
    results['PnL_All'] = np.where(results['Bet_Type'] == "Back", stake * (results['Last_Back'] / results['True_Lay'] - 1),\
                                np.where(results['Bet_Type'] == "Lay", (stake * (1 - results['Last_Lay'] / results['True_Back'])), 0))
    results['PnL_Min%'] = results['PnL_All'] * results['Min_Tick_Change_Predicted']
    results['PnL_Midpoint'] = np.where(results['Bet_Type'] == "Back", stake * (results['Last_Odds'] / results['True_Odds'] - 1),\
                                np.where(results['Bet_Type'] == "Lay", (stake * (1 - results['Last_Odds'] / results['True_Odds'])), 0))
    results['PnL_Min%_MM'] = results['PnL_Midpoint'] * results['Min_Tick_Change_Predicted']
    return results
