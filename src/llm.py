# src/llm.py

"""
Groq LLM configuration for TaskPilot AI.
"""

import os

from langchain_groq import ChatGroq


def get_groq_api_key() -> str:
    """
    Retrieve the Groq API key.

    Streamlit secrets are preferred when running the Streamlit app.
    Environment variables are supported for local development/testing.
    """

    # Try environment variable first.
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key

    # Try Streamlit secrets.
    try:
        import streamlit as st

        api_key = st.secrets.get("GROQ_API_KEY")

        if api_key:
            return api_key

    except Exception:
        pass

    raise ValueError(
        "GROQ_API_KEY was not found. "
        "Add GROQ_API_KEY to .streamlit/secrets.toml."
    )


def get_llm(
    model_name: str,
    temperature: float = 0.2,
) -> ChatGroq:
    """
    Create a LangChain ChatGroq model.
    """

    api_key = get_groq_api_key()

    return ChatGroq(
        model=model_name,
        temperature=temperature,
        groq_api_key=api_key,
    )