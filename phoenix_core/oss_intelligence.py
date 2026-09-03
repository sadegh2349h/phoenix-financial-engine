"""Evidence-ranked open-source architecture patterns for PHOENIX.

The registry is informed by external OSS ecosystems but contains no copied
third-party source. Adoption is separated from discovery and scored before
integration.
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
    return [
        {"rank": item.rank, "project": item.project, "capability": item.capability,
         "phoenix_target": item.phoenix_target, "adoption_mode": item.adoption_mode,
         "human_approval_required": item.human_approval_required}
        for item in OSS_PATTERNS
    ]


def recommended_patterns(*, domain: str | None = None) -> list[dict[str, object]]:
    if not domain:
        return oss_pattern_registry()
    needle = domain.lower().strip()
    return [item for item in oss_pattern_registry()
            if needle in str(item["capability"]).lower()
            or needle in str(item["phoenix_target"]).lower()
            or needle in str(item["project"]).lower()]


def adoption_score(*, fit: float, security: float, maintenance: float,
                   integration_cost: float, license_ok: bool = True) -> dict[str, object]:
    values = (fit, security, maintenance, integration_cost)
    if any(value < 0 or value > 1 for value in values):
        raise ValueError("all scores must be between 0 and 1")
    score = round((0.40 * fit + 0.25 * security + 0.20 * maintenance
                   + 0.15 * (1 - integration_cost)), 4)
    decision = "adopt" if license_ok and score >= 0.75 else "evaluate"
    return {"score": score, "decision": decision,
            "license_ok": license_ok, "human_approval_required": True}
