#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List
import copy

# Other Library
# An extension of itertools
from more_itertools import pairwise
# To overide method
from functools import singledispatchmethod

# Modules
from problem.node import nodeWithCoord
import utils.mathfunctions as mathfunc


class Route:
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #

    def __init__(self, route: List[nodeWithCoord]) -> Route:
       """
       """
       
       # List of customers representing the route made by one vehicule
       self.__customers_route: List[nodeWithCoord] = route
       
    def __str__(self) -> str:
        """
        """
        # Show every node (in the order of the route) seperates by "-"
        return "-".join(str(customer.node_id) for customer in self.__customers_route)
        
    def __repr__(self) -> str:
        """
        """
        # Show every node (in the order of the route) seperates by "-"
        return "-".join(str(customer.node_id) for customer in self.__customers_route)
        
    def __copy__(self) -> Route:
        """
        """
        # Put all the customers in a list
        customers_route_copy: List[nodeWithCoord] = self.__customers_route[:]
        # Create a copy of the route based on the customers_route_copy created on the prvious line
        route_copy: Route = Route(route=customers_route_copy)
        
        return route_copy
      
    def __deepcopy__(self) -> Route:
        """
        """
        # Copy all the customers in the route
        customers_route_copy: List[nodeWithCoord] = [copy.copy(route) for route in self.__customers_route]
        # Create a copy of the route based on the customers_route_copy created on the prvious line
        route_copy: Route = Route(route=customers_route_copy)
        
        return route_copy  
      
    def __len__(self) -> int:
        """
        """
        # Return the len of the string
        return len(self.__customers_route)
    
    # TODO a tester    
    def __eq__(self, other: Route) -> bool:
        """
        """
        
        # We do not compare their cost because it's an heavy operation, which would cost
        # a lot of time
        
        # Since we will use more than one time this operation it's more optimal to do it once and store the result
        route_length: int = len(self)
        
        # Compare their lengh
        # If the len of this route and the other route are different we can be sure that they are different
        # If they have the same amount of node we need to test each node one by one
        if route_length != len(other):
            return False
            
        # If we are here we know that both routes have the same length
        # Since they both starts and end at depot (or at least should if it's a valid solution)
        # We will not compare the first and last element to gain some ressource time
        # If one or both does not start and/or end at the depot it will then (a bit later normaly)
        # consider as a non valid route
        # /!\ This must have been done earlier to test if it's a valid route
        
        # We compare every customer of the route
        # If they are all equal return true else false
        return self[1:route_length] == other[1:route_length]
      
    @singledispatchmethod  
    def __getitem__(self, indices) -> nodeWithCoord:
        """
        """
        raise TypeError(f"The method __getitem__ is not implemented with the {type(indices)} type.")
       
    @__getitem__.register 
    def getitemImplementation(self, indices: int) -> nodeWithCoord:
        """
        """
        return self.__customers_route[indices]
        
    @__getitem__.register 
    def getitemImplementation(self, indices: slice) -> List[nodeWithCoord]:
        """
        """
        return self.__customers_route[indices]
        
    
# --------------------------------- Methods --------------------------------- #

    # TODO: Put the evealuation in integer ? (as the cvrplib do) with a round or keep it in float and be more precise ?
    def evaluation(self) -> float:
        """
        """
        
        # The evaluation of the route
        evaluation: float = 0
        
        # For every node in the route
        # The pairwise function of itertools create pair of elements that are
        # following in an iterable (here a list)
        # More info : https://docs.python.org/3/library/itertools.html#itertools-recipes
        for node_pair in pairwise(self.__customers_route):
            # sum the euclidean distance of node that are following each other
            # Get the distance between the nodes
            distance: float = mathfunc.euclideanDistance(node_pair[0], node_pair[1])
            # Add the distance to the evaluation
            evaluation += distance
            
        # Return the evaluation of the route
        return evaluation
        
    def isValid(self) -> bool:
        """
        """
        pass
       
# ----------------------------- Getter / Setter ----------------------------- #

    @property 
    def customers_route(self) -> List[nodeWithCoord]:
        return self.__customers_route
        
    @customers_route.setter
    def customers_route(self, value: List[nodeWithCoord]) -> None:
        self.__customers_route = value
