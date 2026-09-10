from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from src.domain.PatientRecordDocument import PatientRecordDocument


class PatientRecordDocumentReader(ABC):
    @abstractmethod
    def read(self, path: Path) -> list[PatientRecordDocument]:
        raise NotImplementedError
