"""
Standard exercises for LLM benchmarking.
"""

from .basic_exercises import get_basic_exercises
from .intermediate_exercises import get_intermediate_exercises
from .advanced_exercises import get_advanced_exercises
from .super_hard_exercises import get_super_hard_exercises

__all__ = [
    "get_basic_exercises",
    "get_intermediate_exercises",
    "get_advanced_exercises",
    "get_super_hard_exercises",
]
