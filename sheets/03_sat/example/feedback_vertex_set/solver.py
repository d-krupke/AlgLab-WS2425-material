import logging
import math
from enum import Enum

import networkx as nx  # pip install networkx
from _timer import Timer
from greedy import greedy_fvs
from pysat.solvers import Solver as SATSolver  # pip install python-sat
from util import Node


class _NodeVars:
    """
    The SAT-Solver interface uses integers for variables, with negative integers for negations
    and zero for a false "dummy" variable. Shifting variable management to its own class
    can enhance code cleanliness and reduce errors.
    """

    def __init__(self, graph: nx.Graph, start: int = 1) -> None:
        self._vars = {node: i for i, node in enumerate(graph.nodes, start=start)}
        self._reverse = {i: node for node, i in self._vars.items()}

    def x(self, node: Node):
        """
        Return the variable representing the given node.
        """
        return self._vars[node]

    def node(self, x: int) -> tuple[Node, bool]:
        """
        Return the node represented by the given variable.
        The second return value indicates whether the node is negated.
        """
        if x < 0:
            return self._reverse[x], False
        return self._reverse[x], True

    def not_x(self, node: Node):
        """
        Return the variable representing the negation of the given node.
        """
        return -self.x(node)

    def get_node_selection(self, model: list[int]) -> set[Node]:
        """
        Parse the selected nodes from a given model (solution for a SAT-formula).
        """
        return {self.node(x)[0] for x in model if x in self._reverse}


class FeedbackVertexSetDecisionVariant:
    """
    A SAT-based solver for checking if a given graph contains a Feedback Vertex Set of size k.
    Iteratively used for the optimization to find the smallest feasible k.
    """

    def __init__(
        self, graph: nx.Graph, k: int, logger: logging.Logger | None = None
    ) -> None:
        # Logs are easier to analyze and mange than prints.
        self._logger = logger if logger else logging.getLogger("FVS-SAT")
        self.graph = graph
        self.k = k
        self._logger.info("Building SAT formula for FVS of size %d.", k)
        self.solver = SATSolver("Minicard")
        self.node_vars = _NodeVars(graph)
        self.limit_k(k)
        self._find_and_handle_cycle_basis(graph)
        self._logger.info("SAT formula built.")

    def _find_and_handle_cycle_basis(self, subgraph: nx.Graph) -> int:
        """
        For a given graph (likely a subgraph of self.graph), find the cycle basis,
        add clauses to select at least one node per cycle. A cycle basis, calculable
        in polynomial time, is a set of combinable cycles to construct any graph cycle.
        This method returns the found cycle basis size.
        """
        cycle_list = nx.cycle_basis(subgraph)
        for cycle in cycle_list:
            # at least one node per cycle must be selected (positive variable assignment)
            self.solver.add_clause([self.node_vars.x(v) for v in cycle])
        self._logger.info("Added %d cycle constraints.", len(cycle_list))
        return len(cycle_list)

    def limit_k(self, k: int):
        """
        Update the model in order to enforce a new limit of k selected nodes.
        """
        if k > self.k:
            # Increasing k is not possible without resetting the solver.
            msg = "The new value for k must be smaller than the old value."
            raise ValueError(msg)

        self.solver.add_atmost([self.node_vars.x(v) for v in self.graph.nodes], k)
        self.k = k

    def solve(self, time_limit: float = 900) -> set[Node] | None:
        """
        Determines if a feedback vertex set of <= k vertices exists, returning it or 'None'.
        This is achieved by solving a Cardinality-SAT instance. Constraints:
        - At least one vertex in every cycle must be "selected".
            This constraint is introduced lazily if a cycle remains post-solving.
        - A cardinality constraint allows selection of at most k vertices.
        """
        # As long as the SAT solver returns "satisfiable"
        timer = Timer(time_limit)
        while self.solver.solve():
            timer.check()  # throws TimeoutError if time is up
            # Retrieve the solution from the solver.
            model = self.solver.get_model()
            assert (
                model is not None
            ), "We expect a solution. Otherwise, we would have had a timeout."
            feedback_nodes = self.node_vars.get_node_selection(model)
            # get subgraph induced by the graph excluding the feedback nodes
            subgraph = self.graph.copy()
            subgraph.remove_nodes_from(feedback_nodes)
            # Add constraint to forbid found cycle and solve again.
            # This approach is efficient as the solver continues from its stop point.
            # Fewer constraints lead to simpler, faster solved models despite potential exponential constraints.
            num_cycles = self._find_and_handle_cycle_basis(subgraph)
            if num_cycles == 0:
                # The remaining graph contains no cycles. A valid solution was found!
                self._logger.info("Found FVS of size %d.", self.k)
                return feedback_nodes

        # The SAT-solver proved the formula to be infeasible.
        # This proves that there exists no FVS of size k.
        self._logger.info("No FVS of size %d exists.", self.k)
        return None


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


