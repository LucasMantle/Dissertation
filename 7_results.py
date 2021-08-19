import pickle

# read python dict back from the file
result_nn = open('Results/5_Results.pkl', 'rb')
result_rnn = open('Results/6_Results.pkl', 'rb')

result_nn1 = pickle.load(result_nn)
result_rnn1 = pickle.load(result_rnn)

result_nn.close()
result_rnn.close()

print('-----------')
print('RESULTS')
print('NN Results')
print(result_nn1)
print('-----------')
print('RNN Results')
print(result_rnn1)