import pyomo.environ as pyo
from itertools import combinations
import numpy as np
#import pyomo

class Solver():
    #class solver to resolve the CVRP problem from the mathematical modeling presented
    #in the report
    def __init__(self,customers,nb_vehicles,Q,cost):
        #super(Solver,self).__init__()
        #using of a concrete model
        self.__model = pyo.ConcreteModel()
        #retrieving the parameters of the CVRP problem
        self.__customers = customers
        self.__nbVehicules = nb_vehicles
        self.__capacity = Q
        self.__cost = cost
        #initialization of the sets, the parameters, the variables used, the
        #objective function and the constraints
        self.init_customers_parameters()
        self.create_sets()
        self.create_parameters()
        self.create_variables()
        self.create_objectif()
        self.create_constraintes()

    #function to initialize the parameters of customers
    def init_customers_parameters(self):

        self.__numCustomers = []
        self.__demands = {}
        for c in self.__customers:
            self.__numCustomers.append(c.node_id-1)
            self.__demands[c.node_id-1] = c.demand

    #function to initialize the sets used in the mathematical model
    def create_sets(self):

        #set {1,...,n} number of customers
        self.__model.__n = pyo.Set(initialize=self.__numCustomers)

        #print(self.__model.n.data())
        K = []
        for i in range(1,self.__nbVehicules+1):
            K.append(i)
        #set {1,...,k} number of vehicles
        self.__model.__k = pyo.Set(initialize=K)

        P = list(self.__numCustomers)
        for j in range(len(P)):
            P[j] = P[j] - 1
        P.append(self.__numCustomers[len(self.__numCustomers)-1])
        print(P)
        #set {0,...,p} number of nodes (depot + customers)
        self.__model.__p = pyo.Set(initialize=P)

    #function to initialize the parameters of the mathematical model
    def create_parameters(self):

        self.__model.__D = pyo.Param(self.__model.__n,initialize = self.__demands)

        q = {}
        for i in range(1, self.__nbVehicules+1):
            q[i] = self.__capacity
        self.__model.__Q = pyo.Param(self.__model.__k,initialize = q)

        c = {}

        for x in range(np.shape(self.__cost)[0]):
            for y in range(np.shape(self.__cost)[1]):
                if x==y :
                    c[(x,y)] = 0.
                else:
                    c[(x,y)] = self.__cost[x,y]

        self.__model.__C = pyo.Param(self.__model.__p,self.__model.__p, initialize =  c)

    #function to create the binary variables
    def create_variables(self):

        self.__model.__x = pyo.Var(self.__model.__p,self.__model.__p,self.__model.__k,within = pyo.Binary)
    #methode to create the objective function to minimize
    def create_objectif(self):

        self.__model.__obj = pyo.Objective(expr = sum(self.__model.__C[i,j]*self.__model.__x[i,j,k]
                                                    for i in self.__model.__p
                                                    for j in self.__model.__p if j!=i
                                                    for k in self.__model.__k),sense = pyo.minimize)

    #methode to define mathematically the different constraints of the CVRP problem
    def create_constraintes(self):

        self.__model.__C1 = pyo.ConstraintList(doc = "Each customer be visited by exactly one vehicle")
        for j in self.__model.__n:
            self.__model.__C1.add(sum(self.__model.__x[i,j,k]
                                    for i in self.__model.__p if i!=j
                                    for k in self.__model.__k) == 1)

        self.__model.__C2 = pyo.ConstraintList(doc = "Each vehicle leave the depot")
        for k in self.__model.__k:
            self.__model.__C2.add(sum(self.__model.__x[0,j,k]
                                    for j in self.__model.__n) == 1)


        self.__model.__C3 = pyo.ConstraintList(doc = "number of vehicles which leave or arrive in the depot must be equal to the total number of vehicles")
        for k in self.__model.__k:
            for j in self.__model.__p:
                self.__model.__C3.add(
                    sum(self.__model.__x[i,j,k] for i in self.__model.__p if i!=j) ==
                    sum(self.__model.__x[j,i,k] for i in self.__model.__p))

        self.__model.__C4 = pyo.ConstraintList(doc = "capacity constraint")
        for k in self.__model.__k:
            self.__model.__C4.add(
                sum(self.__model.__D[j] * self.__model.__x[i,j,k]
                    for i in self.__model.__p
                    for j in self.__model.__n if j!=i) <= self.__model.__Q[k])

        self.__model.__C5 = pyo.ConstraintList(doc = "ensure no cycle disconnected : eliminate the subtours")
        for u in range (2,len(self.__numCustomers)+1):
            for s in combinations(self.__model.__n,u):
                self.__model.__C5.add(
                    sum(self.__model.__x[i,j,k] for i in s
                        for j in s if j!=i
                        for k in self.__model.__k) <= len(s) - 1
                )
    #methode to run the solver
    def run(self):
        self.__instance = self.__model.create_instance('data.dat')
        opt = pyo.SolverFactory('glpk')
        self.__result = opt.solve(self.__model)

    #methode to show the results of the solver
    def show(self):

        #instance.pprint()
        #opt = pyo.SolverFactory('gurobi', solver_io="python")
        #results = opt.solve(self.__model)
        #print(results)

        print(self.__result)
        #for v in self.__model.component_data_objects(pyo.Var):
                #if v.value == 1:
                    #print(str(v), v.value, )
        self.__instance.solutions.load_from(self.__result)
        res = 0
        for v in self.__instance.component_objects(pyo.Var, active=True):
            print ("Variable",v)
            varobject = getattr(self.__instance, str(v))
            for index in varobject:
                if self.__model.__x[index[0],index[1],index[2]].value==1:
                    print ("   ",index, self.__model.__x[index[0],index[1],index[2]].value)
                    res = res + self.__model.__C[index[0],index[1]]
        print("res : ", res)
        #self.__model.display()
