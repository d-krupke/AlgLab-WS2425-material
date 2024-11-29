# Random instance generator for the TSP problem


import networkx as nx


def generate_instance(n=200) -> tuple[nx.Graph, list[tuple[int, int]]]:
    # generate n random points
    import random

    points = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(n)]

    def eucl_dist(p1, p2):
        return round(((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5)

    # create weighted graph
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=eucl_dist(points[i], points[j]))
    return G, points


def draw_integral_solution(
    ax, solution: nx.Graph, points: list[tuple[int, int]], title="Integral Solution"
):
    ax.set_title(title)
    # equal aspect ratio
    ax.set_aspect("equal", adjustable="box")
    pos = {i: points[i] for i in range(len(points))}
    nx.draw(
        solution,
        pos,
        ax=ax,
        with_labels=False,
        node_size=10,
        node_color="blue",
        edge_color="black",
    )


def draw_fractional_solution(
    ax, solution: nx.Graph, points: list[tuple[int, int]], title="Linear Relaxation"
):
    ax.set_title(title)
    # equal aspect ratio
    ax.set_aspect("equal", adjustable="box")
    pos = {i: points[i] for i in range(len(points))}
    # draw fractional edges in red. An edge is fractional if the attribute `x` is between 0.01 and 0.99
    for u, v, d in solution.edges(data=True):
        if 0.01 < d["x"] < 0.99:
            nx.draw(
                nx.Graph([(u, v)]),
                pos,
                ax=ax,
                with_labels=False,
                node_size=10,
                node_color="red",
                edge_color="red",
            )
    # draw integral edges in black. An edge is integral if the attribute `x` is > 0.99
    for u, v, d in solution.edges(data=True):
        if d["x"] > 0.99:
            nx.draw(
                nx.Graph([(u, v)]),
                pos,
                ax=ax,
                with_labels=False,
                node_size=10,
                node_color="blue",
                edge_color="black",
            )


def draw_overlap(
    ax, solution: nx.Graph, linear_relaxation: nx.Graph, points: list[tuple[int, int]]
):
    # draw the edges of the integral solution that have a value >= 0.5 in the fractional solution

    ax.set_title("Overlap")
    # equal aspect ratio
    ax.set_aspect("equal", adjustable="box")
    # draw all nodes
    nx.draw(
        solution,
        points,
        ax=ax,
        with_labels=False,
        node_size=10,
        node_color="blue",
        edge_color="grey",
        width=0.1,
    )
    # draw the edges of the integral solution that have a value >= 0.5 in the fractional solution
    n = 0
    for u, v, d in solution.edges(data=True):
        # if not in linear relaxation, skip
        if not linear_relaxation.has_edge(u, v):
            continue
        if linear_relaxation[u][v]["x"] >= 0.5:
            nx.draw(
                nx.Graph([(u, v)]),
                points,
                ax=ax,
                with_labels=False,
                node_size=10,
                node_color="blue",
                edge_color="green",
            )
            n += 1
    return n


import matplotlib.pyplot as plt
from solution_dantzig import GurobiTspSolver
from solution_relaxation import GurobiTspRelaxationSolver

samples = []
n = 200


def get_sample():
    instance, points = generate_instance(n)

    # Create a figure with 2 rows and 3 columns
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # First row: k=2 relaxation, integral solution, difference
    # Second row: k=1 relaxation, integral solution, difference

    # Solving the linear relaxation with k=2
    print("Solving the linear relaxation with k=2")
    relaxation_solver_k2 = GurobiTspRelaxationSolver(instance, k=2)
    relaxation_solver_k2.solve()
    relaxed_solution_k2 = relaxation_solver_k2.get_solution()
    linear_relaxation_value_k2 = relaxation_solver_k2.get_objective()
    assert relaxed_solution_k2 is not None
    draw_fractional_solution(
        axes[0, 0],
        relaxed_solution_k2,
        points,
        f"Linear Relaxation k=2 (obj: {linear_relaxation_value_k2:.2f})",
    )

    # Solving the integral problem
    print("Solving the integral problem")
    solver = GurobiTspSolver(instance)
    solver.solve(30)
    solution = solver.get_solution()
    objective_value = solver.get_objective()
    assert solution is not None
    draw_integral_solution(
        axes[0, 1], solution, points, f"Optimal Solution (obj: {objective_value:.2f})"
    )

    # Difference between integral solution and k=2 relaxation
    overlap_k2 = draw_overlap(axes[0, 2], solution, relaxed_solution_k2, points)
    axes[0, 2].set_title(f"Overlap with k=2 relaxation ({overlap_k2}/{n})")

    # Solving the linear relaxation with k=1
    print("Solving the linear relaxation with k=1")
    relaxation_solver_k1 = GurobiTspRelaxationSolver(instance, k=1)
    relaxation_solver_k1.solve()
    relaxed_solution_k1 = relaxation_solver_k1.get_solution()
    linear_relaxation_value_k1 = relaxation_solver_k1.get_objective()
    assert relaxed_solution_k1 is not None
    draw_fractional_solution(
        axes[1, 0],
        relaxed_solution_k1,
        points,
        f"Linear Relaxation k=1 (obj: {linear_relaxation_value_k1:.2f})",
    )

    # Re-use integral solution for second row
    draw_integral_solution(
        axes[1, 1], solution, points, f"Optimal Solution (obj: {objective_value:.2f})"
    )

    # Difference between integral solution and k=1 relaxation
    overlap_k1 = draw_overlap(axes[1, 2], solution, relaxed_solution_k1, points)
    axes[1, 2].set_title(f"Overlap with k=1 relaxation ({overlap_k1}/{n})")

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()

    print(
        f"Objective value: {objective_value}, Linear relaxation k=2 value: {linear_relaxation_value_k2}, Overlap: {overlap_k2}/{n}"
    )
    print(
        f"Objective value: {objective_value}, Linear relaxation k=1 value: {linear_relaxation_value_k1}, Overlap: {overlap_k1}/{n}"
    )
    samples.append((objective_value, linear_relaxation_value_k2, overlap_k2))
