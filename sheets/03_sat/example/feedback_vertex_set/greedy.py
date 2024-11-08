import networkx as nx
from util import Node, find_cycle


def greedy_fvs(graph: nx.Graph) -> set[Node]:
    """
    This method generates a greedy solution to the Feedback Vertex Set problem.
    The algorithm iteratively identifies and "breaks open" remaining cycles in the graph.
    The utilized greedy strategy always removes the vertex with the highest degree from a
    found cycle, as the chance for breaking open more than one cycle increases.
    """
    graph = graph.copy()
    feedback_vertex_set = set()
    while (cycle := find_cycle(graph)) is not None:
        highest_degree_vertex = max(cycle, key=lambda v: graph.degree(v))
        graph.remove_node(highest_degree_vertex)
        feedback_vertex_set.add(highest_degree_vertex)
    return feedback_vertex_set
