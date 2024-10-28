"""
A simple implementation of the branch and bound algorithm for the knapsack problem.
It is primarily intended to illustrate the algorithm and not optimized for efficiency.
It is modular such that the performance difference between different strategies can be
explored. All strategies will be exponential in the worst case, but some strategies
will still result in significantly smaller branch and bound trees than others.
"""

import typing

from .bnb_nodes import BnBNode, NodeFactory, NodeStatus
from .branching_strategy import BranchingStrategy
from .heuristics import Heuristics
from .instance import Instance
from .progress_tracker import ProgressTracker
from .relaxation import FractionalSolution, RelaxationSolver
from .search_strategy import SearchStrategy
from .solutions import SolutionSet


class BnBSearch:
    """
    Perform the branch-and-bound search to determine the fractional solution for
    a specified instance of the knapsack problem.
    """

    def __init__(
        self,
        instance: Instance,
        relaxation: RelaxationSolver,
        search_strategy: SearchStrategy,
        branching_strategy: BranchingStrategy,
        heuristics: Heuristics,
    ) -> None:
        """
        instance: knapsack problem instance
        relaxation: An efficient relaxation solver for the knapsack problem
        search_strategy: A strategy for managing the unprocessed nodes of the search tree, especially
            the order in which they are processed.
        branching_strategy: A strategy for creating decision branches based on the fractional solution
            of a node.
        """
        self.instance = instance

        self.relaxation = relaxation
        self.search_strategy = search_strategy
        self.branching_strategy = branching_strategy
        self.heuristics = heuristics
        self.solutions = SolutionSet()
        self.progress_tracker = ProgressTracker(
            instance, self.search_strategy, self.solutions
        )
        self.node_factory = NodeFactory(
            instance, relaxation, on_new_node=self.progress_tracker.on_new_node_in_tree
        )

    def _process_node(self, node: BnBNode) -> NodeStatus:
        if not node.relaxed_solution.is_fractionally_feasible():
            node.status = NodeStatus.INFEASIBLE
            return node.status  # infeasibility prune
        if node.relaxed_solution.value() <= self.solutions.best_solution_value():
            node.status = NodeStatus.PRUNED
            return node.status  # suboptimality prune
        if node.relaxed_solution.is_integral():
            # update best solution
            self.solutions.add(node.relaxed_solution)
            node.status = NodeStatus.FEASIBLE
            return node.status  # integral solution
        # try to find solutions using heuristics
        for heur_sol in self.heuristics.search(self.instance, node):
            assert heur_sol.is_fractionally_feasible(), "Heuristic solution is feasible"
            assert heur_sol.is_integral(), "Heuristic solution is integral"
            self.solutions.add(heur_sol)
            self.progress_tracker.on_heuristic_solution(node, heur_sol)
        # branch on a non-integer variable
        for decisions in self.branching_strategy.make_branching_decisions(node):
            child = self.node_factory.create_child(node, decisions)
            self.search_strategy.enqueue(child)
            child.status = NodeStatus.ENQUEUED
        node.status = NodeStatus.BRANCHED
        return node.status

    def search(
        self, iteration_limit: int = 10_000
    ) -> typing.Optional[FractionalSolution]:
        """
        Perform a branch-and-bound search to find the optimal fractional solution
        for the knapsack problem instance.
        """
        # the branch-and-bound search start from the root node and
        # continue until the search strategy has no more nodes to explore.
        root = self.node_factory.create_root()
        self.search_strategy.enqueue(root)
        self.progress_tracker.start_search()
        while self.search_strategy.has_next():
            node = self.search_strategy.next()
            self.progress_tracker.start_iteration(node)
            status = self._process_node(node)
            self.progress_tracker.end_iteration(status)
            if (
                self.search_strategy.upper_bound()
                <= self.solutions.best_solution_value()
            ):
                # prune the rest of the tree as it cannot contain a better solution
                break
            if (iteration_limit := iteration_limit - 1) <= 0:
                # make sure we don't run forever
                msg = "Iteration limit reached"
                raise ValueError(msg)
        self.progress_tracker.end_search()
        return self.solutions.best_solution()
