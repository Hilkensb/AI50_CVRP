#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import threading
import json

# Other Library
import matplotlib.pyplot as plt
import numpy as np
import redis as red

# Modules
from solution.cvrp.solution import SolutionCvrp
from solution.cvrp.route import RouteCvrp
from problem.cvrp.customer import CustomerCvrp
from problem.cvrp.depot import DepotCvrp
from problem.node import NodeWithCoord
from solution.constructive.clarkwrightsaving import clarkWrightSaving
from gui.config import redis_server, SOLUTION_TOPIC, SHOW_SOLUTION
from utils.redisutils import isRedisAvailable


# -------------------- Tabu Search Neighborhood functions ------------------- #

def __getPermutationNeighbours(sol: SolutionCvrp, proximity_swaps: int = 1, total_cost: int = None):
    """
    """
    return sol.getPermutationNeighbours(proximity_swaps=proximity_swaps, total_cost=total_cost) 
    
def __getRouteSwapNeighbours(sol: SolutionCvrp, proximity_swaps: int = 1, total_cost: int = None):
    """
    """
    return sol.getRouteSwapNeighbours(proximity_swaps=proximity_swaps, total_cost=total_cost) 
    
def __getClosestPermutationNeighbours(sol: SolutionCvrp, proximity_swaps: int = 1, total_cost: int = None):
    """
    """
    return sol.getClosestPermutationNeighbours(proximity_swaps=proximity_swaps, total_cost=total_cost) 
    
def __getClosestInsertionNeighbours(sol: SolutionCvrp, proximity_swaps: int = 1, total_cost: int = None):
    """
    """
    return sol.getClosestInsertionNeighbours(proximity_swaps=proximity_swaps, total_cost=total_cost) 
    
def __getInsertionNeighbours(sol: SolutionCvrp, proximity_swaps: int = 1, total_cost: int = None):
    """
    """
    return sol.getInsertionNeighbours(proximity_swaps=proximity_swaps, total_cost=total_cost) 

# -------------------------------- Variables -------------------------------- #

NEIGHBORHOODFUNCTION = {"permutationNeighbours": __getPermutationNeighbours,
                        "routeSwapNeighbours": __getRouteSwapNeighbours,
                        "closestPermutationNeighbours": __getClosestPermutationNeighbours,
                        "closestInsertionNeighbours": __getClosestInsertionNeighbours,
                        "insertionNeighbours": __getInsertionNeighbours
                        }

# ---------------------------- Tabu Search Class ---------------------------- #

