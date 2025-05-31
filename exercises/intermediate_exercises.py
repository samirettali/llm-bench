"""
Intermediate programming exercises for LLM benchmarking.
"""

from typing import List
from benchmarker.exercise import (
    Exercise,
    create_function_test,
    create_code_execution_test,
)


def get_intermediate_exercises() -> List[Exercise]:
    """Get a list of intermediate programming exercises."""
    exercises = []

    # Exercise 1: Factorial
    exercises.append(
        Exercise(
            name="Factorial Function",
            description="Write a function called 'factorial' that calculates the factorial of a number (n!).",
            test_function=create_function_test(
                "factorial",
                [
                    {"input": 0, "output": 1},
                    {"input": 1, "output": 1},
                    {"input": 5, "output": 120},
                    {"input": 4, "output": 24},
                    {"input": 3, "output": 6},
                ],
            ),
            difficulty="medium",
        )
    )

    # Exercise 2: Fibonacci
    exercises.append(
        Exercise(
            name="Fibonacci Sequence",
            description="Write a function called 'fibonacci' that returns the nth number in the Fibonacci sequence (starting with 0, 1).",
            test_function=create_function_test(
                "fibonacci",
                [
                    {"input": 0, "output": 0},
                    {"input": 1, "output": 1},
                    {"input": 2, "output": 1},
                    {"input": 3, "output": 2},
                    {"input": 4, "output": 3},
                    {"input": 5, "output": 5},
                    {"input": 6, "output": 8},
                ],
            ),
            difficulty="medium",
        )
    )

    # Exercise 3: Prime numbers
    exercises.append(
        Exercise(
            name="Prime Number Check",
            description="Write a function called 'is_prime' that checks if a given number is prime.",
            test_function=create_function_test(
                "is_prime",
                [
                    {"input": 2, "output": True},
                    {"input": 3, "output": True},
                    {"input": 4, "output": False},
                    {"input": 17, "output": True},
                    {"input": 1, "output": False},
                    {"input": 0, "output": False},
                    {"input": 25, "output": False},
                    {"input": 29, "output": True},
                ],
            ),
            difficulty="medium",
        )
    )

    # Exercise 4: String palindrome
    exercises.append(
        Exercise(
            name="Palindrome Check",
            description="Write a function called 'is_palindrome' that checks if a string reads the same forwards and backwards (ignore case and spaces).",
            test_function=create_function_test(
                "is_palindrome",
                [
                    {"input": "racecar", "output": True},
                    {"input": "hello", "output": False},
                    {"input": "A man a plan a canal Panama", "output": True},
                    {"input": "race a car", "output": False},
                    {"input": "", "output": True},
                    {"input": "a", "output": True},
                ],
            ),
            difficulty="medium",
        )
    )

    # Exercise 5: List sorting
    exercises.append(
        Exercise(
            name="Bubble Sort",
            description="Write a function called 'bubble_sort' that sorts a list of numbers using the bubble sort algorithm.",
            test_function=create_function_test(
                "bubble_sort",
                [
                    {"input": [64, 34, 25, 12, 22, 11, 90], "output": [11, 12, 22, 25, 34, 64, 90]},
                    {"input": [5, 1, 4, 2, 8], "output": [1, 2, 4, 5, 8]},
                    {"input": [1], "output": [1]},
                    {"input": [], "output": []},
                ],
            ),
            difficulty="medium",
        )
    )

    # Exercise 6: Dictionary operations
    exercises.append(
        Exercise(
            name="Word Count",
            description="Write a function called 'word_count' that takes a string and returns a dictionary with word counts.",
            test_function=create_function_test(
                "word_count",
                [
                    {"input": "hello world", "output": {"hello": 1, "world": 1}},
                    {
                        "input": "the quick brown fox jumps over the lazy dog",
                        "output": {
                            "the": 2,
                            "quick": 1,
                            "brown": 1,
                            "fox": 1,
                            "jumps": 1,
                            "over": 1,
                            "lazy": 1,
                            "dog": 1,
                        },
                    },
                    {"input": "", "output": {}},
                    {"input": "hello hello hello", "output": {"hello": 3}},
                ],
            ),
            difficulty="medium",
        )
    )

    # Exercise 7: Binary search
    exercises.append(
        Exercise(
            name="Binary Search",
            description="Write a function called 'binary_search' that finds the index of a target value in a sorted list using binary search. Return -1 if not found.",
            test_function=create_function_test(
                "binary_search",
                [
                    {"input": ([1, 2, 3, 4, 5], 3), "output": 2},
                    {"input": ([1, 2, 3, 4, 5], 6), "output": -1},
                    {"input": ([1, 2, 3, 4, 5], 1), "output": 0},
                    {"input": ([1, 2, 3, 4, 5], 5), "output": 4},
                    {"input": ([], 1), "output": -1},
                ],
            ),
            difficulty="medium",
        )
    )

    # Exercise 8: String anagram
    exercises.append(
        Exercise(
            name="Anagram Check",
            description="Write a function called 'are_anagrams' that checks if two strings are anagrams (ignore case and spaces).",
            test_function=create_function_test(
                "are_anagrams",
                [
                    {"input": ("listen", "silent"), "output": True},
                    {"input": ("hello", "world"), "output": False},
                    {"input": ("The Eyes", "They See"), "output": True},
                    {"input": ("", ""), "output": True},
                    {"input": ("a", "b"), "output": False},
                ],
            ),
            difficulty="medium",
        )
    )

    return exercises
