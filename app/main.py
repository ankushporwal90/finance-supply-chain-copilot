"""Streamlit entrypoint for the Finance & Supply Chain Copilot.

Run locally:
    streamlit run app/main.py
"""

import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.finance.market_data import get_price_history, get_stock_snapshot
from src.memory.session_state import initialize_session_state
from src.utils.config import load_yaml_config


def render_stock_dashboard(ticker: str) -> None:
    """Render the first finance dashboard slice."""

    snapshot = get_stock_snapshot(ticker)
    history = get_price_history(ticker)

    col1, col2, col3 = st.columns(3)
    col1.metric("Ticker", snapshot.ticker)
    col2.metric("Latest Price", f"{snapshot.price:.2f}" if snapshot.price else "Unavailable")
    col3.metric("Previous Close", f"{snapshot.previous_close:.2f}" if snapshot.previous_close else "Unavailable")

    if not history.empty:
        chart_data = history.reset_index()
        st.plotly_chart(
            px.line(chart_data, x=chart_data.columns[0], y="Close", title=f"{snapshot.ticker} Price History"),
            use_container_width=True,
        )
    else:
        st.info("No price history returned for this ticker.")


def main() -> None:
    """Render the application shell."""

    config = load_yaml_config()
    initialize_session_state()

    st.set_page_config(
        page_title=config.get("app", {}).get("name", "Finance & Supply Chain Copilot"),
        page_icon=config.get("ui", {}).get("page_icon", ":bar_chart:"),
        layout=config.get("ui", {}).get("layout", "wide"),
    )

    st.sidebar.title("Copilot")
    page = st.sidebar.radio(
        "Navigation",
        ["Finance Dashboard", "Document RAG", "Supply Chain Risk", "Alerts", "Architecture"],
    )
    ticker = st.sidebar.text_input("Stock ticker", value=st.session_state.selected_ticker)
    st.session_state.selected_ticker = ticker.upper().strip()

    st.title("Finance & Supply Chain Copilot")
    st.caption("A free, modular AI decision-support platform built with Streamlit, Groq, ChromaDB, and open-source embeddings.")

    if page == "Finance Dashboard":
        render_stock_dashboard(st.session_state.selected_ticker)
    elif page == "Document RAG":
        st.header("Document RAG")
        st.file_uploader("Upload annual reports or financial PDFs", type=["pdf"], accept_multiple_files=True)
        st.chat_input("Ask a grounded question about uploaded documents")
        st.info("PDF ingestion, citations, and grounded chat will be implemented in Phase 5 and Phase 6.")
    elif page == "Supply Chain Risk":
        st.header("Supply Chain Risk")
        st.info("This module will extract supplier, logistics, inventory, and operational risks from reports.")
    elif page == "Alerts":
        st.header("Alerts")
        st.info("This module will support price thresholds, percentage moves, volatility alerts, and sentiment alerts.")
    else:
        st.header("Architecture")
        st.markdown("Open `docs/ARCHITECTURE.md` for system diagrams and explanations.")


if __name__ == "__main__":
    main()
