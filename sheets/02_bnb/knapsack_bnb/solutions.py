import typing

from .relaxation import FractionalSolution


class SolutionSet:
    """
    Store feasible found solutions,
    determine and keep track the best solution among them.
    """

    def __init__(self) -> None:
        self._best_solution = None
        self._solutions = []

    def add(self, solution: FractionalSolution) -> None:
        """
        Add a feasible and integral solution to the solution set and
        update the best solution if necessary.
        """
        assert solution.is_fractionally_feasible()
        assert solution.is_integral()
        if solution not in self._solutions:
            self._solutions.append(solution)
        if not self._best_solution or solution.value() > self._best_solution.value():
            self._best_solution = solution

    def best_solution_value(self) -> float:
        """
        Get the value of the best solution in the solution set.
        -inf if no solution is available.
        """
        return self._best_solution.value() if self._best_solution else float("-inf")

    def best_solution(self) -> typing.Optional[FractionalSolution]:
        """
        Get the best solution in the solution set.
        """
        return self._best_solution
