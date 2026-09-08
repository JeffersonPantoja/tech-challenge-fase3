from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from src.domain.SyntheticPatientRecord import SyntheticPatientRecord


class SyntheticPatientRecordWriter(ABC):
    @abstractmethod
    def write(self, records: Iterable[SyntheticPatientRecord]) -> Path:
        raise NotImplementedError

    @abstractmethod
    def append(self, record: SyntheticPatientRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def output_path(self) -> Path:
        raise NotImplementedError
