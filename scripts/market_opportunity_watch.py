from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from financial_engine.multifactor import build_features, score_row
from phoenix_core.market_data import PublicMarketData
from phoenix_core.telegram import TelegramNotifier


def main() -> int:
    provider = PublicMarketData(timeout=15)
    frame = provider.klines("BTCUSDT", "15m", 250)
    if len(frame) < 120:
        raise SystemExit(f"insufficient BTC intraday history: {len(frame)} rows")

    features = build_features(frame)
    # Use only closed candles for the alert decision.
    latest = features.iloc[-2]
    previous = features.iloc[-3]
    latest_signal = score_row(latest)
    previous_signal = score_row(previous)

    if not (previous_signal.signal == 0 and latest_signal.signal == 1):
        print(
            f"No new BTC opportunity: previous={previous_signal.signal} "
            f"latest={latest_signal.signal} score={latest_signal.score} "
            f"regime={latest_signal.regime}"
        )
        return 0

    notifier = TelegramNotifier()
    if not notifier.configured() and not notifier.token:
        print("Telegram credentials are not configured; opportunity detected but not delivered")
        return 0

    price = float(latest["close"])
    reasons = ", ".join(latest_signal.reasons) or "multi-factor confirmation"
    text = (
        "PHOENIX — فرصت معاملاتی جدید BTC\n\n"
        f"قیمت: {price:,.2f} USD\n"
        f"امتیاز: {latest_signal.score:.2f}/1.00\n"
        f"رژیم بازار: {latest_signal.regime}\n"
        f"دلایل: {reasons}\n\n"
        "این پیام هشدار تحلیلی است، نه تضمین سود. قبل از تصمیم نهایی، مدیریت ریسک باید بررسی شود."
    )
    result = notifier.send(text)
    if not result.ok:
        raise SystemExit(f"Telegram opportunity delivery failed: {result.error}")

    print(f"Opportunity alert delivered; status={result.status_code}, message_id={result.message_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
