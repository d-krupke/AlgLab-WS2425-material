import os

from _alglab_utils import CHECK, main, mandatory_testcase
from _db_impl import SqliteTransplantDatabase, TransplantDatabase
from data_schema import Donation, Solution
from solution_basic import CrossoverTransplantSolver

INSTANCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instances")


def solve_instance_and_check_solution(db_name: str, solution_score: int):
    """
    Solves the given instance and compares it against the reference solution
    score. Also evaluates the validity of the solution.
    """
    db_path = os.path.join(INSTANCE_DIR, db_name)
    db: TransplantDatabase = SqliteTransplantDatabase(path=db_path)
    solver = CrossoverTransplantSolver(database=db)
    solution: Solution = solver.optimize()

    # check logical validity
    check_solution_validity(solution, db)

    # check solution score
    CHECK(
        len(solution.donations) == solution_score,
        f"The returned solution is not of optimal size. {len(solution.donations)} != {solution_score} (Most likely, your model is faulty).",
    )


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
    solution = solution.donations
    CHECK(
        all(isinstance(don, Donation) for don in solution),
        "The solution list must be made of entries of type 'Donation'!",
    )
    # check that donations are between compatible donor+patient
    for donation in solution:
        patient = donation.recipient
        compatible_donors = database.get_compatible_donors(patient)
        CHECK(
            donation.donor in compatible_donors,
            "The solution contains donations between incompatible donors and patients!",
        )

    # check that every donor only donates once
    CHECK(
        len(set(don.donor for don in solution)) == len(solution),
        "There is at least one donor who occurs multiple times in the solution list!",
    )
    # check that every patient only receives once
    CHECK(
        len(set(don.recipient for don in solution)) == len(solution),
        "There is at least one patient who occurs multiple times in the solution list!",
    )
    # check that for every receiving recipient, exactly one associated donor donates
    for donation in solution:
        patient = donation.recipient
        associated_donors = set(database.get_partner_donors(patient))
        associated_donors &= set(don.donor for don in solution)
        CHECK(
            len(associated_donors) == 1,
            f"Every patient that receives a donation needs exactly one representative donor to make a donation to somebody else! Total count for patient {patient.id}: {len(associated_donors)}",
        )
    # check that no donor donates, whose associated patient does not receive a donation
    for donation in solution:
        donor = donation.donor
        assoc_patient = database.get_partner_recipient(donor)
        CHECK(
            any(don.recipient == assoc_patient for don in solution),
            f"Donor {donor.id} donates, but their associated patient ({assoc_patient.id}) does not receive a donation!",
        )


@mandatory_testcase(max_runtime_s=30)
def db_20():
    solve_instance_and_check_solution("20.db", 19)


@mandatory_testcase(max_runtime_s=30)
def db_50():
    solve_instance_and_check_solution("50.db", 46)


@mandatory_testcase(max_runtime_s=30)
def db_100():
    solve_instance_and_check_solution("100.db", 91)


@mandatory_testcase(max_runtime_s=30)
def db_200():
    solve_instance_and_check_solution("200.db", 192)


@mandatory_testcase(max_runtime_s=90)
def db_500():
    solve_instance_and_check_solution("500.db", 499)


@mandatory_testcase(max_runtime_s=180)
def db_600():
    solve_instance_and_check_solution("600.db", 597)


if __name__ == "__main__":
    main()
