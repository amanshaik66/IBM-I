import pytest

from behavior_lab.validation import ValidationFailure, _assert_acyclic


def test_build_cycle_is_rejected() -> None:
    with pytest.raises(ValidationFailure, match="cycle"):
        _assert_acyclic({"a": ["b"], "b": ["a"]}, "test-build")


def test_unknown_build_prerequisite_is_rejected() -> None:
    with pytest.raises(ValidationFailure, match="unknown prerequisite"):
        _assert_acyclic({"a": ["missing"]}, "test-build")
