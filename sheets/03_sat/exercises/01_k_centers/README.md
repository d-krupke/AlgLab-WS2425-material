# Exercise: k-centers using a SAT-solver

![Vertex K-Centers](./.figures/dalle-kcentre.png)

Your next client is a logistics company tasked with establishing emergency
response centers across a metropolitan area. These centers will serve as crucial
hubs for dispatching essential services and supplies, but budget constraints
limit the number of centers that can be built. The company aims to minimize the
maximum travel time any neighborhood would face to reach its closest center in
an emergency.

The company's data engineers have simplified the city's layout, representing
each neighborhood by a central location. This center has been chosen to ensure
that most places within the neighborhood are quickly reachable from it. The
travel times between these neighborhood centers form a network, where
neighborhoods are nodes, and roads with corresponding travel times are edges
between them.

## Vertex K-Centers - A Facility Location Problem

This abstraction brings us to the **Vertex K-Center Problem**. Formally, you are
given a weighted, undirected graph $G = (V, E)$, where $V$ represents
neighborhood centers and $E$ represents direct travel routes between them, with
each edge $vw \in E$ assigned a weight $d_{vw}$ indicating the travel time
between the neighborhood centers. For pairs of neighborhoods not directly
connected by an edge, you will need to compute the shortest path distance
$d_{vw}$ as the minimum travel time via other neighborhoods.

Given a maximum number $k$ of centers, the objective is to select a subset
$C \subseteq V$ with $|C| \leq k$ such that the maximum distance from any
neighborhood center to its closest service center is minimized. In other words,
your goal is to place the service centers in locations that reduce the longest
travel distance any neighborhood faces to reach a center.

This problem is a classic in mathematical optimization, with applications beyond
emergency response, including urban planning, facility placement, and logistics.

## Deliverables

1. **Formulate the Decision Variant as a SAT Problem** Begin by formulating the
   decision variant of the Vertex K-Center Problem as a SAT problem with
   cardinality constraints. The decision variant asks whether a solution exists
   with an objective value of at most $c$ for a given $k$. Since
   $d_{vw} \in \mathbb{R}^+_0$, $c$ can be any non-negative floating-point
   number. Think about how to minimize the number of queries to the decision
   variant by identifying the possible values that $c$ can take.
2. **Implement a Heuristic for an Upper Bound** Develop a heuristic to quickly
   obtain an upper bound on the objective value. This heuristic does not need to
   be optimal but should be efficient enough to find an initial feasible
   solution for the problem.
3. **Implement the Decision Variant Using a SAT Solver** Implement the decision
   variant, which, for a given $c$, either finds a feasible solution with
   $|C| \leq k$ and objective value at most $c$ or proves that no such solution
   exists. Use a SAT solver for this task.
4. **Develop an Exact Solver for the Minimum Feasible $c$** Using the decision
   variant, implement an exact solver that identifies the smallest feasible $c$
   and returns the corresponding set $C$. This will require multiple calls to
   the decision variant. Implement your solution in `solution.py`. To verify
   your implementation, run `python3 verify.py` in the terminal.

> [!TIP]
>
> The number of potential optimal values for $c$ is quadratic in the number of
> nodes.

> [!NOTE]
>
> **Heuristics as Warm Starts**
>
> Developing a heuristic to quickly generate an initial solution can also
> enhance the performance of advanced solvers like CP-SAT. While this initial
> solution does not need to be optimal, closer proximity to the optimal solution
> typically results in a stronger speedup effect. Most solvers offer an
> interface to provide this solution as a **hint** or **warm start**.

> [!IMPORTANT]
>
> Proving unsatisfiability is often significantly more challenging than finding
> a feasible solution. When selecting a search strategy (e.g., up, down, binary,
> etc.), the type of calls made to the SAT solver is far more important than the
> number of calls. The optimal strategy can vary significantly depending on the
> specific problem, so it is crucial to adapt your approach accordingly.
> Additionally, if you progress sequentially from a feasible solution toward
> infeasibility, you can recycle your SAT solver state, including previously
> learned clauses, as the newly added constraints build on the existing ones.

