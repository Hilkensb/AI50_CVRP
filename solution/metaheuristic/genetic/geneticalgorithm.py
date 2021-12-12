from olution.metaheuristic.genetic.algo_genetic import genetic 
import numpy as np
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from solution.cvrp.route import RouteCvrp
import copy


def geneticAlgorithm(cvrp: Cvrp):
    """
    """
    
    number_conductor: int = cvrp.minVehiculeNumber()
    number_node: int = cvrp.nb_customer
    vehicle_capacity: int = cvrp.vehicule_capacity
    customer_demand: List[int] = [customer.demand for customer in cvrp.customers]
    distance: np.nparray = np.array(cvrp.distanceMatrix())

    fitness, population = genetic(number_conductor, number_node, vehicle_capacity, customer_demand, distance)

    route_list = []
    while len(population) > 0:
        population, subroute = createSubRoute(population, vehicle_capacity, customer_demand)
        subroute = [cvrp.getCustomerByCustomerNumber(sub) for sub in subroute]
        route: RouteCvrp = RouteCvrp(route=[cvrp.depot, *subroute, cvrp.depot])
        route_list.append(route)
        
    solution: SolutionCvrp = SolutionCvrp(instance=cvrp, route=route_list)
    
    return solution, solution.evaluation()
    
    
def createSubRoute(population, vehicle_capacity, customer_demand):
    """
    """
    
    # The demand supplied
    demand_supplied: int = vehicle_capacity
    
    # Store teh customers
    result: List = []
    
    # Copy the population
    population_copy: List = copy.copy(population)

    print(population)
    for customer in population:
        if (demand_supplied - customer_demand[customer] > 0):
            demand_supplied -= customer_demand[customer]
            result.append(customer)
            population_copy.remove(customer)
  
    return population_copy, result

