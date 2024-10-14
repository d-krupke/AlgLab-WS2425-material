"""
This module defines the data schema for the network placement problem.
By defining strict data schemas, we simplify the development as it is clearly defined what data is expected.
"""

# pip install pydantic
from pydantic import BaseModel, Field


class DirectConnection(BaseModel):
    """
    A direct connection between two endpoints in the network.
    As the network is undirected, the order of the endpoints does not matter.
    The network, thus, should not contain both (A, B) and (B, A), as they are the same connection.
    """

    endpoint_a: str = Field(
        ...,
        description="The first endpoint in the connection. As the order does not matter, it can be swapped with endpoint_b.",
    )
    endpoint_b: str = Field(
        ...,
        description="The second endpoint in the connection. As the order does not matter, it can be swapped with endpoint_a.",
    )
    distance: int = Field(..., description="The distance between the two endpoints.")


class ProblemInstance(BaseModel):
    """
    Represents a problem instance of the network placement problem.
    """

    endpoints: list[str] = Field(..., description="A list of endpoints in the network.")
    connections: list[DirectConnection] = Field(
        ..., description="A list of direct connections between endpoints."
    )
    approved_endpoints: list[str] = Field(
        ..., description="A list of endpoints that are approved for placement."
    )
    min_distance_between_placements: int = Field(
        ..., description="The minimum distance between any two placements."
    )


class Solution(BaseModel):
    """
    Represents a solution to the network placement problem.
    """

    selected_placements: list[str] = Field(
        ...,
        description="A list of endpoints that are selected for placement. Have to be a subset of approved_endpoints.",
    )
