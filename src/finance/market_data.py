"""Free stock-market data access using yfinance."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
YFINANCE_CACHE_DIR = PROJECT_ROOT / "data" / "yfinance_cache"
YFINANCE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
yf.set_tz_cache_location(str(YFINANCE_CACHE_DIR))


@dataclass
class StockSnapshot:
    """Simple business-friendly stock summary used by the dashboard."""

    ticker: str
    price: float | None
    previous_close: float | None
    currency: str | None


def get_stock_snapshot(ticker: str) -> StockSnapshot:
    """Fetch the latest stock price snapshot for a ticker."""

    stock = yf.Ticker(ticker)
    info = stock.fast_info
    history = get_price_history(ticker, period="5d", interval="1d")

    latest_close = None
    previous_close = None
    if not history.empty and "Close" in history.columns:
        close_prices = history["Close"].dropna()
        if not close_prices.empty:
            latest_close = float(close_prices.iloc[-1])
        if len(close_prices) > 1:
            previous_close = float(close_prices.iloc[-2])

    fast_price = safe_fast_info_get(info, "last_price")
    fast_previous_close = safe_fast_info_get(info, "previous_close")

    return StockSnapshot(
        ticker=ticker.upper(),
        price=float(fast_price) if fast_price else latest_close,
        previous_close=float(fast_previous_close) if fast_previous_close else previous_close,
        currency=safe_fast_info_get(info, "currency"),
    )


def get_price_history(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Fetch historical prices for charts and alert calculations."""

    history = yf.download(
        ticker,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=False,
    )
    return normalize_price_history(history, ticker)


def normalize_price_history(history: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Return yfinance history with simple column names.

    yfinance may return columns like ("Close", "NVDA") when it treats a ticker
    as part of a multi-ticker download. Plotly and beginner-friendly app code
    are easier to work with when the columns are simply Close, Open, Volume,
    and so on.
    """

    if isinstance(history.columns, pd.MultiIndex):
        ticker = ticker.upper()
        if ticker in history.columns.get_level_values(-1):
            history = history.xs(ticker, axis=1, level=-1)
        else:
            history.columns = history.columns.get_level_values(0)
    elif all(isinstance(column, tuple) for column in history.columns):
        history.columns = [column[0] for column in history.columns]

    history.columns = [str(column).title() for column in history.columns]
    return history


def safe_fast_info_get(info: object, key: str) -> object | None:
    """Read yfinance fast_info fields without letting missing metadata crash UI."""

    try:
        return info.get(key)
    except (KeyError, TypeError, AttributeError):
        return None