class TabuSearch:
    def __init__(self, publish_topic: str = None):
        """
        Constructor
        """
        # Evolution of the best solution evaluation found
        self.__best_solution_evaluation_evolution: List[SolutionCvrp] = []
        # Evolution of the best solution found
        self.__best_solution_evolution: List[SolutionCvrp] = []
        # Set the topic where to publish evolution
        self.__topic = publish_topic

    def runMultiPhaseTabuSearch(
        self, initial_solution: SolutionCvrp, neighborhood_function_list: List[function],
        function_iteration_list: List[int], number_iteration: int = 250,
        tabu_length: int = 60, aspiration: bool = True
    ) -> SolutionCvrp:
        """
        runMultiPhaseTabuSearch()
        
        Method to run a multi phase tabu search
        
        :param initial_solution: The initial solution
        :type initial_solution: SolutionCvrp
        :param neighborhood_function_list: List of functions to find neighbours
        :type neighborhood_function_list: List of function
        :param function_iteration_list: Number of iteration to do for each function
        :type function_iteration_list: List of int
        :param number_iteration: Number of iteration to do
        :type number_iteration: int
        :param tabu_length: Length of tabu list
        :type tabu_length: int
        :param aspiration: If the aspirate criteria is enabled or not (ignore the tabu list if it upgrade the solution)
        :type aspiration: bool
        :return: An improved solution
        :rtype: SolutionCvrp
        
        """
        
        # Best solution found
        best_solution: SolutionCvrp = initial_solution
        
        # Reset the value of the evolution
        # Evolution of the best solution evaluation found
        self.__best_solution_evaluation_evolution: List[SolutionCvrp] = []
        # Evolution of the best solution found
        self.__best_solution_evolution: List[SolutionCvrp] = []
        
        # Cost of the best solution
        best_eval: float = initial_solution.evaluation()
        # Current solution
        current_solution: SolutionCvrp = initial_solution
        # Sawps that are tabu actualy
        tabu_swaps: Set[str] = set()
        # Tabu index
        tabu_index: List[str] = [None] * number_iteration
        
        # Counter of teh number of iteration made with this neighborhood function
        function_iteration_count: int = 0
        # Number of iteration for te actual function
        function_iteration_number: int = function_iteration_list[0]
        # Function used for neighborhood
        neighborhood_function = neighborhood_function_list[0]
        # Index of function
        function_index: int = 0
        
        # The current evaluation of the solution
        current_eval: float = None
        
        # For each iteration
        for iteration in range(number_iteration):
        
            # Change the function
            if function_iteration_count >= function_iteration_number:
                # Update the index
                function_index = (function_index + 1) % len(function_iteration_list)
                function_iteration_number = function_iteration_list[function_index]
                neighborhood_function = neighborhood_function_list[function_index]
                # Reset the counter
                function_iteration_count = 0
            else:
                function_iteration_count += function_iteration_count + 1
        
            # Find the length of the smallest route
            smallest_route: int = min(current_solution.route, key=lambda r: len(r))
            
            # List of neighbours
            neighbours: List(Solution) = []
            for proximity_swaps in range(len(smallest_route) - 2):
                # Get neighbours
                neighbours += neighborhood_function(current_solution, total_cost=current_eval, proximity_swaps=proximity_swaps)
              
            # Find the best solution    
            neighbours.sort(key=lambda sol: sol[1], reverse=True)
            # Get the best neighbours
            best_neighbours: Solution = neighbours.pop()
            
            # get the swap value (to be hashable)
            swap: str = best_neighbours[2]
            # Reverse the swap to be sure that if the swap is tabu
            # no matter how it is ordered the algorithm will catch it
            reverse_swap: str = "-".join(n for n in best_neighbours[2].split("-")[::1])
            
            # If the aspiration as not been activated or the new solution does not upgrade the solution
            if not aspiration or best_neighbours[1] > best_eval:
                # While the swaps is tabu
                while (swap in tabu_swaps or reverse_swap in tabu_swaps) and len(neighbours):
                    # find another good solution
                    best_neighbours=neighbours.pop()
                    swap: str = best_neighbours[2]
                    reverse_swap: str = "-".join(n for n in best_neighbours[2].split("-")[::1])
                # If there's no solution non tabu go to next iteration
                if len(neighbours) == 0:
                    # Create an history of the  best value
                    self.__addNewSolution(solution=best_solution, evaluation=best_eval)
                    continue
            # If the solution triggered the aspiration, check if it was tabu
            elif swap in tabu_swaps or reverse_swap in tabu_swaps:
                # Replace the swap in the tabu index by None
                tabu_index = tabu_index[:max(iteration-tabu_length, 0)] + [None if neighbor == best_neighbours[2] else neighbor for neighbor in tabu_index[max(iteration-tabu_length, 0):iteration]] + tabu_index[iteration:]
 
 
            # Update the current solution   
            current_solution = best_neighbours[0]
            current_eval = best_neighbours[1]
            # Make the swap tabu
            tabu_swaps.add(swap)
            # Set the swap tabu in a list to keep the iteration where it should pop
            # from the set
            tabu_index[iteration] = swap
            
            # Remove a tabu value
            if iteration >= tabu_length and tabu_index[iteration-tabu_length] is not None:
                tabu_swaps.remove(tabu_index[iteration-tabu_length])
                   
            # update the best value if needed       
            if best_neighbours[1] < best_eval:
                best_solution = best_neighbours[0]
                best_eval = best_neighbours[1] 
                
            # Create an history of the  best value
            self.__addNewSolution(solution=best_solution, evaluation=best_eval)

        return best_solution

    def runTabuSearch(
        self, initial_solution: SolutionCvrp, neighborhood_function: function,
        number_iteration: int = 250, tabu_length: int = 10,
        aspiration: bool = True
    ) -> SolutionCvrp:
        """        
        runTabuSearch()
        
         Method to run a tabu search
        
        :param initial_solution: The initial solution
        :type initial_solution: SolutionCvrp
        :param neighborhood_function: function to find neighbours
        :type neighborhood_function: function
        :param number_iteration: Number of iteration to do
        :type number_iteration: int
        :param tabu_length: Length of tabu list
        :type tabu_length: int
        :param aspiration: If the aspirate criteria is enabled or not (ignore the tabu list if it upgrade the solution)
        :type aspiration: bool
        :return: An improved solution
        :rtype: SolutionCvrp
        """
        
        # Best solution found
        best_solution: SolutionCvrp = initial_solution
        
        # Reset the value of the evolution
        # Evolution of the best solution evaluation found
        self.__best_solution_evaluation_evolution: List[SolutionCvrp] = []
        # Evolution of the best solution found
        self.__best_solution_evolution: List[SolutionCvrp] = []
        
        # Cost of the best solution
        best_eval: float = initial_solution.evaluation()
        # Current solution
        current_solution: SolutionCvrp = initial_solution
        # Sawps that are tabu actualy
        tabu_swaps: Set[str] = set()
        # Tabu index
        tabu_index: List[str] = [None] * number_iteration
        
        # The current evaluation of the solution
        current_eval: float = None
        
        # For each iteration
        for iteration in range(number_iteration):
        
            # Find the length of the smallest route
            smallest_route: int = min(current_solution.route, key=lambda r: len(r))
            
            # List of neighbours
            neighbours: List(Solution) = []
            for proximity_swaps in range(len(smallest_route) - 2):
                # Get neighbours
                neighbours += neighborhood_function(current_solution, total_cost=current_eval, proximity_swaps=proximity_swaps)
              
            # Find the best solution    
            neighbours.sort(key=lambda sol: sol[1], reverse=True)
            # Get the best solution
            best_neighbours: Solution = neighbours.pop()
            
            # Get the swap realize
            swap: str = best_neighbours[2]
            # Reverse the string of the maded swap
            reverse_swap: str = "-".join(n for n in best_neighbours[2].split("-")[::1])
            
            # If the aspiration as not been activated or the new solution does not upgrade the solution
            if not aspiration or best_neighbours[1] > best_eval:
                # While the swaps is tabu
                while (swap in tabu_swaps or reverse_swap in tabu_swaps):
                    # find another good solution
                    best_neighbours = neighbours.pop()
                    swap: str = best_neighbours[2]
                    reverse_swap: str = "-".join(n for n in best_neighbours[2].split("-")[::1])
                # If there's no solution non tabu go to next iteration
                if len(neighbours):
                    # Go to next iteration
                    continue
            # If the solution triggered the aspiration, check if it was tabu
            elif swap in tabu_swaps or reverse_swap in tabu_swaps:
                # Replace the swap in the tabu index by None
                tabu_index = tabu_index[:max(iteration-tabu_length, 0)] + [None if neighbor == best_neighbours[2] else neighbor for neighbor in tabu_index[max(iteration-tabu_length, 0):iteration]] + tabu_index[iteration:]
                
            
            # Update the current solution   
            current_solution = best_neighbours[0]
            current_eval = best_neighbours[1]
            # Make the swap tabu
            tabu_swaps.add(best_neighbours[2])
            tabu_index[iteration] = best_neighbours[2]
            
            # Remove a tabu value
            if iteration >= tabu_length and tabu_index[iteration-tabu_length] is not None:
                tabu_index = [None if neighbor == best_neighbours[2] else neighbor for neighbor in tabu_index]
                   
            # update the best value if needed       
            if best_neighbours[1] < best_eval:
                best_solution = best_neighbours[0]
                best_eval = best_neighbours[1]
                
            # Create an history of the  best value
            self.__addNewSolution(solution=best_solution, evaluation=best_eval)

        return best_solution
      
    def runMultiPhaseTabuSearchThread(
        self, initial_solution: SolutionCvrp, neighborhood_function: List[function],
        function_iteration: List[int], number_iteration: int = 250,
        tabu_length: int = 60, aspiration: bool = True, max_second_run: int = 45
    ) -> None:
        """
        runMultiPhaseTabuSearchThread()
        
        Method to run a multi phase tabu search in an other thread to be stoped after a giving amount of time
        
        :param initial_solution: The initial solution
        :type initial_solution: SolutionCvrp
        :param neighborhood_function_list: List of functions to find neighbours
        :type neighborhood_function_list: List of function
        :param function_iteration_list: Number of iteration to do for each function
        :type function_iteration_list: List of int
        :param number_iteration: Number of iteration to do
        :type number_iteration: int
        :param tabu_length: Length of tabu list
        :type tabu_length: int
        :param aspiration: If the aspirate criteria is enabled or not (ignore the tabu list if it upgrade the solution)
        :type aspiration: bool
        :param max_second_run: Maximum second to run tabu search
        :type max_second_run: int
        :return: An improved solution
        :rtype: SolutionCvrp
        """
        # Thread running the tabu search       
        thread_tabu = threading.Thread(
            target=self.runMultiPhaseTabuSearch,
            kwargs={
                "initial_solution":initial_solution,
                "neighborhood_function_list":neighborhood_function,
                "number_iteration":number_iteration, "tabu_length":tabu_length, 
                "function_iteration_list":function_iteration, "aspiration":aspiration
            }, daemon=True
        )
        
        # launch the thread  
        thread_tabu.start()
        # wait n seconds for the thread to finish its work
        thread_tabu.join(max_second_run)
        
    def runTabuSearchThread(
        self, initial_solution: SolutionCvrp, neighborhood_function: funtion,
        number_iteration: int = 250, tabu_length: int = 60,
        aspiration: bool = True, max_second_run: int = 45
    )  -> None:
        """
        runTabuSearchThread()
        
        Method to run a multi phase tabu search in an other thread to be stoped after a giving amount of time
        
        :param initial_solution: The initial solution
        :type initial_solution: SolutionCvrp
        :param neighborhood_function: functions to find neighbours
        :type neighborhood_function: function
        :param number_iteration: Number of iteration to do
        :type number_iteration: int
        :param tabu_length: Length of tabu list
        :type tabu_length: int
        :param aspiration: If the aspirate criteria is enabled or not (ignore the tabu list if it upgrade the solution)
        :type aspiration: bool
        :param max_second_run: Maximum second to run tabu search
        :type max_second_run: int
        :return: An improved solution
        :rtype: SolutionCvrp
        """
        
        # Thread running the tabu search       
        thread_tabu = threading.Thread(
            target=self.runTabuSearch,
            kwargs={
                "initial_solution":initial_solution,
                "neighborhood_function":neighborhood_function,
                "number_iteration":number_iteration, "tabu_length":tabu_length,
                 "aspiration":aspiration
            }, daemon=True
        )
        
        # launch the thread  
        thread_tabu.start()
        # wait n seconds for the thread to finish its work
        thread_tabu.join(max_second_run)  
        
        # Check if the tabu thread is still alive
        if thread_tabu.isAlive():
            # If tth thread is alive, kill it
            thread_tabu.join()
               

    def __addNewSolution(self, solution: SolutionCvrp, evaluation: float, rounded_json: int = 2):
        """
        """
        # Create an history of the  best value
        self.__best_solution_evaluation_evolution.append(evaluation)
        self.__best_solution_evolution.append(solution)
        
        # if redis is on
        if isRedisAvailable():
            # Create the data
            json_data = {
                "algorithm_name": "Tabu search", "cost": round(evaluation, 2),
                "iteration":len(self.__best_solution_evaluation_evolution),
                "graph": solution.drawPlotlyJSON() if SHOW_SOLUTION else ""
            }
            # Publish
            redis_server.publish(self.__topic, json.dumps(json_data))

    @property 
    def best_solution_evaluation_evolution(self) -> List[int]:
        return self.__best_solution_evaluation_evolution
        
    @property 
    def best_solution_evolution(self) -> List[SolutionCvrp]:
        return self.__best_solution_evolution

