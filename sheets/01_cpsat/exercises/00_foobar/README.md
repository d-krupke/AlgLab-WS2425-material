# Exercise: Foobar

This is a simple exercise just meant to get you familiar with the type of
exercises you will face.

- **Given:** A list of integers.
- **Return:** The largest distance between two numbers in the list.

For example, given the list `[1, 3, 5, 7, 9]`, the largest distance is `8` (from
`1` to `9`).

You can install all necessary dependencies by running
`pip install -r requirements.txt`.

## Tasks

### Implement a solver in pure Python

You may have noticed that the problem is not very difficult. In fact, there is a
very simple solution to it. So, your first task is to quickly implement it in
Python, just to get familiar with our workflow.

1. Implement function `solve` in `solution_python.py`. The input and output data
   schemas are defined in `data_schema.py` using pydantic.
2. To verify your implementation, run `python3 verify_pure_python.py` in the
   terminal. If your implementation is correct, you will see a success message.
   Otherwise, you will see an error message.

The output will look similar to this:

```plaintext
# python3 verify_pure_python.py
--------------------------------------------------------------------------------
You can run a single test by passing the name of the test as an argument.
Use this to debug a single test. It will also show the output of the test.
Available tests:
  simple_test
  shuffled_test
  single_number_test
  negative_numbers_test
  random_numbers
--------------------------------------------------------------------------------
Running all checks...
Progress:   0%|                                                                         | 0/5 [00:00<?, ?it/s]Running test 'simple_test'...
Test 'simple_test' passed in 0.2s.
Progress:  20%|█████████████                                                    | 1/5 [00:00<00:00,  6.20it/s]Running test 'shuffled_test'...
Check failed: The distance is not optimal.


Test 'shuffled_test' failed.
========================================
Please fix the error and press enter to try again. Press Ctrl+C to abort.
```

### Implement a solver using CP-SAT

CP-SAT is not really needed for this problem, but it is a good opportunity to
get familiar with the library. Thus, your next task is to let CP-SAT solve the
problem. You can use any function from the `ortools` library, such as:

- `model = cp_model.CpModel()` to create a model
- `model.new_bool_var(...)` to create a boolean variable
- `model.new_int_var(...)` to create an integer variable
- `model.add(... <= ...)`/`model.add(... >= ...)` to add a linear constraint
- `model.maximize(...)` to maximize an objective
- `solver = cp_model.CpSolver()` to create a solver
- `status = solver.solve(model)` to solve the model
- `status == cp_model.OPTIMAL` to check if the model was solved optimally
- `solver.value(...)` to get the value of a variable
- Find more [here](https://d-krupke.github.io/cpsat-primer/04_modelling.html)

> [!IMPORTANT]
>
> Reading through the
> [chapter on modelling](https://d-krupke.github.io/cpsat-primer/04_modelling.html)
> will make this exercise much easier. Getting familiar with the interface of
> CP-SAT is part of the exercise.

1. Implement function `solve` in `solution_cpsat.py`. It has the same interface
   as the pure Python implementation. Be sure that you do not tell CP-SAT the
   solution, but rather let it find the solution itself.
2. To verify your implementation, run `python3 verify_cpsat.py` in the terminal.
   If your implementation is correct, you will see a success message. Otherwise,
   you will see an error message.

## References

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
