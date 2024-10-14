# Exercise Sheet 01 (A+B): Constraint Programming with CP-SAT

_Algorithms Lab Winter 2024/2025 - Dr. Dominik Krupke, TU Braunschweig, IBR,
Algorithms Group_

You probably already know SQL as a way to declaratively work with data: Describe
which data you want, and the database system will try to provide them as quickly
as possible. Now imagine the same for optimization problems: Describe the
variables, an objective (a score for how good a solution is), and constraints
that have to be satisfied, and the system tries to provide you with the best
variable assignment (i.e., solution) satisfying all constraints. Of course, this
is a significantly harder task as the system may have to solve NP-hard problems.
Such a system also gets pretty close to generic artificial intelligence that can
solve any problem you state. While you cannot expect such a system to work for
all problems you state, there actually exist some that are powerful enough for
many real problems. The general term for this is _Constraint Programming_, but
things are not as much standardized as for databases and the implementations
vary a lot. Here, we will learn how to use
[CP-SAT](https://developers.google.com/optimization/cp/cp_solver) of
[Google's ortools-suite](https://developers.google.com/optimization) to solve
combinatorial optimization problems.

## Installation

The installation of CP-SAT, which is part of the ortools package, is very easy
and can be done via pip.

```shell
pip install -U ortools
```

This command will also update an existing installation of ortools. As this tool
is in active development, it is recommendable to update it frequently. We
actually encountered wrong behavior, i.e., bugs, in earlier versions that then
have been fixed by updates (this was on some more advanced features, don't worry
about correctness with basic usage).

You may ask why we are using a tool that is still in active development. The
reason is that CP-SAT is not only one of the most powerful constraint solvers
available, but also very easy to install and use.

You will also commonly need the networkx and matplotlib libraries. You can
install them via pip as well.

```shell
pip install networkx matplotlib
```

[NetworkX](https://networkx.org/) is a very useful graph library, which
implements many useful data structures and algorithms associated with problems
rooted in graph theory. It is purely written in Python, which makes it rather
slow in certain cases. But, it will suffice for our needs.

[Matplotlib](https://matplotlib.org/) is a comprehensive library for creating
static, animated, and interactive visualizations in Python. We will mostly use
it to plot graph drawings and visualize solutions to the optimization problems
we aim to solve.

## What hardware do you need?

It is important to note that for CP-SAT usage, you do not need the capabilities
of a supercomputer. A standard laptop is often sufficient for solving many
problems. The primary requirements are CPU power and memory bandwidth, with a
GPU being unnecessary.

In terms of CPU power, the key is balancing the number of cores with the
performance of each individual core. CP-SAT leverages all available cores by
default, implementing different strategies on each.
[Depending on the number of cores, CP-SAT will behave differently](https://github.com/google/or-tools/blob/main/ortools/sat/docs/troubleshooting.md#improving-performance-with-multiple-workers).
However, the effectiveness of these strategies can vary, and it is usually not
apparent which one will be most effective. A higher single-core performance
means that your primary strategy will operate more swiftly. I recommend a
minimum of 4 cores and 16GB of RAM.

While CP-SAT is quite efficient in terms of memory usage, the amount of
available memory can still be a limiting factor in the size of problems you can
tackle. When it came to setting up our lab for extensive benchmarking at TU
Braunschweig, we faced a choice between desktop machines and more expensive
workstations or servers. We chose desktop machines equipped with AMD Ryzen 9
7900 CPUs (Intel would be equally suitable) and 96GB of DDR5 RAM, managed using
Slurm. This decision was driven by the fact that the performance gains from
higher-priced workstations or servers were relatively marginal compared to their
significantly higher costs. When on the road, I am often still able to do stuff
with my old Intel Macbook Pro from 2018 with an i7 and only 16GB of RAM, but
large models will overwhelm it. My workstation at home with AMD Ryzen 7 5700X
and 32GB of RAM on the other hand rarely has any problems with the models I am
working on.

For further guidance, consider the
[hardware recommendations for the Gurobi solver](https://support.gurobi.com/hc/en-us/articles/8172407217041-What-hardware-should-I-select-when-running-Gurobi-),
which are likely to be similar. Since we frequently use Gurobi in addition to
CP-SAT, our hardware choices were also influenced by their recommendations.

## Example

Before we dive into any internals, let us take a quick look at a simple
application of CP-SAT. This example is so simple that you could solve it by
hand, but know that CP-SAT would (probably) be fine with you adding a thousand
(maybe even ten- or hundred-thousand) variables and constraints more. The basic
idea of using CP-SAT is, analogous to MIPs, to define an optimization problem in
terms of variables, constraints, and objective function, and then let the solver
find a solution for it. We call such a formulation that can be understood by the
corresponding solver a _model_ for the problem. For people not familiar with
this
[declarative approach](https://programiz.pro/resources/imperative-vs-declarative-programming/),
you can compare it to SQL, where you also just state what data you want, not how
to get it. However, it is not purely declarative, because it can still make a
huge(!) difference how you model the problem and getting that right takes some
experience and understanding of the internals. You can still get lucky for
smaller problems (let us say a few hundred to thousands of variables) and obtain
optimal solutions without having an idea of what is going on. The solvers can
handle more and more 'bad' problem models effectively with every year.

> [!NOTE]
>
> A **model** in mathematical programming refers to a mathematical description
> of a problem, consisting of variables, constraints, and optionally an
> objective function that can be understood by the corresponding solver class.
> _Modelling_ refers to transforming a problem (instance) into the corresponding
> framework, e.g., by making all constraints linear as required for Mixed
> Integer Linear Programming. Be aware that the
> [SAT](https://en.wikipedia.org/wiki/SAT_solver)-community uses the term
> _model_ to refer to a (feasible) variable assignment, i.e., solution of a
> SAT-formula. If you struggle with this terminology, maybe you want to read
> this short guide on
> [Math Programming Modelling Basics](https://www.gurobi.com/resources/math-programming-modeling-basics/).

Our first problem has no deeper meaning, except for showing the basic workflow
of creating the variables (x and y), adding the constraint $x+y<=30$ on them,
setting the objective function (maximize $30x + 50y$), and obtaining a solution:

```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Variables
x = model.new_int_var(0, 100, "x")
y = model.new_int_var(0, 100, "y")

# Constraints
model.add(x + y <= 30)

# Objective
model.maximize(30 * x + 50 * y)

# Solve
solver = cp_model.CpSolver()
status_code = solver.solve(model)
status_name = solver.status_name()

# Print the solver status and the optimal solution.
print(f"{status_name} ({status_code})")
print(f"x={solver.value(x)},  y={solver.value(y)}")
```

    OPTIMAL (4)
    x=0,  y=30

Pretty easy, right? For solving a generic problem, not just one specific
instance, you would of course create a dictionary or list of variables and use
something like `model.add(sum(vars)<=n)`, because you do not want to create the
model by hand for larger instances.

> [!TIP]
>
> The solver can return five different statuses:
>
> | Status          | Code | Description                                                                                                                                                                           |
> | --------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `UNKNOWN`       | 0    | The solver has not run for long enough.                                                                                                                                               |
> | `MODEL_INVALID` | 1    | The model is invalid. You will rarely see that status.                                                                                                                                |
> | `FEASIBLE`      | 2    | The model has a feasible, but not necessarily optimal, solution. If your model does not have an objective, every feasible model will return `OPTIMAL`, which may be counterintuitive. |
> | `INFEASIBLE`    | 3    | The model has no feasible solution. This means that your constraints are too restrictive.                                                                                             |
> | `OPTIMAL`       | 4    | The model has an optimal solution. If your model does not have an objective, `OPTIMAL` is returned instead of `FEASIBLE`.                                                             |
>
> The status `UNBOUNDED` does _not_ exist, as CP-SAT does not have unbounded
> variables.

For larger models, CP-SAT will unfortunately not always able to compute an
optimal solution. However, the good news is that the solver will likely still
find a satisfactory solution and provide a bound on the optimal solution. Once
you reach this point, understanding how to interpret the solver's log becomes
crucial for analyzing the solver's performance. We will learn more about this
later.

### Mathematical Model

The mathematical model of the code above would usually be written by experts
something like this:

```math
\max 30x + 50y
```

```math
\text{s.t. } x+y \leq 30
```

```math
\quad 0\leq x \leq 100
```

```math
\quad 0\leq y \leq 100
```

```math
x,y \in \mathbb{Z}
```

The `s.t.` stands for `subject to`, sometimes also read as `such that`.

### Overloading

One aspect of using CP-SAT solver that often poses challenges for learners is
understanding operator overloading in Python and the distinction between the two
types of variables involved. In this context, `x` and `y` serve as mathematical
variables. That is, they are placeholders that will only be assigned specific
values during the solving phase. To illustrate this more clearly, let us explore
an example within the Python shell:

```pycon
>>> model = cp_model.CpModel()
>>> x = model.new_int_var(0, 100, "x")
>>> x
x(0..100)
>>> type(x)
<class 'ortools.sat.python.cp_model.IntVar'>
>>> x + 1
sum(x(0..100), 1)
>>> x + 1 <= 1
<ortools.sat.python.cp_model.BoundedLinearExpression object at 0x7d8d5a765df0>
```

In this example, `x` is not a conventional number but a placeholder defined to
potentially assume any value between 0 and 100. When 1 is added to `x`, the
result is a new placeholder representing the sum of `x` and 1. Similarly,
comparing this sum to 1 produces another placeholder, which encapsulates the
comparison of the sum with 1. These placeholders do not hold concrete values at
this stage but are essential for defining constraints within the model.
Attempting operations like `if x + 1 <= 1: print("True")` will trigger a
`NotImplementedError`, as the condition `x+1<=1` cannot be evaluated directly.

Although this approach to defining models might initially seem perplexing, it
facilitates a closer alignment with mathematical notation, which in turn can
make it easier to identify and correct errors in the modeling process.

### More examples

If you are not yet satisfied,
[this folder contains many Jupyter Notebooks with examples from the developers](https://github.com/google/or-tools/tree/stable/examples/notebook/sat).
For example

- [multiple_knapsack_sat.ipynb](https://github.com/google/or-tools/blob/stable/examples/notebook/sat/multiple_knapsack_sat.ipynb)
  shows how to solve a multiple knapsack problem.
- [nurses_sat.ipynb](https://github.com/google/or-tools/blob/stable/examples/notebook/sat/nurses_sat.ipynb)
  shows how to schedule the shifts of nurses.
- [bin_packing_sat.ipynb](https://github.com/google/or-tools/blob/stable/examples/notebook/sat/bin_packing_sat.ipynb)
  shows how to solve a bin packing problem.
- ... (if you know more good examples I should mention here, please let me
  know!)

Further, you can find an extensive and beginner-friendly example on scheduling
workers
[here](https://pganalyze.com/blog/a-practical-introduction-to-constraint-programming-using-cp-sat).

In the [more extensive primer](https://d-krupke.github.io/cpsat-primer/) you can
find what options you have to model a problem. Note that an experienced
optimizer may be able to model most problems with just the elements shown above,
but showing your intentions may help CP-SAT optimize your problem better.

## Example: 0-1-Knapsack

You are given a knapsack that can carry a certain weight limit $C$, and you have
various items $I$ you can put into it. Each item $i\in I$ has a weight $w_i$ and
a value $v_i$. The goal is to pick items to maximize the total value while
staying within the weight limit. We can express this problem mathematically, by
introducing a _decision variable_ $x_i\in \{0,1\}$ for each item $i\in I$ that
states whether the item is in the knapsack or not. Then, we can write the
mathematical problem formulation as follows:

$$\max \sum_{i \in I} v_i x_i$$

$$\text{s.t.} \sum_{i \in I} w_i x_i \leq C$$

$$\forall i\in I: x_i \in \{0,1\}$$

A model usually consists of the following parts:

1. Decision variables (here: $x_i$)
2. Constraints (here only: $\sum_{i \in I} w_i x_i \leq C$)
3. An objective function (here: $\sum_{i \in I} v_i x_i$)

Let us try to implement this model with CP-SAT. There are a few important steps:

1. Creating a boolean variable for each item, which indicates whether it is in
   the knapsack or not.
2. Creating the weight constraint.
3. Creating the objective.
4. Setting up the solver.
5. Solving the model.
6. Returning the solution.

```python
from ortools.sat.python import cp_model
from collections import namedtuple

Item = namedtuple("Item", ["weight", "value"])


class KnapsackModel:
    def __init__(self, items, capacity):
        self.items = items
        self.model = cp_model.CpModel()
        # 1. Create a boolean variable for each item
        self.x = [self.model.NewBoolVar(f"x_{i}") for i in range(len(items))]
        # 2. Create the weight constraint
        self.model.Add(sum(x * i.weight for x, i in zip(self.x, items)) <= capacity)
        # 3. Create the objective
        self.model.Maximize(sum(x * i.value for x, i in zip(self.x, items)))

    def solve(self):
        # 4, Create the solver
        solver = cp_model.CpSolver()
        # Enabling logging will show us the progress of the search
        solver.parameters.log_search_progress = True
        # 5. Solve the model
        status = solver.Solve(self.model)
        # 6. Check and return the solution
        assert status == cp_model.OPTIMAL
        return [solver.Value(x) for x in self.x]


if __name__ == "__main__":
    items = [Item(10, 10), Item(20, 20), Item(30, 30)]
    capacity = 50
    model = KnapsackModel(items, capacity)
    solution = model.solve()
    print("===========================")
    print("Solution:")
    for i, x in enumerate(solution):
        if x:
            print(f"Item {i} is in the knapsack.")
        else:
            print(f"Item {i} is not in the knapsack.")
    assert solution == [0, 1, 1]
```

When we solve this model, we get the following output, which may look
overwhelming in the beginning:

    Starting CP-SAT solver v9.7.2996
    Parameters: log_search_progress: true
    Setting number of workers to 16

    Initial optimization model '': (model_fingerprint: 0xe6c7f45766634620)
    #Variables: 3 (#bools: 3 in objective)
    - 3 Booleans in [0,1]
    #kLinear3: 1

    Starting presolve at 0.00s
    [ExtractEncodingFromLinear] #potential_supersets=0 #potential_subsets=0 #at_most_one_encodings=0 #exactly_one_encodings=0 #unique_terms=0 #multiple_terms=0 #literals=0 time=5.71e-07s
    [Symmetry] Graph for symmetry has 3 nodes and 0 arcs.
    [Symmetry] Symmetry computation done. time: 7.704e-06 dtime: 1.8e-07
    [DetectDuplicateConstraints] #duplicates=0 #without_enforcements=0 time=4.799e-06s
    [DetectDominatedLinearConstraints] #relevant_constraints=0 #work_done=0 #num_inclusions=0 #num_redundant=0 time=5.01e-07s
    [ProcessSetPPC] #relevant_constraints=0 #num_inclusions=0 work=0 time=9.22e-07s
    [FindBigHorizontalLinearOverlap] #blocks=0 #saved_nz=0 #linears=0 #work_done=0/1e+09 time=3.1e-07s
    [FindBigVerticalLinearOverlap] #blocks=0 #nz_reduction=0 #work_done=0 time=1.7e-07s
    [MergeClauses] #num_collisions=0 #num_merges=0 #num_saved_literals=0 work=0/100000000 time=8.11e-07s
    [Symmetry] Graph for symmetry has 3 nodes and 0 arcs.
    [Symmetry] Symmetry computation done. time: 2.585e-06 dtime: 1.8e-07
    [DetectDuplicateConstraints] #duplicates=0 #without_enforcements=0 time=1.753e-06s
    [DetectDominatedLinearConstraints] #relevant_constraints=0 #work_done=0 #num_inclusions=0 #num_redundant=0 time=2.1e-07s
    [ProcessSetPPC] #relevant_constraints=0 #num_inclusions=0 work=0 time=3.4e-07s
    [FindBigHorizontalLinearOverlap] #blocks=0 #saved_nz=0 #linears=0 #work_done=0/1e+09 time=7e-08s
    [FindBigVerticalLinearOverlap] #blocks=0 #nz_reduction=0 #work_done=0 time=1.4e-07s
    [MergeClauses] #num_collisions=0 #num_merges=0 #num_saved_literals=0 work=0/100000000 time=2.71e-07s
    [ExpandObjective] #propagations=0 #entries=0 #tight_variables=0 #tight_constraints=0 #expands=0 #issues=0 time=1.172e-06s

    Presolve summary:
    - 0 affine relations were detected.
    - rule 'independent linear: solved by DP' was applied 1 time.
    - rule 'linear: divide by GCD' was applied 1 time.
    - rule 'linear: simplified rhs' was applied 1 time.
    - rule 'objective: variable not used elsewhere' was applied 3 times.
    - rule 'presolve: 3 unused variables removed.' was applied 1 time.
    - rule 'presolve: iteration' was applied 2 times.

    Presolved optimization model '': (model_fingerprint: 0xff7559ba82d6f157)
    #Variables: 0 ( in objective)


    Preloading model.
    #Bound   0.00s best:-inf  next:[50,50]    initial_domain
    [Symmetry] Graph for symmetry has 0 nodes and 0 arcs.
    #Model   0.00s var:0/0 constraints:0/0

    Starting search at 0.00s with 16 workers.
    6 full problem subsolvers: [default_lp, less_encoding, max_lp, no_lp, quick_restart, quick_restart_no_lp]
    8 first solution subsolvers: [jump, jump_decay_perturb, jump_decay_rnd_on_rst, jump_no_rst, random(2), random_quick_restart(2)]
    2 incomplete subsolvers: [feasibility_pump, rins/rens]
    2 helper subsolvers: [neighborhood_helper, synchronization_agent]
    #1       0.00s best:50    next:[]         default_lp fixed_bools:0/0
    #Done    0.00s default_lp
    #Done    0.00s less_encoding

    Task timing                        n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
    'synchronization_agent':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
        'neighborhood_helper':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
                'default_lp':         1 [106.26us, 106.26us] 106.26us   0.00ns 106.26us         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
            'less_encoding':         1 [116.92us, 116.92us] 116.92us   0.00ns 116.92us         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
                    'no_lp':         1 [ 67.20us,  67.20us]  67.20us   0.00ns  67.20us         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
                    'max_lp':         1 [103.14us, 103.14us] 103.14us   0.00ns 103.14us         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
            'quick_restart':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
        'quick_restart_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
        'feasibility_pump':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
                'rins/rens':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns

    Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
            'default_lp':      0          0         0         0           0              1
            'less_encoding':      0          0         0         0           0              1
                    'no_lp':      0          0         0         0           0              0
                'max_lp':      0          0         0         0           0              0
            'quick_restart':      0          0         0         0           0              0
    'quick_restart_no_lp':      0          0         0         0           0              0

    LNS stats       Improv/Calls  Closed  Difficulty  TimeLimit
    'rins/rens':           0/0      0%        0.50       0.10

    Solutions (1)    Num   Rank
    'default_lp':    1  [1,1]

    Objective bounds     Num
    'initial_domain':    1

    Solution repositories    Added  Queried  Ignored  Synchro
    'feasible solutions':      0        0        0        0
            'lp solutions':      0        0        0        0
                    'pump':      0        0

    CpSolverResponse summary:
    status: OPTIMAL
    objective: 50
    best_bound: 50
    integers: 0
    booleans: 0
    conflicts: 0
    branches: 0
    propagations: 0
    integer_propagations: 0
    restarts: 0
    lp_iterations: 0
    walltime: 0.00280518
    usertime: 0.00280529
    deterministic_time: 0
    gap_integral: 0
    solution_fingerprint: 0x50a599cdc5daff51

    ===========================
    Solution:
    Item 0 is not in the knapsack.
    Item 1 is in the knapsack.
    Item 2 is in the knapsack.

These logs are extremely valuable when trying to solve really difficult
problems. After a while, you will see patterns and understand what is going on,
allowing you to improve your models accordingly. You can use the
[CP-SAT Log Analyzer](https://cpsat-log-analyzer.streamlit.app/) to
interactively explore the logs.

## Exercises

Solve the following four exercises (they are considered as two different sheets,
meant for two different weeks):

### Part A:

1. [Exercise: Foobar](./exercises/00_foobar/) A simple exercise to get familiar
   with our workflow.
2. [Exercise: Scalene](./exercises/01_profiling_exercise/) Learn about profiling
   and networkx by fixing the worst code I have every written!

### Part B:

3. [Exercise: Multi-Knapsack](./exercises/02_multi_knapsack/) A more complex
   problem that requires you to model a multi-knapsack problem and solve it
   using CP-SAT.
4. [Exercise: Crossover Transplantation](./exercises/03_organ_donor_problem/) A
   problem that is less abstract and asks you to model and solve a real-world
   problem with CP-SAT.

## Hints

To guide you in tackling the exercises effectively, consider the following
hints:

1. **Utilize Basic Model Elements**: All exercises can be successfully solved
   using the fundamental elements of CP-SAT introduced earlier. While CP-SAT
   does have more advanced features and complex constraints, they are not
   essential for these exercises. Utilizing them might not necessarily simplify
   your model or boost its performance. The aim is to understand and apply the
   basic principles effectively.

2. **Start Simple**: Initially, opt for the simplest modeling approach that
   comes to mind. Don't worry if it seems inefficient at first. It's often more
   effective to start with a basic model and refine it as needed. Remember, your
   initial assumptions about the solver's runtime may not be accurate.
   Surprisingly, larger models with straightforward constraints often outperform
   smaller, more complex ones. CP-SAT can efficiently handle models with a high
   number (sometimes millions) of variables, provided the structure remains
   relatively simple. Keep in mind that the time taken to create the model in
   Python can be a significant factor.

3. **Focus on Linear Expressions and Boolean Variables**: Aim to primarily use
   linear expressions and boolean variables. A linear expression typically
   involves a sum of variables, each multiplied by a constant. For the scope of
   these exercises, there should be no need to venture beyond these types of
   variables and constraints. Sticking to this approach will help maintain
   clarity and efficiency in your models.

4. **There are more than one way to model a problem**: There are often multiple
   ways to model a problem. The performance differences between these models can
   be significant. If your model is not performing well enough to satisfy the
   verification tests, consider rethinking your approach. Are there alternative
   ways to implement the constraints? Can different variables be used?
