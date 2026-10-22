# src/ui.py

"""
Streamlit UI components for TaskPilot.
"""

import streamlit as st

from src.config import TASK_STATUSES
from src.models import Task
from src.task_manager import delete_task, update_task_status


# ---------------------------------------------------------------------------
# Task helpers & callbacks
# ---------------------------------------------------------------------------

def get_priority_icon(priority: str) -> str:
    """
    Return an icon corresponding to task priority.
    """

    priority_icons = {
        "High": "🔴",
        "Medium": "🟡",
        "Low": "🟢",
    }

    return priority_icons.get(priority, "⚪")


def get_status_icon(status: str) -> str:
    """
    Return an icon corresponding to task status.
    """

    status_icons = {
        "To Do": "📋",
        "In Progress": "⏳",
        "Done": "✅",
    }

    return status_icons.get(status, "📌")


def on_plan_status_change(task_id: str) -> None:
    """Callback triggered when task status is changed in the plan view."""
    new_status = st.session_state.get(f"status_{task_id}")
    if new_status:
        update_task_status(task_id=task_id, new_status=new_status)


def on_board_status_change(task_id: str) -> None:
    """Callback triggered when task status is changed in the board view."""
    new_status = st.session_state.get(f"board_status_{task_id}")
    if new_status:
        update_task_status(task_id=task_id, new_status=new_status)


def on_delete_task(task_id: str) -> None:
    """Callback triggered when a task is deleted."""
    delete_task(task_id)


# ---------------------------------------------------------------------------
# Task card
# ---------------------------------------------------------------------------

def render_task_card(
    task: Task,
    show_status_control: bool = False,
) -> None:
    """
    Render an individual task card.

    Parameters
    ----------
    task:
        Task object to render.

    show_status_control:
        Whether to display an interactive status selector.
    """

    priority_icon = get_priority_icon(task.priority)
    status_icon = get_status_icon(task.status)

    with st.container(border=True):
        st.markdown(f"**{task.title}**")

        st.caption(task.description)

        st.markdown(
            f"👤 **{task.assignee}** · "
            f"🛠️ {task.role}"
        )

        st.markdown(
            f"{priority_icon} **{task.priority}** · "
            f"⏱️ **{task.estimated_hours:g}h** · "
            f"{status_icon} **{task.status}**"
        )

        if show_status_control:
            plan_key = f"status_{task.id}"
            plan_kwargs = {
                "key": plan_key,
                "options": TASK_STATUSES,
                "on_change": on_plan_status_change,
                "args": (task.id,),
            }
            if plan_key not in st.session_state:
                plan_kwargs["index"] = TASK_STATUSES.index(task.status)

            st.selectbox(
                "Status",
                **plan_kwargs,
            )

        st.button(
            "Delete",
            key=f"delete_plan_{task.id}",
            width="stretch",
            on_click=on_delete_task,
            args=(task.id,),
        )


# ---------------------------------------------------------------------------
# Task plan
# ---------------------------------------------------------------------------

def render_task_plan(tasks: list[Task]) -> None:
    """
    Render all generated tasks.
    """

    st.subheader("Generated Task Plan")

    if not tasks:
        st.info("No tasks have been generated yet.")
        return

    for task in tasks:
        render_task_card(
            task,
            show_status_control=False,
        )


# ---------------------------------------------------------------------------
# Task board
# ---------------------------------------------------------------------------

def render_task_board(tasks: list[Task]) -> None:
    """
    Render an interactive Kanban-style task board.
    """

    st.subheader("Task Board")

    columns = st.columns(3)

    statuses = [
        ("To Do", columns[0]),
        ("In Progress", columns[1]),
        ("Done", columns[2]),
    ]

    for status, column in statuses:

        status_tasks = [
            task
            for task in tasks
            if task.status == status
        ]

        with column:

            st.markdown(
                f"### {status} "
                f"({len(status_tasks)})"
            )

            if not status_tasks:
                st.caption("No tasks")

            for task in status_tasks:

                with st.container(border=True):

                    st.markdown(
                        f"**{task.title}**"
                    )

                    st.caption(
                        task.description
                    )

                    st.caption(
                        f"👤 {task.assignee} · "
                        f"{task.estimated_hours:g}h"
                    )

                    priority_icon = get_priority_icon(
                        task.priority
                    )

                    st.caption(
                        f"{priority_icon} "
                        f"{task.priority}"
                    )

                    board_key = f"board_status_{task.id}"
                    board_kwargs = {
                        "key": board_key,
                        "options": TASK_STATUSES,
                        "on_change": on_board_status_change,
                        "args": (task.id,),
                    }
                    if board_key not in st.session_state:
                        board_kwargs["index"] = TASK_STATUSES.index(task.status)

                    st.selectbox(
                        "Move task",
                        **board_kwargs,
                    )

                    st.button(
                        "Delete",
                        key=f"delete_board_{task.id}",
                        width="stretch",
                        on_click=on_delete_task,
                        args=(task.id,),
                    )