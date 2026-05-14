"""Registry of AI-callable tools.

Beginner concept:
    Tool calling means the AI does not have to guess live facts. It can call a
    Python function such as get_stock_price or search_documents, then use the
    result to write a better grounded answer.
"""

from collections.abc import Callable

from src.finance.market_data import get_stock_snapshot


Tool = Callable[..., object]


def get_tool_registry() -> dict[str, Tool]:
    """Return the tools available to the copilot orchestration layer."""

    return {
        "get_stock_snapshot": get_stock_snapshot,
    }
