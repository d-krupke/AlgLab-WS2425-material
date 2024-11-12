# Exercise: Bottleneck TSP Using a SAT Solver

![Symbol Image](./.figures/dalle-btsp.png)

After working hard and earning some well-deserved money, it is time to plan a
vacation. However, efficiency remains a priority, so your goal is to minimize
the longest single-day travel distance during your trip. Instead of focusing on
the total travel distance, you want to reduce the longest driving time between
any two consecutive cities, avoiding overly exhausting days.

This scenario is modeled as the **Bottleneck Traveling Salesman Problem
(BTSP)**. In this version of the TSP, you have a weighted graph where vertices
represent cities, and edges represent the connections with associated travel
times. The objective is to find a tour that visits every city exactly once and
returns to the starting city, while minimizing the maximum travel time for any
single leg of the journey, i.e., the longest connection used.

An interesting feature of BTSP, especially when solved with SAT-based
optimization, is the limited range of possible objective values. Since the
objective depends only on the weight of the longest edge in the tour, there are
at most $n^2$ possible objective values in a graph with $n$ cities. This
constrained domain contrasts with the classical TSP, where minimizing the total
tour length introduces a much larger range of potential values.

> [!NOTE]
>
> **The Dantzig-Fulkerson-Johnson Formulation for Tours**
>
> There are multiple ways to model the Hamiltonian cycle problem. One of the
> most efficient is the **Dantzig-Fulkerson-Johnson (DFJ) formulation**, which
> ensures that each subset of vertices has at least two edges exiting it. Since
> enumerating all possible subsets is impractical, these constraints are
> typically added iteratively as needed.
>
> **Parameters:**
>
> - $G = (V, E)$: A graph with vertices $V$ and edges $E$, where every pair of
>   vertices is connected by an edge.
> - $N(v)$: The set of neighbors of vertex $v$.
>
> **Decision Variables:**
>
> - $x_{vw} \in \mathbb{B} \quad \forall (v, w) \in E$: Binary variables
>   indicating whether edge $(v, w)$ is part of the Hamiltonian cycle. Since the
>   graph is undirected, $x_{vw} = x_{wv}$.
>
> **Constraints:**
>
> 1. **Degree Constraints**: Each vertex $v$ must have exactly two incident
>    edges. This will ensure that the selected edges form cycles.
>
> - $\sum_{w \in N(v)} x_{vw} = 2 \quad \forall v \in V$
>
> 2. **Subtour Elimination Constraints**: For each subset $S \subseteq V$ with
>    $|S| \geq 2$, ensure there are at least two edges exiting the subset. This
>    will ensure that the selected edges are connected, and in combination with
>    the degree constraints, form a Hamiltonian cycle.
>
> - $\sum_{(v, w) \in E, v \in S, w \notin S} x_{vw} \geq 2 \quad \forall S \subseteq V, |S| \geq 2$

## Deliverables

### Deliverable 1: Hamiltonian Cycle Solver

1. Think about if the subtour elimination constraint would also work with only
   one edge exiting the subset, which would be a common disjunctive clause.
2. Think about how to implement the Degree Constraints using the `add_atmost`
   method in PySAT.
3. Implement a solver to determine whether a given graph contains a Hamiltonian
   cycle. Place your implementation in `solution_hamiltonian.py`.
4. Test your implementation by running the script
   `python3 verify_hamiltonian.py`.

> [!IMPORTANT]
>
> Use the Dantzig-Fulkerson-Johnson formulation for efficiency. Leverage
> `nx.connected_components` from the `networkx` library to identify connected
> components and incrementally add clauses to ensure each component has an edge
> leaving it.

### Deliverable 2: Bottleneck Traveling Salesman Problem (BTSP) Solver

1. Develop a solver to find the optimal solution to the Bottleneck Traveling
   Salesman Problem (BTSP). Implement this in `solution_btsp.py`. You can access
   edge weights in NetworkX using `graph.edges[e]["weight"]`. Use a binary
   search on the sorted edge weights to find the smallest value $t$ for which
   the graph $G = (V, \{(v, w) \mid v, w \in V, \text{ weight}(v, w) \leq t \})$
   contains a Hamiltonian cycle. This will yield the optimal solution to the
   BTSP.
2. Verify your implementation by executing `python3 verify_btsp.py`.

> [!TIP]
>
> <details>
> <summary>Click here for a list of common mistakes to avoid in this exercise</summary>
>
> 1. **Using Simplified Constraints Instead of the Dantzig-Fulkerson-Johnson
>    (DFJ) Formulation** A common mistake is to replace the DFJ formulation with
>    a simpler constraint that only prohibits cycles of length $|C|$ by
>    enforcing $\sum_{(i, j) \in C} x_{ij} \leq |C| - 1$, resp., adding a clause
>    prohibiting one of the edges. While this constraint is often introduced in
>    the literature as a first step, it is exponentially weaker than the DFJ
>    formulation. The DFJ formulation also prohibits any permutations of a
>    cycle, making it much more effective for finding valid Hamiltonian cycles.
> 2. **Not Reducing the Search Space with Every New Incumbent** Remember that
>    you can not only reduce the search space by the value you queried but
>    directly to the objective value you found. This can drastically reduce the
>    number of queries to your decision variant.
> 3. **Trying to use cardinality constraints for the subtour elimination
>    constraints** Cardinality constraints are much more expensive than common
>    clauses. While the $\geq 2$ constraint can be implemented with cardinality
>    constraints and is actually more accurate, $\geq 1$ is actually sufficient
>    and can be implemented with common clauses.
> 4. **Restricting the Objective Search to Integer Values** Another frequent
>    error is limiting the search for the objective to integer values or
>    attempting to round edge weights to large integers. Edge weights are not
>    always integral, and rounding can lead to inaccuracies. Although a
>    sufficiently high resolution might allow tests to pass, this approach is
>    likely to be too slow for larger instances. Make sure to work directly with
>    the original edge weights to achieve accurate and efficient results.
> 5. **Attempting to Add All Subtour Elimination Constraints at Once** A
>    frequent mistake is trying to add all subtour elimination constraints at
>    the start of the optimization process, rather than adding them dynamically
>    as needed. Since there is an exponential number of these constraints,
>    adding them all upfront makes the optimization process prohibitively slow.
>    Instead, add subtour elimination constraints only for detected subtours
>    during the optimization process to improve efficiency.
>
> </details>

## References

- [A peek inside SAT Solvers - Jon Smock](https://www.youtube.com/watch?v=d76e4hV1iJY):
  The most important aspects of SAT solvers in half an hour.
- [networkx](https://networkx.org/documentation/stable/reference/algorithms/index.html):
  The inputs of the solvers will be weighted NetworkX graphs.
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
  For those interested in the historical development of SAT solvers. As computer
  science is a very fast-moving field, it is always helpful to understand how
  young the field of SAT solving actually is.
- [Bottleneck Traveling Salesman Problem](https://en.wikipedia.org/wiki/Bottleneck_traveling_salesman_problem)
