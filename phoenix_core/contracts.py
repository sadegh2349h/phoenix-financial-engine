from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Event:
    event_type: str
    source: str
    payload: Dict[str, Any]
    created_at: str = field(default_factory=utc_now)
    correlation_id: Optional[str] = None


@dataclass(frozen=True)
class Task:
    task_id: str
    objective: str
    priority: int = 50
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class Decision:
    decision_id: str
    objective: str
    action: str
    confidence: float
    evidence: List[Dict[str, Any]]
    risks: List[str] = field(default_factory=list)
    requires_human_approval: bool = True
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class ModuleManifest:
    name: str
    version: str
    capabilities: List[str]
    enabled: bool = True
