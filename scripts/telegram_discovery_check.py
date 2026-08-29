from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phoenix_core.telegram import TelegramNotifier

notifier = TelegramNotifier()
health = notifier.health_check()
if not health.ok:
    raise SystemExit(f"Telegram API unhealthy: {health.error}")

chat_id = notifier.discover_chat_id()
if not chat_id:
    raise SystemExit("Telegram API is healthy, but no recent chat update was found")

print(f"Telegram chat discovered successfully: {chat_id}")
