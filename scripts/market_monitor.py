import os
import requests


def send_telegram(message: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram credentials are not configured; monitor remains analysis-only.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=15)
    response.raise_for_status()


def main() -> None:
    # Provider/strategy execution is intentionally injected later.
    # This keeps the monitoring transport independent from financial logic.
    send_telegram("PHOENIX monitor heartbeat: monitoring workflow executed.")


if __name__ == "__main__":
    main()
