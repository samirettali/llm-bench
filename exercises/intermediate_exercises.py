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
                "factorial", [(0, 1), (1, 1), (5, 120), (4, 24), (3, 6)]
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
                "fibonacci", [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8)]
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
                    (2, True),
                    (3, True),
                    (4, False),
                    (17, True),
                    (1, False),
                    (0, False),
                    (25, False),
                    (29, True),
                ],
            ),
            difficulty="medium",
        )
    )

    # Exercise 4: String palindrome
    exercises.append(
        Exercise(
            name="Palindrome Check",
            description="Write a function called 'is_palindrome' that checks if a string reads the same forwards and backwards (ignore case).",
            test_function=create_function_test(
                "is_palindrome",
                [
                    ("racecar", True),
                    ("hello", False),
                    ("A man a plan a canal Panama", True),
                    ("race a car", False),
                    ("", True),
                    ("a", True),
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
                    ([64, 34, 25, 12, 22, 11, 90], [11, 12, 22, 25, 34, 64, 90]),
                    ([5, 1, 4, 2, 8], [1, 2, 4, 5, 8]),
                    ([1], [1]),
                    ([], []),
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
                    ("hello world", {"hello": 1, "world": 1}),
                    (
                        "the quick brown fox jumps over the lazy dog",
                        {
                            "the": 2,
                            "quick": 1,
                            "brown": 1,
                            "fox": 1,
                            "jumps": 1,
                            "over": 1,
                            "lazy": 1,
                            "dog": 1,
                        },
                    ),
                    ("", {}),
                    ("hello hello hello", {"hello": 3}),
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
                    ([1, 2, 3, 4, 5], 3, 2),
                    ([1, 2, 3, 4, 5], 6, -1),
                    ([1, 2, 3, 4, 5], 1, 0),
                    ([1, 2, 3, 4, 5], 5, 4),
                    ([], 1, -1),
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
                    ("listen", "silent", True),
                    ("hello", "world", False),
                    ("The Eyes", "They See", True),
                    ("", "", True),
                    ("a", "b", False),
                ],
            ),
            difficulty="medium",
        )
    )

    return exercises
