"""PHOENIX data-to-execution pipeline for opportunity and scenario engines.

The engines consume normalized observations and emit governed execution intents.
No external side effect is performed here; an execution adapter must explicitly
approve and execute the returned intent.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Protocol

from .opportunity_engine import OpportunityEngine, OpportunitySignal
from .scenario_engine import ForecastSignal, PredictionScenarioEngine


class DataProvider(Protocol):
    def load(self) -> dict[str, Any]: ...


class ExecutionAdapter(Protocol):
    def execute(self, intent: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True)
class PipelineResult:
    opportunities: dict[str, Any]
    scenarios: dict[str, Any]
    execution_intents: tuple[dict[str, Any], ...]
    decision_owner: str = "human"


class OpportunityScenarioPipeline:
    """Connect Data -> Intelligence -> governed Execution."""

    def __init__(self, data_provider: DataProvider, execution: ExecutionAdapter) -> None:
        self.data_provider = data_provider
        self.execution = execution
        self.opportunity_engine = OpportunityEngine()
        self.scenario_engine = PredictionScenarioEngine()

    def analyze(self) -> PipelineResult:
        payload = self.data_provider.load()
        opportunity_signals: Iterable[OpportunitySignal] = payload.get("opportunity_signals", ())
        forecast_signals: Iterable[ForecastSignal] = payload.get("forecast_signals", ())
        opportunities = self.opportunity_engine.run(opportunity_signals)
        scenarios = self.scenario_engine.run(forecast_signals)
        intents = tuple({
            "type": "human_approval_required",
            "action": item["action"],
            "title": item["title"],
            "source": item["source"],
            "score": item["score"],
        } for item in opportunities["opportunities"])
        return PipelineResult(opportunities, scenarios, intents)

    def execute_approved(self, intent: dict[str, Any], approved: bool) -> dict[str, Any]:
        if not approved:
            return {"status": "blocked", "reason": "human_approval_required", "intent": intent}
        return self.execution.execute(intent)
