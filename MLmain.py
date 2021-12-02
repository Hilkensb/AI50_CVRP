#!/usr/bin/env python3

# A supprimer !!!!
# Juste pour tester le programme facilement
import problem.cvrp.instance as cvrp
import networkx as nx
import utils.mathfunctions as mathfunc
import tkinter as tk
import matplotlib
import csv
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy
import solution.cvrp.solution as sol
import solution.solver.solver as slv
import numpy as np
import problem.cvrp.customer as cust
from gui.app import Application
from utils.parseparameters import getOptions
import sys
from solution.constructive.clarkwrightsaving import clarkWrightSaving
from solution.metaheuristic.tabusearch import easyTabuSearch
from solution.metaheuristic.tabusearch import tabuSearch
from utils.otherplotting import showSolutionEvolutionAnimationMatplotlib
import ML.k_means as ml
import ML.createDataset as db
import ML.model as md

def main():

    model = md.ModelSeq()

    #c = cvrp.Cvrp(file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp", file_type="web")
    #s = clarkWrightSaving(c)
    #t = tabuSearch(initial_solution=s,number_iteration = 100,aspiration = False,tabu_length = 3,max_second_run = 60)
    #res = t.best_solution_evaluation_evolution[-1]

    #c = cvrp.Cvrp()
    #c.randomInstance(70,40,7,30,100)
    #KM = ml.K_means(c)
    #KM.run()
    #print(KM.DB)
    #KM.show()


    #with open('data.csv','w',newline='') as fichiercsv:
        #writer=csv.writer(fichiercsv)
        #writer.writerow(['Number of iterations','aspiration','lenght of tabu list','maximum run time',
        #'Nb customers','Nb vehicles','Capacity','DB','results','num graph'])

    #with open('dataComplet.csv','w',newline='') as fichiercsv2:
        #writer=csv.writer(fichiercsv2)
        #writer.writerow(['Number of iterations','aspiration','lenght of tabu list','maximum run time',
        #'Nb customers','Nb vehicles','Capacity','DB','results','num graph'])




    #s = sol.SolutionCvrp(c)
    #s.readSolutionWeb(url="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.sol")
    #print(s.showFigure())


    #S = slv.Solver(c.customers,c.minVehiculeNumber(),c.vehicule_capacity,c.distanceMatrix())
    #S.run()
    #S.show()



    cvrp_bench = [
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n19-k2.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n20-k2.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n21-k2.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n22-k2.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n22-k8.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n23-k8.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n40-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n45-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n50-k7.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n50-k8.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n50-k10.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n55-k7.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n55-k10.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n55-k15.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n60-k10.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n60-k15.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n65-k10.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n70-k10.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n76-k4.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n76-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n101-k4.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/M/M-n101-k10.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/M/M-n121-k7.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/M/M-n151-k12.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/M/M-n200-k16.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/M/M-n200-k17.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n32-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n33-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n33-k6.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n34-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n36-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n37-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n37-k6.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n38-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n39-k5.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n39-k6.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n44-k6.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n45-k6.vrp",
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n45-k7.vrp"
    ]

    paramCVRP_alea = [(40,7,30),(35,1,31),(160,1,30),(3000,100,2500),
    (140,5,45),(45,3,30),(150,8,31),(50,5,29),(280,5,40),(100,5,29),(170,6,30),(55,5,40),
    (60,5,40),(80,5,40),(130,4,37),(135,5,40),(350,5,40),(400,3,50),(200,10,50),(200,3,35),(100,4,30)]

    dataset = db.Dataset('data.csv','dataComplet.csv',cvrp_bench,paramCVRP_alea)
    #dataset.create(0,1)   #chaque dataset.create a une durée d'environ 3h20
    #dataset.create(1,2)
    #dataset.create(2,3)
    #dataset.create(3,4)
    #dataset.create(4,5)
    #dataset.create(5,6)
    #dataset.create(6,7)
    #dataset.create(7,8)
    #dataset.create(8,9)
    #dataset.create(9,10)
    #dataset.create(10,11)
    #dataset.create(11,12)
    #dataset.create_from_bench(0,10)
    #dataset.create_from_bench(10,20)
    #dataset.create_from_bench(20,30)
    #dataset.create_from_bench(30,40)



if __name__ == "__main__":
    main()
