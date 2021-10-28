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
    euclideanDistance()
    
    Function to get the distance between 2 points
    
    :param a: First point
    :param b: Second point
    :return: The distance between those 2 points
    :rtype: float
    """

    raise TypeError(f"The function euclideanDistance is not implemented with the {type(a)} type.")

# Implementations of the function
@euclideanDistance.register
def euclideanDistanceImplementation(a: tuple, b: tuple) -> float:
    """
    euclideanDistance()
    
    Function to get the distance between 2 points
    
    :param a: First point
    :type a: tuple
    :param b: Second point
    :type b: tuple
    :return: The distance between those 2 points
    :rtype: float
    """

    # Calcul the euclidean distance
    dist = np.linalg.norm(a - b)

    return dist

@euclideanDistance.register
def euclideanDistanceImplementation(a: NodeWithCoord, b: NodeWithCoord) -> float:
    """
    euclideanDistance()
    
    Function to get the distance between 2 points
    
    :param a: First point
    :type a: NodeWithCoord
    :param b: Second point
    :type b: NodeWithCoord
    :return: The distance between those 2 points
    :rtype: float
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
    linearInterpolation()
    
    Function to put a value between 0 and 1 given a max value, min value, and the value to situated
    
    :param min_value: minimum value of the list
    :param max_value: maximum value of the list
    :param value: value to place
    :return: A value between 0 and 1
    :rtype: float
    """
    raise TypeError(f"The function linearInterpolation is not implemented with the {type(a)} type.")

# Implementations of the function
@linearInterpolation.register
def linearInterpolationImplementation(min_value: int, max_value: int, value: int) -> float:
    """   
    linearInterpolation()
    
    Function to put a value between 0 and 1 given a max value, min value, and the value to situated
    
    :param min_value: minimum value of the list
    :type min_value: int
    :param max_value: maximum value of the list
    :type max_value: int
    :param value: value to place
    :type value: int
    :return: A value between 0 and 1
    :rtype: float     
    """
    # Put everything in float to return a float (if not it will return either 0 or 1)
    return (1.0/(float(max_value) - float(min_value))) * (float(value) - float(min_value))

@linearInterpolation.register
def linearInterpolationImplementation(min_value: float, max_value: float, value: float) -> float:
    """
    linearInterpolation()
    
    Function to put a value between 0 and 1 given a max value, min value, and the value to situated
    
    :param min_value: minimum value of the list
    :type min_value: float
    :param max_value: maximum value of the list
    :type max_value: float
    :param value: value to place
    :type value: float
    :return: A value between 0 and 1
    :rtype: float
    """
    # Since everything is already floats, no need to cast them
    return (1.0/(max_value - min_value)) * (value - min_value)

