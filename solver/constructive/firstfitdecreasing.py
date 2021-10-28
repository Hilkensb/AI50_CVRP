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


def firstFitDecreasing(cvrp: Cvrp) -> SolutionCvrp:
        """
        firstFitDecreasing()
        
        Method to get a solution of the given cvrp instance
        
        :param cvrp: Cvrp instance to get a valid solution
        :type cvrp: Cvrp
        :return: A valid Solution
        :rtype: SolutionCvrp

        :raises RuntimeError: If there's no feasible solution (if a demand of at least on customer is higher than the capacity of vehicules)

        """
        
        # Get the depot of the cvrp
        depot_node: DepotCvrp = cvrp.depot
        
        # Get all the customers demand into a list
        # To do so iterate throw all customers (only the customers node)
        # and get their demand
        customers: List[int] = [customer for customer in cvrp.customers]
        
        # Sort the demand (in decreasing order)
        customers.sort(key=lambda c:c.demand, reverse=True)
        
        # To calculate the number of vehicule we need to have a variable that will
        # be decreasing for every customer demand and which start from the 
        # vehicule capacity 
        actual_vehicule_capacity: int = cvrp.vehicule_capacity

        # Check if a solution exists or not
        # If the highest demand is higher than the vehicule capacity,
        # it means that this customer (may be others too ?) cannot be delivered by
        # vehicule with this capacity
        # There will no feasible solution for this problem (since at least one
        # customer can't be delivered).
        # Since there will be no solution, the minimum vehicule to solve the problem
        # is none
        if customers[0].demand > cvrp.vehicule_capacity:
            # Raise a RuntimeError to show that there's no feasible solution
            raise RuntimeError(f"The highest customer demand is higher than the vehicule capacity ({customers_demand[0]} > {self.__vehicule_capacity}). At least one (or more) customer(s) can't be deliver by a vehicule. No feasible solution for this problem!") 

        # List of all routes
        route_list: List[RouteCvrp] = []

        # while the customers_demand has values in it, run the while loop
        while customers:
            # Reset the actual vehicule capacity (we start from a new vehicule,
            # because the previous had his maximum capacity)
            actual_vehicule_capacity = cvrp.vehicule_capacity
            
            # Create a list that will store the customer
            new_route: List[CustomerCvrp] = []
            # Add the depot as first node
            new_route.append(depot)
            
            # Customers demand that have not been delivered by the previous vehicules
            # Create a copy of the customer_demand
            # Since we are using after a for loop, we can't pop element of the list
            # we are iterating throw in the for loop
            # We need 2 list, one we iterate throw and another one where we pop
            # demand that have been delivered by the vehicule
            # Update the customers demand
            actual_customer = customers[:]
            
            # for every demand (sorted in decreasing order)
            for customer in actual_customer:
                # Check if the demand can be delivered by the vehicule
                if customer.demand <= actual_vehicule_capacity:
                    # Add the demand in the vehicule
                    # So remove the demand space free in the vehicule
                    actual_vehicule_capacity -= customer.demand
                    # The customer demand have been solved
                    # We can remove it from the list of demand
                    customers.remove(customer)
                    # Add the customer to the route
                    new_route.append(customer)
                    
            # add the depot as the last node
            new_route.append(depot)
            # Build the route
            builded_route: RouteCvrp = RouteCvrp(route=new_route)
            # Add the builded route to the solution
            route_list.append(builded_route)
            
        # Create the solution with the route found    
        solution: SolutionCvrp = SolutionCvrp(instance=cvrp, route=route_list)
        # Return the solution found         
        return solution
