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

    def __init__(self, cvrp : Cvrp ):
        self.__K = cvrp.minVehiculeNumber()
        self.__cvrp = cvrp
        self.init_parameters()
        self.__Size=len(self.__Inputs)
        self.__C=np.zeros(self.__Size,dtype=int)


    def init_parameters(self):
        cust = self.__cvrp.customers
        Lx = []
        Ly = []
        inputs = []
        centers = []
        for c in cust:
            Lx.append(c.x)
            Ly.append(c.y)
            inputs.append((c.x,c.y))

        self.__minx = min(Lx)
        self.__maxx = max(Lx)
        self.__miny = min(Ly)
        self.__maxy = max(Ly)

        for k in range(self.__K):
            centers.append([np.random.randint(self.__minx,self.__maxx),np.random.randint(self.__miny,self.__maxy)])

        self.__Centers = np.array(centers)
        self.__Inputs = inputs

    def indice_DB(self):
        self.__H = np.zeros(self.__K)
        self.__N = np.zeros(self.__K)
        for i in range(len(self.__C)):
            d = self.dist_eucli(np.array(list(self.__Inputs[i])),np.array(self.__Centers[self.__C[i]-1]))
            self.__H[self.__C[i]-1] +=  d
            self.__N[self.__C[i]-1] +=  1


        for j in range(len(self.__N)):
            if self.__N[j] != 0:
                self.__H[j] = self.__H[j]/self.__N[j]



        DBK = []
        for k in range(self.__K):
            L = []
            if self.__N[k]!=0:
                for u in range(self.__K):
                    if u!=k:
                        S = self.dist_eucli(np.array(self.__Centers[k]),np.array(self.__Centers[u]))
                        L.append((self.__H[k]+self.__H[u])/S)
                if L!=[]:
                    DBK.append(max(L))
                else:
                    DBK.append(0)

        self.__DB = float(sum(DBK)/len(DBK))



    def stop_(self):
        return (self.__oldCenters == self.__Centers).all()


    def show(self):
        fig,ax = plt.subplots()
        plt.title("K_means")
        for c in self.__Centers:
            plt.scatter(c[0],c[1],c='black', s=100)
        col = []
        for k in range(self.__K):
            col.append(np.random.rand(3,))

        for i in range(len(self.__Inputs)):

            plt.scatter(self.__Inputs[i][0],self.__Inputs[i][1],color=col[self.__C[i]-1])
        plt.show()

    def run(self):
        self.assignToCenter()
        self.updateCenters()
        #print(self.__Centers)
        #print(self.__C)
        while self.stop_() == False:
            self.assignToCenter()
            self.updateCenters()
            #print(self.__Centers)
            #print(self.__C)
        self.indice_DB()

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
        self.__oldCenters = copy.deepcopy(self.__Centers)
        for i in range(np.shape(self.__Centers)[0]):
            s = 0
            v = np.zeros((1,2))
            for j in range(len(self.__C)):
                if self.__C[j]==i+1:
                    s = s+1
                    v = v + np.array(list(self.__Inputs[j]))
            if s!=0:
                moy = v * (1/s)
                self.__Centers[i] = moy


    def dist_eucli(self,x,y):
        return np.linalg.norm(x-y)

# ----------------------------- Getter / Setter ----------------------------- #

    @property
    def DB(self) -> float:
        return self.__DB



#test
#data=np.array([(1,10),(1.5,2),(1,6),(2,1.5),(2,10),(3,2.5),(3,6),(4,2)])
#classes=np.array([1,2,1,2,1,2,1,2],dtype=np.int)

#KM = K_means(2,1,1,1,1,data)
#KM.run(2)
