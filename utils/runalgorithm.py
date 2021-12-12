#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import json
import time

# Other library
from solution.metaheuristic.tabusearch import tabuSearch
from solution.constructive.clarkwrightsaving import clarkWrightSaving
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from utils.redisutils import isRedisAvailable
from gui.config import SOLUTION_TOPIC, redis_server


def runAlgorithm(
    cvrp_instance: Cvrp, algorithm_list: List, algorithm_kargs: List,
    algorithm_name: List, publish_topic: str
) -> List[Union[List[SolutionCvrp], SolutionCvrp]]:
    """
    """
    
    # List of all solution found
    solution_found: List[Union[List[SolutionCvrp], SolutionCvrp]] = []
    # List of solution's costs
    cost_list: List[float] = []
    # time took by each algorithm
    time_algorithm: List[float] = []
    
    # For every algorithm
    for index, algorithm in enumerate(algorithm_list):
    
        # if redis is on
        if isRedisAvailable():
            # Create the data
            json_data = {
                "algorithm_name": algorithm_name[index], "cost": 0,
                "iteration" : 0,"graph": ""
            }
            # Publish
            redis_server.publish(publish_topic, json.dumps(json_data))
    
        # Algorithm arguments
        algo_args = algorithm_kargs[index]
        
        # Start mesuring time took by algorithm runned
        start_algorithm = time.time()
        # Run the algorihtm
        solution, cost = algorithm(
            **algo_args
        )
        # Stop mesuring time took by algorithm runned
        end_algorithm = time.time()
        
        # add the time took into the list
        time_algorithm.append(round(end_algorithm - start_algorithm, 2))
        # add the solution's costs to the list
        cost_list.append(cost)
        # add the solution to the list of solution found
        solution_found.append(solution)
        
    # Return the solutions found
    return solution_found, cost_list, time_algorithm

