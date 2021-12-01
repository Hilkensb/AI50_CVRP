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

def main():

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
    #dataset.create(12,13)   #chaque dataset.create a une durée d'environ 3h20
    #dataset.create(13,14)
    #dataset.create(14,15)
    #dataset.create(15,16)
    #dataset.create(16,17)
    #dataset.create(17,18)
    #dataset.create(18,19)
    #dataset.create(19,20)
    dataset.create(20,21)
    #dataset.create(21,22)
    #dataset.create(22,23)
    #dataset.create(23,24)




if __name__ == "__main__":
    main()
