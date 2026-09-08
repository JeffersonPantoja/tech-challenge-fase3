from __future__ import annotations

from src.application.ports import QARecordReader
from src.application.SyntheticPatientRecordsCheckpointStore import SyntheticPatientRecordsCheckpointStore
from src.application.SyntheticPatientRecordGenerator import SyntheticPatientRecordGenerator
from src.application.SyntheticPatientRecordWriter import SyntheticPatientRecordWriter
from src.infrastructure.QARecordCurationService import QARecordCurationService
from src.domain.BuildDatasetResult import BuildDatasetResult
from src.domain.QARecord import QARecord
from src.domain.SyntheticPatientRecordsCheckpoint import SyntheticPatientRecordsCheckpoint


class BuildSyntheticPatientRecordsUseCase:
    _MAX_BATCH_RETRIES = 3

    def __init__(
        self,
        reader: QARecordReader,
        generator: SyntheticPatientRecordGenerator,
        writer: SyntheticPatientRecordWriter,
        curation_service: QARecordCurationService,
        checkpoint_store: SyntheticPatientRecordsCheckpointStore | None = None,
        resume: bool = False,
        batch_size: int = 10,
        num_batches: int | None = None,
    ) -> None:
        self._reader = reader
        self._generator = generator
        self._writer = writer
        self._curation_service = curation_service
        self._checkpoint_store = checkpoint_store
        self._resume = resume
        self._batch_size = max(1, batch_size)
        self._num_batches = num_batches if num_batches is None else max(1, num_batches)

    def execute(self) -> BuildDatasetResult:
        curated = self._curation_service.curate(self._reader.read())
        checkpoint = self._load_checkpoint()
        pending_records = [record for record in curated.records if record.source not in checkpoint.processed_sources]

        if not self._resume:
            checkpoint = SyntheticPatientRecordsCheckpoint()

        if not self._resume and self._writer.output_path().exists():
            self._writer.output_path().unlink()

        total = len(pending_records)
        batches = self._chunked(pending_records, self._batch_size)
        if self._num_batches is not None:
            batches = batches[: self._num_batches]

        for batch_index, batch in enumerate(batches, start=1):
            print(f"[T3] lote {batch_index} iniciando com {len(batch)} registros")
            synthetic_records = self._generate_batch_with_retry(batch_index, batch)
            if not synthetic_records:
                print(f"[T3] lote {batch_index} ignorado após {self._MAX_BATCH_RETRIES} tentativas")
                continue
            synthetic_by_source = {record.source: record for record in synthetic_records}

            for item_index, record in enumerate(batch, start=1):
                absolute_index = ((batch_index - 1) * self._batch_size) + item_index
                synthetic_record = synthetic_by_source[record.source]
                print(f"[T3] processando {absolute_index}/{total}: {record.source}")
                self._writer.append(synthetic_record)
                checkpoint.processed_sources.add(record.source)
                self._save_checkpoint(checkpoint)
            print(f"[T3] lote {batch_index} concluído")

        return BuildDatasetResult(
            records_count=sum(len(batch) for batch in batches),
            output_path=self._writer.output_path(),
            curation_stats=curated.stats,
        )

    def _load_checkpoint(self) -> SyntheticPatientRecordsCheckpoint:
        if self._checkpoint_store is None:
            return SyntheticPatientRecordsCheckpoint()
        return self._checkpoint_store.load()

    def _save_checkpoint(self, checkpoint: SyntheticPatientRecordsCheckpoint) -> None:
        if self._checkpoint_store is not None:
            self._checkpoint_store.save(checkpoint)

    def _chunked(self, records: list[QARecord], batch_size: int) -> list[list[QARecord]]:
        return [records[index : index + batch_size] for index in range(0, len(records), batch_size)]

    def _generate_batch_with_retry(self, batch_index: int, batch: list[QARecord]) -> list:
        last_error: Exception | None = None
        for attempt in range(1, self._MAX_BATCH_RETRIES + 1):
            try:
                if attempt > 1:
                    print(f"[T3] reprocessando lote {batch_index}, tentativa {attempt}/{self._MAX_BATCH_RETRIES}")
                return self._generator.generate_batch(batch)
            except ValueError as exc:
                last_error = exc
                print(f"[T3] validação do lote {batch_index} falhou: {exc}")
                if attempt == self._MAX_BATCH_RETRIES:
                    break

        if last_error is not None:
            print(f"[T3] lote {batch_index} descartado após {self._MAX_BATCH_RETRIES} tentativas")
        return []
