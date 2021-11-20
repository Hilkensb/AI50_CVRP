#!/usr/bin/env python3
# Standard Library
import argparse
import sys
from test.unittestrunner import runTest
from typing import List, Dict, Tuple, Union

# Modules
from gui import config


def getOptions(args: List[str]):
    """
    """
    
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
    config.SHOW_SOLUTION = options.show_evolution
        

