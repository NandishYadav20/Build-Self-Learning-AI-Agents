"""
Self-Learning AI Agents Framework

A production-ready framework for building AI agents with:
- Long-term memory management
- Agentic patterns (prompt chaining, routing, parallelization)
- Tool use and function calling
- Structured output parsing
- Experience replay and learning
"""

__version__ = "1.0.0"
__author__ = "Nandish Yadav"

from .agents.base_agent import BaseAgent
from .agents.learning_agent import LearningAgent
from .agents.task_agent import TaskAgent
from .memory.memory_manager import MemoryManager
from .learning.learner import Learner

__all__ = [
    "BaseAgent",
    "LearningAgent",
    "TaskAgent",
    "MemoryManager",
    "Learner",
]
