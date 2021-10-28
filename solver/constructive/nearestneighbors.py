#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union
from itertools import combinations
import sys

import numpy as np

# Modules
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from solution.cvrp.route import RouteCvrp
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import NodeWithCoord
import utils.mathfunctions as mathfunc


def nearestNeighbors(cvrp: Cvrp) -> SolutionCvrp:
    """
    nearestNeighbors()
    
    Function to run nearestNeighbors algorithm on a given cvrp
    
    :param cvrp: Cvrp instance
    :type cvrp: Cvrp
    :return: A valid solution for the cvrp instance
    :rtype: SolutionCvrp
    """
    
    # Get the depot
    depot: DepotCvrp = cvrp.depot
    
    # Create a list of node to insert in route
    node_to_insert: List[CustomerCvrp] = cvrp.customers[:]
    
    # Cost of the route
    route_cost: Dict[int, Dict[int, float]] = {}
    
    route_list: List[RouteCvrp] = []
    
    for node in node_to_insert:
        # Initialize the dictionnary
        route_cost[node.node_id] = {}
    
    # for each node
    for index, node in enumerate(node_to_insert[:-1]):
        # For all next nodes
        for arrival in node_to_insert[index:]:
            # Compute their distance
            distance = mathfunc.euclideanDistance(node, arrival)
            # Add the values to the dict
            route_cost[node.node_id].update({arrival.node_id: distance})
            route_cost[arrival.node_id].update({node.node_id: distance})
    
    # List of route
    route_list: List[RouteCvrp] = []
    
    customer_insert: CustomerCvrp = None
    new_route_list: List[NodeWithCoord] = []
    # While there's node to insert into route
    while len(node_to_insert) > 0:
        # If the route is finished
        if customer_insert is None:
            # First iteration
            if len(new_route_list) == 0:
                # Start the route at the depot
                new_route_list = [depot]
                # Add the first customer to the route
                new_route_list.append(node_to_insert.pop())
                # Compute the demand
                demand_supplied: int = new_route_list[-1].demand
            else:
                # Add the depot at the end of the route
                new_route_list.append(depot)
                # Build the route
                new_route: Route = RouteCvrp(route=new_route_list)
                # Add the route to the route list
                route_list.append(new_route)
                # Start the route at the depot
                new_route_list = [depot]
                # Add the first customer to the route
                new_route_list.append(node_to_insert.pop())
                # Compute the demand
                demand_supplied: int = new_route_list[-1].demand
        else:
            # Route demand supplied
            demand_supplied += customer_insert.demand
            # add the customer to the list
            new_route_list.append(customer_insert)
            # Remove the customer from the list of customer to add
            node_to_insert.remove(customer_insert)
            # Reset the customer_insert value
            customer_insert = None
           
        # To get the nearest neighbors   
        closest: float = sys.maxsize
        
        for node in node_to_insert:
            # If the node could be integrated in the route and the distance is near
            if (demand_supplied + node.demand <= cvrp.vehicule_capacity and
                route_cost[new_route_list[-1].node_id][node.node_id] < closest):
                # Set the customer to be add
                customer_insert = node
                     
    # Add the depot at the end of the route
    new_route_list.append(depot)
    # Build the route
    new_route: Route = RouteCvrp(route=new_route_list)
    # Add the route to the route list
    route_list.append(new_route)
                
    # Build the solution
    sol: SolutionCvrp = SolutionCvrp(instance=cvrp, route=route_list)
    
    return sol
        
