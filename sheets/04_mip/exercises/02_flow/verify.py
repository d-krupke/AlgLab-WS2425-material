from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from _alglab_utils import CHECK, main, mandatory_testcase
from data_schema import Instance
from solution import MiningRoutingSolver

CWD = Path(__file__).parent
EPS = 0.001


def solve_hc_instance(filepath: Path, objective_sol: int):
    with filepath.open() as f:
        instance: Instance = Instance.model_validate_json(f.read())

    solver = MiningRoutingSolver(instance)
    solution = solver.solve()
    CHECK(solution is not None, "The returned solution must not be 'None'!")
    solution = solution.flow
    CHECK(len(solution) > 0, "The solution flow must not be empty!")

    flow_graph = nx.DiGraph()

    def find_road(from_: int, to_: int):
        tunnel_set: set = {from_, to_}
        matching_tunnels = [
            tunnel
            for tunnel in instance.tunnels
            if {tunnel.source, tunnel.target} == tunnel_set
        ]
        CHECK(
            len(matching_tunnels) == 1,
            f"The solution contains a tunnel from {from_} to {to_} that is not part of the given instance!",
        )
        return matching_tunnels[0]

    budget_used = 0.0
    for (u, v), util in solution:
        CHECK(
            isinstance(util, int),
            f"The utilization of a tunnel from {u} to {v} must be an integer! Current type: {type(util)} ({util})",
        )
        for i in (u, v):
            CHECK(
                i == instance.elevator_location or u in instance.mines,
                f"Location id '{i}' from solution is not part of the given instance!",
            )
        road = find_road(u, v)
        budget_used += road.reinforcement_costs
        capacity = road.throughput_per_hour
        CHECK(
            util > 0,
            f"Tunnels in the solution must only have positive utilization! However, there is a tunnel from {u} to {v} with utilization {util}!",
        )
        CHECK(
            util <= capacity,
            f"The capacity of a tunnel from {u} to {v} was exceeded! (utilization: {util}, capacity: {capacity})",
        )
        flow_graph.add_edge(u, v, capacity=capacity, utilization=util)
    CHECK(
        budget_used <= instance.budget + EPS,
        f"The instance budget was exceeded! (even with granted rounding inaccuracy) {budget_used} > {instance.budget}",
    )
    CHECK(
        instance.elevator_location in flow_graph.nodes,
        "The elevator is not connected!",
    )
    CHECK(
        flow_graph.to_undirected().number_of_edges() == flow_graph.number_of_edges(),
        "Tunnels can only be used in one direction at once! Your solution contains a tunnel between {u} and {v} that is used in both directions!",
    )

    for loc in flow_graph.nodes:
        in_sum = sum(
            d["utilization"] for u, v, d in flow_graph.in_edges(loc, data=True)
        )
        out_sum = sum(
            d["utilization"] for u, v, d in flow_graph.out_edges(loc, data=True)
        )
        if loc == instance.elevator_location:
            CHECK(
                out_sum == 0,
                f"No resources must leave the elevator location! Current: {out_sum}",
            )
            CHECK(
                in_sum == objective_sol,
                f"The objective is not optimal! {in_sum} != {objective_sol}",
            )
        else:
            CHECK(
                out_sum <= in_sum + instance.mines[loc].ore_per_hour,
                f"There is more ore leaving mine {loc} than entering + produced!",
            )
    visualize_solution(flow_graph, instance)


def visualize_solution(flow_graph: nx.DiGraph, instance: Instance):
    pos = nx.spring_layout(flow_graph)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(flow_graph, pos, node_size=700)

    # edges
    edges = flow_graph.edges(data=True)
    nx.draw_networkx_edges(flow_graph, pos, edgelist=edges, width=2, edge_color="black")

    # labels
    labels = {node: str(node) for node in flow_graph.nodes()}
    nx.draw_networkx_labels(flow_graph, pos, labels, font_size=20)

    # edge labels
    edge_labels = {
        (u, v): f"{d['utilization']}/{d['capacity']}"
        for u, v, d in flow_graph.edges(data=True)
    }
    nx.draw_networkx_edge_labels(flow_graph, pos, edge_labels=edge_labels)

    plt.title("Mining Routing Solution")
    plt.show()


@mandatory_testcase(max_runtime_s=30)
def instance_10():
    solve_hc_instance(CWD / "./instances/instance_10.json", 46)


@mandatory_testcase(max_runtime_s=30)
def instance_20():
    solve_hc_instance(CWD / "./instances/instance_20.json", 83)


@mandatory_testcase(max_runtime_s=30)
def instance_50():
    solve_hc_instance(CWD / "./instances/instance_50.json", 226)


@mandatory_testcase(max_runtime_s=30)
def instance_200():
    solve_hc_instance(CWD / "./instances/instance_200.json", 892)


@mandatory_testcase(max_runtime_s=60)
def instance_500():
    solve_hc_instance(CWD / "./instances/instance_500.json", 2193)


if __name__ == "__main__":
    main()
