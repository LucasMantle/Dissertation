import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import datetime

import random
from collections import deque
from sklearn import preprocessing


def date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d')


def train_test_split(df, train_split=0.8):
    # This splits the data into train and test splits
    obs = df.shape[0]
    train_split_point = int(train_split * obs)
    # Sort date columns to ensure its in order n then you can split
    df['prediction_day'] = df['prediction_day'].apply(date)
    df.sort_values(by='prediction_day', ascending=True)

    df['time_int'] = df['prediction_day'].apply(lambda x: x.value)

    # Split the data first and then do the rest
    train = df.iloc[:train_split_point]
    test = df.iloc[train_split_point:]

    return train.values, test.values


#  Change this for RNN
def train_validation_split(df, val_split=0.8):
    import random
    obs = df.shape[0]
    train_split_point = int(val_split * obs)

    # Sort data
    df = df[np.argsort(df[:, -1])]

    # Split the data first and then do the rest
    train = df[:train_split_point, :]
    val = df[train_split_point:, :]

    np.random.shuffle(train)
    np.random.shuffle(val)

    return train, val


# make a function which is given train validation test and then does processing all to do with training data
# regardless of the CV type, it does it correctly

def sequencer(df, seq_len=1):
    # This function is specifically for sequencing the data so it can be used with an RNN
    sequential_data = []
    prev_days = deque(maxlen=seq_len)

    for i in df:  # iterate over the values
        prev_days.append([n for n in i[1:-2]])
        if len(prev_days) == seq_len:
            sequential_data.append([np.array(prev_days), i[-2]])
    X = []
    y = []
    for seq, target in sequential_data:
        X.append(seq)
        y.append(target)
    return np.array(X), np.array(y)


def processing_cv(train, validation, test, seq=True, seq_length=1, fg=(False, 0)):
    # This function uses the data from train, val test split and processes data in the correct manner so there is no
    # data leakage. All scaling and sequencing is done so there is no data leakage to ensure the robustness of the
    # model . Must sort again just in case
    train_s = train[np.argsort(train[:, -1])]
    validation_s = validation[np.argsort(validation[:, -1])]
    test_s = test[np.argsort(test[:, -1])]

    # Scale
    train_scaled = train_s.copy()
    validation_scaled = validation_s.copy()
    test_scaled = test_s.copy()

    if not fg[0]:

        features_train = train_scaled[:, 1:-2]
        features_validation = validation_scaled[:, 1:-2]
        features_test = test_scaled[:, 1:-2]

        scaler = StandardScaler().fit(features_train)

        features_train1 = scaler.transform(features_train)
        features_validation1 = scaler.transform(features_validation)
        features_test1 = scaler.transform(features_test)

        train_scaled[:, 1:-2] = features_train1
        validation_scaled[:, 1:-2] = features_validation1
        test_scaled[:, 1:-2] = features_test1

    else:
        col_num = fg[1]
        features_train = train_scaled[:, 1:col_num]
        features_validation = validation_scaled[:, 1:col_num]
        features_test = test_scaled[:, 1:col_num]
        scaler = StandardScaler().fit(features_train)
        features_train1 = scaler.transform(features_train)
        features_validation1 = scaler.transform(features_validation)
        features_test1 = scaler.transform(features_test)
        train_scaled[:, 1:col_num] = features_train1
        validation_scaled[:, 1:col_num] = features_validation1
        test_scaled[:, 1:col_num] = features_test1

    if seq:
        # sequence for rnn
        x_train, y_train = sequencer(train_scaled, seq_len=seq_length)
        x_val, y_val = sequencer(validation_scaled, seq_len=seq_length)
        x_test, y_test = sequencer(test_scaled, seq_len=seq_length)


        return x_train.astype(np.float), y_train.astype(np.float) \
            , x_val.astype(np.float), y_val.astype(np.float) \
            , x_test.astype(np.float), y_test.astype(np.float)

    return train_scaled[:, 1:-2].astype(np.float), train_scaled[:, -2].astype(np.float), \
           validation_scaled[:, 1:-2].astype(np.float), validation_scaled[:, -2].astype(np.float), \
           test_scaled[:, 1:-2].astype(np.float), test_scaled[:, -2].astype(np.float)


def processing_test(train, test, seq=False, seq_length=5):
    # This function uses the data from train, val test split and processes data in the correct manner so there is no
    # data leakage. All scaling and sequencing is done so there is no data leakage to ensure the robustness of the
    # model . Must sort again just in case
    train_s = train[np.argsort(train[:, -1])]
    test_s = test[np.argsort(test[:, -1])]

    # Scale
    train_scaled = train_s.copy()
    test_scaled = test_s.copy()

    features_train = train_scaled[:, 1:-2]
    features_test = test_scaled[:, 1:-2]

    scaler = StandardScaler().fit(features_train)

    features_train1 = scaler.transform(features_train)
    features_test1 = scaler.transform(features_test)

    train_scaled[:, 1:-2] = features_train1
    test_scaled[:, 1:-2] = features_test1

    if seq:
        # sequence for rnn
        x_train, y_train = sequencer(train_scaled, seq_len=seq_length)
        x_test, y_test = sequencer(test_scaled, seq_len=seq_length)

        return x_train, y_train, x_test, y_test

    return train_scaled[:, 1:-2].astype(np.float), train_scaled[:, -2].astype(np.float) \
        , test_scaled[:, 1:-2].astype(np.float), test_scaled[:, -2].astype(np.float)
