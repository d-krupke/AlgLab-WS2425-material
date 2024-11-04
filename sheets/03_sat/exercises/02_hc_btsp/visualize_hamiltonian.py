import matplotlib.pyplot as plt
import networkx as nx
from solution_hamiltonian import HamiltonianCycleModel

if __name__ == "__main__":
    graph = nx.generators.connected_caveman_graph(4, 6)
    layout = nx.kamada_kawai_layout(graph)
    plt.figure(0)
    nx.draw_networkx(graph, pos=layout)
    plt.title("Original Graph")
    plt.show(block=False)

    # solve HC
    hc_solver = HamiltonianCycleModel(graph)
    tour_edges = hc_solver.solve()
    tour_graph = graph.edge_subgraph(tour_edges)

    plt.figure(1)
    nx.draw_networkx(tour_graph, pos=layout)
    plt.title("Hamiltonian Cycle")
    plt.show(block=True)
