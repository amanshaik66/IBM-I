"""Deterministic test double. Its output is never IBM i semantic evidence."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from behavior_lab.models import Authority, CommandResult, JobRef, Observation


class MockTransport:
    """In-memory adapter with irrevocably non-authoritative authority."""

    def __init__(self) -> None:
        self.connected = False
        self.commands: list[str] = []
        self.files: dict[str, bytes] = {}

    @property
    def authority(self) -> Authority:
        return Authority.NON_AUTHORITATIVE

    def connect(self) -> None:
        self.connected = True

    def close(self) -> None:
        self.connected = False

    def create_workspace(self, library: str, ifs_root: PurePosixPath) -> None:
        self.commands.append(f"CREATE {library} {ifs_root}")

    def cleanup_workspace(self, library: str, ifs_root: PurePosixPath) -> None:
        self.commands.append(f"CLEAN {library} {ifs_root}")

    def upload(self, local: Path, remote: PurePosixPath) -> str:
        self.files[str(remote)] = local.read_bytes()
        return "mock-upload-not-a-platform-hash"

    def inspect_filesystem(self, root: PurePosixPath) -> Observation:
        return Observation("filesystem", sorted(self.files))

    def execute_cl(self, command: str) -> CommandResult:
        return self._command(command)

    def compile(self, language: str, command: str) -> CommandResult:
        return self._command(f"{language}:{command}")

    def call_program(self, library: str, program: str, parameters: Sequence[str]) -> CommandResult:
        return self._command(f"CALL {library}/{program} {' '.join(parameters)}")

    def execute_sql(self, statement: str, parameters: Sequence[Any] = ()) -> Observation:
        return Observation(
            "sql", {"statement": statement, "parameters": list(parameters), "rows": []}
        )

    def capture_database_state(self, specification: dict[str, Any]) -> Observation:
        return Observation("database", specification)

    def submit(self, command: str) -> JobRef:
        self.commands.append(command)
        return JobRef("MOCKJOB", "MOCKUSER", "000001")

    def wait(self, job: JobRef, timeout_seconds: int) -> str:
        return "COMPLETED_MOCK"

    def job_log(self, job: JobRef) -> str:
        return "NON-AUTHORITATIVE MOCK JOB LOG"

    def messages(self, target: str) -> Observation:
        return Observation("messages", [])

    def objects(self, library: str) -> Observation:
        return Observation("objects", [])

    def locks(self, target: str) -> Observation:
        return Observation("locks", [])

    def data_queue(self, library: str, name: str) -> Observation:
        return Observation("data_queue", [])

    def message_queue(self, library: str, name: str) -> Observation:
        return Observation("message_queue", [])

    def spool(self, job: JobRef) -> Observation:
        return Observation("spool", [])

    def _command(self, command: str) -> CommandResult:
        self.commands.append(command)
        return CommandResult(command, 0, "MOCK ONLY — NOT IBM i OUTPUT")
