from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from src.domain.qa_record import QARecord


@dataclass(frozen=True)
class CurationStats:
    kept: int = 0
    discarded_empty_fields: int = 0
    discarded_duplicates: int = 0
    discarded_too_short: int = 0


@dataclass
class CurationResult:
    records: list[QARecord] = field(default_factory=list)
    stats: CurationStats = field(default_factory=CurationStats)


class QARecordCurationService:
    def curate(self, records: Iterable[QARecord]) -> CurationResult:
        curated: list[QARecord] = []
        seen: set[tuple[str, str, str]] = set()
        empty_fields = 0
        duplicates = 0
        too_short = 0

        for record in records:
            normalized = self._normalize(record)
            if not self._has_required_content(normalized):
                empty_fields += 1
                continue

            if self._is_too_short(normalized):
                too_short += 1
                continue

            signature = (normalized.question, normalized.answer, normalized.context)
            if signature in seen:
                duplicates += 1
                continue
            seen.add(signature)
            curated.append(normalized)

        return CurationResult(
            records=curated,
            stats=CurationStats(
                kept=len(curated),
                discarded_empty_fields=empty_fields,
                discarded_duplicates=duplicates,
                discarded_too_short=too_short,
            ),
        )

    def _normalize(self, record: QARecord) -> QARecord:
        return QARecord(
            source=record.source.strip(),
            question=self._normalize_text(record.question),
            answer=self._normalize_text(record.answer),
            context=self._normalize_text(record.context),
        )

    def _normalize_text(self, text: str) -> str:
        return " ".join(text.split()).strip()

    def _has_required_content(self, record: QARecord) -> bool:
        return bool(record.source and record.question and record.answer)

    def _is_too_short(self, record: QARecord) -> bool:
        return len(record.question) < 8 or len(record.answer) < 8
