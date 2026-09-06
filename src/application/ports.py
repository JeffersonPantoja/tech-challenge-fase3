from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from src.domain.QARecord import QARecord
from src.domain.MedicalAssistantCommandOptions import MedicalAssistantCommandOptions
from src.domain.MedicalAssistantRuntime import MedicalAssistantRuntime


class QARecordReader(ABC):
    @abstractmethod
    def read(self) -> Iterable[QARecord]:
        raise NotImplementedError


class QARecordWriter(ABC):
    @abstractmethod
    def write(self, records: Iterable[QARecord]) -> Path:
        raise NotImplementedError


class MedicalAssistantRuntimeLoader(ABC):
    @abstractmethod
    def load(self, options: MedicalAssistantCommandOptions) -> MedicalAssistantRuntime:
        raise NotImplementedError


class MedicalAssistantResponseGenerator(ABC):
    @abstractmethod
    def generate(self, question: str) -> str:
        raise NotImplementedError