# ----------------------- Function to run tabu search ----------------------- #

def tabuSearch(
    initial_solution: SolutionCvrp, multiphase: bool = True,
    neighborhood_function_list: Union[List[str], str] = ["closestInsertionNeighbours", "routeSwapNeighbours"],
    function_iteration_list: List[int] = [3, 9], number_iteration: int = -1,
    tabu_length: int = -1, aspiration: bool = True, max_second_run: int = 45,
    publish_topic: str = SOLUTION_TOPIC
) -> TabuSearch:
    """
    tabuSearch()
    
    Function to run tabu search
    
    :param initial_solution: The initial solution
    :type initial_solution: SolutionCvrp
    :param multiphase: Boolean to know if the tabu search need to have multiple phase
    :type multiphase: bool
    :param neighborhood_function_list: List of functions to find neighbours
    :type neighborhood_function_list: List of function
    :param function_iteration_list: Number of iteration to do for each function
    :type function_iteration_list: List of int
    :param number_iteration: Number of iteration to do
    :type number_iteration: int
    :param tabu_length: Length of tabu list
    :type tabu_length: int
    :param aspiration: If the aspirate criteria is enabled or not (ignore the tabu list if it upgrade the solution)
    :type aspiration: bool
    :param max_second_run: Maximum second to run tabu search
    :type max_second_run: int
    :param publish_topic: topic name where to publish the solution
    :type publish_topic: str
    :return: An improved solution with all the historical solution found
    :rtype: TabuSearch
    """

    # Create the object to run the tabu search
    tabu_search = TabuSearch(publish_topic=publish_topic)
    
    # Set the param for the tabu search
    # Set the number_iteration if it has not been set
    if number_iteration < 0:
        # The number of iteration is equal to the number of customer up to 500, but higher than 100
        number_iteration = max(min(len(initial_solution.cvrp_instance.customers), 500), 100)
    
    # Set the tabu list length
    if tabu_length < 0:
        # Set the tabu lenght to a 10th of iteration
        tabu_length = round(number_iteration * 0.1)
        
    # If it's a multiphase tabusearch
    if multiphase:
        # tabu search function
        tabu_search_function = tabu_search.runMultiPhaseTabuSearch
        
        neighborhood_function: List[function] = []
        # Check if we need to fill neighborhood_function_list
        if (neighborhood_function_list is None or len(neighborhood_function_list) < 1):
            # Fill it with insertion and swap neighborhood function
            neighborhood_function = [__getClosestInsertionNeighbours, __getRouteSwapNeighbours]
        # Set the string to the corresponding neighborhood function
        else:
            # for each function representation passed in arguement
            for neighbor_func_str in neighborhood_function_list:
                # Try to get the function
                try:
                    neighborhood_function.append(NEIGHBORHOODFUNCTION[neighbor_func_str])
                except IndexError:
                    raise ValueError(f"The function linked to the string {neighbor_func_str} does not exists.")
          
        function_iteration: List[int] = []
        # Check if we need to fill the iteration list for each function            
        if (function_iteration_list is None):
            # Fill the list with 5
            function_iteration = [5] * len(neighborhood_function)
        elif (len(function_iteration_list) < len(neighborhood_function)):
            # Fill the list with 5
            function_iteration = [5] * (len(neighborhood_function) - len(function_iteration_list))
        else:
            # Be sure it does not exceed the size of the function list
            function_iteration = function_iteration_list[:len(function_iteration_list)]
    else:
        neighborhood_function: function = None
        # If the neighborhood is empty
        if (neighborhood_function_list is None or
            (isinstance(neighborhood_function_list, list) and len(neighborhood_function_list) == 0)):
            # Set the neighborhood function
            neighborhood_function = __getClosestInsertionNeighbours
        # neighborhood_function_list is a list
        elif (isinstance(neighborhood_function_list, list)):
            # Try to parse the argue and find the corresponding function
            try:
                neighborhood_function = NEIGHBORHOODFUNCTION[neighborhood_function_list[0]]
            except IndexError:
                raise ValueError(f"The function linked to the string {neighborhood_function_list[0]} does not exists.")
        else:
            # Try to parse the argue and find the corresponding function
            try:
                neighborhood_function = NEIGHBORHOODFUNCTION[neighborhood_function_list]
            except IndexError:
                raise ValueError(f"The function linked to the string {neighborhood_function_list} does not exists.")

    if multiphase:
        # Run in another thread the tabu search
        tabu_search.runMultiPhaseTabuSearchThread(
            initial_solution=initial_solution, neighborhood_function=neighborhood_function,
            function_iteration=function_iteration, number_iteration=number_iteration,
            tabu_length=tabu_length, aspiration=aspiration, max_second_run=max_second_run
        )
    else:
        # Run in another thread the tabu search
        tabu_search.runTabuSearchThread(
            initial_solution=initial_solution, neighborhood_function=neighborhood_function,
            number_iteration=number_iteration, tabu_length=tabu_length,
            aspiration=aspiration, max_second_run=max_second_run
        )
    
    return tabu_search

