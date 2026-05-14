from src.alerts.engine import PriceAlert, evaluate_price_alert


def test_price_alert_above_triggers() -> None:
    alert = PriceAlert(ticker="NVDA", direction="above", threshold=100.0)

    assert evaluate_price_alert(alert, latest_price=101.0) is True


def test_price_alert_below_triggers() -> None:
    alert = PriceAlert(ticker="NVDA", direction="below", threshold=100.0)

    assert evaluate_price_alert(alert, latest_price=99.0) is True
