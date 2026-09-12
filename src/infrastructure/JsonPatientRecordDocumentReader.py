from __future__ import annotations

import json
from pathlib import Path

from src.application.PatientRecordDocumentReader import PatientRecordDocumentReader
from src.domain.PatientRecordDocument import PatientRecordDocument


class JsonPatientRecordDocumentReader(PatientRecordDocumentReader):
    def read(self, path: Path) -> list[PatientRecordDocument]:
        if not path.exists():
            raise FileNotFoundError(f"Arquivo de prontuários não encontrado: {path}")

        documents: list[PatientRecordDocument] = []
        seen_sources: set[str] = set()
        with path.open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                item = json.loads(line)
                source = str(item.get("source", "")).strip()
                if not source:
                    raise ValueError(f"Registro sem source na linha {line_number}")
                if source in seen_sources:
                    raise ValueError(f"Source duplicado na linha {line_number}: {source}")
                seen_sources.add(source)
                documents.append(
                    PatientRecordDocument(
                        source=source,
                        patient_id=str(item.get("patient_id", "")),
                        content=self._to_content(item),
                    )
                )
        return documents

    def _to_content(self, item: dict[str, object]) -> str:
        fields = (
            ("Patient ID", item.get("patient_id", "")),
            ("Chief complaint", item.get("chief_complaint", "")),
            ("History", item.get("history", "")),
            ("Medications", item.get("medications", "")),
            ("Vitals", item.get("vitals", "")),
            ("Assessment", item.get("assessment", "")),
        )
        return "\n".join(f"{label}: {value}" for label, value in fields)
