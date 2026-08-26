from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .agent_orchestrator import AgentOrchestrator, AgentTask
from .agent_performance import AgentPerformanceTracker
from .evaluation_loop import SelfEvaluationLoop


@dataclass(frozen=True)
class ExecutionResult:
    decision: dict[str, Any]
    evaluation: dict[str, Any] | None
    agent_performance: list[dict[str, Any]]


class PhoenixExecutionLoop:
    """Connects decision execution, observed outcomes, evaluation, and learning metrics."""

    def __init__(self, orchestrator: AgentOrchestrator, evaluator: SelfEvaluationLoop,
                 performance: AgentPerformanceTracker) -> None:
        self.orchestrator = orchestrator
        self.evaluator = evaluator
        self.performance = performance

    def run(self, task: AgentTask, outcome_provider: Callable[[dict[str, Any]], tuple[str, float, str]] | None = None) -> ExecutionResult:
        decision = self.orchestrator.execute(task)
        if decision.get("status") != "completed":
            return ExecutionResult(decision, None, [p.__dict__ for p in self.performance.report()])
        evaluation_data = None
        if outcome_provider is not None:
            outcome, score, lesson = outcome_provider(decision)
            decision_id = f"{task.objective}:{decision.get('agent', 'unknown')}"
            evaluation = self.evaluator.evaluate(decision_id, outcome, score, lesson)
            self.performance.record(decision.get("agent", "unknown"), decision_id, score, outcome)
            evaluation_data = evaluation.__dict__
        return ExecutionResult(decision, evaluation_data, [p.__dict__ for p in self.performance.report()])
