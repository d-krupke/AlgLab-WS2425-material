import typing
from abc import ABC, abstractmethod

from .bnb_nodes import BnBNode, BranchingDecisions


class BranchingStrategy(ABC):
    """
    Abstract base class for creating decision branches based on the fractional solution of a given node.
    """

    @abstractmethod
    def make_branching_decisions(
        self, node: BnBNode
    ) -> typing.Iterable[BranchingDecisions]:
        """
        Abstract method for making branching decisions.
        """


