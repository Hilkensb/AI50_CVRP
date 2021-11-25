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


# wolf class
class Wolf:
    def __init__(self, cvrp: Cvrp):
        """
        Constructor
        
        :param cvrp: Cvrp instance to solve
        :type cvrp: Cvrp
        """
        
        # Create random cluster
        self.cluster_center, self.assignment = kMeanCapacited(cvrp)
 
    def computeFitness(self) -> float:
        """
        computeFitness()
        
        Method to compute the fitness of a wolf
        
        :return: The fitness of the wolf
        :rtype: float
        """
        
        # Initialize the fitness
        fitness: float = 0.0
        
        # For all cluster
        for index, cluster_center in enumerate(self.cluster_center):
            # For all customer in the cluster
            for customer in self.assignment[index]:
                # Compute the fitness, by adding the distance of the customer to the
                # center of the cluster
                fitness += euclideanDistancePoint(customer, cluster_center)
                
        return fitness

def greyWolfSolver(cvrp: Cvrp, iteration: int = 100, wolf_number: int = 20) -> Tuple[List[SolutionCvrp], List[float]]:
    """
    greyWolfSolver()
    
    Function to launch the Grey Wolf Optimizer
    
    :param cvrp: The cvrp instance to find a solution
    :type cvrp: Cvrp
    :param iteration: Number of iteration to run
    :type iteration: int
    :param wolf_number: Number of wolf
    :type wolf_number: int

    .. note: based on: https://iopscience.iop.org/article/10.1088/1757-899X/83/1/012014/pdf
    """
    
    # Run the greyWolfOptimizer
    wolf = gwo(max_iter=iteration, cvrp=cvrp, wolf_number=wolf_number)
    # Get the assigment and the cluster centers
    customer_assignment = wolf.assignment
    customer_cluster = wolf.cluster_center
         
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
    
def findBestPlace(customer: CustomerCvrp, route: List[NodeWithCoord]) -> int:
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
            
# grey wolf optimization (GWO)
def gwo(max_iter: int, wolf_number: int, cvrp: Cvrp) -> Wolf:
    """
    gwo()
    
    Function to run the Grey Wolf Optimizer
    
    :param cvrp: The cvrp instance to find a solution
    :type cvrp: Cvrp
    :param max_iter: Number of iteration to run
    :type max_iter: int
    :param wolf_number: Number of wolf
    :type wolf_number: int
    :return: The alpha wolf
    :rtype: Wolf
    """
    rnd = random.Random(0)
 
    # create n random wolves
    population = [ Wolf(cvrp) for i in range(wolf_number)]
 
    # On the basis of fitness values of wolves
    # sort the population in asc order
    population = sorted(population, key = lambda temp: temp.computeFitness())
 
    # best 3 solutions will be called as
    # alpha, beta and gaama
    alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
 
    # Get the minimum number of vehicles
    cluster_number: int = cvrp.minVehiculeNumber()
 
    # main loop of gwo
    Iter = 0
    while Iter < max_iter:
 
        # linearly decreased from 2 to 0
        a = 2*(1 - Iter/max_iter)
 
        # updating each population member with the help of best three members
        for i in range(wolf_number):
            # Compute the A
            A1, A2, A3 = a * (2 * rnd.random() - 1), a * (
              2 * rnd.random() - 1), a * (2 * rnd.random() - 1)
            C1, C2, C3 = 2 * rnd.random(), 2*rnd.random(), 2*rnd.random()
 
            # Create vectors 0
            X1 = [tuple([0.0, 0.0]) for i in range(cluster_number)]
            X2 = [tuple([0.0, 0.0]) for i in range(cluster_number)]
            X3 = [tuple([0.0, 0.0]) for i in range(cluster_number)]
            Xnew = [tuple([0.0, 0.0]) for i in range(cluster_number)]
            
            # For each cluster
            for j in range(cluster_number):
                # Update the position values with given alpha, beta and gamma position
                X1[j] = tuple(
                    cluster_center - A1 * abs(
                        C1 - cluster_center - population[i].cluster_center[j][index]
                    )
                    for index, cluster_center in enumerate(alpha_wolf.cluster_center[j])
                )
                
                X2[j] = tuple(
                    cluster_center - A2 * abs(
                        C2 - cluster_center - population[i].cluster_center[j][index]
                    )
                    for index, cluster_center in enumerate(beta_wolf.cluster_center[j])
                )
                
                X3[j] = tuple(
                    cluster_center - A3 * abs(
                        C3 - cluster_center - population[i].cluster_center[j][index]
                    )
                    for index, cluster_center in enumerate(gamma_wolf.cluster_center[j])
                )
                
                Xnew[j] = tuple(Xnew[j][val] + X1[j][val] + X2[j][val] + X3[j][val] for val in range(len(Xnew[j])))
             
            # Create a new wolf 
            for j in range(cluster_number):
                # Set it's value
                Xnew[j] = tuple(Xnew[j][val] / 3.0 for val in range(len(Xnew[j])))
             
            # fitness calculation of new solution
            cluster_center, assignment = kMeanCapacited(cvrp, cluster_center=Xnew, update_centers=False)
 
            # Compute the fitness of the new wolf
            fnew: float = 0.0
            # For every cluster center
            for index, center in enumerate(cluster_center):
                # For every customer
                for customer in assignment[index]:
                    # Compute it's fitness
                    fnew += euclideanDistancePoint(customer, center)
 
            # greedy selection
            # If the fitness is better
            if fnew < population[i].computeFitness():
                population[i].position = Xnew
                population[i].fitness = fnew
                 
        # On the basis of fitness values of wolves
        # sort the population in asc order
        population = sorted(population, key = lambda temp: temp.computeFitness())
 
        # best 3 solutions will be called as
        # alpha, beta and gaama
        alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
         
        Iter+= 1
    # end-while
 
    # returning the best solution
    return alpha_wolf
           
#----------------------------

def kMeanCapacited(
    cvrp: Cvrp, cluster_center: List[Tuple[float, float]] = None,
    update_centers: bool = True
) -> Tuple[List[Tuple[float, float]], List[List[CustomerCvrp]]]:
    """
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
    random.shuffle(customer_shuffle)

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
    
    # Updating the cluster center  
    if update_centers:
        # For each cluster assignment
        for index, cluster_assignment in enumerate(customer_assignment):
            # Update the cluster centers
            cluster_center[index] = updateClusterCenter(point_assignment=cluster_assignment)
        
    return cluster_center, customer_assignment

def euclideanDistanceCluster(
    customer: CustomerCvrp, cluster_centers: List[Tuple[float, float]]
) -> List[float]:
    """
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
    """
    
    # Sum of x and y and get then there avg
    x_avg: int = sum(
        [point.x for point in point_assignment]
    ) / len(point_assignment)
    y_avg: int = sum(
        [point.x for point in point_assignment]
    ) / len(point_assignment)
    
    return x_avg, y_avg

def euclideanDistancePoint(customer: CustomerCvrp, point: Tuple[int]) -> float:
    """
    """
    
    # Compute the euclidean distance
    distance = math.sqrt(
        math.pow((customer.x - point[0]), 2) +
        math.pow((customer.y - point[1]), 2)
    )
        
    return distance
 
