from pathlib import Path

import pytest

from behavior_lab.status import InvalidTransition, load_machine, validate_transition

ROOT = Path(__file__).parents[2]


def test_normal_offline_transition() -> None:
    validate_transition(load_machine(ROOT), "source_written", "statically_validated")


def test_skipping_to_verified_is_forbidden() -> None:
    with pytest.raises(InvalidTransition, match="forbidden"):
        validate_transition(
            load_machine(ROOT),
            "source_written",
            "behavior_verified_on_ibmi",
            authoritative_evidence=True,
        )


def test_compile_requires_authoritative_evidence() -> None:
    with pytest.raises(InvalidTransition, match="authoritative"):
        validate_transition(load_machine(ROOT), "statically_validated", "compiled_on_ibmi")
