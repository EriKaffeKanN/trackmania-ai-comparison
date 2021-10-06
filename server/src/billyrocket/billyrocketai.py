from tensorflow.python.ops.gen_array_ops import immutable_const


import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

imageData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

nImageInput = 10
nGameDataInput = 2
nHidden1 = 10
nHidden2 = 6
nOutput = 4

validationReserve = 10
batchSize = 5
epochs = 2

inputs = keras.Input(shape=(nImageInput,nGameDataInput), name="gameStates")
x = layers.Dense((nHidden1,), activation=tf.nn.tanh, name="dense1")(inputs)
x = layers.Dense((nHidden2,), activation=tf.nn.tanh, name="dense2")(x)
output = layers.Dense((nOutput,), activation=tf.nn.tanh, name="gameDecisions")(x)

model = keras.Model(inputs=inputs, outputs=output)

# REMOVE: Replace with actual data and load them from a dataset folder
xTrain = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]) # Training Data
yTrain = np.array([0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1]) # Training Data Label
xTest = np.array([]) # Test Data
yTest = np.array([]) # Test Data Labels

# Data formatting
xTrain = xTrain.astype("float32")
yTrain = yTrain.astype("float32")

# Reserving data for validation
xVal = xTrain[-validationReserve:]
yVal = yTrain[-validationReserve:]

xTrain = xTrain[:-validationReserve]
yTrain = yTrain[:-validationReserve]

model.compile(
    optimizer=keras.optimizers.RMSprop,
    loss=keras.losses.MeanSquaredError(), # Loss means cost
    metrics=[keras.metrics.Accuracy()],
)

print("Compiled successfully")
model.fit(
    xTrain,
    yTrain,
    batch_size=batchSize,
    epochs=epochs,
    validation_data=(xVal, yVal) # Validation is performed at the end of each epoch
)