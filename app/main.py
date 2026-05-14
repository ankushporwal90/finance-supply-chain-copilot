"""Streamlit entrypoint for the Finance & Supply Chain Copilot.

Run locally:
    streamlit run app/main.py
"""

import sys
from pathlib import Path

import plotly.express as px
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.finance.market_data import get_company_profile, get_price_history, get_stock_snapshot
from src.memory.session_state import initialize_session_state
from src.utils.config import load_yaml_config


def render_stock_dashboard(ticker: str) -> None:
    """Render the finance dashboard experience."""

    if not ticker:
        st.warning("Enter a stock ticker in the sidebar to load the dashboard.")
        return

    period = st.segmented_control(
        "Time range",
        options=["1mo", "3mo", "6mo", "1y", "5y"],
        default="6mo",
    )

    with st.spinner(f"Loading {ticker.upper()} market data..."):
        snapshot = get_stock_snapshot(ticker)
        profile = get_company_profile(ticker)
        history = get_price_history(ticker, period=period or "6mo")

    if history.empty and snapshot.price is None:
        st.error(
            "No market data was returned for this ticker. Check the symbol or try again in a moment."
        )
        return

    st.subheader(profile.name or snapshot.ticker)
    st.caption(build_company_caption(profile.sector, profile.industry, snapshot.currency))

    kpi_cols = st.columns(5)
    kpi_cols[0].metric("Ticker", snapshot.ticker)
    kpi_cols[1].metric("Latest Price", format_currency(snapshot.price, snapshot.currency))
    kpi_cols[2].metric(
        "Daily Change",
        format_currency(snapshot.daily_change, snapshot.currency),
        delta=format_percent(snapshot.daily_change_percent),
    )
    kpi_cols[3].metric("Previous Close", format_currency(snapshot.previous_close, snapshot.currency))
    kpi_cols[4].metric("Market Cap", format_large_number(profile.market_cap))

    chart_col, context_col = st.columns([2, 1])
    with chart_col:
        render_price_chart(history, snapshot.ticker)

    with context_col:
        st.markdown("#### Company Snapshot")
        st.write(f"**52-week high:** {format_currency(profile.fifty_two_week_high, snapshot.currency)}")
        st.write(f"**52-week low:** {format_currency(profile.fifty_two_week_low, snapshot.currency)}")
        if profile.website:
            st.link_button("Company Website", profile.website)

        st.markdown("#### AI Investment Insight")
        st.info(
            "Next phase: Groq will summarize price movement, valuation context, report risks, "
            "and supply chain signals into a grounded business insight."
        )

    if profile.summary:
        with st.expander("Business Description"):
            st.write(profile.summary)


def render_price_chart(history: pd.DataFrame, ticker: str) -> None:
    """Render a close-price chart with volume context."""

    if history.empty or "Close" not in history.columns:
        st.info("No price history returned for the selected period.")
        return

    chart_data = history.reset_index()
    date_column = chart_data.columns[0]
    figure = px.line(
        chart_data,
        x=date_column,
        y="Close",
        title=f"{ticker} Closing Price",
        labels={"Close": "Close Price", str(date_column): "Date"},
    )
    figure.update_traces(line_width=2.5)
    figure.update_layout(
        hovermode="x unified",
        margin={"l": 0, "r": 0, "t": 48, "b": 0},
    )
    st.plotly_chart(figure, use_container_width=True)

    if "Volume" in history.columns:
        latest_volume = history["Volume"].dropna().iloc[-1] if not history["Volume"].dropna().empty else None
        st.caption(f"Latest reported volume: {format_large_number(float(latest_volume) if latest_volume else None)}")


def build_company_caption(sector: str | None, industry: str | None, currency: str | None) -> str:
    """Create a compact business context line for the selected company."""

    parts = [part for part in [sector, industry, currency] if part]
    return " | ".join(parts) if parts else "Company metadata unavailable from yfinance."


def format_currency(value: float | None, currency: str | None = "USD") -> str:
    """Format currency values while handling missing data."""

    if value is None:
        return "Unavailable"
    prefix = "$" if currency in (None, "USD") else f"{currency} "
    return f"{prefix}{value:,.2f}"


def format_percent(value: float | None) -> str | None:
    """Format a percentage delta for Streamlit metric cards."""

    if value is None:
        return None
    return f"{value:+.2f}%"


def format_large_number(value: float | None) -> str:
    """Format market cap and volume in readable business units."""

    if value is None:
        return "Unavailable"
    units = [
        (1_000_000_000_000, "T"),
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "K"),
    ]
    for divisor, suffix in units:
        if abs(value) >= divisor:
            return f"{value / divisor:,.2f}{suffix}"
    return f"{value:,.0f}"


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
    st.caption(
        "A free, modular AI decision-support platform built with Streamlit, Groq, "
        "ChromaDB, and open-source embeddings."
    )

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
