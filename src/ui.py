# src/ui.py

"""
Streamlit UI components for TaskPilot.
"""

import streamlit as st

from src.models import Task


def render_task_card(task: Task) -> None:
    """
    Render an individual task.
    """

    priority_icons = {
        "High": "🔴",
        "Medium": "🟡",
        "Low": "🟢",
    }

    icon = priority_icons.get(task.priority, "⚪")

    with st.container(border=True):
        st.markdown(f"### {task.title}")

        st.write(task.description)

        st.markdown(
            f"**Assignee:** {task.assignee}  \n"
            f"**Role:** {task.role}  \n"
            f"**Priority:** {icon} {task.priority}  \n"
            f"**Estimated effort:** {task.estimated_hours:g} hours"
        )


def render_task_plan(tasks: list[Task]) -> None:
    """
    Render generated tasks in a list.
    """

    st.subheader("Generated Task Plan")

    if not tasks:
        st.info("No tasks have been generated yet.")
        return

    for task in tasks:
        render_task_card(task)


def render_task_board(tasks: list[Task]) -> None:
    """
    Render tasks as a simple Kanban-style board.
    """

    st.subheader("Task Board")

    columns = st.columns(3)

    statuses = [
        ("To Do", columns[0]),
        ("In Progress", columns[1]),
        ("Done", columns[2]),
    ]

    for status, column in statuses:
        with column:
            st.markdown(f"### {status}")

            status_tasks = [
                task
                for task in tasks
                if task.status == status
            ]

            if not status_tasks:
                st.caption("No tasks")

            for task in status_tasks:
                with st.container(border=True):
                    st.markdown(f"**{task.title}**")
                    st.caption(
                        f"{task.assignee} · "
                        f"{task.priority} · "
                        f"{task.estimated_hours:g}h"
                    )