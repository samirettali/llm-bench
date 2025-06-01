#!/usr/bin/env python3
"""
Main script to run LLM benchmarking using OpenRouter.
"""

import argparse
import os
import sys
from typing import List

from benchmarker import BenchmarkRunner
from exercises import (
    get_basic_exercises,
    get_intermediate_exercises,
    get_advanced_exercises,
    get_super_hard_exercises,
)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LLM Benchmarking Framework using OpenRouter"
    )
    parser.add_argument(
        "model",
        help="Name of the model to benchmark (e.g., 'openai/gpt-4', 'anthropic/claude-3-sonnet')",
    )
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
        "--api-key",
        help="OpenRouter API key (or set OPENROUTER_API_KEY environment variable)",
    )
    parser.add_argument(
        "--base-url",
        default="https://openrouter.ai/api/v1",
        help="OpenRouter API base URL",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Run in quiet mode (less verbose output)"
    )
    parser.add_argument(
        "--no-save", action="store_true", help="Don't save results to files"
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Save only JSON results (no HTML report)",
    )
    parser.add_argument(
        "--temperature", type=float, default=0.0, help="Temperature for the model"
    )
    parser.add_argument(
        "--output-folder",
        default="reports",
        help="Output folder for saving results (default: reports)",
    )
    parser.add_argument(
        "--list-models", action="store_true", help="List available models and exit"
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

    # Check for API key
    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OpenRouter API key is required.")
        print("Set OPENROUTER_API_KEY environment variable or use --api-key argument.")
        print("Get your API key from: https://openrouter.ai/keys")
        sys.exit(1)

    # Load exercises
    exercises = load_exercises(args.difficulty, args.max_attempts)

    if not exercises:
        print("No exercises loaded. Check difficulty setting.")
        sys.exit(1)

    if args.output_folder and not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # Create benchmark runner
    try:
        runner = BenchmarkRunner(
            verbose=not args.quiet,
            save_results=not args.no_save,
            generate_html=not args.json_only,
            output_folder=args.output_folder,
            api_key=api_key,
            base_url=args.base_url,
            temperature=args.temperature,
        )
    except Exception as e:
        print(f"Error creating benchmark runner: {e}")
        sys.exit(1)

    # Add exercises to runner
    runner.add_exercises(exercises)

    # Run benchmark
    try:
        print(
            f"Starting benchmark for model '{args.model}' with {len(exercises)} exercises..."
        )
        print(f"Using OpenRouter API at {args.base_url}")

        if not args.no_save:
            if args.json_only:
                print("📄 Results will be saved as JSON only")
            else:
                print("📊 Results will be saved as JSON + HTML report")

        stats = runner.run_benchmark(args.model)

        # Generate additional HTML report if requested manually
        if args.json_only and not args.no_save:
            if not args.quiet:
                print("\n💡 Tip: Generate HTML report with:")
                print(
                    f"python generate_html_report.py benchmark_results_{args.model.replace('/', '_')}_*.json"
                )

        # Display final summary
        if args.quiet:
            print("\nBenchmark completed!")
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
