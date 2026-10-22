# app.py

import streamlit as st

from src.config import (
    APP_ICON,
    APP_TITLE,
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
)
from src.llm import get_llm
from src.task_agent import generate_task_plan
from src.task_manager import (
    add_tasks,
    clear_tasks,
    get_tasks,
    initialize_task_state,
)
from src.team import get_team_members
from src.ui import render_task_board, render_task_plan


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
)


# ---------------------------------------------------------------------------
# Initialize application state
# ---------------------------------------------------------------------------

initialize_task_state()

team_members = get_team_members()


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🤖 TaskPilot AI")

st.write(
    "Describe a project in natural language and let AI break it "
    "into actionable tasks, assign them to the right team members, "
    "and estimate their priority and effort."
)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:

    st.header("Configuration")

    model_name = st.selectbox(
        "Groq Model",
        options=list(AVAILABLE_MODELS.keys()),
        index=list(AVAILABLE_MODELS.values()).index(
            DEFAULT_MODEL
        ),
    )

    selected_model = AVAILABLE_MODELS[model_name]

    st.caption(
        f"Model ID: `{selected_model}`"
    )

    st.divider()

    st.subheader("Team")

    for member in team_members:

        st.write(
            f"**{member.name}**  \n"
            f"{member.role}"
        )

    st.divider()

    st.button(
        "Clear All Tasks",
        width="stretch",
        on_click=clear_tasks,
    )


# ---------------------------------------------------------------------------
# Task creation
# ---------------------------------------------------------------------------

st.subheader("Create Tasks")

user_request = st.text_area(
    "Describe what needs to be done",
    placeholder=(
        "Example: Build an e-commerce website with "
        "product listing, shopping cart, payment integration "
        "and an admin dashboard."
    ),
    height=150,
)


if st.button(
    "✨ Generate Task Plan",
    type="primary",
    width="stretch",
):

    if not user_request.strip():

        st.warning(
            "Please describe the project first."
        )

    else:

        with st.spinner(
            "AI is analyzing the project and creating tasks..."
        ):

            try:

                llm = get_llm(
                    model_name=selected_model,
                    temperature=0.2,
                )

                task_plan = generate_task_plan(
                    user_request=user_request,
                    team_members=team_members,
                    llm=llm,
                )

                add_tasks(task_plan.tasks)

                st.success(
                    f"Generated "
                    f"{len(task_plan.tasks)} tasks successfully."
                )

            except Exception as exc:

                st.error(
                    "Something went wrong while "
                    "generating the task plan."
                )

                st.exception(exc)


# ---------------------------------------------------------------------------
# Current tasks
# ---------------------------------------------------------------------------

tasks = get_tasks()


if tasks:

    st.divider()

    # ---------------------------------------------------------------
    # Project statistics
    # ---------------------------------------------------------------

    total_tasks = len(tasks)

    todo_tasks = sum(
        task.status == "To Do"
        for task in tasks
    )

    in_progress_tasks = sum(
        task.status == "In Progress"
        for task in tasks
    )

    completed_tasks = sum(
        task.status == "Done"
        for task in tasks
    )

    total_hours = sum(
        task.estimated_hours
        for task in tasks
    )

    st.subheader("Project Overview")

    metric_columns = st.columns(4)

    with metric_columns[0]:
        st.metric(
            "Total Tasks",
            total_tasks,
        )

    with metric_columns[1]:
        st.metric(
            "To Do",
            todo_tasks,
        )

    with metric_columns[2]:
        st.metric(
            "In Progress",
            in_progress_tasks,
        )

    with metric_columns[3]:
        st.metric(
            "Completed",
            completed_tasks,
        )

    st.caption(
        f"Estimated total effort: "
        f"{total_hours:g} hours"
    )

    st.divider()

    # ---------------------------------------------------------------
    # Generated task list
    # ---------------------------------------------------------------

    render_task_plan(tasks)

    st.divider()

    # ---------------------------------------------------------------
    # Interactive task board
    # ---------------------------------------------------------------

    render_task_board(tasks)

else:

    st.info(
        "No tasks yet. Describe a project above and click "
        "**Generate Task Plan**."
    )