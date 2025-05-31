#!/usr/bin/env python3
"""
Main script to run LLM benchmarking using Ollama.
"""

import argparse
import sys
from typing import List

from benchmarker import BenchmarkRunner, OllamaClient
from exercises import (
    get_basic_exercises,
    get_intermediate_exercises,
    get_advanced_exercises,
    get_super_hard_exercises,
)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LLM Benchmarking Framework using Ollama"
    )
    parser.add_argument("model", help="Name of the Ollama model to benchmark")
    parser.add_argument(
        "--difficulty",
        choices=["basic", "intermediate", "advanced", "super_hard", "all"],
        default="all",
        help="Difficulty level of exercises to run",
    )
    parser.add_argument(
        "--max-attempts", type=int, default=3, help="Maximum attempts per exercise"
    )
    parser.add_argument(
        "--ollama-url", default="http://localhost:11434", help="Ollama API URL"
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Run in quiet mode (less verbose output)"
    )
    parser.add_argument(
        "--no-save", action="store_true", help="Don't save results to file"
    )

    return parser.parse_args()


def load_exercises(difficulty: str, max_attempts: int) -> List:
    """Load exercises based on difficulty level."""
    exercises = []

    if difficulty in ["basic", "all"]:
        basic_exercises = get_basic_exercises()
        for exercise in basic_exercises:
            exercise.max_attempts = max_attempts
        exercises.extend(basic_exercises)

    if difficulty in ["intermediate", "all"]:
        intermediate_exercises = get_intermediate_exercises()
        for exercise in intermediate_exercises:
            exercise.max_attempts = max_attempts
        exercises.extend(intermediate_exercises)

    if difficulty in ["advanced", "all"]:
        advanced_exercises = get_advanced_exercises()
        for exercise in advanced_exercises:
            exercise.max_attempts = max_attempts
        exercises.extend(advanced_exercises)

    if difficulty in ["super_hard", "all"]:
        super_hard_exercises = get_super_hard_exercises()
        for exercise in super_hard_exercises:
            exercise.max_attempts = max_attempts
        exercises.extend(super_hard_exercises)

    return exercises


def main():
    """Main function to run the benchmark."""
    args = parse_arguments()

    # Create Ollama client
    client = OllamaClient(base_url=args.ollama_url)

    # Check if Ollama is available
    if not client.is_available():
        print(f"Error: Cannot connect to Ollama at {args.ollama_url}")
        print("Make sure Ollama is running and accessible.")
        sys.exit(1)

    # Check if model is available
    try:
        available_models = client.list_models()
        if args.model not in available_models:
            print(f"Model '{args.model}' not found in available models.")
            print(f"Available models: {', '.join(available_models)}")
            print(f"Attempting to pull model '{args.model}'...")

            if not client.pull_model(args.model):
                print(
                    f"Failed to pull model '{args.model}'. Please check the model name."
                )
                sys.exit(1)
            print(f"Successfully pulled model '{args.model}'")

    except Exception as e:
        print(f"Error checking available models: {e}")
        sys.exit(1)

    # Load exercises
    exercises = load_exercises(args.difficulty, args.max_attempts)

    if not exercises:
        print("No exercises loaded. Check difficulty setting.")
        sys.exit(1)

    # Create benchmark runner
    runner = BenchmarkRunner(
        ollama_client=client, verbose=not args.quiet, save_results=not args.no_save
    )

    # Add exercises to runner
    runner.add_exercises(exercises)

    # Run benchmark
    try:
        print(
            f"Starting benchmark for model '{args.model}' with {len(exercises)} exercises..."
        )
        stats = runner.run_benchmark(args.model)

        # Print final summary
        if args.quiet:
            print(f"\nBenchmark completed!")
            print(
                f"Success rate: {stats.success_rate:.1f}% ({stats.passed_exercises}/{stats.total_exercises})"
            )
            print(f"Total time: {stats.total_time:.1f} seconds")

        # Exit with appropriate code
        sys.exit(0 if stats.success_rate > 0 else 1)

    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running benchmark: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
