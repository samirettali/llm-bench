"""
Super hard programming exercises for LLM benchmarking.
These exercises test the absolute limits of algorithmic reasoning and implementation.
"""

from typing import List
from benchmarker.exercise import (
    Exercise,
    create_solve_test,
    create_code_execution_test,
    ExerciseResult,
    ExerciseStatus,
)


def create_trie_test() -> callable:
    """Create a custom test for the Trie data structure (special case that needs a class)."""

    def test_function(code: str) -> ExerciseResult:
        try:
            # Execute the code to define the Trie class
            namespace = {}
            exec(code, namespace)

            if "Trie" not in namespace:
                return ExerciseResult(
                    status=ExerciseStatus.ERROR,
                    error_message="Trie class not found in code",
                )

            # Test case 1
            trie = namespace["Trie"]()
            operations1 = [
                ("insert", "apple"),
                ("insert", "app"),
                ("insert", "application"),
                ("search", "app"),
                ("search", "apple"),
                ("search", "appl"),
                ("prefix_count", "app"),
            ]
            expected1 = [None, None, None, True, True, False, 3]

            results1 = []
            for op, arg in operations1:
                if op == "insert":
                    results1.append(trie.insert(arg))
                elif op == "search":
                    results1.append(trie.search(arg))
                elif op == "prefix_count":
                    results1.append(trie.prefix_count(arg))

            if results1 != expected1:
                return ExerciseResult(
                    status=ExerciseStatus.FAILED,
                    expected_output=expected1,
                    actual_output=results1,
                    error_message="Test case 1 failed",
                )

            # Test case 2
            trie2 = namespace["Trie"]()
            operations2 = [
                ("insert", "cat"),
                ("insert", "car"),
                ("prefix_count", "ca"),
                ("prefix_count", "dog"),
                ("search", "cat"),
            ]
            expected2 = [None, None, 2, 0, True]

            results2 = []
            for op, arg in operations2:
                if op == "insert":
                    results2.append(trie2.insert(arg))
                elif op == "search":
                    results2.append(trie2.search(arg))
                elif op == "prefix_count":
                    results2.append(trie2.prefix_count(arg))

            if results2 != expected2:
                return ExerciseResult(
                    status=ExerciseStatus.FAILED,
                    expected_output=expected2,
                    actual_output=results2,
                    error_message="Test case 2 failed",
                )

            return ExerciseResult(
                status=ExerciseStatus.PASSED,
                expected_output="All test cases passed",
                actual_output="All test cases passed",
            )

        except Exception as e:
            return ExerciseResult(status=ExerciseStatus.ERROR, error_message=str(e))

    return test_function


