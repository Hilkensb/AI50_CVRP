#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union
from itertools import combinations

# Modules
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from solution.cvrp.route import RouteCvrp
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import NodeWithCoord
import utils.mathfunctions as mathfunc


def clarkWrightSaving(cvrp: Cvrp) -> SolutionCvrp:
    """
    clarkWrightSaving()
    
    Function to run Clark Wright Saving algorithm on a given cvrp
    
    :param cvrp: Cvrp instance
    :type cvrp: Cvrp
    :return: A valid solution for the cvrp instance
    :rtype: SolutionCvrp
    """
    
    # Get the depot node
    depot: DepotCvrp = cvrp.depot
    # Get all customers
    customers_list: List[CustomerCvrp] = cvrp.customers
    # List of routes 
    routes_list: List[RouteCvrp] = []
    # Saving of customers
    route_saving: List[Tuple[NodeWithCoord, NodeWithCoord, int]] = []
    # Dictionnary to link customers node id to their route
    route_finder: Dict[int, RouteCvrp] = {}
    # Get the vehicule capacity
    vehicule_capacity: int = cvrp.vehicule_capacity
    
    # Build the firsts routes  
    for customer in customers_list:
        # Create a route (node list) for the customer
        # The route is depot then the customer and finally the depot
        customer_route: List[NodeWithCoord] = [depot, customer, depot]
        # Build the Route
        route: RouteCvrp = RouteCvrp(route=customer_route)
        # Index the customer and it's route
        route_finder[customer.node_id] = route
        # Add the route to the list of route
        routes_list.append(route)
    
    # Iterate for each customer combination to calcul their savings
    for customer1, customer2 in combinations(customers_list, 2):
        # Get the distance to the calcul the saving
        # Distance between customer1 and depot
        dist_cust1_depot: float = mathfunc.euclideanDistance(depot, customer1)
        # Distance between customer2 and depot
        dist_cust2_depot: float = mathfunc.euclideanDistance(depot, customer2)
        # Distance between customer1 and customer2
        dist_cust1_cust2: float = mathfunc.euclideanDistance(depot, customer2)
        
        # cacul the saving
        cost_saving: float = dist_cust1_depot + dist_cust2_depot - dist_cust1_cust2
        # customers combination and their saving
        saving_tuple: Tuple[NodeWithCoord, NodeWithCoord, int] = (customer1, customer2, cost_saving)
        # Add the saving tuple to our list of savings
        route_saving.append(saving_tuple)
        
    # Sort the route_saving by their saving cost in increasing order
    # We will then use pop to get the largest saving (in the tail of the list)
    # Taking tail of list is more time saving than taking head
    route_saving.sort(key=lambda x:x[2])
    
    # for each saving
    while len(route_saving) > 0:
        # Get the saving tuple
        saving_tuple: Tuple[NodeWithCoord, NodeWithCoord, int] = route_saving.pop()
        # Get the route of the first customer
        route1: RouteCvrp = route_finder[saving_tuple[0].node_id]
        # Get the route of the second customer
        route2: RouteCvrp = route_finder[saving_tuple[1].node_id]
        
        # Check condition to merge the route
        # If the two route are the same, skip it
        if (route1 == route2):
            # Go to the next saving
            continue
       
        # Position of the customer1 in the route1
        customer1_index = route1.customers_route.index(saving_tuple[0])     
        # The customer need to be either first or last customer of the route
        if (customer1_index != 1 and customer1_index != len(route1.customers_route) - 2):
            # Go to the next saving
            continue
            
        # Position of the customer1 in the route1
        customer2_index = route2.customers_route.index(saving_tuple[1])     
        # The customer need to be either first or last customer of the route
        if (customer2_index != 1 and customer2_index != len(route2.customers_route) - 2):
            # Go to the next saving
            continue

        # Ensure that the vehicule capacity is lower than the sum of demand supplied by both route
        if (route1.demandSupplied() + route2.demandSupplied() > vehicule_capacity):
            continue

        # If it's here the route can be merged
        # Route of customer start the route
        start_route_list: List[CustomerCvrp] = None
        # Route of customer end the route
        end_route_list: List[CustomerCvrp] = None
        
        # If both customer are at the end of their route
        if (customer1_index == 1 and customer2_index == 1):
            start_route_list = route1.customers_route[1:-1]
            end_route_list = route2.customers_route[1:-1]
            end_route_list.reverse()
        # If both customer are at the start of their route
        elif (customer1_index == len(route1.customers_route) - 2 and
                  customer2_index == len(route2.customers_route) - 2):
            start_route_list = route1.customers_route[1:-1]
            start_route_list.reverse()
            end_route_list = route2.customers_route[1:-1]
        # If customer1 is at the start of his route and customer2 is at the end of his route
        elif (customer1_index == 1):
            start_route_list = route1.customers_route[1:-1]
            end_route_list = route2.customers_route[1:-1]
        # If customer2 is at the start of his route and customer1 is at the end of his route
        elif (customer2_index == 1):
            start_route_list = route2.customers_route[1:-1]
            end_route_list = route1.customers_route[1:-1]

        # Merge the lists
        # Starts and end by depot
        # merge the list by fusionning the customer at the end of end_route_list
        # and at the start of start_route_list
        merged_route: List[NodeWithCoord] = [depot, *end_route_list, *start_route_list, depot]
        
        # Build the route
        new_route: RouteCvrp = RouteCvrp(route=merged_route)
        # Update the index of the customer and it's route
        for customer_updated in merged_route[1:-1]:
            route_finder[customer_updated.node_id] = new_route

        # Update the route list
        # Removes the previous lists
        routes_list.remove(route1)
        routes_list.remove(route2)
        # Add the new route
        routes_list.append(new_route)
        
    # Build the solution
    solution: SolutionCvrp = SolutionCvrp(instance=cvrp, route=routes_list)
    # Return the solution
    return solution
        
