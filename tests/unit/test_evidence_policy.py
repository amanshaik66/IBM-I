import pytest

from behavior_lab.evidence.policy import UntrustedEvidence, assert_authoritative


def test_mock_evidence_is_rejected_even_if_claimed_authoritative() -> None:
    evidence = {"authority": {"level": "authoritative"}, "environment": {"environment_id": "mock"}}
    environment = {"kind": "mock", "authority": "non_authoritative", "environment_id": "mock"}
    with pytest.raises(UntrustedEvidence, match="cannot produce"):
        assert_authoritative(evidence, environment)
