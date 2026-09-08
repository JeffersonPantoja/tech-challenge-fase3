from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from src.application.SyntheticPatientRecordWriter import SyntheticPatientRecordWriter
from src.domain.SyntheticPatientRecord import SyntheticPatientRecord


class JsonSyntheticPatientRecordWriter(SyntheticPatientRecordWriter):
    def __init__(self, output_path: Path) -> None:
        self._output_path = output_path

    def write(self, records: Iterable[SyntheticPatientRecord]) -> Path:
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        with self._output_path.open("w", encoding="utf-8") as file:
            for record in records:
                file.write(self._serialize(record))
        return self._output_path

    def append(self, record: SyntheticPatientRecord) -> None:
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        with self._output_path.open("a", encoding="utf-8") as file:
            file.write(self._serialize(record))

    def output_path(self) -> Path:
        return self._output_path

    def _serialize(self, record: SyntheticPatientRecord) -> str:
        item = {
            "source": record.source,
            "patient_id": record.patient_id,
            "chief_complaint": record.chief_complaint,
            "history": record.history,
            "medications": record.medications,
            "vitals": record.vitals,
            "assessment": record.assessment,
            "plan": record.plan,
        }
        return json.dumps(item, ensure_ascii=False) + "\n"
