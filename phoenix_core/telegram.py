from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class TelegramResult:
    ok: bool
    status_code: int | None
    message_id: int | None
    error: str | None = None


class TelegramNotifier:
    """Reliable Telegram delivery with bounded retries and no secret logging."""

    def __init__(self, token: str | None = None, chat_id: str | None = None,
                 timeout: float = 10.0, retries: int = 3, backoff: float = 1.0) -> None:
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.timeout = timeout
        self.retries = max(1, retries)
        self.backoff = max(0.0, backoff)

    def configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def _request(self, method: str, payload: dict[str, Any] | None = None) -> TelegramResult:
        if not self.configured():
            return TelegramResult(False, None, None, "telegram_not_configured")
        url = f"https://api.telegram.org/bot{self.token}/{method}"
        last_error = None
        status = None
        for attempt in range(self.retries):
            try:
                response = requests.post(url, json=payload or {}, timeout=self.timeout)
                status = response.status_code
                data = response.json()
                if response.ok and data.get("ok"):
                    result = data.get("result") or {}
                    return TelegramResult(True, status, result.get("message_id"))
                last_error = str(data.get("description") or f"http_{status}")
            except (requests.RequestException, ValueError) as exc:
                last_error = type(exc).__name__
            if attempt + 1 < self.retries:
                time.sleep(self.backoff * (2 ** attempt))
        return TelegramResult(False, status, None, last_error or "telegram_delivery_failed")

    def health_check(self) -> TelegramResult:
        return self._request("getMe")

    def send(self, text: str) -> TelegramResult:
        if not text.strip():
            return TelegramResult(False, None, None, "empty_message")
        return self._request("sendMessage", {"chat_id": self.chat_id, "text": text})
