import pathlib
import pickle
from typing import List

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch
from solution import KCentersSolver

CWD = pathlib.Path(__file__).parent


def find_bottleneck_path_edges(graph: nx.Graph, centers: List[int]):
    """
    Find the bottleneck path of the solution:
    This is the longest path of all shortest paths from each non-center node to a center node.
    """

    bottleneck_path_length: int = 0
    bottleneck_path_tuple: tuple = ()

    for node in set(graph.nodes) - set(centers):
        center_distances = [
            (c, nx.dijkstra_path_length(graph, node, c)) for c in centers
        ]
        closest_center, distance = min(center_distances, key=lambda t: t[1])
        if distance > bottleneck_path_length:
            bottleneck_path_length = distance
            bottleneck_path_tuple = (node, closest_center)

    bottleneck_path_nodes = nx.dijkstra_path(graph, *bottleneck_path_tuple)
    bottleneck_path_edges = list(zip(bottleneck_path_nodes, bottleneck_path_nodes[1:]))
    return bottleneck_path_length, bottleneck_path_edges


def draw_k_centers_solution(graph: nx.Graph, centers: List[int]):
    # calculate the bottleneck distance and path
    bottleneck, path = find_bottleneck_path_edges(graph, centers)
    path = set(path) | set((u, v) for v, u in path)
    edge_color = ["purple" if e in path else (0.5, 0.5, 0.5, 0.5) for e in graph.edges]
    edge_width = [4 if e in path else 1 for e in graph.edges]
    # prepare node colors and positions
    node_col = ["orange" if v in centers else "black" for v in graph.nodes]
    node_sizes = [30 if v in centers else 10 for v in graph.nodes]
    pos = {node: graph.nodes[node]["coords"] for node in graph.nodes}
    # draw
    nx.draw_networkx_nodes(graph, pos=pos, node_color=node_col, node_size=node_sizes)
    nx.draw_networkx_edges(graph, pos=pos, edge_color=edge_color, width=edge_width)
    plt.title(f"{len(centers)}-Centers Solution (Bottleneck = {bottleneck})")
    legend_handles = [
        Patch(color="purple", label="Bottleneck Path"),
        Patch(color="orange", label="Center Nodes"),
    ]
    plt.legend(handles=legend_handles)
    plt.show(block=True)


if __name__ == "__main__":
    # feel free to change these parameters:
    INSTANCE = "att48.pickle"
    NUM_CENTERS = 3

    with (CWD / "instances" / INSTANCE).open("rb") as f:
        graph = pickle.load(f)

    centers = KCentersSolver(graph).solve(NUM_CENTERS)
    assert len(centers) == NUM_CENTERS
    draw_k_centers_solution(graph, centers)
