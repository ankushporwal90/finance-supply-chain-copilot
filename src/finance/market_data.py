"""Free stock-market data access using yfinance."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
    daily_change: float | None = None
    daily_change_percent: float | None = None


@dataclass
class CompanyProfile:
    """Business-friendly company metadata for the dashboard."""

    ticker: str
    name: str | None
    sector: str | None
    industry: str | None
    market_cap: float | None
    website: str | None
    summary: str | None
    fifty_two_week_high: float | None
    fifty_two_week_low: float | None


def get_stock_snapshot(ticker: str) -> StockSnapshot:
    """Fetch the latest stock price snapshot for a ticker."""

    ticker = clean_ticker(ticker)
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

    daily_change, daily_change_percent = calculate_price_change(
        latest_price=float(fast_price) if fast_price else latest_close,
        previous_close=float(fast_previous_close) if fast_previous_close else previous_close,
    )

    return StockSnapshot(
        ticker=ticker,
        price=float(fast_price) if fast_price else latest_close,
        previous_close=float(fast_previous_close) if fast_previous_close else previous_close,
        currency=safe_fast_info_get(info, "currency"),
        daily_change=daily_change,
        daily_change_percent=daily_change_percent,
    )


def get_company_profile(ticker: str) -> CompanyProfile:
    """Fetch company profile fields for dashboard context.

    yfinance's detailed metadata can be incomplete or occasionally unavailable,
    so every field is optional. The UI decides how to present missing data.
    """

    ticker = clean_ticker(ticker)
    stock = yf.Ticker(ticker)
    info = get_ticker_info(stock)
    fast_info = stock.fast_info

    return CompanyProfile(
        ticker=ticker,
        name=get_first_present(info, ["longName", "shortName"]),
        sector=info.get("sector"),
        industry=info.get("industry"),
        market_cap=to_float(info.get("marketCap") or safe_fast_info_get(fast_info, "market_cap")),
        website=info.get("website"),
        summary=info.get("longBusinessSummary"),
        fifty_two_week_high=to_float(
            info.get("fiftyTwoWeekHigh") or safe_fast_info_get(fast_info, "year_high")
        ),
        fifty_two_week_low=to_float(
            info.get("fiftyTwoWeekLow") or safe_fast_info_get(fast_info, "year_low")
        ),
    )


def get_price_history(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Fetch historical prices for charts and alert calculations."""

    ticker = clean_ticker(ticker)
    history = yf.download(
        ticker,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=False,
    )
    return normalize_price_history(history, ticker)


def calculate_price_change(
    latest_price: float | None,
    previous_close: float | None,
) -> tuple[float | None, float | None]:
    """Calculate absolute and percentage change from previous close."""

    if latest_price is None or previous_close in (None, 0):
        return None, None

    daily_change = latest_price - previous_close
    daily_change_percent = (daily_change / previous_close) * 100
    return daily_change, daily_change_percent


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


def safe_dict(value: object) -> dict[str, Any]:
    """Return a dictionary or an empty fallback when metadata retrieval fails."""

    try:
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def get_ticker_info(stock: yf.Ticker) -> dict[str, Any]:
    """Fetch yfinance company metadata with a safe empty fallback."""

    try:
        return safe_dict(stock.info)
    except Exception:
        return {}


def get_first_present(data: dict[str, Any], keys: list[str]) -> str | None:
    """Return the first non-empty text value from a metadata dictionary."""

    for key in keys:
        value = data.get(key)
        if value:
            return str(value)
    return None


def to_float(value: object) -> float | None:
    """Convert numeric-looking values to float without raising UI errors."""

    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_ticker(ticker: str) -> str:
    """Normalize user-entered ticker symbols."""

    return ticker.upper().strip()
