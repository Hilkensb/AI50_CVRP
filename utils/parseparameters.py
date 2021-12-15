#!/usr/bin/env python3
# Standard Library
import argparse
import sys
from test.unittestrunner import runTest
from typing import List, Dict, Tuple, Union
import json
import os
from sys import platform
import subprocess

# Others library
# To color text in terminal
from colorama import Fore, Back, Style

# Modules
from gui import config
from utils.redisutils import isRedisAvailable


# Show or not solution on loading page
# If not showed it will improved time cost of the algorithms
SHOW_SOLUTION: bool = bool(int(config.redis_server.get('SHOW_SOLUTION').decode("UTF-8"))) if isRedisAvailable() and config.redis_server.get('SHOW_SOLUTION') is not None else config.SHOW_SOLUTION

def getOptions(args: List[str]):
    """
    """
    
    # Check if redis is available
    if not isRedisAvailable():
        # Display a warning message
        print(Fore.YELLOW + "/!\ WARNING: Redis server is not available for the application. Some functionnalities will not work." + Style.RESET_ALL)
        
        # If we should launch redis 
        if config.AUTO_LAUNCH_REDIS:
            # Check the os
            # If it's windows
            if platform == "win32":
                # Run redis server
                subprocess.Popen(os.path.join(config.WINDOWS_REDIS_FOLDER, "redis-server.exe"))
                print(Fore.GREEN + "Redis has been launched." + Style.RESET_ALL)
            elif platform == "linux":
                # Run redis server
                subprocess.Popen(os.path.join(UNIX_REDIS_FOLDER, "redis-server"))
                print(Fore.GREEN + "Redis has been launched." + Style.RESET_ALL)
            else:
               print(Fore.RED + "/!\ ERRROR: Functionnality unavailable for your os. You need to launch redis manually." + Style.RESET_ALL)
    
    # Create a parser
    parser = argparse.ArgumentParser(description="Command.")
    # Add an argument
    parser.add_argument("-t", "--unittest",dest='test',action='store_true', help="Run unit test before running the application.")
    parser.add_argument("-s", "--show_evolution", dest='show_evolution',action='store_true', help="Display the current solution on the load page.")


    # Store all the inputs
    options = parser.parse_args(args)

    # Run test
    if options.test:
        runTest()
        
    # Show evolution
    if options.show_evolution:
        config.redis_server.set('SHOW_SOLUTION',  1 if options.show_evolution else 0)
    else:
        config.redis_server.set('SHOW_SOLUTION', 1 if config.SHOW_SOLUTION else 0)

