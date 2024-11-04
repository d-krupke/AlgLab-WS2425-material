import pathlib
import pickle

import networkx as nx
from _alglab_utils import CHECK, main, mandatory_testcase
from solution_btsp import BottleneckTSPSolver

CWD = pathlib.Path(__file__).parent


def solve_instance_and_check_bottleneck(filename: str, bottleneck: float):
    filepath = CWD / filename
    with open(filepath, "rb") as f:
        graph: nx.Graph = pickle.load(f)
    CHECK(isinstance(graph, nx.Graph), "Error while loading the pickled instance!")

    solver = BottleneckTSPSolver(graph)
    solution_edges = solver.optimize_bottleneck()

    CHECK(solution_edges is not None, "The returned solution must not be 'None'!")
    assert isinstance(solution_edges, list), "The returned solution must be a list!"
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
        all(d == 2 for v, d in tour_graph.degree),  # type: ignore[attr-defined]
        "Every node must have two neighbors in the tour!",
    )
    CHECK(
        len(list(nx.connected_components(tour_graph))) == 1,
        "The returned solution must only contain one cycle! (It contained multiple components)",
    )

    solution_bottleneck = max(graph.edges[e]["weight"] for e in solution_edges)
    CHECK(
        round(solution_bottleneck, 4) == bottleneck,
        f"The returned tour is not the optimal one! Your bottleneck: {solution_bottleneck}. Optimal bottleneck: {bottleneck}",
    )


@mandatory_testcase(max_runtime_s=30)
def att48():
    solve_instance_and_check_bottleneck("./instances/att48.tsp.pickle", 16382.8968)


@mandatory_testcase(max_runtime_s=60)
def lin318():
    solve_instance_and_check_bottleneck("./instances/lin318.tsp.pickle", 4870.5734)


if __name__ == "__main__":
    main()
