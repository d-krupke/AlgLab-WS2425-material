from pydantic import (
    BaseModel,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveInt,
    model_validator,
)

LocationId = NonNegativeInt


class Tunnel(BaseModel):
    """
    This class represents a tunnel connecting two locations. Tunnels are undirected.
    Your instance should only contain one tunnel between two locations.
    """

    source: LocationId = Field(
        ...,
        description="The ID of the start location of the tunnel. Note that tunnels are undirected, i.e., they can also be used from target to source. However, you have to decide for one direction in your solution, as it cannot be used in both directions at the same time.",
    )
    target: LocationId = Field(
        ...,
        description="The ID of the end location of the tunnel. Note that tunnels are undirected, i.e., they can also be used from target to source. However, you have to decide for one direction in your solution, as it cannot be used in both directions at the same time.",
    )
    throughput_per_hour: NonNegativeInt = Field(
        ..., description="The maximum throughput of the tunnel per hour."
    )
    reinforcement_costs: NonNegativeFloat = Field(
        ..., description="The cost of reinforcing the tunnel."
    )

    model_config = {"frozen": True}

    @model_validator(mode="after")
    def _validate_tunnel(self):
        if self.source == self.target:
            msg = "The tunnel must connect two different locations."
            raise ValueError(msg)
        return self


class Mine(BaseModel):
    """
    This class represents a mine in the mining problem.
    """

    location: LocationId = Field(..., description="The unique identifier of the mine.")
    ore_per_hour: NonNegativeInt = Field(
        ..., description="The amount of ore produced by the mine per hour."
    )

    model_config = {"frozen": True}


class Instance(BaseModel):
    """
    This class represents an instance of the Mining Problem,
    """

    locations: list[LocationId] = Field(..., description="List of all locations.")
    tunnels: list[Tunnel] = Field(..., description="List of all tunnels.")
    elevator_location: LocationId = Field(..., description="The ID of the elevator.")
    mines: dict[LocationId, Mine] = Field(
        ..., description="List of all mines. Each location has at most one mine."
    )
    budget: NonNegativeFloat = Field(..., description="The budget for the instance.")

    model_config = {"frozen": True}

    @model_validator(mode="after")
    def _validate_locations(self):
        # check that the instance is valid
        if self.elevator_location not in self.locations:
            msg = "The elevator location must be one of the locations."
            raise ValueError(msg)
        assert all(
            t.source in self.locations and t.target in self.locations
            for t in self.tunnels
        ), "All tunnel endpoints must be locations."
        assert all(
            m.location in self.locations for m in self.mines.values()
        ), "All mine locations must be locations."
        assert all(
            m.location == location for location, m in self.mines.items()
        ), "Location of mine should match the key"
        return self


class Solution(BaseModel):
    """
    This class represents the solution to an Instance.

    Attributes:
        flow: List of utilized edges (directed) and their utilization.
            Each entry is a tuple:
            - A directed edge (a tuple of two IDs).
            - The utilization of that edge (must be > 0).
    """

    flow: list[tuple[tuple[LocationId, LocationId], PositiveInt]] = Field(
        ..., description="List of utilized edges and their utilization."
    )

    model_config = {"frozen": True}
