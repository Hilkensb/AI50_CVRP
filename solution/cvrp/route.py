#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict
import copy
# To overide method
from functools import singledispatchmethod
from itertools import permutations
from collections import Counter

# Other Library
# An extension of itertools
from more_itertools import pairwise

# Modules
from problem.node import NodeWithCoord
import utils.mathfunctions as mathfunc
from problem.cvrp.depot import DepotCvrp
from problem.cvrp.customer import CustomerCvrp


class RouteCvrp:
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #

    def __init__(self, route: List[NodeWithCoord]) -> RouteCvrp:
       """
       Constructor
       
       :param route: Route to build
       :type route: List[NodeWithCoord]
       
       
       """
       
       # List of customers representing the route made by one vehicule
       self.__customers_route: List[NodeWithCoord] = route
       
    def __str__(self) -> str:
        """
        str
        
        Get the string value of the instance
        
        :return: A string value of the route
        :rtype: str
        
        """
        # Show every node (in the order of the route) seperates by "-"
        return "-".join(str(customer.node_id) for customer in self.__customers_route)
        
    def __repr__(self) -> str:
        """
        repr
        
        Get the string representation value of the instance
        
        :return: A string representation value of the route
        :rtype: str
        
        """
        # Show every node (in the order of the route) seperates by "-"
        return "-".join(str(customer.node_id) for customer in self.__customers_route)
        
    def __copy__(self) -> RouteCvrp:
        """
        copy
        
        Create a copy of the route
        
        :return: A copy of the route
        :rtype: RouteCvrp
        
        :exemple:

        >>> import copy
        >>> route: RouteCvrp = RouteCvrp(route[])
        >>> route_copy: RouteCvrp = copy.copy(route)
        """
        # Put all the customers in a list
        customers_route_copy: List[NodeWithCoord] = self.__customers_route[:]
        # Create a copy of the route based on the customers_route_copy created on the prvious line
        route_copy: RouteCvrp = RouteCvrp(route=customers_route_copy)
        
        return route_copy
      
    def __deepcopy__(self) -> RouteCvrp:
        """
        deepcopy
        
        Create a deepcopy of the route
        
        :return: A deepcopy of the route
        :rtype: RouteCvrp
        
        :exemple:

        >>> import copy
        >>> route: RouteCvrp = RouteCvrp(route[])
        >>> route_copy: RouteCvrp = copy.deepcopy(route)
        """
        # Copy all the customers in the route
        customers_route_copy: List[NodeWithCoord] = [copy.copy(route) for route in self.__customers_route]
        # Create a copy of the route based on the customers_route_copy created on the prvious line
        route_copy: RouteCvrp = RouteCvrp(route=customers_route_copy)
        
        return route_copy  
      
    def __len__(self) -> int:
        """
        len
        
        Method to get the length of the route (in other the number of nodes in the route)
        
        :return: The length of the route
        :rtype: int
        
        """
        # Return the len of the string
        return len(self.__customers_route)
    
    # TODO a tester    
    def __eq__(self, other: RouteCvrp) -> bool:
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
        # If the solution is the same but reversed will also return true
        return ((self[1:route_length] == other[1:route_length]).all() or
                 (self[1:route_length] == other[1:route_length].reverse()).all())
      
    @singledispatchmethod  
    def __getitem__(self, indices) -> NodeWithCoord:
        """
        """
        raise TypeError(f"The method __getitem__ is not implemented with the {type(indices)} type.")
       
    @__getitem__.register 
    def getitemImplementation(self, indices: int) -> NodeWithCoord:
        """
        """
        return self.__customers_route[indices]
        
    @__getitem__.register 
    def getitemImplementation(self, indices: slice) -> List[NodeWithCoord]:
        """
        """
        return self.__customers_route[indices]
        
    
