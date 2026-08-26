from __future__ import annotations

import os
import time
from datetime import datetime, timezone

from .multi_source_analysis import cross_source_consensus
from alerting.telegram import TelegramNotifier


def run_forever(symbol: str = "BTCUSDT", interval: str = "1h", poll_seconds: int = 300) -> None:
    """Long-running PHOENIX monitor for a VM/container; independent of GitHub Actions."""
    token, chat_id = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    notifier = TelegramNotifier(token, chat_id) if token and chat_id else None
    while True:
        started = datetime.now(timezone.utc).isoformat()
        try:
            result = cross_source_consensus(symbol, interval)
            if result.sources:
                message = (f"PHOENIX | {symbol} | {result.direction}\n"
                           f"Confidence: {result.confidence:.2%}\n"
                           f"Source agreement: {result.agreement:.0%}\n"
                           f"Sources: {result.sources}\nUTC: {started}")
                if notifier and result.confidence >= 0.60:
                    notifier.send(message)
        except Exception as exc:
            if notifier:
                notifier.send(f"PHOENIX MONITOR ERROR\n{type(exc).__name__}: {exc}")
        time.sleep(max(30, int(poll_seconds)))


if __name__ == "__main__":
    run_forever()
