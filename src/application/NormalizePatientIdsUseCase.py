from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from src.application.SyntheticPatientRecordReader import SyntheticPatientRecordReader
from src.application.SyntheticPatientRecordWriter import SyntheticPatientRecordWriter
from src.domain.NormalizePatientIdsResult import NormalizePatientIdsResult


class NormalizePatientIdsUseCase:
    def __init__(
        self,
        reader: SyntheticPatientRecordReader,
        writer: SyntheticPatientRecordWriter,
    ) -> None:
        self._reader = reader
        self._writer = writer

    def execute(self, input_path: Path) -> NormalizePatientIdsResult:
        records = self._reader.read(input_path)
        normalized_records = [
            replace(record, patient_id=str(index))
            for index, record in enumerate(records, start=1)
        ]
        output_path = self._writer.write(normalized_records)
        return NormalizePatientIdsResult(
            records_count=len(normalized_records),
            output_path=output_path,
        )
