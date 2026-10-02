# src/task_manager.py

"""
Task state management for TaskPilot.

The MVP uses Streamlit session state instead of a database.
"""

import streamlit as st

from src.models import Task


TASK_STATE_KEY = "tasks"


def initialize_task_state() -> None:
    """
    Initialize the task list in Streamlit session state.
    """

    if TASK_STATE_KEY not in st.session_state:
        st.session_state[TASK_STATE_KEY] = []


def get_tasks() -> list[Task]:
    """
    Return all currently stored tasks.
    """

    initialize_task_state()

    return st.session_state[TASK_STATE_KEY]


def add_tasks(tasks: list[Task]) -> None:
    """
    Add generated tasks to the current task list.
    """

    initialize_task_state()

    st.session_state[TASK_STATE_KEY].extend(tasks)


def update_task_status(
    task_id: str,
    new_status: str,
) -> None:
    """
    Update the status of a task.
    """

    initialize_task_state()

    for task in st.session_state[TASK_STATE_KEY]:
        if task.id == task_id:
            task.status = new_status
            break


def clear_tasks() -> None:
    """
    Remove all tasks from the current session.
    """

    st.session_state[TASK_STATE_KEY] = []