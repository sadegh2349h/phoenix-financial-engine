import os
from typing import Optional
import requests


class TelegramNotifier:
    """Telegram transport. Credentials are read only from environment variables."""

    def __init__(self, token: Optional[str] = None, chat_id: Optional[str] = None) -> None:
        self.token = token or os.getenv("PHOENIX_TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("PHOENIX_TELEGRAM_CHAT_ID")

    @property
    def configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def send(self, message: str) -> bool:
        if not self.configured:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.post(url, json={"chat_id": self.chat_id, "text": message}, timeout=15)
        response.raise_for_status()
        return bool(response.json().get("ok"))
