# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 11:44:45 2021

@author: jeome
"""


import numpy as np
import matplotlib.pyplot as plt
from problem.cvrp.instance import Cvrp
#k means ex 2

class K_means():

    def __init__(self, K, minx, maxx, miny, maxy, inputs):
        self.__K = K
        self.__minx = minx
        self.__maxx = maxx
        self.__miny = miny
        self.__maxy = maxy
        self.__Inputs = inputs
        self.__Centers= np.array([[0,8],[0,-4]])       #np.random.randint()
        self.__Size=len(self.__Inputs)
        self.__C=np.zeros(self.__Size,dtype=int)



    def run(self, N):
        for i in range(N):
            self.assignToCenter()
            self.updateCenters()
            print(self.__Centers)
            print(self.__C)

    def assignToCenter(self):
        i = 0
        for p in self.__Inputs:
            L = []
            for c in self.__Centers:

                dist = np.sqrt(sum((np.array(list(p))-np.array(c))**2))
                #print(dist)
                L.append(dist)

            m = np.argmin(L)
            self.__C[i] = m+1
            i=i+1



    def updateCenters(self):
        for i in range(np.shape(self.__Centers)[0]):
            s = 0
            v = np.zeros((1,2))
            for j in range(len(self.__C)):
                if self.__C[j]==i+1:
                    s = s+1
                    v = v + np.array(list(self.__Inputs[j]))
            moy = v * (1/s)
            self.__Centers[i] = moy


    def dist_eucli(self,x,y):
        return np.linalg.norm(x-y)


#test
data=np.array([(1,10),(1.5,2),(1,6),(2,1.5),(2,10),(3,2.5),(3,6),(4,2)])
classes=np.array([1,2,1,2,1,2,1,2],dtype=np.int)

KM = K_means(2,1,1,1,1,data)
KM.run(2)
