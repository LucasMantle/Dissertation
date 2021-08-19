import numpy as np
import pandas as pd

import numpy as np
from scipy.stats import norm as distribution_fit
import matplotlib.pyplot as plt

from _2_functions import *

tense_folders = ['Present']
# We only need dist for prior data
type_folders = ['Data/DataPrior']
dist = {}

with open('Users&Keywords/checked_users.txt', 'r') as users:
    Lines = users.readlines()
    for line in Lines:
        # Get user
        user = line.strip()
        dist[user] = {}
        for type_folder in type_folders:
            for tense_folder in tense_folders:
                # Create path to save
                path = type_folder + '/' + tense_folder + '/' + user + '.csv'
                try:
                    data = pd.read_csv(path)
                except:
                    continue

                if data.empty or len(data.index) <= 10:
                    print(user + ' DataFrame is empty!')
                    continue

                dist[user][tense_folder] = {}

                data['new_time_zone'] = data['date'].apply(chigago_time_change)
                data['date_only'] = data['new_time_zone'].apply(date_finder)

                data['time'] = data['new_time_zone'].apply(time)
                data['after_cut_off'] = data['time'].apply(after_cut_off)

                data['sentiment_day'] = data.apply(
                    lambda xy: sentiment_day(date=xy['date_only'], cut_off=xy['after_cut_off']), axis=1)

                daily_sentiment = (data.groupby(['sentiment_day']).mean()['Sentiment_Score'])

                plt.figure(figsize=(12, 7))

                weights_hist = data.groupby(['sentiment_day']).count()['Sentiment_Score']
                plt.hist(daily_sentiment, bins=25, density=True, alpha=0.4, color='gray')

                try:
                    # this fit needs to be weighted
                    loc = distribution_fit.fit(daily_sentiment)
                    # loc = weighted_avg_and_std(daily_sentiment, weights)
                    dist[user][tense_folder] = loc
                except:
                    dist[user][tense_folder]["pos"] = None
                    continue

                # Plot the PDF.
                x = np.linspace(-1, 1, 200)
                p = distribution_fit.pdf(x, *loc)
                plt.plot(x, p, 'k', linewidth=2)

                rounded = tuple([round(x, 4) if isinstance(x, float) else x for x in loc])

                plt.title('User: ' + user + ' - ' + 'Tense: ' + tense_folder + ' - (Mean, Std): ' + str(rounded))
                plt.savefig('Plots_Prior_Sentiment/' + tense_folder + '/' + user + '_' + tense_folder + '.png')
                plt.close('all')

test = pd.DataFrame.from_dict({(i, j): dist[i][j]
                               for i in dist.keys()
                               for j in dist[i].keys()}, orient='index')
test.to_csv('store_dist.csv')
test2 = pd.read_csv('store_dist.csv')
test2.rename(columns={'Unnamed: 0': 'user', 'Unnamed: 1': 'tense'}, inplace=True)
test2.to_csv('Data/DataPrior/Prior_Distributions_daily.csv', index=False)
