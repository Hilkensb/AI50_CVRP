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
import ML as ml

class test():

    def __init__(self):
        self.__t = [1, 2, 3]

    @property
    def t(self) :
        return self.__t


def main():
    #c = cvrp.Cvrp(file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp", file_type="web")
    c = cvrp.Cvrp()
    c.randomInstance(7,50,10,30,100)
    #s = sol.SolutionCvrp(c)
    #s.readSolutionWeb(url="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.sol")
    #print(s.showFigure())


    #S = slv.Solver(c.customers,c.minVehiculeNumber(),c.vehicule_capacity,c.distanceMatrix())
    #S.run()
    #S.show()

    #test
    data=np.array([(1,10),(1.5,2),(1,6),(2,1.5),(2,10),(3,2.5),(3,6),(4,2)])
    classes=np.array([1,2,1,2,1,2,1,2],dtype=np.int)

    KM = ml.K_means(2,1,1,1,1,data)
    KM.run(2)
    
    """
    root = Tk.Tk()
    root.wm_title("Animated Graph embedded in TK")
    # Quit when the window is done
    root.wm_protocol('WM_DELETE_WINDOW', root.quit)
    f=c.getFigure(fixed_size=False, show_legend=True)
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    Tk.mainloop()
    """

if __name__ == "__main__":
    main()
