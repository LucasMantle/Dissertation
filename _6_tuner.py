from _6_tuner_functions import *
import time
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def tune(df, model_name, **params):
    train, test = train_test_split(df)

    tuner = CVTuner(
        hypermodel=build_model,
        oracle=kerastuner.oracles.BayesianOptimization(
            objective=kerastuner.Objective("val_accuracy", direction="max"),
            max_trials=params['max_trials']),
        directory='Tuning/' + model_name,
        project_name=str(time.time()))

    tuner.search(train, test, epochs=params['epochs'], executions=params['executions'], f_graph=params['f_graph'])

    train, val = train_validation_split(train)

    x_train, y_train, x_val, y_val, x_test, y_test = processing_cv(train, val, test, seq=True, fg=params['f_graph'])

    # Get the optimal hyperparameters
    best_hps = tuner.get_best_hyperparameters(num_trials=10)[0]

    # Build the model with the optimal hyperparameters
    model = tuner.hypermodel.build(best_hps)

    history = model.fit(x_train, y_train, epochs=250, validation_data=(x_val, y_val))

    val_acc_per_epoch = history.history['val_accuracy']
    best_epoch = val_acc_per_epoch.index(max(val_acc_per_epoch)) + 1

    hypermodel = tuner.hypermodel.build(best_hps)
    # Retrain the model
    hypermodel.fit(x_train, y_train, epochs=best_epoch, validation_data=(x_val, y_val))

    hypermodel.save('Models/' + model_name + '.h5')

    print('RNN --------')
    print(model_name + ' done')
    print('--------')

    cm = confusion_matrix(y_test, hypermodel.predict(x_test) > 0.5, normalize='true')
    print(cm)

    cm = np.round(cm, decimals=2)

    plt.figure(figsize=(10, 7))
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, fmt='g', ax=ax)  # annot=True to annotate cells, ftm='g' to disable scientific notation

    # labels, title and ticks
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion matrix: ' + model_name)
    ax.xaxis.set_ticklabels(['Increase', 'Decrease'])
    ax.yaxis.set_ticklabels(['Increase', 'Decrease'])

    plt.savefig('Results/CM_LSTM' + model_name + '.png')

    eval_result = hypermodel.evaluate(x_test, y_test)
    # Save the train, val, test sets
    # np.savetxt("Data/Train_Val_Test_Sets/_6_train_" + model_name + '.csv', train, delimiter=",")
    # np.savetxt("Data/Train_Val_Test_Sets/_6_train_" + model_name + '.csv', test, delimiter=",")

    return eval_result[1]
