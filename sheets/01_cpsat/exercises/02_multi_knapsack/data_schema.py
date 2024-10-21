from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, NonNegativeInt, model_validator


class Item(BaseModel):
    """
    A class representing an item with a value and weight.
    """

    value: NonNegativeInt = Field(
        description="The value of the item. The value of the packed items in a knapsack should be maximized."
    )
    weight: NonNegativeInt = Field(
        description="The weight of the item. The weight of the packed items in a knapsack must not exceed the knapsack's capacity."
    )
    toxic: bool = Field(
        default=False,
        description="Whether the item is toxic. A toxic item cannot be packed with a non-toxic item.",
    )
    id: UUID = Field(
        default_factory=uuid4,
        alias="_id",
        description="A unique identifier for the item.",
    )

    class Config:
        frozen = True


class Instance(BaseModel):
    """
    A class representing an instance of the multi-knapsack problem.
    """

    items: List[Item] = Field(
        description="A list of the items to be packed into the knapsacks."
    )
    capacities: List[int] = Field(
        description="A list of the knapsack capacities. The first capacity is for the first knapsack, the second capacity for the second knapsack, and so on. It implicitly defines the number of knapsacks."
    )


class Solution(BaseModel):
    """
    A class representing a solution to the multi-knapsack problem.
    """

    trucks: List[List[Item]] = Field(
        description="A list of lists of items, representing the items in each knapsack. The first list represents the items in the first knapsack, the second list the items in the second knapsack, and so on."
    )

    # Some basic model validation to make sure there are no trivial errors.
    @model_validator(mode="after")
    def _items_only_in_one_knapsack(self):
        """
        Ensure that each item is only in one knapsack.
        """
        already_packed_items = set()
        for truck in self.trucks:
            for item in truck:
                assert (
                    item.id not in already_packed_items
                ), f"Item {item.id} is in more than one truck!"
                already_packed_items.add(item.id)
        return self
