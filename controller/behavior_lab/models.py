"""Strongly typed controller value objects; credentials are never stored here."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Any, Mapping

from behavior_lab.capabilities import Capability


class Authority(StrEnum):
    AUTHORITATIVE_CANDIDATE = "authoritative_candidate"
    NON_AUTHORITATIVE = "non_authoritative"


@dataclass(frozen=True)
class EnvironmentFingerprint:
    fingerprint_id: str
    captured_at: str
    ibmi_release: str | None
    technology_refresh: str | None
    ptf_groups: tuple[Mapping[str, object], ...]
    partition: Mapping[str, object]
    processor_architecture: str | None
    licensed_products: tuple[Mapping[str, object], ...]
    compilers: Mapping[str, object]
    db2_level: str | None
    sql_services: Mapping[str, object]
    ccsid: int | None
    locale: str | None
    timezone: str | None
    language_id: str | None
    formats: Mapping[str, object]
    system_values: Mapping[str, object]
    job_attributes: Mapping[str, object]
    user_profile: Mapping[str, object]
    library_list: tuple[str, ...]
    work_management: Mapping[str, object]
    capability_flags: Mapping[str, bool]


@dataclass(frozen=True)
class Environment:
    environment_id: str
    kind: str
    release_id: str | None
    authority: Authority
    library_prefix: str
    ifs_root: PurePosixPath
    capability_adapters: Mapping[str, str]
    secret_refs: tuple[str, ...] = ()
    fingerprint: EnvironmentFingerprint | None = None
    capabilities: tuple[Capability, ...] = ()
    security_personas: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.kind == "mock" and self.authority is not Authority.NON_AUTHORITATIVE:
            raise ValueError("mock environments must be non-authoritative")
        if not self.ifs_root.is_absolute():
            raise ValueError("IFS root must be absolute")


@dataclass(frozen=True)
class CommandResult:
    command: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class JobRef:
    name: str
    user: str
    number: str


@dataclass(frozen=True)
class Observation:
    category: str
    value: Any
