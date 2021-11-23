# A supprimer une fois que sarl marche !!!!

from solution.multiagents.sarlcommunication import sarlSender
from problem.cvrp.instance import Cvrp

c = Cvrp()
print(sarlSender("aa", c))
