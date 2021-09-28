#!/usr/bin/env python3

# A supprimer !!!!
# Juste pour tester le programme facilement
import problem.cvrp.cvrp as cvrp
import networkx as nx
import utils.mathfunctions as mathfunc
import tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy
#Added in order to display matrix
import numpy as np
import pandas as pd



def main():
    c = cvrp.Cvrp(file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp", file_type="web")
    d = copy.copy(c)
    d.showMathPlotLib()

    #this should be put into a function 'maybe distanceMatrix
    #Creates columns and rows name for distance matrix
    row_names =[]
    column_names =[]
    for i in range(c.nb_customer+1):
        row_names.append("Node number "+str(i+1)+"  ")
        column_names.append("Distance from node number "+str(i))

    #Allows to see the whole matrix
    pd.set_option('display.max_columns', None)
    #Data frame in order to display columns and rows names
    distanceMatrix = pd.DataFrame(c.distanceMatrix(), columns=column_names, index=row_names)
    #Print de distance matrix
    print(distanceMatrix)
    """
    root = Tk.Tk()
    root.wm_title("Animated Graph embedded in TK")
    # Quit when the window is done
    root.wm_protocol('WM_DELETE_WINDOW', root.quit)
    f=c.getFigureMathPlotLib()
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    Tk.mainloop()
    """


if __name__ == "__main__":
    main()
