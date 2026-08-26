from dataclasses import dataclass
from typing import Iterable, Set


@dataclass(frozen=True)
class Policy:
    name: str
    allowed_capabilities: Set[str]
    require_human_approval: bool = True


class Governance:
    """Central policy gate for module capabilities and sensitive actions."""

    def __init__(self, policies: Iterable[Policy] = ()) -> None:
        self._policies = {p.name: p for p in policies}

    def register(self, policy: Policy) -> None:
        self._policies[policy.name] = policy

    def authorize(self, policy_name: str, capability: str, human_approved: bool = False) -> bool:
        policy = self._policies[policy_name]
        if capability not in policy.allowed_capabilities:
            return False
        return not policy.require_human_approval or human_approved
