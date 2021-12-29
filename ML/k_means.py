# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 11:44:45 2021

@author: jeome
"""

import copy
import numpy as np
import matplotlib.pyplot as plt
from problem.cvrp.instance import Cvrp
#k means ex 2

class K_means():
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #
    def __init__(self, cvrp : Cvrp ):
        """
        Constructor of K_means class

        :param cvrp: A Cvrp instance
        :type file_path: Cvrp
        :return: Itself (implicitly as constructor)
        :rtype: K_means

        """
        # K clusters for the K vehicles
        self.__K = cvrp.minVehiculeNumber()
        #cvrp problem
        self.__cvrp = cvrp
        #initialization of the parameters
        self.init_parameters()
        #size of the imputs
        self.__Size=len(self.__Inputs)
        #C is the Array which contain the number of the class for each inputs
        self.__C=np.zeros(self.__Size,dtype=int)


    def init_parameters(self):
        """
        init_parameters()

        Method to initialize the parameters used by the k-means algorithm

        """
        #retrieving the list of customers
        cust = self.__cvrp.customers
        Lx = []
        Ly = []
        inputs = []
        centers = []
        #Adding the coordinates of customers in the list Lx, Ly and inputs
        for c in cust:
            Lx.append(c.x)
            Ly.append(c.y)
            inputs.append((c.x,c.y))

        #retrieving the minimum and maximum of the coordinates of customers
        self.__minx = min(Lx)
        self.__maxx = max(Lx)
        self.__miny = min(Ly)
        self.__maxy = max(Ly)

        #creation of the K random coordinates of the centers of clusters
        for k in range(self.__K):
            centers.append([np.random.randint(self.__minx,self.__maxx),np.random.randint(self.__miny,self.__maxy)])

        self.__Centers = np.array(centers)
        self.__Inputs = inputs

    def indice_DB(self):
        """
        indice_DB()

        Method to compute the Davies-Bouldin index

        """
        #initialization of the list H which will contains the Hk (intra-cluster quality) of each K clusters
        self.__H = np.zeros(self.__K)
        #initialization of the list N which will contains the number of customers for each K clusters
        self.__N = np.zeros(self.__K)
        #calculation of intra-cluster quality Hk
        for i in range(len(self.__C)):
            #compute the euclidian distance between the center of the cluster and a customer in the cluster K
            d = self.dist_eucli(np.array(list(self.__Inputs[i])),np.array(self.__Centers[self.__C[i]-1]))
            self.__H[self.__C[i]-1] +=  d
            self.__N[self.__C[i]-1] +=  1

        for j in range(len(self.__N)):
            if self.__N[j] != 0:
                self.__H[j] = self.__H[j]/self.__N[j]


        #computation of the inter-cluster quality and the DBk
        DBK = []
        for k in range(self.__K):
            L = []
            if self.__N[k]!=0:
                for u in range(self.__K):
                    if u!=k:
                        #S is the inter-cluster quality
                        S = self.dist_eucli(np.array(self.__Centers[k]),np.array(self.__Centers[u]))
                        L.append((self.__H[k]+self.__H[u])/S)
                if L!=[]:
                    #retrieving the DBk of the cluster K
                    DBK.append(max(L))
                else:
                    DBK.append(0)
        #calculation of the DB from the DBk
        self.__DB = float(sum(DBK)/len(DBK))



    def stop_(self):
        """
        stop_()

        Method giving the stop condition of the K-means algorithm.
        The algorithm is stopped when the centers of cluster don't change.

        :return: True if the algorithme must be stopped False otherwise.
        :rtype: boolean
        """
        return (self.__oldCenters == self.__Centers).all()


    def show(self):
        """
        show()

        Method to show in a graph the k-means solution.

        :exemple:

        >>> K_means.show()

        """

        fig,ax = plt.subplots()
        plt.title("K_means")
        for c in self.__Centers:
            #the centers are represented by big black points
            plt.scatter(c[0],c[1],c='black', s=100)
        col = []
        for k in range(self.__K):
            col.append(np.random.rand(3,))

        for i in range(len(self.__Inputs)):
            #giving different colors for each clusters. The points of customers
            #in the same cluster have the same color
            plt.scatter(self.__Inputs[i][0],self.__Inputs[i][1],color=col[self.__C[i]-1])
        plt.show()

    def run(self):
        """
        run()

        Method to run the K-means algorithm.

        :exemple:

        >>> K_means.run()

        """
        #first iteration
        self.assignToCenter()
        self.updateCenters()
        #execution of the algorithm while the stop condition is False
        while self.stop_() == False:
            self.assignToCenter()
            self.updateCenters()
        #computation of the DB index
        self.indice_DB()

    def assignToCenter(self):

        """
        assignToCenter()

        Method to assign each input to its center/class.

        """
        i = 0
        for p in self.__Inputs:
            L = []
            for c in self.__Centers:
                #calculation of the euclidian distance between the point of customer
                #and the different centers
                dist = np.sqrt(sum((np.array(list(p))-np.array(c))**2))
                L.append(dist)
            #the center the closest of the customer's point is chosen
            m = np.argmin(L)
            self.__C[i] = m+1 #class affectation
            i=i+1



    def updateCenters(self):
        """
        updateCenters()

        Method to update the positions of the centers of the clusters.
        For ach cluster, the new position of its center is the mean of
        the positions of customers in the cluster.

        """
        #copy the old position of the centers
        self.__oldCenters = copy.deepcopy(self.__Centers)

        #computation of the new positions of the centers
        #For ach cluster, the new position of its center is the mean of
        #the positions of customers in the cluster.
        for i in range(np.shape(self.__Centers)[0]):
            s = 0
            v = np.zeros((1,2))
            for j in range(len(self.__C)):
                if self.__C[j]==i+1:
                    s = s+1
                    v = v + np.array(list(self.__Inputs[j]))
            if s!=0:
                #computation of the mean
                moy = v * (1/s)
                self.__Centers[i] = moy #new position affectation


    def dist_eucli(self,x,y):
        """
        dist_eucli()

        Methode to compute the euclidian distance between two vectors.

        :param x : first vector
        :type x : array of float
        :param y : second vector
        :type y : array of float
        :return: the euclidian distance
        :rtype: float
        """
        return np.linalg.norm(x-y)

# ----------------------------- Getter / Setter ----------------------------- #

    @property
    def DB(self) -> float:
        return self.__DB
