import keras
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.metrics import mean_squared_error
import numpy as np

class ModelSeq(Sequential):

    def __init__(self):
        super(ModelSeq, self).__init__()
        self.add(Dense(units = 64, kernel_initializer = 'uniform', activation = 'relu', input_dim = 4))
        self.add(Dense(units = 64, kernel_initializer = 'uniform', activation = 'relu'))
        self.add(Dense(units = 4, kernel_initializer = 'uniform', activation = 'linear'))
        self.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=0.1), loss = 'mean_squared_error', metrics = [tf.keras.metrics.MeanSquaredError()])

    def info(self):
        print(self.summary())


    def calcul_score(self):
        som = 0
        for i in range(np.shape(self.__Y_test)[0]):
            som += sum((self.__Y_test[i] - self.__Y_pred[i])**2)

        self.__squared_error=som
        self.__mean_squared_error = mean_squared_error(self.__Y_test,self.__Y_pred)

    def learn(self,data,score = "./ML/score.csv", weights = "./ML/model_weights.h5"):
        dataset = pd.read_csv(data)
        self.__X = dataset.iloc[:,4:8].values
        self.__Y = dataset.iloc[:,0:4].values

        for i in range(np.shape(self.__Y)[0]):
            if self.__Y[i,1] == True:
                self.__Y[i,1] = 1.0
            else:
                self.__Y[i,1] = 0.0

        self.__Y.astype(np.float32)

        self.__X_train, self.__X_test, self.__Y_train, self.__Y_test = train_test_split(self.__X, self.__Y.astype(float), test_size = 0.20, random_state = 0)
        self.__X_train = normalize(self.__X_train)
        self.__X_test = normalize(self.__X_test)

        #print("X_train : ", self.__X_train)
        #print("X_test : ", self.__X_test)
        #print("Y_train : ", self.__Y_train)
        #print("Y_test : ", self.__Y_test)
        self.fit(self.__X_train, self.__Y_train, batch_size = 10, epochs = 10000)

        self.__Y_pred = self.predict(self.__X_test)

        self.calcul_score()
        data_score  = pd.DataFrame(np.array([[self.__squared_error,self.__mean_squared_error]]),columns = ["squared_error","mean_squared_error"])
        data_score.to_csv(score, index=False)
        print(self.__squared_error)
        print(self.__mean_squared_error)

        #save model_weights
        self.save_weights(weights)

    def pred(self, nb_customers, nb_vehicles, capacity, DB, weights = "./ML/model_weights.h5"):
        X = np.array([[nb_customers, nb_vehicles, capacity, DB]])
        X = normalize(X)
        self.load_weights(weights)
        y_pred = self.predict(X)
        for i in range(len(y_pred[0])):
            y_pred[0][i] = int(round(y_pred[0][i]))

        y_pred = y_pred[0].astype(int)

        return y_pred
