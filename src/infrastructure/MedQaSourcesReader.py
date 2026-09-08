from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from typing import Iterable

from src.application.ports import QARecordReader
from src.domain.QARecord import QARecord


class MedQaSourcesReader(QARecordReader):
    def __init__(self, resources_dir: Path) -> None:
        self._resources_dir = resources_dir

    def read(self) -> Iterable[QARecord]:
        yield from self._load_medquad()
        yield from self._load_pubmedqa()

    def _load_medquad(self) -> Iterable[QARecord]:
        medquad_dir = self._resources_dir / "MedQuAD"
        for source_path in medquad_dir.rglob("*.xml"):
            yield from self._parse_medquad_xml(source_path)

    def _parse_medquad_xml(self, path: Path) -> Iterable[QARecord]:
        root = ET.parse(path).getroot()
        focus = (root.findtext("Focus") or "").strip()
        relative_path = path.relative_to(self._resources_dir / "MedQuAD")
        for pair in root.findall(".//QAPair"):
            pid = (pair.get("pid") or "").strip()
            question = (pair.findtext("Question") or "").strip()
            answer = (pair.findtext("Answer") or "").strip()
            if question and answer:
                yield QARecord(
                    source=f"MedQuAD:{relative_path}:{pid or 'unknown'}",
                    question=question,
                    answer=answer,
                    context=focus
                )

    def _load_pubmedqa(self) -> Iterable[QARecord]:
        pubmedqa_dir = self._resources_dir / "pubmedqa"
        for json_file in pubmedqa_dir.glob("*.json"):
            data = json.loads(json_file.read_text(encoding="utf-8"))
            for doc_id, item in data.items():
                question = str(item.get("QUESTION", "")).strip()
                contexts = item.get("CONTEXTS", [])
                answer = self._select_pubmedqa_answer(item)
                if question and answer:
                    yield QARecord(
                        source=f"PubMedQA:{json_file.name}:{doc_id}",
                        question=question,
                        answer=answer,
                        context=" \n".join(contexts),
                    )

    def _select_pubmedqa_answer(self, item: dict[str, Any]) -> str:
        labels = item.get("LABELS", [])
        long_answer = str(item.get("LONG_ANSWER", "")).strip()
        if long_answer:
            return long_answer
        return "; ".join(labels)
