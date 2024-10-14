from _alglab_utils import CHECK, main, mandatory_testcase
from data_schema import Instance
from solution_cpsat import solve


@mandatory_testcase(max_runtime_s=10)
def simple_test():
    instance = Instance(numbers=[1, 2, 3, 4, 5])
    solution = solve(instance)
    CHECK(solution.number_a in instance.numbers, "The first number is not in the list.")
    CHECK(
        solution.number_b in instance.numbers, "The second number is not in the list."
    )
    CHECK(
        solution.distance == abs(solution.number_a - solution.number_b),
        "The distance is not correct.",
    )
    CHECK(solution.distance == 4, "The distance is not correct.")


@mandatory_testcase(max_runtime_s=10)
def shuffled_test():
    numbers = [1, 2, 3, 4, 5]
    import random

    random.shuffle(numbers)
    instance = Instance(numbers=numbers)
    solution = solve(instance)
    CHECK(solution.number_a in instance.numbers, "The first number is not in the list.")
    CHECK(
        solution.number_b in instance.numbers, "The second number is not in the list."
    )
    CHECK(
        solution.distance == abs(solution.number_a - solution.number_b),
        "The distance is not correct.",
    )
    CHECK(solution.distance == 4, "The distance is not optimal.")


@mandatory_testcase(max_runtime_s=10)
def single_number_test():
    instance = Instance(numbers=[1])
    solution = solve(instance)
    CHECK(solution.number_a in instance.numbers, "The first number is not in the list.")
    CHECK(
        solution.number_b in instance.numbers, "The second number is not in the list."
    )
    CHECK(
        solution.distance == abs(solution.number_a - solution.number_b),
        "The distance is not correct.",
    )
    CHECK(solution.distance == 0, "The distance is not optimal.")


@mandatory_testcase(max_runtime_s=10)
def negative_numbers_test():
    instance = Instance(numbers=[-1, -2, -3, -4, -5])
    solution = solve(instance)
    CHECK(solution.number_a in instance.numbers, "The first number is not in the list.")
    CHECK(
        solution.number_b in instance.numbers, "The second number is not in the list."
    )
    CHECK(
        solution.distance == abs(solution.number_a - solution.number_b),
        "The distance is not correct.",
    )
    CHECK(solution.distance == 4, "The distance is not optimal.")


@mandatory_testcase(max_runtime_s=10)
def random_numbers():
    import random

    random.seed(42)
    numbers = [random.randint(-100, 100) for _ in range(100)]
    instance = Instance(numbers=numbers)
    solution = solve(instance)
    max_distances = max(numbers) - min(numbers)
    CHECK(solution.number_a in instance.numbers, "The first number is not in the list.")
    CHECK(
        solution.number_b in instance.numbers, "The second number is not in the list."
    )
    CHECK(
        solution.distance == abs(solution.number_a - solution.number_b),
        "The distance is not correct.",
    )
    CHECK(solution.distance == max_distances, "The distance is not optimal.")


if __name__ == "__main__":
    main()
