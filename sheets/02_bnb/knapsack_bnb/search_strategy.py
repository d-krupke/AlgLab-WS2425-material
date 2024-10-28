import queue
import typing

from .bnb_nodes import BnBNode


class SearchStrategy:
    """
    Manage the nodes of branch-and-bound search tree with priority queue.
    """

    def __init__(self, priority: typing.Callable[[BnBNode], typing.Any]) -> None:
        """Initialize the SearchStrategy.

        This method initializes an instance of the SearchStrategy class with the given priority function.

        Args:
            priority: A callable that takes a BnBNode object as input and returns a value used for priority.

        Returns:
            None

        Examples:
            # Higher solution values have higher priority
            >>> priority_func = lambda node: -node.relaxed_solution.value()
            # Nodes at lower depths have higher priority
            >>> priority_func = lambda node: node.depth
            # First sort for depth, then for solution value
            >>> priority_func = lambda node: (node.depth, -node.relaxed_solution.value())
            >>> strategy = SearchStrategy(priority_func)
        """

        self.queue = queue.PriorityQueue()
        self._priority = priority

    def enqueue(self, node: BnBNode) -> None:
        """
        Add a node to the priority queue.
        """
        self.queue.put((self._priority(node), node))

    def next(self) -> BnBNode:
        """
        Get the next node from the priority queue.
        """
        if self.has_next():
            return self.queue.get()[1]
        msg = "No more nodes to explore."
        raise ValueError(msg)

    def __len__(self) -> int:
        """
        Get the number of nodes in the priority queue.
        """
        return self.queue.qsize()

    def nodes_in_queue(self) -> typing.Iterable[BnBNode]:
        """
        Get a iterable of nodes in the priority queue.
        """
        return (node for _, node in self.queue.queue)

    def has_next(self) -> bool:
        """
        Check if there are more nodes to explore in the priority queue.
        """
        return not self.queue.empty()

    def upper_bound(self) -> float:
        """
        Get the maximum solution value of nodes in the priority queue.

        CAVEAT: This is the upper bound for the solution value of the nodes in the priority queue. Not
        the upper bound for the whole search. To get the true upper bound of the search, use the
        maximum of this upper bound and the largest feasible solution.
        """
        if not self.has_next():
            return float("-inf")
        return max(
            (
                n
                for n in self.nodes_in_queue()
                if n.relaxed_solution.is_fractionally_feasible()
            ),
            key=lambda node: node.relaxed_solution.value(),
        ).relaxed_solution.value()
