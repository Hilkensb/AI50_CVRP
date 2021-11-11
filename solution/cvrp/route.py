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
# Library to create the graph plot
import matplotlib.pyplot as plt
# To display plotly grah
import plotly.graph_objects as go

# Modules
from problem.node import NodeWithCoord
import utils.mathfunctions as mathfunc
from problem.cvrp.depot import DepotCvrp
from problem.cvrp.customer import CustomerCvrp
from utils.colorpallette import DEFAULT_COLOR_PALETTE


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
        return ((self.__customers_route[1:-1] == other.__customers_route[1:-1]) or
                 (self.__customers_route[1:-1] == other.__customers_route[1:-1:-1]))
      
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
    
    def __dict__(self):
        """
        dict()
        
        Create the dictionnary of the object
        
        :return: The dictionnary with al values of the object
        :rtype: dict
        """  
        
        # Create the dictionnary
        object_dict: Dict = {}
        
        # Set every variable of it
        # Convert every customer into dictionnary before putting them inside
        # the dictionnary of the route
        # it will then be easier to generate the json string
        object_dict["customers_route"] = [customer.__dict__() for customer in self.__customers_route]
        
        return object_dict  
    
    def __hash__(self):
        """
        """
        return hash(self.__str__)
    
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
       
    # TODO   
    def getAllNeighboursSwap(
        self, solution_evaluation: float = 0
    ) -> List[Tuple[RouteCvrp, int]]:
        """
        getAllNeighboursSwap()
        
        Method to get all customers swap possible of the route
        
        :param solution_evaluation: Evaluation of the solution (to then get the cost the whole solution), default to 0 (opt.)
        :type solution_evaluation: float
        :return: A tuple containing the routes with swaps and their evaluation
        :rtype: List[Tuple[RouteCvrp, int]]
        
        .. warning: For a large number of node, take a long time to run. Too many neighbours to consider.
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
        self, proximity_swaps: int = 1, solution_evaluation: float = 0,
        route_cost: float = None
    ) -> List[Tuple[RouteCvrp, int, str]]:
        """
        getNeighboursSwap()
        
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
        :param route_cost: Cost the route, default to None (opt.)
        :type route_cost: float
        :return: A tuple containing the routes with swaps, their evaluation (it will contain n route, with n being the number of customer in the route) and the string representing the swap realized
        :rtype: List[Tuple[RouteCvrp, int, str]]
        
        .. warning: If proximity_swaps % (len(route) - 2) == 0 then no swaps will be realized
        """  
        # If the route has less than 9 route (10 node or 8  customer) 
        # considered as short
        if len(self.__customers_route) < 10:
            return self.__getNeighboursSwapShort(
                proximity_swaps=proximity_swaps,
                solution_evaluation=solution_evaluation
            )
        else:
            return self.__getNeighboursSwapLong(
                proximity_swaps=proximity_swaps,
                solution_evaluation=solution_evaluation,
                route_cost=route_cost
            )
      
    def __getNeighboursSwapLong(
        self, proximity_swaps: int = 1, solution_evaluation: float = 0,
        route_cost: float = None
    ) -> List[Tuple[RouteCvrp, int, str]]:
        """
        getNeighboursSwapLong()
        
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
        :param route_cost: Cost the route, default to None (opt.)
        :type route_cost: float
        :return: A tuple containing the routes with swaps, their evaluation (it will contain n route, with n being the number of customer in the route) and the string representing the swap realized
        :rtype: List[Tuple[RouteCvrp, int, str]]
        
        .. warning: If proximity_swaps % (len(route) - 2) == 0 then no swaps will be realized

        """
        
        # Create a list to store all neighbours solution and their evaluation
        neighbours: List[Tuple[RouteCvrp, int, str]] = []
        
        # Get the cost of the route
        # If the cost was not passed to the method
        if route_cost is None:
            # Calcul the cost
            self_cost: float = self.evaluation()
        else:
            # If the cost was passed to the method use it
            self_cost = route_cost
        
        # 
        for customer_index in range(1, len(self.__customers_route) - 2):
            # We minus 2 because 2 nodes are exclude and we add one since the first node is the depot
            swap_index: int = ((customer_index + proximity_swaps) % (len(self.__customers_route) - 2)) + 1
            # Copy the list of route
            route_copy: List[NodeWithCoord] = self.__customers_route[:]
            
            # Calcul the cost of the removed route
            # By this way we only have 8 distance to calcul 
            # That's why this method is only for route that have 10 node or mode
            # in other word where 9 or more distance is needed to calcul the cost of
            # route
            cost_previous_swap1: float = sum(
                [mathfunc.euclideanDistance(node_pair[0], node_pair[1])
                for node_pair in pairwise(self.__customers_route[swap_index - 1:swap_index + 2])]
            )
            # Calcul the cost of the removed route
            cost_previous_swap2: float = sum(
                [mathfunc.euclideanDistance(node_pair[0], node_pair[1])
                for node_pair in pairwise(self.__customers_route[customer_index - 1:customer_index + 2])]
            )
            
            # make the swap
            route_copy[customer_index], route_copy[swap_index] = self.__customers_route[swap_index], self.__customers_route[customer_index]
            
            # Calcul the cost of the new route
            cost_insert_swap1: float = sum(
                [mathfunc.euclideanDistance(node_pair[0], node_pair[1])
                for node_pair in pairwise(route_copy[swap_index - 1:swap_index + 2])]
            )
            # Calcul the cost of the new route
            cost_insert_swap2: float = sum(
                [mathfunc.euclideanDistance(node_pair[0], node_pair[1])
                for node_pair in pairwise(route_copy[customer_index - 1:customer_index + 2])]
            )
            
            # Create a new route
            route: RouteCvrp = RouteCvrp(route=route_copy)
            # Calcul the cost of the route
            # The objective behind that is to not have to calcul the cost for the whole
            # solution but just for the changed route and then apply this change to the
            # to determine the new cost of the solution without cacul at any time the
            # cost of the whole route of the solution. By this way we can save a
            # lot of time
            cost_route: float = self_cost - cost_previous_swap1 - cost_previous_swap2 + cost_insert_swap1 + cost_insert_swap2
            cost: int = cost_route + solution_evaluation
            # Create a string to represent the swap realized
            swap_realized: str = f"{route_copy[customer_index].node_id}-{route_copy[swap_index].node_id}"
            # Create a tuple to store the route and it's cost
            solution: Tuple[RouteCvrp, int, str] = (route, cost, swap_realized)
            # add the solution found to the route
            neighbours.append(solution)
            
        return neighbours  
      
    def __getNeighboursSwapShort(
        self, proximity_swaps: int = 1, solution_evaluation: float = 0
    ) -> List[Tuple[RouteCvrp, int, str]]:
        """
        getNeighboursSwapShort()
        
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
        :return: A tuple containing the routes with swaps, their evaluation (it will contain n route, with n being the number of customer in the route) and the string representing the swap realized
        :rtype: List[Tuple[RouteCvrp, int, str]]
        
        .. warning: If proximity_swaps % (len(route) - 2) == 0 then no swaps will be realized

        """
        
        # Create a list to store all neighbours solution and their evaluation
        neighbours: List[Tuple[RouteCvrp, int, str]] = []
        
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
            # Create a string to represent the swap realized
            swap_realized: str = f"{route_copy[customer_index].node_id}-{route_copy[swap_index].node_id}"
            # Create a tuple to store the route and it's cost
            solution: Tuple[RouteCvrp, int, str] = (route, cost, swap_realized)
            # add the solution found to the route
            neighbours.append(solution)
            
        return neighbours
      
    # TODO remove cost eval 
    def getNeighboursRouteSwap(
        self, other_route: RouteCvrp, vehicule_capacity: int,
        proximity_swaps: float = 0, solution_evaluation: int = 0
    ) -> List[Tuple[RouteCvrp, RouteCvrp, int, str]]:
        """
        getNeighboursRouteSwap()
        
        Method to swap a customers between 2 routes
        
        :param proximity_swaps: The proximity of elements swaps, default to 0 (opt.)
        :type proximity_swaps: int
        :param vehicule_capacity: The capacity of the vehicule in the cvrp instance
        :type vehicule_capacity: int
        :param solution_evaluation: Evaluation of the solution (to then get the cost the whole solution), default to 0 (opt.)
        :type solution_evaluation: float
        :return: A tuple containing the routes with swaps and their evaluation (it will contain n route, with n being the number of customer in the route) and the string representing the swap realized
        :rtype: List[Tuple[RouteCvrp, int, str]]
        
        .. warning: The result of route1.getNeighboursRouteSwap(other_route=route2) will be different of route2.getNeighboursRouteSwap(other_route=route1) if the number of customer is different in route1 and route2. ALWAYS prefer route1.getNeighboursRouteSwap(other_route=route2) if and only if len(route1)>=len(route2). If not less swaps will be made !
        
        :exemple:
        
        >>> if len(route1) >= len(route2):
        >>>     route1.getNeighboursRouteSwap(other_route=route2)
        >>> else:
        >>>     route2.getNeighboursRouteSwap(other_route=route1)
        """

        # Store the depot node to then build route
        depot: DepotCvrp = self.customers_route[0]
        
        # Demand supplied by each route
        self_supplied: int = self.demandSupplied() - vehicule_capacity
        other_supplied: int = other_route.demandSupplied() - vehicule_capacity
        
        # Create a list to store all neighbours solution and their evaluation
        neighbours: List[Tuple[RouteCvrp, int, str]] = []
        
        # For each customer except the first and last node (depot)
        for customer_index in range(1, len(self.__customers_route) - 2):
            # We minus 2 because 2 nodes are exclude and we add one since the first node is the depot
            swap_index: int = ((customer_index + proximity_swaps) % (len(other_route.customers_route) - 2)) + 1
            
            # Copy the list of route of self
            route_copy_self: List[NodeWithCoord] = self.__customers_route[:]
            # copy the route of the other
            route_copy_other: List[NodeWithCoord] = other_route.__customers_route[:]
                        
            # Verify the capacity constraints
            new_self_supplied: int = self_supplied - route_copy_self[customer_index].demand + route_copy_other[swap_index].demand
            new_other_supplied: int = other_supplied - route_copy_other[swap_index].demand + route_copy_self[customer_index].demand
            # If lower than zero at least one route does not respect the capacity constraints
            if (new_self_supplied > 0 or new_other_supplied > 0):
                continue
            
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
            # Create a string to represent the swap realized
            swap_realized: str = f"{route_copy_self[customer_index].node_id}-{route_copy_other[swap_index].node_id}"
            # Create a tuple to store the route and it's cost
            solution: Tuple[RouteCvrp, RouteCvrp, int, str] = (route_1, route_2, cost_1+cost_2+solution_evaluation, swap_realized)
            # add the solution found to the route
            neighbours.append(solution)
            
        return neighbours
        
    def getNeighboursRouteInsertion(
        self, other_route: RouteCvrp, vehicule_capacity: int,
        proximity_swaps: float = 0, solution_evaluation: int = 0,
        self_route_cost: float = None, other_route_cost: float = None
    ) -> List[Tuple[RouteCvrp, RouteCvrp, int, str]]:
        """
        getNeighboursRouteInsertion()
        
        Method to swap a customers between 2 routes
        
        :param proximity_swaps: The proximity of elements swaps, default to 0 (opt.)
        :type proximity_swaps: int
        :param vehicule_capacity: The capacity of the vehicule in the cvrp instance
        :type vehicule_capacity: int
        :param solution_evaluation: Evaluation of the solution (to then get the cost the whole solution), default to 0 (opt.)
        :type solution_evaluation: float
        :param self_route_cost: cost of this route, default to None (opt.)
        :type self_route_cost: float
        :param other_route_cost: cost of the other route given in argument, default to None (opt.)
        :type other_route_cost: float
        :return: A tuple containing the routes with swaps and their evaluation (it will contain n route, with n being the number of customer in the route) and the string representing the swap realized
        :rtype: List[Tuple[RouteCvrp, int, str]]
        
        .. warning: The result of route1.getNeighboursRouteSwap(other_route=route2) will be different of route2.getNeighboursRouteSwap(other_route=route1) if the number of customer is different in route1 and route2. ALWAYS prefer route1.getNeighboursRouteSwap(other_route=route2) if and only if len(route1)>=len(route2). If not less swaps will be made !
        
        :exemple:
        
        >>> if len(route1) >= len(route2):
        >>>     route1.getNeighboursRouteSwap(other_route=route2)
        >>> else:
        >>>     route2.getNeighboursRouteSwap(other_route=route1)
        """

        # Store the depot node to then build route
        depot: DepotCvrp = self.customers_route[0]
        
        # Demand supplied by each route
        max_demand: int = vehicule_capacity - self.demandSupplied()
        
        # Create a list to store all neighbours solution and their evaluation
        neighbours: List[Tuple[RouteCvrp, int, str]] = []
        
        
        # Get the cost of the route
        # If the cost was not passed to the method
        if self_route_cost is None:
            # Calcul the cost
            self_route_cost: float = self.evaluation()
        
        # If the cost was not passed to the method
        if other_route_cost is None:
            # Calcul the cost
            other_route_cost: float = other_route.evaluation()
        
        # For each customer of the other route except the first and last node (depot)
        for index_other_customer, other_customer in enumerate(other_route.customers_route[1:-1]):
            # Check if the demand is too hight to be inserted
            if other_customer.demand > max_demand:
                # Skip this iteration
                continue
            
            # We minus 2 because 2 nodes are exclude and we add one since the first node is the depot
            insert_index: int = ((proximity_swaps) % (len(self.customers_route) - 2)) + 1
            
            # Copy the route
            # Insert the customer in his new route
            # To do so put the at the start of a new list the list from start
            # to the index we want to add the element
            instert_route_copy: List[CustomerCvrp] = [
                *self.customers_route[:insert_index],
                other_customer, *self.customers_route[insert_index:]
            ]
            # Remove the customer from his previous route
            remove_route_copy: List[CustomerCvrp] = [
                *other_route.customers_route[:index_other_customer + 1],
                *other_route.customers_route[index_other_customer + 2:]
            ]
            
            # Cost of insert node
            # To calcul the cost of the insertion, we look at the distance
            # between the node inserted and his 2 neighbours minus the distance
            # between the two neighbours of the inserted node
            insertion_cost: float = (sum(
                [mathfunc.euclideanDistance(node_pair[0], node_pair[1])
                for node_pair in pairwise(instert_route_copy[insert_index - 1:insert_index + 2])]
            ) - mathfunc.euclideanDistance(
                instert_route_copy[insert_index - 1],
                instert_route_copy[insert_index + 1])
            )
            # Removed cost node
            remove_cost: float = (sum(
                [mathfunc.euclideanDistance(node_pair[0], node_pair[1])
                for node_pair in pairwise(other_route.customers_route[index_other_customer:index_other_customer + 3])]
            ) - mathfunc.euclideanDistance(
                other_route.customers_route[index_other_customer],
                other_route.customers_route[index_other_customer + 2])
            )
            
            # Create new route
            # new route made after insertion
            insert_route: RouteCvrp = RouteCvrp(route=instert_route_copy)
            remove_route: RouteCvrp = RouteCvrp(route=remove_route_copy)
            
            # Calcul the cost of the route
            # The objective behind that is to not have to calcul the cost for the whole
            # solution but just for the changed route and then apply this change to the
            # to determine the new cost of the solution without cacul at any time the
            # cost of the whole route of the solution. By this way we can save a
            # lot of time
            cost_instert: int = self_route_cost + insertion_cost
            cost_remove: int = other_route_cost - remove_cost
            
            # Create a string to represent the swap realized
            swap_realized: str = f"{other_customer.node_id}"
            # Create a tuple to store the route and it's cost
            solution: Tuple[RouteCvrp, RouteCvrp, int, str] = (insert_route, remove_route, cost_instert+cost_remove+solution_evaluation, swap_realized)
            # add the solution found to the route
            neighbours.append(solution)
            
        return neighbours

    def demandSupplied(self) -> int:
        """
        demandSupplied()
        
        The sum of demand of all customers in the route
        
        :return: The total demand supplied by this route
        :rtype: int
        """
        # List of demand in the route
        demand_list: List[int] = [customer.demand for customer in self.__customers_route]
        
        return sum(demand_list)

# _____________________________ Extract Methods _____________________________ #

    def toJSON(self) -> str:
        """
        toJSON()
        
        Method to get the JSON value of the class
        """
    
        return json.dumps(self.__dict__())
        
    def fromJSON(self, json: dict) -> None:
        """
        fromJSON()
        
        Method to transform a JSON into an object
        
        :param json: Json data of the object
        :type json: dict
        :raises: KeyValueError if the json is incomplete
        """
    
        # Create a list of customers
        customers_list: List[CustomerCvrp] = []
        # Iterate throw every customers of the route
        # Excludes the first and last node that should be depot node
        # So it has to be another object, so another constructor
        for customer_dict in json["customers_route"][1:-1]:
            # Create a new customer
            customer: CustomerCvrp = CustomerCvrp(node_id=0, x=0, y=0, demand=0)
            # Read the json of the customer and update the customer
            # with information stored inside
            customer.fromJSON(json=customer_dict)
            # Add the customer to the list
            customers_list.append(customer)
        
        # Since every route should start and end at the depot they should be
        # of type DpotCvrp
        # We could have made only one object and put it at the start and end
        # But for the safety we will prefer create 2 objects
        # Even if the two object should be the same (at least if the json
        # is correct)
        start_depot: DepotCvrp = DepotCvrp(node_id=0, x=0, y=0)
        end_depot: DepotCvrp = DepotCvrp(node_id=0, x=0, y=0)
        # Read the json to update the objects
        start_depot.fromJSON(json=json["customers_route"][0])
        end_depot.fromJSON(json=json["customers_route"][-1])
        
        # Create the route with all nodes build before
        self.__customers_route = [start_depot, *customers_list, end_depot]

# _____________________________ Display Methods _____________________________ #

    def drawPlotly(
        self, depot_node_color: str = "#a6f68e", node_size: int = 15, 
        route_color: str = DEFAULT_COLOR_PALETTE[0], show_legend_edge: bool = True,
        show_legend_node: bool = False, route_number: int = -1
    ) -> Tuple(List[Scatter], List[Scatter]):
        """
        drawPlotly()
        
        Method to create the scatter that compose the graph made with plotly
        
        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :type route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param node_size: Size of the nodes, default to 15 (opt)
        :type node_size: int
        :param show_legend_edge: Display or not the legend of edges, default to True (opt.)
        :type show_legend_edge: bool
        :param show_legend_node: Display or not the legend of nodes, default to False (opt.)
        :type show_legend_edge: bool
        :param route_number: Number of the route drawn
        :type route_number: int
        :return: Two lists of scatters, one of nodes and one of edges
        :rtype: Tuple(List[Scatter], List[Scatter])
        """
        
        # Get the depot node 
        depot_node = self.__customers_route[0]
        
        # List of scatter plot 
        # List of the nodes
        node_scatter_dict: Dict[int, Scatter] = {}
        
        # List of edges
        edge_x = []
        edge_y = []
        # List of nodes
        node_x = []
        node_y = []
        # Text when hovered
        node_text: List[str] = []
        
        x1, y1 = depot_node.getCoordinates()
        # For every customer in the solution (excluding the depot, so excluding the first and last node of the route)
        for customer in self.__customers_route[1:-1]:
            # Get the x and y position of the departure of the route
            x0, y0 = x1, y1
            # Get the x and y position of the arrival of the route
            x1, y1 = customer.getCoordinates()
            
            # Set the positions of the ege
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
            
            # Set the node
            # Set is position
            node_x = [x1]
            node_y = [y1]
            # Set his name
            node_text = [f"{customer.node_id}"]
  
            # Node of the trace
            node_trace: Scatter = go.Scatter(
                x=node_x, y=node_y,
                showlegend=show_legend_node,
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    color=route_color,
                    size=node_size,
                    line_width=0.5
                ),
                name=f"Customers in route #{route_number + 1}",
                text=node_text
            )
            # Add the node scatter 
            # Garrentee that each node will be in the same oreder
            node_scatter_dict[customer.node_id - 1] = node_trace

        # Set the returning edge to the depot
        # Get the x and y position of last customer
        x0, y0 = x1, y1
        # Get the x and y position of the depot
        x1, y1 = depot_node.getCoordinates()
        # Set the positions of the ege
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

        # Edge of the trace
        edge_trace: Scatter = go.Scatter(
            x=edge_x, y=edge_y,
            showlegend=show_legend_edge,
            line=dict(width=0.5, color=route_color),
            hoverinfo='none',
            mode='lines',
            name=f"Route #{route_number + 1}"
        )

        return node_scatter_dict, edge_trace
        
    def updateDrawPlotly(
        self, depot_node_color: str = "#a6f68e", node_size: int = 15, 
        route_color: str = DEFAULT_COLOR_PALETTE[0], show_legend_edge: bool = True,
        show_legend_node: bool = False, route_number: int = -1,
        node_scatter_parent: List[go.Scatter] = [],
        edge_scatter_parent: List[go.Scatter] = []
    ) -> None:
        """
        updateDrawPlotly()
        

        Method to create the scatter that compose the graph made with plotly
        
        :param route_color: List of colors of the routes in the solution, default the DEFAULT_COLOR_PALETTE (utils.colorpallete) (opt.)
        :type route_color: List[str]
        :param depot_node_color: Color of the node depot, default to \"#a6f68e\" (opt.)
        :type depot_node_color: str
        :param node_size: Size of the nodes, default to 15 (opt)
        :type node_size: int
        :param show_legend_edge: Display or not the legend of edges, default to True (opt.)
        :type show_legend_edge: bool
        :param show_legend_node: Display or not the legend of nodes, default to False (opt.)
        :type show_legend_edge: bool
        :param route_number: Number of the route drawn
        :type route_number: int
        :param node_scatter_parent: List of node scatter of the main figure animation
        :type node_scatter_parent: List[go.Scatter]
        :param edge_scatter_parent: List of edge scatter of the main figure animation
        :type edge_scatter_parent: List[go.Scatter]
        """
        
        # List of customers x positions
        x_position_list: List[int] = [customer.x for customer in self.__customers_route]
        # List of customers y positions
        y_position_list: List[int] = [customer.y for customer in self.__customers_route]
        
        # List of edges
        # Initialize the x position of edges
        edge_x: List[int] = [None] * ((len(self.__customers_route) - 1) * 3)
        # List of x position for the start of the edge
        edge_x[::3] = x_position_list[:-1]
        # List of x position for the end of the edge
        edge_x[1::3] = x_position_list[1:]
        # Initialize the y position of edges
        edge_y: List[int] = [None] * ((len(self.__customers_route) - 1) * 3)
        # List of y position for the start of the edge
        edge_y[::3] = y_position_list[:-1]
        # List of y position for the end of the edge
        edge_y[1::3] = y_position_list[1:]
        
        # Customer node group name 
        customer_group_name: str = f"Customers in route #{route_number + 1}"

        # For every customer in the solution (excluding the depot, so excluding the first and last node of the route)
        for customer in self.__customers_route[1:-1]:
            
            # Add the node scatter 
            # Garrentee that each node will be in the same oreder
            node_scatter_copy = copy.copy(node_scatter_parent[customer.node_id - 1])
            # Update the group name of the node
            node_scatter_copy.name = customer_group_name
            # Update the color of the node
            node_scatter_copy.marker["color"] = route_color
            # Update the node on the figure
            node_scatter_parent[customer.node_id - 1] = node_scatter_copy

        # update the edge of the route
        # First create a copy of the edge scatter
        edge_scatter_copy = copy.copy(edge_scatter_parent[route_number])
        # Set the x position of edge
        edge_scatter_copy.x = edge_x
        # Set the y position of edge
        edge_scatter_copy.y = edge_y
        # update the edge scatter
        edge_scatter_parent[route_number] = edge_scatter_copy
        
# ----------------------------- Getter / Setter ----------------------------- #

    @property 
    def customers_route(self) -> List[NodeWithCoord]:
        return self.__customers_route
        
    @customers_route.setter
    def customers_route(self, value: List[NodeWithCoord]) -> None:
        self.__customers_route = value