# --------------------------------- Methods --------------------------------- #

    def evaluation(self) -> float:
        """
        evaluation()
        
        Method to get the cost of the route (not rounded)
        
        :return: The cost (the sum of all distance between the nodes of the route)
        :rtype: float
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
        isValid()
        
        Method to know whether a route is valid or not
        
        :return: True if the route is valid, False else
        :rtype: bool
        """
        
        # Test if it start at a depot and end at depot
        # For this purpose we first test that the startpoint and end point are the same
        # To do this we just ensure that the first and last node of the route is the same
        if self.__customers_route[0] != self.__customers_route[len(self.__customers_route) - 1]:
            return False

        # Test if this first and last value are realy a depot (we do that by
        # verifying that the type of the node is DepotCvrp)
        if not isinstance(self.__customers_route[0], DepotCvrp):
            return False

        # Create a counter (to count the number of every values)
        # Do this only for customers (exclude first and last values since they are 
        # depot
        counter_nodes: Dict[NodeWithCoord, int] = Counter(self.__customers_route[1:-1])
        
        # Get all non valid nodes
        # It can be either because their come multiple time or they are not
        # the right type
        non_valid_customers: List[NodeWithCoord] = [
            node for node in counter_nodes.keys()
            if counter_nodes[node]>1
            or not isinstance(node, CustomerCvrp)
       ]
        
        # To be a valid solution there's should none non valid nodes
        return len(non_valid_customers) == 0
       
    def getAllNeighboursSwap(self, solution_evaluation: float = 0) -> List[Tuple[RouteCvrp, int]]:
        """
        getAllNeighboursSwap()
        
        Method to get all customers swap possible of the route
        
        :param solution_evaluation: Evaluation of the solution (to then get the cost the whole solution), default to 0 (opt.)
        :type solution_evaluation: float
        :return: A tuple containing the routes with swaps and their evaluation
        :rtype: List[Tuple[RouteCvrp, int]]
        """
        
        # Store the depot node to then build route
        depot: DepotCvrp = self.customers_route[0]
        
        # Create a list to store all neighbours solution and their evaluation
        neighbours: List[Tuple[RouteCvrp, int]] = []
        
        # For every permutations possible of customers
        for new_routes in permutations(self.customers_route[1:-1], len(self.customers_route[1:-1])):
            # Insert the depot at the very start of the route
            new_routes.insert(0, depot)
            # Add the depot at the of the route
            new_routes.append(depot)
            
            # Create a new route
            route: RouteCvrp = RouteCvrp(route=new_routes)
            # Calcul the cost of the route
            # The objective behind that is to not have to calcul the cost for the whole
            # solution but just for the changed route and then apply this change to the
            # to determine the new cost of the solution without cacul at any time the
            # cost of the whole route of the solution. By this way we can save a
            # lot of time
            cost: int = route.evaluation() + solution_evaluation
            # Create a tuple to store the route and it's cost
            solution: Tuple[RouteCvrp, int] = (route, cost)
            # add the solution found to the route
            neighbours.append(solution)
            
        return neighbours
            
    def getNeighboursSwap(
        self, proximity_swaps: int = 1, solution_evaluation: float = 0
    ) -> List[Tuple[RouteCvrp, int]]:
        """
        getAllNeighboursSwap()
        
        Method to get a customers swap of the route. The swaps will be made
        between 2 elements of the route depending of the parameter proximity_swaps.
        For exemple if the proximity_swaps is equal to 1, the route generated
        will be a swap between an element of the route and the node that is following.
        Let's imagine we have route like (node 1 being the depot):
        [1, 2, 3, 4, 1]
        The swaps will be:
        [1, 3, 2, 4, 1]
        [1, 2, 4, 3, 1]
        [1, 4, 3, 2, 1]
        
        :param proximity_swaps: The proximity of elements swaps, default to 1 (opt.)
        :type proximity_swaps: int
        :param solution_evaluation: Evaluation of the solution (to then get the cost the whole solution), default to 0 (opt.)
        :type solution_evaluation: float
        :return: A tuple containing the routes with swaps and their evaluation (it will contain n route, with n being the number of customer in the route)
        :rtype: List[Tuple[RouteCvrp, int]]
        
        .. warning: If proximity_swaps % (len(route) - 2) == 0 then no swaps will be realized

        """
        
        # Create a list to store all neighbours solution and their evaluation
        neighbours: List[Tuple[RouteCvrp, int]] = []
        
        # 
        for customer_index in range(1, len(self.__customers_route) - 2):
            # We minus 2 because 2 nodes are exclude and we add one since the first node is the depot
            swap_index: int = ((customer_index + proximity_swaps) % (len(self.__customers_route) - 2)) + 1
            # Copy the list of route
            route_copy: List[NodeWithCoord] = self.__customers_route[:]
            # make the swap
            route_copy[customer_index], route_copy[swap_index] = self.__customers_route[swap_index], self.__customers_route[customer_index]
            
            # Create a new route
            route: RouteCvrp = RouteCvrp(route=route_copy)
            # Calcul the cost of the route
            # The objective behind that is to not have to calcul the cost for the whole
            # solution but just for the changed route and then apply this change to the
            # to determine the new cost of the solution without cacul at any time the
            # cost of the whole route of the solution. By this way we can save a
            # lot of time
            cost: int = route.evaluation() + solution_evaluation
            # Create a tuple to store the route and it's cost
            solution: Tuple[RouteCvrp, int] = (route, cost)
            # add the solution found to the route
            neighbours.append(solution)
            
        return neighbours
        
    def getNeighboursRouteSwap(
        self, other_route: RouteCvrp, proximity_swaps: float = 0, solution_evaluation: int = 0
    ) -> List[Tuple[RouteCvrp, int]]:
        """
        getNeighboursRouteSwap()
        
        Method to swap a customers between 2 routes
        
        :param proximity_swaps: The proximity of elements swaps, default to 0 (opt.)
        :type proximity_swaps: int
        :param solution_evaluation: Evaluation of the solution (to then get the cost the whole solution), default to 0 (opt.)
        :type solution_evaluation: float
        :return: A tuple containing the routes with swaps and their evaluation (it will contain n route, with n being the number of customer in the route)
        :rtype: List[Tuple[RouteCvrp, int]]
        
        .. warning: The result of route1.getNeighboursRouteSwap(other_route=route2) will be different of route2.getNeighboursRouteSwap(other_route=route1) if the number of customer is different in route1 and route2. ALWAYS prefer route1.getNeighboursRouteSwap(other_route=route2) if and only if len(route1)>=len(route2). If not less swaps will be made !
        
        :exemple:
        
        >>> if len(route1) >= len(route2):
        >>>     route1.getNeighboursRouteSwap(other_route=route2)
        >>> else:
        >>>     route2.getNeighboursRouteSwap(other_route=route1)
        """

        # Store the depot node to then build route
        depot: DepotCvrp = self.customers_route[0]
        
        # Create a list to store all neighbours solution and their evaluation
        neighbours: List[Tuple[RouteCvrp, int]] = []
        
        # 
        for customer_index in range(1, len(self.__customers_route) - 2):
            # We minus 2 because 2 nodes are exclude and we add one since the first node is the depot
            swap_index: int = ((customer_index + proximity_swaps) % (len(other.customers_route) - 2)) + 1
            
            # Copy the list of route of self
            route_copy_self: List[NodeWithCoord] = self.__customers_route[:]
            # copy the route of the other
            route_copy_other: List[NodeWithCoord] = self.__customers_route[:]
            
            # make the swap
            route_copy_self[customer_index], route_copy_other[swap_index] = route_copy_other[swap_index], route_copy_self[customer_index]
            
            # Create new route
            # new route made from self after the swap
            route_1: RouteCvrp = RouteCvrp(route=route_copy_self)
            # new route made from other after the swap
            route_2: RouteCvrp = RouteCvrp(route=route_copy_other)
            # Calcul the cost of the route
            # The objective behind that is to not have to calcul the cost for the whole
            # solution but just for the changed route and then apply this change to the
            # to determine the new cost of the solution without cacul at any time the
            # cost of the whole route of the solution. By this way we can save a
            # lot of time
            cost_1: int = route_1.evaluation()
            cost_2: int = route_2.evaluation()
            # Create a tuple to store the route and it's cost
            solution: Tuple[RouteCvrp, RouteCvrp, int] = (route_1, route_2, cost_1+cost_2+solution_evaluation)
            # add the solution found to the route
            neighbours.append(solution)
            
        return neighbours

# ----------------------------- Getter / Setter ----------------------------- #

    @property 
    def customers_route(self) -> List[NodeWithCoord]:
        return self.__customers_route
        
    @customers_route.setter
    def customers_route(self, value: List[NodeWithCoord]) -> None:
        self.__customers_route = value
