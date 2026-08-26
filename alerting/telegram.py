from __future__ import annotations
import os
from typing import Optional
import requests


class TelegramNotifier:
    """Minimal Telegram Bot API adapter. Credentials are read only from environment secrets."""

    def __init__(self, token: Optional[str] = None, chat_id: Optional[str] = None) -> None:
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    def send(self, text: str) -> bool:
        if not self.token or not self.chat_id:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.post(url, json={"chat_id": self.chat_id, "text": text}, timeout=15)
        response.raise_for_status()
        return bool(response.json().get("ok"))
