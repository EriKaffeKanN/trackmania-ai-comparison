from tensorflow import keras
import numpy as np

validationReserve = 10
batchSize = 5
epochs = 2

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
xVal = xTrain[-validationReserve:]
yVal = yTrain[-validationReserve:]

xTrain = xTrain[:-validationReserve]
yTrain = yTrain[:-validationReserve]


print("Training")
model.fit(
    xTrain, # The training data
    yTrain, # The answers to the training data
    batch_size=batchSize, # Nr of training examples used at a time to calculate the gradient
    epochs=epochs, # Nr of times each training example is used
    validation_data=(xVal, yVal) # Validation is performed at the end of each epoch
)

# The record for the model.fit() call is stored in history.history