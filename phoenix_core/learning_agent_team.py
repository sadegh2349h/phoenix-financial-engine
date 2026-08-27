from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .agent_learning import AgentLearningContext
from .specialist_agents import SpecialistAgentTeam


@dataclass(frozen=True)
class TeamLearningResult:
    objective: str
    memories: list[dict[str, Any]]
    agents: list[dict[str, Any]]


class LearningAgentTeam:
    """Runs specialist agents with shared, bounded prior experience."""

    def __init__(self, team: SpecialistAgentTeam, learning: AgentLearningContext) -> None:
        self.team = team
        self.learning = learning

    def run(self, objective: str, task: dict[str, Any]) -> TeamLearningResult:
        context = self.learning.build(objective)
        enriched = {
            **task,
            "objective": objective,
            "memory": context.memories,
            "historical_average_score": context.average_score,
        }
        results = self.team.run_by_domain(enriched)
        agents = [
            {"agent": result.agent, "status": result.status, "result": result.output,
             "confidence": result.confidence}
            for result in results
        ]
        return TeamLearningResult(objective, context.memories, agents)
