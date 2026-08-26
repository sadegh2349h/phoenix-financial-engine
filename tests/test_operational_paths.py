import os

from requests import RequestException

from phoenix_core.market_data import PublicMarketData
from phoenix_core.telegram import TelegramNotifier, TelegramResult


def test_coinbase_failover_path(monkeypatch) -> None:
    client = PublicMarketData(timeout=2)

    def forced_binance_failure(symbol: str, interval: str, limit: int):
        raise RequestException("forced Binance failure for failover test")

    def fake_coinbase(symbol: str, interval: str, limit: int):
        return client._frame([
            [i * 3600000, 100 + i, 101 + i, 99 + i, 100.5 + i, 10 + i]
            for i in range(limit)
        ])

    monkeypatch.setattr(client, "_binance", forced_binance_failure)
    monkeypatch.setattr(client, "_coinbase", fake_coinbase)
    frame = client.klines("BTCUSDT", "1h", 60)
    assert client.last_provider == "coinbase"
    assert len(frame) == 60
    assert not frame.empty


def test_telegram_delivery_path_is_network_independent(monkeypatch) -> None:
    class FakeResponse:
        ok = True
        status_code = 200

        def json(self):
            return {"ok": True, "result": {"message_id": 12345}}

    def fake_post(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("phoenix_core.telegram.requests.post", fake_post)
    notifier = TelegramNotifier(token="test-token", chat_id="test-chat", retries=1)
    result = notifier.send("PHOENIX TEST ALERT")
    assert result.ok is True
    assert result.status_code == 200
    assert result.message_id == 12345


def test_telegram_real_delivery_is_optional() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    assert (token is None) == (chat_id is None) or (token is not None and chat_id is not None)
