import pathlib
import pickle

import networkx as nx
from _alglab_utils import CHECK, main, mandatory_testcase
from solution_hamiltonian import HamiltonianCycleModel

CWD = pathlib.Path(__file__).parent


def solve_hc_instance(filepath: pathlib.Path):
    with filepath.open("rb") as f:
        graph = pickle.load(f)
    CHECK(isinstance(graph, nx.Graph), "Error while loading the pickled instance!")

    solver = HamiltonianCycleModel(graph)
    solution_edges = solver.solve()

    CHECK(solution_edges is not None, "The returned solution must not be 'None'!")
    assert solution_edges is not None, "The returned solution must not be 'None'!"
    CHECK(isinstance(solution_edges, list), "The returned solution must be a list!")
    CHECK(
        len(solution_edges) == graph.number_of_nodes(),
        "The number of returned edges must be equal to the number of nodes!",
    )
    CHECK(
        all(type(e) is tuple for e in solution_edges),
        "The hamiltonian cycle solution must be returned as a list of edges!",
    )
    CHECK(
        all(len(e) == 2 for e in solution_edges),
        "The hamiltonian cycle solution must be returned as a list of edges!",
    )
    CHECK(
        all(graph.has_edge(*e) for e in solution_edges),
        "The returned solution contains edges that are not part of the graph!",
    )

    tour_graph = graph.edge_subgraph(solution_edges)

    CHECK(
        all(d == 2 for v, d in tour_graph.degree),
        "Every node must have two neighbors in the tour!",
    )
    CHECK(
        len(list(nx.connected_components(tour_graph))) == 1,
        "The returned solution must only contain one cycle! (It contained multiple components)",
    )


@mandatory_testcase(max_runtime_s=30)
def alb1000():
    solve_hc_instance(CWD / "./instances/alb1000.pickle")


@mandatory_testcase(max_runtime_s=30)
def alb4000():
    solve_hc_instance(CWD / "./instances/alb4000.pickle")


@mandatory_testcase(max_runtime_s=30)
def alb5000():
    solve_hc_instance(CWD / "./instances/alb5000.pickle")


if __name__ == "__main__":
    main()
