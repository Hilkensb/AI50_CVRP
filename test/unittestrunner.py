#!/usr/bin/env python3
# Standard Library
import unittest
import os


def runTest():
    """
    Function to run the unittest
    """

    # Load the unittest
    loader = unittest.TestLoader()
    # Set the directory where the test are
    start_dir = os.getcwd()
    # Load all tests
    suite = loader.discover(start_dir)

    # Initialize them
    runner = unittest.TextTestRunner()
    # run the test
    runner.run(suite)
