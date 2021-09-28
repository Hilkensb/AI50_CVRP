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



def main():
    c = cvrp.Cvrp(file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp", file_type="web")
    d = copy.copy(c)
    d.showMathPlotLib()
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
