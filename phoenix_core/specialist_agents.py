from __future__ import annotations

from typing import Any

from .agents import AgentManifest


def _brief(*, task: str = "", context: dict[str, Any] | None = None, **_: Any) -> dict[str, Any]:
    return {
        "status": "ready",
        "task": task,
        "context": context or {},
        "requires_external_model": True,
        "autonomous_action": False,
    }


def _financial(*, task: str = "", context: dict[str, Any] | None = None, **_: Any) -> dict[str, Any]:
    result = _brief(task=task, context=context)
    result["governance"] = "analysis_only; execution requires explicit human approval"
    return result


SPECIALIST_AGENTS = [
    (AgentManifest("marketing", "1.0.0", ("market_analysis", "campaign_strategy", "customer_acquisition"), "medium", "Marketing strategy and growth analysis."), _brief),
    (AgentManifest("brand_storyteller", "1.0.0", ("brand_positioning", "messaging", "storytelling"), "low", "Brand narrative, positioning and message architecture."), _brief),
    (AgentManifest("financial_analyst", "1.0.0", ("market_analysis", "financial_research", "risk_analysis", "backtesting"), "high", "Financial research, signals and risk analysis; never autonomous trading.", True), _financial),
    (AgentManifest("sports_coach", "1.0.0", ("training_plans", "performance_analysis", "goal_tracking"), "medium", "Sports training and performance planning."), _brief),
    (AgentManifest("mindfulness_guide", "1.0.0", ("meditation", "mindfulness", "habit_support"), "low", "Meditation and mindfulness guidance."), _brief),
    (AgentManifest("future_researcher", "1.0.0", ("trend_analysis", "scenario_planning", "foresight"), "medium", "Future trends, scenarios and opportunity research."), _brief),
    (AgentManifest("strategy_council", "1.0.0", ("strategic_analysis", "decision_support", "prioritization"), "high", "Cross-domain strategy synthesis and decision support.", True), _brief),
    (AgentManifest("systemization_specialist", "1.0.0", ("process_design", "automation", "operating_systems"), "medium", "Process architecture, standardization and automation."), _brief),
    (AgentManifest("growth_specialist", "1.0.0", ("growth_strategy", "funnel_design", "retention"), "medium", "Growth systems, customer journeys and retention."), _brief),
]


def default_agent_names() -> tuple[str, ...]:
    return tuple(manifest.name for manifest, _ in SPECIALIST_AGENTS)
