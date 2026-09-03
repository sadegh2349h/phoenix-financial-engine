"""Bridge opportunity detection with scenario analysis."""
from __future__ import annotations
from .opportunity_engine import OpportunityEngine, OpportunitySignal
from .scenario_engine import PredictionScenarioEngine, ForecastSignal

class OpportunityScenarioBridge:
    def __init__(self) -> None:
        self.opportunities = OpportunityEngine()
        self.scenarios = PredictionScenarioEngine()

    def run(self, opportunity_signals, forecast_signals):
        return {"opportunities": self.opportunities.run(opportunity_signals), "scenarios": self.scenarios.run(forecast_signals)}
