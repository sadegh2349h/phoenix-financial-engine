from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class AgentMessage:
    sender: str
    recipient: str
    content: dict[str, Any]
    round: int


class AgentDialogue:
    """Multi-round specialist dialogue with an auditable message trail."""

    def __init__(self) -> None:
        self._agents: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}
        self.messages: list[AgentMessage] = []

    def register(self, name: str, handler: Callable[[dict[str, Any]], dict[str, Any]]) -> None:
        if name in self._agents:
            raise ValueError(f"agent already registered: {name}")
        self._agents[name] = handler

    def run(self, task: dict[str, Any], rounds: int = 2) -> list[AgentMessage]:
        if rounds < 1:
            raise ValueError("rounds must be positive")
        previous: dict[str, Any] = {}
        for current_round in range(1, rounds + 1):
            for name, handler in self._agents.items():
                context = {**task, "round": current_round, "previous": previous}
                output = handler(dict(context))
                self.messages.append(AgentMessage(name, "team", output, current_round))
                previous[name] = output
        return list(self.messages)

    def transcript(self) -> list[dict[str, Any]]:
        return [
            {"sender": m.sender, "recipient": m.recipient, "content": m.content, "round": m.round}
            for m in self.messages
        ]
