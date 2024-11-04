import itertools

import networkx as nx
from pysat.solvers import Solver as SATSolver


class HamiltonianCycleModel:
    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph
        self.solver = SATSolver("Minicard")
        self.assumptions = []
        # TODO: Implement me!


    def solve(self) -> list[tuple[int, int]] | None:
        """
        Solves the Hamiltonian Cycle Problem. If a HC is found,
        its edges are returned as a list.
        If the graph has no HC, 'None' is returned.
        """
        # TODO: Implement me!
