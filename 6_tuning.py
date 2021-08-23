from _6_tuner import *
import pickle
import os

results = {}
cm = {}

# Read in data for each type of model for NN
data_prior = pd.read_csv('Data/Cleaned/NoFG_Prior_Present.csv')
data_nonprior = pd.read_csv('Data/Cleaned/NoFG_NoPrior_Present.csv')
data_fg_prior = pd.read_csv('Data/Cleaned/FG_Prior_Present.csv')

# need to change the data for the type of model being produced. Each model will have its own data to use

models = ['NoFG_NoPrior_', 'NoFG_Prior_', 'FG_Prior_']
datas = [data_nonprior, data_prior, data_fg_prior]
fgs = [False, False, True]

for model, data, f_graph in zip(models, datas, fgs):
    if f_graph:
        users = []
        with open('Users&Keywords/checked_users.txt', 'r') as x:
            Lines = x.readlines()
            for line in Lines:
                users.append(line.strip())
        x = list(set(users).intersection(set(data.columns)))
        f_graph_col = len(x) + 1
    else:
        f_graph_col = 0

    params = {'epochs': 100,
              'max_trials': 150,
              'executions': 2,
              'f_graph': (f_graph, f_graph_col)}
    results[model] = tune(data, model, **params)

    try:
        os.remove("Results/6_Results_" + model + ".pkl")
    except:
        pass
    # Save results
    file = open("Results/6_Results_" + model + ".pkl", "wb")
    pickle.dump(results, file)
    file.close()


print(results)

try:
    os.remove("Results/6_Results.pkl")
except:
    pass
# Save results
file = open("Results/6_Results.pkl", "wb")
pickle.dump(results, file)
file.close()