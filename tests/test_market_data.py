import pandas as pd

from src.finance.market_data import calculate_price_change, normalize_price_history


def test_calculate_price_change_returns_absolute_and_percent_change() -> None:
    daily_change, daily_change_percent = calculate_price_change(
        latest_price=110.0,
        previous_close=100.0,
    )

    assert daily_change == 10.0
    assert daily_change_percent == 10.0


def test_calculate_price_change_handles_missing_values() -> None:
    daily_change, daily_change_percent = calculate_price_change(
        latest_price=None,
        previous_close=100.0,
    )

    assert daily_change is None
    assert daily_change_percent is None


def test_normalize_price_history_flattens_tuple_columns() -> None:
    history = pd.DataFrame(
        {
            ("Close", "NVDA"): [100.0, 101.0],
            ("Volume", "NVDA"): [1_000_000, 1_200_000],
        }
    )

    normalized = normalize_price_history(history, ticker="NVDA")

    assert list(normalized.columns) == ["Close", "Volume"]
