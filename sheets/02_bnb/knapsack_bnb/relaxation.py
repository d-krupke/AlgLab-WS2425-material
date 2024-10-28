import abc
import typing
from typing import List, Optional

from .instance import Instance


class BranchingDecisions:
    """
    Represents the branching decisions made during the branch and bound algorithm.

    This class provides methods to initialize, access, fix, and split the branching decisions.

    Args:
        length: Number of variables.

    Returns:
        None

    Methods:
        __getitem__(self, index): Get the value at the specified index.
        fix(self, index, value): Fix the value at the specified index.
        length(self): Get the length of the branching decisions. Equals the number of variables and is constant.
        __iter__(self): Iterate over the branching decisions.
        split_on(self, index): Split the branching decisions into two based on the specified index.
    """

    def __init__(self, length) -> None:
        self._assignments: List[Optional[int]] = [None] * length

    def __getitem__(self, item_index: int) -> typing.Optional[int]:
        return self._assignments[item_index]

    def fix(self, item_index: int, value: int) -> None:
        """
        Fixes the usage of an item in the knapsack to the specified value.
        Only do this if you are sure that you do not prohibit the optimal solution.
        """
        assert value in {0, 1}, "Value must be 0 or 1."
        assert self._assignments[item_index] is None, "Item is already fixed."
        self._assignments[item_index] = value

    def copy(self) -> "BranchingDecisions":
        """Create a copy of the branching decisions.

        Returns:
            BranchingDecisions: A copy of the branching decisions.

        Examples:
            >>> decisions = BranchingDecisions(5)
            >>> copy = decisions.copy()
        """
        copy = BranchingDecisions(len(self))
        copy._assignments = self._assignments.copy()
        return copy

    def __len__(self) -> int:
        return len(self._assignments)

    def __iter__(self):
        return iter(self._assignments)

    def split_on(
        self, item_index: int
    ) -> typing.Tuple["BranchingDecisions", "BranchingDecisions"]:
        """Split the branching decisions into two based on the specified item index.

        This method creates two new instances of BranchingDecisions, left and right,
        with the same assignments as the current instance, except for the specified item index.
        The left instance fixes the item to 0, while the right instance fixes it to 1.

        Args:
            item_index: The index of the item to split on.

        Returns:
            Tuple[BranchingDecisions, BranchingDecisions]: The left and right instances of BranchingDecisions. The left instance does not use the item, while the right instance uses it.

        Examples:
            >>> decisions = BranchingDecisions(5)
            >>> left, right = decisions.split_on(2)
        """

        left = BranchingDecisions(len(self))
        right = BranchingDecisions(len(self))
        left._assignments = self._assignments.copy()
        right._assignments = self._assignments.copy()
        left.fix(item_index, 0)
        right.fix(item_index, 1)
        return left, right


class FractionalSolution:
    """
    Represents a fractional solution to the knapsack problem.
    """

    def __init__(self, instance: Instance, selection: typing.List[float]):
        """
        instance: knapsack problem instance
        selection: list of predefined item selections, where 0 means not taken
          and 1 means fully taken, and None means not fixed.
        """
        if len(selection) != len(instance.items):
            msg = "Selection must have same length as items."
            raise ValueError(msg)
        self.instance = instance
        self.selection = selection

    def value(self) -> float:
        """
        Total value of packed items in fractional solution.
        """
        return sum(
            item.value * taken
            for item, taken in zip(self.instance.items, self.selection)
        )

    def weight(self) -> float:
        """
        Total weight of items of fractional solution.
        """
        return sum(
            item.weight * taken
            for item, taken in zip(self.instance.items, self.selection)
        )

    def is_fractionally_feasible(self) -> bool:
        """
        Check if total weight of fractional solution doesn't exceed knapsack capacity.
        """
        return self.weight() <= self.instance.capacity and all(
            0 <= taken <= 1 for taken in self.selection
        )

    def is_integral(self) -> bool:
        """
        Check if all item selections of fractional solution are integers.
        """
        return all(taken == int(taken) for taken in self.selection)

    def __str__(self) -> str:
        return (
            "["
            + "|".join(f"{round(x,1) if x!=int(x) else int(x)}" for x in self.selection)
            + "]"
        )

    def copy(self):
        return FractionalSolution(self.instance, self.selection.copy())


class RelaxationSolver(abc.ABC):
    @abc.abstractmethod
    def solve(
        self, instance: Instance, fixation: BranchingDecisions
    ) -> FractionalSolution:
        """
        Solve the fractional knapsack problem from the given instance and deduced
          fixations.
        instance: knapsack problem instance
        fixation: list of predefined item selections, where 0 means not taken,
            1 means fully taken, and None means not fixed
        """


class BasicRelaxationSolver(RelaxationSolver):
    """
    Solve the fractional knapsack problem from the given instance and branching
    decisions.
    """

    def solve(
        self, instance: Instance, fixation: BranchingDecisions
    ) -> FractionalSolution:
        """
        Solve the fractional knapsack problem from the given instance and deduced
          fixations.
        instance: knapsack problem instance
        fixation: list of predefined item selections, where 0 means not taken,
            1 means fully taken, and None means not fixed
        """
        remaining_capacity = instance.capacity - sum(
            item.weight for item, x in zip(instance.items, fixation) if x == 1
        )
        # Compute solution
        selection = [1.0 if x == 1 else 0.0 for x in fixation]
        remaining_indices = [i for i, x in enumerate(fixation) if x is None]
        remaining_indices.sort(
            key=lambda i: instance.items[i].value / instance.items[i].weight,
            reverse=True,
        )
        for i in remaining_indices:
            # Fill solution with items sorted by value/weight
            if instance.items[i].weight <= remaining_capacity:
                selection[i] = 1.0
                remaining_capacity -= instance.items[i].weight
            else:
                selection[i] = remaining_capacity / instance.items[i].weight
                break  # no capacity left
        assert all(
            x0 == x1 for x0, x1 in zip(fixation, selection) if x0 is not None
        ), "Fixed part is not allowed to change."
        return FractionalSolution(instance, selection)


