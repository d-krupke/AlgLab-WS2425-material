import sqlite3
from pathlib import Path
from typing import List

from database import Donor, Recipient, TransplantDatabase


class SqliteTransplantDatabase(TransplantDatabase):
    """
    This is a concrete implementation of the TransplantDatabase interface,
    which fetches the data from an underlying sqlite3 database.
    """

    def __init__(self, path: str) -> None:
        if not Path(path).exists():
            msg = f"File {path} does not exist!"
            raise FileNotFoundError(msg)
        self.dbcon = sqlite3.connect(path)

    def get_all_donors(self) -> List[Donor]:
        """
        Get all registered donors from the database.
        """
        cur = self.dbcon.cursor()
        cur.row_factory = sqlite3.Row  # type: ignore[attr-defined]
        cur.execute("SELECT id, represents FROM donors")
        return [Donor(id=row["id"]) for row in cur.fetchall()]

    def get_all_recipients(self) -> List[Recipient]:
        """
        Get all recipients from the database.
        """
        cur = self.dbcon.cursor()
        cur.row_factory = sqlite3.Row  # type: ignore[attr-defined]
        cur.execute("SELECT id FROM recipients")
        return [Recipient(id=row["id"]) for row in cur.fetchall()]

    def get_compatible_donors(self, recipient: Recipient) -> List[Donor]:
        """
        For a given recipient, get (calculate) a list of all compatible donors,
        that are registered in the database.

        This is calculated using a SQL query, using blood types and tissue types
        from the database schema.
        """

        cur = self.dbcon.cursor()
        cur.row_factory = sqlite3.Row  # type: ignore[attr-defined]
        cur.execute(
            """
            SELECT d.id
            FROM donors AS d
            JOIN recipients AS r ON d.tissue_type = r.tissue_type AND (
                CASE
                    WHEN d.blood_type = 'A' THEN r.blood_type IN ('A', 'AB')
                    WHEN d.blood_type = 'B' THEN r.blood_type IN ('B', 'AB')
                    WHEN d.blood_type = 'AB' THEN r.blood_type = 'AB'
                    WHEN d.blood_type = 'O' THEN 1  -- 'O' can donate to any blood type
                    ELSE 0  -- Handle other cases if needed
                END
            )
            WHERE r.id = ?
            """,
            (int(recipient.id),),
        )
        return [Donor(id=row["id"]) for row in cur.fetchall()]

    def get_compatible_recipients(self, donor: Donor) -> List[Recipient]:
        """
        For a given donor, get (calculate) a list of all compatible recipients,
        that are registered in the database.

        This is calculated using a SQL query, using blood types and tissue types
        from the database schema.
        """

        cur = self.dbcon.cursor()
        cur.row_factory = sqlite3.Row  # type: ignore[attr-defined]
        cur.execute(
            """
            SELECT r.id
            FROM donors AS d
            JOIN recipients AS r ON d.tissue_type = r.tissue_type AND (
                CASE
                    WHEN d.blood_type = 'A' THEN r.blood_type IN ('A', 'AB')
                    WHEN d.blood_type = 'B' THEN r.blood_type IN ('B', 'AB')
                    WHEN d.blood_type = 'AB' THEN r.blood_type = 'AB'
                    WHEN d.blood_type = 'O' THEN 1  -- 'O' can donate to any blood type
                    ELSE 0  -- Handle other cases if needed
                END
            )
            WHERE d.id = ?
            """,
            (int(donor.id),),
        )
        return [Recipient(id=row["id"]) for row in cur.fetchall()]

    def get_partner_donors(self, recipient: Recipient) -> List[Donor]:
        """
        For a given recipient, find the associated representative donor(s).
        Even if only one donor is registered as the partner of the given
        donor, a list is returned.
        """

        cur = self.dbcon.cursor()
        cur.row_factory = sqlite3.Row  # type: ignore[attr-defined]
        cur.execute(
            "SELECT id FROM donors WHERE represents = ?",
            (int(recipient.id),),
        )
        return [Donor(id=row["id"]) for row in cur.fetchall()]

    def get_partner_recipient(self, donor: Donor) -> Recipient:
        """
        For a given donor, find the represented recipient.
        """

        cur = self.dbcon.cursor()
        cur.row_factory = sqlite3.Row  # type: ignore[attr-defined]
        cur.execute(
            """
            SELECT r.id
            FROM recipients r
            JOIN donors d
            ON r.id = d.represents
            WHERE d.id = ?
            """,
            (int(donor.id),),
        )
        row = cur.fetchone()
        return Recipient(id=row["id"])
