"""Authority and immutability checks separate controller tests from IBM i evidence."""

from __future__ import annotations

import hashlib
import json
from typing import Any


class UntrustedEvidence(ValueError):
    pass


def canonical_sha256(document: dict[str, Any], *, exclude: tuple[str, ...] = ()) -> str:
    content = {key: value for key, value in document.items() if key not in exclude}
    encoded = json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def assert_authoritative(evidence: dict[str, Any], environment: dict[str, Any]) -> None:
    authority = evidence.get("authority", {})
    if (
        environment.get("kind") == "mock"
        or environment.get("authority") != "authoritative_candidate"
    ):
        raise UntrustedEvidence(
            "mock/non-authoritative environment cannot produce trusted evidence"
        )
    if authority.get("level") != "authoritative":
        raise UntrustedEvidence("evidence is explicitly non-authoritative")
    if evidence.get("environment", {}).get("environment_id") != environment.get("environment_id"):
        raise UntrustedEvidence("evidence environment does not match registration")
    fingerprint = evidence.get("environment", {}).get("fingerprint")
    if not fingerprint:
        raise UntrustedEvidence("authoritative evidence requires an environment fingerprint")
    claimed_fingerprint = evidence["environment"].get("fingerprint_sha256")
    if canonical_sha256(fingerprint) != claimed_fingerprint:
        raise UntrustedEvidence("environment fingerprint hash does not match")
    claimed_evidence = evidence.get("evidence_sha256")
    if canonical_sha256(evidence, exclude=("evidence_sha256",)) != claimed_evidence:
        raise UntrustedEvidence("evidence content hash does not match")
