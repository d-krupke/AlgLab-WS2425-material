from typing import List

from pydantic import BaseModel, Field, model_validator


class Instance(BaseModel):
    numbers: List[int] = Field(
        description="A list of numbers", examples=[[1, 2, 3, 4, 5]]
    )


class Solution(BaseModel):
    number_a: int = Field(description="First selected number")
    number_b: int = Field(description="Second selected number")
    distance: int = Field(description="The distance between the two selected numbers")

    # This is a model validator that will directly complain if the solution is inconsistent.
    @model_validator(mode="after")
    def _validate_distance(self):
        assert self.distance == abs(
            self.number_a - self.number_b
        ), "The distance is not correct."
        return self
