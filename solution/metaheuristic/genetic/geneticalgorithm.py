#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import copy

# Other Library
import numpy as np

# Other module
from solution.metaheuristic.genetic.algo_genetic import genetic 
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from solution.cvrp.route import RouteCvrp
from gui.config import SOLUTION_TOPIC


def geneticAlgorithm(
    cvrp: Cvrp, num_generations: int = 20, topic: str = SOLUTION_TOPIC
) -> Tuple[List[SolutionCvrp], List[int]]:
    """
    geneticAlgorithm()
    
    Function to run and return result of the genetic algorithm
    
    :param cvrp: Cvrp instance to solve
    :type cvrp: Cvrp
    :param num_generations: Number of generation to run, default to 20 (opt.)
    :type num_generations: int
    :return: The best solution found and it's evaluation
    :param topic: Redis topic, default to SOLUTION_TOPIC (opt.)
    :type topic: str
    """
    
    # Compute variable needed by the genetic algorithm
    # Get the number of vehicles needed at least
    number_conductor: int = cvrp.minVehiculeNumber()
    # Get the number of customers
    number_node: int = cvrp.nb_customer
    # Get the vehicle capacity
    vehicle_capacity: int = cvrp.vehicule_capacity
    # Get the demand of each customer
    customer_demand: List[int] = [customer.demand for customer in cvrp.customers]
    # Get the distance matrix
    distance: np.nparray = np.array(cvrp.distanceMatrix())

    # Run the genetic algorithm
    fitness, population = genetic(number_conductor, number_node, vehicle_capacity, customer_demand, distance, topic=topic, num_generations=num_generations)

    # Create the routes
    route_list = []
    # While ther's customers in the population
    while len(population) > 0:
        population, subroute = createSubRoute(population, vehicle_capacity, customer_demand)
        subroute = [cvrp.getCustomerByCustomerNumber(sub) for sub in subroute]
        route: RouteCvrp = RouteCvrp(route=[cvrp.depot, *subroute, cvrp.depot])
        route_list.append(route)
        
    solution: SolutionCvrp = SolutionCvrp(instance=cvrp, route=route_list)
    
    return [solution], [solution.evaluation()]
    
    
def createSubRoute(population, vehicle_capacity, customer_demand) -> Tuple[List[SolutionCvrp], List[int]]:
    """
    createSubRoute()
    
    Function to create route from the population returned by the genetic algorithm
    
    :param population: Population generated by the genetic algorithm
    :type population: List[int]
    :param vehicle_capacity: Capacity of vehicles
    :type vehicle_capacity: int
    :param customer_demand: Demand of the customers
    :type customer_demand: List[int]
    :return: The updated population and the builded route
    :rtype: Tuple[List[SolutionCvrp], List[int]]
    """
    
    # The demand supplied
    demand_supplied: int = vehicle_capacity
    
    # Store teh customers
    result: List = []
    
    # Copy the population
    population_copy: List = copy.copy(population)

    # For every customers that are still in the population
    for customer in population:
        # If the capacity constraint is respected
        if (demand_supplied - customer_demand[customer] > 0):
            demand_supplied -= customer_demand[customer]
            # Add the customer to the route
            result.append(customer)
            population_copy.remove(customer)
  
    return population_copy, result

