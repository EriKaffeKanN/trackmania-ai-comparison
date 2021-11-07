import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class BillyRocket:
    nInput = 13
    nHidden1 = 10
    nHidden2 = 6
    nOutput = 3

    validationReserve = 10
    batchSize = 5
    epochs = 2

    @staticmethod
    def initNetwork():
        inputs = keras.Input(shape=(BillyRocket.nInput,), name="gameStates")
        x = layers.Dense(BillyRocket.nHidden1, activation=tf.nn.tanh, name="dense1")(inputs)
        x = layers.Dense(BillyRocket.nHidden2, activation=tf.nn.tanh, name="dense2")(x)
        output = layers.Dense(BillyRocket.nOutput, activation=tf.nn.tanh, name="gameDecisions")(x)

        model = keras.Model(inputs=inputs, outputs=output)

        model.compile(
            optimizer=keras.optimizers.RMSprop(),
            loss=keras.losses.MeanSquaredError(), # Loss means cost
            metrics=[keras.metrics.Accuracy()], # Useful for analysing performance
        )

        model.save("state")
    
    @staticmethod
    def train():
        model = keras.models.load_model("state") # Get compiled(!!!) model

        # REMOVE: Replace with actual data and load them from a dataset folder
        # TODO: change to xTest = JsonConvert.thisandthat(y'know?)
        xTrain = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]) # Training Data
        yTrain = np.array([0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1]) # Training Data Label
        xTest = np.array([]) # Test Data
        yTest = np.array([]) # Test Data Labels

        # Data formatting
        xTrain = xTrain.astype("float32")
        yTrain = yTrain.astype("float32")

        # Reserving data for validation
        xVal = xTrain[-BillyRocket.validationReserve:]
        yVal = yTrain[-BillyRocket.validationReserve:]

        xTrain = xTrain[:-BillyRocket.validationReserve]
        yTrain = yTrain[:-BillyRocket.validationReserve]


        print("Training")
        model.fit(
            xTrain, # The training data
            yTrain, # The answers to the training data
            batch_size=BillyRocket.batchSize, # Nr of training examples used at a time to calculate the gradient
            epochs=BillyRocket.epochs, # Nr of times each training example is used
            validation_data=(xVal, yVal) # Validation is performed at the end of each epoch
        )
        # The record for the model.fit() call is stored in history.history
    
    def runNetwork():
        model = keras.models.load_model("state")
        # PLACEHOLDER:
        return (1, 0, 0, 0)
    