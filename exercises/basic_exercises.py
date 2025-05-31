"""
Basic programming exercises for LLM benchmarking.
"""

from typing import List
from benchmarker.exercise import (
    Exercise,
    create_function_test,
    create_code_execution_test,
)


def get_basic_exercises() -> List[Exercise]:
    """Get a list of basic programming exercises."""
    exercises = []

    # Exercise 1: Simple arithmetic
    exercises.append(
        Exercise(
            name="Simple Addition",
            description="Write a function called 'add_numbers' that takes two numbers and returns their sum.",
            test_function=create_function_test(
                "add_numbers",
                [
                    {"input": (2, 3), "output": 5},
                    {"input": (10, -5), "output": 5},
                    {"input": (0, 0), "output": 0},
                    {"input": (-3, -7), "output": -10},
                ],
            ),
            difficulty="easy",
        )
    )

    # Exercise 2: String manipulation
    exercises.append(
        Exercise(
            name="String Reversal",
            description="Write a function called 'reverse_string' that takes a string and returns it reversed.",
            test_function=create_function_test(
                "reverse_string",
                [
                    {"input": "hello", "output": "olleh"},
                    {"input": "", "output": ""},
                    {"input": "a", "output": "a"},
                    {"input": "Python", "output": "nohtyP"},
                ],
            ),
            difficulty="easy",
        )
    )

    # Exercise 3: List operations
    exercises.append(
        Exercise(
            name="List Maximum",
            description="Write a function called 'find_max' that takes a list of numbers and returns the maximum value.",
            test_function=create_function_test(
                "find_max",
                [
                    {"input": [1, 2, 3, 4, 5], "output": 5},
                    {"input": [-1, -2, -3], "output": -1},
                    {"input": [42], "output": 42},
                    {"input": [3, 1, 4, 1, 5, 9], "output": 9},
                ],
            ),
            difficulty="easy",
        )
    )

    # Exercise 4: Conditional logic
    exercises.append(
        Exercise(
            name="Even or Odd",
            description="Write a function called 'is_even' that takes a number and returns True if it's even, False if it's odd.",
            test_function=create_function_test(
                "is_even",
                [
                    {"input": 2, "output": True},
                    {"input": 3, "output": False},
                    {"input": 0, "output": True},
                    {"input": -4, "output": True},
                    {"input": -3, "output": False},
                ],
            ),
            difficulty="easy",
        )
    )

    # Exercise 5: Loop operations
    exercises.append(
        Exercise(
            name="Sum of List",
            description="Write a function called 'sum_list' that takes a list of numbers and returns their sum.",
            test_function=create_function_test(
                "sum_list",
                [
                    {"input": [1, 2, 3], "output": 6},
                    {"input": [], "output": 0},
                    {"input": [-1, 1], "output": 0},
                    {"input": [10, -5, 3], "output": 8},
                ],
            ),
            difficulty="easy",
        )
    )

    # Exercise 6: String processing
    exercises.append(
        Exercise(
            name="Count Vowels",
            description="Write a function called 'count_vowels' that takes a string and returns the number of vowels (a, e, i, o, u) in it.",
            test_function=create_function_test(
                "count_vowels",
                [
                    {"input": "hello", "output": 2},
                    {"input": "aeiou", "output": 5},
                    {"input": "bcdfg", "output": 0},
                    {"input": "Hello World", "output": 3},
                    {"input": "", "output": 0},
                ],
            ),
            difficulty="easy",
        )
    )

    # Exercise 7: Simple print output
    exercises.append(
        Exercise(
            name="Print Hello World",
            description="Write code that prints exactly 'Hello, World!' to the console.",
            test_function=create_code_execution_test("Hello, World!"),
            difficulty="easy",
        )
    )

    # Exercise 8: Basic math
    exercises.append(
        Exercise(
            name="Calculate Average",
            description="Write a function called 'calculate_average' that takes a list of numbers and returns their average.",
            test_function=create_function_test(
                "calculate_average",
                [
                    {"input": [1, 2, 3], "output": 2.0},
                    {"input": [10, 20], "output": 15.0},
                    {"input": [5], "output": 5.0},
                    {"input": [2, 4, 6, 8], "output": 5.0},
                ],
            ),
            difficulty="easy",
        )
    )

    return exercises
