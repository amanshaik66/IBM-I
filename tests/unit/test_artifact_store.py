from io import BytesIO
from pathlib import Path

import pytest

from behavior_lab.artifacts import LocalArtifactStore


def test_artifact_store_is_content_addressed_and_deduplicated(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path)
    first = store.put(
        BytesIO(b"job log"),
        artifact_type="job_log",
        media_type="text/plain",
        logical_role="execution log",
        execution_id="exec-1",
    )
    second = store.put(
        BytesIO(b"job log"),
        artifact_type="job_log",
        media_type="text/plain",
        logical_role="execution log",
        execution_id="exec-1",
    )
    assert first.sha256 == second.sha256
    assert first.storage_locator == second.storage_locator
    with store.open(first.sha256) as stream:
        assert stream.read() == b"job log"


def test_artifact_mutation_is_detected(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path)
    ref = store.put(
        BytesIO(b"original"),
        artifact_type="other",
        media_type="application/octet-stream",
        logical_role="test",
        execution_id="exec-1",
    )
    (tmp_path / ref.storage_locator).chmod(0o644)
    (tmp_path / ref.storage_locator).write_bytes(b"changed")
    with pytest.raises(ValueError, match="hash"):
        store.open(ref.sha256)
