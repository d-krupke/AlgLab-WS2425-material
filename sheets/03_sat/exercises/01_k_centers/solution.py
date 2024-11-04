import math
from typing import Iterable

import networkx as nx
from pysat.solvers import Solver as SATSolver



class KCentersSolver:
    def __init__(self, graph: nx.Graph) -> None:
        """
        Creates a solver for the k-centers problem on the given networkx graph.
        The graph is not necessarily complete, so not all nodes are neighbors.
        The distance between two neighboring nodes is a numeric value (int / float), saved as
        an edge data parameter called "weight".
        There are multiple ways to access this data, and networkx also implements
        several algorithms that automatically make use of this value.
        Check the networkx documentation for more information!
        """
        self.graph = graph
        # TODO: Implement me!

    def solve_heur(self, k: int) -> list[int]:
        """
        Calculate a heuristic solution to the k-centers problem.
        Returns the k selected centers as a list of ints.
        (nodes will be ints in the given graph).
        """
        # TODO: Implement me!
        centers = None
        return centers


    def solve(self, k: int) -> list[int]:
        """
        For the given parameter k, calculate the optimal solution
        to the k-centers solution and return the selected centers as a list.
        """
        sat = SATSolver("MiniCard")
        centers = self.solve_heur(k)

        # TODO: Implement me!

        return centers
