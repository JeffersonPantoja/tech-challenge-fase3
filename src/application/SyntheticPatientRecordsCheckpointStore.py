from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.SyntheticPatientRecordsCheckpoint import SyntheticPatientRecordsCheckpoint


class SyntheticPatientRecordsCheckpointStore(ABC):
    @abstractmethod
    def load(self) -> SyntheticPatientRecordsCheckpoint:
        raise NotImplementedError

    @abstractmethod
    def save(self, checkpoint: SyntheticPatientRecordsCheckpoint) -> None:
        raise NotImplementedError
