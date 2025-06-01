"""
Main benchmark runner that coordinates exercises and model evaluation.
"""

import time
import json
from typing import List, Optional
from dataclasses import dataclass, asdict
from colorama import Fore, init

from .exercise import Exercise, ExerciseResult, ExerciseStatus
from .ollama_client import OllamaClient

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Import HTML generation function
try:
    from generate_html_report import generate_html_report_file

    HTML_GENERATION_AVAILABLE = True
except ImportError:
    HTML_GENERATION_AVAILABLE = False


@dataclass
class BenchmarkStats:
    """Statistics for a benchmark run."""

    total_exercises: int
    passed_exercises: int
    failed_exercises: int
    error_exercises: int
    total_attempts: int
    total_time: float
    model_name: str

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_exercises == 0:
            return 0.0
        return (self.passed_exercises / self.total_exercises) * 100

    @property
    def average_attempts(self) -> float:
        """Calculate average attempts per exercise."""
        if self.total_exercises == 0:
            return 0.0
        return self.total_attempts / self.total_exercises


class BenchmarkRunner:
    """Main class for running LLM benchmarks."""

    def __init__(
        self,
        ollama_client: Optional[OllamaClient] = None,
        verbose: bool = True,
        save_results: bool = True,
        generate_html: bool = True,
        temperature: float = 0.0,
    ):
        self.client = ollama_client or OllamaClient()
        self.verbose = verbose
        self.save_results = save_results
        self.generate_html = generate_html
        self.temperature = temperature
        self.exercises: List[Exercise] = []
        self.current_stats: Optional[BenchmarkStats] = None

    def add_exercise(self, exercise: Exercise):
        """Add an exercise to the benchmark suite."""
        self.exercises.append(exercise)

    def add_exercises(self, exercises: List[Exercise]):
        """Add multiple exercises to the benchmark suite."""
        self.exercises.extend(exercises)

    def clean_code_response(self, response: str) -> str:
        """
        Clean the model's response to extract only the code.
        Removes markdown formatting and explanations.
        """
        # TODO: improve this
        think_index = response.find("</think>")
        if think_index != -1:
            response = response[think_index + len("</think>") :]

        lines = response.strip().split("\n")
        code_lines = []
        in_code_block = False

        for line in lines:
            # Skip markdown code block delimiters
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # If we're in a markdown code block, take everything
            if in_code_block:
                code_lines.append(line)
                continue

            # Skip lines that look like explanations
            stripped = line.strip()
            if not stripped:
                continue

            # Skip obvious explanation patterns
            explanation_patterns = [
                "here is",
                "here's",
                "this code",
                "this function",
                "explanation:",
                "solution:",
                "answer:",
                "output:",
                "the above",
                "this will",
                "this should",
            ]

            if any(pattern in stripped.lower() for pattern in explanation_patterns):
                continue

            # If the line looks like code (contains common code patterns)
            code_patterns = [
                "def ",
                "import ",
                "from ",
                "=",
                "if ",
                "for ",
                "while ",
                "class ",
                "return",
                "print(",
            ]
            if any(pattern in line for pattern in code_patterns) or line.startswith(
                "    "
            ):
                code_lines.append(line)
            elif (
                code_lines
            ):  # If we've started collecting code, include continuation lines
                code_lines.append(line)

        # If no clear code was found, return the original response
        if not code_lines:
            return response.strip()

        return "\n".join(code_lines).strip()

    def run_exercise(self, exercise: Exercise, model: str) -> bool:
        """
        Run a single exercise with the specified model.

        Args:
            exercise: The exercise to run
            model: Name of the model to use

        Returns:
            True if the exercise was completed successfully
        """
        if self.verbose:
            print(f"\n{Fore.CYAN}{'=' * 60}")
            print(f"{Fore.CYAN}Running Exercise: {exercise.name}")
            print(f"{Fore.CYAN}Difficulty: {exercise.difficulty}")
            print(f"{Fore.CYAN}{'=' * 60}")

        while exercise.can_retry():
            attempt_num = exercise.attempts + 1

            if self.verbose:
                print(f"\n{Fore.YELLOW}Attempt {attempt_num}/{exercise.max_attempts}")

            try:
                # Get the messages for this attempt (includes full conversation history on retries)
                messages = exercise.get_current_messages()

                if self.verbose and attempt_num > 1:
                    print(f"{Fore.YELLOW}Retrying with full conversation history...")
                    print(f"{Fore.YELLOW}Messages in conversation: {len(messages)}")

                # Get response from model using chat interface
                start_time = time.time()
                response = self.client.chat(
                    model, messages, temperature=self.temperature
                )
                generation_time = time.time() - start_time

                # Clean the response to extract only code
                code = self.clean_code_response(response)

                if self.verbose:
                    print(f"{Fore.BLUE}Generated code:")
                    print(f"{Fore.WHITE}{code}")

                # Execute the exercise
                result = exercise.execute(code)
                result.execution_time = generation_time

                # Display result
                if result.status == ExerciseStatus.PASSED:
                    if self.verbose:
                        print(f"\n{Fore.GREEN}✓ PASSED!")
                        if result.actual_output is not None:
                            print(f"{Fore.GREEN}Output: {result.actual_output}")
                    return True

                elif result.status == ExerciseStatus.FAILED:
                    if self.verbose:
                        print(f"\n{Fore.RED}✗ FAILED")
                        print(f"{Fore.RED}Expected: {result.expected_output}")
                        print(f"{Fore.RED}Got: {result.actual_output}")

                elif result.status == ExerciseStatus.ERROR:
                    if self.verbose:
                        print(f"\n{Fore.RED}✗ ERROR")
                        print(f"{Fore.RED}Error: {result.error_message}")

            except Exception as e:
                if self.verbose:
                    print(f"\n{Fore.RED}✗ SYSTEM ERROR: {str(e)}")

                # Create an error result
                error_result = ExerciseResult(
                    status=ExerciseStatus.ERROR, error_message=f"System error: {str(e)}"
                )
                exercise.results.append(error_result)
                exercise.attempts += 1

        if self.verbose:
            print(f"\n{Fore.RED}Exercise failed after {exercise.max_attempts} attempts")

        return False

    def run_benchmark(self, model: str) -> BenchmarkStats:
        """
        Run the complete benchmark suite with the specified model.

        Args:
            model: Name of the model to use

        Returns:
            BenchmarkStats object with results
        """
        if not self.client.is_available():
            raise Exception(
                "Ollama is not available. Make sure it's running on the expected port."
            )

        if self.verbose:
            print(f"\n{Fore.MAGENTA}{'=' * 70}")
            print(f"{Fore.MAGENTA}Starting LLM Benchmark")
            print(f"{Fore.MAGENTA}Model: {model}")
            print(f"{Fore.MAGENTA}Total Exercises: {len(self.exercises)}")
            print(f"{Fore.MAGENTA}{'=' * 70}")

        start_time = time.time()
        passed = 0
        failed = 0
        errors = 0
        total_attempts = 0

        for i, exercise in enumerate(self.exercises, 1):
            if self.verbose:
                print(f"\n{Fore.MAGENTA}Progress: {i}/{len(self.exercises)}")

            success = self.run_exercise(exercise, model)
            total_attempts += exercise.attempts

            if success:
                passed += 1
            else:
                # Determine if it was a failure or error
                if (
                    exercise.results
                    and exercise.results[-1].status == ExerciseStatus.ERROR
                ):
                    errors += 1
                else:
                    failed += 1

        total_time = time.time() - start_time

        # Create stats
        stats = BenchmarkStats(
            total_exercises=len(self.exercises),
            passed_exercises=passed,
            failed_exercises=failed,
            error_exercises=errors,
            total_attempts=total_attempts,
            total_time=total_time,
            model_name=model,
        )

        self.current_stats = stats

        # Display summary
        if self.verbose:
            self._display_summary(stats)

        # Save results if requested
        if self.save_results:
            self._save_results(stats)

        return stats

    def _display_summary(self, stats: BenchmarkStats):
        """Display a summary of the benchmark results."""
        print(f"\n{Fore.MAGENTA}{'=' * 70}")
        print(f"{Fore.MAGENTA}BENCHMARK SUMMARY")
        print(f"{Fore.MAGENTA}{'=' * 70}")
        print(f"{Fore.WHITE}Model: {stats.model_name}")
        print(f"{Fore.WHITE}Temperature: {self.temperature}")
        print(f"{Fore.WHITE}Total Exercises: {stats.total_exercises}")
        print(f"{Fore.GREEN}Passed: {stats.passed_exercises}")
        print(f"{Fore.RED}Failed: {stats.failed_exercises}")
        print(f"{Fore.RED}Errors: {stats.error_exercises}")
        print(f"{Fore.CYAN}Success Rate: {stats.success_rate:.1f}%")
        print(f"{Fore.CYAN}Average Attempts: {stats.average_attempts:.1f}")
        print(f"{Fore.CYAN}Total Time: {stats.total_time:.1f} seconds")
        print(f"{Fore.MAGENTA}{'=' * 70}")

    def _save_results(self, stats: BenchmarkStats):
        """Save detailed results to a JSON file and generate HTML report."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        json_filename = f"benchmark_results_{stats.model_name}_{timestamp}.json"

        # Prepare detailed results
        detailed_results = {"stats": asdict(stats), "exercises": []}

        for exercise in self.exercises:
            exercise_data = {
                "name": exercise.name,
                "description": exercise.description,
                "difficulty": exercise.difficulty,
                "max_attempts": exercise.max_attempts,
                "attempts": exercise.attempts,
                "completed": exercise.is_completed(),
                "chat_history": exercise.chat_history,  # Include full chat history
                "results": [],
            }

            for result in exercise.results:
                result_data = {
                    "status": result.status.value,
                    "expected_output": result.expected_output,
                    "actual_output": result.actual_output,
                    "error_message": result.error_message,
                    "execution_time": result.execution_time,
                    "code_generated": result.code_generated,
                }
                exercise_data["results"].append(result_data)

            detailed_results["exercises"].append(exercise_data)

        # Add calculated stats to the results
        detailed_results["stats"]["success_rate"] = stats.success_rate
        detailed_results["stats"]["average_attempts"] = stats.average_attempts

        try:
            # Save JSON results
            with open(json_filename, "w") as f:
                json.dump(detailed_results, f, indent=2, default=str)

            if self.verbose:
                print(f"\n{Fore.CYAN}Results saved to: {json_filename}")
                print(f"{Fore.CYAN}📜 Chat history included for conversation analysis")

            # Generate HTML report if HTML generation is available and enabled
            if HTML_GENERATION_AVAILABLE and self.generate_html:
                try:
                    html_filename = generate_html_report_file(detailed_results)
                    if self.verbose:
                        print(f"{Fore.CYAN}📊 HTML report generated: {html_filename}")
                        print(
                            f"{Fore.CYAN}🎨 Interactive report with syntax highlighting and chat history"
                        )
                except Exception as e:
                    if self.verbose:
                        print(
                            f"{Fore.YELLOW}Warning: Could not generate HTML report: {e}"
                        )
            elif not self.generate_html:
                if self.verbose:
                    print(
                        f"{Fore.YELLOW}📄 HTML report generation disabled (JSON only)"
                    )
                    print(
                        f"{Fore.YELLOW}Generate HTML manually with: python generate_html_report.py {json_filename}"
                    )
            else:
                if self.verbose:
                    print(
                        f"{Fore.YELLOW}Note: HTML generation not available. Install requirements for HTML reports."
                    )
                    print(
                        f"{Fore.YELLOW}You can generate HTML reports manually with: python generate_html_report.py {json_filename}"
                    )

        except Exception as e:
            if self.verbose:
                print(f"\n{Fore.YELLOW}Warning: Could not save results to file: {e}")

    def get_exercise_by_name(self, name: str) -> Optional[Exercise]:
        """Get an exercise by name."""
        for exercise in self.exercises:
            if exercise.name == name:
                return exercise
        return None

    def reset_exercises(self):
        """Reset all exercises to their initial state."""
        for exercise in self.exercises:
            exercise.reset()

    def generate_html_report(self, output_file: Optional[str] = None) -> Optional[str]:
        """
        Generate HTML report from current benchmark results.

        Args:
            output_file: Optional output filename

        Returns:
            Generated HTML filename if successful, None otherwise
        """
        if not self.current_stats:
            print(f"{Fore.RED}No benchmark results available. Run benchmark first.")
            return None

        if not HTML_GENERATION_AVAILABLE:
            print(
                f"{Fore.RED}HTML generation not available. Check generate_html_report.py is in the path."
            )
            return None

        # Prepare results data
        detailed_results = {"stats": asdict(self.current_stats), "exercises": []}

        for exercise in self.exercises:
            exercise_data = {
                "name": exercise.name,
                "description": exercise.description,
                "difficulty": exercise.difficulty,
                "max_attempts": exercise.max_attempts,
                "attempts": exercise.attempts,
                "completed": exercise.is_completed(),
                "chat_history": exercise.chat_history,
                "results": [],
            }

            for result in exercise.results:
                result_data = {
                    "status": result.status.value,
                    "expected_output": result.expected_output,
                    "actual_output": result.actual_output,
                    "error_message": result.error_message,
                    "execution_time": result.execution_time,
                    "code_generated": result.code_generated,
                }
                exercise_data["results"].append(result_data)

            detailed_results["exercises"].append(exercise_data)

        # Add calculated stats
        detailed_results["stats"]["success_rate"] = self.current_stats.success_rate
        detailed_results["stats"]["average_attempts"] = (
            self.current_stats.average_attempts
        )

        try:
            html_filename = generate_html_report_file(detailed_results, output_file)
            if self.verbose:
                print(f"{Fore.GREEN}📊 HTML report generated: {html_filename}")
            return html_filename
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}Error generating HTML report: {e}")
            return None
