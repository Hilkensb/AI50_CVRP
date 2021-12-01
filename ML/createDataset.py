import numpy as np
import csv

import ML.k_means as ml
from solution.constructive.clarkwrightsaving import clarkWrightSaving
from solution.metaheuristic.tabusearch import tabuSearch
import problem.cvrp.instance as cvrp
import time

class Dataset():

    def __init__(self, filename1, filename2, cvrpbench, paramCVRP_alea):
        self.__paramCVRP_alea = paramCVRP_alea
        self.__file1 = filename1
        self.__file2 = filename2
        self.__cvrpbench = cvrpbench

        self.__nb_iteration = [100,125,150]
        self.__aspiration = [False,True]
        self.__time =[60,75]
        self.__nb_customer=[15,19,178,189,20,39,254,297,44,49,50,54,59,64,69,75,100,120,150,199,31,32,
        33,35,37,79,107,112,134,167,16,18,202,231,247,276,21,22,301,376,403,387,10,88,
        93,127,146,29,171,212]
        self.__tabu_list_lenght = []


    def create(self,d,f):
        #for i in range(len(self.__nb_customer)):
        start_time = time.time()
        for i in range(d,f):
            for j in range(10):
                nb_c = self.__nb_customer[i]
                self.__tabu_list_lenght = [int(nb_c/4),int(nb_c/2),nb_c-1]
                ind_alea = np.random.randint(0,len(self.__paramCVRP_alea))
                c = cvrp.Cvrp()
                c.randomInstance(nb_c,self.__paramCVRP_alea[ind_alea][0],self.__paramCVRP_alea[ind_alea][1],self.__paramCVRP_alea[ind_alea][2],100)
                KM = ml.K_means(c)
                KM.run()
                DB = KM.DB
                num_graph = i + j
                self.test_all_parameters(nb_c,c,c.minVehiculeNumber(),c.vehicule_capacity,DB,num_graph)
        print(time.time() - start_time, " seconds")

    def create_from_bench(self,d,f):
        start_time = time.time()
        for i in range(d,f):
                c = cvrp.Cvrp(file_path=self.__cvrpbench[i], file_type="web")
                nb_c = c.nb_customer
                self.__tabu_list_lenght = [int(nb_c/4),int(nb_c/2),nb_c-1]
                KM = ml.K_means(c)
                KM.run()
                DB = KM.DB
                num_graph = i
                self.test_all_parameters(nb_c,c,c.minVehiculeNumber(),c.vehicule_capacity,DB,num_graph)
        print(time.time() - start_time, " seconds")

    def test_all_parameters(self, nb_cust, cvrp, nb_V,capacity,DB,num_graph):
        L = []
        L_all_res = []
        a = np.random.randint(0,2)
        if a==0:
            a = False
        else:
            a = True

        for n in self.__nb_iteration:
            for l in self.__tabu_list_lenght :
                for t in self.__time :
                    s = clarkWrightSaving(cvrp)
                    tab = tabuSearch(initial_solution=s,number_iteration = n,aspiration = a,tabu_length = l,max_second_run = t)
                    res = tab.best_solution_evaluation_evolution[-1]
                    L.append(res)
                    P = [n,a,l,t,nb_cust,nb_V,capacity,DB,res,num_graph]
                    L_all_res.append(P)
                    with open(self.__file2,'a',newline='', encoding='utf-8') as fichiercsv2:
                        writer=csv.writer(fichiercsv2)
                        writer.writerow(P)

        ind = np.argmin(L)
        with open(self.__file1,'a',newline='', encoding='utf-8') as fichiercsv:
            writer=csv.writer(fichiercsv)
            writer.writerow(L_all_res[ind])
