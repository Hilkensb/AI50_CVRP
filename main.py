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
from solver.constructive.clarkwrightsaving import clarkWrightSaving
from solver.constructive.nearestneighbors import nearestNeighbors
from solver.metaheuristic.tabusearch import tabuSearch
from utils.otherplotting import getHtmlSolutionEvolutionAnimationPlotly


def main():
    c = cvrp.Cvrp(file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n101-k4.vrp", file_type="web")
    s = sol.SolutionCvrp(c)
    #s.readSolutionWeb(url="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/X/X-n502-k39.sol")
    #print(s.getHtmlFigurePlotly())
    # s.showFigure()
    s = clarkWrightSaving(c)
    #s = nearestNeighbors(c)
    #print(s.evaluation())
    #print(s.isValid())
    #displayTabuSearchResult(s)
    t = tabuSearch(s, max_second_run=10, number_iteration=500)
    #print(t.best_solution_evolution[-1].isValid())
    #print(t.best_solution_evolution[-1].evaluation())
    #print(len(t.best_solution_evolution))
    #showSolutionEvolutionAnimation(t.best_solution_evolution, auto_node_size=True, with_labels=True)
    print(getHtmlSolutionEvolutionAnimationPlotly(t.best_solution_evolution))

if __name__ == "__main__":
    main()
