#!/usr/bin/env python3
import abc
from typing import Tuple


class nodeWithCoord(abc.ABC):
    """
    """

    @abc.abstractclassmethod
    def getCoordinates(self) -> Tuple[int, int]:
        """
        """
        pass
