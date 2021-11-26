#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
import sys
import copy
import random
from typing import List, Dict, Tuple, Union
import math

# Other Library
import numpy

# Modules
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from solution.cvrp.solution import RouteCvrp
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import NodeWithCoord


def clusteringSolver(cvrp: Cvrp, iteration: int = 75) -> Tuple[List[SolutionCvrp], List[float]]:
    """
    clusteringSolver()
    
    Function to solve the cvrp by designing cluster and building route around it
    
    :param cvrp: The cvrp instance to find a solution
    :type cvrp: Cvrp
    :param iteration: Number of iteration to run
    :type iteration: int
    :return: Solution found and the evaluation
    :rtype: Tuple[List[SolutionCvrp], List[float]]
    """
    
    # Create a first cluster center
    cluster_center, customer_assignment = kMeanCapacited(cvrp=cvrp)
    
    # Initilize the iteration number
    iteration_number: int = 1
    
    while iteration_number < iteration:
        # Memorize the previous cluster center
        previous_cluster_center: List[Tuple[float, float]] = cluster_center
        # Compute the new cluster center
        cluster_center, customer_assignment = kMeanCapacited(cvrp=cvrp, cluster_center=cluster_center)
        
        # If there's no change stop the algorithm
        if cluster_center == previous_cluster_center:
            break
         
    builded_route: List[RouteCvrp] = []   
    # Build the route with the customer assignment to cluster
    for customer_cluster in customer_assignment:
        # Build route wih the assignment in the cluster
        route_list: List[NodeWithCoord] = buildClusterRoute(
            cluster_customer=customer_cluster, depot=cvrp.depot
        )
        # Build the route cvrp
        new_route: RouteCvrp = RouteCvrp(route=route_list)
        # Add it to the list of route
        builded_route.append(new_route)
        
    # Build the solution
    solution_found: SolutionCvrp = SolutionCvrp(instance=cvrp, route=builded_route)
    
    return [solution_found], [solution_found.evaluation()]
    
    
def buildClusterRoute(cluster_customer: List[Customer], depot: DepotCvrp) -> List[NodeWithCoord]:
    """
    buildClusterRoute()
    
    Method to build route from the cluster
    
    :param cluster_customer: Customer in the cluster
    :type cluster_customer: List[Customer]
    :param depot: Depot of the cvrp instance
    :type depot: DepotCvrp
    :return: List of NodeWithCoord ordered representing the route
    :rtype: List[NodeWithCoord]
    """
    
    # Build a list that will represent the route
    route_list: List[NodeWithCoord] = [depot, depot]
    
    # for every customer in the cluster
    for customer in cluster_customer:
        # Search for the best place to insert
        best_place: int = findBestPlace(customer=customer, route=route_list)
        # Insert it at the place found
        route_list.insert(best_place + 1, customer)
        
    return route_list
    
def findBestPlace(customer: CustomerCvrp, route: List[NodeWithCoord]) -> float:
    """
    findBestPlace()
    
    Method to find the best place to insert a customer in the route
    
    :param customer: Customer to insert in the route
    :type customer: CustomerCvrp
    :param route: Route to insert customer
    :type route:  List[NodeWithCoord]
    :return: The best place to insert the customer
    :rtype: int
    """
    
    # Place where the insertion cost is minimized
    best_place: int = 0
    # Cost of the insertion at the place choose
    best_place_cost: float = sys.maxsize
    
    # For each place in the route
    for place in range(len(route) - 1):
        # Compute teh insertion cost
        cost: int = costInsertion(customer=customer, route=route, place=place)
        # If the insertion cost is minimized
        if cost < best_place_cost:
            # Update the best place for insertion
            best_place = place
            # Update the lowest insertion cost
            best_place_cost = cost
            
    return best_place
        
def costInsertion(customer: CustomerCvrp, route: List[NodeWithCoord], place: int) -> float:
    """
    costInsertion()
    
    Method to compute the insertion cost of a customer
    
    :param customer: Customer to insert in the route
    :type customer: CustomerCvrp
    :param route: Route to insert customer
    :type route:  List[NodeWithCoord]
    :param place: Place to estimate the insertion of the customer
    :type place: int
    :return: The cost of the insertion at the given place
    :rtype: float
    """
    
    # Compute all the distances
    distance1: float = euclideanDistance(route[place], route[place+1])
    distance2: float = euclideanDistance(route[place], customer)
    distance3: float = euclideanDistance(route[place+1], customer)
    
    return distance2 + distance3 - distance1
    

