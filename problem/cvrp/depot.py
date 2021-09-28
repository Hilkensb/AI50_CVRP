#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import Tuple

# Modules
from problem.node import nodeWithCoord


class DepotCvrp(nodeWithCoord):
    """
    """

# ---------------------------- Overrided Methods ---------------------------- #

    def __init__(self, node_id: int, x: int, y: int):
        """
        Constructor of the CustomerCvrp
        """
        
        # Set the customers attribute
        self.__node_id: int = node_id
        self.__x : int = x
        self.__y : int = y
        self.__demand: int = 0
     
    def __str__(self) -> str:
        """
        """
        return f"Node id: {self.node_id} ({self.x}, {self.y})"
                 
    def __repr__(self) -> str:
        """
        """
        return str(self.node_id)
        
    def __copy__(self) -> DepotCvrp:
        """
        """
        return DepotCvrp(node_id=self.__node_id, x=self.__x, y=self.__y)

# --------------------------------- Methods --------------------------------- #

    def getCoordinates(self) -> Tuple[int, int]:
        return self.x, self.y
     
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


