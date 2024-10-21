from abc import ABC as AbstractClass
from typing import List

from data_schema import Donor, Recipient


class TransplantDatabase(AbstractClass):
    """
    This abstract class defines an interface to the database API.
    There is a concrete implementation in _db_impl.py (that you do not need to worry about).
    Use this API to interact with the recipient/donor data
    """

    def __init__(self) -> None:
        pass

    def get_all_donors(self) -> List[Donor]:
        """
        Get all registered donors from the database.
        """
        raise NotImplementedError("This is an abstract class!")

    def get_all_recipients(self) -> List[Recipient]:
        """
        Get all registered patients from the database.
        """
        raise NotImplementedError("This is an abstract class!")

    def get_compatible_donors(self, recipient: Recipient) -> List[Donor]:
        """
        For a given recipient, get (calculate) a list of all compatible donors,
        that are registered in the database.
        """
        raise NotImplementedError("This is an abstract class!")

    def get_compatible_recipients(self, donor: Donor) -> List[Recipient]:
        """
        For a given donor, get (calculate) a list of all compatible recipients,
        that are registered in the database.
        """
        raise NotImplementedError("This is an abstract class!")

    def get_partner_donors(self, recipient: Recipient) -> List[Donor]:
        """
        For a given recipient, find the associated representative donor(s).
        Even if only one donor is registered as the partner of the given
        donor, a list is returned.
        """
        raise NotImplementedError("This is an abstract class!")

    def get_partner_recipient(self, donor: Donor) -> Recipient:
        """
        For a given donor, find the represented recipient.
        """
        raise NotImplementedError("This is an abstract class!")
