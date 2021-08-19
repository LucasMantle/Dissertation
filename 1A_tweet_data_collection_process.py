import _1A_twint_function
import _1A_data_processing_functions
import _1A_finbert_mine
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import numpy as np
import os
import pandas as pd

# Do pre-processing to all twitter data
folders = ['Data/DataPrior', 'Data/DataTest']

with open('Users&Keywords/users_files_checked.txt', 'r') as users:
    Lines = users.readlines()
    for folder in folders:
        print(folder)
        for line in Lines:
            print(line)
            # Get users
            user = line.strip().lower()
            user_data = folder + '/Raw/' + user + '.csv'
            # Set up processed data
            user_data_save = folder + '/Processed/' + user + '_processed.csv'
            try:
                os.remove(user_data_save)
            except:
                pass

            try:
                # Get the dataframe from CSV into pandas
                file = pd.read_csv(user_data)
            except:
                # If there was no tweets extracted
                print(user_data, 'is not here')
                continue
            # Apply processing
            df = _1A_data_processing_functions.apply_processing(file)

            df = df[~((df['past_tense'] == 1) & (df['present_tense'] == 0) & (df['future_tense'] == 0))]

            if len(df.index) == 0:
                continue

            # Apply sentiment analysis
            # Pull in model. Doing this now is more efficient.
            model_name = 'ProsusAI/finbert'
            finbert_mod = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
            tokenizer = AutoTokenizer.from_pretrained(model_name)

            # Concat finbert results to dataframe and adjust columns
            df = pd.concat(
                [df, df['tweet'].apply(_1A_finbert_mine.finbert_sentiment, pt_model=finbert_mod, tokenizer=tokenizer)],
                axis=1)
            df.rename(columns={0: 'pos_score', 1: 'neg_score', 2: 'neutral_score', 3: 'sentiment'}, inplace=True)

            # Aggregated sentiment scores which gives us the sentiment score I will be using.
            df['Sentiment_Score'] = df['pos_score'] + df['neg_score'] * -1

            df['user'] = user

            # Save all processed
            df.to_csv(user_data_save)

            # Get present and future tweets
            # If a tweet contains a tense, it will be included in the respective dataframe
            df_present = df[(df['present_tense'] == 1)]
            df_future = df[(df['future_tense'] == 1)]

            # Save all prior + present + future
            df.to_csv(folder + '/All/' + user + '.csv')
            df_present.to_csv(folder + '/Present/' + user + '.csv')
            df_future.to_csv(folder + '/Future/' + user + '.csv')

            print(user_data_save, 'has been processed and saved')
