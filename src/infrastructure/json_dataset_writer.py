from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from src.application.ports import QARecordWriter
from src.domain.qa_record import QARecord


class JsonDatasetWriter(QARecordWriter):
    def __init__(self, output_path: Path) -> None:
        self._output_path = output_path

    def write(self, records: Iterable[QARecord]) -> Path:
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        with self._output_path.open("w", encoding="utf-8") as file:
            file.write("[")
            first = True
            for record in records:
                item = {
                    "source": record.source,
                    "text": record.to_finetuning_text(),
                }
                if first:
                    file.write("\n")
                    first = False
                else:
                    file.write(",\n")
                json.dump(item, file, ensure_ascii=False, indent=2)
            if not first:
                file.write("\n")
            file.write("]")
        return self._output_path
