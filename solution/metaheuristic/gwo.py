#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
import sys
import copy
import random
from typing import List, Dict, Tuple, Union
import math
import json
import threading

# Other Library
import numpy

# Modules
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from solution.cvrp.solution import RouteCvrp
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import NodeWithCoord
from gui.config import redis_server, SOLUTION_TOPIC
from utils.redisutils import isRedisAvailable
from utils.parseparameters import SHOW_SOLUTION

    
# ----------------------------- Global variables ---------------------------- #    
   
# Set and dicts to memorize which cluster of point we already treated
# And get the route and their evaluation of cluster point already treated
# Used to build route and their evaluation more quickly  
cluster_set = set()
route_dict = dict()
route_values_dict = dict()

# ------------------------ Grey Wolf Optimizer Class ------------------------ #

# wolf class
class Wolf:
    def __init__(self, cvrp: Cvrp, cluster_center: List[Tuple[float, float]] = None):
        """
        Constructor
        
        :param cvrp: Cvrp instance to solve
        :type cvrp: Cvrp
        :param penalty: Penalty if the demand supplied is greater than the vehicle capacity
        :type penalty: int
        """
        
        if cluster_center is None:
            # Get the x and y values of customer in the cvrp
            x_values: List[int] = [customer.x for customer in cvrp.customers]
            y_values: List[int] = [customer.y for customer in cvrp.customers]
            
            # Determine the max and min value of x and y
            # For x
            max_x: int = max(x_values)
            min_x: int = min(x_values)
            # For y
            max_y: int = max(y_values)
            min_y: int = min(y_values)
            
            # Create random cluster center
            self.cluster_center: List[Tuple[float]] = [tuple([
                (random.uniform(0,1) * (max_x - min_x)) + min_x,
                (random.uniform(0,1) * (max_y - min_y)) + min_y
            ]) for i in range(cvrp.minVehiculeNumber())]
        else:
            self.cluster_center = cluster_center

        # Create random cluster
        self.cluster_center, self.assignment = kMeanCapacited(cvrp=cvrp, cluster_center=self.cluster_center, update_centers=False)
        
        self.cvrp: Cvrp = cvrp
        # Compute the fitness
        self.fitness: float = self.computeFitness()
 
    def computeFitness(self) -> float:
        """
        computeFitness()
        
        Method to compute the fitness of a wolf
        
        :return: The fitness of the wolf
        :rtype: float
        """
           
        evaluation: float = 0.0
        
        global cluster_set
        global route_dict
        global route_values_dict
           
        builded_route: List[RouteCvrp] = []   
        # Build the route with the customer assignment to cluster
        for customer_cluster in self.assignment:
        
            # hash the clusters point
            key=hash(tuple(customer_cluster))  
            # If this cluster has already been seen      
            if key in cluster_set:
                builded_route.append(route_dict[key])
                evaluation += route_values_dict[key]
            else:
                # Build route wih the assignment in the cluster
                route_list: List[NodeWithCoord] = buildClusterRoute(
                    cluster_customer=customer_cluster, depot=self.cvrp.depot
                )
                # Build the route cvrp
                new_route: RouteCvrp = RouteCvrp(route=route_list)
                # Add it to the list of route
                builded_route.append(new_route)
                evaluation += new_route.evaluation()
                cluster_set.add(key)
                route_dict[key] = new_route
                route_values_dict[key] = evaluation
            
        # Build the solution
        self.solution_found: SolutionCvrp = SolutionCvrp(instance=self.cvrp, route=builded_route)
        self.fitness: float = evaluation
        
        return self.fitness

