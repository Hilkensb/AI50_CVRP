#!/usr/bin/env python3
import numpy as np
from functools import singledispatch
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import nodeWithCoord


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
def euclideanDistanceImplementation(a: nodeWithCoord, b: nodeWithCoord) -> float:
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
