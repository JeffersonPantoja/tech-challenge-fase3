from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from src.application.ports import QARecordReader, QARecordWriter
from src.domain.qa_record import QARecord


@dataclass(frozen=True)
class BuildDatasetResult:
    records_count: int
    output_path: Path


class BuildMedQaDatasetUseCase:
    def __init__(self, reader: QARecordReader, writer: QARecordWriter) -> None:
        self._reader = reader
        self._writer = writer

    def execute(self) -> BuildDatasetResult:
        records_count = 0

        def counting_records() -> Iterable[QARecord]:
            nonlocal records_count
            for record in self._reader.read():
                records_count += 1
                yield record

        output_path = self._writer.write(counting_records())
        return BuildDatasetResult(records_count=records_count, output_path=output_path)
