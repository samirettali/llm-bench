# LLM Benchmarking Framework

A comprehensive Python framework for benchmarking Large Language Models (LLMs) using Ollama. This framework tests LLMs on various programming tasks with automatic code execution and validation.

## Features

- **Ollama Integration**: Seamless integration with Ollama for local LLM inference
- **Automatic Code Extraction**: Intelligent extraction of code from LLM responses
- **Progressive Difficulty**: Basic, intermediate, advanced, and super hard programming exercises
- **Error Feedback Loop**: Failed attempts receive error feedback for retry
- **Chat History Tracking**: Full conversation history for analysis
- **Automatic HTML Reports**: Beautiful, interactive HTML reports with syntax highlighting
- **Comprehensive Reporting**: Detailed statistics and JSON result export
- **Colored Output**: Beautiful terminal output with progress indicators
- **Flexible Configuration**: Customizable attempts, timeouts, and exercise selection

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install and start Ollama:**
```bash
# Install Ollama (visit https://ollama.ai for platform-specific instructions)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

3. **Pull a model (optional - the framework can do this automatically):**
```bash
ollama pull llama2  # or any other model you want to test
```

## Quick Start

Run a benchmark with a specific model:

```bash
python run_benchmark.py llama2
```

Run only basic exercises:
```bash
python run_benchmark.py llama2 --difficulty basic
```

Run in quiet mode:
```bash
python run_benchmark.py codellama --quiet
```

## Usage

### Command Line Options

```bash
python run_benchmark.py <model_name> [options]
```

**Arguments:**
- `model_name`: Name of the Ollama model to benchmark (required)

**Options:**
- `--difficulty {basic,intermediate,advanced,super_hard,all}`: Exercise difficulty level (default: all)
- `--max-attempts N`: Maximum attempts per exercise (default: 3)
- `--ollama-url URL`: Ollama API URL (default: http://localhost:11434)
- `--quiet`: Run in quiet mode with minimal output
- `--no-save`: Don't save results to files
- `--json-only`: Save only JSON results (no HTML report)

### Examples

```bash
# Test all exercises with llama2
python run_benchmark.py llama2

# Test only basic exercises with codellama
python run_benchmark.py codellama --difficulty basic

# Allow up to 5 attempts per exercise
python run_benchmark.py mistral --max-attempts 5

# Connect to Ollama on different host
python run_benchmark.py llama2 --ollama-url http://192.168.1.100:11434

# Run quietly without saving results
python run_benchmark.py llama2 --quiet --no-save

# Save only JSON results (no HTML report)
python run_benchmark.py llama2 --json-only

# Test super hard exercises
python run_benchmark.py llama2 --difficulty super_hard
```

## Exercise Categories

### Basic Exercises (8 exercises)
- Simple Addition
- String Reversal
- List Maximum
- Even or Odd Check
- Sum of List
- Count Vowels
- Print Hello World
- Calculate Average

### Intermediate Exercises (8 exercises)
- Factorial Function
- Fibonacci Sequence
- Prime Number Check
- Palindrome Check
- Bubble Sort
- Word Count
- Binary Search
- Anagram Check

### Advanced Exercises (8 exercises)
- Merge Sort
- Longest Common Subsequence
- Valid Parentheses
- Depth-First Search
- Coin Change (Dynamic Programming)
- Binary Tree Max Depth
- String Pattern Matching
- LRU Cache Implementation

## Framework Architecture

### Core Components

1. **BenchmarkRunner** (`benchmarker/runner.py`):
   - Main orchestrator for benchmark execution
   - Handles model communication and result aggregation
   - Provides colored terminal output and progress tracking

2. **Exercise** (`benchmarker/exercise.py`):
   - Defines individual programming challenges
   - Manages test cases and validation logic
   - Handles retry attempts with error feedback

3. **OllamaClient** (`benchmarker/ollama_client.py`):
   - Handles communication with Ollama API
   - Manages model availability and pulling
   - Provides error handling and timeouts

4. **Exercise Collections** (`exercises/`):
   - Organized by difficulty level
   - Easy to extend with new challenges
   - Comprehensive test case coverage

### Key Features

#### Intelligent Code Extraction
The framework automatically extracts executable code from LLM responses by:
- Removing markdown formatting (```python blocks)
- Filtering out explanatory text
- Preserving code structure and indentation
- Handling various response formats

