import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class BillyRocket:

    # Static
    nInput = 12
    nHidden1 = 10
    nHidden2 = 6
    nOutput = 3

    validationReserve = 10
    batchSize = 5
    epochs = 2

    @staticmethod
    def initNetwork() -> None:
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
    def train() -> None:
        model = keras.models.load_model("state") # Get compiled(!!!) model

        # REMOVE: Replace with actual data and load them from a dataset folder
        # TODO: change to xTest = JsonConvert.thisandthat(y'know?)
        trainingExamples = []
        trainingExamplesLabels = []
        
        with open("./training-data.json") as f:
            trainingJson = json.load(f)
            for ex in trainingJson["TrainingExamples"]:
                trainingExamples.append(
                    ex["LineLengths"] +
                    ex["GameState"]
                )
                trainingExamplesLabels.append(
                    ex["KeyboardInput"]
                )

        xTrain = np.array(trainingExamples) # Training Data
        yTrain = np.array(trainingExamplesLabels) # Training Data Label
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

    # Non-static
    def __init__(self, model) -> None:
        self.model = model
    
    def runNetwork(self, inputs) -> tf.Tensor:
        return self.model(inputs, training=False)