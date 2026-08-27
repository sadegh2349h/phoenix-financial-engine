from __future__ import annotations

from pathlib import Path
from phoenix_core.telegram import TelegramNotifier

report = Path("phoenix_performance_report.md")
if not report.exists():
    raise SystemExit("performance report was not generated")

notifier = TelegramNotifier()
if not notifier.configured():
    raise SystemExit("Telegram credentials are not configured")

text = report.read_text(encoding="utf-8").strip()
message = "🦅 PHOENIX — گزارش عملکرد\n\n" + text
result = notifier.send(message)
if not result.ok:
    raise SystemExit(f"Telegram delivery failed: {result.error}")

print(f"PHOENIX performance report delivered to Telegram; message_id={result.message_id}")
