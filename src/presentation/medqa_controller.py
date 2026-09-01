from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from src.application.use_cases import BuildMedQaDatasetUseCase
from src.infrastructure.curation import QARecordCurationService
from src.infrastructure.json_dataset_writer import JsonDatasetWriter
from src.infrastructure.medqa_sources_reader import MedQaSourcesReader


@dataclass(frozen=True)
class CommandOptions:
    resources_dir: Path
    output_path: Path


class MedQaController:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description="Estrutura dados do MedQuAD e PubMedQA.")
        self._parser.add_argument("--resources-dir", default="resources")
        self._parser.add_argument("--output", default="resources/finetuning_qa.json")

    def run(self) -> None:
        args = self._parser.parse_args()
        options = CommandOptions(resources_dir=Path(args.resources_dir), output_path=Path(args.output))

        reader = MedQaSourcesReader(options.resources_dir)
        writer = JsonDatasetWriter(options.output_path)
        curation_service = QARecordCurationService()
        use_case = BuildMedQaDatasetUseCase(reader=reader, writer=writer, curation_service=curation_service)
        result = use_case.execute()

        print(f"Arquivos processados: {result.records_count}")
        print(f"Saída gerada em: {result.output_path}")
        print(
            "Curadoria: "
            f"vazios={result.curation_stats.discarded_empty_fields}, "
            f"duplicados={result.curation_stats.discarded_duplicates}, "
            f"muito_curto={result.curation_stats.discarded_too_short}"
        )
