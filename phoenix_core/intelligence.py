from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class IntelligenceRequest:
    objective: str
    context: dict[str, Any]
    agent: str


@dataclass(frozen=True)
class IntelligenceResponse:
    status: str
    agent: str
    answer: str
    confidence: float
    requires_human_review: bool
    provider: str


class IntelligenceProvider(Protocol):
    name: str

    def generate(self, request: IntelligenceRequest) -> IntelligenceResponse: ...


class RuleBasedProvider:
    name = "rule-based"

    def generate(self, request: IntelligenceRequest) -> IntelligenceResponse:
        return IntelligenceResponse("ready", request.agent, f"Task received: {request.objective}", 0.0, True, self.name)


class IntelligenceLayer:
    """Provider-agnostic intelligence gateway with a safe local fallback."""

    def __init__(self, provider: IntelligenceProvider | None = None) -> None:
        self.provider = provider or RuleBasedProvider()

    def analyze(self, request: IntelligenceRequest) -> IntelligenceResponse:
        return self.provider.generate(request)
