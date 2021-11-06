#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import Tuple
import json

# Modules
from problem.node import NodeWithCoord


class CustomerCvrp(NodeWithCoord):
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #

    def __init__(self, node_id: int, x: int, y: int, demand: int) -> CustomerCvrp:
        """
        Constructor of the CustomerCvrp
        
        :param node_id: The id of the node in th graph
        :type node_id: int
        :param x: x coordinates of the node
        :type x: int
        :param y: y coordinates of the node
        :type y: int
        :param demand: Demand of the node
        :type demand: int
        """
        
        # Set the customers attribute
        self.__node_id: int = node_id
        self.__x : int = x
        self.__y : int = y
        self.__demand : int = demand

    def __str__(self) -> str:
        """
        string
        
        Method to get the string of the Customer
        
        :return: The node id with it's position
        :rtype: str

        """
        return f"Node id: {self.node_id} ({self.x}, {self.y})"
                 
    def __repr__(self) -> str:
        """
        representation
        
        Method to get the representation of the Customer
        
        :return: The node id
        :rtype: str
        """
        return str(self.node_id)
        
    def __copy__(self) -> CustomerCvrp:
        """
        copy
        
        Create a copy of the customer
        
        :return: A copy of the customer
        :rtype: CustomerCvrp
        
        :exemple:

        >>> import copy
        >>> customer_copy = copy.copy(customer)
        """
        return CustomerCvrp(node_id=self.__node_id, x=self.__x, y=self.__y, demand=self.__demand)
        
    def __eq__(self, other: CustomerCvrp) -> bool:
        """
        equality
        
        Method to enable to test if 2 customers are the same
        
        :return: True if the customers are the same, False else
        :rtype: bool
        """
        return self.node_id == other.node_id
        
    def __hash__(self):
        """
        """
        return hash((self.__node_id, self.__x, self.__y, self.__demand))

    def __dict__(self):
        """
        dict
        
        Create the dictionnary of the object
        
        :return: The dictionnary with al values of the object
        :rtype: dict
        """
        
        # Create the dictionnary
        object_dict: Dict = {}
        
        # Set every variable of it
        object_dict["id"] = self.__node_id
        object_dict["x"] = self.__x
        object_dict["y"] = self.__y
        object_dict["demand"] = int(self.__demand)
        
        return object_dict

# --------------------------------- Methods --------------------------------- #

    def getCoordinates(self) -> Tuple[int, int]:
        """
        getCoordinates()
        
        Method to get the coordinates (the x and y position of the node)
        
        :return: A tuple of int representing the x and y position of the customer node
        :rtype: Tuple[int, int]
        """
        return self.x, self.y
     
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
    
        # Set every variable of it
        self.__node_id = json["id"]
        self.__x = json["x"]
        self.__y = json["y"]
        self.__demand = json["demand"]
     
# ----------------------------- Getter / Setter ----------------------------- #
   
    @property 
    def node_id(self) -> int:
        return self.__node_id

    @property 
    def x(self) -> int:
        return self.__x
        
    @x.setter
    def x(self, value: int) -> None:  
        self.__x = value
        
    @property 
    def y(self) -> int:
        return self.__y
        
    @y.setter
    def y(self, value: int) -> None:  
        self.__y = value
        
    @property 
    def demand(self) -> int:
        return self.__demand
        
    @demand.setter
    def demand(self, value: int) -> None:
        self.__demand = value

