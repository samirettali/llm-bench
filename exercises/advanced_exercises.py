"""
Advanced programming exercises for LLM benchmarking.
These test complex algorithms, data structures, and optimization techniques.
"""

from typing import List
from benchmarker.exercise import Exercise, create_solve_test


def get_advanced_exercises() -> List[Exercise]:
    """Get a list of advanced programming exercises."""
    exercises = []

    # Exercise 1: Quick Sort
    exercises.append(
        Exercise(
            name="Quick Sort",
            description="Implement a function that takes a list of numbers and returns them sorted using the quicksort algorithm.",
            test_function=create_solve_test(
                [
                    {"input": [3, 6, 8, 10, 1, 2, 1], "output": [1, 1, 2, 3, 6, 8, 10]},
                    {"input": [5, 2, 8, 1, 9], "output": [1, 2, 5, 8, 9]},
                    {"input": [1], "output": [1]},
                    {"input": [], "output": []},
                ]
            ),
            difficulty="advanced",
        )
    )

    # Exercise 2: Merge Sort
    exercises.append(
        Exercise(
            name="Merge Sort",
            description="Implement a function that takes a list of numbers and returns them sorted using the merge sort algorithm.",
            test_function=create_solve_test(
                [
                    {
                        "input": [38, 27, 43, 3, 9, 82, 10],
                        "output": [3, 9, 10, 27, 38, 43, 82],
                    },
                    {"input": [5, 2, 8, 1, 9], "output": [1, 2, 5, 8, 9]},
                    {"input": [1], "output": [1]},
                    {"input": [], "output": []},
                ]
            ),
            difficulty="advanced",
        )
    )

    # Exercise 3: Binary Tree Traversal
    exercises.append(
        Exercise(
            name="Binary Tree Inorder Traversal",
            description="Implement a function that takes a binary tree (represented as [value, left, right] or None for empty) and returns the inorder traversal as a list.",
            test_function=create_solve_test(
                [
                    {"input": [1, None, [2, [3], None]], "output": [1, 3, 2]},
                    {"input": None, "output": []},
                    {"input": [1], "output": [1]},
                    {"input": [1, [2], [3]], "output": [2, 1, 3]},
                ]
            ),
            difficulty="advanced",
        )
    )

    # Exercise 4: Longest Increasing Subsequence
    exercises.append(
        Exercise(
            name="Longest Increasing Subsequence",
            description="Implement a function that takes a list of integers and returns the length of the longest increasing subsequence.",
            test_function=create_solve_test(
                [
                    {"input": [10, 9, 2, 5, 3, 7, 101, 18], "output": 4},
                    {"input": [0, 1, 0, 3, 2, 3], "output": 4},
                    {"input": [7, 7, 7, 7, 7, 7, 7], "output": 1},
                    {"input": [], "output": 0},
                ]
            ),
            difficulty="advanced",
        )
    )

    # Exercise 5: Graph BFS
    exercises.append(
        Exercise(
            name="Graph Breadth-First Search",
            description="Implement a function that takes a graph (as adjacency list dict) and a start node, returns nodes visited in BFS order.",
            test_function=create_solve_test(
                [
                    {
                        "input": (
                            {
                                "A": ["B", "C"],
                                "B": ["D", "E"],
                                "C": ["F"],
                                "D": [],
                                "E": ["F"],
                                "F": [],
                            },
                            "A",
                        ),
                        "output": ["A", "B", "C", "D", "E", "F"],
                    },
                    {
                        "input": ({"1": ["2", "3"], "2": ["4"], "3": [], "4": []}, "1"),
                        "output": ["1", "2", "3", "4"],
                    },
                    {
                        "input": ({"A": []}, "A"),
                        "output": ["A"],
                    },
                ]
            ),
            difficulty="advanced",
        )
    )

    # Exercise 6: Dynamic Programming - Coin Change
    exercises.append(
        Exercise(
            name="Coin Change",
            description="Implement a function that takes a list of coin denominations and an amount, returns minimum number of coins needed (or -1 if impossible).",
            test_function=create_solve_test(
                [
                    {"input": ([1, 3, 4], 6), "output": 2},
                    {"input": ([2], 3), "output": -1},
                    {"input": ([1], 0), "output": 0},
                    {"input": ([1, 2, 5], 11), "output": 3},
                ]
            ),
            difficulty="advanced",
        )
    )

    # Exercise 7: LRU Cache Implementation
    exercises.append(
        Exercise(
            name="LRU Cache",
            description="Implement a function that simulates LRU cache operations. Take capacity and list of operations [('get', key), ('put', key, value)], return list of results.",
            test_function=create_solve_test(
                [
                    {
                        "input": (
                            2,
                            [
                                ("put", 1, 1),
                                ("put", 2, 2),
                                ("get", 1),
                                ("put", 3, 3),
                                ("get", 2),
                                ("put", 4, 4),
                                ("get", 1),
                                ("get", 3),
                                ("get", 4),
                            ],
                        ),
                        "output": [None, None, 1, None, -1, None, -1, 3, 4],
                    }
                ]
            ),
            difficulty="advanced",
        )
    )

    # Exercise 8: Regular Expression Matching
    exercises.append(
        Exercise(
            name="Regular Expression Matching",
            description="Implement a function that takes a string and a pattern (with '.' and '*'), returns True if the string matches the pattern.",
            test_function=create_solve_test(
                [
                    {"input": ("aa", "a"), "output": False},
                    {"input": ("aa", "a*"), "output": True},
                    {"input": ("ab", ".*"), "output": True},
                    {"input": ("aab", "c*a*b"), "output": True},
                ]
            ),
            difficulty="advanced",
        )
    )

    return exercises
