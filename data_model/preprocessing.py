import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import FunctionTransformer
from pickle import dump
from pickle import load


def mask_first(x):
    result = np.ones_like(x)
    result[0] = 0
    return result

def subsample_sequence(df, length, start):
    
    df_sample = df[start: start + length]
    
    return df_sample

    
def split_subsample_sequence(df, length, start):
    
    df_subsample = subsample_sequence(df, length, start)
    
    X_subsample = df_subsample[0:(length - 4)][['Implied_Prob_s', 'Pressure1_s', 'Pressure2_s', 'Pressure3_s', 'Matched_Percentage_s']]
    y_subsample_0s = df_subsample.iloc[length - 5]['Implied_Prob']
    y_subsample_5s = df_subsample.iloc[length - 4]['Implied_Prob']
    y_subsample_10s = df_subsample.iloc[length - 3]['Implied_Prob']
    y_subsample_20s = df_subsample.iloc[length - 1]['Implied_Prob']
    

    return X_subsample, y_subsample_0s, y_subsample_5s, y_subsample_10s, y_subsample_20s


def get_X_y(df, number_of_sequences, length):
    
    X = []
    y_0s = []
    y_5s = []
    y_10s = []
    y_20s = []
    start_points = []
    
    for i in range(number_of_sequences):
        
        start_point = get_start_point(df, length, start_points)
        start_points.append(start_point)
        
        X_subsample, y_subsample_0s, y_subsample_5s, y_subsample_10s, y_subsample_20s = split_subsample_sequence(df, length, start_point)
        X.append(X_subsample)
        y_0s.append(y_subsample_0s)
        y_5s.append(y_subsample_5s)
        y_10s.append(y_subsample_10s)
        y_20s.append(y_subsample_20s)
        
    return np.array(X), np.array(y_0s), np.array(y_5s), np.array(y_10s), np.array(y_20s)


def get_start_point(df, length, start_points):
    start = np.random.randint(0, high=df.shape[0] - length)
    
    if start in start_points:
        start = get_start_point(df, length, start_points)
        
    return start




