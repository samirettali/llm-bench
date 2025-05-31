"""
LLM Benchmarking Framework using Ollama
"""

__version__ = "1.0.0"

from .runner import BenchmarkRunner
from .exercise import Exercise, ExerciseResult
from .ollama_client import OllamaClient

__all__ = ["BenchmarkRunner", "Exercise", "ExerciseResult", "OllamaClient"]
