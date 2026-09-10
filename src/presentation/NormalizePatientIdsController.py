from __future__ import annotations

import argparse
from pathlib import Path

from src.application.NormalizePatientIdsUseCase import NormalizePatientIdsUseCase
from src.infrastructure.JsonSyntheticPatientRecordReader import JsonSyntheticPatientRecordReader
from src.infrastructure.JsonSyntheticPatientRecordWriter import JsonSyntheticPatientRecordWriter


class NormalizePatientIdsController:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
            description="Substitui patient_id por identificadores sequenciais."
        )
        self._parser.add_argument("--input", default="resources/patient_records.jsonl")
        self._parser.add_argument(
            "--output",
            default="resources/patient_records_sequential.jsonl",
        )

    def run(self) -> None:
        args = self._parser.parse_args()
        use_case = NormalizePatientIdsUseCase(
            reader=JsonSyntheticPatientRecordReader(),
            writer=JsonSyntheticPatientRecordWriter(Path(args.output)),
        )
        result = use_case.execute(Path(args.input))

        print(f"Registros processados: {result.records_count}")
        print(f"Saída gerada em: {result.output_path}")
