from __future__ import annotations

import json
from pathlib import Path

from src.application.SyntheticPatientRecordsFailedCheckpointStore import SyntheticPatientRecordsFailedCheckpointStore
from src.domain.SyntheticPatientRecordsCheckpoint import SyntheticPatientRecordsCheckpoint


class JsonSyntheticPatientRecordsFailedCheckpointStore(SyntheticPatientRecordsFailedCheckpointStore):
    def __init__(self, checkpoint_path: Path) -> None:
        self._checkpoint_path = checkpoint_path

    def load(self) -> SyntheticPatientRecordsCheckpoint:
        if not self._checkpoint_path.exists():
            return SyntheticPatientRecordsCheckpoint()

        data = json.loads(self._checkpoint_path.read_text(encoding="utf-8"))
        return SyntheticPatientRecordsCheckpoint(failed_sources=set(data.get("failed_sources", [])))

    def save(self, checkpoint: SyntheticPatientRecordsCheckpoint) -> None:
        self._checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"failed_sources": sorted(checkpoint.failed_sources)}
        self._checkpoint_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
