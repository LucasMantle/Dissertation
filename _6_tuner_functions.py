from _6_processing_functions import *
from tensorflow import keras
import keras_tuner as kerastuner
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    BatchNormalization,
    LSTM
)
import numpy as np
from sklearn import model_selection
import tensorflow as tf
from sklearn.model_selection import TimeSeriesSplit, KFold


def build_model(hp):
    METRICS = ['accuracy']

    model = keras.Sequential()

    for i in range(hp.Choice('num_LSTM_layers', [1, 2, 3, 4, 5, 6])):
        model.add(LSTM(units=hp.Choice('LSTM_layer_' + str(i) + '_width', [4, 8, 16, 32, 64, 128, 256]),
                        kernel_initializer=hp.Choice('kernel_' + str(i), ['glorot_uniform', 'glorot_normal']),
                        activation=hp.Choice('activation_' + str(i), ['relu', 'tanh']),
                       return_sequences = True))
        model.add(BatchNormalization())
        model.add(Dropout(rate=hp.Choice('dropout_' + str(i), [0.0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9])))

    model.add(LSTM(units=hp.Choice('LSTM_layer_outside' + '_width', [4, 8, 16, 32, 64, 128, 256]),
                   kernel_initializer=hp.Choice('kernel_lstm_outside', ['glorot_uniform', 'glorot_normal']),
                   activation=hp.Choice('activation_outside', ['relu', 'tanh']),
                   return_sequences=False))
    model.add(BatchNormalization())
    model.add(Dropout(rate=hp.Choice('dropout_outside', [0.0, 0.1, 0.2, 0.3, 0.5, 0.7])))

    for j in range(hp.Choice('num_dense_layers', [0, 1, 2, 3])):
        model.add(Dense(units=hp.Choice('layer_' + str(j) + '_width', [4, 8, 16, 32, 64, 128, 256]),
                        kernel_initializer=hp.Choice('kernel_' + str(j), ['glorot_uniform', 'glorot_normal']),
                        activation=hp.Choice('activation_' + str(j), ['relu', 'tanh']),
                        kernel_regularizer=tf.keras.regularizers.l1(hp.Choice('xlearning_rate' + str(j), [1.0,0.1, 0.01, 0.001]))))
        model.add(BatchNormalization())
        model.add(Dropout(rate=hp.Choice('dropout_' + str(j), [0.0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9])))

    # Add different optimizers
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=keras.optimizers.Adam(hp.Choice('learning_rate', [1.0, 0.1, 0.01, 0.001])),
                  loss='binary_crossentropy',
                  metrics=METRICS)
    return model


class CVTuner(kerastuner.engine.tuner.Tuner):
    def run_trial(self, trial, train, test, executions=3, *args, **kwargs):
        early_stop = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', min_delta=0, patience=25, verbose=0,
            mode='min', baseline=None, restore_best_weights=True
        )

        kwargs['batch_size'] = trial.hyperparameters.Choice('batch_size', [8, 16, 32, 64, 128])
        print(kwargs)
        exec_store = []
        exec_store_loss = []
        for exe in range(executions):

            cv = TimeSeriesSplit(n_splits=4)
            val_acc = []
            val_loss = []
            for train_indices, test_indices in cv.split(train):
                x_train, x_val = train[train_indices], train[test_indices]
                x_train, y_train, x_val, y_val, _1, _2 = processing_cv(x_train, x_val, test, seq=True, fg = kwargs['f_graph'])


                model = self.hypermodel.build(trial.hyperparameters)
                model.fit(x_train, y_train,
                          batch_size=kwargs['batch_size'],
                          epochs=kwargs['epochs'],
                          validation_data=(x_val, y_val),
                          callbacks=[early_stop])

                val_acc.append(model.evaluate(x_val, y_val)[1])
                val_loss.append(model.evaluate(x_val, y_val)[0])
            # Mean or max??
            exec_store.append(np.mean(val_acc))
            exec_store_loss.append(np.mean(val_loss))

        self.oracle.update_trial(trial.trial_id, {'val_accuracy': np.mean(exec_store),
                                                  'val_loss': np.mean(exec_store_loss)})
        self.save_model(trial.trial_id, model)