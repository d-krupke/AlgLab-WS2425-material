import os
from pathlib import Path

import networkx as nx
from _alglab_utils import CHECK, main, mandatory_testcase
from _db_impl import SqliteTransplantDatabase, TransplantDatabase
from data_schema import Donation, Solution
from solution_small_cycles import CycleLimitingCrossoverTransplantSolver

INSTANCE_DIR = os.path.join(os.path.dirname(Path(__file__).resolve()), "instances")
MAX_CYCLE_LEN = 3


def solve_instance_and_check_solution(db_name: str, solution_score: int):
    db_path = Path(INSTANCE_DIR) / db_name
    db: TransplantDatabase = SqliteTransplantDatabase(path=str(db_path))
    solver = CycleLimitingCrossoverTransplantSolver(database=db)
    solution: Solution = solver.optimize()

    # check logical validity
    check_solution_validity(solution, db)

    donation_graph = get_donation_graph(solution, db)
    CHECK(
        all(d == 2 for _, d in donation_graph.degree),  # type: ignore[attr-defined]
        "The donation graph indicates an invalid solution!",
    )
    for cycle in nx.simple_cycles(donation_graph):
        CHECK(
            len(cycle) <= MAX_CYCLE_LEN,
            f"The solution contains a donation cycle longer than {MAX_CYCLE_LEN}",
        )

    # check solution value
    CHECK(
        len(solution.donations) == solution_score,
        f"The returned solution is not of optimal size. {len(solution.donations)} != {solution_score} (Most likely, your model is faulty).",
    )


def get_donation_graph(solution: Solution, database: TransplantDatabase) -> nx.DiGraph:
    graph = nx.DiGraph()
    for donation in solution.donations:
        represented_patient = database.get_partner_recipient(donation.donor)
        patient = donation.recipient
        graph.add_edge(represented_patient, patient)
    return graph


def check_solution_validity(solution: Solution, database: TransplantDatabase):
    """
    Check the validity of the solution datastructure itself,
    and the logical validity under the constraints of the problem.
    More specifically:
    - The solution must not be None and it must be of the correct solution type.
    - Donations must be between compatible Donors and Recipients.
    - Donors donate atmost once.
    - Recipients receive atmost once.
    - Donors only donate if their associated Recipient receives.
    """
    CHECK(solution is not None, "The solution is None!")
    CHECK(isinstance(solution, Solution), "The solution must be of type 'Solution'.")
    donations = solution.donations
    CHECK(
        all(isinstance(don, Donation) for don in donations),
        "The solution list must be made of entries of type 'Donation'!",
    )
    # check that donations are between compatible donor+patient
    for donation in donations:
        patient = donation.recipient
        compatible_donors = database.get_compatible_donors(patient)
        CHECK(
            donation.donor in compatible_donors,
            "The solution contains donations between incompatible donors and patients!",
        )

    # check that every donor only donates once
    CHECK(
        len({don.donor for don in donations}) == len(donations),
        "There is at least one donor who occurs multiple times in the solution list!",
    )
    # check that every patient only receives once
    CHECK(
        len({don.recipient for don in donations}) == len(donations),
        "There is at least one patient who occurs multiple times in the solution list!",
    )
    # check that for every receiving recipient, exactly one associated donor donates
    for donation in donations:
        patient = donation.recipient
        associated_donors = set(database.get_partner_donors(patient))
        associated_donors &= {don.donor for don in donations}
        CHECK(
            len(associated_donors) == 1,
            f"Every patient that receives a donation needs exactly one representative donor to make a donation to somebody else! Total count for patient {patient.id}: {len(associated_donors)}",
        )
    # check that no donor donates, whose associated patient does not receive a donation
    for donation in donations:
        donor = donation.donor
        assoc_patient = database.get_partner_recipient(donor)
        CHECK(
            any(don.recipient == assoc_patient for don in donations),
            f"Donor {donor.id} donates, but their associated patient ({assoc_patient.id}) does not receive a donation!",
        )


@mandatory_testcase(max_runtime_s=30)
def db_20():
    solve_instance_and_check_solution("20.db", 18)


@mandatory_testcase(max_runtime_s=30)
def db_50():
    solve_instance_and_check_solution("50.db", 43)


@mandatory_testcase(max_runtime_s=30)
def db_100():
    solve_instance_and_check_solution("100.db", 91)


@mandatory_testcase(max_runtime_s=60)
def db_200():
    solve_instance_and_check_solution("200.db", 192)


if __name__ == "__main__":
    main()
