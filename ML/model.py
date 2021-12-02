import keras
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

class ModelSeq(Sequential):

    def __init__(self):
        super(ModelSeq, self).__init__()
        self.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu', input_dim = 4))
        self.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu', input_dim = 4))
        self.add(Dense(units = 4, kernel_initializer = 'uniform', activation = 'linear'))
        self.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = [tf.keras.metrics.MeanSquaredError()])
