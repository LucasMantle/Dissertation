import os
import shutil
import numpy as np

try:
    shutil.rmtree('Data/Test')
except:
    pass

# os.mkdir('Data')

# os.mkdir('Data/DataPrior')
os.mkdir('Data/DataTest')
# os.mkdir('Data/Cleaned')

for dir in ['Data/DataTest']:
    #'Data/DataPrior'
    for i in ['All', 'Present', 'Future', 'Raw', 'Processed', 'Combined', 'FollowerGraphsProcessed']:
        os.mkdir(dir + '/' + i)