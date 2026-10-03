"""Capability discovery records and side-effect-free scheduling decisions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping, Sequence


class CapabilityStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"
    REQUIRES_CONFIGURATION = "requires_configuration"


class SchedulingDisposition(StrEnum):
    RUNNABLE = "runnable"
    UNAVAILABLE = "unavailable"
    BLOCKED = "blocked"
    REQUIRES_CONFIGURATION = "requires_configuration"


@dataclass(frozen=True)
class Capability:
    capability_id: str
    status: CapabilityStatus
    version: str | None = None
    configuration_required: tuple[str, ...] = ()
    attributes: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class CapabilityRequirement:
    capability_id: str
    minimum_version: str | None = None
    required_configuration: tuple[str, ...] = ()


@dataclass(frozen=True)
class SchedulingDecision:
    disposition: SchedulingDisposition
    reasons: tuple[str, ...]


def evaluate_capabilities(
    requirements: Sequence[CapabilityRequirement], discovered: Sequence[Capability]
) -> SchedulingDecision:
    """Classify feasibility; this is never a semantic PASS/FAIL result."""
    available = {item.capability_id: item for item in discovered}
    reasons: list[str] = []
    outcome = SchedulingDisposition.RUNNABLE
    precedence = {
        SchedulingDisposition.RUNNABLE: 0,
        SchedulingDisposition.REQUIRES_CONFIGURATION: 1,
        SchedulingDisposition.UNAVAILABLE: 2,
        SchedulingDisposition.BLOCKED: 3,
    }

    def raise_to(candidate: SchedulingDisposition) -> None:
        nonlocal outcome
        if precedence[candidate] > precedence[outcome]:
            outcome = candidate

    for requirement in requirements:
        actual = available.get(requirement.capability_id)
        if actual is None or actual.status is CapabilityStatus.UNKNOWN:
            raise_to(SchedulingDisposition.BLOCKED)
            reasons.append(f"{requirement.capability_id}: discovery incomplete")
        elif actual.status is CapabilityStatus.UNAVAILABLE:
            raise_to(SchedulingDisposition.UNAVAILABLE)
            reasons.append(f"{requirement.capability_id}: unavailable")
        elif actual.status is CapabilityStatus.REQUIRES_CONFIGURATION:
            raise_to(SchedulingDisposition.REQUIRES_CONFIGURATION)
            reasons.append(f"{requirement.capability_id}: configuration required")
        elif requirement.required_configuration and actual.configuration_required:
            raise_to(SchedulingDisposition.REQUIRES_CONFIGURATION)
            reasons.append(f"{requirement.capability_id}: required settings are not ready")
        # Version ordering is adapter/domain-specific. A declared minimum without a
        # discovered version is blocked rather than guessed or lexically compared.
        if requirement.minimum_version and (actual is None or actual.version is None):
            raise_to(SchedulingDisposition.BLOCKED)
            reasons.append(f"{requirement.capability_id}: version is unknown")
    return SchedulingDecision(outcome, tuple(reasons))
