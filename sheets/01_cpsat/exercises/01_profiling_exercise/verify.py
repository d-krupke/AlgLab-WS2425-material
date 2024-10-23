from pathlib import Path

from _alglab_utils import CHECK, main, mandatory_testcase
from solution import MaxPlacementsSolver, ProblemInstance

INSTANCE_FOLDER = Path(__file__).parent / "instances"


@mandatory_testcase(max_runtime_s=30)
def instance_30():
    # load instance
    with (INSTANCE_FOLDER / "instance_30.json").open() as f:
        instance = ProblemInstance.model_validate_json(f.read())
    # solve instance
    solver = MaxPlacementsSolver(instance)
    solution = solver.solve()
    CHECK(
        len(solution.selected_placements) == 12,
        "The solution does not contain the expected number of placements. You probably have falsified the model.",
    )


@mandatory_testcase(max_runtime_s=30)
def instance_50():
    # load instance
    with (INSTANCE_FOLDER / "instance_50.json").open() as f:
        instance = ProblemInstance.model_validate_json(f.read())
    # solve instance
    solver = MaxPlacementsSolver(instance)
    solution = solver.solve()
    CHECK(
        len(solution.selected_placements) == 18,
        "The solution does not contain the expected number of placements. You probably have falsified the model.",
    )


@mandatory_testcase(max_runtime_s=30)
def instance_100():
    # load instance
    with (INSTANCE_FOLDER / "instance_100.json").open() as f:
        instance = ProblemInstance.model_validate_json(f.read())
    # solve instance
    solver = MaxPlacementsSolver(instance)
    solution = solver.solve()
    CHECK(
        len(solution.selected_placements) == 24,
        "The solution does not contain the expected number of placements. You probably have falsified the model.",
    )


@mandatory_testcase(max_runtime_s=30)
def instance_200():
    # load instance
    with (INSTANCE_FOLDER / "instance_200.json").open() as f:
        instance = ProblemInstance.model_validate_json(f.read())
    # solve instance
    solver = MaxPlacementsSolver(instance)
    solution = solver.solve()
    CHECK(
        len(solution.selected_placements) == 27,
        "The solution does not contain the expected number of placements. You probably have falsified the model.",
    )


@mandatory_testcase(max_runtime_s=30)
def instance_500():
    # load instance
    with (INSTANCE_FOLDER / "instance_500.json").open() as f:
        instance = ProblemInstance.model_validate_json(f.read())
    # solve instance
    solver = MaxPlacementsSolver(instance)
    solution = solver.solve()
    CHECK(
        len(solution.selected_placements) == 33,
        "The solution does not contain the expected number of placements. You probably have falsified the model.",
    )


if __name__ == "__main__":
    main()