def easyTabuSearch(
    initial_solution: SolutionCvrp, multiphase: bool = True,
    neighborhood_function_list: Union[List[str], str] = ["closestInsertionNeighbours", "routeSwapNeighbours"],
    function_iteration_list: List[int] = [3, 9], number_iteration: int = -1,
    tabu_length: int = -1, aspiration: bool = True, max_second_run: int = 45,
    publish_topic: str = SOLUTION_TOPIC
) -> List[SolutionCvrp]:
    """
    tabuSearch()
    
    Function to run tabu search
    
    :param initial_solution: The initial solution
    :type initial_solution: SolutionCvrp
    :param multiphase: Boolean to know if the tabu search need to have multiple phase
    :type multiphase: bool
    :param neighborhood_function_list: List of functions to find neighbours
    :type neighborhood_function_list: List of function
    :param function_iteration_list: Number of iteration to do for each function
    :type function_iteration_list: List of int
    :param number_iteration: Number of iteration to do
    :type number_iteration: int
    :param tabu_length: Length of tabu list
    :type tabu_length: int
    :param aspiration: If the aspirate criteria is enabled or not (ignore the tabu list if it upgrade the solution)
    :type aspiration: bool
    :param max_second_run: Maximum second to run tabu search
    :type max_second_run: int
    :param publish_topic: topic name where to publish the solution
    :type publish_topic: str
    :return: An improved solution with all the historical solution found
    :rtype: TabuSearch
    """
    
    tabu_search_result: TabuSearch = tabuSearch(
        initial_solution=initial_solution, multiphase=multiphase,
        neighborhood_function_list=neighborhood_function_list,
        function_iteration_list=function_iteration_list, number_iteration=number_iteration,
        tabu_length=tabu_length, aspiration=aspiration, max_second_run=max_second_run,
        publish_topic=publish_topic
    )
    
    return tabu_search_result.best_solution_evolution, tabu_search_result.best_solution_evaluation_evolution
                    
