import networkx as nx
from _alglab_utils import CHECK, main, mandatory_testcase
from _tsplib import TspLibGraphInstanceDb
from solution_relaxation import GurobiTspRelaxationSolver


def _in_between(lb, obj, ub):
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(obj < ub, "Did you just use the MIP?")
    CHECK(obj >= lb, "Try to improve your lower bound")


def _connected(solution):
    # Create graph consisting of all edges with `x >= 0.01`
    g = nx.Graph()
    g.add_nodes_from(solution.nodes)
    for u, v, x in solution.edges.data("x"):
        CHECK(
            x is not None,
            "Solution graph does not include variable assignments! Make sure to add each variable assignment as edge data attribute 'x'",
        )
        if x >= 0.01:
            g.add_edge(u, v, x=x)
    CHECK(
        nx.is_connected(g),
        "Solution is not connected. Make sure you add the subtour elimination constraints. We consider an edge to be used in the fractional solution if `x >= 0.01`.",
    )


@mandatory_testcase(max_runtime_s=30)
def att48():
    db = TspLibGraphInstanceDb()
    instance = db["att48"]
    solver = GurobiTspRelaxationSolver(instance)
    solver.solve()
    solution = solver.get_solution()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    assert solution is not None
    CHECK(
        solution.number_of_nodes() == instance.number_of_nodes(),
        "Solution has wrong number of nodes",
    )
    _connected(solution)
    obj = solver.get_objective()
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(
        obj <= 33522.0,
        "You objective is worse than the integral solution. This is not a linear relaxation.",
    )

    # Check if every node has degree 2
    def frac_deg(v):
        incident_edges = solution.edges([v])
        return round(sum(solution.edges[e]["x"] for e in incident_edges), 2)

    CHECK(all(frac_deg(v) == 2 for v in solution.nodes), "Solution is not a cycle")
    _in_between(31668.5, solver.get_objective(), 33522.0)


@mandatory_testcase(max_runtime_s=30)
def eil101():
    db = TspLibGraphInstanceDb()
    instance = db["eil101"]
    solver = GurobiTspRelaxationSolver(instance)
    solver.solve()
    solution = solver.get_solution()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    assert solution is not None
    CHECK(
        solution.number_of_nodes() == instance.number_of_nodes(),
        "Solution has wrong number of nodes",
    )
    _connected(solution)
    obj = solver.get_objective()
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(
        obj <= 629.0,
        "You objective is worse than the integral solution. This is not a linear relaxation.",
    )

    # Check if every node has degree 2
    def frac_deg(v):
        incident_edges = solution.edges([v])
        return round(sum(solution.edges[e]["x"] for e in incident_edges), 2)

    CHECK(all(frac_deg(v) == 2 for v in solution.nodes), "Solution is not a cycle")
    _in_between(619.0, solver.get_objective(), 629.0)


@mandatory_testcase(max_runtime_s=30)
def eil76():
    db = TspLibGraphInstanceDb()
    instance = db["eil76"]
    solver = GurobiTspRelaxationSolver(instance)
    solver.solve()
    solution = solver.get_solution()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    assert solution is not None
    CHECK(
        solution.number_of_nodes() == instance.number_of_nodes(),
        "Solution has wrong number of nodes",
    )
    _connected(solution)
    obj = solver.get_objective()
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(
        obj <= 542.0,
        "You objective is worse than the integral solution. This is not a linear relaxation.",
    )

    # Check if every node has degree 2
    def frac_deg(v):
        incident_edges = solution.edges([v])
        return round(sum(solution.edges[e]["x"] for e in incident_edges), 2)

    CHECK(all(frac_deg(v) == 2 for v in solution.nodes), "Solution is not a cycle")
    _in_between(534.0, solver.get_objective(), 542.0)


@mandatory_testcase(max_runtime_s=30)
def kroA100():
    db = TspLibGraphInstanceDb()
    instance = db["kroA100"]
    solver = GurobiTspRelaxationSolver(instance)
    solver.solve()
    solution = solver.get_solution()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    assert solution is not None
    CHECK(
        solution.number_of_nodes() == instance.number_of_nodes(),
        "Solution has wrong number of nodes",
    )
    _connected(solution)
    CHECK(nx.is_connected(solution), "Solution is not connected")
    obj = solver.get_objective()
    CHECK(obj is not None, "Objective value is 'None'")
    assert obj is not None
    CHECK(
        obj <= 21282.0,
        "You objective is worse than the integral solution. This is not a linear relaxation.",
    )

    # Check if every node has degree 2
    def frac_deg(v):
        incident_edges = solution.edges([v])
        return round(sum(solution.edges[e]["x"] for e in incident_edges), 2)

    CHECK(all(frac_deg(v) == 2 for v in solution.nodes), "Solution is not a cycle")
    _in_between(19378.5, solver.get_objective(), 21282.0)


if __name__ == "__main__":
    db = TspLibGraphInstanceDb()
    db.download()
    main()
