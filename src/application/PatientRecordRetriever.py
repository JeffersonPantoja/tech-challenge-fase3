from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.PatientRecordDocument import PatientRecordDocument


class PatientRecordRetriever(ABC):
    @abstractmethod
    def retrieve(
        self,
        question: str,
        patient_id: str | None = None,
    ) -> list[PatientRecordDocument]:
        raise NotImplementedError
