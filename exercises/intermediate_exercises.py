"""
Intermediate programming exercises for LLM benchmarking.
These test more complex algorithms and data structure manipulation.
"""

from typing import List
from benchmarker.exercise import Exercise, create_solve_test


def get_intermediate_exercises() -> List[Exercise]:
    """Get a list of intermediate programming exercises."""
    exercises = []

    # Exercise 1: Fibonacci
    exercises.append(
        Exercise(
            name="Fibonacci Sequence",
            description="Implement a function that takes an integer n and returns the nth Fibonacci number (0-indexed).",
            test_function=create_solve_test(
                [
                    {"input": 0, "output": 0},
                    {"input": 1, "output": 1},
                    {"input": 5, "output": 5},
                    {"input": 10, "output": 55},
                ]
            ),
            difficulty="intermediate",
        )
    )

    # Exercise 2: Prime Numbers
    exercises.append(
        Exercise(
            name="Prime Check",
            description="Implement a function that takes an integer and returns True if it's a prime number, False otherwise.",
            test_function=create_solve_test(
                [
                    {"input": 2, "output": True},
                    {"input": 3, "output": True},
                    {"input": 4, "output": False},
                    {"input": 17, "output": True},
                    {"input": 1, "output": False},
                ]
            ),
            difficulty="intermediate",
        )
    )

    # Exercise 3: Binary Search
    exercises.append(
        Exercise(
            name="Binary Search",
            description="Implement a function that takes a sorted list and a target value, returns the index of the target or -1 if not found.",
            test_function=create_solve_test(
                [
                    {"input": ([1, 2, 3, 4, 5], 3), "output": 2},
                    {"input": ([1, 2, 3, 4, 5], 6), "output": -1},
                    {"input": ([1], 1), "output": 0},
                    {"input": ([], 1), "output": -1},
                ]
            ),
            difficulty="intermediate",
        )
    )

    # Exercise 4: Anagram Check
    exercises.append(
        Exercise(
            name="Anagram Check",
            description="Implement a function that takes two strings and returns True if they are anagrams, False otherwise.",
            test_function=create_solve_test(
                [
                    {"input": ("listen", "silent"), "output": True},
                    {"input": ("hello", "world"), "output": False},
                    {"input": ("a", "a"), "output": True},
                    {"input": ("", ""), "output": True},
                ]
            ),
            difficulty="intermediate",
        )
    )

    # Exercise 5: Two Sum
    exercises.append(
        Exercise(
            name="Two Sum",
            description="Implement a function that takes a list of integers and a target sum, returns indices of two numbers that add up to target, or [-1, -1] if none found.",
            test_function=create_solve_test(
                [
                    {"input": ([2, 7, 11, 15], 9), "output": [0, 1]},
                    {"input": ([3, 2, 4], 6), "output": [1, 2]},
                    {"input": ([3, 3], 6), "output": [0, 1]},
                    {"input": ([1, 2], 5), "output": [-1, -1]},
                ]
            ),
            difficulty="intermediate",
        )
    )

    # Exercise 6: Merge Sorted Lists
    exercises.append(
        Exercise(
            name="Merge Sorted Lists",
            description="Implement a function that takes two sorted lists and returns a single merged sorted list.",
            test_function=create_solve_test(
                [
                    {"input": ([1, 3, 5], [2, 4, 6]), "output": [1, 2, 3, 4, 5, 6]},
                    {"input": ([], [1, 2, 3]), "output": [1, 2, 3]},
                    {"input": ([1, 2, 3], []), "output": [1, 2, 3]},
                    {"input": ([1], [2]), "output": [1, 2]},
                ]
            ),
            difficulty="intermediate",
        )
    )

    # Exercise 7: Valid Parentheses
    exercises.append(
        Exercise(
            name="Valid Parentheses",
            description="Implement a function that takes a string containing parentheses and returns True if they are balanced, False otherwise.",
            test_function=create_solve_test(
                [
                    {"input": "()", "output": True},
                    {"input": "()[]{}", "output": True},
                    {"input": "(]", "output": False},
                    {"input": "([)]", "output": False},
                    {"input": "{[]}", "output": True},
                ]
            ),
            difficulty="intermediate",
        )
    )

    # Exercise 8: Longest Common Subsequence Length
    exercises.append(
        Exercise(
            name="Longest Common Subsequence",
            description="Implement a function that takes two strings and returns the length of their longest common subsequence.",
            test_function=create_solve_test(
                [
                    {"input": ("abcde", "ace"), "output": 3},
                    {"input": ("abc", "abc"), "output": 3},
                    {"input": ("abc", "def"), "output": 0},
                    {"input": ("", "abc"), "output": 0},
                ]
            ),
            difficulty="intermediate",
        )
    )

    return exercises
