"""Transport-neutral operation control, cancellation, retry, and recovery contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from behavior_lab.models import JobRef


class RetryClassification(StrEnum):
    NEVER = "never"
    TRANSIENT = "transient"
    IDEMPOTENT_ONLY = "idempotent_only"
    OPERATOR_REQUIRED = "operator_required"


@dataclass(frozen=True)
class RetryPolicy:
    maximum_attempts: int = 1
    initial_delay_seconds: float = 0
    maximum_delay_seconds: float = 0
    classification: RetryClassification = RetryClassification.NEVER

    def __post_init__(self) -> None:
        if self.maximum_attempts < 1:
            raise ValueError("maximum_attempts must be positive")


@dataclass(frozen=True)
class OperationControl:
    timeout_seconds: float
    cancellation_token: str
    retry: RetryPolicy = RetryPolicy()


class CancellationPort(Protocol):
    def cancel(self, token: str, reason: str) -> None: ...
    def is_cancelled(self, token: str) -> bool: ...


class RecoveryPort(Protocol):
    def detect_stuck_job(self, job: JobRef, threshold_seconds: int) -> bool: ...
    def detect_msgw(self, job: JobRef) -> bool: ...
    def find_orphans(self, lease_id: str) -> tuple[str, ...]: ...
    def cleanup_orphans(self, resource_ids: tuple[str, ...], control: OperationControl) -> None: ...
    def checkpoint(self, execution_id: str, phase: str) -> None: ...
    def recover_after_controller_crash(self, execution_id: str) -> str: ...
