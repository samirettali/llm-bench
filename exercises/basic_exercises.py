"""
Basic programming exercises for LLM benchmarking.
These test fundamental programming concepts and simple problem-solving.
"""

from typing import List
from benchmarker.exercise import Exercise, create_solve_test


def get_basic_exercises() -> List[Exercise]:
    """Get a list of basic programming exercises."""
    exercises = []

    # Exercise 1: Simple Addition
    exercises.append(
        Exercise(
            name="Simple Addition",
            description="Implement a function that takes two numbers and returns their sum.",
            test_function=create_solve_test(
                [
                    {"input": (2, 3), "output": 5},
                    {"input": (0, 0), "output": 0},
                    {"input": (-1, 1), "output": 0},
                    {"input": (10, -5), "output": 5},
                ]
            ),
            difficulty="basic",
        )
    )

    # Exercise 2: String Length
    exercises.append(
        Exercise(
            name="String Length",
            description="Implement a function that takes a string and returns its length.",
            test_function=create_solve_test(
                [
                    {"input": "hello", "output": 5},
                    {"input": "", "output": 0},
                    {"input": "a", "output": 1},
                    {"input": "hello world", "output": 11},
                ]
            ),
            difficulty="basic",
        )
    )

    # Exercise 3: List Sum
    exercises.append(
        Exercise(
            name="List Sum",
            description="Implement a function that takes a list of numbers and returns their sum.",
            test_function=create_solve_test(
                [
                    {"input": [1, 2, 3], "output": 6},
                    {"input": [], "output": 0},
                    {"input": [5], "output": 5},
                    {"input": [-1, 1, 0], "output": 0},
                ]
            ),
            difficulty="basic",
        )
    )

    # Exercise 4: Maximum Number
    exercises.append(
        Exercise(
            name="Find Maximum",
            description="Implement a function that takes a list of numbers and returns the maximum value.",
            test_function=create_solve_test(
                [
                    {"input": [1, 2, 3], "output": 3},
                    {"input": [5], "output": 5},
                    {"input": [-1, -2, -3], "output": -1},
                    {"input": [0, 0, 0], "output": 0},
                ]
            ),
            difficulty="basic",
        )
    )

    # Exercise 5: Even Numbers
    exercises.append(
        Exercise(
            name="Count Even Numbers",
            description="Implement a function that takes a list of integers and returns the count of even numbers.",
            test_function=create_solve_test(
                [
                    {"input": [1, 2, 3, 4], "output": 2},
                    {"input": [1, 3, 5], "output": 0},
                    {"input": [2, 4, 6], "output": 3},
                    {"input": [], "output": 0},
                ]
            ),
            difficulty="basic",
        )
    )

    # Exercise 6: String Reversal
    exercises.append(
        Exercise(
            name="Reverse String",
            description="Implement a function that takes a string and returns it reversed.",
            test_function=create_solve_test(
                [
                    {"input": "hello", "output": "olleh"},
                    {"input": "a", "output": "a"},
                    {"input": "", "output": ""},
                    {"input": "12345", "output": "54321"},
                ]
            ),
            difficulty="basic",
        )
    )

    # Exercise 7: Palindrome Check
    exercises.append(
        Exercise(
            name="Palindrome Check",
            description="Implement a function that takes a string and returns True if it's a palindrome, False otherwise.",
            test_function=create_solve_test(
                [
                    {"input": "racecar", "output": True},
                    {"input": "hello", "output": False},
                    {"input": "a", "output": True},
                    {"input": "", "output": True},
                ]
            ),
            difficulty="basic",
        )
    )

    # Exercise 8: Factorial
    exercises.append(
        Exercise(
            name="Factorial",
            description="Implement a function that takes a non-negative integer and returns its factorial.",
            test_function=create_solve_test(
                [
                    {"input": 5, "output": 120},
                    {"input": 0, "output": 1},
                    {"input": 1, "output": 1},
                    {"input": 3, "output": 6},
                ]
            ),
            difficulty="basic",
        )
    )

    return exercises
