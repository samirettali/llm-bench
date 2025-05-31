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
        self.chat_history: List[Dict[str, str]] = []

    def get_initial_messages(self) -> List[Dict[str, str]]:
        """Generate the initial chat messages for this exercise."""
        system_message = {
            "role": "system",
            "content": """You are an expert Python programmer. Your task is to solve coding problems by writing clean, working Python code.

IMPORTANT RULES:
- Output ONLY the executable Python code, no markdown formatting
- Do not include explanations, comments, or descriptions outside the code
- Do not use ```python or ``` code blocks
- The code should be ready to execute immediately
- Focus on correctness and simplicity
- If you make an error, learn from the feedback and fix it in the next attempt sending back the entire code.
- Only the code in the last message you send will be executed.""",
        }

        user_message = {
            "role": "user",
            "content": f"""Solve this coding problem:

{self.description}

Provide only the Python code that solves this problem.""",
        }

        return [system_message, user_message]

    def get_retry_messages(
        self, previous_result: ExerciseResult
    ) -> List[Dict[str, str]]:
        """Generate retry messages based on the previous result."""
        # Start with existing chat history
        messages = self.chat_history.copy()

        # Add feedback about the previous attempt
        error_info = ""
        if previous_result.error_message:
            error_info = f"Error: {previous_result.error_message}"
        elif (
            previous_result.actual_output is not None
            and previous_result.expected_output is not None
        ):
            error_info = f"Expected: {previous_result.expected_output}, but got: {previous_result.actual_output}"

        feedback_message = {
            "role": "user",
            "content": f"""Your previous solution failed. Here's what went wrong:
{error_info}

Please analyze the error and provide a corrected version. Remember to output only the Python code without any formatting or explanations.""",
        }

        messages.append(feedback_message)
        return messages

    def execute(self, code: str) -> ExerciseResult:
        """Execute the provided code and return the result."""
        self.attempts += 1
        result = self.test_function(code)
        result.code_generated = code
        self.results.append(result)

        # Add the assistant's response to chat history
        if self.attempts == 1:
            # First attempt - initialize with initial messages
            self.chat_history = self.get_initial_messages()

        # Add the model's response to chat history
        self.chat_history.append({"role": "assistant", "content": code})

        return result

    def get_current_messages(self) -> List[Dict[str, str]]:
        """Get the current chat messages for the next attempt."""
        if self.attempts == 0:
            return self.get_initial_messages()
        else:
            # Get retry messages based on the last result
            last_result = self.results[-1]
            return self.get_retry_messages(last_result)

    def is_completed(self) -> bool:
        """Check if this exercise has been completed successfully."""
        return any(result.status == ExerciseStatus.PASSED for result in self.results)

    def can_retry(self) -> bool:
        """Check if this exercise can be retried."""
        return self.attempts < self.max_attempts and not self.is_completed()

    def reset(self):
        """Reset the exercise to initial state."""
        self.attempts = 0
        self.results = []
        self.chat_history = []


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
    function_name: str, test_cases: List[Dict[str, Any]]
) -> Callable[[str], ExerciseResult]:
    """
    Create a test function that tests a specific function with multiple test cases.

    Args:
        function_name: Name of the function to test
        test_cases: List of dictionaries with 'input' and 'output' keys
                   where 'input' can be:
                   - A single value (scalar, list, tuple, etc.) for single-argument functions
                   - A tuple/list of multiple values to be unpacked as separate arguments
                   and 'output' is the expected result

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
            for i, test_case in enumerate(test_cases):
                if "input" not in test_case or "output" not in test_case:
                    return ExerciseResult(
                        status=ExerciseStatus.ERROR,
                        error_message=f"Test case {i + 1} must have 'input' and 'output' fields",
                    )

                inputs = test_case["input"]
                expected = test_case["output"]

                # Call function with inputs
                # If inputs is a tuple with multiple elements, unpack them as separate arguments
                # Otherwise, pass inputs as a single argument (even if it's a tuple/list)
                try:
                    if isinstance(inputs, tuple) and len(inputs) > 1:
                        # This is for functions that take multiple arguments
                        actual = func(*inputs)
                    else:
                        # This is for functions that take a single argument
                        # (which could be a scalar, list, tuple, etc.)
                        actual = func(inputs)
                except TypeError as e:
                    # If we get a TypeError, it might be because we need to try the other way
                    # This handles edge cases where the distinction isn't clear
                    try:
                        if isinstance(inputs, tuple) and len(inputs) > 1:
                            actual = func(inputs)
                        else:
                            actual = (
                                func(*inputs)
                                if isinstance(inputs, (tuple, list))
                                else func(inputs)
                            )
                    except:
                        return ExerciseResult(
                            status=ExerciseStatus.ERROR,
                            error_message=f"Test case {i + 1} failed to execute: {str(e)}",
                        )

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