> [!TIP]
>
> <details>
> <summary>Click here for a list of common mistakes to avoid in this exercise</summary>
>
> 1. **Not Reducing the Search Space with Each New Incumbent** When the decision
>    variant returns a solution, the objective value of that solution serves as
>    a valid upper bound for the optimization variant. Do not forget to narrow
>    the search space accordingly, rather than continuing to search for the
>    previously targeted objective value.
> 2. **Restricting the Objective Search to Integer Values** A common mistake is
>    limiting the search for objective values to integers or rounding distances
>    to large integers. Distances may not be integral, and rounding can lead to
>    inefficiencies. Instead, compute the list of all potential objective values
>    and work directly with this list.
>
> </details>

> [!TIP]
>
> <details>
> <summary>Click here for a hint on implementing a reasonable heuristic for this problem.</summary>
>
> Here is a guideline to help you implement the heuristic part if you get stuck.
> To maximize your learning, ensure you have thoroughly attempted to solve it on
> your own before referring to this hint.
>
> Add centers one by one. At each step, select the vertex farthest from all
> already chosen centers. Stop once you have selected $k$ centers. To avoid
> repeatedly computing shortest paths, use `networkx` to precompute all
> distances upfront, e.g., with `nx.all_pairs_dijkstra_path_length`. This is
> already provided in the `Distances` class.
>
> </details>

> [!TIP]
>
> <details>
> <summary>Click here for a hint on implementing the decision variant.</summary>
>
> Here is a guideline to help you implement the decision part if you get stuck.
> To maximize your learning, ensure you have thoroughly attempted to solve it on
> your own before referring to this hint.
>
> 1. Create a class for your decision solver that offers a `solve` method which
>    either returns a solution or `None` if no solution exists.
> 2. Create a mapping of vertices to variable indices, where each index
>    indicates if the corresponding vertex is selected as a center.
> 3. Add an `atmost` constraint to ensure at most $k$ centers are selected.
> 4. Implement an auxiliary function that, for a vertex $v$ and distance $l$,
>    returns the list of vertices reachable from $v$ within $l$.
> 5. Add a `limit_distance` method to your decision solver. This method should
>    take a distance `l` and enforce, for each vertex, that at least one vertex
>    within the given range (determined by the auxiliary function) is selected
>    as a center. Note that this method can be called repeatedly as long as the
>    `l` is decreasing.
>
> </details>

> [!TIP]
>
> <details>
> <summary>Click here for a hint on implementing the optimization variant.</summary>
>
> Here is a guideline to help you implement the optimization part if you get
> stuck. To maximize your learning, ensure you have thoroughly attempted to
> solve it on your own before referring to this hint.
>
> 1. Create a sorted list of all potential objective values (distances).
> 2. Run your heuristic to obtain an initial incumbent solution.
> 3. Iterate as follows:
>    1. Discard all distances that are worse than the incumbent solution.
>    2. Take the next best distance and use `limit_distance` to enforce a
>       solution with this maximum distance.
>    3. Solve the decision variant.
>    4. If infeasible, return the current incumbent solution as the optimal
>       solution.
>    5. Otherwise, update the incumbent solution.
>
> </details>

## References

- [A peek inside SAT Solvers - Jon Smock](https://www.youtube.com/watch?v=d76e4hV1iJY):
  The most important aspects of SAT solvers in half an hour.
- [networkx](https://networkx.org/documentation/stable/reference/algorithms/index.html):
  The inputs of the solvers will be weighted networkx graphs.
- [pysat](https://pysathq.github.io/): The SAT solver library we will use.
- [Propositional Calculus](https://en.wikipedia.org/wiki/Propositional_calculus):
  You should already know propositional calculus from your studies in logic.
- [SAT Solvers](https://en.wikipedia.org/wiki/SAT_solver): Wikipedia article on
  SAT solvers.
- [2hr Lecture on SAT Solving by Armin Biere](https://www.youtube.com/watch?v=Emhg0uZnbNg):
  For those who want to dive deeper into the topic.
- [4.5hr Lecture on SAT Solving by Armin Biere](https://www.youtube.com/watch?v=II2RhzwYszQ&list=PLgKuh-lKre12GSaYimhmuTsD-l41VsGQI&index=10):
  For those who want to dive even deeper into the topic.
- [History of SAT Solving - Armin Biere](https://www.youtube.com/live/DU44Y9Pt504?si=D4686hn6mi1E1Ml8):
  For those, who are interested in the historical development of SAT solvers. As
  computer science is a very fast moving field, it is always good to know how
  young the field of SAT solving actually is.
- [Facility Location Problem](https://en.wikipedia.org/wiki/Optimal_facility_location):
  This problem belongs to the class of facility location problems.
