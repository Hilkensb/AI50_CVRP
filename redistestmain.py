# A supprimer une fois que sarl marche !!!!
from __future__ import annotations
from solution.multiagents.sarlcommunication import sarlSender
from problem.cvrp.instance import Cvrp
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from solution.cvrp.solution import RouteCvrp
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import NodeWithCoord
import random
import numpy
import sys
import copy
from typing import List, Dict, Tuple, Union
import math
from solution.metaheuristic.gwo import greyWolfSolver


c = Cvrp("http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n76-k5.vrp", "web")
# s = sarlSender("aa", c)
s = greyWolfSolver(c)[0][0]
print(s.evaluation())
print(s.isValid())
s.showFigure()