class WolfPack:
    def __init__(self):
        """
        Constructor
        """

        # Evolution of the best solution evaluation found
        self.__best_solution_evaluation_evolution: List[float] = []
        # Evolution of the best solution found
        self.__best_solution_evolution: List[SolutionCvrp] = []        
        # Varaible to know if the tabu serach is still running
        self.__running: bool = False
    
    # grey wolf optimization (GWO)
    def gwo(
        self, max_iter: int, wolf_number: int, cvrp: Cvrp, topic: str
    ) -> Tuple[List[SolutionCvrp], List[float]]:
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
        
        self.__running = True
        rnd: random.Random = random.Random(0)
     
        # create n random wolves
        population: List[Wolf] = [ Wolf(cvrp=cvrp) for i in range(wolf_number)]
     
        # On the basis of fitness values of wolves
        # sort the population in asc order
        population = sorted(population, key = lambda temp: temp.fitness)
     
        # best 3 solutions will be called as
        # alpha, beta and gaama
        alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
     
        # Get the minimum number of vehicles
        cluster_number: int = cvrp.minVehiculeNumber()
     
        # main loop of gwo
        Iter: int = 0
        while Iter < max_iter and self.__running:
     
            # linearly decreased from 2 to 0
            a: float = 2.0 * (1.0 - Iter/max_iter)
     
            # updating each population member with the help of best three members
            for i in range(wolf_number):
            
                r1: float = rnd.random()
                # Compute the A
                A1: float = 2.0 * a * r1 - a
                A2: float = 2.0 * a * r1 - a
                A3: float = 2.0 * a * r1 - a
                
                r2: float = rnd.random()
                # Compute the c values
                C1: float = 2.0 * r2
                C2: float = 2.0 * r2
                C3: float = 2.0 * r2
     
                # Create vectors 0
                X1: List[Tuple[float]] = [tuple([0.0, 0.0]) for i in range(cluster_number)]
                X2: List[Tuple[float]] = [tuple([0.0, 0.0]) for i in range(cluster_number)]
                X3: List[Tuple[float]] = [tuple([0.0, 0.0]) for i in range(cluster_number)]
                Xnew: List[Tuple[float]] = [tuple([0.0, 0.0]) for i in range(cluster_number)]
                
                # For each cluster
                for j in range(cluster_number):
                    # Update the position values with given alpha, beta and gamma position
                    X1[j] = tuple(
                        cluster_center - A1 * abs(
                            C1 * cluster_center - population[i].cluster_center[j][index]
                        )
                        for index, cluster_center in enumerate(alpha_wolf.cluster_center[j])
                    )
                    
                    X2[j] = tuple(
                        cluster_center - A2 * abs(
                            C2 * cluster_center - population[i].cluster_center[j][index]
                        )
                        for index, cluster_center in enumerate(beta_wolf.cluster_center[j])
                    )
                    
                    X3[j] = tuple(
                        cluster_center - A3 * abs(
                            C3 * cluster_center - population[i].cluster_center[j][index]
                        )
                        for index, cluster_center in enumerate(gamma_wolf.cluster_center[j])
                    )
                    
                    Xnew[j] = tuple(X1[j][val] + X2[j][val] + X3[j][val] for val in range(len(Xnew[j])))
                 
                # Create a new wolf 
                for j in range(cluster_number):
                    # Set it's value
                    Xnew[j] = tuple(Xnew[j][val] / 3.0 for val in range(len(Xnew[j])))
     
                # Create a temporary wolf
                wolf_temp: Wolf = Wolf(cvrp, Xnew)
     
                # greedy selection
                # If the fitness is better
                if wolf_temp.fitness < population[i].fitness:
                    population[i] = wolf_temp
                     
            # On the basis of fitness values of wolves
            # sort the population in asc order
            population = sorted(population, key = lambda temp: temp.fitness)
     
            # best 3 solutions will be called as
            # alpha, beta and gaama
            alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
             
            # Increase the iteration 
            Iter+= 1
            
            # Add the solution
            self.__best_solution_evolution.append(alpha_wolf.solution_found)
            self.__best_solution_evaluation_evolution.append(alpha_wolf.fitness)
            
            # if redis is on
            if isRedisAvailable():
                # Create the data
                json_data = {
                    "algorithm_name": "Grey Wolf Optimizer", "cost": round(alpha_wolf.fitness, 2),
                    "iteration": Iter,
                    "graph": solution.drawPlotlyJSON() if SHOW_SOLUTION else ""
                }
                # Publish
                redis_server.publish(topic, json.dumps(json_data))
            
        # end-while
     
        # returning the best solution
        return self.__best_solution_evolution, self.__best_solution_evaluation_evolution
        
    def runGwoThread(
        self, max_iter: int, wolf_number: int, cvrp: Cvrp, topic: str,
        max_second_run: int = 45
    ) -> None:
        """
        runGwoThread()
        
        Function to launch the Grey Wolf Optimizer in an other thread to be stoped when we need.
    
        :param cvrp: The cvrp instance to find a solution
        :type cvrp: Cvrp
        :param iteration: Number of iteration to run
        :type iteration: int
        :param wolf_number: Number of wolf
        :type wolf_number: int
        :param max_second_run: Maximum second to run tabu search
        :type max_second_run: int
        """
        
        self.__running = True
        
        # Thread running the tabu search       
        thread_gwo = threading.Thread(
            target=self.gwo,
            kwargs={
                "max_iter": max_iter, "wolf_number": wolf_number, "cvrp": cvrp,
                "topic": topic
            }, daemon=True
        )
        
        # launch the thread  
        thread_gwo.start()
        # wait n seconds for the thread to finish its work
        thread_gwo.join(max_second_run)
        
        self.__running = False
        
    @property 
    def best_solution_evaluation_evolution(self) -> List[int]:
        return self.__best_solution_evaluation_evolution
        
    @property 
    def best_solution_evolution(self) -> List[SolutionCvrp]:
        return self.__best_solution_evolution

