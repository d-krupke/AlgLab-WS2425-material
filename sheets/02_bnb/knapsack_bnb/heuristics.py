import math
import typing
from abc import ABC, abstractmethod

from .bnb_nodes import BnBNode, FractionalSolution
from .instance import Instance


class Heuristics(ABC):
    """
    Abstract base class for heuristics.
    """

    @abstractmethod
    def search(
        self, instance: Instance, node: BnBNode
    ) -> typing.Iterable[FractionalSolution]:
        """
        Abstract method to search for a feasible solution.
        """


