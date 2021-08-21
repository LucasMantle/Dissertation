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

    cms = []
    ev_res = {}

    # Get the optimal hyperparameters
    best_hps_list = tuner.get_best_hyperparameters(num_trials=10)
    for best_hps, count in zip(best_hps_list[:5], range(5)):
        # Build the model with the optimal hyperparameters
        #model = tuner.hypermodel.build(best_hps)
        # history = model.fit(x_train, y_train, epochs=150, validation_data=(x_val, y_val))
        # val_acc_per_epoch = history.history['val_accuracy']
        # best_epoch = val_acc_per_epoch.index(max(val_acc_per_epoch)) + 1
        early_stop = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', min_delta=0, patience=25, verbose=0,
            mode='min', baseline=None, restore_best_weights=True
        )
        hypermodel = tuner.hypermodel.build(best_hps)
        # Retrain the model
        hypermodel.fit(x_train, y_train, epochs=250, validation_data=(x_val, y_val), callbacks = [early_stop])
        hypermodel.save('Models/' + model_name + str(count) + '.h5')

        cm = confusion_matrix(y_test, hypermodel.predict(x_test) > 0.5, normalize='true')
        cm = np.round(cm, decimals=2)

        plt.figure(figsize=(10, 7))
        ax = plt.subplot()
        sns.heatmap(cm, annot=True, fmt='g', ax=ax)

        # labels, title and ticks
        ax.set_xlabel('Predicted labels')
        ax.set_ylabel('True labels')
        ax.set_title('Confusion matrix: ' + model_name)
        ax.xaxis.set_ticklabels(['Decrease', 'Increase'])
        ax.yaxis.set_ticklabels(['Increase', 'Decrease'])
        plt.savefig('Results/CM_LSTM_' + str(count) + model_name + '.png')
        eval_result = hypermodel.evaluate(x_test, y_test)
        ev_res[count] = eval_result[1]

    # Save the train, val, test sets
    # np.savetxt("Data/Train_Val_Test_Sets/_6_train_" + model_name + '.csv', train, delimiter=",")
    # np.savetxt("Data/Train_Val_Test_Sets/_6_train_" + model_name + '.csv', test, delimiter=",")

    return ev_res
