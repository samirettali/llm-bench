"""
Advanced programming exercises for LLM benchmarking.
"""

from typing import List
from benchmarker.exercise import (
    Exercise,
    create_function_test,
    create_code_execution_test,
)


def get_advanced_exercises() -> List[Exercise]:
    """Get a list of advanced programming exercises."""
    exercises = []

    # Exercise 1: Merge sort
    exercises.append(
        Exercise(
            name="Merge Sort",
            description="Write a function called 'merge_sort' that implements the merge sort algorithm to sort a list of numbers.",
            test_function=create_function_test(
                "merge_sort",
                [
                    ([64, 34, 25, 12, 22, 11, 90], [11, 12, 22, 25, 34, 64, 90]),
                    ([38, 27, 43, 3, 9, 82, 10], [3, 9, 10, 27, 38, 43, 82]),
                    ([1], [1]),
                    ([], []),
                    ([5, 2, 8, 1, 9], [1, 2, 5, 8, 9]),
                ],
            ),
            difficulty="hard",
        )
    )

    # Exercise 2: Longest common subsequence
    exercises.append(
        Exercise(
            name="Longest Common Subsequence",
            description="Write a function called 'lcs_length' that finds the length of the longest common subsequence between two strings.",
            test_function=create_function_test(
                "lcs_length",
                [
                    ("ABCDGH", "AEDFHR", 3),
                    ("AGGTAB", "GXTXAYB", 4),
                    ("", "ABC", 0),
                    ("ABC", "", 0),
                    ("ABC", "ABC", 3),
                ],
            ),
            difficulty="hard",
        )
    )

    # Exercise 3: Valid parentheses
    exercises.append(
        Exercise(
            name="Valid Parentheses",
            description="Write a function called 'is_valid_parentheses' that checks if a string of parentheses (), brackets [], and braces {} is valid.",
            test_function=create_function_test(
                "is_valid_parentheses",
                [
                    ("()", True),
                    ("()[]{}", True),
                    ("(]", False),
                    ("([)]", False),
                    ("{[]}", True),
                    ("", True),
                    ("((()))", True),
                    ("((())", False),
                ],
            ),
            difficulty="hard",
        )
    )

    # Exercise 4: Graph traversal
    exercises.append(
        Exercise(
            name="Depth-First Search",
            description="Write a function called 'dfs' that performs depth-first search on a graph represented as an adjacency list. Return a list of visited nodes starting from a given node.",
            test_function=create_function_test(
                "dfs",
                [
                    (
                        {"A": ["B", "C"], "B": ["D"], "C": ["E"], "D": [], "E": []},
                        "A",
                        ["A", "B", "D", "C", "E"],
                    ),
                    (
                        {"1": ["2", "3"], "2": ["4"], "3": [], "4": []},
                        "1",
                        ["1", "2", "4", "3"],
                    ),
                    ({"A": []}, "A", ["A"]),
                ],
            ),
            difficulty="hard",
        )
    )

    # Exercise 5: Dynamic programming - coin change
    exercises.append(
        Exercise(
            name="Coin Change",
            description="Write a function called 'coin_change' that finds the minimum number of coins needed to make a given amount. Return -1 if impossible.",
            test_function=create_function_test(
                "coin_change",
                [
                    ([1, 3, 4], 6, 2),  # 3 + 3
                    ([2], 3, -1),
                    ([1], 0, 0),
                    ([1, 2, 5], 11, 3),  # 5 + 5 + 1
                ],
            ),
            difficulty="hard",
        )
    )

    # Exercise 6: Binary tree operations
    exercises.append(
        Exercise(
            name="Binary Tree Max Depth",
            description="Write a function called 'max_depth' that finds the maximum depth of a binary tree. The tree is represented as nested lists where [val, left, right] or [val] for leaf nodes.",
            test_function=create_function_test(
                "max_depth",
                [
                    ([3, [9], [20, [15], [7]]], 3),
                    ([1, None, [2]], 2),
                    ([1], 1),
                    (None, 0),
                ],
            ),
            difficulty="hard",
        )
    )

    # Exercise 7: String matching
    exercises.append(
        Exercise(
            name="String Pattern Matching",
            description="Write a function called 'pattern_match' that checks if a string matches a pattern with '.' (any character) and '*' (zero or more of preceding character).",
            test_function=create_function_test(
                "pattern_match",
                [
                    ("aa", "a", False),
                    ("aa", "a*", True),
                    ("ab", ".*", True),
                    ("aab", "c*a*b", True),
                    ("mississippi", "mis*is*p*.", False),
                ],
            ),
            difficulty="hard",
        )
    )

    # Exercise 8: Data structure implementation
    exercises.append(
        Exercise(
            name="LRU Cache",
            description="Implement an LRU (Least Recently Used) cache class called 'LRUCache' with get(key) and put(key, value) methods. Initialize with capacity.",
            test_function=create_function_test(
                "test_lru_cache",
                [
                    (None, True)  # This will be a custom test
                ],
            ),
            difficulty="hard",
        )
    )

    return exercises
