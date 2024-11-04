import pathlib
import pickle

import networkx as nx
from _alglab_utils import CHECK, main, mandatory_testcase
from solution import KCentersSolver

CWD = pathlib.Path(__file__).parent


def solve_instance_and_compare_value(
    instance_path: pathlib.Path, k: int, optimal_bottleneck_distance: float
):
    with instance_path.open("rb") as f:
        graph: nx.Graph = pickle.load(f)
    solver = KCentersSolver(graph)
    centers = solver.solve(k)

    CHECK(isinstance(centers, list), "The centers must be returned as a list!")
    CHECK(
        len(centers) > 0 and len(centers) <= k,
        "The number of centers must be between 0 and k!",
    )
    CHECK(
        all(node in graph.nodes for node in centers),
        "Make sure that the returned centers are valid nodes and in the graph!",
    )

    # calc bottleneck distance
    apsp = dict(nx.all_pairs_dijkstra_path_length(graph))
    bottleneck_distance = max(min(apsp[u][c] for c in centers) for u in graph.nodes)

    CHECK(
        round(bottleneck_distance, 4) == optimal_bottleneck_distance,
        "The bottleneck distance is not optimal!",
    )


@mandatory_testcase(max_runtime_s=90)
def test_att48_k3():
    solve_instance_and_compare_value(CWD / "./instances/att48.pickle", 3, 2203.8833)


@mandatory_testcase(max_runtime_s=90)
def test_att48_k7():
    solve_instance_and_compare_value(CWD / "./instances/att48.pickle", 7, 1401.6460)


@mandatory_testcase(max_runtime_s=90)
def test_att48_k15():
    solve_instance_and_compare_value(CWD / "./instances/att48.pickle", 15, 893.3951)


@mandatory_testcase(max_runtime_s=90)
def test_lin318_k2():
    solve_instance_and_compare_value(CWD / "./instances/lin318.pickle", 2, 2072.0952)


@mandatory_testcase(max_runtime_s=90)
def test_lin318_k3():
    solve_instance_and_compare_value(CWD / "./instances/lin318.pickle", 3, 1937.4858)


if __name__ == "__main__":
    main()
