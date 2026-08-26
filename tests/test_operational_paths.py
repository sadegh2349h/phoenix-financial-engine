from requests import RequestException
import os
import pytest

from phoenix_core.market_data import PublicMarketData
from alerting.telegram import TelegramNotifier


def test_coinbase_failover_path() -> None:
    client = PublicMarketData(timeout=15)

    def forced_binance_failure(symbol: str, interval: str, limit: int):
        raise RequestException("forced Binance failure for failover test")

    client._binance = forced_binance_failure  # type: ignore[method-assign]
    frame = client.klines("BTCUSDT", "1h", 20)
    assert not frame.empty
    assert {"timestamp", "open", "high", "low", "close", "volume"}.issubset(frame.columns)


def test_telegram_delivery_path() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        pytest.skip("Telegram secrets are not configured; delivery is tested only in the operational workflow")
    ok = TelegramNotifier(token=token, chat_id=chat_id).send(
        "PHOENIX TEST ALERT\nOperational test: Telegram delivery path is active."
    )
    assert ok is True