class FeedbackVertexSetSolverSAT:
    """
    A solver for the Feedback Vertex Set problem that uses a SAT-solver
    to check if a given graph contains a FVS of size k. By iteratively
    trying out different values for k, the smallest FVS is found.
    """

    def __init__(self, graph: nx.Graph, logger: logging.Logger | None = None) -> None:
        # Logs are easier to analyze and mange than prints.
        self._logger = logger if logger else logging.getLogger("FVS-Optimizer")
        self.graph = graph
        self.best_solution = greedy_fvs(graph)
        self.upper_bound = len(self.best_solution)
        self.lower_bound = 0
        self.sat_formula = FeedbackVertexSetDecisionVariant(
            graph, k=len(self.best_solution)
        )

    def _add_solution(self, solution: set[Node]):
        k = len(solution)
        if k < self.upper_bound:
            self._logger.info("A solution of size %d was found!", k)
            self.upper_bound = k
            self.best_solution = solution
            self.sat_formula.limit_k(k)

    def _add_lower_bound(self, lower_bound: int):
        if lower_bound > self.lower_bound:
            self._logger.info("Increased lower bound to %d.", lower_bound)
        self.lower_bound = max(self.lower_bound, lower_bound)

    def _get_next_k(self, search_strategy: SearchStrategy) -> int:
        # The next k to try.
        if search_strategy == SearchStrategy.SEQUENTIAL_UP:
            # Try the smallest possible k.
            k = self.lower_bound
        elif search_strategy == SearchStrategy.SEQUENTIAL_DOWN:
            # Try the smallest possible improvement.
            k = self.upper_bound - 1
        elif search_strategy == SearchStrategy.BINARY_SEARCH:
            # Try a binary search
            k = math.floor((self.lower_bound + self.upper_bound) / 2)
        else:
            msg = "Invalid search strategy!"
            raise ValueError(msg)
        assert self.lower_bound <= k < self.upper_bound
        return k

    def _solve_for_k(self, k: int, timer: Timer) -> set[Node] | None:
        # Check if <=k is feasible.
        if k <= self.sat_formula.k:  # Reuse the SAT-formula if possible
            self.sat_formula.limit_k(k)
        else:
            # If we increase k, we need to reset the model.
            self.sat_formula = FeedbackVertexSetDecisionVariant(self.graph, k=k)
        return self.sat_formula.solve(timer.remaining())

    def solve(
        self,
        time_limit: float = 900,
        search_strategy: SearchStrategy = SearchStrategy.SEQUENTIAL_DOWN,
    ) -> set[Node]:
        """
        Finds the smallest FVS on the given graph.
        """
        self._logger.info("Starting search with upper bound %d.", self.upper_bound)
        timer = Timer(time_limit)  # rough time limit for the whole algorithm
        try:
            while self.lower_bound < self.upper_bound:
                timer.check()  # throws TimeoutError if time is up
                # Tighten the constraints on the model to check
                # whether a smaller solution exists.
                k = self._get_next_k(search_strategy)
                k_limited_fvs = self._solve_for_k(k, timer)
                if k_limited_fvs is None:  # Infeasible!
                    self._add_lower_bound(k + 1)
                else:  # New solution found!
                    self._add_solution(k_limited_fvs)
        except TimeoutError:
            self._logger.info("Timeout reached.")
        return self.best_solution