def kMeanCapacited(
    cvrp: Cvrp, cluster_center: List[Tuple[float, float]] = None
) -> Tuple[List[Tuple[float, float]], List[List[CustomerCvrp]]]:
    """
    kMeanCapacited()
    
    Function to run the capacited kmean algorithm
    
    :param cvrp: Cvrp instance
    :type cvrp: Cvrp
    :param cluster_center: List of cluster center, default to None (opt.)
    :type cluster_center: List[Tuple[float, float]]
    :param update_centers: Boolean to know if the centers should be updated or not
    :type update_centers: bool
    :return: The cluster center and the customer assign to clusters
    :rtype: Tuple[List[Tuple[float, float]], List[List[CustomerCvrp]]]
    """
    
    # Get the minimum number of vehicles
    cluster_number: int = cvrp.minVehiculeNumber()
    
    # List of customers assign to a cluster
    customer_assignment: List[List[CustomerCvrp]] = [[] for x in range(cluster_number)]
    
    # If the cluster centers have not been precised
    if cluster_center is None:
        # Create the cluster center
        cluster_center: List[Tuple[float, float]] = []
        # Choose randomly k unique customers to be the centers of the clusters
        cluster_center = random.sample(cvrp.customers, k=cluster_number)
        cluster_center = [cluster.getCoordinates() for cluster in cluster_center]
    
    # Get the reamining capacity of the cluster
    cluster_capacity: List[int] = [cvrp.vehicule_capacity] * cluster_number
    
    # Shuffle the list to never have the customers in the same order
    customer_shuffle: List[CustomerCvrp] = copy.copy(cvrp.customers)
    customer_shuffle.sort(key=lambda x: x.demand, reverse=True)

    # For each customer
    for customer in customer_shuffle:
        # Save the distance to each cluster
        distance_cluster: List[float] = euclideanDistanceCluster(
            customer=customer, cluster_centers=cluster_center
        )
        
        # Smallest distance with capacity ok
        smallest_dist: float = sys.maxsize
        # Smallest ratio with capacity not
        smallest_ratio: float = -sys.maxsize
        
        # best index
        best_cluster: int = -1 
        
        # Cluster distance where non violated constraint
        for index, distance in enumerate(distance_cluster):
        
            # Check if the capacity constraint is respected or not
            if (cluster_capacity[index] - customer.demand) > 0:
                # The capacity constraint is respected
                # If the cluster is nearer
                if (distance < smallest_dist):
                    # Change the best cluster
                    best_cluster = index
                    smallest_dist = distance
            # Capacity is not respected
            else:
                # Compute the ratio
                # ratio: float = distance / customer.demand
                ratio: int = cluster_capacity[index] - customer.demand
                # If the ratio is the best
                if (smallest_dist == sys.maxsize and ratio > smallest_ratio):
                    # Change the best cluster
                    best_cluster = index
                    # Update the smallest ratio
                    smallest_ratio = ratio
                 
        # Assign to the cluster
        customer_assignment[best_cluster].append(customer)
        # Update the cluster capacity
        cluster_capacity[best_cluster] = cluster_capacity[best_cluster] - customer.demand
      
    # For each cluster assignment
    for index, cluster_assignment in enumerate(customer_assignment):
        # Update the cluster centers
        cluster_center[index] = updateClusterCenter(point_assignment=cluster_assignment)
        
    return cluster_center, customer_assignment
        
def euclideanDistanceCluster(
    customer: CustomerCvrp, cluster_centers: List[Tuple[float, float]]
) -> List[float]:
    """
    euclideanDistanceCluster()
    
    Compute the euclidean distance between a cutomer and the clusters
    
    :param customer: Customer
    :type customer: CustomerCvrp
    :param cluster_centers: List of clusters center
    :type cluster_centers: List[Tuple[float, float]]
    :return: LIst of distance between customer and clusters center
    :rtype: List[float]
    """
    
    distances: List[float] = []
    
    # For each cluster center
    for cluster in cluster_centers:
        # Compute the euclidean distance
        distances.append(
            math.sqrt(
                math.pow((customer.x - cluster[0]), 2) +
                math.pow((customer.y - cluster[1]), 2)
            )
        )
        
    return distances
    
def euclideanDistance(
    customer1: CustomerCvrp, customer2: CustomerCvrp
) -> float:
    """
    euclideanDistance()
    
    Function to compute the euclidean distance between 2 customers
    
    :param customer1: First customer
    :type customer1: CustomerCvrp
    :param customer2: Second customer
    :type customer2: CustomerCvrp
    :return: The distance between the 2 customers
    :rtype: float
    """
    
    # Compute the euclidean distance
    distance = math.sqrt(
        math.pow((customer1.x - customer2.x), 2) +
        math.pow((customer1.y - customer2.y), 2)
    )
        
    return distance

def updateClusterCenter(
    point_assignment: List[CustomerCvrp]
) -> Tuple[float, float]:
    """
    updateClusterCenter()
    
    Method to update the cluster center
    
    :param point_assignment: Cluster of customer assignment
    :type point_assignment: List[CustomerCvrp]
    :return: The update cluster center
    :rtype: Tuple[float, float]
    """
    
    # Sum of x and y and get then there avg
    x_avg: int = sum(
        [point.x for point in point_assignment]
    ) / len(point_assignment)
    y_avg: int = sum(
        [point.x for point in point_assignment]
    ) / len(point_assignment)
    
    return x_avg, y_avg
