"""Minimal orchestration seam; real execution is intentionally deferred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from behavior_lab.models import Authority, Environment
from behavior_lab.transports.base import LifecycleTransport


@dataclass
class WorkspaceLease:
    library: str
    ifs_root: PurePosixPath


class BehaviorLabController:
    def __init__(self, environment: Environment, lifecycle: LifecycleTransport) -> None:
        if environment.kind == "mock" and lifecycle.authority is not Authority.NON_AUTHORITATIVE:
            raise ValueError("mock environment cannot use an authoritative adapter")
        self.environment = environment
        self.lifecycle = lifecycle

    def open_workspace(self, execution_suffix: str) -> WorkspaceLease:
        suffix = "".join(c for c in execution_suffix.upper() if c.isalnum())[:4]
        if not suffix:
            raise ValueError("execution suffix must contain an alphanumeric character")
        library = f"{self.environment.library_prefix}{suffix}"[:10]
        root = self.environment.ifs_root / suffix.lower()
        self.lifecycle.create_workspace(library, root)
        return WorkspaceLease(library, root)

    def cleanup(self, lease: WorkspaceLease) -> None:
        self.lifecycle.cleanup_workspace(lease.library, lease.ifs_root)
