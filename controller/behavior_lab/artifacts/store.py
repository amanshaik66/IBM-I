"""Content-addressed evidence artifact storage for local development."""

from __future__ import annotations

import hashlib
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO


@dataclass(frozen=True)
class ArtifactRef:
    artifact_type: str
    sha256: str
    media_type: str
    size_bytes: int
    logical_role: str
    storage_locator: str
    created_at: str
    execution_id: str


class LocalArtifactStore:
    """Write-once SHA-256 store; existing content is verified, never replaced."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def put(
        self,
        stream: BinaryIO,
        *,
        artifact_type: str,
        media_type: str,
        logical_role: str,
        execution_id: str,
    ) -> ArtifactRef:
        self.root.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256()
        size = 0
        with tempfile.NamedTemporaryFile(dir=self.root, delete=False) as temporary:
            temp_path = Path(temporary.name)
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
                size += len(chunk)
                temporary.write(chunk)
        value = digest.hexdigest()
        locator = f"sha256/{value[:2]}/{value}"
        target = self.root / locator
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if _hash_file(target) != value:
                temp_path.unlink()
                raise ValueError("content-address collision or corrupted artifact")
            temp_path.unlink()
        else:
            os.replace(temp_path, target)
            target.chmod(0o444)
        return ArtifactRef(
            artifact_type,
            value,
            media_type,
            size,
            logical_role,
            locator,
            datetime.now(timezone.utc).isoformat(),
            execution_id,
        )

    def open(self, sha256: str) -> BinaryIO:
        path = self.root / f"sha256/{sha256[:2]}/{sha256}"
        if _hash_file(path) != sha256:
            raise ValueError("artifact is missing or its content hash has changed")
        return path.open("rb")


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()
