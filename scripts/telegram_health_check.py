from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phoenix_core.telegram import TelegramNotifier

notifier = TelegramNotifier()
result = notifier.health_check()
if not result.ok:
    raise SystemExit(f"Telegram health check failed: {result.error}")

print(f"Telegram API healthy; status={result.status_code}")

if notifier.configured():
    sent = notifier.send("PHOENIX Telegram health check: OK")
    if not sent.ok:
        raise SystemExit(f"Telegram delivery failed: {sent.error}")
    print(f"Telegram delivery confirmed; status={sent.status_code}, message_id={sent.message_id}")
else:
    print("Telegram credentials are not configured; health-only check passed")
