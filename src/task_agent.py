# src/task_agent.py

"""
Core AI task planning logic for TaskPilot.
"""

from langchain_core.runnables import Runnable

from src.models import TaskPlan
from src.prompts import TASK_PLANNING_PROMPT, format_team_for_prompt


def create_task_planner(llm) -> Runnable:
    """
    Create a LangChain task-planning chain.

    The LLM is configured to return a validated TaskPlan object.
    """

    structured_llm = llm.with_structured_output(TaskPlan)

    chain = TASK_PLANNING_PROMPT | structured_llm

    return chain


def generate_task_plan(
    user_request: str,
    team_members,
    llm,
) -> TaskPlan:
    """
    Generate a structured task plan from a natural-language request.
    """

    if not user_request.strip():
        raise ValueError("Task request cannot be empty.")

    team_text = format_team_for_prompt(team_members)

    planner = create_task_planner(llm)

    task_plan = planner.invoke(
        {
            "user_request": user_request,
            "team": team_text,
        }
    )

    return task_plan