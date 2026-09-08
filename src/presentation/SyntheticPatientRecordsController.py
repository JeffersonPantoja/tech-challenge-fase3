from __future__ import annotations

import argparse
from pathlib import Path

from src.application.BuildSyntheticPatientRecordsUseCase import BuildSyntheticPatientRecordsUseCase
from src.domain.CommandOptions import CommandOptions
from src.infrastructure.JsonSyntheticPatientRecordsCheckpointStore import JsonSyntheticPatientRecordsCheckpointStore
from src.infrastructure.JsonSyntheticPatientRecordWriter import JsonSyntheticPatientRecordWriter
from src.infrastructure.MedQaSourcesReader import MedQaSourcesReader
from src.infrastructure.OpenAISyntheticPatientRecordGenerator import OpenAISyntheticPatientRecordGenerator
from src.infrastructure.QARecordCurationService import QARecordCurationService


class SyntheticPatientRecordsController:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description="Gera prontuários sintéticos a partir de MedQuAD e PubMedQA.")
        self._parser.add_argument("--resources-dir", default="resources")
        self._parser.add_argument("--output", default="resources/patient_records.jsonl")
        self._parser.add_argument("--checkpoint", default="resources/patient_records.checkpoint.json")
        self._parser.add_argument("--resume", action="store_true", default=True)
        self._parser.add_argument("--no-resume", action="store_false", dest="resume")
        self._parser.add_argument("--batch-size", type=int, default=10)
        self._parser.add_argument("--num-batches", type=int, default=None)
        self._parser.add_argument("--openai-model", default="gpt-4o-mini")

    def run(self) -> None:
        args = self._parser.parse_args()
        options = CommandOptions(resources_dir=Path(args.resources_dir), output_path=Path(args.output))
        checkpoint_store = JsonSyntheticPatientRecordsCheckpointStore(Path(args.checkpoint))

        reader = MedQaSourcesReader(options.resources_dir)
        generator = OpenAISyntheticPatientRecordGenerator(model=args.openai_model)
        writer = JsonSyntheticPatientRecordWriter(options.output_path)
        curation_service = QARecordCurationService()
        use_case = BuildSyntheticPatientRecordsUseCase(
            reader=reader,
            generator=generator,
            writer=writer,
            curation_service=curation_service,
            checkpoint_store=checkpoint_store,
            resume=args.resume,
            batch_size=args.batch_size,
            num_batches=args.num_batches,
        )
        result = use_case.execute()

        print(f"Registros processados: {result.records_count}")
        print(f"Saída gerada em: {result.output_path}")
        print(
            "Curadoria: "
            f"vazios={result.curation_stats.discarded_empty_fields}, "
            f"duplicados={result.curation_stats.discarded_duplicates}, "
            f"muito_curto={result.curation_stats.discarded_too_short}"
        )
