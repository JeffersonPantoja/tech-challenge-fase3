from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from src.domain.qa_record import QARecord


class QARecordReader(ABC):
    @abstractmethod
    def read(self) -> Iterable[QARecord]:
        raise NotImplementedError


class QARecordWriter(ABC):
    @abstractmethod
    def write(self, records: Iterable[QARecord]) -> Path:
        raise NotImplementedError
