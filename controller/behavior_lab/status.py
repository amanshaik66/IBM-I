"""Status transition guards."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast


class InvalidTransition(ValueError):
    pass


def load_machine(root: Path) -> dict[str, object]:
    return cast(dict[str, object], json.loads((root / "registry/status-machine.json").read_text()))


def validate_transition(
    machine: dict[str, object], current: str, target: str, *, authoritative_evidence: bool = False
) -> None:
    transitions = machine["transitions"]
    assert isinstance(transitions, dict)
    allowed = transitions.get(current, [])
    if target not in allowed:
        raise InvalidTransition(f"forbidden status transition: {current} -> {target}")
    evidence_states = machine["evidence_required_from"]
    assert isinstance(evidence_states, list)
    if target in evidence_states and not authoritative_evidence:
        raise InvalidTransition(f"{target} requires authoritative IBM i evidence")
