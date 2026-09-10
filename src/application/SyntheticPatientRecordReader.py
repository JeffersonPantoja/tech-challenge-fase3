from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from src.domain.SyntheticPatientRecord import SyntheticPatientRecord


class SyntheticPatientRecordReader(ABC):
    @abstractmethod
    def read(self, path: Path) -> list[SyntheticPatientRecord]:
        raise NotImplementedError
