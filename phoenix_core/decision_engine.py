from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Decision:
    status: str
    recommendation: str
    confidence: float
    rationale: tuple[str, ...]
    requires_human_approval: bool


class DecisionEngine:
    """Conservative synthesis layer; it never executes external actions."""

    def evaluate(self, *, agent_results: list[dict[str, Any]], risk_level: str = "low") -> Decision:
        if not agent_results:
            return Decision("insufficient_data", "no_decision", 0.0, ("no agent results",), True)
        successful = [r for r in agent_results if r.get("status") in {"ready", "completed"}]
        if not successful:
            return Decision("insufficient_data", "no_decision", 0.0, ("no successful agent results",), True)
        confidence = min(0.95, max(0.0, len(successful) / max(1, len(agent_results))))
        approval = risk_level in {"high", "critical"} or any(r.get("requires_human_review", False) for r in successful)
        return Decision("ready", "review_recommendation", confidence,
                        (f"successful_agents={len(successful)}", f"risk_level={risk_level}"), approval)
