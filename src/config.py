# src/config.py

"""
Application-wide configuration for TaskPilot AI.
"""

# ---------------------------------------------------------------------------
# Groq models
# ---------------------------------------------------------------------------

AVAILABLE_MODELS = {
    "GPT OSS 120B": "openai/gpt-oss-120b",
    "GPT OSS 20B": "openai/gpt-oss-20b",
    "Qwen 3.8 27B": "qwen/qwen3.8-27b",
}

DEFAULT_MODEL = "openai/gpt-oss-120b"


# ---------------------------------------------------------------------------
# Task configuration
# ---------------------------------------------------------------------------

TASK_PRIORITIES = [
    "Low",
    "Medium",
    "High",
]

TASK_STATUSES = [
    "To Do",
    "In Progress",
    "Done",
]


# ---------------------------------------------------------------------------
# Application configuration
# ---------------------------------------------------------------------------

APP_TITLE = "TaskPilot AI"
APP_ICON = "🤖"

MAX_TASKS_PER_REQUEST = 15