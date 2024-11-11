import networkx as nx
from _alglab_utils import CHECK, main, mandatory_testcase
from _tsplib import TspLibGraphInstanceDb
from solution_dantzig import GurobiTspSolver


@mandatory_testcase(max_runtime_s=30)
def att48():
    db = TspLibGraphInstanceDb()
    instance = db["att48"]
    solver = GurobiTspSolver(instance)
    solver.solve(time_limit=30)
    solution = solver.get_solution()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    assert solution is not None
    CHECK(
        solution.number_of_nodes() == instance.number_of_nodes(),
        "Solution has wrong number of nodes",
    )
    CHECK(nx.is_connected(solution), "Solution is not connected")
    # Check if every node has degree 2
    CHECK(
        all(solution.degree(v) == 2 for v in solution.nodes),  # type: ignore[attr-defined]
        "Solution is not a cycle",
    )
    obj = solver.get_objective()
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(obj == 33522.0, "Objective value is wrong")


@mandatory_testcase(max_runtime_s=30)
def eil101():
    db = TspLibGraphInstanceDb()
    instance = db["eil101"]
    solver = GurobiTspSolver(instance)
    solver.solve(time_limit=30)
    solution = solver.get_solution()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    assert solution is not None
    CHECK(
        solution.number_of_nodes() == instance.number_of_nodes(),
        "Solution has wrong number of nodes",
    )
    CHECK(nx.is_connected(solution), "Solution is not connected")
    # Check if every node has degree 2
    CHECK(
        all(solution.degree(v) == 2 for v in solution.nodes),  # type: ignore[attr-defined]
        "Solution is not a cycle",
    )
    obj = solver.get_objective()
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(obj == 629.0, "Objective value is wrong")


@mandatory_testcase(max_runtime_s=30)
def eil76():
    db = TspLibGraphInstanceDb()
    instance = db["eil76"]
    solver = GurobiTspSolver(instance)
    solver.solve(time_limit=30)
    solution = solver.get_solution()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    assert solution is not None
    CHECK(
        solution.number_of_nodes() == instance.number_of_nodes(),
        "Solution has wrong number of nodes",
    )
    CHECK(nx.is_connected(solution), "Solution is not connected")
    # Check if every node has degree 2
    CHECK(
        all(solution.degree(v) == 2 for v in solution.nodes),  # type: ignore[attr-defined]
        "Solution is not a cycle",
    )
    obj = solver.get_objective()
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(obj == 538.0, "Objective value is wrong")


@mandatory_testcase(max_runtime_s=30)
def kroA100():
    db = TspLibGraphInstanceDb()
    instance = db["kroA100"]
    solver = GurobiTspSolver(instance)
    solver.solve(time_limit=30)
    solution = solver.get_solution()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    assert solution is not None
    CHECK(
        solution.number_of_nodes() == instance.number_of_nodes(),
        "Solution has wrong number of nodes",
    )
    CHECK(nx.is_connected(solution), "Solution is not connected")
    # Check if every node has degree 2
    CHECK(
        all(solution.degree(v) == 2 for v in solution.nodes),  # type: ignore[attr-defined]
        "Solution is not a cycle",
    )
    obj = solver.get_objective()
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(obj == 21282.0, "Objective value is wrong")


if __name__ == "__main__":
    db = TspLibGraphInstanceDb()
    db.download()
    main()
