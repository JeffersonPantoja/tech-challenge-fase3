from __future__ import annotations

import argparse
from pathlib import Path

from src.application.BuildSyntheticPatientRecordsUseCase import BuildSyntheticPatientRecordsUseCase
from src.domain.CommandOptions import CommandOptions
from src.infrastructure.JsonSyntheticPatientRecordsFailedCheckpointStore import JsonSyntheticPatientRecordsFailedCheckpointStore
from src.infrastructure.JsonSyntheticPatientRecordsCheckpointStore import JsonSyntheticPatientRecordsCheckpointStore
from src.infrastructure.JsonSyntheticPatientRecordWriter import JsonSyntheticPatientRecordWriter
from src.infrastructure.MedQaSourcesReader import MedQaSourcesReader
from src.infrastructure.LlamaSyntheticPatientRecordGenerator import LlamaSyntheticPatientRecordGenerator
from src.infrastructure.OpenAISyntheticPatientRecordGenerator import OpenAISyntheticPatientRecordGenerator
from src.infrastructure.QARecordCurationService import QARecordCurationService


class SyntheticPatientRecordsController:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description="Gera prontuários sintéticos a partir de MedQuAD e PubMedQA.")
        self._parser.add_argument("--resources-dir", default="resources")
        self._parser.add_argument("--output", default="resources/patient_records.jsonl")
        self._parser.add_argument("--save-to-drive", action="store_true", default=False)
        self._parser.add_argument("--drive-dir", default="/content/drive/MyDrive/tech-challenge-fase-3")
        self._parser.add_argument("--checkpoint", default="resources/patient_records.checkpoint.json")
        self._parser.add_argument("--failed-checkpoint", default="resources/patient_records.failed.checkpoint.json")
        self._parser.add_argument("--resume", action="store_true", default=True)
        self._parser.add_argument("--no-resume", action="store_false", dest="resume")
        self._parser.add_argument("--batch-size", type=int, default=10)
        self._parser.add_argument("--num-batches", type=int, default=None)
        self._parser.add_argument("--openai-model", default="gpt-4o-mini")
        self._parser.add_argument("--backend", choices=["openai", "llama"], default="openai")
        self._parser.add_argument("--llama-model-path", default="/content/drive/MyDrive/tech-challenge-fase-3/llama-model")
        self._parser.add_argument("--llama-max-new-tokens", type=int, default=512)

    def run(self) -> None:
        args = self._parser.parse_args()
        output_path = Path(args.output)
        checkpoint_path = Path(args.checkpoint)
        failed_checkpoint_path = Path(args.failed_checkpoint)
        if args.save_to_drive:
            drive_dir = Path(args.drive_dir)
            output_path = drive_dir / output_path.name
            checkpoint_path = drive_dir / checkpoint_path.name
            failed_checkpoint_path = drive_dir / failed_checkpoint_path.name

        options = CommandOptions(resources_dir=Path(args.resources_dir), output_path=output_path)
        checkpoint_store = JsonSyntheticPatientRecordsCheckpointStore(checkpoint_path)
        failed_checkpoint_store = JsonSyntheticPatientRecordsFailedCheckpointStore(failed_checkpoint_path)

        reader = MedQaSourcesReader(options.resources_dir)
        if args.backend == "llama":
            generator = LlamaSyntheticPatientRecordGenerator(
                model_path=args.llama_model_path,
                max_new_tokens=args.llama_max_new_tokens,
            )
        else:
            generator = OpenAISyntheticPatientRecordGenerator(model=args.openai_model)
        writer = JsonSyntheticPatientRecordWriter(options.output_path)
        curation_service = QARecordCurationService()
        use_case = BuildSyntheticPatientRecordsUseCase(
            reader=reader,
            generator=generator,
            writer=writer,
            curation_service=curation_service,
            checkpoint_store=checkpoint_store,
            failed_checkpoint_store=failed_checkpoint_store,
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
