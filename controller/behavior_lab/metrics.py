"""Multi-dimensional coverage reporting without a misleading global percentage."""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable


def build_report(cases: Iterable[dict[str, Any]], releases: Iterable[str]) -> dict[str, Any]:
    records = list(cases)
    implementation = Counter(item["implementation_status"] for item in records)
    verification = Counter(item["verification_status"] for item in records)
    return {
        "total_specified_cases": len(records),
        "status_counts": {
            "written": implementation["source_written"],
            "statically_validated": implementation["statically_validated"],
            "ibmi_compiled": verification["compiled_on_ibmi"],
            "ibmi_executed": verification["executed_on_ibmi"],
            "behavior_verified": verification["behavior_verified_on_ibmi"],
            "integration_verified": verification["integration_verified"],
            "blocked": implementation["blocked"] + verification["blocked"],
            "requires_investigation": implementation["requires_investigation"]
            + verification["requires_investigation"],
        },
        "by_release": {
            release: sum(release in item["applicability"]["release_ids"] for item in records)
            for release in releases
        },
        "by_domain": dict(sorted(Counter(item["taxonomy"]["domain"] for item in records).items())),
        "by_case_kind": dict(sorted(Counter(item["case_kind"] for item in records).items())),
        "negative_cases": sum(bool(item["negative_dimensions"]) for item in records),
        "stale_evidence": 0,  # Requires baseline/evidence timestamps once packages exist.
        "lacking_authoritative_evidence": sum(not item["evidence_refs"] for item in records),
        "warning": "Counts are registry dimensions, not a percentage of IBM i functionality.",
    }
