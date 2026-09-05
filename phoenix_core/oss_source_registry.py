"""PHOENIX multi-source open-source intelligence registry.

The registry deliberately goes beyond GitHub. It describes trusted discovery
surfaces that PHOENIX can scan before a candidate reaches technical evaluation.
No source is treated as authoritative by itself; candidates require evidence,
compatibility, security and measurable PHOENIX value before adoption.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class OSSSource:
    name: str
    category: str
    url: str
    strengths: tuple[str, ...]
    trust_notes: str
    priority: int


@dataclass(frozen=True)
class OSSCandidate:
    name: str
    source: str
    capability: str
    target_layer: str
    evidence_url: str
    status: str = "discovered"


SOURCE_REGISTRY: tuple[OSSSource, ...] = (
    OSSSource(
        "Hugging Face", "models_datasets_agents", "https://huggingface.co/",
        ("models", "datasets", "agent tooling", "evaluation", "local models"),
        "Strong ecosystem signal; verify license, provenance and benchmark evidence.", 1,
    ),
    OSSSource(
        "Kaggle", "models_datasets_benchmarks", "https://www.kaggle.com/",
        ("models", "datasets", "benchmarks", "notebooks", "GPU experiments"),
        "Useful for reproducible experiments; community artifacts require vetting.", 2,
    ),
    OSSSource(
        "PyPI", "python_packages", "https://pypi.org/",
        ("Python libraries", "release metadata", "dependency discovery"),
        "Package metadata is useful evidence; source, maintainers and dependencies must be checked separately.", 1,
    ),
    OSSSource(
        "arXiv", "research", "https://arxiv.org/",
        ("reasoning", "agents", "memory", "inference", "optimization"),
        "Research discovery only; claims must be validated experimentally before engineering adoption.", 2,
    ),
    OSSSource(
        "OpenML", "datasets_benchmarks", "https://www.openml.org/",
        ("reproducible benchmarks", "datasets", "experiment comparison"),
        "Strong for comparable ML experiments; task relevance to PHOENIX must be established.", 2,
    ),
    OSSSource(
        "GitLab", "source_code_agents", "https://gitlab.com/",
        ("source code", "agents", "CI/CD", "automation"),
        "Evaluate project activity, maintainership, license and dependency risk.", 2,
    ),
    OSSSource(
        "npm", "javascript_packages", "https://www.npmjs.com/",
        ("web tooling", "MCP integrations", "JavaScript/TypeScript"),
        "Useful for interface and integration capabilities; dependency-chain review required.", 3,
    ),
    OSSSource(
        "Docker Hub", "runtime_images", "https://hub.docker.com/",
        ("service images", "runtime packaging", "self-hosted components"),
        "Image provenance, CVEs, base image, permissions and reproducibility require verification.", 3,
    ),
)


CURATED_CANDIDATES: tuple[OSSCandidate, ...] = (
    OSSCandidate("agent-evaluator", "PyPI", "agent evaluation and quality gates", "Monitoring/Intelligence", "https://pypi.org/project/agent-evaluator/"),
    OSSCandidate("memoryeval", "PyPI", "memory evaluation and regression testing", "Memory/Monitoring", "https://pypi.org/project/memoryeval/"),
    OSSCandidate("agentevals-cli", "PyPI", "trace-based agent evaluation without replay", "Monitoring", "https://pypi.org/project/agentevals-cli/"),
    OSSCandidate("AgenticLens", "PyPI", "local observability, evaluation and operational intelligence", "Monitoring", "https://pypi.org/project/agenticlens/"),
    OSSCandidate("agentic-memory-ai", "PyPI", "framework-agnostic memory with conflict detection", "Memory", "https://pypi.org/project/agentic-memory-ai/"),
    OSSCandidate("Hugging Face Agents", "Hugging Face", "agent access to models, datasets, Spaces and community tools", "Intelligence/Data", "https://huggingface.co/docs/hub/en/agents"),
)


def sources_by_priority(sources: Iterable[OSSSource] = SOURCE_REGISTRY) -> list[OSSSource]:
    return sorted(sources, key=lambda item: (item.priority, item.name))


def candidates_by_source(candidates: Iterable[OSSCandidate] = CURATED_CANDIDATES) -> dict[str, list[OSSCandidate]]:
    grouped: dict[str, list[OSSCandidate]] = {}
    for candidate in candidates:
        grouped.setdefault(candidate.source, []).append(candidate)
    return grouped
