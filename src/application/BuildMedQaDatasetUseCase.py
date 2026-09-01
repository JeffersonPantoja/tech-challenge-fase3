from __future__ import annotations

from src.application.ports import QARecordReader, QARecordWriter
from src.domain.BuildDatasetResult import BuildDatasetResult
from src.domain.CurationStats import CurationStats
from src.infrastructure.QARecordCurationService import QARecordCurationService


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
