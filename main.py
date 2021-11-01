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

def main():
    app = Application()
    app.run()

if __name__ == "__main__":
    main()
