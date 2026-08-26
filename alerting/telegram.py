from __future__ import annotations
import os
from typing import Optional
import requests

class TelegramNotifier:
    def __init__(self, token: Optional[str]=None, chat_id: Optional[str]=None)->None:
        self.token=token or os.getenv("TELEGRAM_BOT_TOKEN"); self.chat_id=chat_id or os.getenv("TELEGRAM_CHAT_ID")
    def send(self,text:str)->bool:
        if not self.token or not self.chat_id: return False
        r=requests.post(f"https://api.telegram.org/bot{self.token}/sendMessage",json={"chat_id":self.chat_id,"text":text},timeout=15); r.raise_for_status(); return bool(r.json().get("ok"))
