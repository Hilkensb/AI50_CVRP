#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
import abc

# Other Library
import numpy as np
import networkx as nx


class VehiculeRootingProblem(abc.ABC):
    """
    """

    @abc.abstractclassmethod
    def distanceMatrix(self) -> np.matrix:   
        """
        """
        pass
        
    @abc.abstractclassmethod
    def graph(self) -> nx.Graph:
        """
        """
        pass
        
    @abc.abstractclassmethod
    def readInstanceVrp(self, file_path: str) -> VehiculeRootingProblem:
        """
        """
        pass

    @abc.abstractclassmethod
    def writeInstanceVrp(self, file_path: str) -> None:  
        """
        """
        pass
        
    @abc.abstractclassmethod
    def randomInstance(self, nb_customer: int = 30, nb_vehicule: int = 5, vehicule_capacity: int = 100, customer_demand_lb: int = 1, customer_demand_ub: int = 20, grid_size: int = 100) -> VehiculeRootingProblem:  
        """
        """
        pass
        
    @abc.abstractclassmethod
    def min_vehicule_number(self) -> int:
        """
        """ 
        pass

