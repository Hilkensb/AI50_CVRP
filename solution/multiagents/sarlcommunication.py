#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import json
import time
from ast import literal_eval
import re

# Modules
from gui.config import redis_server, SARL_SOLUTION_TOPIC
from problem.cvrp.instance import Cvrp
from solution.cvrp.solution import SolutionCvrp


def sarlSender(topic: str, instance: Cvrp) -> Tuple[List[SolutionCvrp], float]:
    """
    sarlSender()
    
    Send the instance to sarl
    
    :param topic: Topic where the result will be published
    :type topic: str
    :param instance: Instance we are trying to solve
    :type instance: Cvrp
    :return: The solution found by sarl
    :rtype: SolutionCvrp
    """

    # Create the list of string (representing customers) for sarl
    customers_sarl: List[str] = instance.customersForSarl()
    # Create the depot as string for sal
    depot_sarl: str = instance.depotForSarl()
    
    # Create the json data to send
    json_data: Dict = {
        "topic": topic, "depot": depot_sarl, "customers": customers_sarl,
        "vehicle_capacity": instance.vehicule_capacity
    }
    
    # Publish the data
    redis_server.publish("sarlTopic", json.dumps(json_data))
    
    return sarlListener(topic=topic, instance=instance)
    

def sarlListener(topic: str, instance: Cvrp) -> Tuple[List[SolutionCvrp], float]:
    """
    sarlListener()
    
    Listen to sarl to get the solution found by it
    
    :param topic: Topic where the result will be published
    :type topic: str
    :param instance: Instance we are trying to solve
    :type instance: Cvrp
    :return: The solution found by sarl
    :rtype: SolutionCvrp
    """
    
    # Create the pub sub on the redis server
    pub_sub = redis_server.pubsub(ignore_subscribe_messages=True)

    # Subscribe to the topic
    pub_sub.subscribe(f"{SARL_SOLUTION_TOPIC}_{topic}")
    
    # Check for new messages
    message = pub_sub.get_message()
    
    # While there's no message on the topic loop
    while message is None:
        # Check for new messages
        message = pub_sub.get_message()
        # Sleep to wait messages
        time.sleep(0.01)
        
    # Decode the binary string into UTF-8
    response_raw: str  = message["data"].decode('UTF-8')
    # Remove all the spaces before and after ,
    response: str = re.sub(r"\s,\s|\s,|,\s", ",", response_raw)
    # Put " "arround the customer strings to then parse it
    response = response.replace(",", "\",\"")
    response = response.replace("[", "[\"")
    response = response.replace("]", "\"]")
    response = response.replace("]\",\"[", "],[")
    response = response.replace("[\"[", "[[")
    response = response.replace("]\"]","]]")
    
    # Parse the string to convert into a List[List[str]]
    response = literal_eval(response)

    # Create a new solution
    solution: SolutionCvrp = SolutionCvrp(instance=instance)
    # Build it with the information returned by sarl
    solution.fromSarl(sarl_response=response)
    
    return [solution], [solution.evaluation()]
    
    
