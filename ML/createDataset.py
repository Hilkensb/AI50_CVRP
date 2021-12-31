import numpy as np
import csv

import ML.k_means as ml
from solution.constructive.clarkwrightsaving import clarkWrightSaving
from solution.metaheuristic.tabusearch import tabuSearch
import problem.cvrp.instance as cvrp
import time

class Dataset():
    #class used to create the dataset for the training of the neural network
    def __init__(self, filename1, filename2, cvrpbench, paramCVRP_alea):
        #some random parameters to create random cvrp problems
        self.__paramCVRP_alea = paramCVRP_alea
        #.csv files to save the data
        self.__file1 = filename1
        self.__file2 = filename2
        #CVRP problems from the benchmark
        self.__cvrpbench = cvrpbench

        #the set of variations applied to the different parameters of the tabu search algorithm
        #to have different results depending on the parameters used
        self.__nb_iteration = [100,125,150]
        self.__aspiration = [False,True]
        self.__time =[60,75]
        self.__nb_customer=[15,19,178,189,20,39,254,297,44,49,50,54,59,64,69,75,100,120,150,199,31,32,
        33,35,37,79,107,112,134,167,16,18,202,231,247,276,21,22,301,376,403,387,10,88,
        93,127,146,29,171,212]
        self.__tabu_list_lenght = []

    #function to create the dataset for random CVRP problems
    def create(self,d,f):
        #for i in range(len(self.__nb_customer)):
        start_time = time.time()

        #we collect the data of the CVRP problems (number of customer, DB index ans so on)
        #before the computation of the tabu search
        for i in range(d,f):
            for j in range(10):
                nb_c = self.__nb_customer[i]#number of customers
                self.__tabu_list_lenght = [int(nb_c/4),int(nb_c/2),nb_c-1]#possible size of tabu list according the number of customers
                ind_alea = np.random.randint(0,len(self.__paramCVRP_alea))
                c = cvrp.Cvrp()#instanciation of random cvrp problem
                c.randomInstance(nb_c,self.__paramCVRP_alea[ind_alea][0],self.__paramCVRP_alea[ind_alea][1],self.__paramCVRP_alea[ind_alea][2],100)
                KM = ml.K_means(c) #using of the K_means algorithms to calculate the DB index
                KM.run()
                DB = KM.DB #DB index
                num_graph = i + j
                self.test_all_parameters(nb_c,c,c.minVehiculeNumber(),c.vehicule_capacity,DB,num_graph)
        print(time.time() - start_time, " seconds")

    #function to create the dataset for CVRP problems from benchmark
    def create_from_bench(self,d,f):
        start_time = time.time()
        for i in range(d,f):
                c = cvrp.Cvrp(file_path=self.__cvrpbench[i], file_type="web")#instanciation of cvrp problem from benchmark
                nb_c = c.nb_customer #number of customers
                self.__tabu_list_lenght = [int(nb_c/4),int(nb_c/2),nb_c-1] #possible size of tabu list according the number of customers
                KM = ml.K_means(c) #using of the K_means algorithms to calculate the DB index
                KM.run()
                DB = KM.DB #DB index
                num_graph = i
                self.test_all_parameters(nb_c,c,c.minVehiculeNumber(),c.vehicule_capacity,DB,num_graph)
        print(time.time() - start_time, " seconds")

    #this function is used in the creation of the dataset to test different parameters
    #for the tabu search algorithm and save those that provide the best results
    def test_all_parameters(self, nb_cust, cvrp, nb_V,capacity,DB,num_graph):
        L = []
        L_all_res = []
        a = np.random.randint(0,2)
        if a==0:
            a = False
        else:
            a = True
        #test all differents parameters of tabu search
        for n in self.__nb_iteration:
            for l in self.__tabu_list_lenght :
                for t in self.__time :
                    #we use clark and wright algorithm to have a first solution
                    #then tabusearch is used to improve this solution
                    s = clarkWrightSaving(cvrp)
                    tab = tabuSearch(initial_solution=s,number_iteration = n,aspiration = a,tabu_length = l,max_second_run = t)
                    res = tab.best_solution_evaluation_evolution[-1]
                    L.append(res)
                    P = [n,a,l,t,nb_cust,nb_V,capacity,DB,res,num_graph]
                    L_all_res.append(P)
                    #we save all the data tested in a first file
                    with open(self.__file2,'a',newline='', encoding='utf-8') as fichiercsv2:
                        writer=csv.writer(fichiercsv2)
                        writer.writerow(P)

        ind = np.argmin(L)
        #we save the best parameters in a second file which will used for the training of
        #of the neural network model
        with open(self.__file1,'a',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv)
            writer.writerow(L_all_res[ind])
