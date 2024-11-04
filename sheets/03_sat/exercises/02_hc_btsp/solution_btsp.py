import math
from enum import Enum

import networkx as nx
from _timer import Timer
from solution_hamiltonian import HamiltonianCycleModel


class SearchStrategy(Enum):
    """
    Different search strategies for the solver.
    """

    SEQUENTIAL_UP = 1  # Try smallest possible k first.
    SEQUENTIAL_DOWN = 2  # Try any improvement.
    BINARY_SEARCH = 3  # Try a binary search for the optimal k.

    def __str__(self):
        return self.name.title()

    @staticmethod
    def from_str(s: str):
        return SearchStrategy[s.upper()]


class BottleneckTSPSolver:
    def __init__(self, graph: nx.Graph) -> None:
        """
        Creates a solver for the Bottleneck Traveling Salesman Problem on the given networkx graph.
        You can assume that the input graph is complete, so all nodes are neighbors.
        The distance between two neighboring nodes is a numeric value (int / float), saved as
        an edge data parameter called "weight".
        There are multiple ways to access this data, and networkx also implements
        several algorithms that automatically make use of this value.
        Check the networkx documentation for more information!
        """
        self.graph = graph
        # TODO: Implement me!

    def lower_bound(self) -> float:
        # TODO: Implement me!

    def optimize_bottleneck(
        self,
        time_limit: float = math.inf,
        search_strategy: SearchStrategy = SearchStrategy.BINARY_SEARCH,
    ) -> list[tuple[int, int]] | None:
        """
        Find the optimal bottleneck tsp tour.
        """

        self.timer = Timer(time_limit)
        # TODO: Implement me!
