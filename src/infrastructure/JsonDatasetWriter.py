from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from src.application.ports import QARecordWriter
from src.domain.QARecord import QARecord


class JsonDatasetWriter(QARecordWriter):
    def __init__(self, output_path: Path) -> None:
        self._output_path = output_path

    def write(self, records: Iterable[QARecord]) -> Path:
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        with self._output_path.open("w", encoding="utf-8") as file:
            for record in records:
                item = {
                    "source": record.source,
                    "text": record.to_finetuning_text(),
                }
                file.write(json.dumps(item, ensure_ascii=False))
                file.write("\n")
        return self._output_path
