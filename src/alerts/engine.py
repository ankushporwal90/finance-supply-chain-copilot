"""Simple stock alert engine.

This starts as an in-session rule evaluator. Later it can persist rules in
SQLite and run on a schedule.
"""

from dataclasses import dataclass


@dataclass
class PriceAlert:
    """User-defined price threshold alert."""

    ticker: str
    direction: str
    threshold: float


def evaluate_price_alert(alert: PriceAlert, latest_price: float | None) -> bool:
    """Return True when the latest price crosses the configured threshold."""

    if latest_price is None:
        return False
    if alert.direction == "above":
        return latest_price >= alert.threshold
    if alert.direction == "below":
        return latest_price <= alert.threshold
    return False
