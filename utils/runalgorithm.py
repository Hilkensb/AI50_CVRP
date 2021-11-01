#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import json

# Other library
from solution.metaheuristic.tabusearch import tabuSearch
from solution.constructive.clarkwrightsaving import clarkWrightSaving
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp
from utils.redisutils import isRedisAvailable
from gui.config import SOLUTION_TOPIC, redis_server


def runAlgorithm(
    cvrp_instance: Cvrp, algorithm_list: List, algorithm_kargs: List,
    algorithm_name: List
) -> List[SolutionCvrp]:
    """
    """
    
    
    # List of all solution found
    solution_found: List = []
    
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
            redis_server.publish(SOLUTION_TOPIC, json.dumps(json_data))
    
        # Algorithm arguments
        algo_args = algorithm_kargs[index]
        # Run the algorihtm
        solution = algorithm(
            **algo_args
        )

        # add the solution to the list of solution found
        solution_found.append(solution)
        
    # Return the solutions found
    return solution_found

