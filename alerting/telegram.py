from __future__ import annotations
import os
import time
from typing import Optional
import requests

class TelegramNotifier:
    def __init__(self, token: Optional[str] = None, chat_id: Optional[str] = None, retries: int = 3) -> None:
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.retries = max(1, retries)

    def send(self, text: str) -> bool:
        if not self.token or not self.chat_id:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        for attempt in range(self.retries):
            try:
                response = requests.post(url, json={"chat_id": self.chat_id, "text": text}, timeout=15)
                response.raise_for_status()
                if response.json().get("ok"):
                    return True
            except requests.RequestException:
                if attempt + 1 < self.retries:
                    time.sleep(2 ** attempt)
        return False
