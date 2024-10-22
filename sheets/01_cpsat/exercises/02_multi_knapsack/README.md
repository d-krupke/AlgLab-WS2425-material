# Exercise: Multi-Knapsack Optimization

![Symbol Image](./.assets/dalle-multiknapsack.png)

Your client runs a logistics company managing a fleet of trucks, each with a
specific weight limit. They need to efficiently distribute cargo among the
trucks to maximize the value of the loaded items without exceeding truck
capacities. Additionally, they cannot pack all cargo items due to space
limitations, so deciding which items to leave out is part of the challenge.

Your task is to develop a solution that optimizes the arrangement of cargo in
trucks while maximizing the total value, and respecting each truck’s weight
limit.

---

## Deliverables

### 1. **Mathematical Model**

The first step is to generalize the basic knapsack problem to the multi-knapsack
scenario, where multiple trucks (knapsacks) are involved.

- What are the variables in this problem?
- What is the objective function?
- What constraints do you need to consider?

**Hint**: Assume that $K$ is the set of trucks, and $C_i$ represents the
capacity of truck $i, i\in K$. Use the knapsack model as a
reference.

<details>
   <summary>Click here for a fill-in-the-blank exercise to help you model the problem.</summary>
   
#### Parameters:

- $I$: Set of available items.
- $K$: Set of available trucks.
- $v_i \in \mathbb{N}_0$ for $i \in I$: Value of item $i$.
- $w_i \in \mathbb{N}_0$ for $i \in I$: Weight of item $i$.
- $C_j \in \mathbb{N}_0$ for $j \in K$: Capacity of truck $j$.

#### Decision Variables:

- $x_{i,j} \in \mathbb{B} \quad \forall i \in I, j \in K$
    - $x_{i,j} = 1$ if truck $j$ packs item $i$, and 0 otherwise.

#### Objective Function:

Maximize the total value of packed items:

$$\max \sum_{i \in I} \sum_{j \in K} v_i \cdot \square$$

#### Constraints:

1. **Truck capacity constraint**: Do not exceed the capacity of any truck.
   - $\sum_{i \in I} w_i \cdot \square \leq \square \quad \forall j \in \square$
2. **Item assignment constraint**: Each item is packed in at most one truck.
   - $\sum_{j \in K} \square \leq \square \quad \forall i \in I$
     
</details>

---

### 2. **Solver Implementation in CP-SAT**

Once you have formulated the model, you will implement a solver using CP-SAT.
This problem is NP-hard, so solving larger instances may take some time, but
CP-SAT should handle it efficiently.

**Steps:**

1. Review the data structure in `data_schema.py` for both instance and solution
   formats. Ignore the `toxic` field for now.
2. Extend the class in `solution.py` to implement your solver based on the
   multi-knapsack problem you have modeled.
3. Perform a quick test on a small instance by running
   `python3 verify.py instance_1`.
4. Verify your final implementation across all test instances by running
   `python3 verify.py`.

---

### Client Feedback: Toxic Item Constraint

After demonstrating your initial solution to the client, they raise a concern.
Some cargo items are classified as toxic, and these should not be packed
together with non-toxic items. The client requests that you add this constraint
to your model.

To meet this new requirement:

1. Adapt your solver to handle the constraint that toxic and non-toxic items
   cannot be packed together. The `activate_toxic` flag is provided in the code.
   When this flag is set to `True`, add the necessary constraints to separate
   toxic from non-toxic items. If the flag is set to `False`, the solver should
   behave as before.
2. Test your updated solver by running `python3 verify_toxic.py`.

**Hint**: Use auxiliary variables to track whether a truck is used for toxic
items.

<details>
   <summary>Click here for a fill-in-the-blank exercise to help you model the problem.</summary>
   
#### Parameters:

- $I$: Set of available items.
- $I_T\subseteq I$: Set of toxic items.
- $I_N = I\setminus I_T$: Set of non-toxic items.
- $K$: Set of available trucks.
- $v_i \in \mathbb{N}_0$ for $i \in I$: Value of item $i$.
- $w_i \in \mathbb{N}_0$ for $i \in I$: Weight of item $i$.
- $C_j \in \mathbb{N}_0$ for $j \in K$: Capacity of truck $j$.

#### Decision Variables:

- $x_{i,j} \in \mathbb{B} \quad \forall i \in I, j \in K$
    - $x_{i,j} = 1$ if truck $j$ packs item $i$, and 0 otherwise.
- $y_{j} \in \mathbb{B} \quad \forall j\in K$
   - $y_{j}=1$ if truck $j$ packs toxic items, and 0 otherwise.

#### Objective Function:

Maximize the total value of packed items:

$$\max \sum_{i \in I} \sum_{j \in K} v_i \cdot \square$$

#### Constraints:

1. **Truck capacity constraint**: Do not exceed the capacity of any truck.
   - $\sum_{i \in I} w_i \cdot \square \leq \square \quad \forall j \in \square$
2. **Item assignment constraint**: Each item is packed in at most one truck.
   - $\sum_{j \in K} \square \leq \square \quad \forall i \in I$
3. **Toxic items constraint**: Do not mix toxic and non-toxic items in the same truck
   - $\square \Rightarrow \square \quad \forall i \in \square, j \in \square$
   - $\square \Rightarrow \neg \square \quad \forall i \in \square, j\in \square$

Note that this is only one possible way of modelling the problem.
</details>

---

## References

- [The Knapsack Problem on Wikipedia](https://en.wikipedia.org/wiki/Knapsack_problem)
- [pydantic](https://docs.pydantic.dev/latest/): Make yourself familiar with the
  abilities of `pydantic` to ensure valid data. While there are many similar
  libraries, including Python's own `dataclasses`, `pydantic` is a very popular
  choice for data validation and serialization in industry.
- [CP-SAT Primer](https://github.com/d-krupke/cpsat-primer): A primer by us for
  CP-SAT.
- [pre-commit](https://pre-commit.com/): We have set up a pre-commit
  configuration for you that you can use to quickly pretty up and check your
  code. You can install it by running `pip install pre-commit` and then
  `pre-commit run --all-files` to run it on all files in your repository.