def filter_data(csv_file):
    length = 24
    df = pd.read_csv(csv_file)
    df = df[~df['Horse'].str.endswith("(NR)")]
    df = df.sort_values(["Race", "TimeToOff"], ascending=[True, False])
    df['SecondsToOff'] = round(df['TimeToOff'] * 24 * 60 * 60)
    df['TimeDiff'] = - df['SecondsToOff'].diff()
    df_group = df[df['TimeDiff'] > 0].groupby("Race").agg({'TimeDiff': ['mean', 'min', 'max', 'count'], 'Book': ['min', 'max']})
    df_races = df_group[(df_group['TimeDiff']['min'] >= 4) & (df_group['TimeDiff']['max'] <= 6) & \
         (df_group['TimeDiff']['mean'].between(4.98, 5.02)) & (df_group['TimeDiff']['count'] >= 30) & \
         (df_group['Book']['min'] >= 0.985) & (df_group['Book']['max'] <= 1.015)]
    df_filtered = df[df['Race'].isin(df_races.index)].sort_values(['Race', 'Horse', 'SecondsToOff'], ascending = [True, True, False])
    df_filtered['MatchedDiff'] = df_filtered['TotalMatched'].diff()
    df_filtered['Horse_Race'] = df_filtered['Horse'] + df_filtered['Race']
    horse_races = df_filtered['Horse_Race'].unique()
    mask = df_filtered.groupby(['Horse_Race'])['Horse_Race'].transform(mask_first).astype(bool)
    df_matched_filtered = df_filtered[mask]
    df_matched_filtered_grouped = df_matched_filtered.groupby("Horse_Race").agg({"MatchedDiff": ["min"]})
    df_horses_matched_neg = df_matched_filtered_grouped[df_matched_filtered_grouped['MatchedDiff']['min'] < 0].index
    df_filtered_preodds = df_matched_filtered[~ df_matched_filtered['Horse_Race'].isin(df_horses_matched_neg)]
    df_odds_filter = df_filtered_preodds.groupby("Horse_Race").agg({"BackOdds1": ["max", "min"]})
    df_horses_high_odds = df_odds_filter[(df_odds_filter['BackOdds1']['min'] >= 10) & (df_odds_filter['BackOdds1']['max'] < 200)].index
    df_filtered_final = df_filtered_preodds[df_filtered_preodds['Horse_Race'].isin(df_horses_high_odds)]
    df = df_filtered_final.copy()
    df['Implied_Prob'] = 1 / (0.5 * (df['BackOdds1'] + df['LayOdds1']))
    df['Pressure1'] = df['BackAvail1'] / (df['BackAvail1'] + df['LayAvail1'])
    df['Pressure2'] = df['BackAvail2'] / (df['BackAvail2'] + df['LayAvail2'])
    df['Pressure3'] = df['BackAvail3'] / (df['BackAvail3'] + df['LayAvail3'])
    df['Matched_Percentage'] = df['MatchedDiff'] / df['TotalMatched']


    r_scaler = RobustScaler() # Instanciate Robust Scaler
    r_scaler.fit(df[['Implied_Prob', 'Pressure1', 'Pressure2', 'Pressure3', 'Matched_Percentage']])
    dump(r_scaler, open('robust_scaler.pkl', 'wb') ) # Fit scaler to feature
    df[['Implied_Prob_s', 'Pressure1_s', 'Pressure2_s', 'Pressure3_s', 'Matched_Percentage_s']] = \
        r_scaler.transform(df[['Implied_Prob', 'Pressure1', 'Pressure2', 'Pressure3', 'Matched_Percentage']]) #Scale
    

    X_nested = []
    y_0s_nested = []
    y_5s_nested = []
    y_10s_nested = []
    y_20s_nested = []
    counter = 1
    horse_races = df['Horse_Race'].unique()
    for horse in horse_races:
        
        if counter%1000 == 0:
            print(f"Iteration: {counter}")
        counter+=1
        
        n_snapshots = df[df['Horse_Race'] == horse].shape[0]
        n_sequences = max(1, int(np.floor((n_snapshots - length) / 10)))
        X_temp, y_0s_temp, y_5s_temp, y_10s_temp, y_20s_temp = get_X_y(df[df['Horse_Race'] == horse], n_sequences, length)
        X_nested.append(X_temp)
        y_0s_nested.append(y_0s_temp)
        y_5s_nested.append(y_5s_temp)
        y_10s_nested.append(y_10s_temp)
        y_20s_nested.append(y_20s_temp)
    X_unnested = [seq for seq_list in X_nested for seq in seq_list]
    y_0s_unnested = [seq for seq_list in y_0s_nested for seq in seq_list]
    y_5s_unnested = [seq for seq_list in y_5s_nested for seq in seq_list]
    y_10s_unnested = [seq for seq_list in y_10s_nested for seq in seq_list]
    y_20s_unnested = [seq for seq_list in y_20s_nested for seq in seq_list]


    X_prelim = np.array(X_unnested)
    y_0s_prelim = np.array(y_0s_unnested)
    y_5s_prelim = np.array(y_5s_unnested)
    y_10s_prelim = np.array(y_10s_unnested)
    y_20s_prelim = np.array(y_20s_unnested)


    rows_to_delete = []
    X = np.delete(X_prelim, rows_to_delete, 0)
    y_0s = np.delete(y_0s_prelim, rows_to_delete, 0)
    y_5s = np.delete(y_5s_prelim, rows_to_delete, 0)
    y_10s = np.delete(y_10s_prelim, rows_to_delete, 0)
    y_20s = np.delete(y_20s_prelim, rows_to_delete, 0)


    return X, y_5s


