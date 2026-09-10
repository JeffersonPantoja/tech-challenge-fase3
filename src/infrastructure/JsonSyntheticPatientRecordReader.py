from __future__ import annotations

import json
from pathlib import Path

from src.application.SyntheticPatientRecordReader import SyntheticPatientRecordReader
from src.domain.SyntheticPatientRecord import SyntheticPatientRecord


class JsonSyntheticPatientRecordReader(SyntheticPatientRecordReader):
    def read(self, path: Path) -> list[SyntheticPatientRecord]:
        if not path.exists():
            raise FileNotFoundError(f"Arquivo de prontuários não encontrado: {path}")

        records: list[SyntheticPatientRecord] = []
        with path.open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                item = json.loads(line)
                source = str(item.get("source", "")).strip()
                if not source:
                    raise ValueError(f"Registro sem source na linha {line_number}")
                records.append(
                    SyntheticPatientRecord(
                        source=source,
                        patient_id=str(item.get("patient_id", "")),
                        chief_complaint=str(item.get("chief_complaint", "")),
                        history=str(item.get("history", "")),
                        medications=str(item.get("medications", "")),
                        vitals=str(item.get("vitals", "")),
                        assessment=str(item.get("assessment", "")),
                        plan=str(item.get("plan", "")),
                    )
                )
        return records
