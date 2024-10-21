from typing import List

from pydantic import BaseModel


class Donor(BaseModel):
    """
    A class representing a donor in the organ donor problem.

    Attributes:
    - id (int): The unique identifier for the donor.
    """

    id: int

    class Config:
        frozen = True

    def __hash__(self) -> int:
        return hash(self.id)


class Recipient(BaseModel):
    """
    A class representing a recipient in the organ donor problem.

    Attributes:
    - id (int): The unique identifier for the recipient.
    """

    id: int

    class Config:
        frozen = True

    def __hash__(self) -> int:
        return hash(self.id)


class Donation(BaseModel):
    """
    A class representing a donation from a donor to a recipient.

    Attributes:
    - donor (Donor): The organ donor.
    - recipient (Recipient): The receiving patient.
    """

    donor: Donor
    recipient: Recipient

    def __hash__(self) -> int:
        return hash((self.donor, self.recipient))


class Solution(BaseModel):
    """
    A class representing a solution to the crossover transplant problem.

    Attributes:
    - donations (List[Donation]): The list of selected donations between compatible donors and patients.
    """

    donations: List[Donation]
