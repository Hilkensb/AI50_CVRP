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


def main():
    getOptions(sys.argv[1:])

    app = Application()
    app.run()
    

if __name__ == "__main__":
    main()

