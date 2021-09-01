import os
import shutil
import numpy as np

try:
    shutil.rmtree('Data')
    shutil.rmtree('Results')
    shutil.rmtree('Models')
    shutil.rmtree('Plots_Prior_Sentiment')
except:
    pass

os.mkdir('Data')
os.mkdir('Results')
os.mkdir('Models')
os.mkdir('Plots_Prior_Sentiment')

os.mkdir('Data/DataPrior')
os.mkdir('Data/DataTest')
os.mkdir('Data/Cleaned')

for dir in ['Data/DataTest']:
    #'Data/DataPrior'
    for i in ['All', 'Present', 'Future', 'Raw', 'Processed', 'Combined', 'FollowerGraphsProcessed']:
        os.mkdir(dir + '/' + i)