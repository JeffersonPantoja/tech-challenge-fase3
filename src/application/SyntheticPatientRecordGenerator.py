from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.QARecord import QARecord
from src.domain.SyntheticPatientRecord import SyntheticPatientRecord


class SyntheticPatientRecordGenerator(ABC):
    @abstractmethod
    def generate(self, record: QARecord) -> SyntheticPatientRecord:
        raise NotImplementedError

    @abstractmethod
    def generate_batch(self, records: list[QARecord]) -> list[SyntheticPatientRecord]:
        raise NotImplementedError