# ------------------------- Grey Wolf Optimizer Run ------------------------- #

def greyWolfSolver(
    cvrp: Cvrp, topic: str, iteration: int = 100, wolf_number: int = 20,
    max_second_run: int = 45
) -> Tuple[List[SolutionCvrp], List[float]]:
    """
    greyWolfSolver()
    
    Function to launch the Grey Wolf Optimizer
    
    :param cvrp: The cvrp instance to find a solution
    :type cvrp: Cvrp
    :param iteration: Number of iteration to run
    :type iteration: int
    :param wolf_number: Number of wolf
    :type wolf_number: int
    :param max_second_run: Maximum second to run tabu search
    :type max_second_run: int
    :return: Solution found and the evaluation
    :rtype: Tuple[List[SolutionCvrp], List[float]]

    .. note: Based on: https://iopscience.iop.org/article/10.1088/1757-899X/83/1/012014/pdf
    """
    
    # Create the wolf pack for the grey wolf optimizer
    wolf_pack: WolfPack = WolfPack()
    
    # Run the algorithm
    wolf_pack.runGwoThread(
        max_iter=iteration, cvrp=cvrp, wolf_number=wolf_number, topic=topic,
        max_second_run=max_second_run
    )
    
    return wolf_pack.best_solution_evolution, wolf_pack.best_solution_evaluation_evolution
    
# ----------------------------- Utils functions ----------------------------- #
    
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
           
#----------------------------

def kMeanCapacited(
    cvrp: Cvrp, cluster_center: List[Tuple[float, float]] = None,
    update_centers: bool = True
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
    # customer_shuffle.sort(key=lambda x: x.demand)
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

def euclideanDistancePoint(customer: CustomerCvrp, point: Tuple[int]) -> float:
    """
    euclideanDistancePoint()
    
    :param customer: Customer to compute the distance
    :type customer: CustomerCvrp
    :param point: Point to compute the distance
    :type point: Tuple[int]
    """
    
    # Compute the euclidean distance
    distance = math.sqrt(
        math.pow((customer.x - point[0]), 2) +
        math.pow((customer.y - point[1]), 2)
    )
        
    return distance
 
