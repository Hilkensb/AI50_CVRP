#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List

# Other Library
# An extension of itertools
from more_itertools import pairwise

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
        
        return "-".join(str(customer.node_id) for customer in self.__customers_route)
        
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
       
# ----------------------------- Getter / Setter ----------------------------- #

    @property 
    def customers_route(self) -> List[nodeWithCoord]:
        return self.__customers_route
        
    @customers_route.setter
    def customers_route(self, value: List[nodeWithCoord]) -> None:
        self.__customers_route = value
