import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from solution_btsp import BottleneckTSPSolver
from solution_hamiltonian import HamiltonianCycleModel


def draw_solution_in_figure(
    tour_edges: list[tuple[int, int]], title: str, figure_id: int, block: bool = False
):
    plt.figure(figure_id)
    tour_graph = graph.edge_subgraph(tour_edges)
    bottleneck = max(graph.edges[e]["weight"] for e in tour_edges)
    edge_color = [
        "red" if graph.edges[e]["weight"] == bottleneck else "black"
        for e in tour_graph.edges
    ]
    nx.draw_networkx(
        tour_graph, pos=layout, node_size=20, edge_color=edge_color, with_labels=False
    )
    plt.title(f"{title} (Bottleneck = {bottleneck})")
    plt.show(block=block)


if __name__ == "__main__":
    with Path("./instances/att48.tsp.pickle").open("rb") as f:
        graph: nx.Graph = pickle.load(f)
    layout = dict(graph.nodes.data("coords"))

    plt.figure(0)
    nx.draw_networkx_nodes(graph, pos=layout, label=None, node_size=20)
    plt.title("Original Graph")
    plt.show(block=False)

    hc_solver = HamiltonianCycleModel(graph)
    hc_edges = hc_solver.solve()
    assert hc_edges is not None, "There should be a solution!"
    draw_solution_in_figure(hc_edges, "Any Hamiltonian Cycle", 1, block=False)

    btsp_solver = BottleneckTSPSolver(graph)
    tour_edges = btsp_solver.optimize_bottleneck()
    assert tour_edges is not None, "There should be a solution!"
    draw_solution_in_figure(tour_edges, "BTSP Tour", 2, block=True)
