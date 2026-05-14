"""Streamlit session-state helpers.

Beginner concept:
    Streamlit reruns the script whenever a user interacts with the page. The
    session_state object is how we remember the selected company, uploaded
    documents, chat history, and active alerts across those reruns.
"""

from typing import Any

import streamlit as st


DEFAULT_SESSION_STATE: dict[str, Any] = {
    "selected_ticker": "NVDA",
    "messages": [],
    "uploaded_documents": [],
    "alerts": [],
    "last_finance_snapshot": None,
}


def initialize_session_state() -> None:
    """Create default state keys if this is a new Streamlit session."""

    for key, value in DEFAULT_SESSION_STATE.items():
        st.session_state.setdefault(key, value.copy() if isinstance(value, list) else value)
