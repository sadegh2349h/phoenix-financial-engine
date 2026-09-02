"""Evidence-ranked open-source architecture patterns for PHOENIX.

This module records adoption decisions without importing third-party projects.
It keeps the PHOENIX core provider-agnostic while making external research
machine-readable for routing, planning and future integration work.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OSSPattern:
    rank: int
    project: str
    capability: str
    phoenix_target: str
    adoption_mode: str
    human_approval_required: bool = True


OSS_PATTERNS: tuple[OSSPattern, ...] = (
    OSSPattern(1, "obra/superpowers", "disciplined skills, planning, TDD, review and verification", "skill governance and engineering quality gates", "adopt patterns"),
    OSSPattern(2, "langchain-ai/langchain", "composable LLM, tool, data and provider integrations", "integration fabric and model/tool composition", "selective architecture adoption"),
    OSSPattern(3, "TauricResearch/TradingAgents", "specialist financial analysis, debate, risk and decision logging", "Financial Engine research council and shadow evaluation", "selective domain-pattern adoption"),
    OSSPattern(4, "vllm-project/vllm", "high-throughput and memory-efficient model serving", "optional self-hosted inference tier", "infrastructure option"),
    OSSPattern(5, "FoundationAgents/MetaGPT", "role-based multi-agent collaboration and SOP-driven workflows", "specialist collaboration and governed handoffs", "architecture pattern"),
)


def oss_pattern_registry() -> list[dict[str, object]]:
    """Return the evidence-ranked external architecture registry."""
    return [
        {
            "rank": item.rank,
            "project": item.project,
            "capability": item.capability,
            "phoenix_target": item.phoenix_target,
            "adoption_mode": item.adoption_mode,
            "human_approval_required": item.human_approval_required,
        }
        for item in OSS_PATTERNS
    ]


def recommended_patterns(*, domain: str | None = None) -> list[dict[str, object]]:
    """Filter recommendations by a simple PHOENIX target/domain keyword."""
    if not domain:
        return oss_pattern_registry()
    needle = domain.lower().strip()
    return [
        item for item in oss_pattern_registry()
        if needle in str(item["capability"]).lower()
        or needle in str(item["phoenix_target"]).lower()
        or needle in str(item["project"]).lower()
    ]
