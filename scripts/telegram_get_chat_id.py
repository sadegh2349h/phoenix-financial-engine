from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import requests


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not configured")
    response = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=15)
    data = response.json()
    if not response.ok or not data.get("ok"):
        raise SystemExit(str(data.get("description") or "Telegram getUpdates failed"))
    updates = data.get("result") or []
    chats = {}
    for update in updates:
        message = update.get("message") or update.get("edited_message") or update.get("channel_post") or {}
        chat = message.get("chat") or {}
        if chat.get("id") is not None:
            chats[str(chat["id"])] = {
                "id": chat["id"],
                "type": chat.get("type"),
                "title": chat.get("title") or chat.get("first_name") or "",
                "username": chat.get("username") or "",
            }
    if not chats:
        raise SystemExit("No chat found. Send a message to the bot first, then rerun this workflow.")
    for chat in chats.values():
        print(f"CHAT_ID={chat['id']} TYPE={chat['type']} TITLE={chat['title']} USERNAME={chat['username']}")


if __name__ == "__main__":
    main()
