#!/usr/bin/env python3
import numpy as np
from functools import singledispatch
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import NodeWithCoord

# ---------------------------- Euclidean Distance --------------------------- #

@singledispatch
def euclideanDistance(a, b) -> float:
    """
    """

    raise TypeError(f"The function euclideanDistance is not implemented with the {type(a)} type.")

@euclideanDistance.register
def euclideanDistanceImplementation(a: tuple, b: tuple) -> float:
    """
    """

    # Calcul the euclidean distance
    dist = np.linalg.norm(a - b)

    return dist

@euclideanDistance.register
def euclideanDistanceImplementation(a: NodeWithCoord, b: NodeWithCoord) -> float:
    """
    """

    # Create the vectors of coodinates
    # Create the vector 1 from the coordinates of node a
    vector_1 = np.array(a.getCoordinates())
    # Create the vector 2 from the coordinates of node b
    vector_2 = np.array(b.getCoordinates())
    # Calcul the euclidean distance
    dist = np.linalg.norm(vector_1 - vector_2)

    return dist

# --------------------------- Linear Interpolation -------------------------- #
  
@singledispatch
def linearInterpolation(min_value, max_value, value) -> float:
    """
    """
    raise TypeError(f"The function linearInterpolation is not implemented with the {type(a)} type.")

@linearInterpolation.register
def linearInterpolationImplementation(min_value: int, max_value: int, value: int) -> float:
    """        
    """
    # Put everything in float to return a float (if not it will return either 0 or 1)
    return (1.0/(float(max_value) - float(min_value))) * (float(value) - float(min_value))

@linearInterpolation.register
def linearInterpolationImplementation(min_value: float, max_value: float, value: float) -> float:
    """
    """
    # Since everything is already floats, no need to cast them
    return (1.0/(max_value - min_value)) * (value - min_value)

