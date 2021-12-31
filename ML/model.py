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
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #
    def __init__(self):
        """
        Constructor of ModelSeq class

        :return: Itself (implicitly as constructor)
        :rtype: ModelSeq

        """
        #inheritance of the class Sequential from keras
        super(ModelSeq, self).__init__()
        #add the first input layer with 4 inputs and the first hidden layer with
        #64 neurons and a relu activation function
        self.add(Dense(units = 64, kernel_initializer = 'uniform', activation = 'relu', input_dim = 4))
        #add the second hidden layer with 64 neurons and a relu activation function
        self.add(Dense(units = 64, kernel_initializer = 'uniform', activation = 'relu'))
        #add the output layer with 4 outputs and a linear activation function
        self.add(Dense(units = 4, kernel_initializer = 'uniform', activation = 'linear'))
        #add the Adam optimizer with a learning rate of 0.1 and fix the loss as mean squarred error
        self.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=0.1), loss = 'mean_squared_error', metrics = [tf.keras.metrics.MeanSquaredError()])

    def info(self):
        """
        info()

        Method to print informations about the neural network model

        """
        print(self.summary())


    def calcul_score(self):
        """
        calcul_score()

        Method to compute the score of the model : squarred error and mean squarred error

        """
        som = 0
        for i in range(np.shape(self.__Y_test)[0]):
            #calculation of the squarred error
            som += sum((self.__Y_test[i] - self.__Y_pred[i])**2)

        self.__squared_error=som
        #calculate the mean squarred error with the funtion from sklearn
        self.__mean_squared_error = mean_squared_error(self.__Y_test,self.__Y_pred)

    def learn(self,data,score = "./ML/score.csv", weights = "./ML/model_weights.h5"):
        """
        learn()

        Method to train the model with the dataset

        :param data : path and name of the dataset
        :type data : string
        :param score : path of the .csv for the score
        :type score : string
        :param weights : path and name of the file for saving the weights
        :type weights : string

        """
        #load the dataset with pandas
        dataset = pd.read_csv(data)
        #affectation of the inputs data and the target
        self.__X = dataset.iloc[:,4:8].values
        self.__Y = dataset.iloc[:,0:4].values

        #we assign 1 to true and 0 to false
        for i in range(np.shape(self.__Y)[0]):
            if self.__Y[i,1] == True:
                self.__Y[i,1] = 1.0
            else:
                self.__Y[i,1] = 0.0

        self.__Y.astype(np.float32)

        #split the data between test dataset and train dataset thanks to the
        #split function from sklearn
        self.__X_train, self.__X_test, self.__Y_train, self.__Y_test = train_test_split(self.__X, self.__Y.astype(float), test_size = 0.20, random_state = 0)
        self.__X_train = normalize(self.__X_train)
        self.__X_test = normalize(self.__X_test)

        #training the model with a batch size equal to 10 and 10 000 epochs
        self.fit(self.__X_train, self.__Y_train, batch_size = 10, epochs = 10000)
        #prediction of the model with the test dataset after the training
        #this prediction is used for the calculation of the score
        self.__Y_pred = self.predict(self.__X_test)

        #computation of the score : squarred error and mean squarred error
        self.calcul_score()
        #saving the score
        data_score  = pd.DataFrame(np.array([[self.__squared_error,self.__mean_squared_error]]),columns = ["squared_error","mean_squared_error"])
        data_score.to_csv(score, index=False)
        #print(self.__squared_error)
        #print(self.__mean_squared_error)

        #save model_weights
        self.save_weights(weights)

    def pred(self, nb_customers, nb_vehicles, capacity, DB, weights = "./ML/model_weights.h5"):
        """
        pred()

        Method to predict the parameters to use for the setting of the tabu
        search algorithm

        :param nb_customers : number of customers in the CVRP problem
        :type nb_customers : int
        :param nb_vehicles : number of vehicles used in the CVRP problem
        :type nb_vehicles : int
        :param capacity : capacity of each vehicle in the CVRP problem
        :type capacity : int
        :param DB : Davies-Bouldin index
        :type DB : float
        :param weights : path and name of the file for saving the weights
        :type weights : string
        :return: the best parameters for the setting of the tabu search algorithm
        :rtype: list of integers
        """
        X = np.array([[nb_customers, nb_vehicles, capacity, DB]])
        X = normalize(X)
        self.load_weights(weights)
        y_pred = self.predict(X)
        for i in range(len(y_pred[0])):
            y_pred[0][i] = int(round(y_pred[0][i]))

        y_pred = y_pred[0].astype(int)

        return y_pred
