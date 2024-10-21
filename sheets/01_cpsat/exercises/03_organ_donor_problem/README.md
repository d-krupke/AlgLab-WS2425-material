# Exercise: Maximizing Crossover Transplantations

![Symbol Image](./.assets/dalle-transpl.png)

Your client is a healthcare organization managing an organ transplant program.
Organ transplantation is critical for patients with end-stage organ failure, but
finding compatible donors is a significant challenge. To address this, the
organization runs a **crossover transplantation program**, where pairs of
incompatible donor-recipient pairs exchange organs with other pairs to maximize
compatibility.

In this system, a donor who is incompatible with their intended recipient agrees
to donate to another patient, provided their associated recipient receives an
organ from a different, compatible donor. By optimizing these exchanges, the
program reduces waiting times and increases the number of successful
transplantations.

Your task is to help the client maximize the number of successful
transplantations by identifying the best matches among donor-recipient pairs
based on compatibility, while adhering to certain operational constraints.

---

### Formal Problem Definition

You are given a set of donor-recipient pairs with specific compatibility
parameters, and your objective is to maximize the number of successful crossover
transplantations.

**Input:**

- A list of $n$ donor-recipient pairs, labeled
  $(d_1, r_1), (d_2, r_2), \ldots, (d_n, r_n)$.

  - The set of donors is $D = \{d_1, d_2, \ldots, d_n\}$.
  - The set of recipients is $R = \{r_1, r_2, \ldots, r_n\}$. Recipients can
    appear more than once, e.g., $r_1 = r_3$, but donors are unique, i.e.,
    $\forall i \neq j: d_i \neq d_j$.

- A compatibility function $f: D \times R \rightarrow \mathbb{B}$, where
  $f(d_i, r_j)$ is 1 if donor $d_i$ is compatible with recipient $r_j$, and 0
  otherwise.

**Constraints:**

1. A donor can donate only once.
2. A recipient can receive only one organ.
3. A donor is willing to donate only if their associated recipient receives an
   organ in exchange.

**Objective:**

Maximize the number of successful transplantations, ensuring that all
constraints are satisfied.

---

### Deliverables

#### 1. **Mathematical Model**

The first task is to create a mathematical model for this problem, defining the
necessary variables, objective function, and constraints in a way that aligns
with the capabilities of CP-SAT.

- What are the decision variables for this problem?
- What is the objective function to maximize?
- What constraints must be respected?

**Hint**: Focus on Boolean variables and linear constraints to make the model
compatible with CP-SAT.

---

#### 2. **Solver Implementation in CP-SAT**

Once the mathematical model is defined, your next task is to implement a solver
using CP-SAT.

**Steps:**

1. Review the provided framework in `solution_basic.py`. The donor-recipient
   pair data is available via a database.
2. Extend the framework to implement a solver that maximizes the number of
   successful transplantations, based on the model you created.
3. Verify your solution by running the tests with `python3 verify_basic.py`. You
   can also use the simple visualizer (`python3 visualization.py`) to help debug
   your model.

**Hint**: Be mindful of inefficient loops. Use the `get_compatible_recipients`
and `get_compatible_donors` functions to reduce unnecessary checks and improve
performance.

---

### Client Feedback: Limiting Surgery Cycle Sizes

After presenting your solution, the client identified an additional operational
constraint. Due to limited operating room availability, all transplant surgeries
must be performed in parallel, ensuring that no donor changes their mind. This
means that no transplantation cycle can involve more than 3 donor-recipient
pairs.

Your task is to modify your solver to incorporate this cycle size limit,
ensuring that each cycle includes at most 3 transplantations.

**Steps:**

1. Implement a new solver in `solver_small_cycles.py` that restricts the size of
   transplantation cycles to a maximum of 3 pairs.
2. Test your updated solver using `python3 verify_small_cycles.py`.

**Hint**: Start by creating the set of transplantation cycles
$\mathcal{C}_{2,3}$ of size 2 and 3. Create variables for each cycle, and avoid
reusing the previous model. Check the references for algorithms that only
generate (directed) cycles of a specific size.

---

### Additional Information: Column Generation

In practice, restricting cycles to a small length (such as 2 or 3) is feasible
for small problems, but as the number of donor-recipient pairs increases, larger
cycles can be beneficial. However, creating variables for all possible cycles
becomes computationally impractical due to the **combinatorial explosion** of
possible cycles.

For larger cycles, a more sophisticated approach known as **column generation**
can be employed. This method involves iteratively solving the problem by
focusing on a subset of promising cycles, solving the model, and then adding
more cycles as needed. In essence, the model does not consider all possible
cycles upfront; instead, it dynamically generates new cycles based on
intermediate solutions, improving efficiency.

This technique, while powerful, requires a deep understanding of duality and
linear programming, which is beyond the scope of this exercise. However, it is
commonly used in advanced optimization problems and will be covered in more
detail in future courses such as our advanced MMA course.

---

### References

- [How OR helps kidney patients UK](https://www.theorsociety.com/ORS/ORS/About-OR/Case-Studies/How-OR-helps-kidney-patients-UK.aspx)
- [Mathematical Modelling](https://www.gurobi.com/resources/math-programming-modeling-basics/):
  A crash-course in mathematical modeling.
- [pydantic](https://docs.pydantic.dev/latest/): A popular library for data
  validation and serialization in Python.
- [networkx](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cycles.simple_cycles.html):
  Documentation for the `simple_cycle` function in the `networkx` library, which
  may be useful for identifying cycles in the second task.
- [CP-SAT Primer](https://github.com/d-krupke/cpsat-primer): Our primer on
  CP-SAT.
- [pre-commit](https://pre-commit.com/): A tool for running code formatting and
  checks before commits.
- [Git LFS](https://git-lfs.com/): Used for storing large files such as test
  instances.