#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of the LLM benchmarking framework.
"""

from benchmarker import BenchmarkRunner, OllamaClient, Exercise
from benchmarker.exercise import create_function_test, create_code_execution_test
from exercises import get_basic_exercises


def custom_exercise_example():
    """Create a custom exercise to demonstrate flexibility."""
    return Exercise(
        name="Custom String Length",
        description="Write a function called 'string_length' that returns the length of a string without using len().",
        test_function=create_function_test(
            "string_length",
            [
                {"input": "hello", "output": 5},
                {"input": "", "output": 0},
                {"input": "Python", "output": 6},
                {"input": "a", "output": 1},
            ],
        ),
        difficulty="easy",
        max_attempts=2,
    )


def run_custom_benchmark():
    """Example of running a custom benchmark with specific exercises."""
    print("=== Custom Benchmark Example ===")

    # Create Ollama client
    client = OllamaClient()

    # Check if Ollama is available
    if not client.is_available():
        print("Ollama is not available. Please start Ollama service.")
        return

    # Get available models
    try:
        models = client.list_models()
        print(f"Available models: {', '.join(models)}")

        if not models:
            print("No models available. Please pull a model first:")
            print("ollama pull llama2")
            return

        # Use the first available model
        model_name = models[0]
        print(f"Using model: {model_name}")

    except Exception as e:
        print(f"Error getting models: {e}")
        return

    # Create benchmark runner
    runner = BenchmarkRunner(ollama_client=client, verbose=True, save_results=True)

    # Add some basic exercises
    basic_exercises = get_basic_exercises()[:3]  # Just first 3 exercises
    runner.add_exercises(basic_exercises)

    # Add our custom exercise
    runner.add_exercise(custom_exercise_example())

    # Run the benchmark
    try:
        print(f"\nRunning benchmark with {len(runner.exercises)} exercises...")
        stats = runner.run_benchmark(model_name)

        print(f"\n=== Results Summary ===")
        print(f"Model: {stats.model_name}")
        print(f"Success Rate: {stats.success_rate:.1f}%")
        print(f"Passed: {stats.passed_exercises}")
        print(f"Failed: {stats.failed_exercises}")
        print(f"Errors: {stats.error_exercises}")
        print(f"Average Attempts: {stats.average_attempts:.1f}")
        print(f"Total Time: {stats.total_time:.1f} seconds")

    except Exception as e:
        print(f"Error running benchmark: {e}")


def test_single_exercise():
    """Example of testing a single exercise directly."""
    print("\n=== Single Exercise Test ===")

    # Create a simple exercise
    exercise = Exercise(
        name="Simple Math",
        description="Write code that calculates 2 + 2 and assigns it to a variable called 'result'.",
        test_function=create_code_execution_test(4),
        max_attempts=1,
    )

    # Test with manually provided code
    test_code = "result = 2 + 2"
    result = exercise.execute(test_code)

    print(f"Exercise: {exercise.name}")
    print(f"Test Code: {test_code}")
    print(f"Result: {result.status.value}")
    print(f"Expected: {result.expected_output}")
    print(f"Actual: {result.actual_output}")


def demonstrate_error_feedback():
    """Demonstrate the error feedback mechanism."""
    print("\n=== Error Feedback Example ===")

    # Create an exercise
    exercise = Exercise(
        name="Fibonacci",
        description="Write a function called 'fibonacci' that returns the nth Fibonacci number.",
        test_function=create_function_test(
            "fibonacci",
            [
                {"input": 5, "output": 5},
                {"input": 6, "output": 8},
            ],
        ),
        max_attempts=3,
    )

    # Show prompts for different scenarios
    print("Initial prompt:")
    print("-" * 50)
    print(exercise.get_prompt())

    # Simulate a failed attempt
    bad_code = "def fibonacci(n): return n"
    result = exercise.execute(bad_code)

    print(f"\nAfter failed attempt (status: {result.status.value}):")
    print("-" * 50)
    print(exercise.get_retry_prompt(result))


if __name__ == "__main__":
    print("LLM Benchmarking Framework - Example Usage")
    print("=" * 50)

    # Run different examples
    test_single_exercise()
    demonstrate_error_feedback()

    # Run full benchmark (uncomment to test with actual Ollama)
    # run_custom_benchmark()
