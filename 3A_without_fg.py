import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import pandas as pd
import pytz

from _3A_functions import *

folders = ['Present']

with open('Users&Keywords/checked_users.txt', 'r') as users:
    Lines = users.readlines()
    for folder in folders:
        path = 'Data/DataTest/' + folder + '/'
        combined_csv = pd.concat([pd.read_csv(path + line.strip() + '.csv', index_col=0) for line in Lines])

        new_path = 'Data/DataTest/Combined/CombinedData_' + folder + '.csv'
        combined_csv.to_csv(new_path, index=False)

users = []
with open('Users&Keywords/checked_users.txt', 'r') as x:
    Lines = x.readlines()
    for line in Lines:
        users.append(line.strip())

files = ['Present']

for tense in files:
    file = 'Data/DataTest/Combined/' \
           'CombinedData_' + tense + '.csv'
    data = pd.read_csv(file)
    data['new_time_zone'] = data['date'].apply(chigago_time_change)
    data['dow'] = data['new_time_zone'].apply(weekday)
    data['time'] = data['new_time_zone'].apply(time)
    data['after_cut_off'] = data['time'].apply(after_cut_off)

    data['prediction_day'] = data.apply(lambda x: prediction_day(x['new_time_zone'], x['after_cut_off'], x['dow']),
                                        axis=1)

    df = data[['date', 'tweet', 'pos_score', 'neg_score', 'neutral_score', 'Sentiment_Score', 'user', 'new_time_zone',
               'prediction_day']]

    means = df.groupby(['prediction_day', 'user']).mean()
    unstacked = means['Sentiment_Score'].unstack('user')
    unstacked.reset_index(level=0, inplace=True)
    unstacked.columns.name = None

    data_fg = unstacked

    msft = yf.Ticker("^GSPC")
    # get stock info
    # get historical market data
    hist = msft.history(start="2015-01-01")
    hist.reset_index(inplace=True)
    hist['Date_open'] = hist['Date'].apply(get_date)
    hist['y'] = hist.apply(lambda x: up_or_down(x['Open'], x['Close']), axis=1)
    new = pd.merge(data_fg, hist[['Date_open', 'y']], left_on='prediction_day', right_on='Date_open', how='left')
    del new['Date_open']

    new.to_csv('Data/DataTest/FollowerGraphsProcessed/V1_NoFG_NoPrior_' + tense + '.csv', index=False)

    distributions = pd.read_csv('Data/DataPrior/Prior_Distributions_daily.csv')
    for user in users:
        mean = float(distributions[distributions['user'] == str((user, tense))]['0'])
        std = float(distributions[distributions['user'] == str((user, tense))]['1'])

        hold = new[user]

        new[user] = (hold - mean)/std

    new.to_csv('Data/DataTest/FollowerGraphsProcessed/V1_NoFG_Prior_' + tense + '.csv', index=False)