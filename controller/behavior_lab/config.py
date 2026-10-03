"""Environment loading after JSON Schema validation by the repository validator."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any

from behavior_lab.capabilities import Capability, CapabilityStatus
from behavior_lab.models import Authority, Environment, EnvironmentFingerprint


def _fingerprint(raw: dict[str, Any] | None) -> EnvironmentFingerprint | None:
    if raw is None:
        return None
    return EnvironmentFingerprint(
        raw["fingerprint_id"],
        raw["captured_at"],
        raw["ibmi_release"],
        raw["technology_refresh"],
        tuple(raw["ptf_groups"]),
        raw["partition"],
        raw["processor_architecture"],
        tuple(raw["licensed_products"]),
        raw["compilers"],
        raw["db2_level"],
        raw["sql_services"],
        raw["ccsid"],
        raw["locale"],
        raw["timezone"],
        raw["language_id"],
        raw["formats"],
        raw["system_values"],
        raw["job_attributes"],
        raw["user_profile"],
        tuple(raw["library_list"]),
        raw["work_management"],
        raw["capability_flags"],
    )


def load_environment(path: Path) -> Environment:
    raw = json.loads(path.read_text())
    workspace = raw["workspace"]
    capabilities = tuple(
        Capability(
            item["id"],
            CapabilityStatus(item["status"]),
            item["version"],
            tuple(item["configuration_required"]),
            item["attributes"],
        )
        for item in raw["capabilities"]
    )
    return Environment(
        raw["environment_id"],
        raw["kind"],
        raw["release_id"],
        Authority(raw["authority"]),
        workspace["library_prefix"],
        PurePosixPath(workspace["ifs_root"]),
        raw["capability_adapters"],
        tuple(raw["secret_refs"]),
        _fingerprint(raw["fingerprint"]),
        capabilities,
        tuple(raw["security_personas"]),
    )
