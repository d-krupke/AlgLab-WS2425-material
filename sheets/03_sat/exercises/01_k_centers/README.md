# Exercise: k-centers using a SAT-solver

### 01. Vertex K-Centers

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
> The number of potential optimal values for $c$ is quadratic in the number of nodes.

> [!NOTE]
>
> **Heuristics as Warm Starts**
>
> Developing a heuristic to quickly generate an initial solution can also
> enhance the performance of advanced solvers like CP-SAT. While this initial
> solution does not need to be optimal, closer proximity to the optimal solution
> typically results in a stronger speedup effect. Most solvers offer an
> interface to provide this solution as a **hint** or **warm start**.

> [!TIP]
>
> <details>
> <summary>Click here for a list of common mistakes to avoid in this exercise</summary>
>
> 1. **Encoding Shortest Paths within the SAT Formulation** A common error is
>    attempting to let the SAT solver compute shortest paths as part of the
>    solution. Remember, the SAT solver is not meant to handle shortest-path
>    computations. It is absolutely fine to preprocess the graph and compute all
>    shortest paths before formulating the SAT constraints, as path lengths are
>    not part of the decisions in this problem.
> 2. **Overlooking the Center Vertex in Distance Calculations** When identifying
>    which vertices are within a given distance of a potential center, do not
>    forget that the center vertex itself is always within zero distance. Be
>    sure to include the center vertex in the set of reachable vertices within
>    the specified distance.
> 3. **Restricting the Objective Search to Integer Values** Another frequent
>    error is limiting the search for the objective to integer values or
>    attempting to round distances to large integers. The distances may not be
>    integral and rounding can be highly inefficient. Compute the list of
>    possible objective values first and work directly on this list.
>
> </details>

> [!TIP]
>
> <details>
>  <summary>Click here for a hint on how to implement a reasonable heuristic for this problem.</summary>
> Add the centers one by one. Always add a center at the vertex which is most distanced to all already selected centers. Stop as soon as you reached $k$ centers.
> In order not to compute too many shortest paths repeatedly, use networkx to compute all distances in the beginning, e.g., with `nx.all_pairs_dijkstra_path_length`.
> </details>

> [!TIP]
>
> <details>
> <summary>Click here for a hint on how to implement the decision variant.</summary>
>
> 1. Create a container that maps every vertex to a variable index, which we will use to indicate if this vertex has been selected as center.
> 2. Add an `atmost` constraint on all these variables that at most $k$ of them are allowed to be true.
> 3. Create an auxiliary function that returns you for a vertex $v$ and a distance $l$ the list of vertices that are in reach of $v$ within $l$.
> 4. Create a `limit_distance` method to you decision solver that takes a distance `l` and adds for every vertex a clause that one of the vertices in range (given by the auxiliary function) needs to be True.
>
> </details>

> [!TIP]
> 
> <details>
> <summary>Click here for a hint on how to implement the optimization variant.</summary>
>
> 1. Create a sorted list of all the distances that may still be better than the solution of your heuristic.
> 2. Create a while loop that takes the next best distance in your list and uses the `limit_distance` with it to enforce a solution that has at most this distance.
> 2. Solve the decition variant. If it is infeasible, return the pervious solution as the optimal solution. Otherwise, save the solution as best solution and do the next loop after poping the last distance.
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
- [Facility Location Problem](https://en.wikipedia.org/wiki/Optimal_facility_location)
- [Git LFS](https://git-lfs.com/): The instances are stored using Git LFS. You
  may need to install it as otherwise the instances will be empty and result in
  an error.
