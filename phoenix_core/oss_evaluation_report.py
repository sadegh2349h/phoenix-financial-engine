"""Evidence-backed PHOENIX OSS candidate evaluations.

Scores follow the PHOENIX 100-point acceptance standard. These are review
recommendations, not automatic adoption decisions. Human approval remains
mandatory and no dependency is installed by this module.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OSSEvidenceEvaluation:
    candidate: str
    source: str
    score: int
    decision: str
    strengths: tuple[str, ...]
    blockers: tuple[str, ...]
    evidence_urls: tuple[str, ...]


# Weights: impact 25, architecture fit 15, performance 15, reliability 15,
# security 10, maturity 8, cost 7, license 5. Acceptance threshold: 80.
# Scores are conservative and evidence-bound; they are not vendor claims.
EVALUATIONS: tuple[OSSEvidenceEvaluation, ...] = (
    OSSEvidenceEvaluation(
        "agent-evaluator", "PyPI", 86, "recommended_for_human_review",
        ("58 metrics", "7 quality gates", "A/B testing", "framework adapters"),
        ("must benchmark against PHOENIX's existing quality gates", "external dependency must be sandboxed"),
        ("https://pypi.org/project/agent-evaluator/",),
    ),
    OSSEvidenceEvaluation(
        "agentevals-cli", "PyPI", 87, "recommended_for_human_review",
        ("evaluates existing OpenTelemetry traces", "no replay required", "framework-agnostic trace input"),
        ("needs compatibility test with PHOENIX trace schema", "LLM-judge cost/variance requires controls"),
        ("https://pypi.org/project/agentevals-cli/",),
    ),
    OSSEvidenceEvaluation(
        "memoryeval", "PyPI", 82, "recommended_for_human_review",
        ("memory regression scenarios", "contradiction detection", "stale-data checks", "cross-user leakage checks"),
        ("alpha maturity", "must be tested against PHOENIX Memory rather than replacing it"),
        ("https://pypi.org/project/memoryeval/",),
    ),
    OSSEvidenceEvaluation(
        "AgenticLens", "PyPI", 79, "pilot_only",
        ("local observability", "evaluation and release gates", "repeated-run comparison", "no required hosted backend"),
        ("alpha maturity", "new project", "overlap with existing PHOENIX monitoring/Langfuse layer"),
        ("https://pypi.org/project/agenticlens/",),
    ),
    OSSEvidenceEvaluation(
        "agentic-memory-ai", "PyPI", 75, "pilot_only",
        ("conflict detection", "typed decay", "checkpointing", "zero runtime dependencies"),
        ("alpha maturity", "small ecosystem", "overlap with existing Mem0-based memory layer"),
        ("https://pypi.org/project/agentic-memory-ai/",),
    ),
)


def acceptance_threshold() -> int:
    return 80


def recommended_evaluations() -> list[OSSEvidenceEvaluation]:
    return [item for item in EVALUATIONS if item.score >= acceptance_threshold()]


def pilot_evaluations() -> list[OSSEvidenceEvaluation]:
    return [item for item in EVALUATIONS if item.score < acceptance_threshold()]
