"""Free stock-market data access using yfinance."""

from dataclasses import dataclass

import pandas as pd
import yfinance as yf


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
    return StockSnapshot(
        ticker=ticker.upper(),
        price=float(info.get("last_price")) if info.get("last_price") else None,
        previous_close=float(info.get("previous_close")) if info.get("previous_close") else None,
        currency=info.get("currency"),
    )


def get_price_history(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Fetch historical prices for charts and alert calculations."""

    return yf.download(ticker, period=period, interval=interval, progress=False)
