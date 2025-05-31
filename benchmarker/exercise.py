"""
Exercise definition and result handling for the LLM benchmarking framework.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional, Dict, List
from enum import Enum
import traceback
import sys
import io
import contextlib


class ExerciseStatus(Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


@dataclass
class ExerciseResult:
    """Result of executing an exercise."""

    status: ExerciseStatus
    expected_output: Any = None
    actual_output: Any = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    code_generated: Optional[str] = None


class Exercise:
    """Represents a single benchmark exercise."""

    def __init__(
        self,
        name: str,
        description: str,
        test_function: Callable[[str], ExerciseResult],
        max_attempts: int = 3,
        difficulty: str = "medium",
    ):
        self.name = name
        self.description = description
        self.test_function = test_function
        self.max_attempts = max_attempts
        self.difficulty = difficulty
        self.attempts = 0
        self.results: List[ExerciseResult] = []

    def get_prompt(self) -> str:
        """Generate the prompt for this exercise."""
        prompt = f"""Solve this coding problem. Output ONLY the executable Python code, no markdown formatting, no explanations, no comments outside the code.

Problem: {self.description}

Requirements:
- Write clean, working Python code
- Do not include any markdown formatting (no ```python or ```)
- Do not include explanations or comments outside the code
- The code should be ready to execute immediately
- Focus on correctness and simplicity

Code:"""
        return prompt

    def get_retry_prompt(self, previous_result: ExerciseResult) -> str:
        """Generate a retry prompt when the previous attempt failed."""
        error_info = ""
        if previous_result.error_message:
            error_info = f"Error: {previous_result.error_message}"
        elif (
            previous_result.actual_output is not None
            and previous_result.expected_output is not None
        ):
            error_info = f"Expected: {previous_result.expected_output}, but got: {previous_result.actual_output}"

        prompt = f"""Your previous solution failed. Here's what went wrong:
{error_info}

Problem: {self.description}

Please fix the issue and provide ONLY the corrected executable Python code, no markdown formatting, no explanations.

Code:"""
        return prompt

    def execute(self, code: str) -> ExerciseResult:
        """Execute the provided code and return the result."""
        self.attempts += 1
        result = self.test_function(code)
        result.code_generated = code
        self.results.append(result)
        return result

    def is_completed(self) -> bool:
        """Check if this exercise has been completed successfully."""
        return any(result.status == ExerciseStatus.PASSED for result in self.results)

    def can_retry(self) -> bool:
        """Check if this exercise can be retried."""
        return self.attempts < self.max_attempts and not self.is_completed()


def create_code_execution_test(
    expected_output: Any, setup_code: str = ""
) -> Callable[[str], ExerciseResult]:
    """
    Create a test function that executes code and compares output.

    Args:
        expected_output: The expected result from the code execution
        setup_code: Optional setup code to run before the main code

    Returns:
        A test function that can be used with Exercise
    """

    def test_function(code: str) -> ExerciseResult:
        try:
            # Create a clean namespace for execution
            namespace = {}

            # Execute setup code if provided
            if setup_code.strip():
                exec(setup_code, namespace)

            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()

            try:
                # Execute the provided code
                exec(code, namespace)

                # Get captured output
                output = captured_output.getvalue().strip()

                # If no output was printed, try to find a result variable or return value
                if not output:
                    if "result" in namespace:
                        actual_output = namespace["result"]
                    else:
                        # Try to evaluate the last expression
                        try:
                            actual_output = eval(code, namespace)
                        except:
                            actual_output = None
                else:
                    try:
                        # Try to convert output to the expected type
                        actual_output = type(expected_output)(output)
                    except:
                        actual_output = output

            finally:
                sys.stdout = old_stdout

            # Compare results
            if actual_output == expected_output:
                return ExerciseResult(
                    status=ExerciseStatus.PASSED,
                    expected_output=expected_output,
                    actual_output=actual_output,
                )
            else:
                return ExerciseResult(
                    status=ExerciseStatus.FAILED,
                    expected_output=expected_output,
                    actual_output=actual_output,
                )

        except Exception as e:
            return ExerciseResult(
                status=ExerciseStatus.ERROR,
                error_message=str(e),
                expected_output=expected_output,
            )

    return test_function


def create_function_test(
    function_name: str, test_cases: List[tuple]
) -> Callable[[str], ExerciseResult]:
    """
    Create a test function that tests a specific function with multiple test cases.

    Args:
        function_name: Name of the function to test
        test_cases: List of (inputs, expected_output) tuples

    Returns:
        A test function that can be used with Exercise
    """

    def test_function(code: str) -> ExerciseResult:
        try:
            # Execute the code to define the function
            namespace = {}
            exec(code, namespace)

            if function_name not in namespace:
                return ExerciseResult(
                    status=ExerciseStatus.ERROR,
                    error_message=f"Function '{function_name}' not found in code",
                )

            func = namespace[function_name]

            # Test all cases
            for i, (inputs, expected) in enumerate(test_cases):
                if isinstance(inputs, tuple):
                    actual = func(*inputs)
                else:
                    actual = func(inputs)

                if actual != expected:
                    return ExerciseResult(
                        status=ExerciseStatus.FAILED,
                        expected_output=expected,
                        actual_output=actual,
                        error_message=f"Test case {i + 1} failed",
                    )

            return ExerciseResult(
                status=ExerciseStatus.PASSED,
                expected_output="All test cases passed",
                actual_output="All test cases passed",
            )

        except Exception as e:
            return ExerciseResult(status=ExerciseStatus.ERROR, error_message=str(e))

    return test_function
