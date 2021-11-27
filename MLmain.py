#!/usr/bin/env python3

# A supprimer !!!!
# Juste pour tester le programme facilement
import problem.cvrp.instance as cvrp
import networkx as nx
import utils.mathfunctions as mathfunc
import tkinter as tk
import matplotlib
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
from utils.otherplotting import showSolutionEvolutionAnimationMatplotlib
import ML.k_means as ml

def main():

    #c = cvrp.Cvrp(file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp", file_type="web")
    c = cvrp.Cvrp()
    c.randomInstance(16,40,7,30,100)
    KM = ml.K_means(c)
    KM.run()
    

    print(KM.DB)
    KM.show()

    #s = sol.SolutionCvrp(c)
    #s.readSolutionWeb(url="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.sol")
    #print(s.showFigure())


    #S = slv.Solver(c.customers,c.minVehiculeNumber(),c.vehicule_capacity,c.distanceMatrix())
    #S.run()
    #S.show()

    #test
    #data=np.array([(1,10),(1.5,2),(1,6),(2,1.5),(2,10),(3,2.5),(3,6),(4,2)])
    #classes=np.array([1,2,1,2,1,2,1,2],dtype=np.int)

    #KM = ml.K_means(2,1,1,1,1,data)
    #KM.run(2)


if __name__ == "__main__":
    main()
