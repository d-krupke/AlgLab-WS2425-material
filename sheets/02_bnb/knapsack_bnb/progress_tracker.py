from .bnb_nodes import BnBNode, NodeStatus
from .instance import Instance
from .relaxation import FractionalSolution
from .search_strategy import SearchStrategy
from .solutions import SolutionSet
from .visualization import BnBVisualization


class ProgressTracker:
    """
    Track and report various statistical information related to the branch-and-bound search.
    """

    def __init__(
        self,
        instance: Instance,
        search_strategy: SearchStrategy,
        solutions: SolutionSet,
    ) -> None:
        self.search_strategy = search_strategy
        self.solutions = solutions
        self._current_node = None
        self._heuristic_solutions = []
        self.num_nodes = 0
        self.num_iterations = 0
        self._vis = BnBVisualization(instance)

    def upper_bound(self) -> float:
        """
        Get maximum solution value of nodes in priority queue, if the queue isn't empty;
        otherwise, the best solution value in the solution set.
        """
        if (ub := self.search_strategy.upper_bound()) is not None:
            return max(ub, self.solutions.best_solution_value())
        if (best_solution := self.solutions.best_solution()) is not None:
            return best_solution.value()
        return float("inf")

    def lower_bound(self) -> float:
        """
        Get the best solution value in the solution set,
        """
        return self.solutions.best_solution_value()

    def on_new_node_in_tree(self, node: BnBNode) -> None:
        """
        Report the creation of a new node in the search tree.
        """
        self.num_nodes += 1
        self._vis.on_new_node_in_tree(node)

    def on_heuristic_solution(
        self, node: BnBNode, solution: FractionalSolution
    ) -> None:
        """
        Report the discovery of a new solution by the heuristics.
        """
        if solution.value() < self.solutions.best_solution_value():
            return
        self._heuristic_solutions.append(solution)
        print(
            f"\tNew solution found by heuristics: {solution} of value {solution.value()}"
        )

    def start_search(self):
        print(
            "Nodes: The number of nodes processed so far of the number of nodes created."
        )
        print("Depth: The depth of the current node in the search tree.")
        print("Status: The status of the current node.")
        print("Value: The value of the current node.")
        print("UB: The upper bound after processing the node.")
        print("LB: The lower bound after processing the node.")
        print()
        print("     Nodes      Depth   Status        Value         UB         LB")

    def start_iteration(self, node: BnBNode):
        self._current_node = node
        self.num_iterations += 1

    def end_iteration(self, status: NodeStatus):
        # self.vis.on_node_processed(node, lb=self.progress_tracker.lower_bound(), ub=self.progress_tracker.upper_bound(), best_solution= self.solutions.best_solution())
        """
        Print the progress information of the search process, which
        includes the explored nodes number,the created nodes number,
        the depth and status of the current node,
        the upper bound, and the lower bound.
        """
        assert self._current_node is not None, "No current node."
        num_nodes = self.num_nodes
        num_nodes_in_queue = len(self.search_strategy)
        num_nodes_explored = num_nodes - num_nodes_in_queue
        last_node_value = (
            round(self._current_node.relaxed_solution.value(), 3)
            if self._current_node
            else "-"
        )
        last_node_depth = self._current_node.depth if self._current_node else "-"
        last_node_status = status.value
        upper_bound = round(self.upper_bound(), 3)
        lower_bound = round(self.lower_bound(), 3)
        print(
            f"{f'{num_nodes_explored}/{num_nodes}':>10} {last_node_depth:>10} {last_node_status:>10} {last_node_value:>10} {upper_bound:>10} {lower_bound:>10}"
        )
        self._vis.on_node_processed(
            self._current_node,
            lb=lower_bound,
            ub=upper_bound,
            best_solution=self.solutions.best_solution(),
            heuristic_solutions=self._heuristic_solutions,
        )
        self._current_node = None
        self._heuristic_solutions = []

    def end_search(self):
        print()
        print(
            f"Search finished in {self.num_iterations} iterations and {self.num_nodes} created nodes."
        )
        print(
            f"The optimal solution is {self.solutions.best_solution()} with value {self.solutions.best_solution_value()}."
        )
        self._vis.visualize()