def filter_new_data(csv_file):
    length = 24
    df = pd.read_csv(csv_file)
    df = df[~df['Horse'].str.endswith("(NR)")]
    df = df.sort_values(["Race", "TimeToOff"], ascending=[True, False])
    df['SecondsToOff'] = round(df['TimeToOff'] * 24 * 60 * 60)
    df['TimeDiff'] = - df['SecondsToOff'].diff()
    df_group = df[df['TimeDiff'] > 0].groupby("Race").agg({'TimeDiff': ['mean', 'min', 'max', 'count'], 'Book': ['min', 'max']})
    df_races = df_group[(df_group['TimeDiff']['min'] >= 4) & (df_group['TimeDiff']['max'] <= 6) & \
         (df_group['TimeDiff']['mean'].between(4.98, 5.02)) & (df_group['TimeDiff']['count'] >= 30) & \
         (df_group['Book']['min'] >= 0.985) & (df_group['Book']['max'] <= 1.015)]
    df_filtered = df[df['Race'].isin(df_races.index)].sort_values(['Race', 'Horse', 'SecondsToOff'], ascending = [True, True, False])
    df_filtered['MatchedDiff'] = df_filtered['TotalMatched'].diff()
    df_filtered['Horse_Race'] = df_filtered['Horse'] + df_filtered['Race']
    horse_races = df_filtered['Horse_Race'].unique()
    mask = df_filtered.groupby(['Horse_Race'])['Horse_Race'].transform(mask_first).astype(bool)
    df_matched_filtered = df_filtered[mask]
    df_matched_filtered_grouped = df_matched_filtered.groupby("Horse_Race").agg({"MatchedDiff": ["min"]})
    df_horses_matched_neg = df_matched_filtered_grouped[df_matched_filtered_grouped['MatchedDiff']['min'] < 0].index
    df_filtered_preodds = df_matched_filtered[~ df_matched_filtered['Horse_Race'].isin(df_horses_matched_neg)]
    df_odds_filter = df_filtered_preodds.groupby("Horse_Race").agg({"BackOdds1": ["max", "min"]})
    df_horses_high_odds = df_odds_filter[(df_odds_filter['BackOdds1']['min'] >= 10) & (df_odds_filter['BackOdds1']['max'] < 200)].index
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
    

    X_nested = []
    y_0s_nested = []
    y_5s_nested = []
    y_10s_nested = []
    y_20s_nested = []
    counter = 1
    horse_races = df['Horse_Race'].unique()
    for horse in horse_races:
        
        if counter%1000 == 0:
            print(f"Iteration: {counter}")
        counter+=1
        
        n_snapshots = df[df['Horse_Race'] == horse].shape[0]
        n_sequences = max(1, int(np.floor((n_snapshots - length) / 10)))
        X_temp, y_0s_temp, y_5s_temp, y_10s_temp, y_20s_temp = get_X_y(df[df['Horse_Race'] == horse], n_sequences, length)
        X_nested.append(X_temp)
        y_0s_nested.append(y_0s_temp)
        y_5s_nested.append(y_5s_temp)
        y_10s_nested.append(y_10s_temp)
        y_20s_nested.append(y_20s_temp)
    X_unnested = [seq for seq_list in X_nested for seq in seq_list]
    y_0s_unnested = [seq for seq_list in y_0s_nested for seq in seq_list]
    y_5s_unnested = [seq for seq_list in y_5s_nested for seq in seq_list]
    y_10s_unnested = [seq for seq_list in y_10s_nested for seq in seq_list]
    y_20s_unnested = [seq for seq_list in y_20s_nested for seq in seq_list]


    X_prelim = np.array(X_unnested)
    y_0s_prelim = np.array(y_0s_unnested)
    y_5s_prelim = np.array(y_5s_unnested)
    y_10s_prelim = np.array(y_10s_unnested)
    y_20s_prelim = np.array(y_20s_unnested)


    rows_to_delete = []
    X = np.delete(X_prelim, rows_to_delete, 0)
    y_0s = np.delete(y_0s_prelim, rows_to_delete, 0)
    y_5s = np.delete(y_5s_prelim, rows_to_delete, 0)
    y_10s = np.delete(y_10s_prelim, rows_to_delete, 0)
    y_20s = np.delete(y_20s_prelim, rows_to_delete, 0)


    return X, y_5s