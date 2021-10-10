import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

nInput = 12
nHidden1 = 10
nHidden2 = 6
nOutput = 4

inputs = keras.Input(shape=(nInput,), name="gameStates")
x = layers.Dense((nHidden1,), activation=tf.nn.tanh, name="dense1")(inputs)
x = layers.Dense((nHidden2,), activation=tf.nn.tanh, name="dense2")(x)
output = layers.Dense((nOutput,), activation=tf.nn.tanh, name="gameDecisions")(x)

model = keras.Model(inputs=inputs, outputs=output)

model.compile(
    optimizer=keras.optimizers.RMSprop,
    loss=keras.losses.MeanSquaredError(), # Loss means cost
    metrics=[keras.metrics.Accuracy()], # Useful for analysing performance
)

model.save("state")