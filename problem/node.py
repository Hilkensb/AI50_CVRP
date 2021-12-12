#!/usr/bin/env python3
import abc
from typing import Tuple


class NodeWithCoord(abc.ABC):
    """
    Node Interface for nodes of vrp problem with coordinates
    """

    @abc.abstractclassmethod
    def getCoordinates(self) -> Tuple[int, int]:
        """
        get coordinates
        
        Abstract Method to ensure that every node that inherated of this
        class can return their coordinates has a tuple of int
        
        :return: Tuple of x, y coordinates
        :rtype: tuple[int, int]
        """
        pass

    @abc.abstractclassmethod
    def toJSON(self):
        """
        toJSON()
        
        Abstract Method to ensure that every node that inherated of this
        class can return a json of theirselvess
        """
        pass
