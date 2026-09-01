from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.application.ports import QARecordReader, QARecordWriter
from src.infrastructure.curation import CurationStats, QARecordCurationService
from src.domain.qa_record import QARecord


@dataclass(frozen=True)
class BuildDatasetResult:
    records_count: int
    output_path: Path
    curation_stats: CurationStats


class BuildMedQaDatasetUseCase:
    def __init__(self, reader: QARecordReader, writer: QARecordWriter, curation_service: QARecordCurationService) -> None:
        self._reader = reader
        self._writer = writer
        self._curation_service = curation_service

    def execute(self) -> BuildDatasetResult:
        curated = self._curation_service.curate(self._reader.read())
        output_path = self._writer.write(curated.records)
        return BuildDatasetResult(
            records_count=curated.stats.kept,
            output_path=output_path,
            curation_stats=curated.stats,
        )
