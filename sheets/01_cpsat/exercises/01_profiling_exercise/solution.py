import itertools

# pip install networkx
import networkx as nx
from data_schema import ProblemInstance, Solution

# pip install ortools
from ortools.sat.python import cp_model


def get_edge_weight(weighted_graph: ProblemInstance, u: str, v: str) -> int:
    """Retrieve the weight of the edge between two nodes."""
    for edge in weighted_graph.connections:
        if (edge.endpoint_a == u and edge.endpoint_b == v) or (
            edge.endpoint_a == v and edge.endpoint_b == u
        ):
            return edge.distance
    raise KeyError(f"Edge {u} - {v} not found in the graph")


def build_weighted_graph(instance: ProblemInstance) -> nx.Graph:
    """Build a NetworkX graph from the problem instance so we can use its shortest path implementation."""
    G = nx.Graph()

    # Add all endpoints as nodes in the graph
    for vertex in instance.endpoints:
        G.add_node(vertex)

    # Add edges with weights to the graph
    for v in instance.endpoints:
        for w in instance.endpoints:
            if v != w:  # Ensure not to check the same node
                # Check if there is an edge between v and w
                if any(
                    edge.endpoint_a == v and edge.endpoint_b == w
                    for edge in instance.connections
                ) or any(
                    edge.endpoint_a == w and edge.endpoint_b == v
                    for edge in instance.connections
                ):
                    # Get the weight of the edge and add it to the graph
                    weight = get_edge_weight(instance, v, w)
                    G.add_edge(v, w, weight=weight)

    return G


def distance(instance: ProblemInstance, u: str, v: str) -> int:
    """Calculate the shortest path distance between two endpoints in the network."""
    graph = build_weighted_graph(instance)
    return nx.shortest_path_length(graph, u, v, weight="weight")


class MaxPlacementsSolver:
    """
    A solver for the maximum number of placements problem using Google OR-Tools' CP-SAT solver.
    """

    def __init__(self, instance: ProblemInstance):
        self.instance = instance
        self.model = cp_model.CpModel()

        # Create a boolean variable for each approved endpoint
        # It will be True if the (approved) endpoint is selected, False otherwise
        self.vars = {
            endpoint: self.model.NewBoolVar(endpoint)
            for endpoint in instance.approved_endpoints
        }

        # Add constraints and objective to the model
        self._add_distance_constraints()
        self._set_objective()

    def _add_distance_constraints(self):
        """Add constraints to ensure selected endpoints are not too close."""
        for endpoint1, endpoint2 in itertools.combinations(
            self.instance.approved_endpoints, 2
        ):
            if (
                distance(self.instance, endpoint1, endpoint2)
                < self.instance.min_distance_between_placements
            ):
                self.model.Add(self.vars[endpoint1] + self.vars[endpoint2] <= 1)

    def _set_objective(self):
        """Set the objective to maximize the number of selected endpoints."""
        self.model.Maximize(sum(self.vars.values()))

    def solve(self, time_limit: float = 10) -> Solution:
        """Solve the optimization problem within the given time limit."""
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        # Enable logging to stdout so we can see the progress
        solver.parameters.log_search_progress = True
        solver.parameters.log_to_stdout = True

        # Solve the model
        status = solver.Solve(self.model)

        # Return the solution if one was found (either optimal or at least feasible)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            # Retrieve the selected endpoints by querying the value of the variables
            selected_placement = [
                endpoint for endpoint in self.vars if solver.Value(self.vars[endpoint])
            ]
            return Solution(selected_placements=selected_placement)

        raise RuntimeError("No solution found within the time limit.")


if __name__ == "__main__":
    # load instance
    instance = ProblemInstance.parse_file("instances/instance_50.json")
    # solve instance
    solver = MaxPlacementsSolver(instance)
    solution = solver.solve()
    print(solution)
