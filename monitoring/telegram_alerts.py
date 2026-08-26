import os
import requests


class TelegramAlerter:
    """Optional Telegram output adapter. Secrets are read only from environment variables."""

    def __init__(self, token: str | None = None, chat_id: str | None = None) -> None:
        self.token = token or os.getenv("PHOENIX_TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("PHOENIX_TELEGRAM_CHAT_ID")

    @property
    def configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def send(self, text: str) -> None:
        if not self.configured:
            raise RuntimeError("Telegram alerting is not configured")
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.post(url, json={"chat_id": self.chat_id, "text": text}, timeout=15)
        response.raise_for_status()
