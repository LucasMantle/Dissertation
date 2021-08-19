import pandas as pd
import numpy as np

# This file iterated through collected data to ensure the users have tweeted a sufficient amount. Otherwise they are
# not used.



users = []
with open('Users&Keywords/users_files_checked.txt', 'r') as x:
    Lines = x.readlines()
    for line in Lines:
        if line.strip().lower() not in users:
            users.append(line.strip().lower())

new_users = []
for user in users:
    try:
        file = pd.read_csv('Data/DataPrior/Present/' + user + '.csv')
        file1 = pd.read_csv('Data/DataTest/Present/' + user + '.csv')
    except:
        continue

    if len(file.index) >= 100:
        new_users.append(user)

np_users = np.array(new_users)

with open('Users&Keywords/checked_users.txt', "w") as txt_file:
    for i, line in enumerate(np_users):
        if i == len(np_users):
            txt_file.write(line)
        else:
            txt_file.write(line + '\n')