def get_super_hard_exercises() -> List[Exercise]:
    """Get a list of super hard programming exercises."""
    exercises = []

    # Exercise 1: Advanced Graph Algorithm - Minimum Spanning Tree
    exercises.append(
        Exercise(
            name="Kruskal's Minimum Spanning Tree",
            description="Implement a function that takes a list of edges [(weight, node1, node2)] and returns the total weight of the minimum spanning tree using Kruskal's algorithm.",
            test_function=create_solve_test(
                [
                    {
                        "input": [
                            (4, "A", "B"),
                            (2, "A", "C"),
                            (3, "B", "C"),
                            (1, "C", "D"),
                            (5, "B", "D"),
                        ],
                        "output": 6,
                    },
                    {
                        "input": [(1, "A", "B"), (2, "B", "C"), (3, "A", "C")],
                        "output": 3,
                    },
                    {"input": [(10, "X", "Y")], "output": 10},
                ],
            ),
            difficulty="super_hard",
        )
    )

    # Exercise 2: Advanced Dynamic Programming - Edit Distance with Operations
    exercises.append(
        Exercise(
            name="Edit Distance with Custom Operations",
            description="Implement a function that takes two strings and calculates minimum edit distance with custom operation costs: insert=1, delete=1, substitute=2.",
            test_function=create_solve_test(
                [
                    {"input": ("kitten", "sitting"), "output": 5},
                    {"input": ("sunday", "saturday"), "output": 4},
                    {"input": ("", "abc"), "output": 3},
                    {"input": ("abc", ""), "output": 3},
                    {"input": ("same", "same"), "output": 0},
                ],
            ),
            difficulty="super_hard",
        )
    )

    # Exercise 3: Advanced Tree Algorithm - Lowest Common Ancestor
    exercises.append(
        Exercise(
            name="Lowest Common Ancestor in Binary Tree",
            description="Implement a function that takes a binary tree (format: [value, left, right] or [value] for leaves) and two node values, returns the LCA value.",
            test_function=create_solve_test(
                [
                    {
                        "input": ([3, [5, [6], [2, [7], [4]]], [1, [0], [8]]], 5, 1),
                        "output": 3,
                    },
                    {
                        "input": ([3, [5, [6], [2, [7], [4]]], [1, [0], [8]]], 5, 4),
                        "output": 5,
                    },
                    {"input": ([1, [2], [3]], 2, 3), "output": 1},
                ],
            ),
            difficulty="super_hard",
        )
    )

    # Exercise 4: Advanced Number Theory - Modular Exponentiation
    exercises.append(
        Exercise(
            name="Modular Exponentiation",
            description="Implement a function that takes base, exponent, and modulus, and computes (base^exp) % mod efficiently using fast exponentiation.",
            test_function=create_solve_test(
                [
                    {"input": (2, 10, 1000), "output": 24},
                    {"input": (3, 4, 5), "output": 1},
                    {"input": (2, 100, 1000000007), "output": 976371285},
                    {"input": (5, 0, 13), "output": 1},
                    {"input": (123456789, 987654321, 1000000007), "output": 357775508},
                ],
            ),
            difficulty="super_hard",
        )
    )

    # Exercise 5: Advanced String Algorithm - KMP Pattern Matching
    exercises.append(
        Exercise(
            name="KMP Pattern Matching",
            description="Implement a function that takes a text string and a pattern, and returns all starting indices where the pattern occurs using the Knuth-Morris-Pratt algorithm.",
            test_function=create_solve_test(
                [
                    {
                        "input": ("ABABDABACDABABCABCABCABCABC", "ABABCABCABCABC"),
                        "output": [15],
                    },
                    {"input": ("AABAACAABAA", "AABA"), "output": [0, 9]},
                    {"input": ("ABABABAB", "ABAB"), "output": [0, 2, 4]},
                    {"input": ("HELLO", "WORLD"), "output": []},
                    {"input": ("AAAAA", "AA"), "output": [0, 1, 2, 3]},
                ],
            ),
            difficulty="super_hard",
        )
    )

    # Exercise 6: Advanced Graph Algorithm - Topological Sort with Cycle Detection
    exercises.append(
        Exercise(
            name="Topological Sort with Cycle Detection",
            description="Implement a function that takes a directed graph as adjacency list {node: [dependencies]} and returns topologically sorted list, or empty list if cycle detected.",
            test_function=create_solve_test(
                [
                    {
                        "input": {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []},
                        "output": ["D", "B", "C", "A"],
                    },
                    {"input": {"A": ["B"], "B": ["C"], "C": ["A"]}, "output": []},
                    {
                        "input": {"X": [], "Y": ["X"], "Z": ["Y"]},
                        "output": ["X", "Y", "Z"],
                    },
                ],
            ),
            difficulty="super_hard",
        )
    )

    # Exercise 7: Advanced Data Structure - Trie with Prefix Operations (special case)
    exercises.append(
        Exercise(
            name="Trie with Prefix Count",
            description="Implement a Trie class with methods: insert(word), search(word), prefix_count(prefix). insert() returns None, search() returns bool, prefix_count() returns int.",
            test_function=create_trie_test(),
            difficulty="super_hard",
        )
    )

    # Exercise 8: Advanced Computational Geometry - Convex Hull
    exercises.append(
        Exercise(
            name="Convex Hull using Graham Scan",
            description="Implement a function that takes a list of 2D points and returns the convex hull points in counter-clockwise order using Graham scan algorithm.",
            test_function=create_solve_test(
                [
                    {
                        "input": [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0.5)],
                        "output": [(1, -1), (2, 0), (1, 1), (0, 0)],
                    },
                    {
                        "input": [(0, 0), (1, 0), (0, 1)],
                        "output": [(0, 0), (1, 0), (0, 1)],
                    },
                    {
                        "input": [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)],
                        "output": [(0, 0), (2, 0), (2, 2), (0, 2)],
                    },
                ],
            ),
            difficulty="super_hard",
        )
    )

    # Exercise 9: Advanced Dynamic Programming - Matrix Chain Multiplication
    exercises.append(
        Exercise(
            name="Matrix Chain Multiplication",
            description="Implement a function that takes a list of matrix dimensions [d0,d1,d2,...,dn] and finds minimum scalar multiplications for optimal parenthesization.",
            test_function=create_solve_test(
                [
                    {"input": [1, 2, 3, 4, 5], "output": 38},
                    {"input": [40, 20, 30, 10, 30], "output": 26000},
                    {"input": [1, 2, 3], "output": 6},
                    {"input": [5, 10, 3, 12, 5, 50, 6], "output": 2010},
                ],
            ),
            difficulty="super_hard",
        )
    )

    # Exercise 10: Advanced Algorithm - Suffix Array Construction
    exercises.append(
        Exercise(
            name="Suffix Array Construction",
            description="Implement a function that takes a string and builds its suffix array - list of starting indices of suffixes in lexicographically sorted order.",
            test_function=create_solve_test(
                [
                    {"input": "banana", "output": [5, 3, 1, 0, 4, 2]},
                    {"input": "abcab", "output": [2, 0, 3, 1, 4]},
                    {"input": "aaa", "output": [2, 1, 0]},
                    {
                        "input": "mississippi",
                        "output": [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2],
                    },
                ],
            ),
            difficulty="super_hard",
        )
    )

    return exercises
