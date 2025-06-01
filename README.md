# LLM Benchmarking Framework

A comprehensive Python framework for benchmarking Large Language Models (LLMs) using OpenRouter. This framework tests LLMs on various programming tasks with automatic code execution and validation, giving you access to models from OpenAI, Anthropic, Google, Meta, and many other providers.

## Features

- **OpenRouter Integration**: Access to 100+ models from multiple providers (OpenAI, Anthropic, Google, Meta, etc.)
- **Unified API**: Test different models through a single, consistent interface
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

2. **Get an OpenRouter API key:**
   - Visit [OpenRouter](https://openrouter.ai/keys)
   - Create an account and generate an API key
   - Set your API key as an environment variable:

```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

3. **List available models (optional):**
```bash
python run_benchmark.py --list-models
```

## Quick Start

Run a benchmark with GPT-4:

```bash
python run_benchmark.py openai/gpt-4
```

Test Claude 3 with basic exercises only:
```bash
python run_benchmark.py anthropic/claude-3-sonnet --difficulty basic
```

Run quietly with Llama 3:
```bash
python run_benchmark.py meta-llama/llama-3-70b-instruct --quiet
```

## Usage

### Command Line Options

```bash
python run_benchmark.py <model_name> [options]
```

**Arguments:**
- `model_name`: Name of the model to benchmark (e.g., 'openai/gpt-4', 'anthropic/claude-3-sonnet')

**Options:**
- `--difficulty {basic,intermediate,advanced,super_hard,all}`: Exercise difficulty level (default: all)
- `--max-attempts N`: Maximum attempts per exercise (default: 3)
- `--api-key KEY`: OpenRouter API key (or set OPENROUTER_API_KEY environment variable)
- `--base-url URL`: OpenRouter API base URL (default: https://openrouter.ai/api/v1)
- `--quiet`: Run in quiet mode with minimal output
- `--no-save`: Don't save results to files
- `--json-only`: Save only JSON results (no HTML report)
- `--temperature TEMP`: Temperature for the model (default: 0.0)
- `--output-folder FOLDER`: Output folder for saving results (default: reports)
- `--list-models`: List available models and exit

### Popular Models

**OpenAI Models:**
- `openai/gpt-4-turbo-preview`
- `openai/gpt-4`
- `openai/gpt-3.5-turbo`

**Anthropic Models:**
- `anthropic/claude-3-opus`
- `anthropic/claude-3-sonnet`
- `anthropic/claude-3-haiku`

**Google Models:**
- `google/gemini-pro`
- `google/gemini-pro-vision`

**Meta Models:**
- `meta-llama/llama-3-70b-instruct`
- `meta-llama/llama-3-8b-instruct`

**Mistral Models:**
- `mistralai/mistral-large`
- `mistralai/mistral-medium`

### Examples

```bash
# Test all exercises with GPT-4
python run_benchmark.py openai/gpt-4

# Test only basic exercises with Claude 3
python run_benchmark.py anthropic/claude-3-sonnet --difficulty basic

# Allow up to 5 attempts per exercise
python run_benchmark.py meta-llama/llama-3-70b-instruct --max-attempts 5

# Use custom API key
python run_benchmark.py openai/gpt-3.5-turbo --api-key sk-your-key-here

# Run quietly without saving results
python run_benchmark.py google/gemini-pro --quiet --no-save

# Save only JSON results (no HTML report)
python run_benchmark.py mistralai/mistral-large --json-only

# Test super hard exercises with high temperature
python run_benchmark.py anthropic/claude-3-opus --difficulty super_hard --temperature 0.3

# List all available models
python run_benchmark.py --list-models
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
   - Handles OpenRouter API communication and result aggregation
   - Provides colored terminal output and progress tracking

2. **Exercise** (`benchmarker/exercise.py`):
   - Defines individual programming challenges
   - Manages test cases and validation logic
   - Handles retry attempts with error feedback

3. **Exercise Collections** (`exercises/`):
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

Example result file: `benchmark_results_openai_gpt-4_20241215_143022.json`

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

1. **API key not working**:
   - Verify your OpenRouter API key is correct
   - Check that you have sufficient credits in your OpenRouter account
   - Ensure the environment variable is set correctly: `echo $OPENROUTER_API_KEY`

2. **Model not found**:
   - Use `--list-models` to see available models
   - Check the exact model name format (e.g., 'openai/gpt-4', not 'gpt-4')
   - Some models may require special access or approval

3. **Rate limiting**:
   - OpenRouter may rate limit requests based on your plan
   - Consider adding delays between requests for high-volume testing
   - Check your usage dashboard at OpenRouter

4. **Code execution errors**:
   - Some models may generate non-executable code
   - The framework provides error feedback for retries
   - Check the generated code in verbose mode for debugging

5. **Network connectivity**:
   - Ensure stable internet connection
   - Check if your firewall allows HTTPS traffic to openrouter.ai
   - Consider using --base-url if you need to use a different endpoint

### Performance Tips

- Use `--difficulty basic` for quick model evaluation
- Use `--quiet` mode for automated testing
- Start with smaller, faster models for debugging
- Monitor your OpenRouter usage and costs
- Use temperature 0.0 for reproducible results

## Model Costs

Different models have different costs per token. Check [OpenRouter's pricing](https://openrouter.ai/docs#models) for current rates. The framework will show token usage in verbose mode to help you track costs.

**Cost-effective models for testing:**
- `meta-llama/llama-3-8b-instruct` (free tier available)
- `mistralai/mistral-7b-instruct` (very low cost)
- `openai/gpt-3.5-turbo` (good balance of cost and performance)

**Premium models for best performance:**
- `anthropic/claude-3-opus`
- `openai/gpt-4-turbo-preview`
- `google/gemini-pro`

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
