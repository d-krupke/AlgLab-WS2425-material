# Exercise Overview

## 1. [CP-SAT / Constraint Programming](./01_cpsat/)

### 1.1 [Foobar](./01_cpsat/exercises/00_foobar/)

**Objective**:

- Practice using a declarative problem description, resisting the urge to
  compute the solution manually.
- Familiarize yourself with the verification script.

---

### 1.2 [Profiling](./02_branch_and_bound/exercises/01_profiling_exercise/)

**Objective**:

- Understand the limitations of polynomial complexity by analyzing the
  impracticality of an $O(n^3)$ for-loop.
- Learn to identify performance bottlenecks using a profiler.
- Gain a basic introduction to graph manipulation in Python.
- Appreciate the importance of understanding algorithm operations to fully
  exploit their efficiency and avoid redundant work.

---

### 1.3 [Multi-Knapsack](./01_cpsat/exercises/02_multi_knapsack/)

**Objective**:

- Explore the formulation of a more complex problem derived from the familiar
  Knapsack problem.
- Introduce the use of auxiliary variables to enhance modeling capabilities.

---

### 1.4 [Organ Donor](./01_cpsat/exercises/03_organ_donor_problem/)

**Objective**:

- Practice graph-based modeling, a crucial abstraction in optimization.
- Learn to compose decisions into aggregated decision variables, such as
  focusing on complete transplantation cycles instead of individual transplants.

---

## 2. [Branch and Bound](./02_bnb/)

### 2.1 [DIY Branch and Bound](./02_bnb/)

**Objective**:

- Recap the Branch and Bound algorithm.
- Experience how small optimizations can significantly reduce the size of the
  search tree.

---

## 3. [SAT](./03_sat/)

### 3.1 [k-Centers](./03_sat/exercises/01_k_centers/)

**Objective**:

- Use a SAT-solver for optimization tasks.
- Learn the concepts of warm-starts.
- Understand the differing complexities of proving versus disproving
  feasibility.

---

### 3.2 [BTSP](./03_sat/exercises/02_hc_btsp/)

**Objective**:

- Familiarize yourself with the DFJ formulation, a cornerstone for tour
  problems.
- Adapt formulations to suit the solver being used.
- Gain additional experience with graph algorithms.

---

## 4. [Mixed Integer Programming](./04_mip/)

### 4.1 [TSP](./04_mip/exercises/01_tsp/)

**Objective**:

- Work on the Traveling Salesperson Problem (TSP), one of the oldest and most
  common exercises in optimization.
- Learn the general use of a Mixed Integer Programming (MIP) solver.
- Understand the reliance of MIP solvers on linear relaxations.

---

### 4.2 [Flow](./04_mip/exercises/02_flow/)

**Objective**:

- Explore the flow problem, a common application in optimization.
- Learn about optimality gaps and optimality tolerances.
- Gain additional training in modeling and Mixed Integer Programming.
