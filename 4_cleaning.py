import pandas as pd

def weight_ma(x):
    t = [i / 10 for i in range(1, len(x) + 1)]
    t1 = [x / sum(t) for x in t]
    return sum(x * y for x, y in zip(t1, x))


files = ['Present']

users = []
with open('Users&Keywords/checked_users.txt', 'r') as x:
    Lines = x.readlines()
    for line in Lines:
        users.append(line.strip())

for tense in files:
    df = pd.read_csv('Data/DataTest/FollowerGraphsProcessed/V1_NoFG_Prior_' + tense + '.csv')
    threshold = len(df.index) * 0.5
    df.dropna(thresh=threshold, axis=1, inplace=True)
    df.dropna(axis=0, subset=['y'], inplace=True)
    df.ffill(inplace=True)

    df.set_index('prediction_day', inplace=True)
    df.index = pd.to_datetime(df.index)
    moving_avg = df.iloc[:, :-1].rolling('7d', 2).apply(weight_ma, raw = True)
    df.iloc[:, :-1] = moving_avg
    df.reset_index(inplace=True)

    count = 0
    while pd.isna(df).any(axis=1)[count]:
        count += 1

    df = df.iloc[count:, :]

    if df.isna().sum().sum() > 0:
        print('There is an error')

    df.to_csv('Data/Cleaned/NoFG_Prior_' + tense + '.csv', index=False)

    df = pd.read_csv('Data/DataTest/FollowerGraphsProcessed/V1_NoFG_NoPrior_' + tense + '.csv')
    threshold = len(df.index) * 0.5
    df.dropna(thresh=threshold, axis=1, inplace=True)
    df.dropna(axis=0, subset=['y'], inplace=True)
    df.ffill(inplace=True)

    df.set_index('prediction_day', inplace=True)
    df.index = pd.to_datetime(df.index)
    moving_avg = df.iloc[:, :-1].rolling('7d', 2).apply(weight_ma, raw = True)
    df.iloc[:, :-1] = moving_avg
    df.reset_index(inplace=True)

    count = 0
    while pd.isna(df).any(axis=1)[count]:
        count += 1

    df = df.iloc[count:, :]

    if df.isna().sum().sum() > 0:
        print('There is an error')

    df.to_csv('Data/Cleaned/NoFG_NoPrior_' + tense + '.csv', index=False)

    df = pd.read_csv('Data/DataTest/FollowerGraphsProcessed/V1_FG_Prior_' + tense + '.csv')
    threshold = len(df.index) * 0.5
    df.dropna(thresh=threshold, axis=1, inplace=True)
    df.dropna(axis=0, subset=['y'], inplace=True)
    df.ffill(inplace=True)

    x = list(set(users).intersection(set(df.columns)))

    df.set_index('prediction_day', inplace=True)
    df.index = pd.to_datetime(df.index)
    moving_avg = df[x].rolling('7d', 2).apply(weight_ma, raw = True)
    df[x] = moving_avg
    df.reset_index(inplace=True)

    x = list(set(users).intersection(set(df.columns)))
    new_comb = ['prediction_day']
    for user in x:
        new_comb.append(user)
    for x1 in x:
        for x2 in x:
            new_comb.append(x1 + "_" + x2)

    new_comb.append('y')

    df = df[new_comb]

    count = 0
    while pd.isna(df).any(axis=1)[count]:
        count += 1

    df = df.iloc[count:, :]

    if df.isna().sum().sum() > 0:
        print('There is an error')

    df.to_csv('Data/Cleaned/FG_Prior_' + tense + '.csv', index=False)
