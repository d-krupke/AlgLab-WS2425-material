import gurobipy as gp
import networkx as nx
from gurobipy import GRB


class Instance:
    """
    Unweighted Steiner Tree Instance
    -------------------------------
    This class represents an instance, consisting of a graph, and
    the list of terminals that have to be connected with as few edges
    as possible.
    """

    def __init__(self, graph: nx.Graph, terminals: list) -> None:
        self.graph = graph
        self.terminals = terminals
        assert all(t in self.graph.nodes() for t in self.terminals)


class _EdgeVariables:
    """
    A helper class that manages the variables for the edges.
    Such a helper class turns out to be useful in many cases.
    """

    def __init__(self, G: nx.Graph, model: gp.Model):
        self._graph = G
        self._model = model
        self._vars = {
            (u, v): model.addVar(vtype=gp.GRB.BINARY, name=f"edge_{u}_{v}")
            for u, v in G.edges
        }

    def x(self, v, w) -> gp.Var:
        """
        Return variable for edge (v, w).
        """
        if (v, w) in self._vars:
            return self._vars[v, w]
        # If (v,w) was not found, try (w,v)
        return self._vars[w, v]

    def outgoing_edges(self, vertices):
        """
        Return all edges&variables that are outgoing from the given vertices.
        """
        # Not super efficient, but efficient enough for our purposes.
        for (v, w), x in self._vars.items():
            if v in vertices and w not in vertices:
                yield (v, w), x
            elif w in vertices and v not in vertices:
                yield (w, v), x

    def incident_edges(self, v):
        """
        Return all edges&variables that are incident to the given vertex.
        """
        for n in self._graph.neighbors(v):
            yield (v, n), self.x(v, n)

    def __iter__(self):
        """
        Iterate over all edges&variables.
        """
        return iter(self._vars.items())

    def as_graph(self, in_callback: bool = False):
        """
        Return the current solution as a graph.
        """
        if in_callback:
            # If we are in a callback, we need to use the solution from the callback.
            used_edges = [vw for vw, x in self if self._model.cbGetSolution(x) > 0.5]
        else:
            # Otherwise, we can use the solution from the model.
            used_edges = [vw for vw, x in self if x.X > 0.5]
        return nx.Graph(used_edges)


def _check_linear(model: gp.Model):
    # check if model has quadratic terms
    if model.NumQConstrs > 0:
        msg = "The model uses quadratic constraints (multiplying variables), which are less efficient. All exercises can be solved with linear constraints."
        raise ValueError(msg)
    if model.NumQNZs > 0:
        msg = "The model uses quadratic terms (multiplying variables) in the objective, which are less efficient. All exercises can be solved with linear terms."
        raise ValueError(msg)


class SteinerTreeSolver:
    """
    A simple solver for the Unweighted Steiner Tree problem.
    """

    def __init__(self, instance: Instance) -> None:
        self.instance = instance
        self.model = gp.Model()
        self._edge_vars = _EdgeVariables(self.instance.graph, self.model)
        self._enforce_outgoing_edge_for_every_terminal()
        self._minimize_edges()

    def _enforce_outgoing_edge_for_every_terminal(self):
        if len(self.instance.terminals) <= 1:
            # Trivial instance, no need to add constraints
            return
        for t in self.instance.terminals:
            self.model.addConstr(
                gp.quicksum(x for _, x in self._edge_vars.incident_edges(t)) >= 1
            )

    def _minimize_edges(self):
        self.model.setObjective(sum(x for _, x in self._edge_vars), GRB.MINIMIZE)

    def lower_bound(self):
        """
        Return the current lower bound.
        """
        # Only works if the model has been optimized once.
        return self.model.ObjBound

    def solve(self, time_limit: float = 900, opt_tol: float = 0.0001):
        self.model.Params.TimeLimit = time_limit  # Limit the runtime
        self.model.Params.MIPGap = opt_tol  # Allowing a small optimality gap
        self.model.Params.NonConvex = 0  # Throw an error if the model is non-convex

        def callback(model, where):
            # This callback is called by Gurobi on various occasions, and
            # we can react to these occasions.
            if where == gp.GRB.Callback.MIPSOL:
                # We are in a new MIP solution. We can query the solution
                # and add additional constraints, if we want to.
                # We are going to enforce a leaving edge for every component
                # that contains only a part of the terminals.
                solution = self._edge_vars.as_graph(in_callback=True)
                comps = list(nx.connected_components(solution))
                if len(comps) == 1:
                    return  # solution is connected
                terminals = set(self.instance.terminals)
                for comp in comps:
                    terms_in_comp = terminals & comp
                    if not terms_in_comp:
                        continue  # the objective will remove this component by itself
                    if terms_in_comp != terminals:
                        # we have a component that contains some terminals but not all
                        # -> we need to add a constraint
                        model.cbLazy(
                            sum(x for _, x in self._edge_vars.outgoing_edges(comp)) >= 1
                        )

        self.model.Params.LazyConstraints = 1  # enable lazy constraints
        self.model.optimize(callback)  # pass the callback with the `solve` call
        _check_linear(self.model)
        if self.model.status == GRB.OPTIMAL:
            return self._edge_vars.as_graph()
        if self.model.SolCount > 0:
            # If the solution is not optimal, it may not be a tree. Apply DFS to get a tree.
            return nx.dfs_tree(self._edge_vars.as_graph())
        return None
