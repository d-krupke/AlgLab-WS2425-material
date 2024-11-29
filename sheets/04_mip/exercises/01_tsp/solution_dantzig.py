"""
Implement the Dantzig-Fulkerson-Johnson formulation for the TSP.
"""

import logging
import typing

import gurobipy as gp
import networkx as nx




class GurobiTspSolver:
    """
    IMPLEMENT ME!
    """

    def __init__(self, G: nx.Graph, k: int = 2):
        """
        G is a weighted networkx graph, where the weight of an edge is stored in the
        "weight" attribute. It is strictly positive.
        """
        self.graph = G
        assert (
            G.number_of_edges() == G.number_of_nodes() * (G.number_of_nodes() - 1) / 2
        ), "Invalid graph"
        assert all(
            weight > 0
            for _, _, weight in G.edges.data("weight", default=None)  # type: ignore[attr-defined]
        ), "Invalid graph"
        assert k in {1, 2}, "Invalid k"
        self.k = k
        logging.info("Creating model ...")
        logging.info(
            "Graph has %d nodes and %d edges", G.number_of_nodes(), G.number_of_edges()
        )
        logging.info("Implementing subtour elimination with >= %d", k)
        self._model = gp.Model()
        # TODO: Implement me!


    def get_lower_bound(self) -> float:
        """
        Return the current lower bound.
        """
        # TODO: Implement me!

    def get_solution(self) -> typing.Optional[nx.Graph]:
        """
        Return the current solution as a graph.
        """
        # TODO: Implement me!

    def get_objective(self) -> typing.Optional[float]:
        """
        Return the objective value of the last solution.
        """
        # TODO: Implement me!

    def solve(self, time_limit: float, opt_tol: float = 0.001) -> None:
        """
        Solve the model. After solving the model, the solution, its objective value,
        and the lower bounds should be available via the corresponding methods.
        """
        logging.info("Solving model ...")
        # Set parameters for the solver.
        self._model.Params.LogToConsole = 1
        self._model.Params.TimeLimit = time_limit
        self._model.Params.LazyConstraints = 1
        self._model.Params.MIPGap = (
            opt_tol  # https://www.gurobi.com/documentation/11.0/refman/mipgap.html
        )

        # ...
        # TODO: Implement me!