#### Error Feedback Loop
When an exercise fails, the framework:
1. Captures the specific error or wrong output
2. Generates a retry prompt with error information
3. Allows the model to fix the issue
4. Tracks attempts and provides detailed failure analysis

#### Comprehensive Testing
Each exercise includes:
- Multiple test cases covering edge cases
- Clear function signatures and requirements
- Automatic execution and validation
- Performance timing and statistics

## Output and Results

### Terminal Output
The framework provides rich terminal output including:
- Progress indicators for each exercise
- Color-coded results (green for pass, red for fail)
- Generated code display
- Error messages and feedback
- Final statistics summary

### JSON Results
Detailed results are automatically saved to timestamped JSON files containing:
- Overall statistics (success rate, timing, attempts)
- Per-exercise results and attempts
- Generated code for each attempt
- Error messages and execution details

Example result file: `benchmark_results_llama2_20241215_143022.json`

## Extending the Framework

### Adding New Exercises

Create new exercises by extending the exercise collections:

```python
from benchmarker.exercise import Exercise, create_function_test

def my_custom_exercise():
    return Exercise(
        name="Custom Exercise",
        description="Write a function called 'my_func' that does something specific.",
        test_function=create_function_test("my_func", [
            (input1, expected_output1),
            (input2, expected_output2),
        ]),
        difficulty="medium"
    )
```

### Custom Test Functions

Create specialized test functions for complex validation:

```python
def custom_test_function(code: str) -> ExerciseResult:
    try:
        # Custom validation logic
        namespace = {}
        exec(code, namespace)
        
        # Your specific testing logic here
        if validation_passes:
            return ExerciseResult(status=ExerciseStatus.PASSED)
        else:
            return ExerciseResult(status=ExerciseStatus.FAILED, error_message="Custom error")
    except Exception as e:
        return ExerciseResult(status=ExerciseStatus.ERROR, error_message=str(e))
```

## Troubleshooting

### Common Issues

1. **Ollama not available**:
   - Ensure Ollama is installed and running (`ollama serve`)
   - Check that the service is accessible on the specified port
   - Verify firewall settings if using remote Ollama

2. **Model not found**:
   - The framework will attempt to pull missing models automatically
   - Manually pull with: `ollama pull <model_name>`
   - Check model name spelling and availability

3. **Code execution errors**:
   - Some models may generate non-executable code
   - The framework provides error feedback for retries
   - Check the generated code in verbose mode for debugging

4. **Timeout issues**:
   - Increase timeout values in `ollama_client.py` if needed
   - Some models may require longer generation times
   - Consider using faster models for initial testing

### Performance Tips

- Use `--difficulty basic` for quick model evaluation
- Use `--quiet` mode for automated testing
- Run single exercises for debugging specific issues
- Monitor system resources during benchmarks

## Contributing

Contributions are welcome! Areas for improvement:
- Additional exercise categories (e.g., data science, web development)
- Support for other LLM providers
- Enhanced code parsing and validation
- Performance optimizations
- Additional output formats

## License

This project is open source and available under the MIT License.

## Report Generation

### Automatic HTML Reports

By default, the framework generates both JSON results and interactive HTML reports:

```bash
# Default: JSON + HTML reports
python run_benchmark.py llama2

# JSON only (faster, no HTML)
python run_benchmark.py llama2 --json-only
```

### Manual HTML Generation

You can also generate HTML reports manually from existing JSON results:

```bash
# Generate HTML from specific JSON file
python generate_html_report.py benchmark_results_llama2_20241215_143022.json

# Generate with custom filename
python generate_html_report.py results.json -o custom_report.html
```

### HTML Report Features

The generated HTML reports include:
- **Interactive Design**: Responsive layout with modern styling
- **Syntax Highlighting**: Python code with syntax highlighting and copy buttons
- **Chat History**: Full conversation flow between user and model
- **Statistics Dashboard**: Visual stats with success rates and timing
- **Exercise Details**: Expandable sections with test cases and results
- **Error Analysis**: Clear display of failed attempts and error messages
