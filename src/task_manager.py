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
    Update the status of a specific task.
    """

    initialize_task_state()

    for task in st.session_state[TASK_STATE_KEY]:
        if task.id == task_id:
            task.status = new_status
            break



def delete_task(task_id: str) -> None:
    """
    Delete a specific task and clean up associated session state keys.
    """

    initialize_task_state()

    st.session_state[TASK_STATE_KEY] = [
        task
        for task in st.session_state[TASK_STATE_KEY]
        if task.id != task_id
    ]

    # Clean up associated session keys
    st.session_state.pop(f"status_{task_id}", None)
    st.session_state.pop(f"board_status_{task_id}", None)
    st.session_state.pop(f"delete_plan_{task_id}", None)
    st.session_state.pop(f"delete_board_{task_id}", None)


def clear_tasks() -> None:
    """
    Remove all tasks from the current session and clean up session keys.
    """

    initialize_task_state()

    for task in st.session_state.get(TASK_STATE_KEY, []):
        st.session_state.pop(f"status_{task.id}", None)
        st.session_state.pop(f"board_status_{task.id}", None)
        st.session_state.pop(f"delete_plan_{task.id}", None)
        st.session_state.pop(f"delete_board_{task.id}", None)

    st.session_state[TASK_STATE_KEY] = []