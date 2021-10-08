#!/usr/bin/env python3

# A supprimer !!!!
# Juste pour tester le programme facilement
import problem.cvrp.instance as cvrp
import networkx as nx
import utils.mathfunctions as mathfunc
import tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy
import solution.cvrp.solution as sol



def main():
    c = cvrp.Cvrp(file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp", file_type="web")
    s = sol.SolutionCvrp(c)
    s.readSolutionWeb(url="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.sol")
    s.showFigure()
    


if __name__ == "__main__":
    main()
