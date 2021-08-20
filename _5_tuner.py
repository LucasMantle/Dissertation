from _5_tuner_functions import *
import time
from sklearn.metrics import confusion_matrix


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

    x_train, y_train, x_val, y_val, x_test, y_test = processing_cv(train, val, test, fg=params['f_graph'])
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

    print('--------')
    print(model_name + ' done')
    print('--------')

    cm = confusion_matrix(y_test, hypermodel.predict(x_test) > 0.5)
    print(cm)

    eval_result = hypermodel.evaluate(x_test, y_test)

    # Save the train, val, test sets
    # np.savetxt("Data/Train_Val_Test_Sets/_5_train" + model_name + '.csv', train, delimiter=",", fmt="%s")
    # np.savetxt("Data/Train_Val_Test_Sets/_5_train" + model_name + '.csv', test, delimiter=",", fmt="%s")

    return eval_result[1]
