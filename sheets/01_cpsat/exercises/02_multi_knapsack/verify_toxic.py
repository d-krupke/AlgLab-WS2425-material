"""
This module contains test cases for the MultiKnapsackSolver class in solver.py.
It tests the correctness of the solution returned by the solver for different instances.
"""

from pathlib import Path

from _alglab_utils import CHECK, main, mandatory_testcase
from solution import Instance, MultiKnapsackSolver, Solution

INSTANCE_DIR = Path(__file__).resolve().parent / "instances"


def solve_instance_and_check_solution(
    filename: str,
    solution_score: int,
    timelimit: int = 120,
    activate_toxic: bool = False,
):
    instance = None
    with Path(INSTANCE_DIR / filename).open() as f:
        instance = Instance.model_validate_json(f.read())
    multi_knapsack = MultiKnapsackSolver(instance, activate_toxic=activate_toxic)
    solution = multi_knapsack.solve(timelimit=timelimit)

    CHECK(isinstance(solution, Solution), "The solution must be of type 'list'.")
    CHECK(solution is not None, "The solution is None!")
    CHECK(
        len(solution.trucks) == len(instance.capacities),
        f"The solution list must contain a list of items for each knapsack! The solution has {len(solution.trucks)} knapsacks, but the instance has {len(instance.capacities)} knapsacks.",
    )

    # count occurrences of each item
    for i, item in enumerate(instance.items):
        if occurrences := [
            j for j, knapsack in enumerate(solution) if item in knapsack
        ]:
            CHECK(
                len(occurrences) == 1,
                f"Item {i} occurs in more than one knapsack! Specifically, in knapsacks nr {occurrences}!",
            )

    # check capacity constraint and solution score
    score = 0
    for (j, knapsack), capacity in zip(enumerate(solution.trucks), instance.capacities):
        used_capacity = sum(item.weight for item in knapsack)
        CHECK(
            used_capacity <= capacity,
            f"'Knapsack {j}'s capacity was exceeded! ({used_capacity}/{capacity})",
        )
        score += sum(item.value for item in knapsack)
        if activate_toxic:
            CHECK(
                all(item.toxic for item in knapsack)
                or not any(item.toxic for item in knapsack),
                f"Knapsack {j} contains toxic and non-toxic items!",
            )

    CHECK(
        score >= solution_score,
        f"The score of the returned solution is not good enough {score} < {solution_score}. Your client looses money and hires someone else!",
    )


@mandatory_testcase(max_runtime_s=30)
def instance_1_toxic():
    solve_instance_and_check_solution(
        "10i_1k.json", 1176, timelimit=25, activate_toxic=True
    )


@mandatory_testcase(max_runtime_s=30)
def instance_2_toxic():
    solve_instance_and_check_solution(
        "20i_5k.json", 88, timelimit=25, activate_toxic=True
    )


@mandatory_testcase(max_runtime_s=30)
def instance_3_toxic():
    solve_instance_and_check_solution(
        "50i_5k.json", 414, timelimit=25, activate_toxic=True
    )


@mandatory_testcase(max_runtime_s=30)
def instance_4_toxic():
    solve_instance_and_check_solution(
        "75i_6k.json", 555, timelimit=25, activate_toxic=True
    )


@mandatory_testcase(max_runtime_s=60)
def instance_5_toxic():
    solve_instance_and_check_solution(
        "10000i_1k.json", 111500, timelimit=25, activate_toxic=True
    )


if __name__ == "__main__":
    main()
