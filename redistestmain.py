# A supprimer une fois que sarl marche !!!!

from solution.multiagents.sarlcommunication import sarlSender
from problem.cvrp.instance import Cvrp

c = Cvrp("http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/X/X-n439-k37.vrp", "web")
s = sarlSender("aa", c)
print(s.evaluation())
print(s.isValid())
s.showFigure()
