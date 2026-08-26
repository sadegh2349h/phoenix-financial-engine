from __future__ import annotations

import os
from typing import Any

import requests

from .intelligence import IntelligenceRequest, IntelligenceResponse


class OpenAICompatibleProvider:
    """Secure OpenAI-compatible provider; credentials remain in environment secrets."""

    name = "openai-compatible"

    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("PHOENIX_LLM_API_KEY")
        self.base_url = (base_url or os.getenv("PHOENIX_LLM_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.model = model or os.getenv("PHOENIX_LLM_MODEL", "gpt-4.1-mini")

    def generate(self, request: IntelligenceRequest) -> IntelligenceResponse:
        if not self.api_key:
            raise RuntimeError("PHOENIX_LLM_API_KEY is not configured")
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a PHOENIX specialist. Analyze only; never execute external actions."},
                {"role": "user", "content": f"Agent: {request.agent}\nObjective: {request.objective}\nContext: {request.context}"},
            ],
            "temperature": 0.2,
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        answer = data["choices"][0]["message"]["content"]
        return IntelligenceResponse("ready", request.agent, answer, 0.5, True, self.name)
