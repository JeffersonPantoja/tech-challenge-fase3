from __future__ import annotations

import argparse
from pathlib import Path

from src.application.BuildMedQaDatasetUseCase import BuildMedQaDatasetUseCase
from src.domain.CommandOptions import CommandOptions
from src.infrastructure.QARecordCurationService import QARecordCurationService
from src.infrastructure.JsonDatasetWriter import JsonDatasetWriter
from src.infrastructure.MedQaSourcesReader import MedQaSourcesReader


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
