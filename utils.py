from typing import NamedTuple
from abc import ABC, abstractmethod

class VerboseECInfo(NamedTuple):
    ec: list[set[int]]
    homogeneity: list[set[int]]
    segregation: list[set[int]]
    reinforcement: list[set[int]]

class NetworkWrapper(ABC):
    def __init__(self, G):
        super().__init__()
        self.G = G

    def getComponents(self, algorithm) -> list[set[int]]:
        """
        Returns the list of components identified by given algorithm.

        Params:
            algorithm (str): algorithm to be applied.
                Following options are available: scc (strongly connected components);
                wcc (weakly connected components);
                cnm (greedy modularity maximization by Clauset et al. (2004)).
        
        Raises:
            ValueError: if unknown algorithm is passed
        
        Returns:
            list[set[int]]: the list of the components (set of int) identified by 
                the given algorithm.
        """
        if algorithm == 'scc':
            return self.getSCC()
        elif algorithm == 'wcc':
            return self.getWCC()
        elif algorithm == 'cnm':
            return self.getCNM()
        else:
            raise ValueError(f'Component detection algorithm {algorithm} is not defined')

    @abstractmethod
    def getSCC(self) -> list[set[int]]:
        """
        Get the list of strongly connected components.
        """
        pass

    @abstractmethod
    def getWCC(self) -> list[set[int]]:
        """
        Get the list of weakly connected components.
        """
        pass

    @abstractmethod
    def getCNM(self):
        """
        Get the list of components identified by 
        the greedy modularity community detection by Clauset et al. (2004).
        If self.G is a directed graph, it should be transformed into the undirected one
        before applying this method.
        """
        pass

    @abstractmethod
    def getEdgesBetween(self, sources, targets=None):
        """
        Get the list of edges whose sources are in 'sources' and targets are in 'targets'.
        If 'targets' are None, edges which start from 'sources' are listed regardless of their targets.
        """
        pass

def hamming(b1: str, b2: str) -> int:
    ## Return the Hamming distance between two beliefs `b1` and `b2`.
    return sum([x1 != x2 for (x1, x2) in zip(b1, b2)])

def is_decreasing(xs: list[float]) -> bool:
    ## Returns `True` if xs[0] >= xs[1] >= ... >= xs[-1]; returns `False` otherwise.
    for i in range(1, len(xs)):
        if xs[i-1] < xs[i]:
            return False
    return True