import typing

from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
    """
    Represents an item with a weight and a value for the knapsack problem.
    """

    weight: int
    value: int

    model_config = ConfigDict(frozen=True)


class Instance(BaseModel):
    """
    Represents an instance with a list of items and capacity of the knapsack problem.
    """

    items: typing.List[Item]
    capacity: int

    model_config = ConfigDict(frozen=True)
